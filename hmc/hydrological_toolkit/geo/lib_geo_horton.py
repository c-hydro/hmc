# libraries
import numpy as np


# method to compute horton parameters
def compute_horton_parameters(
        ct: np.ndarray, cf: np.ndarray, s: np.ndarray, cost_f: np.ndarray, reference: np.ndarray) -> \
        (np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray):

    var_cost_f1 = np.zeros_like(reference)
    var_cost_f1 = np.where(reference >= 0, cf * cost_f, var_cost_f1)
    var_cost_f1[reference < 0] = -9999.0

    var_cost_ch_fix = np.zeros_like(reference)
    var_cost_ch_fix = np.where(reference >= 0, ((1 - ct) * cost_f + ct * var_cost_f1) / ((1 - ct) * s), var_cost_ch_fix)
    var_cost_ch_fix[reference < 0] = -9999.0

    var_c1 = np.zeros_like(reference)
    var_c1 = np.where(reference >= 0, var_cost_f1 * ct / (1 - ct), var_c1)
    var_c1[reference < 0] = -9999.0

    var_f2 = np.zeros_like(reference)
    var_f2 = np.where(reference >= 0, var_cost_f1 / (1 - ct), var_f2)
    var_f2[reference < 0] = -9999.0

    return var_cost_f1, var_cost_ch_fix, var_c1, var_f2
