# libraries
import numpy as np
import pandas as pd
import xarray as xr

from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler
from hmc.hydrological_toolkit.geo.lib_geo_volume import compute_volume_tot, compute_volume_tot_wp


class VolumeHandler(GeoHandler):

    def __init__(self, da_s: xr.DataArray, da_terrain: xr.DataArray, da_ct: xr.DataArray,
                 da_reference: xr.DataArray, parameters: dict) -> None:

        self.da_s = da_s
        self.da_terrain = da_terrain
        self.da_ct = da_ct
        self.da_reference = da_reference

        self.parameters = parameters

        self.tag_volume_tot = 'v_tot'
        self.tag_volume_tot_wp = 'v_tot_wp'

        super().__init__(da_data=da_s, da_reference=da_reference)

    def organize_data(self, dset_data: xr.Dataset = None, **kwargs) -> xr.Dataset:

        # get data
        var_terrain = self.da_terrain.values
        var_s = self.da_s.values
        var_ct = self.da_ct.values

        # define volume tot
        var_v_tot = compute_volume_tot(s=var_s, terrain=var_terrain, cpi=self.parameters['cpi'])
        da_v_tot = self.da_reference.copy()
        da_v_tot.values = var_v_tot

        # define volume tot at wilting point
        var_v_tot_wp = compute_volume_tot_wp(v_tot=var_v_tot, terrain=var_terrain, ct=var_ct)
        da_v_tot_wp = self.da_reference.copy()
        da_v_tot_wp.values = var_v_tot_wp

        # add data to dataset
        dset_data = self.add_data_list(
            da_data_list=[da_v_tot, da_v_tot_wp],
            dset_data=dset_data,
            var_name_list=[self.tag_volume_tot, self.tag_volume_tot_wp ])

        return dset_data
