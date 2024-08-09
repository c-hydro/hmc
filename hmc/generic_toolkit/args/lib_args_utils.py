
import argparse
import os

# method to get options from command line
def get_options():
    """
    get options from the command line
    """
    args = get_args()
    settings_file, time_start, time_end, log_level = check_args(args)

    return settings_file, time_start, time_end, log_level


# method to get command line arguments
def get_args():
    """
    parse arguments from the command line
    two or three arguments are expected:
    - options: a json file with the options
    - time: a date for which to calculate the index
    OR 
    - options
    - time_start: a start date for the time range
    - time_end: an end date for the time range
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-settings_file', help='Settings file with the options', required=True)
    parser.add_argument('-time_start', help='Start date for the time range')
    parser.add_argument('-time_end', help='End date for the time range')
    parser.add_argument('-log_level', help='Log level', default='INFO')
    args = parser.parse_args()

    return args


# method to check command line arguments
def check_args(args):

    settings_file = None
    if args.settings_file:
        settings_file = args.settings_file

    time_start, time_end = None, None
    if args.time_start:
        time_start = args.time_start
    if args.time_end:
        time_end = args.time_end

    if settings_file is None or not os.path.exists(settings_file):
        raise ValueError(f'{settings_file} does not exist')

    log_level = None
    if args.log_level:
        log_level = args.log_level
    if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'NOTSET']:
        raise ValueError(f'Invalid log level: {args.log_level}')

    return settings_file, time_start, time_end, log_level
