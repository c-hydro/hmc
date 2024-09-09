# ----------------------------------------------------------------------------------------------------------------------
# libraries
import os
import pandas as pd
import xarray as xr

from hmc.hydrological_toolkit.land_surface_model.phys_handler_lsm import LSMHandler

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to handle driver physics
class PhysDriver(object):

    def __init__(self, dset_geo_generic: xr.Dataset, dset_geo_parameters: xr.Dataset,
                 dset_data: xr.Dataset, da_reference: xr.DataArray) -> None:

        self.dset_geo_generic = dset_geo_generic
        self.dset_geo_parameters = dset_geo_parameters

        self.dset_data = dset_data
        self.da_reference = da_reference

    # method to wrap physics routine(s)
    def wrap_physics_lsm(self, dset_geo_lsm: xr.Dataset,
                         dset_geo_routing: xr.Dataset, dset_phys_volume: xr.Dataset) -> xr.Dataset:

        # class of land surface model
        driver_phys_lsm = LSMHandler(dset_geo_generic=self.dset_geo_generic,
                                     dset_geo_parameters=self.dset_geo_parameters,
                                     dset_geo_lsm=dset_geo_lsm, dset_geo_routing=dset_geo_routing,
                                     da_reference=self.da_reference)
        # execute lsm routine(s)
        driver_phys_lsm.execute(dset_data=self.dset_data, dset_phys_volume=dset_phys_volume)

        return True
# ----------------------------------------------------------------------------------------------------------------------
