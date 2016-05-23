"""
.. module::  multiprocessing.process_pool
   :synopsis:  Simulate process pool usage.


"""
import multiprocessing
import time
import threading
from common import utils

logger = utils.create_and_init_logger(__name__)


def read_file_wrapper(process_args):
    return read_file(*process_args)


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
    logger.debug('%s: process exiting', i)
    # comment out these lines to avoid simulation of exceptions being raised
    # if i == 0:
    #    msg = '%s: invalid arg %s' % (i, file_name)
    #    logger.error(msg)
    #    raise ValueError(msg)
    return (i, return_code, results)


def parallel_read(file_names, process_count):
    logger.debug('start active_threads: %s', threading.activeCount())
    params = [(index, file_name) for index, file_name in enumerate(file_names)]
    pool = multiprocessing.Pool(process_count)
    logger.debug('create active_threads: %s', threading.activeCount())
    try:
        async_results = pool.map_async(read_file_wrapper, params, chunksize=1)
        results = async_results.get(10)
    except multiprocessing.TimeoutError:
        logger.error('missing results')
        return []
    except:
        logger.exception('underlying process error')
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
        print(results)
