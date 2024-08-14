# libraries
import os
from typing_extensions import Self
from typing import Optional
from datetime import datetime
import pandas as pd
import xarray as xr


class TimeHandler:

    time_data_src_grid, time_data_src_point = None, None
    time_data_dst_grid, time_data_dst_point = None, None
    time_data_state_grid, time_data_state_point = None, None
    time_data_restart_grid, time_data_restart_point = None, None

    def __init__(self, time_run: pd.Timestamp,
                 time_format: str = '%Y%m%d%H%M', time_period: int = 0, time_frequency: str = 'H',
                 dt_run: int = 3600,
                 dt_data_src_grid: int = 3600, dt_data_src_point: int = 3600,
                 dt_data_dst_grid: int = 3600, dt_data_dst_point: int = 3600,
                 dt_data_state_grid: int = 3600, dt_data_state_point: int = 3600,
                 dt_data_restart_grid: int = 3600, dt_data_restart_point: int = 3600,
                 ) -> None:

        self.time_run = time_run
        self.time_format = time_format
        self.time_period = time_period
        self.time_frequency = time_frequency

        self.time_run = self.time_run.floor(self.time_frequency)

        self.dt_run = dt_run
        self.dt_data_src_grid = dt_data_src_grid
        self.dt_data_src_point = dt_data_src_point
        self.dt_data_dst_grid = dt_data_dst_grid
        self.dt_data_dst_point = dt_data_dst_point

        self.dt_data_restart_grid = dt_data_restart_grid
        self.dt_data_restart_point = dt_data_restart_point
        self.dt_data_state_grid = dt_data_state_grid
        self.dt_data_state_grid = dt_data_state_point

        self.time_data_src_grid = self.time_run
        self.time_data_src_point = self.time_run
        self.time_data_dst_grid = self.get_next_time(self.time_run, self.dt_data_src_grid)
        self.time_data_dst_point = self.get_next_time(self.time_run, self.dt_data_src_point)
        self.time_data_state_grid = self.get_next_time(self.time_run, self.dt_data_dst_grid)
        self.time_data_state_point = self.get_next_time(self.time_run, self.dt_data_dst_point)
        self.time_data_restart_grid = self.get_previous_time(self.time_run, self.dt_data_restart_grid)
        self.time_data_restart_point = self.get_previous_time(self.time_run, self.dt_data_restart_point)

    @classmethod
    def from_time_string(cls, time_run: str,
                         time_format: str = '%Y%m%d%H%M', time_period: int = 0, time_frequency: str = 'H') \
            -> Self:

        time_run = cls.convert_time_string_to_stamp(time_string=time_run)
        time_run = time_run.floor(time_frequency)

        return cls(time_run, time_format, time_period, time_frequency)

    @classmethod
    def from_time_period(cls, time_start: str, time_end: str,
                         time_format: str = '%Y%m%d%H%M', time_frequency: str = 'H') \
            -> Self:

        if time_start is not None and time_end is not None:
            time_start, time_end = pd.Timestamp(time_start), pd.Timestamp(time_end)
            time_start, time_end = time_start.floor(time_frequency), time_end.floor(time_frequency)
            time_range = pd.date_range(start=time_start, end=time_end, freq=time_frequency)
            time_period = len(time_range)
        else:
            raise ValueError(f"Invalid time period: {time_start} - {time_end}")

        return cls(time_start, time_format, time_period, time_frequency)

    @staticmethod
    def convert_time_string_to_stamp(time_string: str = None) -> pd.Timestamp:
        """
        Convert time string to timestamp.
        """
        if time_string is not None:
            time_stamp = pd.Timestamp(time_string)
        else:
            raise ValueError(f"Invalid time string: {time_string}")
        return time_stamp

    def get_times(self) -> pd.DatetimeIndex:
        """
        Get the times for a given time.
        """

        time_range = pd.date_range(start=self.time_run, periods=self.time_period, freq=self.time_frequency)

        return time_range

    # method to get previous time
    @staticmethod
    def get_previous_time(time_step: pd.Timestamp, time_seconds: int = 0) -> pd.Timestamp:
        """
        Get the previous time.
        :param time_step: current time stamp
        :param time_seconds: time delta in seconds
        :return: previous time stamp
        """
        return time_step - pd.Timedelta(seconds=time_seconds)

    # method to get next time
    @staticmethod
    def get_next_time(time_step: pd.Timestamp, time_seconds: int = 0) -> pd.Timestamp:
        """
        Get the next time.
        :param time_step: current time stamp
        :param time_seconds: time delta in seconds
        :return: next time stamp
        """
        return time_step + pd.Timedelta(seconds=time_seconds)

    def select_times_by_step(self, time_range: pd.date_range,
                             time_step: int = 0, time_unit='H') -> pd.date_range:
        """
        Select times for a given time step.
        """

        if time_unit == 'H':
            time_range = time_range[time_range.hour == time_step]
        elif time_unit == 'D':
            time_range = time_range[time_range.day == time_step]
        elif time_unit == 'M':
            time_range = time_range[time_range.month == time_step]
        else:
            raise ValueError(f"Invalid time unit: {time_unit}")

        return time_range

    def error_times(self):
        """
        Error times.
        """
        raise NotImplementedError

    def check_times(self):
        """
        Check times.
        """
        raise NotImplementedError

