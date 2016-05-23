'''
Created on May 22, 2016

@author: ajaniv
'''
import logging
import time
import Queue
from common import utils
logger = logging.getLogger(__name__)

utils.init_logger(logger)


def read_file_using_queues(i, work_queue, results_queue):
    while not work_queue.empty():
        logger.debug('%s: fetching next file', i)
        try:
            file_name = work_queue.get(block=False)
            logger.debug('%s: loading: %s', i, file_name)
            time.sleep(i + 2)
            results_queue.put((0, i, file_name))
            work_queue.task_done()
        except Queue.Empty:
            pass
    logger.debug('%s: exiting', i)


def read_file_wrapper(a_b):
    return read_file(*a_b)


def read_file(i, file_name):
    logger.debug('%s: fetching next file %s', i, file_name)

    # TODO: figure out whether we want to capture all exceptions,
    # return as part of result, or let the exceptions be thrown
    return_code = -1
    results = None
    try:
        time.sleep(i + 2)
        return_code = 0
        results = file_name
    except Exception:
        logger.exeption('read process exception')
    logger.debug('%s: process/thread exiting', i)
    # comment out these lines to avoid simulation of exceptions being raised
    # if i == 0:
    #    msg = '%s: invalid arg %s' % (i, file_name)
    #    logger.error(msg)
    #    raise ValueError(msg)
    return (i, return_code, results)
