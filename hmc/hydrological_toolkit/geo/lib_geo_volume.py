# libraries
import numpy as np


# method to compute volume tot
def compute_volume_tot(terrain: np.ndarray = None, s: np.ndarray = None, cpi: float = 0.0,) -> np.ndarray:

    """
    Expression: v_tot = cpi / 2 * s + cpi / 2 * s * (max_terrain - terrain) / max_terrain
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


# method to compute total volume at wilting point
def compute_volume_tot_wp(v_tot: np.ndarray, terrain: np.ndarray, ct: np.ndarray, wp_factor: float = 0.4) -> np.ndarray:
    """
    :param v_tot:
    :param terrain:
    :param ct:
    :param wp_factor:
    :return: total volume at wilting point
    """
    if v_tot is None:
        raise ValueError('Total volume is not defined')
    if ct is None:
        raise ValueError('CT is not defined')

    var_volume_vtot_wp = np.zeros_like(v_tot)
    var_volume_vtot_wp = np.where(terrain >= 0, 0.0, var_volume_vtot_wp)
    # condizione che tagliava un 20% del vtot  a2dVarS * a2dVarCtWP ! ct_wp = 0.4*ct
    var_volume_vtot_wp[terrain < 0] = 0

    return var_volume_vtot_wp

