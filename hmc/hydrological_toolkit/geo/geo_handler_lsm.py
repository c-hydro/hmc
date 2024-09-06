# libraries
import numpy as np
import pandas as pd
import xarray as xr

from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler
from hmc.hydrological_toolkit.geo.lib_geo_lsm import compute_beta_function_parameters, compute_ct_wp


class LSMHandler(GeoHandler):

    def __init__(self, da_ct: xr.DataArray, da_ct_wp: xr.DataArray, da_reference: xr.DataArray,
                 parameters: dict, constants: dict) -> None:

        self.da_ct = da_ct
        self.da_ct_wp = da_ct_wp

        self.da_reference = da_reference

        self.parameters = parameters
        self.constants = constants

        self.ct_wp_tag = 'ct_wp'
        self.kb1_tag = 'kb_1'
        self.kc1_tag = 'kc_1'
        self.kb2_tag = 'kb_2'
        self.kc2_tag = 'kc_2'

        super().__init__(da_data=da_reference, da_reference=da_reference)

    def organize_data(self, dset_data: xr.Dataset = None) -> xr.Dataset:

        var_reference = self.da_reference.values
        var_ct = self.da_ct.values
        var_ct_wp = self.da_ct_wp.values

        var_ct_wp = compute_ct_wp(ct=var_ct, ct_wp=var_ct_wp, reference=var_reference)

        var_kb1, var_kc1, var_kb2, var_kc2 = compute_beta_function_parameters(
            ct=var_ct, ct_wp=var_ct_wp, reference=var_reference,
            bf_min=self.constants['bf_min'], bf_max=self.constants['bf_max'])

        da_ct_wp = self.da_reference.copy()
        da_ct_wp.values = var_ct_wp

        da_kb1 = self.da_reference.copy()
        da_kb1.values = var_kb1
        da_kc1 = self.da_reference.copy()
        da_kc1.values = var_kc1
        da_kb2 = self.da_reference.copy()
        da_kb2.values = var_kb2
        da_kc2 = self.da_reference.copy()
        da_kc2.values = var_kc2

        dset_data = self.add_data_list(
            da_data_list=[da_ct_wp, da_kb1, da_kc1, da_kb2, da_kc2],
            dset_data=dset_data,
            var_name_list=[self.ct_wp_tag, self.kb1_tag, self.kc1_tag, self.kb2_tag, self.kc2_tag])

        return dset_data
