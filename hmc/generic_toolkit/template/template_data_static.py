static_data_grid = {
  "terrain": {
    "file": "{domain_name}.dem.txt",
    "mandatory": True,
    "type": "raster",
    "default": None,
    "no_data": -9999.0
  },
  "flow_directions": {
    "file": "{domain_name}.pnt.txt",
    "mandatory": True,
    "type": "raster",
    "default": None,
    "no_data": -9999
  },
  "channel_network": {
    "file": "{domain_name}.choice.txt",
    "mandatory": True,
    "type": "raster",
    "default": None,
    "no_data": -1
  },
  "curve_number": {
    "file": "{domain_name}.cn.txt",
    "mandatory": False,
    "type": "raster",
    "default": "cn",
    "no_data": -9999.0
  },
  "mask": {
    "file": "{domain_name}.mask.txt",
    "mandatory": True,
    "type": "raster",
    "default": None,
    "no_data": -9999.0
  },
  "alpha": {
    "file": "{domain_name}.alpha.txt",
    "mandatory": True,
    "type": "raster",
    "default": None,
    "no_data": -9999.0
  },
  "beta": {
    "file": "{domain_name}.beta.txt",
    "mandatory": True,
    "type": "raster",
    "default": None,
    "no_data": -9999.0
  },
  "ct": {
    "file": "{domain_name}.ct.txt",
    "mandatory": False,
    "type": "raster",
    "default": "ct",
    "no_data": -9999.0
  },
  "cf": {
    "file": "{domain_name}.cf.txt",
    "mandatory": False,
    "type": "raster",
    "default": "cf",
    "no_data": -9999.0
  },
  "uc": {
    "file": "{domain_name}.uc.txt",
    "mandatory": False,
    "type": "raster",
    "default": "uc",
    "no_data": -9999.0
  },
  "uh": {
    "file": "{domain_name}.uh.txt",
    "mandatory": False,
    "type": "raster",
    "default": "uh",
    "no_data": -9999.0
  }
}
static_data_point = {
  "vegetation_interception": {
    "file": "valori_fo_noIa_AMC2.txt",
    "mandatory": True,
    "type": "array",
    "no_data": None
  }
}
