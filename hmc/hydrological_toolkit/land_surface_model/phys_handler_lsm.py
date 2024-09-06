# libraries
import xarray as xr

from hmc.hydrological_toolkit.constants.phys_constants_lsm import const_lsm as constants
from hmc.hydrological_toolkit.variables.lib_variable_utils import create_dict_from_dset, get_variable_data
from hmc.hydrological_toolkit.land_surface_model.phys_apps_lsm import (
    compute_beta_function, compute_thermal_inertia, compute_richardson, compute_tdeep)


# class to handle land surface model
class LSMHandler:

    def __init__(self, dset_geo_generic: xr.Dataset,
                 dset_geo_lsm: xr.Dataset, dset_geo_routing: xr.Dataset,
                 da_reference: xr.DataArray) -> None:

        self.dset_geo_generic = dset_geo_generic
        self.dset_geo_lsm = dset_geo_lsm
        self.dset_geo_routing = dset_geo_routing

        self.da_reference = da_reference

        self.t_ref = constants['t_ref']
        self.bf_min = constants['bf_min']
        self.bf_max = constants['bf_max']
        self.cp = constants['cp']
        self.cp_s = constants['cp_s']
        self.cp_w = constants['cp_w']
        self.eps_s = constants['eps_s']

    def execute(self, dset_data: xr.Dataset, dset_phys_volume: xr.Dataset) -> None:

        # get variables geo
        var_mask = get_variable_data(self.dset_geo_generic, var_name='mask', var_mandatory=True)
        var_s = get_variable_data(self.dset_geo_generic, var_name='s', var_mandatory=True)

        # get variables lsm
        var_ct_wp = get_variable_data(self.dset_geo_lsm, var_name='ct_wp', var_mandatory=True)
        var_kb_1 = get_variable_data(self.dset_geo_lsm, var_name='kb_1', var_mandatory=True)
        var_kc_1 = get_variable_data(self.dset_geo_lsm, var_name='kc_1', var_mandatory=True)
        # get variables routing
        var_ct = get_variable_data(self.dset_geo_routing, var_name='ct', var_mandatory=True)

        # get variables physics
        var_vtot = get_variable_data(dset_phys_volume, var_name='vtot', var_mandatory=True)

        # get variables data
        var_tair = get_variable_data(dset_data, var_name='tair', var_mandatory=True)
        var_rh = get_variable_data(dset_data, var_name='rh', var_mandatory=True)
        var_inc_rad = get_variable_data(dset_data, var_name='inc_rad', var_mandatory=True)
        var_wind = get_variable_data(dset_data, var_name='wind', var_mandatory=True)
        var_pair = get_variable_data(dset_data, var_name='pair', var_mandatory=True)

        # adapt variables
        var_tair = var_tair + self.t_ref
        var_rh = var_rh / 100.0
        var_sm = var_vtot / var_s

        var_bf, var_bf_bare_soil = compute_beta_function(
            sm=var_sm, ct_wp=var_ct_wp, ct=var_ct,  mask=var_mask, kb1=var_kb_1, kc1=var_kc_1,
            bf_min=self.bf_min, bf_max=self.bf_max)

        compute_thermal_inertia()

        compute_richardson()

        compute_tdeep()
        print()

        """
                    !-------------------------------------------------------------------------------------
            ! Subroutine for calculating thermal inertia
            call HMC_Phys_LSM_Apps_ThermalInertia( iID, iRows, iCols, &
                                                      a2dVarSM, a2dVarDEM, &
                                                      a2dVarPit )
            !-------------------------------------------------------------------------------------

            !-------------------------------------------------------------------------------------
            ! Subroutine for calculating Richardson number
            call HMC_Phys_LSM_Apps_Richardson( iID, iRows, iCols, &
                                                  a2dVarDEM, &
                                                  a2dVarWind, a2dVarTaK, a2dVarPa, &
                                                  a2dVarLSTPStep, &
                                                  a2dVarRb )
            !-------------------------------------------------------------------------------------

            !-----------------------------------------------------------------------------------------
            ! Subroutine for calculating desp soil temperature (TDeep)
            call HMC_Phys_LSM_Apps_TDeep( iID, iRows, iCols, iT, &
                                             a2dVarDEM, &
                                             a2dVarTaK, &
                                             a2dVarTDeep )
            !-----------------------------------------------------------------------------------------"""


