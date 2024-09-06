# libraries
import numpy as np
import pandas as pd
import xarray as xr

from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler
from hmc.hydrological_toolkit.geo.lib_geo_volume import compute_volume_total


class VolumeHandler(GeoHandler):

    def __init__(self, da_s: xr.DataArray, da_reference: xr.DataArray, parameters: dict) -> None:

        self.da_s = da_s

        self.da_reference = da_reference

        self.parameters = parameters

        self.volume_tot_tag = 'vtot'

        super().__init__(da_data=da_s, da_reference=da_reference)

    def organize_data(self, dset_data: xr.Dataset = None, **kwargs) -> xr.Dataset:

        var_reference = self.da_reference.values
        var_s = self.da_s.values

        var_vtot = compute_volume_total(s=var_s, terrain=var_reference, cpi=self.parameters['cpi'])

        da_vtot = self.da_reference.copy()
        da_vtot.values = var_vtot

        dset_data = self.add_data_list(
            da_data_list=[da_vtot],
            dset_data=dset_data,
            var_name_list=[self.volume_tot_tag])

        return dset_data
