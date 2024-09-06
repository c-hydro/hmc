# libraries
import numpy as np
import xarray as xr
from hmc.hydrological_toolkit.geo.lib_geo_utils import mask_data_by_reference


# method to compute area cell information
def compute_info(da_area_cell: xr.DataArray) -> (float, int, float, float):

    da_masked = mask_data_by_reference(da_area_cell, da_area_cell, mask_method='!=', mask_value=-9999, mask_other=0)
    pixels = np.float(np.not_equal(da_masked, 0.0).sum().values)

    res_meters_generic = np.sqrt(np.float(da_masked.sum().values) / pixels)
    dx = res_meters_generic
    dy = res_meters_generic

    area = (float(pixels) * dx * dy) / 1000000
    pixels = int(pixels)

    return area, pixels, dx, dy

