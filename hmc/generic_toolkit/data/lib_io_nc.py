import logging
import xarray as xr


# ----------------------------------------------------------------------------------------------------------------------
# method to read netcdf file
def get_file_grid(file_name: str):

    file_obj = xr.open_dataset(file_name)

    if 'south_north' in file_obj.dims and 'west_east' in file_obj.dims:
        file_obj = file_obj.rename({'longitude': 'lon', 'latitude': 'lat'})
        file_obj = file_obj.rename_dims({'west_east': 'longitude', 'south_north': 'latitude'})

    return file_obj
# ----------------------------------------------------------------------------------------------------------------------
