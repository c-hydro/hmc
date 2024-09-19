# define constants for the phys_snow model
const_snow = {
    "arc_up": (3.0, 4.5, 3.0, 4.0),                     # [-]
    "exp_rho_low": (0.0333, 0.0222, 0.0250, 0.0333),    # Frequency to phys_snow rhow max limit [1/day] --> no melting
    "exp_rho_high": (0.0714, 0.0714, 0.0714, 0.0714),   # Frequency to phys_snow rhow max limit[1/day] --> melting
    "altitude_range": (1500.0, 2000.0, 2500.0, 2500.0), # Altitude range to select ExpRho low and high [m asl]
    "glacier_value": 2,                                 # Value of glacier(s) in nature map [-]
    "rho_snow_fresh": 100,                              # Fresh phys_snow density [kg/m^3]
    "rho_snow_max": 400,                                # Maximum phys_snow density [kg/m^3]
    "snow_quality_thr": 0.3,                            # Quality threshold of phys_snow cover area map
    "melting_t_ref": 1                                  # Soil melting reference temperature [C]
}
