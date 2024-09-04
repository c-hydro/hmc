# libraries
import numpy as np
import xarray as xr
from hmc.hydrological_toolkit.geo.lib_geo_utils import mask_data_by_reference


def compute_volume_total(terrain: np.ndarray = None, s: np.ndarray = None, cpi: float = 0.0,) -> np.ndarray:

    """
    Expression: a2dVarVTot = dCPI/2*a2dVarS + dCPI/2*a2dVarS*(dVarDEMMax - a2dVarDEM)/dVarDEMMax
    :param s:
    :param terrain:
    :param cpi:
    :return: total volume
    """
    if terrain is None:
        raise ValueError('Terrain is not defined')
    if s is None:
        raise ValueError('S is not defined')

    volume_tot = cpi / 2 * s + cpi / 2 * s * (np.nanmax(terrain) - terrain) / np.nanmax(terrain)
    volume_tot[terrain < 0] = 0
    volume_tot[s < 0] = 0

    return volume_tot


# method to compute s information
def compute_cn2s(cn: np.ndarray, mask: np.ndarray) -> np.ndarray:

    cn[(cn < 0) | (cn > 100)] = np.nan
    cn[mask != 1] = np.nan

    s = (1000 / cn - 10) * 25.4

    s[s < 1] = 1
    s[s < 0] = 0
    s[mask < 0] = 0

    return s
