# ----------------------------------------------------------------------------------------------------------------------
# libraries
import os
import pandas as pd
import xarray as xr

from hmc.hydrological_toolkit.land_surface_model.lsm_handler_base import LSMHandler

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to handle driver physics
class PhysDriver(object):

    def __init__(self, dset_data_geo: xr.Dataset, da_reference: xr.DataArray) -> None:

        self.dset_data_geo = dset_data_geo
        self.da_reference = da_reference

    # method to wrap physics routine(s)
    def wrap_physics(self, dset_data_dynamic_src: xr.Dataset) -> xr.Dataset:

        # class of land surface model
        driver_phys_lsm = LSMHandler(dset_geo=self.dset_data_geo, da_reference=self.da_reference)
        # execute lsm routine(s)
        driver_phys_lsm.execute(dset_data_dynamic_src)


        return True
# ----------------------------------------------------------------------------------------------------------------------
