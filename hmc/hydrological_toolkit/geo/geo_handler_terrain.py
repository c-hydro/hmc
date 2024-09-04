# libraries
import xarray as xr

from hmc.hydrological_toolkit.geo.lib_geo_terrain import compute_auxiliary, compute_mask
from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler


class TerrainHandler(GeoHandler):

    def __init__(self, da_terrain: xr.DataArray, da_reference: xr.DataArray) -> None:

        self.mask_tag = 'mask'

        super().__init__(da_data=da_terrain, da_reference=da_reference)

    # method to organize information
    def organize_auxiliary(self, **kwargs) -> dict:

        terrain_value_max, terrain_value_min = compute_auxiliary(self.da_data, self.da_reference)
        obj_data = {'terrain__max': terrain_value_max, 'terrain_min': terrain_value_min}

        return obj_data

    # method to organize data
    def organize_data(self, dset_data: xr.Dataset = None) -> xr.Dataset:

        if dset_data is None:
            raise ValueError('Dataset object is required to organize data')

        da_mask = compute_mask(self.da_data, no_data_value=-9999.0)
        dset_data = self.add_data(da_data=da_mask, dset_data=dset_data, var_name=self.mask_tag)

        return dset_data
