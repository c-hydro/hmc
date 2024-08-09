import os
from typing import Optional
from datetime import datetime
import pandas as pd
import xarray as xr


class TimeHandler:

    def __init__(self, time_run: pd.Timestamp,
                 time_format: str = '%Y%m%d%H%M', time_period: int = 0, time_frequency: str = 'H') -> None:

        self.time_run = time_run
        self.time_format = time_format
        self.time_period = time_period
        self.time_frequency = time_frequency

        self.time_run = self.time_run.floor(self.time_frequency)

    @classmethod
    def from_time_string(cls, time_run: str,
                         time_format: str = '%Y%m%d%H%M', time_period: int = 0, time_frequency: str = 'H') \
            -> pd.DatetimeIndex:

        time_run = cls.convert_time_string_to_stamp(time_string=time_run)
        time_run = time_run.floor(time_frequency)

        return cls(time_run, time_format, time_period, time_frequency)

    @classmethod
    def from_time_period(cls, time_start: str, time_end: str,
                         time_format: str = '%Y%m%d%H%M', time_frequency: str = 'H') \
            -> pd.DatetimeIndex:

        time_start, time_end = pd.Timestamp(time_start), pd.Timestamp(time_end)
        time_start, time_end = time_start.floor(time_frequency), time_end.floor(time_frequency)
        time_range = pd.date_range(start=time_start, end=time_end, freq=time_frequency)

        time_period = len(time_range)

        return cls(time_start, time_format, time_period, time_frequency)

    @staticmethod
    def convert_time_string_to_stamp(time_string: str = None) -> pd.Timestamp:
        """
        Convert time string to timestamp.
        """

        time_stamp = pd.Timestamp(time_string)

        return time_stamp

    def get_times(self) -> pd.DatetimeIndex:
        """
        Get the times for a given time.
        """

        time_range = pd.date_range(start=self.time_run, periods=self.time_period, freq=self.time_frequency)

        return time_range

    @staticmethod
    def get_previous_time(time_step: pd.Timestamp, time_seconds: int = 0) -> pd.Timestamp:
        return time_step - pd.Timedelta(seconds=time_seconds)

    @staticmethod
    def get_next_time(time_step: pd.Timestamp, time_seconds: int = 0) -> pd.Timestamp:
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

