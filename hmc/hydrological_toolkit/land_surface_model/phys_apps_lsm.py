# libraries
import numpy as np
from copy import deepcopy

import matplotlib.pyplot as plt


# method to compute beta function
def compute_beta_function(sm: np.ndarray, ct_wp: np.ndarray, ct: np.ndarray,
                          mask: np.ndarray, kb1: np.ndarray, kc1: np.ndarray,
                          bf_min: float, bf_max: float) -> (np.ndarray, np.ndarray):

    # compute beta function values
    var_bf = np.zeros_like(sm)
    var_bf = np.where(mask > 0.0, bf_max, var_bf)
    var_bf = np.where(((sm >= ct_wp) & (sm <= ct)) & (mask > 0.0), kb1 * sm + kc1, var_bf)
    var_bf = np.where((sm < ct_wp) & (mask > 0.0), bf_min, var_bf)
    var_bf = np.where(var_bf > 1.0, 1.0, var_bf)
    var_bf = np.where(var_bf <= 0.001, 0.001, var_bf)

    # compute beta function values for bare soil
    var_bf_bare_soil = np.zeros_like(sm)
    var_bf_bare_soil = np.where(
        mask > 0.0, 1 + 1 / (np.exp(50.0 * (sm - ct_wp)) / (1000.0 * (ct - ct_wp) + 1.0)), var_bf_bare_soil)
    var_bf_bare_soil = np.where(var_bf > 1.0, 1.0, var_bf_bare_soil)
    var_bf_bare_soil = np.where(var_bf <= 0.001, 0.001, var_bf_bare_soil)

    return var_bf, var_bf_bare_soil


def compute_thermal_inertia(sm: np.ndarray, mask: np.ndarray,
                            rho_s: float, rho_w: float, cp_s: float, cp_w: float,
                            kq: float, kw: float, ko: float, fq_s: float, por_s: float):

    # variable(s) conditions
    var_sm = deepcopy(sm)
    var_sm = np.where((mask == 1.0) & (sm > 1.0), 1.0, var_sm)
    var_sm = np.where((mask == 1.0) & (sm < 0.0), 0.0, var_sm)

    # quartz soil fraction [%]
    var_fq_s = np.zeros_like(sm)
    var_fq_s = np.where(mask == 1.0, fq_s, var_fq_s)

    # heat capacity [J K^-1 m^-3]
    var_c = np.zeros_like(sm)
    var_c = np.where(mask == 1.0, (1 - por_s) * rho_s * cp_s + por_s * sm * rho_w * cp_w, var_c)

    # air dry density [kg m^-3]
    rho_da = (1 - por_s) * rho_s
    # air dry conductivity [W m^-1 K^-1]
    k_da = (0.135 * rho_da + 64.7) / (rho_s - 0.947 * rho_da)

    # solids conductivity [W m^-1 K^-1]
    var_k_sol = kq ** var_fq_s * ko ** (1 - var_fq_s)
    var_k_sol = np.where(mask == 0.0, 0.0, var_k_sol)
    # saturated soil conductivity [W m^-1 K^-1]
    var_k_sol_sat = var_k_sol ** (1 - por_s) * kw ** por_s
    var_k_sol_sat = np.where(mask == 0.0, 0.0, var_k_sol_sat)

    # Kersten number (funzione solo del grado di saturazione VV per terreni sottili)
    var_ke = np.where((mask == 1.0) & (var_sm >= 0.1), np.log10(var_sm) + 1, np.log10(0.1) + 1)
    var_ke = np.where(mask == 0.0, 0.0, var_ke)

    # soil thermal conductivity [W m^-1 K^-1]
    var_ks = var_ke * (var_k_sol_sat - k_da) + k_da
    var_ks = np.where(mask == 0.0, 0.0, var_ks)

    # thermal inertia[J m^-2 K S^-(1/2)]
    var_pit = np.zeros_like(sm)
    var_pit = np.where(mask == 1.0, np.sqrt(var_c * var_ks), var_pit)
    # thermal inertia scaling (to reduce max values from 2500 to 600 --> temporary fixing)
    var_pit = var_pit / 5 + 1500
    var_pit = np.where(mask == 0.0, 0.0, var_pit)

    return var_pit


def compute_richardson(wind: np.ndarray, ta_k: np.ndarray, pa: np.ndarray,
                       lst: np.ndarray, mask: np.ndarray,
                       rd: float, cp: float, g: float, z_ref: float) -> np.ndarray:

    plt.figure(); plt.imshow(wind); plt.colorbar();
    plt.figure(); plt.imshow(ta_k); plt.colorbar();
    plt.figure(); plt.imshow(pa); plt.colorbar();
    plt.figure(); plt.imshow(lst); plt.colorbar();
    plt.show()


    """
             call debug_2dVar(dble(a2dVarWind), iRows, iCols, 1, 2)
     call debug_2dVar(dble(a2dVarTaK), iRows, iCols, 2, 2)
     call debug_2dVar(dble(a2dVarPa), iRows, iCols, 3, 2)
     call debug_2dVar(dble(a2dVarLST), iRows, iCols, 4, 2)     
     call debug_2dVar(dble(a2dVarTp), iRows, iCols, 5, 2)
     call debug_2dVar(dble(a2dVarTp0), iRows, iCols, 6, 2)
     call debug_2dVar(dble(a2dVarRb), iRows, iCols, 7, 2)
     """

    """
            !------------------------------------------------------------------------------------------
        ! Variable(s) initialization
        a2dVarTp = 0.0; a2dVarTp0 = 0.0; a2dVarRb = -0.9
        !------------------------------------------------------------------------------------------

        !------------------------------------------------------------------------------------------
        ! Calculating distributed Richardson number (Richardson from -1 to 0 values)
        where((a2dVarDEM.gt.0.0) .and. (a2dVarWind.gt.0.0))

            a2dVarTp = a2dVarTaK*(1000.0/a2dVarPa)**(dRd/dCp)
            a2dVarTp0 = a2dVarLST*(1000.0/a2dVarPa)**(dRd/dCp)
            a2dVarRb = (dG/a2dVarTp)*(a2dVarTp - a2dVarTp0)*dZRef/(a2dVarWind**2)

        elsewhere(a2dVarDEM.gt.0.0)

            a2dVarTp = a2dVarTaK*(1000.0/a2dVarPa)**(dRd/dCp)
            a2dVarTp0 = a2dVarLST*(1000.0/a2dVarPa)**(dRd/dCp)
            a2dVarRb = (dG/a2dVarTp)*(a2dVarTp - a2dVarTp0)*dZRef/(0.1**2)

        elsewhere(a2dVarDEM.le.0.0)

            a2dVarRb = 0.0
            a2dVarTp0 = 0.0
            a2dVarTp = 0.0

        endwhere
        !------------------------------------------------------------------------------------------
    :return:
    """

    print('Richardson')


def compute_tdeep():
    print('Tdeep')


def runge_kutta():
    print('Runge-Kutta')



