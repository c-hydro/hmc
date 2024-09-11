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
                 ref_data_obj: xr.DataArray, parameters: dict) -> None:

        self.static_data_grid = static_data_grid
        self.static_data_array = static_data_array
        self.ref_data_obj = ref_data_obj
        self.parameters = parameters

    # method to wrap physics routine(s)
    def wrap_geo(self) -> (xr.Dataset, xr.Dataset):

        # initialize data grid
        dset_geo = self.static_data_grid.copy()

        # method to organize, analyze and save area cell object(s)
        drv_geo_area_cell = AreaCellHandler.select_data(self.static_data_grid,  self.ref_data_obj, var_name='area_cell')
        auxiliary_area_cell = drv_geo_area_cell.organize_auxiliary()

        # method to organize, analyze and save terrain object(s)
        driver_geo_terrain = TerrainHandler.select_data(self.static_data_grid,  self.ref_data_obj, var_name='terrain')
        auxiliary_terrain = driver_geo_terrain.organize_auxiliary()
        dset_geo = driver_geo_terrain.organize_data(dset_geo)

        # method to organize, analyze and save curve number object(s)
        driver_cn = CNHandler.select_data(self.static_data_grid,  da_reference=dset_geo['mask'], var_name='curve_number')
        dset_geo = driver_cn.organize_data(
            dset_geo, veg_ia_data=extract_values_from_obj(self.static_data_array['vegetation_ia']))

        # method to organize, analyze and save parameters object(s)
        driver_params = ParamsHandler(da_ct=dset_geo['ct'], da_cf=dset_geo['cf'],
                                      da_uc=dset_geo['uc'], da_uh=dset_geo['uh'], da_reference=self.ref_data_obj,
                                      parameters=self.parameters)
        dset_params = driver_params.organize_data()

        # method to organize, analyze and save volume object(s)
        driver_volume = VolumeHandler(da_s=dset_geo['s'], da_terrain=dset_geo['terrain'],
                                      da_reference=dset_geo['mask'], parameters=self.parameters)
        dset_volume = driver_volume.organize_data()

        # method to organize, analyze and save land surface model object(s)
        driver_lsm = LSMHandler(da_ct=dset_geo['ct'], da_ct_wp=dset_geo['ct_wp'],  da_reference=self.ref_data_obj,
                                constants=const_lsm, parameters=self.parameters)

        dset_lsm = driver_lsm.organize_data()

        # method to organize, analyze and save horton object(s)
        driver_horton = HortonHandler(da_s=dset_geo['s'], da_cost_f=dset_geo['cost_f'],
                                      da_ct=dset_geo['ct'], da_cf=dset_geo['cf'], da_ct_wp=dset_lsm['ct_wp'],
                                      da_reference=self.ref_data_obj,
                                      constants=const_lsm, parameters=self.parameters)
        dset_horton = driver_horton.organize_data()

        # method to organize, analyze and save surface object(s)
        driver_surface = SurfaceHandler(da_uh=dset_geo['uh'], da_uc=dset_geo['uc'], da_reference=self.ref_data_obj,
                                        parameters=self.parameters, constants=const_surface)
        dset_surface = driver_surface.organize_data(**auxiliary_area_cell)

        return dset_geo, dset_params, dset_volume, dset_lsm, dset_horton, dset_surface

    @staticmethod
    def organize_geo(dset_data: xr.Dataset, dset_expected: xr.Dataset) -> xr.Dataset:

        vars_expected = list(dset_expected.variables)
        vars_dropped = []
        for var_name in vars_expected:
            if var_name in list(dset_data.variables):
                dset_expected[var_name] = dset_data[var_name]
            else:
                vars_dropped.append(var_name)
                warnings.warn(f'Variable {var_name} already exists in dset_data_grid')

        dset_expected = dset_expected.drop_vars(vars_dropped)

        return dset_expected
    # ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
