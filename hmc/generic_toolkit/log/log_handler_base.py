import os
import logging

from hmc.generic_toolkit.default.lib_default_log import (
    log_name as log_name_default, log_file as log_file_default, log_folder as log_folder_default,
    log_format as log_format_default, log_handler as log_handler_default)

map_debug_level = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
    'NOTSET': logging.NOTSET
}


class LoggerHandler(logging.Logger):
    def __init__(self, log_name: str = log_name_default, log_level=logging.NOTSET,
                 log_file: str = log_file_default, log_folder: str = log_folder_default,
                 log_formatter: str = log_format_default, log_handler: list = log_handler_default):

        super().__init__(log_name, log_level)
        self.extra_info = None

        # set log formatter
        log_formatter = logging.Formatter(log_formatter)

        # add handlers (e.g., ConsoleHandler, FileHandler, etc.)
        if 'stream' in log_handler:
            log_handler_stream = logging.StreamHandler()
            log_handler_stream.setFormatter(log_formatter)
            self.addHandler(log_handler_stream)

        if 'file' in log_handler:
            log_path = self.set_file(log_file, log_folder)
            log_handler_file = logging.FileHandler(log_path, 'w')
            log_handler_file.setFormatter(log_formatter)
            self.addHandler(log_handler_file)

    @classmethod
    def set_level(cls, log_name: str = 'default', log_level: str = 'INFO'):
        log_level = map_debug_level.get(log_level, cls.key_error)
        return cls(log_name=log_name, log_level=log_level)

    @staticmethod
    def set_file(log_file: str, log_folder: str = log_folder_default):
        if log_folder is None:
            log_folder = os.getcwd()
        log_path = os.path.join(log_folder, log_file)
        os.makedirs(log_folder, exist_ok=True)
        return log_path

    def info(self, msg, *args, xtra=None, **kwargs):
        extra_info = xtra if xtra is not None else self.extra_info
        super().info(msg, *args, extra=extra_info, **kwargs)

    def error(self, msg):
        super().error(msg)

    def exception(self, msg):
        super().error(msg, exc_info=True)

    def key_error(self):
        """
        :return:
        """
        raise NotImplementedError
