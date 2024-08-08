import os
import re
import numpy as np


from hmc.generic_toolkit.namelist import namelist_handler_base


# ----------------------------------------------------------------------------------------------------------------------
# main function
def main(file_name: str = None, folder_name: str = None):

    path_name = os.path.join(folder_name, file_name)

    obj_namelist_handler = namelist_handler_base.NamelistHandler(file_name=path_name)
    obj_namelist_data = obj_namelist_handler.get_data()
    obj_namelist_handler.view_data(obj_namelist_data['HMC_Parameters'])


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# call entrypoint
if __name__ == '__main__':

    file_name = 'marche.info_MANUAL.txt'
    folder_name = '/home/fabio/Desktop/HMC_Package/data/namelist'

    main(file_name=file_name, folder_name=folder_name)
# ----------------------------------------------------------------------------------------------------------------------
