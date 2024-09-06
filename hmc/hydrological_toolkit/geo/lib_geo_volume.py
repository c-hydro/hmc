# libraries
import numpy as np


# method to compute total volume
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
