# libraries
import os
import xarray as xr
import pandas as pd
from typing import Optional


from hmc.generic_toolkit.data.io_handler_base import IOHandler

class IOWrapper(IOHandler):
    def __init__(self, folder_name: str, file_name: str,
                 file_format: Optional[None] = None) -> None:
        super().__init__(folder_name, file_name, file_format)

    def from_path(self, path: str, time: Optional[pd.Timestamp] = None, format: Optional[None] = None):
        path, file = os.path.split(path)
        return super().__init__(path, file, format)


class StaticHandler(IOWrapper):

    type_class = 'io_static'

    def __init__(self, folder_name: str, file_name: str,
                 file_mandatory: bool = True, file_type: str = 'raster') -> None:

        self.folder_name = folder_name
        self.file_name = file_name
        self.file_mandatory = file_mandatory
        self.file_type = file_type

        super().from_path(os.path.join(self.folder_name, self.file_name))

    @classmethod
    def define_file_data(cls, folder_name: str, file_name: str = '{domain_name}.dem.txt',
                         file_mandatory: bool = True, file_type: str = 'raster',
                         file_tags: dict = None):

        if file_tags is None:
            file_tags = {}

        folder_name = substitute_string_by_tags(folder_name, file_tags)
        file_name = substitute_string_by_tags(file_name, file_tags)

        if not os.path.exists(os.path.join(folder_name, file_name)):
            raise FileNotFoundError(f'File {file_name} does not exist in path {folder_name}.')

        return cls(folder_name, file_name)

    def get_file_data(self):

        file_data = self.get_data(
            row_start=None, row_end=None, col_start=None, col_end=None, mandatory=self.file_mandatory
        )

        return file_data

    @classmethod
    def organize_file_data(cls, folder_name: str, file_name: str,
                           file_mandatory: bool = True, file_type: str = 'raster',
                           row_start: int = None, row_end: int = None, col_start: int = None, col_end: int = None)\
            -> xr.Dataset:

        if file_mandatory:
            if not os.path.exists(os.path.join(folder_name, file_name)):
                raise FileNotFoundError(f'File {file_name} does not exist in path {folder_name}.')

        driver_data = cls(folder_name, file_name, file_mandatory, file_type)

        file_da = driver_data.get_data(
            ow_start=None, row_end=None, col_start=None, col_end=None, mandatory=file_mandatory
        )

        if row_start is not None and row_end is not None and col_start is not None and col_end is not None:
            file_da = file_da.isel(latitude=slice(row_start, row_end), longitude=slice(col_start, col_end))

        return file_da
