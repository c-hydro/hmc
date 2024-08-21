
import numpy as np
import xarray as xr
from copy import deepcopy


def mask_data_boundaries(obj_data: (xr.DataArray, xr.Dataset), bounds_value: (float, int) = None) -> xr.DataArray:

    if isinstance(obj_data, xr.DataArray):
        obj_data.values[0, :] = bounds_value
        obj_data.values[-1, :] = bounds_value
        obj_data.values[:, 0] = bounds_value
        obj_data.values[:, -1] = bounds_value
    elif isinstance(obj_data, xr.Dataset):
        for var_name, var_data in obj_data.items():

            print(var_name)

            var_data.values[0, :] = bounds_value
            var_data.values[-1, :] = bounds_value
            var_data.values[:, 0] = bounds_value
            var_data.values[:, -1] = bounds_value

            obj_data[var_name] = var_data

    return obj_data


# method to mask data by reference
def mask_data_by_reference(da_other: xr.DataArray, da_reference: xr.DataArray,
                           mask_value: (float, int) = None) -> xr.DataArray:

    if mask_value is None:
        mask_value = -9999.0
    da_other = da_other.where(da_reference != mask_value, mask_value)

    return da_other


# method to initialize data array with constants value
def initialize_data_by_reference(da_reference, default_value: (float, int) = None) -> xr.DataArray:

    da_default = deepcopy(da_reference)

    data_default = np.zeros(da_default.shape)
    data_default[:, :] = default_value
    da_default.values = data_default

    return da_default


def initialize_data_by_constant(da_other: xr.DataArray,
                                da_reference: xr.DataArray,
                                condition_method: str = ('>', '<', '>=', '<=', '==', '!='),
                                condition_value: (float, int) = None,
                                constant_value: (float, int) = None):

    if (constant_value is not None) and (condition_value is not None):
        if condition_method == '!=':
            da_other = da_other.where(da_reference != condition_value, constant_value)
        elif condition_method == '==':
            da_other = da_other.where(da_reference == condition_value, constant_value)
        elif condition_method == '>':
            da_other = da_other.where(da_reference > condition_value, constant_value)
        elif condition_method == '<':
            da_other = da_other.where(da_reference < condition_value, constant_value)
        elif condition_method == '>=':
            da_other = da_other.where(da_reference >= condition_value, constant_value)
        elif condition_method == '<=':
            da_other = da_other.where(da_reference <= condition_value, constant_value)
        else:
            raise ValueError(f'Condition {condition} not supported.')

    return da_other


# method to initialize data by constants value
def initialize_data_by_default(rows: int, cols: int, default_value: (float, int) = None) -> xr.DataArray:

    if default_value is None:
        default_value = 0.0

    data = xr.DataArray(default_value, dims=['rows', 'cols'], coords={'rows': range(rows), 'cols': range(cols)})

    return data