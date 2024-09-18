# libraries
import numpy as np
import pandas as pd
import xarray as xr

from hmc.generic_toolkit.time.lib_time_utils import compute_value_by_date

from hmc.hydrological_toolkit.constants.phys_constants_lsm import const_lsm as constants
from hmc.hydrological_toolkit.variables.lib_variable_utils import create_dict_from_dset, get_variable_data
from hmc.hydrological_toolkit.land_surface_model.phys_apps_lsm import (
    compute_beta_function, compute_thermal_inertia, compute_richardson, compute_td, compute_ch, compute_lst)


# class to handle land surface model
class LSMHandler:

    def __init__(self, dset_geo_generic: xr.Dataset, dset_geo_parameters: xr.Dataset,
                 dset_geo_lsm: xr.Dataset, dset_geo_routing: xr.Dataset,
                 da_reference: xr.DataArray,
                 time_step: pd.Timestamp, time_info: dict,
                 dt_delta_src: int = 3600, dt_delta_min: int = 900) -> None:

        self.dset_geo_generic = dset_geo_generic
        self.dset_geo_parameters = dset_geo_parameters
        self.dset_geo_lsm = dset_geo_lsm
        self.dset_geo_routing = dset_geo_routing

        self.da_reference = da_reference

        self.time_step = time_step
        self.time_info = time_info

        self.time_steps_day = time_info['time_steps_day']
        self.time_steps_marked = time_info['time_steps_marked']

        self.dt_delta_src = dt_delta_src
        self.dt_delta_min = dt_delta_min

        self.t_ref = constants['t_ref']
        self.z_ref = constants['z_ref']
        self.g = constants['g']
        self.bf_min = constants['bf_min']
        self.bf_max = constants['bf_max']
        self.rd = constants['rd']
        self.cp = constants['cp']
        self.cp_s = constants['cp_s']
        self.cp_w = constants['cp_w']
        self.rho_s = constants['rho_s']
        self.rho_w = constants['rho_w']
        self.eps_s = constants['eps_s']
        self.fq_s = constants['fq_s']
        self.ko = constants['ko']
        self.kw = constants['kw']
        self.kq = constants['kq']
        self.porosity_s = constants['porosity_s']
        self.sigma = constants['sigma']
        self.lst_delta_max = constants['lst_delta_max']
        self.td_steps_shift = constants['td_steps_shift']

        self.ch = compute_value_by_date(data=constants['ch'], time=self.time_step)
        self.albedo = compute_value_by_date(data=constants['albedo'], time=self.time_step)

    def execute(self, dset_data: xr.Dataset,
                dset_phys_lsm: xr.Dataset, dset_phys_volume: xr.Dataset) -> None:

        # get variables geo
        var_mask = get_variable_data(self.dset_geo_generic, var_name='mask', var_mandatory=True)
        var_s = get_variable_data(self.dset_geo_generic, var_name='s', var_mandatory=True)

        # get variables lsm
        var_ct_wp = get_variable_data(self.dset_geo_lsm, var_name='ct_wp', var_mandatory=True)
        var_kb_1 = get_variable_data(self.dset_geo_lsm, var_name='kb_1', var_mandatory=True)
        var_kc_1 = get_variable_data(self.dset_geo_lsm, var_name='kc_1', var_mandatory=True)
        # get variables routing
        var_ct = get_variable_data(self.dset_geo_parameters, var_name='ct', var_mandatory=True)

        # get variables physics
        var_tair_k_day = get_variable_data(dset_phys_lsm, var_name='tak_step_day', var_mandatory=True)
        var_tair_k_marked = get_variable_data(dset_phys_lsm, var_name='tak_step_marked', var_mandatory=True)
        var_lst = get_variable_data(dset_phys_lsm, var_name='lst', var_mandatory=True)
        var_vtot = get_variable_data(dset_phys_volume, var_name='vtot', var_mandatory=True)

        # get variables data
        var_tair_c = get_variable_data(dset_data, var_name='airt', var_mandatory=True)
        var_rh = get_variable_data(dset_data, var_name='rh', var_mandatory=True)
        var_inc_rad = get_variable_data(dset_data, var_name='inc_rad', var_mandatory=True)
        var_wind = get_variable_data(dset_data, var_name='wind', var_mandatory=True)
        var_pair = get_variable_data(dset_data, var_name='airp', var_mandatory=False)

        # adapt variables
        var_tair_k = var_tair_c + self.t_ref
        var_rh = var_rh / 100.0
        var_sm = var_vtot / var_s

        # initialize variables (initial step)
        if np.all(var_lst <= 0.0):
            var_lst = np.where((var_tair_c >= -40.0) & (var_mask > 0.0), var_tair_k + 1.0, var_lst)

        # method to compute beta function
        var_bf, var_bf_bare_soil = compute_beta_function(
            sm=var_sm, ct_wp=var_ct_wp, ct=var_ct,  mask=var_mask, kb1=var_kb_1, kc1=var_kc_1,
            bf_min=self.bf_min, bf_max=self.bf_max)

        # method to compute thermal inertia
        var_pit = compute_thermal_inertia(sm=var_sm, mask=var_mask,
                                          rho_s=self.rho_s, rho_w=self.rho_w,
                                          cp_s=self.cp_s, cp_w=self.cp_w, kq=self.kq, kw=self.kw, ko=self.ko,
                                          fq_s=self.fq_s, por_s=self.porosity_s)

        # method to compute Richardson number
        var_rb = compute_richardson(wind=var_wind, ta_k=var_tair_k, pa=var_pair, lst=var_lst, mask=var_mask,
                                    rd=self.rd, cp=self.cp, g=self.g, z_ref=self.z_ref)

        # compute deep soil temperature
        var_td, var_tair_k_day, var_tair_k_marked = compute_td(
            ta_k=var_tair_k, ta_k_day=var_tair_k_day, ta_k_marked=var_tair_k_marked, mask=var_mask,
            t_ref=self.t_ref, time_step_day=self.time_steps_day, time_step_marked=self.time_steps_marked,
            time_step_shift=self.td_steps_shift)

        # latent heat of vaporization [J/kg]
        var_lambda = (2.5 - 2.36 * 0.001 * var_tair_c) * 1000000
        var_lambda = np.where(var_mask == 0.0, 0.0, var_lambda)
        # water density [kg/m^3]
        var_rho_w = 1000.0 - 0.019549 * np.abs(var_tair_c - 3.98) ** 1.68  # ulteriore check
        var_rho_w = np.where(var_mask == 0.0, 0.0, var_rho_w)
        # vapor pressure [kPa] --> RelHum [%], Ta [C]
        var_ea = var_rh * 0.611 * np.exp(17.3 * var_tair_c / (237.3 + var_tair_c))
        var_ea = np.where(var_mask == 0.0, 0.0, var_ea)
        # vapor pressure at saturation [kPa] --> Ta [C]
        var_ea_sat = 0.611 * np.exp(17.3 * var_tair_c / (237.3 + var_tair_c))
        var_ea_sat = np.where(var_mask == 0.0, 0.0, var_ea_sat)
        # atmospheric actual emissivity [%] --> ea[kPa]*10 = [millibars]
        var_eps_a = 0.740 + 0.0049 * var_ea * 10.0
        var_eps_a = np.where(var_mask == 0.0, 0.0, var_eps_a)
        # air density [kg/m^3] --> Gas air constant R=0.288, Pa [kPa], Ta [K]
        var_rho_a = var_pair / (var_tair_k * 0.288)
        var_rho_a = np.where(var_mask == 0.0, 0.0, var_rho_a)

        # compute net radiation [W/m^2] -> sigma [W/m^2 K^4], EpsA [%], EpsS [%], albedo [-], Ta [K], LST [K], K [W/m^2]
        var_rn = np.where(
            var_mask == 1.0,
            var_inc_rad * (1.0 - self.albedo) + self.sigma * var_eps_a * var_tair_k ** 4 -
            self.sigma * self.eps_s * var_lst ** 4, np.nan)

        # compute ch
        var_ch, var_ratm, var_rsurf, var_rsurf_pot = compute_ch(
            wind=var_wind, bf=var_bf, rb=var_rb, mask=var_mask, ch=self.ch)

        # compute lst
        var_lst = compute_lst(
            lst=var_lst,
            ta_k=var_tair_k, airp=var_pair, ratm=var_ratm, rsurf=var_rsurf,
            td=var_td, pit=var_pit,
            rn=var_rn, lambda_v=var_lambda, ea=var_ea, rhoa=var_rho_a,
            mask=var_mask,
            t_ref=self.t_ref, lst_delta_max=self.lst_delta_max, cp=self.cp,
            dt_data_src=self.dt_delta_src, dt_delta_min=self.dt_delta_min
        )

        print()

        """
                    !-----------------------------------------------------------------------------------------
            ! Net Radiation [W/m^2] --> sigma [W/m^2 K^4], EpsA [%], EpsS [%], albedo [-], Ta [K], LST [K], K [W/m^2]
            where( a2dVarDEM.gt.0.0 )
                a2dVarRn = a2dVarIncRad*(1.0 - a2dVarAlbedo) + dSigma*a2dVarEpsA*a2dVarTaK**4 - &
                                                  dSigma*dEpsS*a2dVarLSTPStep**4
            elsewhere
                a2dVarRn = 0.0
            endwhere
            !-----------------------------------------------------------------------------------------
        
        """


