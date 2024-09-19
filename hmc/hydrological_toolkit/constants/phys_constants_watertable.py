# constants for the water-table
const_water_table = {
    # Maximum watertable losses (water sources losses and water deep losses) [-]
    'wt_loss_max': 0.25,
    # Watertable minimum height [mm]
    'wt_h_min': 10.0,
    # Watertable maximum height under the soil [mm] ---> fmin
    'wt_h_u_soil': 100.0,
    # Watertable maximum height under the channels [mm] ---> fcan
    'wt_h_u_channel': 5.0,
    # Maximum slope BM for initializing watertable using beta [-] ---> fpen
    'wt_slope_bm': 0.08,
    # Watertable maximum height over the bedrock (considering the limit of maximum slope BM)  [mm] ---> fov
    'wt_h_o_bedrock': 25.0
}
