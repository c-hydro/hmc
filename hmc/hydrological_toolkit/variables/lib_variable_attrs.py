# ----------------------------------------------------------------------------------------------------------------------
# libraries
import numpy as np
import pandas as pd
import xarray as xr
# ----------------------------------------------------------------------------------------------------------------------


# method to compute list length
def compute_list_n(*args):
    max_list = []
    for arg in args:
        if not isinstance(arg, list):
            arg = [arg]
        max_list.append(len(arg))
    max_n = np.max(max_list)
    return max_n


# method to fill list length
def fill_list_length(*args, no_data: (int, float, list) = None):
    max_n = compute_list_n(*args)

    if not isinstance(no_data, list):
        no_data = [no_data]
    if len(no_data) < max_n:
        no_data = no_data * max_n

    filled_list = []
    for i, arg in enumerate(args):
        arg_no_data = no_data[i]
        if not isinstance(arg, list):
            arg = [arg]
        if len(arg) < max_n:
            arg = [arg_no_data] * max_n
        filled_list.append(arg)
    args = tuple(filled_list)
    return args
