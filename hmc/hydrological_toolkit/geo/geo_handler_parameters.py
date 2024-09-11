# libraries
import xarray as xr

from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler
from hmc.hydrological_toolkit.geo.lib_geo_parameters import fill_holes_with_param


class ParamsHandler(GeoHandler):

    def __init__(self, da_ct: xr.DataArray, da_cf: xr.DataArray,
                 da_uc: xr.DataArray, da_uh: xr.DataArray,
                 da_reference: xr.DataArray, parameters: dict) -> None:

        self.da_ct = da_ct
        self.da_cf = da_cf
        self.da_uc = da_uc
        self.da_uh = da_uh

        self.da_reference = da_reference

        self.parameters = parameters

        self.tag_uc, self.tag_uh, self.tag_ct, self.tag_cf = 'uc', 'uh', 'ct', 'cf'

        super().__init__(da_data=da_reference, da_reference=da_reference)

    def organize_data(self, dset_data: xr.Dataset = None, **kwargs) -> xr.Dataset:

        ct = self.da_ct.values
        reference = self.da_reference.values

        var_ct, hole_ct = fill_holes_with_param(ct, terrain=reference, param=self.parameters['ct'])
        da_ct = self.da_ct.copy()
        da_ct.values = var_ct

        var_cf, hole_cf = fill_holes_with_param(self.da_cf.values, terrain=reference, param=self.parameters['cf'])
        da_cf = self.da_cf.copy()
        da_cf.values = var_cf

        var_uc, hole_uc = fill_holes_with_param(self.da_uc.values, terrain=reference, param=self.parameters['uc'])
        da_uc = self.da_uc.copy()
        da_uc.values = var_uc

        var_uh, hole_uh = fill_holes_with_param(self.da_uh.values, terrain=reference, param=self.parameters['uh'])
        da_uh = self.da_uh.copy()
        da_uh.values = var_uh

        da_ct = self.da_ct.copy()
        da_ct.values = var_ct

        dset_data = self.add_data_list(
            da_data_list=[self.da_ct, self.da_cf, self.da_uc, self.da_uh],
            dset_data=dset_data,
            var_name_list=[self.tag_ct, self.tag_cf, self.tag_uc, self.tag_uh])

        return dset_data
