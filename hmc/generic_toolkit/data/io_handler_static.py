# libraries
import os
import xarray as xr
import pandas as pd
from typing import Optional

from hmc.generic_toolkit.data.lib_io_utils import substitute_string_by_date, substitute_string_by_tags
from hmc.generic_toolkit.data.io_handler_base import IOHandler
from hmc.generic_toolkit.data.io_handler_base import map_tags


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
    def organize_file_obj(cls, folder_name: str, file_collections: dict, file_tags: dict, file_template: dict,
                          row_start: int = None, row_end: int = None, col_start: int = None, col_end: int = None)\
            -> xr.Dataset:

        file_filled = map_tags(file_tags, file_template.tags_string)

        folder_name = substitute_string_by_tags(folder_name, file_filled)

        file_dset = None
        for file_key, file_collections in file_collections.static_data_grid.items():
            file_name = file_collections['file']
            file_mandatory = file_collections['mandatory']
            file_type = file_collections['type']

            file_name = substitute_string_by_tags(file_name, tags_file)

            if file_mandatory:
                if not os.path.exists(os.path.join(folder_name, file_name)):
                    raise FileNotFoundError(f'File {file_name} does not exist in path {folder_name}.')

            driver_data = cls(folder_name, file_name, file_mandatory, file_type)

            file_da = driver_data.get_data(
                ow_start=None, row_end=None, col_start=None, col_end=None, mandatory=file_mandatory
            )

            if file_dset is None:
                file_dset = xr.Dataset()
            file_dset[file_key] = file_da

        if row_start is not None and row_end is not None and col_start is not None and col_end is not None:
            file_dset = file_dset.isel(latitude=slice(row_start, row_end), longitude=slice(col_start, col_end))

        return file_dset
