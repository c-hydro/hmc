# libraries
import os
from typing_extensions import Self
from typing import Optional
from datetime import datetime
import pandas as pd
import xarray as xr


class LSMHandler:

    def __init__(self, dset_data: xr.Dataset, da_reference: xr.DataArray) -> None:

        self.dset_data = dset_data
        self.da_reference = da_reference


    def phys_lsm(self):

        print()


