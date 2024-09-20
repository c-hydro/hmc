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
from hmc.generic_toolkit.info import info_handler_base

from hmc.hydrological_toolkit.constants import phys_constants_lsm
from hmc.hydrological_toolkit.constants import phys_constants_snow

from hmc.driver_variables import VariablesDriver
from hmc.driver_data_static import StaticDriver
from hmc.driver_data_dynamic import DynamicDriver

from hmc.driver_geo_main import GeoDriver
from hmc.driver_phys_main import PhysDriver

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
    # method to define static grid dimension(s)
    info_dims_data_static_grid = info_handler_base.InfoHandler.get_data_dims_by_file(
        folder_name=namelist_obj['settings']['path_data_static_grid'], file_name='{domain_name}.dem.txt',
        file_tags_definitions={'domain_name':  namelist_obj['parameters']['domain_name']},
        file_tags_pattern=namelist_tags_obj.tags_string, file_type='raster')

    # method to define static point dimension(s)
    info_dims_data_static_point = info_handler_base.InfoHandler.get_data_dims_by_template(
        folder_name=namelist_obj['settings']['path_data_static_point'],
        file_tags_definitions={'domain_name':  namelist_obj['parameters']['domain_name']},
        file_tags_pattern=namelist_tags_obj.tags_string,
        file_template=namelist_data_static_obj.static_data_point)

    # method to define dynamic grid dimension(s)
    info_dims_data_dynamic_grid = info_handler_base.InfoHandler.get_data_dims_by_file(
        folder_name=namelist_obj['settings']['path_data_dynamic_src_grid'],
        file_name='hmc.forcing-grid.{datetime_dynamic_src_grid}.nc.gz',
        file_time=namelist_obj['settings']['time_start'],
        file_tags_definitions={'domain_name': namelist_obj['parameters']['domain_name']},
        file_tags_pattern={**namelist_tags_obj.tags_string, **namelist_tags_obj.tags_time})

    # method to define time dimension(s)
    info_dims_time = info_handler_base.InfoHandler.get_time_dims_by_file(
        folder_name=namelist_obj['settings']['path_data_static_grid'], file_name='{domain_name}.areacell.txt',
        file_tags_definitions={'domain_name':  namelist_obj['parameters']['domain_name']},
        file_tags_pattern=namelist_tags_obj.tags_string,
        time_period_sim=namelist_obj['settings']['time_period'], time_deep_shift=2)
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # driver variables
    driver_variables = VariablesDriver(
        parameters=namelist_obj['parameters'],
        da_reference=info_dims_data_static_grid, time_reference=info_dims_time)
    vars_geo_generic, vars_geo_routing, vars_geo_horton, vars_geo_wt, vars_geo_lsm = driver_variables.allocate_variables_geo()
    vars_data_src = driver_variables.allocate_variables_data()
    (dset_phys_lsm, dset_phys_et, dset_phys_snow,
     dset_phys_volume, dset_phys_routing) = driver_variables.allocate_variables_phys()
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # driver static data
    driver_data_static = StaticDriver(
        obj_namelist=namelist_obj,
        obj_tags={'domain_name': namelist_obj['parameters']['domain_name']},
        obj_reference=reference_static_obj_terrain)
    # method to organize static data (point, grid, array)
    data_geo_point, data_geo_grid, data_geo_array = driver_data_static.organize_data(
        namelist_data_static_obj, namelist_tags_obj)
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # driver physics geo
    driver_geo = GeoDriver(data_geo_grid, data_geo_array, reference_static_obj_terrain,
                           parameters=namelist_obj['parameters'])
    # method to wrap geo routine(
    dset_geo_generic, dset_geo_params, dset_geo_volume, dset_geo_lsm, dset_geo_horton, dset_geo_surface = driver_geo.wrap_geo()
    # method to organize geo object(s)
    dset_geo_lsm = driver_geo.organize_geo(dset_geo_lsm, vars_geo_lsm)
    dset_geo_horton = driver_geo.organize_geo(dset_geo_horton, vars_geo_horton)

    # method to organize phys volume object(s)
    dset_phys_volume = driver_geo.organize_geo(dset_geo_volume, dset_phys_volume)
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # iterate over times
    for time_step in time_range_obj:

        if time_step == time_handler.time_data_src_grid:

            # driver dynamic data
            driver_data_dynamic = DynamicDriver(
                obj_namelist=namelist_obj,
                obj_tags={'domain_name': namelist_obj['parameters']['domain_name']},
                obj_reference=reference_data_static_grid)
            # method to organize dynamic data
            dset_data_dynamic_src_obj = driver_data_dynamic.organize_data(
                time_step, namelist_data_dynamic_obj, namelist_tags_obj)

            # driver physics
            driver_phys = PhysDriver(
                time_step=time_step, time_info=reference_time_obj,
                dset_geo_generic=dset_geo_generic, dset_geo_parameters=dset_geo_params,
                dset_data=dset_data_dynamic_src_obj,
                da_reference=reference_static_obj_terrain)

            # wrap physics lsm routine(s)
            dset_phys_lsm, dset_phys_et = driver_phys.wrap_physics_lsm(
                dset_geo_lsm=dset_geo_lsm,
                dset_phys_lsm=dset_phys_lsm, dset_phys_et=dset_phys_et, dset_phys_snow=dset_phys_snow,
                dset_phys_volume=dset_phys_volume)

            # wrap physics phys_et routine(s)
            dset_phys_et, dset_phys_volume = driver_phys.wrap_physics_et(
                dset_geo_lsm=dset_geo_lsm,
                dset_phys_lsm=dset_phys_lsm, dset_phys_et=dset_phys_et, dset_phys_snow=dset_phys_snow,
                dset_phys_volume=dset_phys_volume)

            # update time
            time_handler.time_data_src_grid = time_handler.get_next_time(
                time_handler.time_data_src_grid, time_handler.dt_data_src_grid)

        print('time cycle:', time_step)

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # info algorithm (end)
    alg_time_elapsed = round(time.time() - start_time, 1)

    logger_obj.info(' ')
    logger_obj.info(' ==> ' + alg_name + ' (Version: ' + alg_version + ' Release_Date: ' + alg_release + ')')
    logger_obj.info(' ==> TIME ELAPSED: ' + str(alg_time_elapsed) + ' seconds')
    logger_obj.info(' ==> ... END')
    logger_obj.info(' ==> Bye, Bye')
    logger_obj.info(' ============================================================================ ')
    # ------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# call entrypoint
if __name__ == '__main__':
    hmc_main()
# ----------------------------------------------------------------------------------------------------------------------
