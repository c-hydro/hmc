import numpy as np

def compute_info_terrain(da_terrain):

    terrain_value_max = np.nanmax(da_terrain.values)
    terrain_value_min = np.nanmin(da_terrain.values)

    return terrain_value_max, terrain_value_min