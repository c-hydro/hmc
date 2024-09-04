# libraries
import numpy as np


# method to compute surface parameters (change units)
def compute_surface_parameters(uh: np.ndarray, uc: np.ndarray, reference: np.ndarray,
                               dx: float, dy: float, bc: float) -> (np.ndarray, np.ndarray):

    """
    :param uh:
    :param uc:
    :param reference:
    :param dx:
    :param dy:
    :param bc:
    :return: uh, uc
    """
    var_uh = np.zeros_like(uh)
    var_uh = np.where(
        (reference > 0.0) & (uh < 0.05), uh * 3600, var_uh)

    var_uc = np.zeros_like(uc)
    var_uc = np.where(
        (reference > 0.0) & (uh < 0.05), uc * (3600 * 1000) / (np.sqrt(dx * dy) * 1000 ** (bc + 1)), var_uc)

    return var_uh, var_uc
