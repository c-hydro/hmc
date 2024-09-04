# libraries
import numpy as np
import xarray as xr

from hmc.hydrological_toolkit.geo.lib_geo_cn import compute_cn2s
from hmc.hydrological_toolkit.geo.lib_geo_vegetation import compute_cost_f
from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler

from hmc.hydrological_toolkit.constants.phys_constants_vegetation import const_vegetation


class CNHandler(GeoHandler):

    def __init__(self, da_cn: xr.DataArray, da_reference: xr.DataArray) -> None:

        self.s_tag = 's'
        self.cost_f_tag = 'cost_f'

        super().__init__(da_data=da_cn, da_reference=da_reference)

    # method to organize data
    def organize_data(self, dset_data: xr.Dataset = None, veg_ia_data: np.ndarray = None) -> xr.Dataset:

        cn = self.da_data.values
        reference = self.da_reference.values

        if dset_data is None:
            raise ValueError('Dataset object is required to organize data')
        if veg_ia_data is None:
            veg_ia_data = np.array(const_vegetation['veg_ia'])
        if veg_ia_data.ndim == 2:
            veg_ia_data = veg_ia_data[:, 1]

        cost_f = compute_cost_f(cn=cn, veg_ia=veg_ia_data)
        s = compute_cn2s(cn=cn, mask=reference)

        da_cost_f = self.da_reference.copy()
        da_cost_f.values = cost_f
        da_s = self.da_reference.copy()
        da_s.values = s

        dset_data = self.add_data(da_data=da_s, dset_data=dset_data, var_name=self.s_tag)
        dset_data = self.add_data(da_data=da_cost_f, dset_data=dset_data, var_name=self.cost_f_tag)

        return dset_data
