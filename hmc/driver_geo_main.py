# ----------------------------------------------------------------------------------------------------------------------
# libraries
import os
import pandas as pd
import xarray as xr

from hmc.hydrological_toolkit.geo.geo_handler_area_cell import AreaCellHandler
from hmc.hydrological_toolkit.geo.geo_handler_terrain import TerrainHandler
from hmc.hydrological_toolkit.geo.geo_handler_cn import CNHandler
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to handle physics driver geo
class GeoDriver(object):

    def __init__(self, static_data_obj: xr.Dataset, ref_data_obj: xr.DataArray) -> None:

        self.static_data_obj = static_data_obj
        self.ref_data_obj = ref_data_obj

    # method to wrap physics routine(s)
    def wrap_geo(self) -> xr.Dataset:

        # method to organize, analyze and save area cell data object(s)
        drv_geo_area_cell = AreaCellHandler.select_data(self.static_data_obj,  self.ref_data_obj, var_name='area_cell')
        area_cell_info_obj = drv_geo_area_cell.organize_area_cell_info()

        # method to organize, analyze and save terrain data object(s)
        driver_geo_terrain = TerrainHandler.select_data(self.static_data_obj,  self.ref_data_obj, var_name='terrain')
        terrain_info_obj = driver_geo_terrain.organize_terrain_info(**area_cell_info_obj)

        driver_cn = CNHandler.select_data(self.static_data_obj,  self.ref_data_obj, var_name='curve_number')
        da_s = driver_cn.organize_info()

        dset_data = CNHandler.add_data(da_data=da_s, dset_data=self.static_data_obj, var_name='s')


        return dset_data
# ----------------------------------------------------------------------------------------------------------------------
