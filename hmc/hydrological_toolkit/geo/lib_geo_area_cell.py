# libraries
import numpy as np
from hmc.hydrological_toolkit.geo.lib_geo_utils import mask_data_by_reference


# method to compute area cell information
def compute_info_area_cell(da_area_cell):

    #         dDxM = nint(sqrt(sum(a2dVarAreaCell, mask=a2dVarAreaCell.gt.0.0) / count(a2dVarAreaCell.gt.0.0)))
    #         dDyM = nint(sqrt(sum(a2dVarAreaCell, mask=a2dVarAreaCell.gt.0.0) / count(a2dVarAreaCell.gt.0.0)))

    da_masked = mask_data_by_reference(da_area_cell, da_area_cell, mask_method='!=', mask_value=-9999, mask_other=0)
    pixels_n = np.float(np.not_equal(da_masked, 0.0).sum().values)

    res_meters_generic = np.sqrt(np.float(da_masked.sum().values) / pixels_n)
    res_meters_x = res_meters_generic
    res_meters_y = res_meters_generic

    area = (float(pixels_n) * res_meters_x * res_meters_y) / 1000000
    pixels_n = int(pixels_n)

    return area, pixels_n, res_meters_x, res_meters_y

