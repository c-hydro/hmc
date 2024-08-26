# ----------------------------------------------------------------------------------------------------------------------
# libraries
import numpy
import numpy as np
import xarray as xr
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to create numpy variable
def create_variable(rows, cols, time=None, var_default_value=-9999, var_dtype='float32'):
    """
    Create a variable with default value and dimensions.

    :param time: int, number of time steps
    :param rows: int, number of rows
    :param cols: int, number of columns
    :param var_default_value: float, default value
    :param var_dtype: str, data type
    :return: np.ndarray, variable
    """
    # check data type
    if var_dtype is None:
        var_dtype = 'float32'
    if var_default_value is None:
        var_default_value = -9999.0

    # create variable
    if time is not None:
        var_data = np.zeros((rows, cols, time), dtype=var_dtype)
        var_data[:, :, :] = var_default_value
    else:
        var_data = np.zeros((rows, cols), dtype=var_dtype)
        var_data[:, :] = var_default_value

    return var_data
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to get variable data
def get_variable_data(dset_data: xr.Dataset, var_name: str, var_mandatory: bool = True) -> numpy.ndarray:

    if var_name in list(dset_data.variables):
        var_data = dset_data[var_name].values
    else:
        if var_mandatory:
            raise ValueError('Variable "' + var_name + '" not found in dset_data')
        else:
            var_data = dset_data.shape

    return var_data
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to convert variables dictionary to xarray dataset
def create_dset_from_dict(vars_dict: dict, da_reference: xr.DataArray) -> xr.Dataset:

    geo_x, geo_y = da_reference['longitude'].values, da_reference['latitude'].values

    dset_data = None
    for var_name, var_data in vars_dict.items():

        if var_data is not None:

            da_data = xr.DataArray(var_data, coords=[geo_y, geo_x], dims=['latitude', 'longitude'])

            if dset_data is None:
                dset_data = xr.Dataset()
            dset_data[var_name] = da_data

        else:
            raise ValueError('Variable "' + var_name + '" is None')

    return dset_data
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to create dictionary from dataset
def create_dict_from_dset(dset_data: xr.Dataset) -> dict:
    vars_dict = {}
    for var_name, var_data in dset_data.items():
        vars_dict[var_name] = var_data.values
    return vars_dict
# ----------------------------------------------------------------------------------------------------------------------
