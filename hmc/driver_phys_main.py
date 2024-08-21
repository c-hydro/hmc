# ----------------------------------------------------------------------------------------------------------------------
# libraries
import os
import pandas as pd
import xarray as xr

from hmc.generic_toolkit.data.lib_io_utils import substitute_string_by_date, substitute_string_by_tags

from hmc.generic_toolkit.data.io_handler_base import IOHandler
from hmc.generic_toolkit.data.io_handler_dynamic_src import DynamicSrcHandler
from hmc.hydrological_toolkit.geo.lib_geo_utils import (
    mask_data_by_reference, mask_data_boundaries,
    initialize_data_by_constant, initialize_data_by_default, initialize_data_by_reference)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to handle physics driver
class PhysDriver(object):

    def __init__(self) -> None:

        self.phys_main = True

    # method to wrap physics routine(s)
    def wrap_physics(self, data_dynamic_src_grid: xr.Dataset, data_static_grid: xr.Dataset) -> xr.Dataset:

        print()
# ----------------------------------------------------------------------------------------------------------------------
