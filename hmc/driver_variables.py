# ----------------------------------------------------------------------------------------------------------------------
# libraries
import os
import numpy as np
import pandas as pd
import xarray as xr

from hmc.hydrological_toolkit.variables.lib_variable_utils import create_variable, create_dset_from_dict
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to handle physics driver geo
class VariablesDriver(object):

    def __init__(self, parameters: dict, da_reference: xr.DataArray) -> None:

        self.parameters = parameters
        self.da_reference = da_reference

        self.rows, self.cols = self.da_reference.shape

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
        var_rain = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_tair = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_rh = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_inc_rad = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_wind = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_pair = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_lai = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_albedo = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_fc = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_sm = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_et_pot = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        # organize data variables
        obj_data = {
            'rain': var_rain, 'tair': var_tair, 'rh': var_rh, 'inc_rad': var_inc_rad, 'wind': var_wind,
            'pair': var_pair, 'lai': var_lai, 'albedo': var_albedo, 'fc': var_fc,
            'sm': var_sm, 'et_pot': var_et_pot}
        # convert data variables to xarray dataset
        dset_data = create_dset_from_dict(obj_data, self.da_reference)

        return dset_data

    # method to allocate variables phys
    def allocate_variables_phys(self) -> (xr.Dataset, xr.Dataset, xr.Dataset, xr.Dataset):

        # allocate lsm variables
        var_lst = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_rn = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_h = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_le = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_g = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_ef = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_tak24 = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_tak24_marked = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        # organize lsm variables
        obj_phys_lsm = {'lst': var_lst, 'rn': var_rn, 'h': var_h, 'le': var_le, 'g': var_g, 'ef': var_ef}
        # convert lsm variables to xarray dataset
        dset_phys_lsm = create_dset_from_dict(obj_phys_lsm, self.da_reference)

        # allocate volume variables
        var_vtot = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_vret = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.001)
        var_vsub = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_vloss = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_vext = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_verr = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        # organize volume variables
        obj_phys_volume = {'vtot': var_vtot, 'vret': var_vret, 'vsub': var_vsub, 'vloss': var_vloss,
                           'vext': var_vext, 'verr': var_verr}
        # convert volume variables to xarray dataset
        dset_phys_volume = create_dset_from_dict(obj_phys_volume, self.da_reference)

        # allocate et variables
        var_et = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_etpot = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_ae = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_aepot_3d = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_ae_3d = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        # organize et variables
        obj_phys_et = {'et': var_et, 'etpot': var_etpot, 'ae': var_ae, 'aepot_3d': var_aepot_3d, 'ae_3d': var_ae_3d}
        # convert et variables to xarray dataset
        dset_phys_et = create_dset_from_dict(obj_phys_et, self.da_reference)

        # allocate routing variables
        var_hydro = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.000001)
        var_hydro_prev = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.000001)
        var_routing = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_darcy = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_qout = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_qdisout = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_qvolout = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_qtot = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_intensity = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_flowdeep = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_flowexf = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_ucact = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_udt = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        # organize routing variables
        obj_phys_routing = {'hydro': var_hydro, 'hydro_prev': var_hydro_prev, 'routing': var_routing,
                            'darcy': var_darcy, 'qout': var_qout, 'qdisout': var_qdisout, 'qvolout': var_qvolout,
                            'qtot': var_qtot, 'intensity': var_intensity, 'flowdeep': var_flowdeep,
                            'flowexf': var_flowexf, 'ucact': var_ucact, 'udt': var_udt}
        # convert routing variables to xarray dataset
        dset_phys_routing = create_dset_from_dict(obj_phys_routing, self.da_reference)

        return dset_phys_lsm, dset_phys_volume, dset_phys_et, dset_phys_routing

    # method to allocate variables geo
    def allocate_variables_geo(self) -> (xr.Dataset, xr.Dataset, xr.Dataset, xr.Dataset, xr.Dataset):

        # initialize geo variables
        var_terrain = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_fdir = create_variable(self.rows, self.cols, var_dtype='int', var_default_value=-9999)
        var_cnet = create_variable(self.rows, self.cols, var_dtype='int', var_default_value=0)
        var_mask = create_variable(self.rows, self.cols, var_dtype='int', var_default_value=0)
        var_cell_area = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_cn = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_s = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=500.0)
        # organize geo variables
        obj_geo_data = {'terrain': var_terrain, 'fdir': var_fdir, 'cnet': var_cnet, 'mask': var_mask,
                        'cell_area': var_cell_area,
                        'cn': var_cn, 's': var_s}
        # convert geo variables to xarray dataset
        dset_geo_data = create_dset_from_dict(obj_geo_data, self.da_reference)

        # initialize routing variables
        var_ct = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=self.get_param('ct'))
        var_cf = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=self.get_param('cf'))
        var_uc = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=self.get_param('uc'))
        var_uh = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=self.get_param('uh'))
        # organize routing variables
        obj_geo_routing = {'ct': var_ct, 'cf': var_cf, 'uc': var_uc, 'uh': var_uh}
        # convert routing variables to xarray dataset
        dset_geo_routing = create_dset_from_dict(obj_geo_routing, self.da_reference)

        # initialize horton variables
        var_c1 = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_f2 = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_cost_f = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_cost_f1 = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_cost_ch_fix = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        # organize horton variables
        obj_geo_horton = {'c1': var_c1, 'f2': var_f2,
                          'cost_f': var_cost_f, 'cost_f1': var_cost_f1, 'cost_ch_fix': var_cost_ch_fix}
        # convert horton variables to xarray dataset
        dset_geo_horton = create_dset_from_dict(obj_geo_horton, self.da_reference)

        # initialize water-table variables
        var_wt = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_wt_max = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_wt_alpha = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_wt_beta = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        # organize water-table variables
        obj_geo_wt = {'wt': var_wt, 'wt_max': var_wt_max, 'wt_alpha': var_wt_alpha, 'wt_beta': var_wt_beta}
        # convert water-table variables to xarray dataset
        dset_geo_wt = create_dset_from_dict(obj_geo_wt, self.da_reference)

        # initialize lsm variables
        var_ct_wp = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_kb1 = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_kc1 = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_kb2 = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_kc2 = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0)
        var_veg_ia = create_variable(100, 2, var_dtype='float32', var_default_value=0.0)
        # organize lsm variables
        obj_geo_lsm = {
            'ct_wp': var_ct_wp, 'kb_1': var_kb1, 'kc_1': var_kc1, 'kb_2': var_kb2, 'kc_2': var_kc2}
        # convert lsm variables to xarray dataset
        dset_geo_lsm = create_dset_from_dict(obj_geo_lsm, self.da_reference)

        return dset_geo_data, dset_geo_routing, dset_geo_horton, dset_geo_wt, dset_geo_lsm

# ----------------------------------------------------------------------------------------------------------------------


