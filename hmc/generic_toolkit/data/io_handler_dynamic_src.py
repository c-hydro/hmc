# libraries
import os
import pandas as pd
from typing import Optional

from hmc.generic_toolkit.data.lib_io_utils import substitute_string_by_date, substitute_string_by_tags
from hmc.generic_toolkit.data.io_handler_base import IOHandler
from hmc.generic_toolkit.data.zip_handler_base import ZipHandler


class ZipWrapper(ZipHandler):
    def __init__(self, file_name_compress: str, file_name_uncompress: str = None,
                 zip_extension: str = '.gz') -> None:
        super().__init__(file_name_compress, file_name_uncompress, zip_extension)


class IOWrapper(IOHandler):
    def __init__(self, folder_name: str, file_name: str, file_format: Optional[str] = None, **kwargs) -> None:
        super().__init__(folder_name, file_name, file_format, **kwargs)

    def from_path(self, file_path: str, file_format: Optional[str] = None, **kwargs):
        folder_name, file_name = os.path.split(file_path)
        return super().__init__(folder_name, file_name, file_format, **kwargs)


class DynamicSrcHandler(ZipWrapper, IOWrapper):

    type_class = 'io_dynamic_src'

    def __init__(self, folder_name: str, file_name: str,
                 vars_list: list = None, vars_mapping: dict = None) -> None:

        self.folder_name = folder_name
        self.file_name = file_name
        self.vars_list = vars_list
        self.vars_mapping = vars_mapping

        extra_args = {'vars_list': self.vars_list, 'vars_mapping': self.vars_mapping}

        super().__init__(file_name_compress=os.path.join(folder_name, file_name), file_name_uncompress=None,
                         zip_extension='.gz')

        if self.zip_check:
            super().from_path(self.file_name_uncompress, **extra_args)
        else:
            super().from_path(self.file_name_compress, **extra_args)

    @classmethod
    def organize_file_data(cls, folder_name: str, file_name: str = 'hmc.forcing-grid.{datetime_dynamic_src_grid}.nc.gz',
                           file_time: pd.Timestamp = None,
                           file_tags: dict = None,
                           file_mandatory: bool = True, file_template: dict = None,
                           file_vars_list: dict = None, file_vars_mapping: dict = None):

        if file_tags is None:
            file_tags = {}
        if file_template is None:
            file_template = {}
        if file_vars_list is None:
            file_vars_list = {}
        if file_vars_mapping is None:
            file_vars_mapping = {}

        folder_name = substitute_string_by_tags(folder_name, file_tags)
        folder_name = substitute_string_by_date(folder_name, file_time, file_template)
        file_name = substitute_string_by_tags(file_name, file_tags)
        file_name = substitute_string_by_date(file_name, file_time, file_template)

        if file_mandatory:
            if not os.path.exists(os.path.join(folder_name, file_name)):
                raise FileNotFoundError(f'File {file_name} does not exist in path {folder_name}.')

        return cls(folder_name, file_name, vars_list=file_vars_list, vars_mapping=file_vars_mapping)

    def get_file_data(self):

        check_data = self.uncompress_file_name()
        if check_data is not None:
            file_data = self.get_data(
                row_start=None, row_end=None, col_start=None, col_end=None, mandatory=True)
        else:
            file_data = self.get_data(
                row_start=None, row_end=None, col_start=None, col_end=None, mandatory=True)

        file_data = self.filter_data(file_data)
        file_data = self.map_data(file_data)

        return file_data


