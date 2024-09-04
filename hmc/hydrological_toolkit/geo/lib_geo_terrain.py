# libraries
import numpy as np
import xarray as xr


# method to compute auxiliary (based on terrain)
def compute_auxiliary(da_terrain: xr.DataArray, da_reference: xr.DataArray = None) -> tuple:

    if da_reference is not None:
        da_terrain = da_terrain.where(da_reference != -9999, np.nan)

    terrain_value_max = np.nanmax(da_terrain.values)
    terrain_value_min = np.nanmin(da_terrain.values)

    return terrain_value_max, terrain_value_min


# method to compute mask (based on terrain)
def compute_mask(da_terrain: xr.DataArray, no_data_value: (float, int) = -9999.0) -> xr.DataArray:

    da_mask = da_terrain.copy()
    da_mask.values = np.where(da_terrain.values != no_data_value, 1, 0)
    da_mask = da_mask.astype(dtype=int)

    return da_mask
