"""
Library Features:

Name:          lib_io_variables
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20240911'
Version:       '1.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
from datetime import datetime

import numpy as np
import pandas as pd
import xarray as xr

from hmc.generic_toolkit.default.lib_default_generic import tags_date_conversion
# ----------------------------------------------------------------------------------------------------------------------


def fill_var_generic():
    print()


# method to fill air pressure
def fill_var_air_pressure(terrain: np.ndarray, no_data: float = -9999.0) -> np.ndarray:
    var_pa = np.where(terrain >= 0, 101.3 * ((293 - 0.0065 * terrain) / 293) ** 5.26, no_data)  # [kPa]
    return var_pa
