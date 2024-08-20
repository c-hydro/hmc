
from hmc.generic_toolkit.data import io_handler_static


# ----------------------------------------------------------------------------------------------------------------------
# main function
def main(file_name: str = None, folder_name: str = None):

    row_start, row_end, col_start, col_end = 0, 9, 3, 15

    # method to define static handler
    io_static_handler = io_handler_static.StaticHandler.define_file_data(
        folder_name=folder_name, file_name=file_name,
        file_tags={'domain_name': 'bisagno'})
    data_static_grid = io_static_handler.get_file_data()

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# call entrypoint
if __name__ == '__main__':

    file_name = 'bisagno.dem.txt'
    folder_name = '/home/fabio/Desktop/HMC_Package/data/geo/'

    main(file_name=file_name, folder_name=folder_name)
# ----------------------------------------------------------------------------------------------------------------------
