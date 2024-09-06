# libraries
import numpy as np
import xarray as xr
from hmc.hydrological_toolkit.geo.lib_geo_utils import mask_data_by_reference


# method to compute s information
def compute_cn2s(cn: np.ndarray, mask: np.ndarray) -> np.ndarray:

    cn[(cn < 0) | (cn > 100)] = np.nan
    cn[mask != 1] = np.nan

    s = (1000 / cn - 10) * 25.4

    s[s < 1] = 1
    s[s < 0] = 0
    s[mask < 0] = 0

    return s
