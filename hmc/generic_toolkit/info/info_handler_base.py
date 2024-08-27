# libraries
import os
import xarray as xr
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
    def __init__(self, folder_name: str, file_name: str,
                 file_format: Optional[None] = None) -> None:
        super().__init__(folder_name, file_name, file_format)

    def from_path(self, path: str, time: Optional[pd.Timestamp] = None, format: Optional[None] = None):
        path, file = os.path.split(path)
        return super().__init__(path, file, format)


class InfoHandler(ZipWrapper, IOWrapper):

    type_class = 'info_base'

    def __init__(self, folder_name: str, file_name: str,
                 file_mandatory: bool = True, file_type: str = 'raster') -> None:

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

    def get_file_info(self):

        check_data = self.uncompress_file_name()
        if check_data is not None:
            file_data = self.get_data(
                row_start=None, row_end=None, col_start=None, col_end=None, mandatory=self.file_mandatory)
        else:
            file_data = self.get_data(
                row_start=None, row_end=None, col_start=None, col_end=None, mandatory=self.file_mandatory)

        return file_data
