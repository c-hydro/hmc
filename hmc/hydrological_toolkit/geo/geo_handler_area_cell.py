# libraries
import xarray as xr

from hmc.hydrological_toolkit.geo.lib_geo_area_cell import compute_info
from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler


class AreaCellHandler(GeoHandler):

    def __init__(self, da_cell_area: xr.DataArray, da_reference: xr.DataArray) -> None:
        super().__init__(da_data=da_cell_area, da_reference=da_reference)

    def organize_auxiliary(self) -> dict:

        area, pixels_n, dx, dy = compute_info(self.da_data)
        obj_auxiliary = {'area': area, 'dx': dx, 'dy': dy, 'pixels': pixels_n}

        return obj_auxiliary
