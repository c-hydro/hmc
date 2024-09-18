# libraries
import numpy as np
import pandas as pd


# method to check string has the date format
def is_date(string: str, date_format: str = '%Y%m%d%H%M') -> bool:
    """
    Return whether the string can be interpreted as a date.
    :param string: str, string to check for date
    :param date_format: str, format of the date
    """
    try:
        pd.to_datetime(string, format=date_format, errors='raise')
        return True

    except ValueError:
        return False


def compute_value_by_date(data: list, time: pd.Timestamp):

    time = time.replace(hour=0, minute=0)

    day_actual = time.day
    month_actual = time.month

    month_before, month_after = month_actual -1, month_actual + 1
    if month_before == 0:
        month_before = 12
    if month_after == 13:
        month_after = 1

    time_mid_actual = time.replace(month=month_actual, day=15)
    time_mid_before = time.replace(month=month_before, day=15)
    time_mid_after = time.replace(month=month_after, day=15)

    days_n_before = (time_mid_actual - time_mid_before).days
    days_n_after = (time_mid_after - time_mid_actual).days

    data_actual, data_before, data_after = data[month_actual - 1], data[month_before - 1], data[month_after - 1]

    if day_actual == 15:
        value = data_actual
    elif day_actual < 15:

        time_mid_actual = time_mid_actual.replace(day=15)

        data_arr = np.linspace(data_before, data_actual, num=days_n_before + 1)
        time_arr = pd.date_range(time_mid_before, time_mid_actual, freq='D')
        data_df = pd.Series(data_arr, index=time_arr)

        value = data_df[time]

    elif day_actual > 15:

        time_mid_actual = time_mid_actual.replace(day=15)

        data_arr = np.linspace(data_actual, data_after, num=days_n_after + 1)
        time_arr = pd.date_range(time_mid_actual, time_mid_after, freq='D')
        data_df = pd.Series(data_arr, index=time_arr)

        value = data_df[time]

    return value






