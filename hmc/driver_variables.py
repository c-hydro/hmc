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

    def __init__(self, parameters : dict, da_reference: xr.DataArray) -> None:

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

    # method to initialize variables phys
    def initialize_variables_phys(self) -> xr.Dataset:

        # create variables for land surface model
        var_lst = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_rn = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_h = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_le = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_g = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_ef = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)

        obj_lsm = {'lst': var_lst, 'rn': var_rn, 'h': var_h, 'le': var_le, 'g': var_g, 'ef': var_ef}

        dset_lsm = create_dset_from_dict(obj_lsm, self.da_reference)

        return dset_lsm

    # method to initialize variables geo
    def initialize_variables_geo(self) -> xr.Dataset:

        # initialize variables (source geo data)
        var_terrain = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_fdir = create_variable(self.rows, self.cols, var_dtype='int', var_default_value=-9999)
        var_cnet = create_variable(self.rows, self.cols, var_dtype='int', var_default_value=0)
        var_cn = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_s = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_alpha = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0001)
        var_beta = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=0.0001)
        var_ct = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=self.get_param('ct'))
        var_cf = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=self.get_param('cf'))
        var_uc = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=self.get_param('uc'))
        var_uh = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=self.get_param('uh'))

        # initialize variables (derived by geo data)
        var_c1 = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_f2 = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_cost_f = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_cost_f1 = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)
        var_cost_ch_fix = create_variable(self.rows, self.cols, var_dtype='float32', var_default_value=-9999.0)

        # organize variables obj data
        obj_geo_data = {'terrain': var_terrain, 'fdir': var_fdir, 'cnet': var_cnet, 'cn': var_cn, 's': var_s,
                        'alpha': var_alpha, 'beta': var_beta,
                        'ct': var_ct, 'cf': var_cf, 'uc': var_uc, 'uh': var_uh}
        # organize variables obj lsm
        obj_geo_lsm = {'c1': var_c1, 'f2': var_f2,
                       'cost_f': var_cost_f, 'cost_f1': var_cost_f1, 'cost_ch_fix': var_cost_ch_fix}

        # convert variables obj to variables dataset
        dset_geo_data = create_dset_from_dict(obj_geo_data, self.da_reference)
        dset_geo_lsm = create_dset_from_dict(obj_geo_lsm, self.da_reference)

        return dset_geo_data, dset_geo_lsm
# ----------------------------------------------------------------------------------------------------------------------


