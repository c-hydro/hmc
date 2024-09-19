# ----------------------------------------------------------------------------------------------------------------------
# libraries
import numpy
import numpy as np
import pandas as pd
import xarray as xr
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to create numpy variable
def create_variable_data(rows, cols, time=None, var_default_value=-9999, var_dtype='float32'):
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
        var_data = np.zeros((time, rows, cols), dtype=var_dtype)
        var_data[:, :, :] = var_default_value
    else:
        var_data = np.zeros((rows, cols), dtype=var_dtype)
        var_data[:, :] = var_default_value

    return var_data
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to get variable data from dataset
def get_variable_data(dset_data: xr.Dataset,
                      var_name: str, var_mandatory: bool = True,
                      var_type: str = 'float32', var_no_data: (float, int) = -9999.0) -> numpy.ndarray:

    if var_name in list(dset_data.variables):
        var_data = dset_data[var_name].values
    else:
        if var_mandatory:
            raise ValueError('Variable "' + var_name + '" not found in dset_data')
        else:
            var_dims = dset_data.dims
            var_cols, var_rows = var_dims['longitude'], var_dims['latitude']
            var_data = np.zeros((var_rows, var_cols), dtype=var_type)
            var_data[:, :] = var_no_data

    return var_data
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to save variable data into dataset
def save_variable_data(dset_data: xr.Dataset, var_data: np.ndarray,
                       var_name: str, var_mandatory: bool = False,
                       var_type: str = 'float32', var_no_data: (float, int) = -9999.0,
                       var_dims: list = None) -> xr.Dataset:

    if var_dims is None:
        var_dims = ['latitude', 'longitude']

    if var_name in list(dset_data.variables):
        dset_data[var_name].values = var_data
    else:
        if var_mandatory:
            raise ValueError('Variable "' + var_name + '" not found in dset_data')
        else:
            var_data = var_data.dtype(var_type)
            var_data[np.isnan(var_data)] = var_no_data
            var_da = xr.DataArray(var_data, dims=var_dims, name=var_name)
            dset_data[var_name] = var_da
    return dset_data
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to convert variables dictionary to xarray dataset
def create_dset_from_dict(vars_dict: dict, vars_coords: dict = None, vars_dims: dict = None,
                          da_reference: xr.DataArray = None, time_reference: {} = None,
                          coord_x : str = 'longitude', coord_y : str = 'latitude', coord_time : str = 'time',
                          dim_x : str = 'longitude', dim_y : str = 'latitude', dim_time : str = 'time') -> xr.Dataset:

    if da_reference is None:
        raise RuntimeError('Reference DataArray must be defined')

    if vars_coords is None:
        vars_coords = {}
        for var_name in vars_dict.keys():
            vars_coords[var_name] = [coord_time, coord_y, coord_x]
    if vars_dims is None:
        vars_dims = {}
        for var_name in vars_dict.keys():
            vars_dims[var_name] = [dim_time, dim_y, dim_x]

    geo_x, geo_y = da_reference[coord_x].values, da_reference[coord_y].values

    dset_data = None
    for var_name, var_data in vars_dict.items():

        var_time_period = None
        if time_reference is not None:
            if var_name in list(time_reference.keys()):
                var_time_length = time_reference[var_name]
                if var_time_length is not None:
                    var_time_period = np.arange(0, var_time_length, 1)

        if var_name not in list(vars_coords.keys()):
            data_dims = [dim_time, dim_y, dim_x]
        else:
            data_dims = vars_dims[var_name]

        if var_name not in list(vars_coords.keys()):
            data_coords = [coord_time, coord_y, coord_x]
        else:
            data_coords = vars_coords[var_name]

        if var_data is not None:
            if var_time_period is None:
                coord_y, coord_x = data_coords[1], data_coords[2]
                dim_y, dim_x = data_dims[1], data_dims[2]
                da_data = xr.DataArray(var_data,
                                       coords={coord_y: geo_y, coord_x: geo_x},
                                       dims=[dim_y, dim_x])
            else:
                coord_time, coord_y, coord_x = data_coords[0], data_coords[1], data_coords[2]
                dim_time, dim_y, dim_x = data_dims[0], data_dims[1], data_dims[2]
                da_data = xr.DataArray(var_data,
                                       coords={coord_time: var_time_period, coord_y: geo_y, coord_x: geo_x},
                                       dims=[dim_time, dim_y, dim_x])

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


# ----------------------------------------------------------------------------------------------------------------------
# method to extract values from object
def extract_values_from_obj(obj_data: (pd.DataFrame, xr.DataArray, xr.Dataset) = None) -> (np.ndarray, dict, None):

    if obj_data is not None:
        if isinstance(obj_data, pd.DataFrame):
            return obj_data.values
        elif isinstance(obj_data, xr.DataArray):
            return obj_data.values
        elif isinstance(obj_data, xr.Dataset):
            data_dict = {}
            for var_name, var_data in obj_data.items():
                data_dict[var_name] = var_data.values
            return data_dict
        else:
            raise NotImplemented('Object type not implemented')
    else:
        return None
# ----------------------------------------------------------------------------------------------------------------------
