# libraries
import numpy as np
import pandas as pd
import xarray as xr

from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler
from hmc.hydrological_toolkit.geo.lib_geo_surface import compute_surface_parameters


class SurfaceHandler(GeoHandler):

    def __init__(self, da_uh: xr.DataArray, da_uc: xr.DataArray,
                 da_reference: xr.DataArray,
                 parameters: dict, constants: dict) -> None:

        self.da_uh = da_uh
        self.da_uc = da_uc

        self.da_reference = da_reference

        self.parameters = parameters
        self.constants = constants

        self.uh_tag = 'uh'
        self.uc_tag = 'uc'

        super().__init__(da_data=da_reference, da_reference=da_reference)

    def organize_data(self, dset_data: xr.Dataset = None,
                      dx: float = None, dy: float = None, **kwargs) -> xr.Dataset:

        if (dx is None) or (dy is None):
            raise ValueError('dx and dy must be provided')

        var_reference = self.da_reference.values
        var_uh = self.da_uh.values
        var_uc = self.da_uc.values

        var_uh, var_uc = compute_surface_parameters(
            uc=var_uc, uh=var_uh, reference=var_reference,
            dx=dx, dy=dy, bc=self.constants['bc'])

        da_uh = self.da_reference.copy()
        da_uh.values = var_uh
        da_uc = self.da_reference.copy()
        da_uc.values = var_uc

        dset_data = self.add_data_list(
            da_data_list=[da_uh, da_uc],
            dset_data=dset_data,
            var_name_list=[self.uh_tag, self.uc_tag])

        return dset_data
