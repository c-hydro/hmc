# libraries
import os
import numpy as np
import xarray as xr
import pandas as pd
from typing import Optional

from hmc.generic_toolkit.data.lib_io_utils import substitute_string_by_date, substitute_string_by_tags
from hmc.generic_toolkit.data.io_handler_base import IOHandler
from hmc.generic_toolkit.data.zip_handler_base import ZipHandler

from hmc.hydrological_toolkit.geo.lib_geo_area_cell import compute_info


# class to wrap zip class
class ZipWrapper(ZipHandler):
    def __init__(self, file_name_compress: str, file_name_uncompress: str = None,
                 zip_extension: str = '.gz') -> None:
        super().__init__(file_name_compress, file_name_uncompress, zip_extension)


# class to wrap io class
class IOWrapper(IOHandler):
    def __init__(self, folder_name: str, file_name: str,
                 file_format: Optional[None] = None) -> None:
        super().__init__(folder_name, file_name, file_format)

    def from_path(self, path: str, time: Optional[pd.Timestamp] = None, format: Optional[None] = None):
        path, file = os.path.split(path)
        return super().__init__(path, file, format)


# class to handle information
class InfoHandler(ZipWrapper, IOWrapper):

    type_class = 'info_base'

    def __init__(self, folder_name: str, file_name: str,
                 file_mandatory: bool = True, file_type: str = 'raster',
                 tc_max: int = 10,
                 dt_data_src: int = 3600, dt_model: int = 3600) -> None:

        self.folder_name = folder_name
        self.file_name = file_name
        self.file_mandatory = file_mandatory
        self.file_type = file_type

        super().__init__(file_name_compress=os.path.join(folder_name, file_name), file_name_uncompress=None,
                         zip_extension='.gz')

        if self.zip_check:
            super().from_path(self.file_name_uncompress)
        else:
            super().from_path(self.file_name_compress)

        self.tc_thr = 840
        self.tc_max = tc_max

        self.dt_data_src = dt_data_src
        self.dt_model = dt_model

    @classmethod
    def organize_file_obj(cls,
                          folder_name: str, file_name: str = '{domain_name}.dem.txt',
                          file_time: pd.Timestamp = None,
                          file_mandatory: bool = True, file_type: str = 'raster',
                          file_tags: dict = None, file_template: dict = None):

        if file_template is None:
            file_template = {}
        if file_tags is None:
            file_tags = {}

        folder_name = substitute_string_by_date(folder_name, file_time, file_template)
        file_name = substitute_string_by_date(file_name, file_time, file_template)

        folder_name = substitute_string_by_tags(folder_name, file_tags)
        file_name = substitute_string_by_tags(file_name, file_tags)

        if not os.path.exists(os.path.join(folder_name, file_name)):
            raise FileNotFoundError(f'File {file_name} does not exist in path {folder_name}.')

        return cls(folder_name, file_name, file_mandatory, file_type)

    # method to get file information
    def get_file_info(self):

        # organize file data
        check_data = self.uncompress_file_name()
        if check_data is not None:
            file_data = self.get_data(
                row_start=None, row_end=None, col_start=None, col_end=None, mandatory=self.file_mandatory)
        else:
            file_data = self.get_data(
                row_start=None, row_end=None, col_start=None, col_end=None, mandatory=self.file_mandatory)

        return file_data

    # method to get time information
    def get_time_info(self, time_period_sim: int, time_deep_shift: int = 2) -> dict:

        # get file data
        file_data = self.get_data(
            row_start=None, row_end=None, col_start=None, col_end=None, mandatory=True)

        # compute cell area info
        area, pixels, dx, dy = compute_info(file_data)

        # compute corrivation time [hour]
        tc_sim = int(0.27 * np.sqrt(0.6 * area) + 0.25)
        if tc_sim > self.tc_thr:
            tc_sim = self.tc_thr
        if tc_sim > self.tc_max:
            tc_sim = self.tc_max

        # compute extra time
        time_period_extra = time_period_sim + tc_sim

        # compute time day steps
        time_steps_day = int(24 * 3600 / self.dt_data_src)
        # compute time marked steps
        time_steps_marked = int(time_deep_shift * (3600 / self.dt_data_src) + 1)

        # organize time data
        time_data = {
            'time_period_sim': time_period_sim,
            'time_period_extra': time_period_extra,
            'time_steps_day': time_steps_day,
            'time_steps_marked': time_steps_marked,
            'tc_sim': tc_sim}

        return time_data
