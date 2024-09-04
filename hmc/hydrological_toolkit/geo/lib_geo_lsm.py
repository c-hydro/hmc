# libraries
import numpy as np


# method to compute beta function parameters
def compute_beta_function_parameters(
        ct: np.ndarray, ct_wp: np.ndarray, reference: np.ndarray,
        bf_min: float, bf_max: float) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray):

    var_kb1 = np.zeros_like(reference)
    var_kb1 = np.where(reference > 0.0, (bf_max - bf_min) / (ct - ct_wp), var_kb1)

    var_kc1 = np.zeros_like(reference)
    var_kc1 = np.where(reference > 0.0, bf_min - (bf_max - bf_min) / (ct - ct_wp) * ct_wp, var_kc1)

    var_kb2 = np.zeros_like(reference)
    var_kb2 = np.where(reference > 0.0, (1 - bf_max) / (1 - ct), var_kb2)

    var_kc2 = np.zeros_like(reference)
    var_kc2 = np.where(reference > 0.0, 1 - var_kb2, var_kc2)

    return var_kb1, var_kc1, var_kb2, var_kc2


# method to compute ct welting point
def compute_ct_wp(ct: np.ndarray, ct_wp: np.ndarray, reference: np.ndarray) -> np.ndarray:

    var_ct_wp = np.zeros_like(reference)
    var_ct_wp = np.where((reference >= 0) & (var_ct_wp <= 0), ct * 0.4, ct_wp)

    return var_ct_wp
