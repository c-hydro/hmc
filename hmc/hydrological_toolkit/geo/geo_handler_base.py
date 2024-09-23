# libraries
import warnings
import xarray as xr
import numpy as np

from typing import Optional

import matplotlib.pylab as plt


# class to handle geospatial data
class GeoHandler:

    def __init__(self, da_data: xr.DataArray, da_reference: xr.DataArray) -> None:

        self.da_data = da_data
        self.da_reference = da_reference

    # class method to select data
    @classmethod
    def select_data(cls, dset_data: xr.Dataset, da_reference: xr.DataArray, var_name: str = 'terrain'):
        if var_name in list(dset_data.variables):
            da_data = dset_data[var_name]
        else:
            raise ValueError('Variable "' + var_name + '" not found in dataset')
        return cls(da_data, da_reference)

    # method to mask data (based on reference)
    def mask_data(self, da_data: xr.DataArray) -> xr.DataArray:
        da_mask = self.da_reference.notnull()
        da_masked = da_data.where(da_mask)
        return da_masked

    # method to check data (not null)
    def check_data_null(self, da_data: xr.DataArray,
                           no_data: (float, int) = -9999.0, fill_data: (int, float) = np.nan) -> bool:
        da_mask = self.da_reference
        da_data = da_data.where(da_mask.values != no_data, fill_data)

        null = np.all(np.isnan(da_data.values))

        return null

    # method to add data (to dataset)
    def add_data(self, da_data: xr.DataArray, dset_data: xr.Dataset,
                 var_name: str = 'variable', var_updating: bool = False, var_mandatory: bool = False,
                 var_no_data: (int, float) = -9999.0) -> xr.Dataset:

        if var_name in list(dset_data.variables):
            if not var_updating:
                if self.check_data_null(dset_data[var_name], no_data=var_no_data):
                    if var_mandatory:
                        raise ValueError('Variable "' + var_name + '" already exists in dataset, but is null')
                    else:
                        warnings.warn('Variable "' + var_name + '" already exists in dataset, but is null')
            else:
                dset_data[var_name] = da_data
        else:
            dset_data[var_name] = da_data

        return dset_data

    def add_data_list(self, da_data_list: list, dset_data: Optional[xr.Dataset] = None,
                      var_name_list: list = None, var_updating_list: list = None,
                      var_mandatory_list: list = None, var_no_data_list: list = None) -> xr.Dataset:

        if var_name_list is None:
            var_name_list = ['variable'] * len(da_data_list)
        if var_updating_list is None:
            var_updating_list = [False] * len(da_data_list)
        if var_mandatory_list is None:
            var_mandatory_list = [False] * len(da_data_list)
        if var_no_data_list is None:
            var_no_data_list = [-9999.0] * len(da_data_list)

        if dset_data is None:
            dset_data = self.init_data()

        for i, da_data in enumerate(da_data_list):
            dset_data = self.add_data(da_data, dset_data, var_name=var_name_list[i], var_updating=var_updating_list[i],
                                      var_mandatory=var_mandatory_list[i], var_no_data=var_no_data_list[i])

        return dset_data

    # method to initialize data (based on reference using a dataset)
    def init_data(self, da_data: xr.DataArray = None, da_name: str = 'data') -> xr.Dataset:

        geo_x, geo_y = self.da_reference['longitude'].values, self.da_reference['latitude'].values
        dset_default = xr.Dataset(coords={'longitude': geo_x, 'latitude': geo_y})

        if da_data is not None:
            dset_default[da_name] = da_data

        return dset_default

    # method to update data
    @staticmethod
    def update_data(dset_data: xr.Dataset, dset_expected: xr.Dataset, drop_variables: bool = False) -> xr.Dataset:

        vars_expected = list(dset_expected.variables)
        vars_dropped = []
        for var_name in vars_expected:
            if var_name in list(dset_data.variables):
                dset_expected[var_name] = dset_data[var_name]
            else:
                vars_dropped.append(var_name)

        if drop_variables:
            dset_expected = dset_expected.drop_vars(vars_dropped)

        return dset_expected

    # method to view data
    @staticmethod
    def view_data(obj_data: (np.ndarray, xr.DataArray, xr.Dataset),
                  var_name: str = None,
                  var_data_min: (int, float) = None, var_data_max: (int, float) = None,
                  var_fill_data: (int, float) = np.nan, var_null_data: (int, float) = np.nan,
                  view_type: str = 'data_array', **kwargs) -> None:
        """
        View the data.
        """

        if isinstance(obj_data, xr.Dataset):
            if var_name is None:
                raise ValueError('Variable name not provided for dataset mode.')
            if var_name not in obj_data:
                raise ValueError(f'Variable {var_name} not found in dataset.')
            obj_data = obj_data[var_name]

        if isinstance(obj_data, xr.DataArray):
            if var_data_min is not None and var_fill_data is not None:
                obj_data = obj_data.where(obj_data >= var_data_min, var_fill_data)
            if var_data_max is not None and var_fill_data is not None:
                obj_data = obj_data.where(obj_data <= var_data_max, var_fill_data)
            if var_fill_data is not None and var_null_data is not None:
                obj_data = obj_data.where(obj_data != var_null_data, var_null_data)

            if view_type == 'data_array':
                plt.figure()
                obj_data.plot()
                plt.colorbar()
            elif view_type == 'array':
                plt.figure()
                plt.imshow(obj_data.values)
                plt.colorbar()
            else:
                raise ValueError(f'View type {view_type} not supported.')

        elif isinstance(obj_data, np.ndarray):

            plt.figure()
            plt.imshow(obj_data)
            plt.colorbar()

        else:
            raise ValueError('Data type not supported.')