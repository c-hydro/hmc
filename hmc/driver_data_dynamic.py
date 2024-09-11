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
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to handle static driver
class DynamicDriver(IOHandler):

    def __init__(self, obj_namelist: dict, obj_reference: xr.DataArray, obj_tags: {} = None) -> None:

        self.obj_namelist_parameters = obj_namelist['parameters']
        self.obj_namelist_settings = obj_namelist['settings']
        self.obj_reference = obj_reference

        if obj_tags is None:
            self.obt_tags = {}
        else:
            self.obj_tags = obj_tags

        self.obj_vars_keys = ['rain', 'airt', 'inc_rad', 'wind', 'rh', 'airp']
        self.obj_vars_data = ['Rain', 'AirTemperature', 'IncomingRadiation', 'Wind', 'RelativeHumidity', 'AirPressure']
        self.obj_vars_mandatory = [True, True, True, True, True, False]

        self.obj_vars_map = dict(zip(self.obj_vars_keys, self.obj_vars_data))
        self.obj_vars_mode = dict(zip(self.obj_vars_keys, self.obj_vars_mandatory))

    # method to organize data
    def organize_data(self, data_time: pd.Timestamp, data_collections: dict, data_template: dict):

        dynamic_collections = data_collections.dynamic_data_grid['dynamic_src_grid']
        dynamic_tags = {**data_template.tags_string, **data_template.tags_time}

        string_tags = map_tags(self.obj_tags, dynamic_tags)

        folder_name = self.obj_namelist_settings['path_data_dynamic_src_grid']
        file_name = dynamic_collections['file_name']
        file_mandatory = dynamic_collections['file_mandatory']
        file_type = dynamic_collections['file_type']
        vars_constant = dynamic_collections['vars_constants']
        vars_no_data = dynamic_collections['vars_no_data']
        vars_list = dynamic_collections['vars_list']
        vars_tags = dynamic_collections['vars_tags']
        vars_mandatory = dynamic_collections['vars_mandatory']

        folder_name = substitute_string_by_tags(folder_name, string_tags)
        folder_name = substitute_string_by_date(folder_name, data_time, dynamic_tags)
        file_name = substitute_string_by_tags(file_name, string_tags)
        file_name = substitute_string_by_date(file_name, data_time, dynamic_tags)

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
        file_dset = io_dynamic_src_grid_handler.fill_file_data(file_dset, vars_mandatory=vars_mandatory)

        # mask data by reference
        file_dset = mask_data_boundaries(file_dset, bounds_value=file_no_data)

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

