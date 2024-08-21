dynamic_data_grid = {
  "dynamic_src_grid": {
        "file": "hmc.forcing-grid.{datetime_dynamic_src_grid}.nc.gz",
        "mandatory": True,
        "type": "raster",
        "constants": None,
        "no_data": -9999.0,
        "vars_list": ['Rain', 'AirTemperature', 'IncRadiation', 'Wind', 'RelHumidity'],
        "vars_mapping" : {
            'Rain': 'rain',
            'AirTemperature': 'airt',
            'IncRadiation': 'inc_rad',
            'Wind': 'wind',
            'RelHumidity': 'rh'}
  },
  "dynamic_dst_grid": {
        "file": "hmc.output-grid.{datetime_dynamic_dst_grid}.nc.gz",
        "mandatory": True,
        "type": "raster",
        "constants": None,
        "no_data": -9999.0,
        "vars_list": None,
        "vars_mapping": None
  }
}
dynamic_data_point = {
   "dynamic_src_point": {
        "file": "hmc.forcing-point.{datetime_dynamic_src_point}.txt",
        "mandatory": True,
        "type": "array",
        "constants": None,
        "no_data": -9999.0,
        "vars_list": None,
        "vars_mapping": None
   },
   "file_data_dynamic_dst_point": {
        "file": "hmc.output-point.{datetime_dynamic_dst_point}.txt",
        "mandatory": True,
        "type": "array",
        "constants": None,
        "no_data": -9999.0,
        "vars_list": None,
        "vars_mapping": None
   }
}
