# libraries
import xarray as xr

from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler


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

        dset_data = self.add_data_list(
            da_data_list=[self.da_ct, self.da_cf, self.da_uc, self.da_uh],
            dset_data=dset_data,
            var_name_list=[self.tag_ct, self.tag_cf, self.tag_uc, self.tag_uh])

        return dset_data
