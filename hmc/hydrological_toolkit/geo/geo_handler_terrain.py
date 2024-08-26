# libraries
import xarray as xr

from hmc.hydrological_toolkit.geo.lib_geo_terrain import compute_info_terrain
from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler


class TerrainHandler(GeoHandler):

    def __init__(self, da_terrain: xr.DataArray, da_reference: xr.DataArray) -> None:

        self.da_terrain = da_terrain
        self.da_reference = da_reference

    def organize_terrain_info(self, **kwargs) -> None:

        terrain_value_max, terrain_value_min = compute_info_terrain(self.da_terrain)

        obj_data = {'terrain_value_max': terrain_value_max, 'terrain_value_min': terrain_value_min}

        return obj_data