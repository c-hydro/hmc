# ----------------------------------------------------------------------------------------------------------------------
# libraries
import os
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

        static_collections = data_collections.static_data_grid
        static_tags = data_template.tags_string

        string_tags = map_tags(self.obj_tags, static_tags)

        folder_name = self.obj_namelist_settings['path_data_static_grid']
        folder_name = substitute_string_by_tags(folder_name, string_tags)

        file_dset = None
        for file_key, file_collections in static_collections.items():

            file_name = file_collections['file']
            file_mandatory = file_collections['mandatory']
            file_type = file_collections['type']
            file_default = file_collections['constants']
            file_no_data = file_collections['no_data']

            folder_name = substitute_string_by_tags(folder_name, string_tags)
            file_name = substitute_string_by_tags(file_name, string_tags)

            grid_da = StaticHandler.organize_file_data(
                folder_name=folder_name,
                file_name=file_name,
                file_mandatory=file_mandatory,
                file_type=file_type,
                row_start=None, row_end=None, col_start=None, col_end=None)

            if grid_da is None:
                grid_da = initialize_data_by_reference(da_reference=self.obj_reference, default_value=file_no_data)

            if file_default is not None:
                if file_default in list(self.obj_namelist_parameters.keys()):
                    file_default_value = self.obj_namelist_parameters[file_default]
                    grid_da = initialize_data_by_constant(
                        da_other=grid_da, da_reference=self.obj_reference,
                        condition_method='<', condition_value=0,
                        constant_value=file_default_value)

            grid_da = mask_data_by_reference(grid_da, self.obj_reference)

            grid_da = mask_data_boundaries(grid_da, bounds_value=file_no_data)

            if file_dset is None:
                file_dset = xr.Dataset()

            file_dset[file_key] = grid_da

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

