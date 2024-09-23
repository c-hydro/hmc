# ----------------------------------------------------------------------------------------------------------------------
# libraries
import os
import numpy as np
import pandas as pd
import xarray as xr

from hmc.hydrological_toolkit.variables.lib_variable_utils import create_variable_data, create_dset_from_dict
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to handle physics driver geo
class VariablesDriver(object):

    def __init__(self, reference_grid: xr.DataArray, parameters: dict,
                 time_dims: dict,
                 static_dims_grid: dict, static_dims_point: dict,
                 dynamic_dims_grid: dict, dynamic_dims_point: dict = None,
                 **kwargs) -> None:

        self.reference_grid = reference_grid

        self.parameters = parameters
        self.static_dims_grid = static_dims_grid
        self.static_dims_point = static_dims_point
        self.dynamic_dims_grid = dynamic_dims_grid
        self.dynamic_dims_point = dynamic_dims_point
        self.time_dims = time_dims

        # get grid dimensions
        self.rows, self.cols = self.static_dims_grid['rows'], self.static_dims_grid['cols']

        # get point dimensions
        self.sections_n = self.static_dims_point['section']
        self.dam_n = self.static_dims_point['dam']
        self.catch_n = self.static_dims_point['catch']
        self.joint_n = self.static_dims_point['joint']
        self.lake_n = self.static_dims_point['lake']
        self.plant_n = self.static_dims_point['plant']
        self.release_n = self.static_dims_point['release']

        # get time steps variable(s)
        self.time_steps_day = self.time_dims['time_steps_day']
        self.time_step_marked = self.time_dims['time_steps_marked']

    # method to get parameter value
    def get_param(self, parameter_name: str = None) -> (float, int):

        parameter_value = None
        if parameter_name in list(self.parameters.keys()):
            parameter_value = self.parameters[parameter_name]
        else:
            raise ValueError('Parameter "' + parameter_name + '" not found in parameters')

        return parameter_value

    def allocate_variables_data(self) -> xr.Dataset:

        # allocate data variables
        var_rain = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_tair = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_rh = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_inc_rad = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_wind = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_pair = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_lai = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_albedo = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_fc = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_sm = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_et_pot = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        # organize data variables
        obj_data = {
            'rain': var_rain, 'tair': var_tair, 'rh': var_rh, 'inc_rad': var_inc_rad, 'wind': var_wind,
            'pair': var_pair, 'lai': var_lai, 'albedo': var_albedo, 'fc': var_fc,
            'sm': var_sm, 'et_pot': var_et_pot}
        # convert data variables to xarray dataset
        dset_data = create_dset_from_dict(obj_data, da_reference=self.reference_grid)

        return dset_data

    # method to allocate variables phys
    def allocate_variables_phys(self) -> (xr.Dataset, xr.Dataset, xr.Dataset, xr.Dataset, xr.Dataset):

        # allocate lsm variables
        var_lst = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_rn = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_h = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_le = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_g = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_ef = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_tak_step_day = create_variable_data(
            self.rows, self.cols, time=self.time_steps_day, var_dtype='float32', var_default_value=-9999.0)
        var_tak_step_marked = create_variable_data(
            self.rows, self.cols, time=self.time_step_marked, var_dtype='float32', var_default_value=-9999.0)

        # organize lsm variables
        obj_phys_lsm = {'lst': var_lst, 'rn': var_rn, 'h': var_h, 'le': var_le, 'g': var_g, 'ef': var_ef,
                        'tak_step_day': var_tak_step_day, 'tak_step_marked': var_tak_step_marked}
        time_phys_lsm = {'lst': None, 'rn': None, 'h': None, 'le': None, 'g': None, 'ef': None,
                         'tak_step_day': self.time_steps_day, 'tak_step_marked': self.time_step_marked}
        vars_coords = {'tak_step_day': ['time_steps_day', 'latitude', 'longitude'],
                       'tak_step_marked': ['time_steps_marked', 'latitude', 'longitude']}
        vars_dims = {'tak_step_day': ['time_steps_day', 'latitude', 'longitude'],
                     'tak_step_marked': ['time_steps_marked', 'latitude', 'longitude']}

        # convert lsm variables to xarray dataset
        dset_phys_lsm = create_dset_from_dict(
            obj_phys_lsm,
            vars_coords=vars_coords, vars_dims=vars_dims,
            time_reference=time_phys_lsm, da_reference=self.reference_grid)

        # allocate phys_et variables
        var_et = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_et_pot = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_ae = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_ae_3d = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_ae_3d_pot = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        # organize phys_et variables
        obj_phys_et = {'et': var_et, 'et_pot': var_et_pot, 'ae': var_ae, 'ae_3d_pot': var_ae_3d_pot, 'ae_3d': var_ae_3d}
        # convert phys_et variables to xarray dataset
        dset_phys_et = create_dset_from_dict(obj_phys_et, da_reference=self.reference_grid)

        # allocate phys_snow variables
        var_snow_mask = create_variable_data(self.rows, self.cols, var_dtype='int', var_default_value=0)
        var_snow_age = create_variable_data(self.rows, self.cols, var_dtype='int', var_default_value=0)
        var_snow_melting = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_snow_density = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        # organize phys_et variables
        obj_phys_snow = {'snow_mask': var_snow_mask, 'snow_age': var_snow_age,
                         'snow_melting': var_snow_melting, 'snow_density': var_snow_density}
        # convert phys_et variables to xarray dataset
        dset_phys_snow = create_dset_from_dict(obj_phys_snow, da_reference=self.reference_grid)

        # allocate volume variables
        var_v_tot = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_v_tot_wp = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_v_ret = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.001)
        var_v_sub = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_v_loss = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_v_ext = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_v_err = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        # organize volume variables
        obj_phys_volume = {'v_tot': var_v_tot, 'v_ret': var_v_ret, 'v_sub': var_v_sub, 'v_loss': var_v_loss,
                           'v_ext': var_v_ext, 'v_err': var_v_err, 'v_tot_wp': var_v_tot_wp}
        # convert volume variables to xarray dataset
        dset_phys_volume = create_dset_from_dict(obj_phys_volume, da_reference=self.reference_grid)

        # allocate routing variables
        var_hydro = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.000001)
        var_hydro_prev = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.000001)
        var_routing = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_darcy = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_qout = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_qdisout = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_qvolout = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_qtot = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_intensity = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_flowdeep = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_flowexf = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_ucact = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_udt = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        # organize routing variables
        obj_phys_routing = {'hydro': var_hydro, 'hydro_prev': var_hydro_prev, 'routing': var_routing,
                            'darcy': var_darcy, 'qout': var_qout, 'qdisout': var_qdisout, 'qvolout': var_qvolout,
                            'qtot': var_qtot, 'intensity': var_intensity, 'flowdeep': var_flowdeep,
                            'flowexf': var_flowexf, 'ucact': var_ucact, 'udt': var_udt}
        # convert routing variables to xarray dataset
        dset_phys_routing = create_dset_from_dict(obj_phys_routing, da_reference=self.reference_grid)

        return dset_phys_lsm, dset_phys_et, dset_phys_snow, dset_phys_volume,  dset_phys_routing

    # method to allocate variables geo
    def allocate_variables_geo(self) -> (xr.Dataset, xr.Dataset, xr.Dataset, xr.Dataset, xr.Dataset):

        # initialize geo variables
        var_terrain = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_fdir = create_variable_data(self.rows, self.cols, var_dtype='int', var_default_value=-9999)
        var_cnet = create_variable_data(self.rows, self.cols, var_dtype='int', var_default_value=0)
        var_mask = create_variable_data(self.rows, self.cols, var_dtype='int', var_default_value=0)
        var_cell_area = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_cn = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_s = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=500.0)

        var_ct = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=self.get_param('ct'))
        var_cf = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=self.get_param('cf'))
        var_uc = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=self.get_param('uc'))
        var_uh = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=self.get_param('uh'))

        var_ct_wp = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)

        # organize geo variables
        obj_geo_generic = {
            'terrain': var_terrain, 'fdir': var_fdir, 'cnet': var_cnet, 'mask': var_mask,
            'area_cell': var_cell_area,
            'curve_number': var_cn, 's': var_s,
            'ct': var_ct, 'cf': var_cf, 'uc': var_uc, 'uh': var_uh,
            'ct_wp': var_ct_wp}

        # convert geo variables to xarray dataset
        dset_geo_generic = create_dset_from_dict(obj_geo_generic, da_reference=self.reference_grid)

        # initialize horton variables
        var_c1 = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_f2 = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_cost_f = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_cost_f1 = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_cost_ch_fix = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        # organize horton variables
        obj_geo_horton = {'c1': var_c1, 'f2': var_f2,
                          'cost_f': var_cost_f, 'cost_f1': var_cost_f1, 'cost_ch_fix': var_cost_ch_fix}
        # convert horton variables to xarray dataset
        dset_geo_horton = create_dset_from_dict(obj_geo_horton, da_reference=self.reference_grid)

        # initialize water-table variables
        var_wt = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_wt_max = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_wt_alpha = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_wt_beta = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        # organize water-table variables
        obj_geo_wt = {'wt': var_wt, 'wt_max': var_wt_max, 'wt_alpha': var_wt_alpha, 'wt_beta': var_wt_beta}
        # convert water-table variables to xarray dataset
        dset_geo_wt = create_dset_from_dict(obj_geo_wt, da_reference=self.reference_grid)

        # initialize lsm variables
        var_ct_wp = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_kb1 = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_kc1 = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_kb2 = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_kc2 = create_variable_data(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_veg_ia = create_variable_data(100, 2, var_dtype='float32', var_default_value=0.0)
        # organize lsm variables
        obj_geo_lsm = {
            'ct_wp': var_ct_wp, 'kb_1': var_kb1, 'kc_1': var_kc1, 'kb_2': var_kb2, 'kc_2': var_kc2}
        # convert lsm variables to xarray dataset
        dset_geo_lsm = create_dset_from_dict(obj_geo_lsm, da_reference=self.reference_grid)

        return dset_geo_generic, dset_geo_horton, dset_geo_wt, dset_geo_lsm

# ----------------------------------------------------------------------------------------------------------------------
