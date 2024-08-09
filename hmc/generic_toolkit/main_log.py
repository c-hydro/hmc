import logging

from hmc.generic_toolkit.log import log_handler_base


# ----------------------------------------------------------------------------------------------------------------------
# main function
def main(logger_name='logger'):

    obj_log_handler = log_handler_base.LoggerHandler(log_name=logger_name, log_level=logging.DEBUG)

    obj_log_handler.info("This is an info message.", xtra={'test': 'set extra info'})
    obj_log_handler.error("This is an error message.")
    obj_log_handler.exception("This is an exception message.")
    obj_log_handler.debug("This is an debug message.")

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# call entrypoint
if __name__ == '__main__':

    logger_name = 'logger'

    main(logger_name=logger_name)
# ----------------------------------------------------------------------------------------------------------------------
