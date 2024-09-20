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
                 file_format: Optional[str] = None) -> None:
        super().__init__(folder_name, file_name, file_format)

    def from_path(self, path_name: str,
                  file_time: Optional[pd.Timestamp] = None, file_format: Optional[str] = None):
        folder_name, file_name = os.path.split(path_name)
        return super().__init__(folder_name, file_name, file_format)


# class to handle information
class InfoHandler(ZipWrapper, IOWrapper):

    buffer_class = {}
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
            super().from_path(path_name=self.file_name_uncompress, file_format=self.file_type)
        else:
            super().from_path(path_name=self.file_name_compress, file_format=self.file_type)

        self.tc_thr = 840
        self.tc_max = tc_max

        self.dt_data_src = dt_data_src
        self.dt_model = dt_model

    @classmethod
    def get_data_dims_by_file(cls,
                          folder_name: str, file_name: str = '{domain_name}.dem.txt',
                          file_time: pd.Timestamp = None,
                          file_mandatory: bool = True, file_type: str = 'raster',
                          file_tags_definitions: dict = None, file_tags_pattern: dict = None):

        if file_tags_pattern is None:
            file_tags_pattern = {}
        if file_tags_definitions is None:
            file_tags_definitions = {}

        folder_name = substitute_string_by_date(folder_name, file_time, file_tags_pattern)
        file_name = substitute_string_by_date(file_name, file_time, file_tags_pattern)

        folder_name = substitute_string_by_tags(folder_name, file_tags_definitions)
        file_name = substitute_string_by_tags(file_name, file_tags_definitions)

        if not os.path.exists(os.path.join(folder_name, file_name)):
            if file_mandatory:
                raise FileNotFoundError(f'File {file_name} does not exist in path {folder_name}.')

        obj_class = cls(folder_name, file_name, file_mandatory, file_type)
        obj_data = obj_class.get_file_info()

        attrs_data = obj_data.attrs

        geo_x = obj_data['longitude'].values
        if geo_x.shape.__len__() == 2:
            geo_x = geo_x[0, :]
        geo_y = obj_data['latitude'].values
        if geo_y.shape.__len__() == 2:
            geo_y = geo_y[:, 0]

        attrs_data['cols'] = geo_x.shape[0]
        attrs_data['rows'] = geo_y.shape[0]

        return attrs_data

    @classmethod
    def get_data_dims_by_template(cls,
                                  folder_name: str,
                                  file_time: pd.Timestamp = None,
                                  file_tags_definitions: dict = None, file_tags_pattern: dict = None,
                                  file_template: dict = None):

        folder_name = substitute_string_by_date(folder_name, file_time, file_tags_pattern)

        attrs_data = {}
        for file_tag, file_settings in file_template.items():

            file_mandatory = file_settings['file_mandatory']
            file_name = file_settings['file_name']
            file_type = file_settings['file_type']

            file_name = substitute_string_by_tags(file_name, file_tags_definitions)

            class_obj = cls(folder_name, file_name, file_mandatory, file_type)
            attrs_dims = class_obj.get_file_info()[1]

            attrs_data = {**attrs_data, **attrs_dims}

        return attrs_data

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

    @classmethod
    def get_time_dims_by_file(cls,
                          folder_name: str, file_name: str = '{domain_name}.dem.txt',
                          file_time: pd.Timestamp = None,
                          file_mandatory: bool = True, file_type: str = 'raster',
                          file_tags_definitions: dict = None, file_tags_pattern: dict = None,
                          time_period_sim: int = 24, time_deep_shift: int = 2):

        if file_tags_pattern is None:
            file_tags_pattern = {}
        if file_tags_definitions is None:
            file_tags_definitions = {}

        folder_name = substitute_string_by_date(folder_name, file_time, file_tags_pattern)
        file_name = substitute_string_by_date(file_name, file_time, file_tags_pattern)

        folder_name = substitute_string_by_tags(folder_name, file_tags_definitions)
        file_name = substitute_string_by_tags(file_name, file_tags_definitions)

        if not os.path.exists(os.path.join(folder_name, file_name)):
            if file_mandatory:
                raise FileNotFoundError(f'File {file_name} does not exist in path {folder_name}.')

        obj_class = cls(folder_name, file_name, file_mandatory, file_type)
        attrs_data = obj_class.get_time_info(time_period_sim=time_period_sim, time_deep_shift=time_deep_shift)

        return attrs_data

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
        time_attrs = {
            'time_period_sim': time_period_sim,
            'time_period_extra': time_period_extra,
            'time_steps_day': time_steps_day,
            'time_steps_marked': time_steps_marked,
            'tc_sim': tc_sim}

        return time_attrs
