# libraries
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
