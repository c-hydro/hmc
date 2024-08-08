
from data import io_handler_base

# ----------------------------------------------------------------------------------------------------------------------
# main function
def main(file_name: str = None, folder_name: str = None):

    row_start, row_end, col_start, col_end = 0, 9, 3, 15

    obj_data_handler = io_handler_base.IOHandler(file_name=file_name, folder_name=folder_name)
    obj_data_domain = obj_data_handler.get_data(
        row_start=row_start, row_end=row_end, col_start=col_start, col_end=col_end, mandatory=True)

    obj_data_handler.view_data(obj_data=obj_data_domain,
                               var_name='AirTemperature', var_data_min=0, var_data_max=None)

    print()

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# call entrypoint
if __name__ == '__main__':

    file_name = 'bisagno.dem.txt'
    folder_name = '/home/fabio/Desktop/HMC_Package/data/geo/'

    file_name = 'hmc.forcing-grid.202203071200.nc'
    folder_name = '/home/fabio/Desktop/HMC_Package/data/meteo/2022/03/07/'

    main(file_name=file_name, folder_name=folder_name)
# ----------------------------------------------------------------------------------------------------------------------
