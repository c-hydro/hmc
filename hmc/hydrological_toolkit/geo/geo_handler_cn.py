# libraries
import xarray as xr

from hmc.hydrological_toolkit.geo.lib_geo_cn import compute_cn2s
from hmc.hydrological_toolkit.geo.geo_handler_base import GeoHandler


class CNHandler(GeoHandler):

    def __init__(self, da_cn: xr.DataArray, da_reference: xr.DataArray) -> None:

        self.da_cn = da_cn
        self.da_reference = da_reference

    def organize_info(self) -> dict:

        da_s = compute_cn2s(self.da_cn, self.da_reference)

        return da_s
