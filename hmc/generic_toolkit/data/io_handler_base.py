import os
from typing import Optional
from datetime import datetime
import numpy as np
import xarray as xr

from hmc.generic_toolkit.data.lib_io_ascii import get_file_grid as get_file_grid_ascii
from hmc.generic_toolkit.data.lib_io_tiff import get_file_grid as get_file_grid_tiff
from hmc.generic_toolkit.data.lib_io_nc import get_file_grid as get_file_grid_nc

import matplotlib.pylab as plt

class IOHandler:

    type_data = {'ascii': get_file_grid_ascii, 'tiff': get_file_grid_tiff, 'netCDF': get_file_grid_nc}

    def __init__(self, folder_name: str, file_name: str,
                 time: Optional[datetime] = None, format: Optional[None] = None) -> None:

        self.folder_name = folder_name
        self.file_name = file_name
        self.path_name = os.path.join(self.folder_name, self.file_name)

        self.time = time

        self.format = format if format is not None else self.file_name.split('.')[-1]
        if self.format.lower() in ['tif', 'tiff', 'geotiff']:
            self.format = 'tiff'
        elif self.format.lower() in ['txt', 'asc']:
            self.format = 'ascii'
        elif self.format.lower() in ['nc', 'netcdf']:
            self.format = 'netCDF'
        else:
            raise ValueError(f'Format {self.format} not supported.')

        self.fx_data = self.type_data.get(self.format, self.error_data)

    @classmethod
    def from_path(cls, path: str, time: Optional[datetime] = None, format: Optional[None] = None):
        folder_name, file_name = os.path.split(path)
        return cls(folder_name, file_name, time, format)

    def get_data(self,
                 row_start: int = None, row_end: int = None,
                 col_start: int = None, col_end: int = None,
                 mandatory: bool = False, **kwargs) -> (xr.DataArray, xr.Dataset):
        """
        Get the data for a given time.
        """

        flag_data = self.check_data(mandatory=mandatory)
        obj_data = self.fx_data(self.path_name)

        if row_start is not None and row_end is not None and col_start is not None and col_end is not None:
            obj_data = obj_data.isel(latitude=slice(row_start, row_end), longitude=slice(col_start, col_end))

        return obj_data

    def error_data(self):
        """
        Error data.
        """
        raise NotImplementedError
    
    def write_data(self, data: xr.DataArray, time: Optional[datetime], tags: dict, **kwargs):
        """
        Write the data for a given time.
        """
        raise NotImplementedError
    
    def view_data(self, obj_data: (xr.DataArray, xr.Dataset),
                  var_name: str = None,
                  var_data_min: (int, float) = None, var_data_max: (int, float) = None,
                  var_fill_data: (int, float) = np.nan, var_null_data: (int, float) = np.nan, **kwargs) -> None:
        """
        View the data for a given time.
        """

        if isinstance(obj_data, xr.Dataset):
            if var_name is None:
                raise ValueError('Variable name not provided for dataset mode.')
            if var_name not in obj_data:
                raise ValueError(f'Variable {var_name} not found in dataset.')
            obj_data = obj_data[var_name]

        if var_data_min is not None and var_fill_data is not None:
            obj_data = obj_data.where(obj_data >= var_data_min, var_fill_data)
        if var_data_max is not None and var_fill_data is not None:
            obj_data = obj_data.where(obj_data <= var_data_max, var_fill_data)
        if var_fill_data is not None and var_null_data is not None:
            obj_data = obj_data.where(obj_data != var_null_data, var_null_data)

        plt.figure()
        obj_data.plot()
        plt.colorbar()


    def check_data(self, mandatory: bool = False, **kwargs) -> bool:
        """
        Check if data is available for a given time.
        """
        if os.path.exists(self.path_name):
            return True
        else:
            if mandatory:
                raise IOError(f'File {self.path_name} not found.')
            return False

