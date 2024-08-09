import unittest
import logging

from hmc.generic_toolkit.log import log_handler_base


class TestLog(unittest.TestCase):
    def setUp(self):
        self.log_handler = log_handler_base.LoggerHandler(name='logger', level=logging.NOTSET)

    def test_init(self):
        self.assertEqual(self.log_handler.name, 'logger')
        self.assertEqual(self.log_handler.extra_info, None)

    def test_set_logger(self):
        pass


if __name__ == '__main__':
    unittest.main()
