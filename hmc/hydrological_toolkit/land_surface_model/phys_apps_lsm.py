import numpy as np


def compute_beta_function(sm: np.ndarray, ct_wp: np.ndarray, ct: np.ndarray,
                  mask: np.ndarray, kb1: np.ndarray, kc1: np.ndarray,
                  bf_min: float, bf_max: float) -> (np.ndarray, np.ndarray):

    # Calculating Beta function values
    var_bf = np.zeros_like(sm)
    var_bf = np.where(mask > 0.0, bf_max, var_bf)
    var_bf = np.where((sm < ct_wp) & (mask > 0.0), bf_min, var_bf)
    var_bf = np.where((sm >= ct_wp) & (sm <= ct) & (mask > 0.0), kb1 * sm + kc1, var_bf)

    # Calculating Beta function values for bare soil
    var_bf_bare_soil = np.where(mask > 0.0, 1 + 1 / (np.exp(50.0 * (sm - ct_wp)) / (1000.0 * (ct - ct_wp) + 1.0)), 0.0)

    # Check beta limit(s) --> just in case
    var_bf = np.where(var_bf > 1.0, 1.0, var_bf)
    var_bf = np.where(var_bf <= 0.001, 0.001, var_bf)
    var_bf_bare_soil = np.where(var_bf_bare_soil > 1.0, 1.0, var_bf_bare_soil)
    var_bf_bare_soil = np.where(var_bf_bare_soil <= 0.001, 0.001, var_bf_bare_soil)

    return var_bf, var_bf_bare_soil


def compute_thermal_inertia():
    print('Thermal inertia')


def compute_richardson():
    print('Richardson')


def compute_tdeep():
    print('Tdeep')


def runge_kutta():
    print('Runge-Kutta')



