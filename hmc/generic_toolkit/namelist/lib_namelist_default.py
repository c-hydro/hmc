namelist_map_default = {
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
    'dWDL': 'wdl'
}


namelist_map_select = {'default': namelist_map_default}


# method to import namelist map
def get_namelist_map(type: str = 'default') -> dict:
    namelist_map = namelist_map_select.get(type, None)
    return namelist_map


# method to convert namelist keys
def convert_namelist_keys(settings_namelist_in: dict, namelist_type='default') -> dict:

    namelist_map_type = get_namelist_map(type=namelist_type)

    if namelist_map_type is None:
        return settings_namelist_in
    settings_namelist_out = {}
    for group_name, group_dict in settings_namelist_in.items():
        for k_in, v in group_dict.items():
            if k_in in namelist_map_type.keys():
                k_out = namelist_map_type[k_in]

                if group_name not in settings_namelist_out.keys():
                    settings_namelist_out[group_name] = {}
                settings_namelist_out[group_name][k_out] = v

    return settings_namelist_out
