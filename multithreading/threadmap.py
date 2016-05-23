"""
.. module::  multisthreading.threadmap
   :synopsis:  Reuse pool for thread management.


"""

from multiprocessing.dummy import Pool as ThreadPool
import multiprocessing
import logging
import time
import threading
from common import utils, file_handling

logger = utils.create_and_init_logger(__name__)


def parallel_read(file_names, thread_count):
    logger.debug('start active_threads: %s', threading.activeCount())
    params = [(index, file_name) for index, file_name in enumerate(file_names)]
    pool = ThreadPool(thread_count)
    logger.debug('create active_threads: %s', threading.activeCount())
    try:
        async_results = pool.map_async(
            file_handling.read_file_wrapper, params, chunksize=1)
        results = async_results.get(10)
    except multiprocessing.TimeoutError:
        logger.error('missing results')
        return []
    except:
        logger.exception('underlying thread error')
        return []
    finally:
        pool.close()
        pool.join()
        logger.debug('end active_threads: %s', threading.activeCount())
    return results

if __name__ == "__main__":
    file_names = ['file_{}'.format(i) for i in range(4)]
    thread_count = 2
    for _ in range(4):
        results = parallel_read(file_names, thread_count)
        logger.debug('%s', (results))
