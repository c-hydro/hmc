namelist_variable_default = {
    'dUc': 'uc',
    'dUh': 'uh',
    'dCt': 'ct',
    'dCf': 'cf',
    'sDomainName': 'domain_name',
    'dCPI': 'cpi',
    'dWTableHbr': 'wtable_hbr',
    'dKSatRatio': 'ksat_ratio',
    'dSlopeMax': 'slope_max',
    'dCN': 'cn',
    'dFrac': 'frac',
    'dWS': 'ws',
    'dWDL': 'wdl',
    'iSimLength': 'time_period',
    'iDtModel': 'dt_model',
    'iDtData_Forcing': 'dt_data_src',
    'iDtData_Output_Gridded': 'dt_data_dst_gridded',
    'iDtData_Output_Point': 'dt_data_dst_point',
    'sTimeStart': 'time_start',
    'sTimeRestart': 'time_restart',
    'sPathData_Static_Gridded': 'path_data_static_grid',
    'sPathData_Static_Point': 'path_data_static_point',
    'sPathData_Forcing_Gridded': 'path_data_dynamic_src_grid',
    'sPathData_Forcing_Point': 'path_data_dynamic_src_point',
    'sPathData_Forcing_TimeSeries': 'path_data_dynamic_src_ts',
    'sPathData_Output_Gridded': 'path_data_dynamic_dst_grid',
    'sPathData_Output_Point': 'path_data_dynamic_dst_point',
    'sPathData_Output_TimeSeries': 'path_data_dynamic_dst_ts',
}

namelist_group_default = {
    'HMC_Parameters': 'parameters',
    'HMC_Namelist': 'settings',
    'HMC_Info': 'info',
}


# namelist map selector
namelist_variable_type = {'default': namelist_variable_default}
# namelist map selector
namelist_group_type = {'default': namelist_group_default}


# method to import namelist map
def map_namelist_variable(type: str = 'default') -> dict:
    namelist_variable_map = namelist_variable_type.get(type, None)
    return namelist_variable_map


def map_namelist_group(type: str = 'default') -> dict:
    namelist_group_map = namelist_group_type.get(type, None)
    return namelist_group_map


# method to convert namelist keys
def convert_namelist_keys(settings_namelist_in: dict,
                          variable_type: str = 'default', group_type: str = 'default') -> dict:

    namelist_variable_map = map_namelist_variable(type=variable_type)
    namelist_group_map = map_namelist_group(type=group_type)

    if namelist_variable_map is None:
        return settings_namelist_in

    settings_namelist_out = {}
    for group_name, group_dict in settings_namelist_in.items():
        for k_in, v in group_dict.items():
            if k_in in namelist_variable_map.keys():
                k_out = namelist_variable_map[k_in]

                if group_name not in settings_namelist_out.keys():
                    settings_namelist_out[group_name] = {}
                settings_namelist_out[group_name][k_out] = v

    for group_name, group_dict in settings_namelist_out.items():
        if group_name in namelist_group_map.keys():
            group_name_out = namelist_group_map[group_name]
            settings_namelist_out[group_name_out] = settings_namelist_out.pop(group_name)

    return settings_namelist_out
