"""
This is the main entrypoint for the HMC project.
"""
# ------------------------------------------------------------------------------------------------------------------
# libraries
import time

from hmc.generic_toolkit.default.lib_default_log import log_name
from hmc.generic_toolkit.default.lib_default_info import alg_version, alg_name, alg_release

from hmc.generic_toolkit.args.lib_args_utils import get_options

from hmc.generic_toolkit.log import log_handler_base
from hmc.generic_toolkit.namelist import namelist_handler_base
from hmc.generic_toolkit.time import time_handler_base

from hmc.generic_toolkit.data import io_handler_static
from hmc.generic_toolkit.data import io_handler_dynamic_src
# ------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Hydrological Model Continuum main (sequential mode
def hmc_main():

    # ------------------------------------------------------------------------------------------------------------------
    # get algorithm options
    settings_file, time_start, time_end, log_level = get_options()
    # get algorithm logger object
    logger_obj = log_handler_base.LoggerHandler(
        log_name=log_name, log_level=log_handler_base.map_debug_level[log_level])
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # info algorithm (start)
    logger_obj.info(' ============================================================================ ')
    logger_obj.info(' ==> ' + alg_name + ' (Version: ' + alg_version + ' Release_Date: ' + alg_release + ')')
    logger_obj.info(' ==> START ... ')
    logger_obj.info(' ')

    # time algorithm
    start_time = time.time()
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # get namelist object(s)
    namelist_handler = namelist_handler_base.NamelistHandler(settings_file)
    namelist_obj = namelist_handler.get_data()
    namelist_tags_obj, namelist_data_static_obj, namelist_data_dynamic_obj = namelist_handler.get_template_default()

    # get time object(s)
    time_handler = time_handler_base.TimeHandler(
        time_run=namelist_obj['settings']['time_start'],
        time_period=namelist_obj['settings']['time_period'],)
    time_range_obj = time_handler.get_times()
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to define static handler
    data_static_grid = io_handler_static.StaticHandler.organize_file_obj(
        folder_name=namelist_obj['settings']['path_data_static_grid'],
        file_collections=namelist_data_static_obj.static_data_grid,
        file_tags={'domain_name': namelist_obj['parameters']['domain_name']},
        file_template=namelist_tags_obj)

    print('geo application ... ')

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # iterate over times
    for time_step in time_range_obj:

        if time_step == time_handler.time_data_src_grid:

            io_dynamic_src_grid_handler = io_handler_dynamic_src.DynamicSrcHandler.organize_file_obj(
                folder_name=namelist_obj['settings']['path_data_dynamic_src_grid'],
                file_name=namelist_data_dynamic_obj.dynamic_data_grid['dynamic_src_grid']['file'],
                file_mandatory=namelist_data_dynamic_obj.dynamic_data_grid['dynamic_src_grid']['mandatory'],
                file_time=time_step,
                file_template=namelist_tags_obj.tags_time)

            data_dynamic_grid_src = io_dynamic_src_grid_handler.get_file_data()

            time_handler.time_data_src_grid = time_handler.get_next_time(
                time_handler.time_data_src_grid, time_handler.dt_data_src_grid)

        print('time cycle:', time_step)

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # info algorithm (end)
    alg_time_elapsed = round(time.time() - start_time, 1)

    alg_logger.info(' ')
    alg_logger.info(' ==> ' + alg_name + ' (Version: ' + alg_version + ' Release_Date: ' + alg_release + ')')
    alg_logger.info(' ==> TIME ELAPSED: ' + str(alg_time_elapsed) + ' seconds')
    alg_logger.info(' ==> ... END')
    alg_logger.info(' ==> Bye, Bye')
    alg_logger.info(' ============================================================================ ')
    # ------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# call entrypoint
if __name__ == '__main__':
    hmc_main()
# ----------------------------------------------------------------------------------------------------------------------
