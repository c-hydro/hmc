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

    def __init__(self,
                 parameters: dict, settings: dict,
                 reference_grid: xr.DataArray,
                 file_tags_definitions: dict = None, file_tags_pattern: dict = None,
                 file_template: dict = None) -> None:

        self.parameters = parameters
        self.settings = settings
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

    # method to organize data
    def organize_data(self) -> tuple:

        folder_name_point, folder_name_grid, folder_name_array = self.__select_folder_by_type(
            tag_point='path_data_static_point', tag_grid='path_data_static_grid', tag_array='path_data_static_grid')

        string_tags = map_tags(self.file_tags_definitions, self.file_tags_pattern)

        file_collections_point, file_collections_grid, file_collections_array = None, None, None
        for file_key, file_collections in self.file_template.items():

            file_name = file_collections['file_name']
            file_mandatory = file_collections['file_mandatory']
            file_type = file_collections['file_type']
            vars_constants = file_collections['vars_constants']
            vars_no_data = file_collections['vars_no_data']

            if 'raster' == file_type:
                folder_name = folder_name_grid
            elif 'array' == file_type:
                folder_name = folder_name_array
            elif 'point' in file_type:
                folder_name = folder_name_point
            else:
                raise ValueError(f'Type {file_type} not supported')

            folder_name = substitute_string_by_tags(folder_name, string_tags)
            file_name = substitute_string_by_tags(file_name, string_tags)

            obj_data = StaticHandler.organize_file_data(
                folder_name=folder_name,
                file_name=file_name,
                file_mandatory=file_mandatory,
                file_type=file_type,
                row_start=None, row_end=None, col_start=None, col_end=None)

            if 'raster' == file_type:

                if obj_data is None:
                    obj_data = initialize_data_by_reference(da_reference=self.reference_grid, default_value=vars_no_data)

                if vars_constants is not None:
                    if vars_constants in list(self.parameters.keys()):
                        var_constant_value = self.parameters[vars_constants]
                        obj_data = initialize_data_by_constant(
                            da_other=obj_data, da_reference=self.reference_grid,
                            condition_method='<', condition_value=0,
                            constant_value=var_constant_value)

                obj_data = mask_data_by_reference(
                    obj_data, self.reference_grid, mask_method='==', mask_value=vars_no_data, mask_other=obj_data)

                obj_data = mask_data_boundaries(obj_data, bounds_value=vars_no_data)

                if file_collections_grid is None:
                    file_collections_grid = xr.Dataset()
                file_collections_grid[file_key] = obj_data

            elif 'array' == file_type:

                if file_collections_array is None:
                    file_collections_array = {}
                file_collections_array[file_key] = obj_data

            elif 'point' in file_type:

                if file_collections_point is None:
                    file_collections_point = {}
                file_collections_point[file_key] = obj_data

            else:
                raise ValueError(f'Type {file_type} not supported.')

        return file_collections_point, file_collections_grid, file_collections_array,

    def __select_folder_by_type(self,
                                tag_grid: str = 'path_data_static_grid', tag_point: str = 'path_data_static_point',
                                tag_array: str = 'path_data_static_grid'):

        if tag_grid in list(self.settings.keys()):
            folder_name_grid = self.settings[tag_grid]
        else:
            raise ValueError(f'Tag {tag_grid} not found in namelist settings.')
        if tag_point in list(self.settings.keys()):
            folder_name_point = self.settings[tag_point]
        else:
            raise ValueError(f'Tag {tag_point} not found in namelist settings.')
        if tag_array in list(self.settings.keys()):
            folder_name_array = self.settings[tag_array]
        else:
            raise ValueError(f'Tag {tag_array} not found in namelist settings.')

        return folder_name_point, folder_name_grid, folder_name_array
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

