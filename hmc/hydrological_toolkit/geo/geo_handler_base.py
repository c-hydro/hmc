# libraries
import os
from typing_extensions import Self
from typing import Optional
from datetime import datetime
import pandas as pd
import xarray as xr


class GeoHandler:

    def __init__(self, da_data: xr.DataArray, da_reference: xr.DataArray) -> None:

        self.da_data = da_data
        self.da_reference = da_reference

    @classmethod
    def select_data(cls, dset_data: xr.Dataset, da_reference: xr.DataArray, var_name: str = 'terrain'):
        if var_name in list(dset_data.variables):
            da_data = dset_data[var_name]
        else:
            raise ValueError('Variable "' + var_name + '" not found in dataset')
        return cls(da_data, da_reference)

    def mask_data(self, da_data: xr.DataArray) -> xr.DataArray:
        da_mask = self.da_reference.notnull()
        da_data_masked = da_data.where(da_mask)
        return da_data_masked

    @staticmethod
    def add_data(da_data: xr.DataArray, dset_data: xr.Dataset, var_name: str = 'variable') -> xr.DataArray:

        if var_name in list(dset_data.variables):
            raise ValueError('Variable "' + var_name + '" already exists in dataset')
        dset_data[var_name] = da_data

        return dset_data