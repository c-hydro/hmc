
from hmc.generic_toolkit.namelist import namelist_handler_base
from hmc.generic_toolkit.info import info_handler_base
from hmc.generic_toolkit.time import time_handler_base

# ----------------------------------------------------------------------------------------------------------------------
# main function
def main(file_name_static: str = None, folder_name_static: str = None,
         file_name_dynamic: str = None, folder_name_dynamic: str = None,
         time_run: str = None):

    namelist_tags_obj, namelist_data_static_obj, namelist_data_dynamic_obj = (
        namelist_handler_base.NamelistHandler.get_template_default())

    time_run = time_handler_base.TimeHandler.convert_time_string_to_stamp(time_run)

    # method to define info handler
    info_handler = info_handler_base.InfoHandler.organize_file_obj(
        folder_name=folder_name_static, file_name=file_name_static,
        file_tags={'domain_name': 'bisagno'}, file_template=namelist_tags_obj.tags_string)
    info_static_obj = info_handler.get_file_info()

    # method to define info handler
    info_handler = info_handler_base.InfoHandler.organize_file_obj(
        folder_name=folder_name_dynamic, file_name=file_name_dynamic,
        file_time=time_run,
        file_tags={'domain_name': 'bisagno'},
        file_template={**namelist_tags_obj.tags_string, **namelist_tags_obj.tags_time})
    info_dynamic_obj = info_handler.get_file_info()

    print()


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# call entrypoint
if __name__ == '__main__':

    file_name_static = 'bisagno.dem.txt'
    folder_name_static = '/home/fabio/Desktop/HMC_Package/data/geo/'

    time_run = '2022-03-07 12:00:00'

    file_name_dynamic = 'hmc.forcing-grid.{datetime_dynamic_src_grid}.nc'
    folder_name_dynamic = '/home/fabio/Desktop/HMC_Package/data/meteo/{sub_path_dynamic_src_grid}/'

    main(file_name_static=file_name_static, folder_name_static=folder_name_static,
         file_name_dynamic=file_name_dynamic, folder_name_dynamic=folder_name_dynamic,
         time_run=time_run)
# ----------------------------------------------------------------------------------------------------------------------
