"""
.. module::  multisthreading.test_performance
   :synopsis:  Check basic threading performance.


"""
import os
import unittest

from common import utils
import threading
from threading import Thread

logger = utils.create_and_init_logger(__name__)


def do_work(task_id):
    """Simulate work"""
    # logger.debug('%s doing work in pid %s', task_id, os.getpid())


def create_threads(thread_count):
    workers = []
    for i in range(thread_count):
        worker = Thread(
            target=do_work,
            args=(i,))
        worker.setDaemon(True)
        workers.append(worker)
    return workers


class ThreadingPerformanceTestCase(unittest.TestCase):

    def test_create_threads(self):
        total_ms = 0
        thread_count = 50
        iter_count = 10
        for _ in xrange(iter_count):
            with utils.Timer('create_threads', logger=logger) as tm:
                workers = create_threads(thread_count)
                for worker in workers:
                    worker.start()
                for worker in workers:
                    worker.join()
            total_ms += tm.msecs
        logger.debug('%s threads create/run  total time(ms): %d avg(ms): %f',
                     thread_count,
                     total_ms,
                     float(total_ms)/iter_count)
