"""
Library Features:

Name:          lib_default_log
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20240808'
Version:       '1.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# log information
logger_name = 'hmc'
logger_file = 'log.txt'
logger_handle = 'file'  # 'file' or 'stream'
logger_format = '%(asctime)s %(name)-12s %(levelname)-8s ' \
                '%(message)-80s %(filename)s:[%(lineno)-6s - %(funcName)-20s()] '
# ----------------------------------------------------------------------------------------------------------------------
