# ----------------------------------------------------------------------------------------------------------------------
# libraries
import os
import pandas as pd
import xarray as xr

from hmc.hydrological_toolkit.phys_lsm.phys_handler_lsm import LSMHandler
from hmc.hydrological_toolkit.phys_et.phys_handler_et import ETHandler
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to handle driver physics
class PhysDriver(object):

    def __init__(self, time_step: pd.Timestamp, time_info: dict,
                 dset_geo_generic: xr.Dataset, dset_geo_parameters: xr.Dataset,
                 dset_data: xr.Dataset, da_reference: xr.DataArray) -> None:

        self.time_step = time_step
        self.time_info = time_info

        self.dset_geo_generic = dset_geo_generic
        self.dset_geo_parameters = dset_geo_parameters

        self.dset_data = dset_data
        self.da_reference = da_reference

    # method to wrap physics routine(s)
    def wrap_physics_lsm(self,
                         dset_geo_lsm: xr.Dataset,
                         dset_phys_lsm: xr.Dataset, dset_phys_et: xr.Dataset, dset_phys_snow: xr.Dataset,
                         dset_phys_volume: xr.Dataset, flag_phys: bool = True) -> (xr.Dataset, xr.Dataset):

        # initialize physics lsm class
        driver_phys_lsm = LSMHandler(
            dset_geo_generic=self.dset_geo_generic,
            dset_geo_parameters=self.dset_geo_parameters, dset_geo_lsm=dset_geo_lsm,
            da_reference=self.da_reference,
            time_step=self.time_step, time_info=self.time_info)

        # activate physics lsm
        if flag_phys:

            # execute physics lsm method(s)
            dset_phys_lsm, dset_phys_et = driver_phys_lsm.execute(
                dset_data=self.dset_data, dset_phys_lsm=dset_phys_lsm, dset_phys_volume=dset_phys_volume,
                dset_phys_et=dset_phys_et, dset_phys_snow=dset_phys_snow)

        else:

            # skip physics lsm method(s) and updating some variables in the datasets
            dset_phys_lsm, dset_phys_et = driver_phys_lsm.skip(
                dset_data=self.dset_data, dset_phys_lsm=dset_phys_lsm,
                dset_phys_volume=dset_phys_volume,
                dset_phys_et=dset_phys_et, dset_phys_snow=dset_phys_snow)

        return dset_phys_lsm, dset_phys_et

    # method to wrap physics routine(s)
    def wrap_physics_et(self,
                        dset_geo_lsm: xr.Dataset,
                        dset_phys_lsm: xr.Dataset, dset_phys_et: xr.Dataset, dset_phys_snow: xr.Dataset,
                        dset_phys_volume: xr.Dataset, flag_phys: bool = True):

        # initialize physics evapotranspiration class
        driver_phys_et = ETHandler(
            dset_geo_generic=self.dset_geo_generic,
            dset_geo_parameters=self.dset_geo_parameters, dset_geo_lsm=dset_geo_lsm,
            da_reference=self.da_reference,
            time_step=self.time_step, time_info=self.time_info)

        # execute physics evapotranspiration method(s)
        dset_phys_et, dset_phys_volume = driver_phys_et.execute(
            dset_data=self.dset_data, dset_phys_lsm=dset_phys_lsm, dset_phys_volume=dset_phys_volume,
            dset_phys_et=dset_phys_et, dset_phys_snow=dset_phys_snow)

        return dset_phys_et, dset_phys_volume

    def wrap_physics_snow(self):
        print()

    def wrap_physics_retention(self):
        print()
# ----------------------------------------------------------------------------------------------------------------------
