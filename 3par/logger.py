# coding=utf8
__author__ = 'David'

import logging
from functools import wraps
import time


class Logger():
    def __init__(self, logname, loglevel, logger):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[%(funcName)s]: %(message)s')
        # formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger


mylogger = Logger(logname='3par_automatic.log', loglevel=1, logger="autostart_logger").getlog()


def fn_timer_logger(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        mylogger.debug("Total time running [%s]: %s seconds" %
                       # (function.func_name, str("%.2f" % (t1 - t0))))
                       (function.func_name, str((t1 - t0))))
        return result

    return function_timer