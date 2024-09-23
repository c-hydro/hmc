# ----------------------------------------------------------------------------------------------------------------------
# libraries
import os
import pandas as pd
import xarray as xr

from hmc.generic_toolkit.data.lib_io_utils import substitute_string_by_date, substitute_string_by_tags

from hmc.generic_toolkit.data.io_handler_base import IOHandler
from hmc.generic_toolkit.data.io_handler_dynamic_src import DynamicSrcHandler
from hmc.hydrological_toolkit.geo.lib_geo_utils import (
    mask_data_by_reference, mask_data_boundaries,
    initialize_data_by_constant, initialize_data_by_default, initialize_data_by_reference)

from hmc.hydrological_toolkit.variables.lib_variable_attrs import fill_list_length
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to handle static driver
class DynamicDriver(IOHandler):

    def __init__(self, parameters: dict, settings: dict,
                 folder_name: str, file_name: str = None,
                 reference_grid: xr.DataArray = None,
                 file_tags_definitions: dict = None, file_tags_pattern: dict = None,
                 file_template: dict = None) -> None:

        self.parameters = parameters
        self.settings = settings

        self.folder_name = folder_name
        self.file_name = file_name

        self.reference_grid = reference_grid

        if file_tags_definitions is None:
            self.file_tags_definitions = {}
        else:
            self.file_tags_definitions = file_tags_definitions
        if file_tags_pattern is None:
            self.file_tags_pattern = {}
        else:
            self.file_tags_pattern = file_tags_pattern

        self.file_template = file_template

        self.obj_vars_keys = ['rain', 'airt', 'inc_rad', 'wind', 'rh', 'airp']
        self.obj_vars_data = ['Rain', 'AirTemperature', 'IncomingRadiation', 'Wind', 'RelativeHumidity', 'AirPressure']
        self.obj_vars_mandatory = [True, True, True, True, True, False]

        self.obj_vars_map = dict(zip(self.obj_vars_keys, self.obj_vars_data))
        self.obj_vars_mode = dict(zip(self.obj_vars_keys, self.obj_vars_mandatory))

    # method to organize data
    def organize_data(self, data_time: pd.Timestamp):

        string_tags = map_tags(self.file_tags_definitions, self.file_tags_pattern)

        folder_name = self.folder_name
        if self.file_name is None:
            file_name = self.file_template['file_name']
        else:
            file_name = self.file_name
        file_mandatory = self.file_template['file_mandatory']
        file_type = self.file_template['file_type']
        vars_constant = self.file_template['vars_constants']
        vars_no_data = self.file_template['vars_no_data']
        vars_list = self.file_template['vars_list']
        vars_tags = self.file_template['vars_tags']
        vars_mandatory = self.file_template['vars_mandatory']

        vars_constant, vars_no_data, vars_list, vars_tags, vars_mandatory = fill_list_length(
            vars_constant, vars_no_data, vars_list, vars_tags, vars_mandatory, no_data=-9999.0)

        folder_name = substitute_string_by_tags(folder_name, string_tags)
        folder_name = substitute_string_by_date(folder_name, data_time, self.file_tags_pattern)
        file_name = substitute_string_by_tags(file_name, string_tags)
        file_name = substitute_string_by_date(file_name, data_time, self.file_tags_pattern)

        io_dynamic_src_grid_handler = DynamicSrcHandler.organize_file_data(
            folder_name=folder_name,
            file_name=file_name,
            file_mandatory=file_mandatory,
            vars_list=vars_list, vars_tags=vars_tags,
        )

        # get data information
        file_dset = io_dynamic_src_grid_handler.get_file_data()
        # adjust data information (according to the specific data type)
        file_dset = io_dynamic_src_grid_handler.adjust_file_data(file_dset)
        # fill data information
        file_dset = io_dynamic_src_grid_handler.fill_file_data(
            file_dset, ref_data=self.reference_grid,
            vars_tags=vars_tags, vars_mandatory=vars_mandatory, vars_no_data=vars_no_data)

        # mask data by reference
        file_dset = mask_data_boundaries(file_dset, bounds_value=vars_no_data)

        return file_dset

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to map tags data to template
def map_tags(tags_data: dict, tags_template: dict) -> dict:
    """
    Map the tags data to the template.
    :param tags_data:
    :param tags_template:
    :return:
    """
    tags_file = {}
    for tag_key, tag_value in tags_data.items():
        if tag_key in tags_template.keys():
            tags_file[tag_key] = tag_value
    return tags_file
# ----------------------------------------------------------------------------------------------------------------------

