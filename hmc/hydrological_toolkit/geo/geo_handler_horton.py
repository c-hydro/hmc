# libraries
import numpy as np
import pandas as pd
import xarray as xr

from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler
from hmc.hydrological_toolkit.geo.lib_geo_horton import compute_horton_parameters


class HortonHandler(GeoHandler):

    def __init__(self, da_s: xr.DataArray, da_cost_f: xr.DataArray,
                 da_cf: xr.DataArray, da_ct: xr.DataArray, da_ct_wp: xr.DataArray,
                 da_reference: xr.DataArray,
                 parameters: dict, constants: dict = None) -> None:

        self.da_s = da_s
        self.da_cf = da_cf
        self.da_ct = da_ct
        self.da_ct_wp = da_ct_wp
        self.da_cost_f = da_cost_f

        self.da_reference = da_reference

        self.parameters = parameters
        self.constants = constants

        self.tag_cost_f1 = 'cost_f'
        self.tag_cost_ch_fix = 'cost_ch_fix'
        self.tag_c1 = 'c1'
        self.tag_f2 = 'f2'

        super().__init__(da_data=da_reference, da_reference=da_reference)

    def organize_data(self, dset_data: xr.Dataset = None) -> (xr.DataArray, xr.DataArray, xr.DataArray, xr.DataArray):

        var_reference = self.da_reference.values
        var_cf = self.da_cf.values
        var_ct = self.da_ct.values
        var_cost_f = self.da_cost_f.values
        var_s = self.da_s.values

        var_cost_f1, var_cost_ch_fix, var_c1, var_f2 = compute_horton_parameters(
            ct=var_ct, cf=var_cf, s=var_s, cost_f=var_cost_f, reference=var_reference)

        da_cost_f1 = self.da_reference.copy()
        da_cost_f1.values = var_cost_f1
        da_cost_ch_fix = self.da_reference.copy()
        da_cost_ch_fix.values = var_cost_ch_fix
        da_c1 = self.da_reference.copy()
        da_c1.values = var_c1
        da_f2 = self.da_reference.copy()
        da_f2.values = var_f2

        dset_data = self.add_data_list(
            da_data_list=[da_cost_f1, da_cost_ch_fix, da_c1, da_f2],
            dset_data=dset_data,
            var_name_list=[self.tag_cost_f1, self.tag_cost_ch_fix, self.tag_c1, self.tag_f2])

        return dset_data
