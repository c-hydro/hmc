# define constants for the land surface model
const_lsm = {
    # Reference temperature [K]
    't_ref': 273.15,
    # Soil emissivity [-]
    'eps_s': 0.96,
    # Stefan-Boltzmann Constant [W/m^2 K]
    'sigma': 0.00000005576,
    # Min value beta function
    'bf_min': 0.1,
    # Max value beta function
    'bf_max': 0.9,
    # LST maximum delta to limit runge-kutta integration method [K]
    'lst_delta_max': 40.0,
    # Z reference for wind [m]
    'z_ref': 3.0,
    # Gravity acceleration [m s^-2]
    'g': 9.81,
    # Specific heat at constant pressure [J/kg/K]
    'cp': 1004.0,
    # Gas constant for air [J/kg K]
    'rd': 287.0,
    # Soil density [kg m^-3]
    'rho_s': 2700,
    # Water density [kg m^-3]
    'rho_w': 1000,
    # Soil specific heat [J kg^-1 K^-1]
    'cp_s': 733,
    # Water specific heat [J kg^-1 K^-1]
    'cp_w': 4186,
    # Quartz thermic conductivity [W m^-1 K^-1]
    'kq': 7.7,
    # Water thermic conductivity [W m^-1 K^-1]
    'kw': 0.57,
    # Other minerals thermic conductivity [W m^-1 K^-1] --> Orba = 4; Casentino = 2
    'ko': 4,
    # Soil Porosity [-]
    'porosity_s': 0.4,
    # Quartz soil fraction [-]
    'fq_s': 0.5,
    # Time steps shift for deep soil temperature [hour]
    'td_steps_shift': 2,
    # CH Monthly Constant [-7.3, -7.3, -5.8, -5.8, -5.8, -4.8, -4.8, -4.8, -4.8, -5.9, -5.9, -7.3]
    'ch': [-7.3, -7.3, -5.8, -5.8, -5.8, -4.8, -4.8, -4.8, -4.8, -5.9, -5.9, -7.3]
}