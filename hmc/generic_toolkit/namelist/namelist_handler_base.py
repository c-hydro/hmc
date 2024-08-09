import re
import pandas as pd

from hmc.generic_toolkit.namelist.lib_namelist_utils import filter_settings, group_settings, parse_settings
from hmc.generic_toolkit.default.lib_default_namelist import convert_namelist_keys


class NamelistHandler:

    def __init__(self, file_name: str) -> None:

        self.file_name = file_name
        self.file_stream = open(self.file_name, 'r').read()

        self.group_regular_expression = re.compile(r'&([^&]+)/', re.DOTALL)

    def get_data(self, **kwargs):
        """
        Get the data for a given namelist.
        """

        settings_lists, comments_lists = filter_settings(self.file_stream)
        settings_blocks = re.findall(self.group_regular_expression, "\n".join(settings_lists))

        settings_group_raw = group_settings(settings_blocks)
        settings_group_parsed = parse_settings(settings_group_raw)

        settings_group_converted = convert_namelist_keys(
            settings_group_parsed, variable_type='default', group_type='default')

        return settings_group_converted

    def error_data(self):
        """
        Error data.
        """
        raise NotImplementedError
    
    def write_data(self):
        """
        Write the data for a given time.
        """
        raise NotImplementedError

    @staticmethod
    def view_data(settings_dict: dict) -> None:
        """
        View the data for a given time.
        """

        settings_dframe = pd.DataFrame.from_dict(settings_dict, orient='index', columns=['value'])
        print(settings_dframe)

    def check_data(self):
        """
        Check if data is available for a given time.
        """
        raise NotImplementedError
