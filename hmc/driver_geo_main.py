# ----------------------------------------------------------------------------------------------------------------------
# libraries
import os
import warnings
import pandas as pd
import xarray as xr

from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler
from hmc.hydrological_toolkit.geo.geo_handler_area_cell import AreaCellHandler
from hmc.hydrological_toolkit.geo.geo_handler_terrain import TerrainHandler
from hmc.hydrological_toolkit.geo.geo_handler_cn import CNHandler

from hmc.hydrological_toolkit.geo.geo_handler_parameters import ParamsHandler
from hmc.hydrological_toolkit.geo.geo_handler_volume import VolumeHandler
from hmc.hydrological_toolkit.geo.geo_handler_lsm import LSMHandler
from hmc.hydrological_toolkit.geo.geo_handler_horton import HortonHandler
from hmc.hydrological_toolkit.geo.geo_handler_surface import SurfaceHandler

from hmc.hydrological_toolkit.constants.phys_constants_lsm import const_lsm
from hmc.hydrological_toolkit.constants.phys_constants_surface import const_surface
from hmc.hydrological_toolkit.variables.lib_variable_utils import extract_values_from_obj
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to handle physics driver geo
class GeoDriver(GeoHandler):

    def __init__(self, static_data_grid: xr.Dataset, static_data_array: dict,
                 reference_grid: xr.DataArray, parameters: dict) -> None:

        self.static_data_grid = static_data_grid
        self.static_data_array = static_data_array
        self.reference_grid = reference_grid
        self.parameters = parameters

    # method to wrap geo generic
    def wrap_geo_generic(self, dset_geo_generic: xr.Dataset) -> xr.Dataset:

        # initialize data grid
        dset_geo_tmp = self.static_data_grid.copy()

        # method to organize, analyze and save area cell object(s)
        drv_geo_area_cell = AreaCellHandler.select_data(
            self.static_data_grid,  self.reference_grid, var_name='area_cell')
        auxiliary_area_cell = drv_geo_area_cell.organize_auxiliary()

        # method to organize, analyze and save terrain object(s)
        driver_geo_terrain = TerrainHandler.select_data(
            self.static_data_grid,  self.reference_grid, var_name='terrain')
        auxiliary_terrain = driver_geo_terrain.organize_auxiliary()
        dset_geo_tmp = driver_geo_terrain.organize_data(dset_geo_tmp)

        # method to organize, analyze and save curve number object(s)
        driver_cn = CNHandler.select_data(
            self.static_data_grid,  da_reference=dset_geo_tmp['mask'], var_name='curve_number')
        dset_geo_tmp = driver_cn.organize_data(
            dset_geo_tmp, veg_ia_data=extract_values_from_obj(self.static_data_array['vegetation_ia']))

        # method to initialize class
        driver_params = ParamsHandler(da_ct=dset_geo_tmp['ct'], da_cf=dset_geo_tmp['cf'],
                                      da_uc=dset_geo_tmp['uc'], da_uh=dset_geo_tmp['uh'],
                                      da_reference=self.reference_grid,
                                      parameters=self.parameters)
        # method to organize and analyze data
        dset_geo_tmp = driver_params.organize_data(dset_geo_tmp)

        # method to update data
        dset_geo_generic = self.update_data(dset_geo_tmp, dset_geo_generic)

        return dset_geo_generic

    # method to wrap geo lsm
    def wrap_geo_lsm(self, dset_geo_generic: xr.Dataset, dset_geo_lsm: xr.Dataset) -> xr.Dataset:

        # method to initialize class
        driver_lsm = LSMHandler(da_ct=dset_geo_generic['ct'], da_ct_wp=dset_geo_generic['ct_wp'],
                                da_reference=self.reference_grid,
                                constants=const_lsm, parameters=self.parameters)
        # method to organize and analyze data
        dset_geo_tmp = driver_lsm.organize_data()
        # method to update data
        dset_geo_lsm = self.update_data(dset_geo_lsm, dset_geo_tmp)

        return dset_geo_lsm

    # method to wrap volume parameters
    def wrap_geo_volume(self, dset_geo_generic: xr.Dataset, dset_geo_volume: xr.Dataset) -> xr.Dataset:

        # method to organize, analyze and save volume object(s)
        driver_volume = VolumeHandler(da_s=dset_geo_generic['s'],
                                      da_terrain=dset_geo_generic['terrain'], da_ct=dset_geo_generic['ct'],
                                      da_reference=dset_geo_generic['mask'], parameters=self.parameters)
        # method to organize and analyze data
        dset_geo_tmp = driver_volume.organize_data()
        # method to update data
        dset_geo_volume = self.update_data(dset_geo_volume, dset_geo_tmp)

        return dset_geo_volume

    # method to wrap geo horton
    def wrap_geo_horton(self, dset_geo_generic: xr.Dataset, dset_geo_horton: xr.Dataset) -> xr.Dataset:

        # method to initialize class
        driver_horton = HortonHandler(
            da_s=dset_geo_generic['s'], da_cost_f=dset_geo_horton['cost_f'],
            da_cf=dset_geo_generic['cf'], da_ct=dset_geo_generic['ct'], da_ct_wp=dset_geo_generic['ct_wp'],
            da_reference=dset_geo_generic['mask'],
            parameters=self.parameters, constants={})
        # method to organize and analyze data
        dset_geo_tmp = driver_horton.organize_data()
        # method to update data
        dset_geo_horton = self.update_data(dset_geo_horton, dset_geo_tmp)

        return dset_geo_horton

    # method to wrap geo surface
    def wrap_geo_surface(self, dset_geo_generic: xr.Dataset, dset_geo_surface: xr.Dataset) -> xr.Dataset:

        # method to initialize class
        driver_surface = SurfaceHandler(da_reference=self.reference_grid, parameters=self.parameters)
        # method to organize and analyze data
        dset_geo_tmp = driver_surface.organize_data()
        # method to update data
        dset_geo_surface = self.update_data(dset_geo_surface, dset_geo_tmp)

        return dset_geo_surface
# ----------------------------------------------------------------------------------------------------------------------

