# ----------------------------------------------------------------------------------------------------------------------
# libraries
import os
import warnings

import xarray as xr

from hmc.generic_toolkit.data.lib_io_utils import substitute_string_by_date, substitute_string_by_tags

from hmc.generic_toolkit.data.io_handler_base import IOHandler
from hmc.generic_toolkit.data.io_handler_static import StaticHandler
from hmc.hydrological_toolkit.geo.lib_geo_utils import (
    mask_data_by_reference, mask_data_boundaries,
    initialize_data_by_constant, initialize_data_by_default, initialize_data_by_reference)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to handle static driver
class StaticDriver(IOHandler):

    def __init__(self, obj_namelist: dict, obj_reference: xr.DataArray, obj_tags: {} = None) -> None:

        self.obj_namelist_parameters = obj_namelist['parameters']
        self.obj_namelist_settings = obj_namelist['settings']
        self.obj_reference = obj_reference

        if obj_tags is None:
            self.obt_tags = {}
        else:
            self.obj_tags = obj_tags

    # method to organize data
    def organize_data(self, data_collections: dict, data_template: dict):

        static_collections = {**data_collections.static_data_grid, **data_collections.static_data_array}
        static_tags = data_template.tags_string

        string_tags = map_tags(self.obj_tags, static_tags)

        folder_name = self.obj_namelist_settings['path_data_static_grid']
        folder_name = substitute_string_by_tags(folder_name, string_tags)

        file_collections_grid, file_collections_array = None, None
        for file_key, file_collections in static_collections.items():

            file_name = file_collections['file_name']
            file_mandatory = file_collections['file_mandatory']
            file_type = file_collections['file_type']
            vars_constants = file_collections['vars_constants']
            vars_no_data = file_collections['vars_no_data']

            folder_name = substitute_string_by_tags(folder_name, string_tags)
            file_name = substitute_string_by_tags(file_name, string_tags)

            obj_data = StaticHandler.organize_file_data(
                folder_name=folder_name,
                file_name=file_name,
                file_mandatory=file_mandatory,
                file_type=file_type,
                row_start=None, row_end=None, col_start=None, col_end=None)

            if file_type == 'raster':

                if obj_data is None:
                    obj_data = initialize_data_by_reference(da_reference=self.obj_reference, default_value=vars_no_data)

                if vars_constants is not None:
                    if vars_constants in list(self.obj_namelist_parameters.keys()):
                        var_constant_value = self.obj_namelist_parameters[vars_constants]
                        grid_da = initialize_data_by_constant(
                            da_other=obj_data, da_reference=self.obj_reference,
                            condition_method='<', condition_value=0,
                            constant_value=var_constant_value)

                obj_data = mask_data_by_reference(
                    obj_data, self.obj_reference, mask_method='==', mask_value=vars_no_data, mask_other=obj_data)

                obj_data = mask_data_boundaries(obj_data, bounds_value=vars_no_data)

                if file_collections_grid is None:
                    file_collections_grid = xr.Dataset()

                file_collections_grid[file_key] = obj_data

            elif file_type == 'array':

                if file_collections_array is None:
                    file_collections_array = {}

                file_collections_array[file_key] = obj_data

            else:
                raise ValueError(f'Type {file_type} not supported.')

        return file_collections_grid, file_collections_array
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

