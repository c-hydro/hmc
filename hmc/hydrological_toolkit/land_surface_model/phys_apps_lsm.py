# libraries
import numpy as np
from copy import deepcopy

import matplotlib.pyplot as plt


# method to compute beta function
def compute_beta_function(sm: np.ndarray, ct_wp: np.ndarray, ct: np.ndarray,
                          mask: np.ndarray, kb1: np.ndarray, kc1: np.ndarray,
                          bf_min: float, bf_max: float, **kwargs) -> (np.ndarray, np.ndarray):

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
                            kq: float, kw: float, ko: float, fq_s: float, por_s: float, **kwargs) -> np.ndarray:

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


# method to compute richardson number
def compute_richardson(wind: np.ndarray, ta_k: np.ndarray, pa: np.ndarray,
                       lst: np.ndarray, mask: np.ndarray,
                       rd: float, cp: float, g: float, z_ref: float, **kwargs) -> np.ndarray:

    var_tp = np.zeros_like(mask)
    var_tp = np.where(mask == 0.0, 0.0, var_tp)
    var_tp = np.where(mask == 1.0, ta_k * (1000.0 / pa) ** (rd / cp), var_tp)
    var_tp = np.where((mask == 1.0) & (wind > 0.0), ta_k * (1000.0 / pa) ** (rd / cp), var_tp)
    var_tp[mask == 0.0] = np.nan

    var_tp0 = np.zeros_like(mask)
    var_tp0 = np.where(mask == 0.0, 0.0, var_tp0)
    var_tp0 = np.where(mask == 1.0, lst * (1000.0 / pa) ** (rd / cp), var_tp0)
    var_tp0 = np.where((mask == 1.0) & (wind > 0.0), lst * (1000.0 / pa) ** (rd / cp), var_tp0)
    var_tp0[mask == 0.0] = np.nan

    var_rb = np.zeros_like(mask)
    var_rb[:, :] = -0.9
    var_rb = np.where(mask == 0.0, 0.0, var_rb)
    var_rb = np.where((mask == 1.0) % (wind <= 0.0), (g / var_tp) * (var_tp - var_tp0) * z_ref / (0.1 ** 2), var_rb)
    var_rb = np.where((mask == 1.0) & (wind > 0.0), (g / var_tp) * (var_tp - var_tp0) * z_ref / (wind ** 2), var_rb)
    var_rb[mask == 0.0] = np.nan

    return var_rb


# method to compute deep soil temperature
def compute_td(ta_k: np.ndarray, ta_k_marked: np.ndarray, ta_k_day: np.ndarray, mask: np.ndarray,
               t_ref: float, time_step_day: int = 24, time_step_marked: int = 3, time_step_shift: int = 2, **kwargs) \
        -> (np.ndarray, np.ndarray, np.ndarray):

    if np.all(ta_k_day <= 0.0):
        ta_k_day[:, :, :] = ta_k
        ta_k_day[time_step_day - 1, :, :] = ta_k + 10.0
        ta_k_day = np.where(mask == 0.0, 0.0, ta_k_day)
    else:
        ta_k_day[1:time_step_day, :, :] = ta_k_day[0:time_step_day-1, :, :]
        ta_k_day[time_step_day - 1, :, :] = ta_k
        ta_k_day = np.where(mask == 0.0, 0.0, ta_k_day)

    ta_k_day_avg_all = np.sum(ta_k_day[0:time_step_day, :, :], axis=0) / time_step_day
    ta_k_day_avg_all = np.where(mask == 0.0, 0.0, ta_k_day_avg_all)
    ta_k_day_avg_half = np.sum(ta_k_day[(time_step_day//2 + 1):time_step_day, :, :], axis=0) / (time_step_day//2)
    ta_k_day_avg_half = np.where(mask == 0.0, 0.0, ta_k_day_avg_half)

    if np.all(ta_k_marked <= 0.0):
        ta_k_marked[0:time_step_marked, :, :] = t_ref + 17.3
    else:
        ta_k_marked[1:time_step_marked, :, :] = ta_k_marked[0:time_step_marked-1, :]
        ta_k_marked[time_step_marked - 1, :, :] = ta_k_day_avg_all + (ta_k_day_avg_half - ta_k_day_avg_all) / np.exp(1.0)
        ta_k_marked = np.where(mask == 0.0, 0.0, ta_k_marked)

    time_step_td = int(time_step_marked - time_step_shift * 24/time_step_day)
    td = ta_k_marked[time_step_td, :, :]
    td = np.where(mask == 0.0, 0.0, td)

    return td, ta_k_day, ta_k_marked


# method to compute ch
def compute_ch(wind: np.ndarray, bf: np.ndarray, rb: np.ndarray, mask: np.ndarray,
               ch: float = -7.3) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):

    # compute static values
    var_psi = np.log(2.0)
    var_ch_n = np.exp(ch)

    # compute psi stable values (from 1 to 3)
    var_psi_stable = np.zeros_like(mask)
    var_psi_stable = np.where(mask == 1.0, 1.0, var_psi_stable)
    var_psi_stable = np.where((rb <= 0.0) & (mask > 0.0), 1 + np.exp(var_psi) * (1 - np.exp(10 * rb)), var_psi_stable)

    # compute ch values
    var_ch = np.zeros_like(mask)
    var_ch = np.where((mask == 1.0) & (wind > 0), var_ch_n * var_psi_stable, var_ch)

    # compute resistances
    var_ratm = np.zeros_like(mask)
    var_ratm = np.where(mask == 1.0, 10000.0, var_ratm)
    var_ratm = np.where((mask == 1.0) & (wind > 0), 1.0 / (var_ch * wind), var_ratm)

    var_rsurf = np.zeros_like(mask)
    var_rsurf = np.where(mask == 1.0, 10000.0, var_rsurf)
    var_rsurf = np.where((mask == 1.0) & (wind > 0), var_ratm / bf, var_rsurf)

    var_rsurf_pot = np.zeros_like(mask)
    var_rsurf_pot = np.where(mask == 1.0, 10000.0, var_rsurf_pot)
    var_rsurf_pot = np.where((mask == 1.0) & (wind > 0), var_ratm, var_rsurf_pot)

    return var_ch, var_ratm, var_rsurf, var_rsurf_pot


# method to compute land surface temperature
def compute_lst(ta_k: np.ndarray, airp: np.ndarray,
                lst: np.ndarray,
                td: np.ndarray, pit: np.ndarray,
                ratm: np.ndarray, rsurf: np.ndarray,
                rn: np.ndarray, lambda_v: np.ndarray, ea: np.ndarray, rhoa: np.ndarray,
                mask: np.ndarray,
                t_ref: float, lst_delta_max: float, cp: float,
                dt_data_src: int = 3600, dt_delta_min: int = 900,
                **kwargs) -> np.ndarray:

    # compute land surface temperature integrating delta for runge-kutta method
    dt_delta_min = min(int(dt_data_src), dt_delta_min)
    dt_delta_steps = int(int(dt_data_src) / int(dt_delta_min))

    # get land surface temperature
    lst = np.where(mask == 1, lst, np.nan)
    lst_prev = np.zeros_like(lst)
    lst_prev = np.where(mask == 1, lst, lst_prev)

    # iterate over delta steps
    for i_step in range(0, dt_delta_steps):

        print(i_step)

        # solve runge-kutta 4th order
        lst_upd = solve_rk4(
            int_delta=dt_delta_min,
            ta_k=ta_k, airp=airp,
            lst_in=deepcopy(lst_prev), td=td, pit=pit,ratm=ratm, rsurf=rsurf,
            rn=rn, lmda=lambda_v, ea=ea, rhoa=rhoa,
            mask=mask, t_ref=t_ref, lst_delta_max=lst_delta_max, cp=cp)

        # update land surface temperature (after each step)
        lst_prev = deepcopy(lst_upd)

    # check land surface temperature
    lst_upd = np.where(mask == 1, lst_upd, 0)
    # check land surface temperature min
    lst_upd = np.where(lst_upd < (273.15 - 70.0), lst, lst_upd)
    # check land surface temperature delta max
    lst_upd = np.where(lst_upd > (lst_delta_max * dt_data_src/3600), lst, lst_upd)

    # check land surface temperature min or max (after previous checks)
    lst_upd = np.where((lst_upd < (273.15 - 70.0)) | (lst_upd > (273.15 + 70.0)), 273.15 + 20, lst_upd)
    lst_upd = np.where(mask == 1, lst_upd, np.nan)

    return lst_upd


# method to solve runge-kutta 4th order
def solve_rk4(
        int_delta: float,
        ta_k: np.ndarray, airp: np.ndarray,
        lst_in: np.ndarray,
        td: np.ndarray, pit: np.ndarray,
        ratm: np.ndarray, rsurf: np.ndarray,
        rn: np.ndarray, lmda: np.ndarray, ea: np.ndarray, rhoa: np.ndarray,
        mask: np.ndarray,
        t_ref: float = 273.15, lst_delta_max: float = 40.0, cp: float = 1004.0) -> np.ndarray:

    # define constants
    pi_greco = 3.14
    omega = 1.0 / (60.0 * 60.0 * 24.0)

    # initialize variables
    lst_out = deepcopy(lst_in)

    # compute K1 argument
    k1 = int_delta * (2 * np.sqrt(pi_greco * omega) / pit * (
            rn - rhoa * cp * (lst_out - ta_k) / ratm -
            rhoa * lmda * (0.611 * np.exp(17.3 * (lst_in - t_ref) / (237.3 + lst_in - t_ref)) - ea) / (
                    airp * rsurf) * 0.622) - 2 * pi_greco * omega * (lst_in - td))
    k1 = np.where(k1 > lst_delta_max, lst_delta_max, k1)

    # update LST using K1 argument
    lst_out = lst_in + k1 / 2.0

    # compute K2 argument
    k2 = int_delta * (2 * np.sqrt(pi_greco * omega) / pit * (
            rn - rhoa * cp * (lst_out - ta_k) / ratm -
            rhoa * lmda * (0.611 * np.exp(17.3 * (lst_out - t_ref) / (237.3 + lst_out - t_ref)) - ea) / (
                    airp * rsurf) * 0.622) - 2 * pi_greco * omega * (lst_out - td))
    k2 = np.where(k2 > lst_delta_max, lst_delta_max, k2)

    # update LST using K2 argument
    lst_out = lst_in + k2 / 2.0

    # compute K3 argument
    k3 = int_delta * (2 * np.sqrt(pi_greco * omega) / pit * (
            rn - rhoa * cp * (lst_out - ta_k) / ratm -
            rhoa * lmda * (0.611 * np.exp(17.3 * (lst_out - t_ref) / (237.3 + lst_out - t_ref)) - ea) / (
                    airp * rsurf) * 0.622) - 2 * pi_greco * omega * (lst_out - td))
    k3 = np.where(k3 > (lst_delta_max / 2), lst_delta_max / 2, k3)

    # update LST using K3 argument
    lst_out = lst_in + k3

    # compute K4 argument
    k4 = int_delta * (2 * np.sqrt(pi_greco * omega) / pit * (
            rn - rhoa * cp * (lst_out - ta_k) / ratm -
            rhoa * lmda * (0.611 * np.exp(17.3 * (lst_out - t_ref) / (237.3 + lst_out - t_ref)) - ea) / (
                    airp * rsurf) * 0.622) - 2 * pi_greco * omega * (lst_out - td))
    k4 = np.where(k4 > lst_delta_max, lst_delta_max, k4)

    # update LST using K4 argument
    lst_out = lst_in + (k1 + 2 * (k2 + k3) + k4) / 6.0

    # apply mask
    lst_out = np.where(mask == 1, lst_out, 0)

    return lst_out
