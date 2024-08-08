
from hmc.generic_toolkit.time import time_handler_base


# ----------------------------------------------------------------------------------------------------------------------
# main function
def main(time_run: str = None, time_period: int = 0, time_start : str = None, time_end: str = None):

    obj_time_handler = time_handler_base.TimeHandler.from_time_string(time_run=time_run, time_period=time_period)
    obj_times_generic = obj_time_handler.get_times()

    obj_times_by_step = obj_time_handler.select_times_by_step(
        time_range=obj_times_generic, time_unit='H', time_step=23)

    obj_time_handler = time_handler_base.TimeHandler.from_time_period(time_start=time_start, time_end=time_end)
    obj_times_generic = obj_time_handler.get_times()

    print()

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# call entrypoint
if __name__ == '__main__':

    time_run = '2022-03-07 12:35'
    time_start, time_end = '2022-03-01 00:00', '2022-03-07 18:00'
    time_period = 96

    main(time_run=time_run, time_period=time_period, time_start=time_start, time_end=time_end)
# ----------------------------------------------------------------------------------------------------------------------
