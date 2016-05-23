'''
Created on May 22, 2016

@author: ajaniv
'''
import logging
import functools
import time

_logger = logging.getLogger(__name__)


def create_and_init_logger(logger_name):
    logger = logging.getLogger(logger_name)
    return init_logger(logger)


def init_logger(logger):

    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.debug("start work")
    return logger
    
    
def timeit(method):
    """
    Time function execution.
    """
    @functools.wraps(method)
    def timed(*args, **kw):
        """timer wrapper function."""
        time_start = time.time()
        result = method(*args, **kw)
        time_end = time.time()

        print('%r (%r, %r) %2.2f sec' %
              (method.__name__, args, kw, time_end - time_start))
        return result

    return timed


class Timer(object):
    """
    Class which measures code block execution time.
    """
    msg = "%s elapsed time: %f ms"

    def __init__(self, user_msg, use_clock=False,
                 verbose=True, logger=None):
        self.verbose = verbose
        self.logger = logger or _logger
        self.extra_msg = user_msg
        self.timer_fn = time.clock if use_clock else time.time

    def __enter__(self):
        self.start = self.now()
        return self

    def __exit__(
            self,
            exception_type, exception_value, traceback):  # @UnusedVariable
        self.end = self.now()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs

        if self.verbose:
            self.logger.debug(self.msg, self.extra_msg, self.msecs)

    def now(self):
        """return current time."""
        return self.timer_fn()