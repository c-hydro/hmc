# libraries
import xarray as xr

from hmc.hydrological_toolkit.geo.lib_geo_area_cell import compute_info_area_cell
from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler


class AreaCellHandler(GeoHandler):

    def __init__(self, da_cell_area: xr.DataArray, da_reference: xr.DataArray) -> None:

        self.da_area_cell = da_cell_area
        self.da_reference = da_reference

    def organize_area_cell_info(self) -> dict:

        area, pixels_n, res_meters_x, res_meters_y = compute_info_area_cell(self.da_area_cell)

        obj_data = {'area': area, 'res_meters_x': res_meters_x, 'res_meters_y': res_meters_y, 'pixels_n': pixels_n}

        return obj_data
