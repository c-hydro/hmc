"""
Library Features:

Name:          lib_io_utils
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20240801'
Version:       '1.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
from datetime import datetime
import os

import pandas as pd
import xarray as xr
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to substitute string
def substitute_string(string, tag_dict, rec=False):
    """
    replace the {tags} in the string with the values in the tag_dict
    """
    while "{" in string and "}" in string:
        for key, value in tag_dict.items():
            # check if the value is a datetime object and the string contains a format specifier for the key
            if isinstance(value, datetime) and '{' + key + ':' in string:
                # extract the format specifier from the string
                fmt = string.split('{' + key + ':')[1].split('}')[0]
                # format the value using the format specifier
                value = value.strftime(fmt)
                key = key + ':' + fmt
            # replace the bracketed part with the value
            string = string.replace('{' + key + '}', str(value))
        if not rec:
            break
    return string
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to create a data array
def create_darray(data, geo_x, geo_y, time=None, name=None,
                  coord_name_x='longitude', coord_name_y='latitude', coord_name_time='time',
                  dim_name_x='longitude', dim_name_y='latitude', dim_name_time='time',
                  dims_order=None):

    if dims_order is None:
        dims_order = [dim_name_y, dim_name_x]
    if time is not None:
        dims_order = [dim_name_y, dim_name_x, dim_name_time]

    if geo_x.shape.__len__() == 2:
        geo_x = geo_x[0, :]
    if geo_y.shape.__len__() == 2:
        geo_y = geo_y[:, 0]

    if time is None:

        data_da = xr.DataArray(data,
                               dims=dims_order,
                               coords={coord_name_x: (dim_name_x, geo_x),
                                       coord_name_y: (dim_name_y, geo_y)})

    elif isinstance(time, pd.DatetimeIndex):

        if data.shape.__len__() == 2:
            data = np.expand_dims(data, axis=-1)

        data_da = xr.DataArray(data,
                               dims=dims_order,
                               coords={coord_name_x: (dim_name_x, geo_x),
                                       coord_name_y: (dim_name_y, geo_y),
                                       coord_name_time: (dim_name_time, time)})
    else:
        logging.error(' ===> Time obj is in wrong format')
        raise IOError('Variable time format not valid')

    if name is not None:
        data_da.name = name

    return data_da
# ----------------------------------------------------------------------------------------------------------------------
