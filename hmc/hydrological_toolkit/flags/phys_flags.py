# flags physical processes
flags = {
    # activate deep flow [0: not activate, 1: activate]
    'flow_deep': 1,
    # restart a run [0: not restart, 1: restart]
    'restart': 1,
    # dynamic integration step of convolution [0: not activate, 1: activate]
    'dt_phys_conv': 1,
    # activate snow [0: not activate, 1: activate]
    'snow': 1,
    # activate snow assimilation [0: not activate, 1: activate]
    'snow_assimilation': 0,
    # activate soil moisture assimilation [0: not activate, 1: activate]
    'sm_assimilation': 0,
    # LAI mode [0: empiric relationship, 1: using data]
    'lai': 0,
    # Albedo mode [0: static value, 1: dynamic monthly values]
    'albedo': 0,
    # Coeff Resolution default mode [0: null, 1: empiric relationship]
    'coeff_res': 0,
    # Watertable sources mode [0: deactivate, 1: activate]
    'ws': 0,
    # Watertable deep losses mode [0: deactivate, 1: activate]
    'wdl': 0,
    # Release MassBalance control [0: deactivate, 1: activate]
    'release_mass': 1,
    # Channel treatment type [1: channel network, 2: channel fraction]
    'ctype': 1,
    # Groundwater bedrock fracturation [0: deactivate, 1: activate]
    'frac': 0,
    # Vegetation Dynamic module [0: deactivate, 1: activate]
    'dyn_veg': 0,
    # Flooding Dynamic module [0: deactivate, 1: activate]
    'flood': 0,
    # Energy Balance module [0: deactivate, 1: activate]
    'energy_balance': 1
}
