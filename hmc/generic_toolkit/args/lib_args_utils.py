import json
import io
import argparse
import os
from datetime import datetime


# method to get options from command line
def get_options():
    """
    get options from the command line
    """
    args = get_args()
    settings_file, time_start, time_end = check_args(args)

    return settings_file, time_start, time_end


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

    return settings_file, time_start, time_end