dynamic_data_grid = {
  "dynamic_src_grid": {
    "file": "hmc.forcing-grid.{datetime_dynamic_src_grid}.nc.gz",
    "mandatory": True,
    "type": "raster"
  },
  "dynamic_dst_grid": {
    "file": "hmc.output-grid.{datetime_dynamic_dst_grid}.nc.gz",
    "mandatory": True,
    "type": "raster"
  }
}
dynamic_data_point = {
   "dynamic_src_point": {
     "file": "hmc.forcing-point.{datetime_dynamic_src_point}.txt",
     "mandatory": True,
     "type": "array"
   },
   "file_data_dynamic_dst_point": {
     "file": "hmc.output-point.{datetime_dynamic_dst_point}.txt",
     "mandatory": True,
     "type": "array"
   }
}
