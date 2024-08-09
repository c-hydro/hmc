"""
This is the main entrypoint for the HMC project.
"""
# ------------------------------------------------------------------------------------------------------------------
# libraries
import time

from hmc.generic_toolkit.default.lib_default_info import alg_version, alg_name, alg_release

from hmc.generic_toolkit.args.lib_args_utils import get_options

from hmc.generic_toolkit.log import log_handler_base
from hmc.generic_toolkit.namelist import namelist_handler_base
from hmc.generic_toolkit.time import time_handler_base
# ------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Hydrological Model Continuum main (sequential mode
def hmc_main():

    # ------------------------------------------------------------------------------------------------------------------
    # get options
    settings_file, time_start, time_end, log_level = get_options()
    # get logger object
    logger_obj = log_handler_base.LoggerHandler(log_name='hmc', log_level=log_handler_base.map_debug_level[log_level])
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
    # get namelist obj
    namelist_handler = namelist_handler_base.NamelistHandler(settings_file)
    namelist_obj = namelist_handler.get_data()

    # get time obj
    time_handler = time_handler_base.TimeHandler(
        time_run=namelist_obj['settings']['time_start'],
        time_period=namelist_obj['settings']['time_period'],)
    time_obj = time_handler.get_times()
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # iterate over times
    for time_step in time_obj:

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
