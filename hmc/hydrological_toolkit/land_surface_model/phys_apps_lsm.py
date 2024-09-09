# libraries
import numpy as np

import matplotlib.pyplot as plt


# method to compute beta function
def compute_beta_function(sm: np.ndarray, ct_wp: np.ndarray, ct: np.ndarray,
                  mask: np.ndarray, kb1: np.ndarray, kc1: np.ndarray,
                  bf_min: float, bf_max: float) -> (np.ndarray, np.ndarray):

    # compute beta function values
    var_bf = np.zeros_like(sm)
    var_bf = np.where(mask > 0.0, bf_max, var_bf)
    var_bf = np.where((sm < ct_wp) & (mask > 0.0), bf_min, var_bf)
    var_bf = np.where(((sm >= ct_wp) & (sm <= ct)) & (mask > 0.0), kb1 * sm + kc1, var_bf)
    var_bf = np.where(var_bf > 1.0, 1.0, var_bf)
    var_bf = np.where(var_bf <= 0.001, 0.001, var_bf)

    """
        where (a2dVarSM.lt.a2dVarCtWP.and.a2dVarDEM.gt.0.0)
                a2dVarBF = dBFMin
        elsewhere ((a2dVarSM.ge.a2dVarCtWP).and.(a2dVarSM.le. (a2dVarCt)).and.(a2dVarDEM.gt.0.))
                a2dVarBF = a2dVarKb1*a2dVarSM + a2dVarKc1
        elsewhere (a2dVarDEM.gt.0.0)
                a2dVarBF = dBFMax       
        endwhere
    """


    plt.figure()
    plt.imshow(var_bf)
    plt.colorbar()
    plt.show()

    # compute beta function values for bare soil
    var_bf_bare_soil = np.where(
        mask > 0.0, 1 + 1 / (np.exp(50.0 * (sm - ct_wp)) / (1000.0 * (ct - ct_wp) + 1.0)), 0.0)
    var_bf_bare_soil = np.where(var_bf_bare_soil > 1.0, 1.0, var_bf_bare_soil)
    var_bf_bare_soil = np.where(var_bf_bare_soil <= 0.001, 0.001, var_bf_bare_soil)

    plt.figure()
    plt.imshow(var_bf)
    plt.colorbar()
    plt.figure()
    plt.imshow(var_bf_bare_soil)
    plt.colorbar()
    plt.show()

    return var_bf, var_bf_bare_soil


def compute_thermal_inertia():
    print('Thermal inertia')


def compute_richardson():
    print('Richardson')


def compute_tdeep():
    print('Tdeep')


def runge_kutta():
    print('Runge-Kutta')


