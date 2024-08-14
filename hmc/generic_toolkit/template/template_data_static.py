static_data_grid = {
  "terrain": {
    "file": "{domain_name}.dem.txt",
    "mandatory": True,
    "type": "raster",
    "default": None
  },
  "flow_directions": {
    "file": "{domain_name}.pnt.txt",
    "mandatory": True,
    "type": "raster",
    "default": None
  },
  "channel_network": {
    "file": "{domain_name}.choice.txt",
    "mandatory": True,
    "type": "raster",
    "default": None
  },
  "curve_number": {
    "file": "{domain_name}.cn.txt",
    "mandatory": False,
    "type": "raster",
    "default": "cn"
  },
  "mask": {
    "file": "{domain_name}.mask.txt",
    "mandatory": True,
    "type": "raster",
    "default": None
  },
  "alpha": {
    "file": "{domain_name}.alpha.txt",
    "mandatory": True,
    "type": "raster",
    "default": None
  },
  "beta": {
    "file": "{domain_name}.beta.txt",
    "mandatory": True,
    "type": "raster",
    "default": None
  },
  "ct": {
    "file": "{domain_name}.ct.txt",
    "mandatory": False,
    "type": "raster",
    "default": "ct"
  },
  "cf": {
    "file": "{domain_name}.cf.txt",
    "mandatory": False,
    "type": "raster",
    "default": "cf"
  },
  "uc": {
    "file": "{domain_name}.uc.txt",
    "mandatory": False,
    "type": "raster",
    "default": "uc"
  },
  "uh": {
    "file": "{domain_name}.uh.txt",
    "mandatory": False,
    "type": "raster",
    "default": "uh"
  }
}
static_data_point = {
  "vegetation_interception": {
    "file": "valori_fo_noIa_AMC2.txt",
    "mandatory": True,
    "type": "array"
  }
}
