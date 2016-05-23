"""
.. module::  multiprocessing.test_performance
   :synopsis:  Capture basic performance metrics.


"""
import time
import unittest
import os
from common import utils
import multiprocessing


logger = utils.create_and_init_logger(__name__)


def do_work(task_id):
    """Simulate process work"""
    # logger.debug('%s doing work in pid %s', task_id, os.getpid())
    # time.sleep(5)


def create_pool(process_count):
    pool = multiprocessing.Pool(process_count)
    return pool


class MultiprocessingPerformanceTestCase(unittest.TestCase):

    def test_do_nothing_process_pool(self):
        total_ms = 0
        process_count = 50
        iter_count = 10
        proc_ids = [proc_id for proc_id in xrange(process_count)]
        for _ in xrange(iter_count):
            with utils.Timer('create_pool', logger=logger) as tm:
                pool = create_pool(process_count)
                pool.map(do_work, proc_ids, chunksize=1)
                pool.close()
                pool.join()
            total_ms += tm.msecs
        msg = 'create & run %s processes total time(ms): %d avg(ms): %f'
        logger.debug(msg,
                     process_count,
                     total_ms,
                     float(total_ms)/iter_count)
