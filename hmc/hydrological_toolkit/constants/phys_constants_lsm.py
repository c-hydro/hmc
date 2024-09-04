# define constants for the land surface model
const_lsm = {
    't_ref': 273.15,            # Reference temperature [K]
    'eps_s': 0.96,              # Soil emissivity [-]
    'sigma': 0.00000005576,     # Stefan-Boltzmann Constant [W/m^2 K]
    'bf_min': 0.1,              # Min value beta function
    'bf_max': 0.9,              # Max value beta function
    'lst_delta_max': 40.0,      # LST maximum delta to limit runge-kutta integration method [K]
    'z_ref': 3.0,               # Z reference for wind [m]
    'g': 9.81,                  # Gravity acceleration [m s^-2]
    'cp': 1004.0,               # Specific heat at constant pressure [J/kg/K]
    'rd': 287.0,                # Gas constant for air [J/kg K]
    'rho_s': 2700,              # Soil density [kg m^-3]
    'rho_w': 1000,              # Water density [kg m^-3]
    'cp_s': 733,                # Soil specific heat [J kg^-1 K^-1]
    'cp_w': 4186,               # Water specific heat [J kg^-1 K^-1]
    'kq': 7.7,                  # Quartz thermic conductivity [W m^-1 K^-1]
    'kw': 0.57,                 # Water thermic conductivity [W m^-1 K^-1]
    'ko': 4,                    # Other minerals thermic conductivity [W m^-1 K^-1] --> Orba = 4; Casentino = 2
    'porosity_s': 0.4,          # Soil Porosity [-]
    'fq_s': 0.5                 # Quartz soil fraction [-]
}