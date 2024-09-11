dynamic_data_grid = {
  "dynamic_src_grid": {
        "file_name": "hmc.forcing-grid.{datetime_dynamic_src_grid}.nc.gz",
        "file_mandatory": True,
        "file_type": "raster",
        "vars_constants": None,
        "vars_no_data": [-9999.0, -9999.0, -9999.0, -9999.0, -9999.0, -9999.0],
        "vars_list": ['Rain', 'AirTemperature', 'IncRadiation', 'Wind', 'RelHumidity', 'AirPressure'],
        "vars_tags": ['rain', 'airt', 'inc_rad', 'wind', 'rh', 'airp'],
        "vars_mandatory": [True, True, True, True, True, False]
  },
  "dynamic_dst_grid": {
        "file_file": "hmc.output-grid.{datetime_dynamic_dst_grid}.nc.gz",
        "file_mandatory": True,
        "file_type": "raster",
        "vars_constants": None,
        "vars_no_data": None,
        "vars_list": None,
        "vars_tags": None,
        "vars_mandatory": None
  },
  "dynamic_state_grid": {
        "file_name": "hmc.state-grid.{datetime_dynamic_dst_grid}.nc.gz",
        "file_mandatory": True,
        "file_type": "raster",
        "vars_constants": None,
        "vars_no_data": None,
        "vars_list": None,
        "vars_tags": None,
        "vars_mandatory": None
    }
}

dynamic_data_point = {
   "dynamic_src_point": {
        "file_name": "hmc.forcing-point.{datetime_dynamic_src_point}.txt",
        "file_mandatory": True,
        "file_type": "array",
        "vars_constants": None,
        "vars_no_data": None,
        "vars_list": None,
        "vars_tags": None,
        "vars_mandatory": None
   },
   "dynamic_dst_point": {
        "file_name": "hmc.output-point.{datetime_dynamic_dst_point}.txt",
        "file_mandatory": True,
        "file_type": "array",
        "vars_constants": None,
        "vars_no_data": None,
        "vars_list": None,
        "vars_tags": None,
        "vars_mandatory": None
   },
   "dynamic_state_point": {
        "file_name": "hmc.state-point.{datetime_dynamic_dst_point}.txt",
        "file_mandatory": True,
        "file_type": "array",
        "vars_constants": None,
        "vars_no_data": None,
        "vars_list": None,
        "vars_tags": None,
        "vars_mandatory": None
    }
}
