# ----------------------------------------------------------------------------------------------------------------------
# libraries
import numpy as np
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to apply metrics to variable
def apply_metrics(data: np.ndarray, mask: np.ndarray = None,
                  metrics: list = None, axis: list = None, decimals: int = 2):
    """
    Apply metrics to data.

    :param mask:
    :param data: np.ndarray, data
    :param metrics: list, metrics
    :param axis: int, axis
    :param decimals: int, number of decimals
    :return: np.ndarray, data
    """
    if metrics is None:
        raise ValueError('Metrics not defined')

    if mask is not None:
        data[mask == 0] = np.nan

    if not isinstance(metrics, list):
        metrics = [metrics]
    if axis is None:
        axis = [0, 1]
    if not isinstance(axis, list):
        axis = [axis]

    # iterate over metrics
    info = {}
    for fx in metrics:
        if fx == 'mean' or fx == 'nanmean':
            if len(axis) == 1:
                metric = np.nanmean(data, axis=axis[0])
            elif len(axis) == 2:
                metric = np.nanmean(np.nanmean(data, axis=axis[0]))
            else:
                raise ValueError(f'Axis "{axis}" not allowed')
        elif fx == 'sum':
            if len(axis) == 1:
                metric = np.nansum(data, axis=axis[0])
            elif len(axis) == 2:
                metric = np.nansum(np.nansum(data, axis=axis[0]))
            else:
                raise ValueError(f'Axis "{axis}" not allowed')
        elif fx == 'min' or fx == 'nanmin':
            if len(axis) == 1:
                metric = np.nanmin(data, axis=axis[0])
            elif len(axis) == 2:
                metric = np.nanmin(np.nanmin(data, axis=axis[0]))
            else:
                raise ValueError(f'Axis "{axis}" not allowed')
        elif fx == 'max' or fx == 'nanmax':
            if len(axis) == 1:
                metric = np.nanmax(data, axis=axis[0])
            elif len(axis) == 2:
                metric = np.nanmax(np.nanmax(data, axis=axis[0]))
            else:
                raise ValueError(f'Axis "{axis}" not allowed')

        elif fx == 'std' or fx == 'nanstd':
            if len(axis) == 1:
                metric = np.nanstd(data, axis=axis[0])
            elif len(axis) == 2:
                metric = np.nanstd(np.nanstd(data, axis=axis[0]))
            else:
                raise ValueError(f'Axis "{axis}" not allowed')

        elif fx == 'var' or fx == 'nanvar':
            if len(axis) == 1:
                metric = np.nanvar(data, axis=axis[0])
            elif len(axis) == 2:
                metric = np.nanvar(np.nanvar(data, axis=axis[0]))
            else:
                raise ValueError(f'Axis "{axis}" not allowed')

        elif fx == 'count' or fx == 'nancount':
            if len(axis) == 1 or len(axis) == 2:
                metric = np.count_nonzero(~np.isnan(data))
            else:
                raise ValueError(f'Axis "{axis}" not allowed')

        else:
            raise ValueError(f'Metric "{fx}" not found')

        # round metric
        metric = np.round(metric, decimals)
        # store metrics
        info[fx] = metric

    return info
# ----------------------------------------------------------------------------------------------------------------------


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
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------------------------------------------------
