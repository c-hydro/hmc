
import pandas as pd


# method to check string has the date format
def is_date(string: str, format :str ='%Y5m5d%H%M') -> bool:
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param format: str, format of the date
    """
    try:
        pd.to_datetime(string, format=format, errors='raise')
        return True

    except ValueError:
        return False
