# libraries
import xarray as xr

from hmc.hydrological_toolkit.constants import phys_constants_lsm as constants
from hmc.hydrological_toolkit.variables.lib_variable_utils import create_dict_from_dset, get_variable_data
from hmc.hydrological_toolkit.land_surface_model.lib_lsm_apps import thermal_inertia, richardson



class LSMHandler:

    def __init__(self, dset_geo: xr.Dataset, da_reference: xr.DataArray) -> None:

        self.dset_geo = dset_geo
        self.da_reference = da_reference

        self.t_ref = constants.t_ref
        self.bf_min = constants.bf_min
        self.bf_max = constants.bf_max
        self.cp = constants.cp
        self.cp_s = constants.cp_s
        self.cp_w = constants.cp_w
        self.eps_s = constants.eps_s


    def execute(self, dset_data: xr.Dataset, dset_phys: xr.Dataset) -> None:

        # get variables geo
        var_s = get_variable_data(dset_phys, var_name='s', var_mandatory=True)

        # get variables physics
        var_vtot = get_variable_data(dset_phys, var_name='vtot', var_mandatory=True)

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



        print()


