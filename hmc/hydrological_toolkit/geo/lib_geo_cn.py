# libraries
import numpy as np
import xarray as xr
from hmc.hydrological_toolkit.geo.lib_geo_utils import mask_data_by_reference


# method to compute s information
def compute_cn2s(da_cn: xr.DataArray, da_mask: xr.DataArray) -> xr.DataArray:

    da_s = da_cn.copy()

    values_cn = da_cn.values
    values_cn[(values_cn < 0) | (values_cn > 100)] = np.nan
    values_cn[da_mask.values != 1] = np.nan

    values_s = (1000 / values_cn - 10) * 25.4

    values_s[values_s < 1] = 1
    values_s[values_s < 0] = 0

    values_s[da_mask.values < 0] = 0

    da_s.values = values_s

    return da_s

