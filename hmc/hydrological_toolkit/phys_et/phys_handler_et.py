# libraries
import numpy as np
import pandas as pd
import xarray as xr

from copy import deepcopy

from hmc.generic_toolkit.time.lib_time_utils import compute_value_by_date

from hmc.hydrological_toolkit.constants.phys_constants_lsm import const_lsm as constants
from hmc.hydrological_toolkit.variables.lib_variable_utils import (
    create_variable_data, get_variable_data, save_variable_data)
from hmc.hydrological_toolkit.variables.lib_variable_attrs import apply_metrics
from hmc.hydrological_toolkit.phys_lsm.phys_apps_lsm import (
    compute_beta_function, compute_thermal_inertia, compute_richardson, compute_td, compute_ch, compute_lst)


# class to handle et model
class ETHandler:

    def __init__(self, dset_geo_generic: xr.Dataset, dset_geo_parameters: xr.Dataset, dset_geo_lsm: xr.Dataset,
                 da_reference: xr.DataArray,
                 time_step: pd.Timestamp, time_info: dict,
                 dt_delta_src: int = 3600, **kwargs) -> None:

        self.dset_geo_generic = dset_geo_generic
        self.dset_geo_parameters = dset_geo_parameters
        self.dset_geo_lsm = dset_geo_lsm

        self.da_reference = da_reference
        self.rows, self.cols = self.da_reference.shape

        self.time_step = time_step
        self.time_info = time_info

        self.time_steps_day = time_info['time_steps_day']
        self.time_steps_marked = time_info['time_steps_marked']

        self.dt_delta_src = dt_delta_src

        self.ch = compute_value_by_date(data=constants['ch'], time=self.time_step)
        self.albedo = compute_value_by_date(data=constants['albedo'], time=self.time_step)

    def execute(self,
                dset_data: xr.Dataset,
                dset_phys_lsm: xr.Dataset, dset_phys_volume: xr.Dataset,
                dset_phys_et: xr.Dataset, dset_phys_snow: xr.Dataset) -> (xr.Dataset, xr.Dataset):

        # get variables geo
        var_mask = get_variable_data(self.dset_geo_generic, var_name='mask', var_mandatory=True)
        var_cnet = get_variable_data(self.dset_geo_generic, var_name='channel_network', var_mandatory=True)
        var_carea = get_variable_data(self.dset_geo_generic, var_name='area_cell', var_mandatory=True)

        # get variables physics
        var_et = get_variable_data(dset_phys_et, var_name='et', var_mandatory=True)
        var_et_pot = get_variable_data(dset_phys_et, var_name='et_pot', var_mandatory=True)
        var_v_tot = get_variable_data(dset_phys_volume, var_name='v_tot', var_mandatory=True)
        var_v_tot_wp = get_variable_data(dset_phys_volume, var_name='v_tot_wp', var_mandatory=True)
        var_v_ret = get_variable_data(dset_phys_volume, var_name='v_ret', var_mandatory=True)

        # copy evapotranspiration to actual evapotranspiration
        var_ae = np.where(var_mask == 1, var_et, 0.0)

        # method to compute retention volume
        tmp_v_ret = deepcopy(var_v_ret)

        # (1) case
        var_v_ret = np.where(
            (tmp_v_ret > 0.0) & (tmp_v_ret >= var_et_pot) & (var_cnet == 0) & (var_mask == 1),
            tmp_v_ret - var_et_pot, tmp_v_ret)
        var_ae = np.where(
            (tmp_v_ret > 0.0) & (tmp_v_ret >= var_et_pot) & (var_cnet == 0) & (var_mask == 1),
            var_et_pot, var_ae)

        # (2) case
        var_v_ret = np.where(
            (var_v_ret > 0.0) & (var_v_ret < var_et_pot) & (var_cnet == 0), 0.0, var_v_ret)
        # compute residual evapotranspiration demand
        var_ae_res = np.where(
            (var_v_ret > 0.0) & (var_v_ret < var_et_pot) & (var_cnet == 0) & (var_mask == 1),
            var_et_pot - var_v_ret, 0.0)

        var_ae = np.where(
            (var_v_ret > 0.0) & (var_v_ret < var_et_pot) & (var_cnet == 0) & (var_mask == 1) & (var_ae_res < var_ae),
            var_ae_res, var_ae)
        var_ae = np.where(
            (var_v_ret > 0.0) & (var_v_ret < var_et_pot) & (var_cnet == 0) & (var_mask == 1) & (var_ae < 0.0),
            0.0, var_ae)
        var_ae = np.where(
            (var_v_ret > 0.0) & (var_v_ret < var_et_pot) & (var_cnet == 0) & (var_mask == 1) &
            (var_v_tot - var_v_tot_wp > var_ae),
            0.0, var_ae)
        var_ae = np.where(
            (var_v_ret > 0.0) & (var_v_ret < var_et_pot) & (var_cnet == 0) & (var_mask == 1) &
            (var_v_tot - var_v_tot_wp <= var_ae) & (var_v_tot - var_v_tot_wp > 0.0),
            var_ae_res + (var_v_tot - var_v_tot_wp), var_ae)
        var_ae = np.where(
            (var_v_ret > 0.0) & (var_v_ret < var_et_pot) & (var_cnet == 0) & (var_mask == 1) &
            (var_v_tot - var_v_tot_wp <= 0.0), 0.0, var_ae)

        var_v_ret = np.where(
            (var_v_ret > 0.0) & (var_cnet == 0) & (var_mask == 1) & (var_ae < 0.0),
            0.0, var_v_ret)

        # (3) case
        var_ae = np.where(
            (var_cnet == 0) & (var_mask == 1) & (var_ae < 0.0),
            0.0, var_ae)
        var_ae = np.where(
            (var_cnet == 0) & (var_mask == 1) & (var_v_tot - var_v_tot_wp > var_ae),
            var_v_ret + var_ae, 0.0)
        var_ae = np.where(
            (var_cnet == 0) & (var_mask == 1) & (var_v_tot - var_v_tot_wp <= var_ae) & (var_v_tot - var_v_tot_wp > 0.0),
            (var_v_tot - var_v_tot_wp), var_ae)
        var_ae = np.where(
            (var_cnet == 0) & (var_mask == 1) & (var_v_tot - var_v_tot_wp <= 0.0), 0.0, var_ae)
        var_v_tot = np.where(
            (var_cnet == 0) & (var_mask == 1) & (var_ae < 0.0),
            var_v_tot - var_ae, var_v_tot)
        var_v_tot = np.where(
            (var_cnet == 0) & (var_mask == 1) & (var_v_tot - var_v_tot_wp > var_ae) & (var_v_tot - var_v_tot_wp > 0.0),
            var_v_tot - var_ae, var_v_tot)

        # create dummy variables
        dummy_et = create_variable_data(self.rows, self.cols, var_default_value=0, var_dtype='float32')
        dummy_et_pot = create_variable_data(self.rows, self.cols, var_default_value=0, var_dtype='float32')

        # compute variable metrics
        metrics_ae = apply_metrics(data=var_ae, mask=var_mask, metrics=['mean', 'std', 'min', 'max', 'sum'])
        metrics_et = apply_metrics(data=var_et, mask=var_mask, metrics=['mean', 'std', 'min', 'max', 'sum'])
        metrics_et_pot = apply_metrics(data=var_et_pot, mask=var_mask, metrics=['mean', 'std', 'min', 'max', 'sum'])

        var_et_tot = metrics_et['sum'] + metrics_et_pot['sum']

        # save variables phys
        dset_phys_volume = save_variable_data(dset_phys_volume, var_data=var_v_tot, var_name='v_tot')
        dset_phys_volume = save_variable_data(dset_phys_volume, var_data=var_v_ret, var_name='v_ret')
        dset_phys_et = save_variable_data(dset_phys_et, var_data=var_ae, var_name='ae')
        dset_phys_et = save_variable_data(dset_phys_et, var_data=var_et_pot, var_name='ae_pot')
        dset_phys_et = save_variable_data(dset_phys_et, var_data=dummy_et, var_name='et')
        dset_phys_et = save_variable_data(dset_phys_et, var_data=dummy_et_pot, var_name='et_pot')

        return dset_phys_et, dset_phys_volume

    def skip(self,
             dset_data: xr.Dataset,
             dset_phys_lsm: xr.Dataset, dset_phys_volume: xr.Dataset,
             dset_phys_et: xr.Dataset, dset_phys_snow: xr.Dataset) -> (xr.Dataset, xr.Dataset):

        # get variables geo
        var_mask = get_variable_data(self.dset_geo_generic, var_name='mask', var_mandatory=True)

        # create variables phys
        var_rn = create_variable_data(self.rows, self.cols, var_default_value=-9999.0, var_dtype='float32')
        var_h = create_variable_data(self.rows, self.cols, var_default_value=-9999.0, var_dtype='float32')
        var_le = create_variable_data(self.rows, self.cols, var_default_value=-9999.0, var_dtype='float32')
        var_g = create_variable_data(self.rows, self.cols, var_default_value=-9999.0, var_dtype='float32')
        var_lst = create_variable_data(self.rows, self.cols, var_default_value=-9999.0, var_dtype='float32')

        # get variable data
        var_et = get_variable_data(dset_phys_et, var_name='phys_et', var_mandatory=True)
        var_et_pot = get_variable_data(dset_phys_et, var_name='et_pot', var_mandatory=True)

        # update variable data
        var_et = np.where((var_et >= 0.0) & (var_mask == 1), var_et, 0.0)
        var_et_pot = np.where((var_et_pot >= 0.0) & (var_mask == 1), var_et_pot, 0.0)

        # save variables phys
        dset_phys_lsm = save_variable_data(dset_phys_lsm, var_data=var_lst, var_name='lst')
        dset_phys_lsm = save_variable_data(dset_phys_lsm, var_data=var_rn, var_name='rn')
        dset_phys_lsm = save_variable_data(dset_phys_lsm, var_data=var_h, var_name='h')
        dset_phys_lsm = save_variable_data(dset_phys_lsm, var_data=var_le, var_name='le')
        dset_phys_lsm = save_variable_data(dset_phys_lsm, var_data=var_g, var_name='g')

        dset_phys_et = save_variable_data(dset_phys_et, var_data=var_et, var_name='phys_et')
        dset_phys_et = save_variable_data(dset_phys_et, var_data=var_et_pot, var_name='et_pot')

        return dset_phys_lsm, dset_phys_et
