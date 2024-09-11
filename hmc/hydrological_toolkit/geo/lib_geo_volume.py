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

    max_terrain = np.nanmax(terrain)

    var_volume_vtot = np.zeros_like(terrain)
    var_volume_vtot = np.where(
        terrain >= 0,
        cpi / 2 * s + cpi / 2 * s * (max_terrain - terrain) / max_terrain, var_volume_vtot)

    var_volume_vtot[terrain < 0] = 0
    var_volume_vtot[s < 0] = 0

    return var_volume_vtot
