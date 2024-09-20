static_data_point = {
  'section': {
    'file_name': '{domain_name}.info_section.txt',
    'file_mandatory': True,
    'file_type': 'point_section',
    'vars_constants': None,
    'vars_no_data': None,
    'vars_list': None,
    'vars_tags': None,
    'vars_mandatory': None
  },
  'lake': {
    'file_name': '{domain_name}.info_lake.txt',
    'file_mandatory': True,
    'file_type': 'point_lake',
    'vars_constants': None,
    'vars_no_data': None,
    'vars_list': None,
    'vars_tags': None,
    'vars_mandatory': None
  },
  'dam': {
    'file_name': '{domain_name}.info_dam.txt',
    'file_mandatory': True,
    'file_type': 'point_dam',
    'vars_constants': None,
    'vars_no_data': None,
    'vars_list': None,
    'vars_tags': None,
    'vars_mandatory': None
  },
  'joint': {
    'file_name': '{domain_name}.info_joint.txt',
    'file_mandatory': True,
    'file_type': 'point_joint',
    'vars_constants': None,
    'vars_no_data': None,
    'vars_list': None,
    'vars_tags': None,
    'vars_mandatory': None
  },
  'intake': {
    'file_name': '{domain_name}.info_intake.txt',
    'file_mandatory': True,
    'file_type': 'point_intake',
    'vars_constants': None,
    'vars_no_data': None,
    'vars_list': None,
    'vars_tags': None,
    'vars_mandatory': None
  }
}

static_data_grid = {
  "terrain": {
    "file_name": "{domain_name}.dem.txt",
    "file_mandatory": True,
    "file_type": "raster",
    "vars_constants": None,
    "vars_no_data": -9999.0,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  },
  "flow_directions": {
    "file_name": "{domain_name}.pnt.txt",
    "file_mandatory": True,
    "file_type": "raster",
    "vars_constants": None,
    "vars_no_data": -9999.0,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  },
  "channel_network": {
    "file_name": "{domain_name}.choice.txt",
    "file_mandatory": True,
    "file_type": "raster",
    "vars_constants": None,
    "vars_no_data": -1,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  },
  "curve_number": {
    "file_name": "{domain_name}.cn.txt",
    "file_mandatory": False,
    "file_type": "raster",
    "vars_constants": "cn",
    "vars_no_data": -9999.0,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  },
  "mask": {
    "file_name": "{domain_name}.mask.txt",
    "file_mandatory": True,
    "file_type": "raster",
    "vars_constants": None,
    "vars_no_data": -9999.0,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  },
  "alpha": {
    "file_name": "{domain_name}.alpha.txt",
    "file_mandatory": True,
    "file_type": "raster",
    "vars_constants": None,
    "vars_no_data": -9999.0,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  },
  "beta": {
    "file_name": "{domain_name}.beta.txt",
    "file_mandatory": True,
    "file_type": "raster",
    "vars_constants": None,
    "vars_no_data": -9999.0,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  },
  "ct": {
    "file_name": "{domain_name}.ct.txt",
    "file_mandatory": False,
    "file_type": "raster",
    "vars_constants": "ct",
    "vars_no_data": -9999.0,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  },
  "cf": {
    "file_name": "{domain_name}.cf.txt",
    "file_mandatory": False,
    "file_type": "raster",
    "vars_constants": "cf",
    "vars_no_data": -9999.0,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  },
  "uc": {
    "file_name": "{domain_name}.uc.txt",
    "file_mandatory": False,
    "file_type": "raster",
    "vars_constants": "uc",
    "vars_no_data": -9999.0,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  },
  "uh": {
    "file_name": "{domain_name}.uh.txt",
    "file_mandatory": False,
    "file_type": "raster",
    "vars_constants": "uh",
    "vars_no_data": -9999.0,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  },
  "area_cell": {
    "file_name": "{domain_name}.areacell.txt",
    "file_mandatory": True,
    "file_type": "raster",
    "vars_constants": None,
    "vars_no_data": -9999.0,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  },
  "ct_wp": {
    "file_name": "{domain_name}.ct_wp.txt",
    "file_mandatory": False,
    "file_type": "raster",
    "vars_constants": None,
    "vars_no_data": -9999.0,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  },
}
static_data_array = {
  "vegetation_ia": {
    "file_name": "valori_fo_noIa_AMC2.txt",
    "file_mandatory": True,
    "file_type": "array",
    "vars_constants": None,
    "vars_no_data": None,
    "vars_list": None,
    "vars_tags": None,
    "vars_mandatory": None
  }
}
