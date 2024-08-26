static_data_grid = {
  "terrain": {
    "file": "{domain_name}.dem.txt",
    "mandatory": True,
    "type": "raster",
    "constants": None,
    "no_data": -9999.0
  },
  "flow_directions": {
    "file": "{domain_name}.pnt.txt",
    "mandatory": True,
    "type": "raster",
    "constants": None,
    "no_data": -9999
  },
  "channel_network": {
    "file": "{domain_name}.choice.txt",
    "mandatory": True,
    "type": "raster",
    "constants": None,
    "no_data": -1
  },
  "curve_number": {
    "file": "{domain_name}.cn.txt",
    "mandatory": False,
    "type": "raster",
    "constants": "cn",
    "no_data": -9999.0
  },
  "mask": {
    "file": "{domain_name}.mask.txt",
    "mandatory": True,
    "type": "raster",
    "constants": None,
    "no_data": -9999.0
  },
  "alpha": {
    "file": "{domain_name}.alpha.txt",
    "mandatory": True,
    "type": "raster",
    "constants": None,
    "no_data": -9999.0,
    "vars_list": None,
    "vars_mapping": None
  },
  "beta": {
    "file": "{domain_name}.beta.txt",
    "mandatory": True,
    "type": "raster",
    "constants": None,
    "no_data": -9999.0,
    "vars_list": None,
    "vars_mapping": None
  },
  "ct": {
    "file": "{domain_name}.ct.txt",
    "mandatory": False,
    "type": "raster",
    "constants": "ct",
    "no_data": -9999.0,
    "vars_list": None,
    "vars_mapping": None
  },
  "cf": {
    "file": "{domain_name}.cf.txt",
    "mandatory": False,
    "type": "raster",
    "constants": "cf",
    "no_data": -9999.0,
    "vars_list": None,
    "vars_mapping": None
  },
  "uc": {
    "file": "{domain_name}.uc.txt",
    "mandatory": False,
    "type": "raster",
    "constants": "uc",
    "no_data": -9999.0,
    "vars_list": None,
    "vars_mapping": None
  },
  "area_cell": {
    "file": "{domain_name}.areacell.txt",
    "mandatory": True,
    "type": "raster",
    "constants": None,
    "no_data": -9999.0,
    "vars_list": None,
    "vars_mapping": None
  }
}
static_data_point = {
  "vegetation_interception": {
    "file": "valori_fo_noIa_AMC2.txt",
    "mandatory": True,
    "type": "array",
    "no_data": None,
    "vars_list": None,
    "vars_mapping": None
  }
}
