"""
.. module::  multisthreading.thread_file_reader
   :synopsis:  Experimental work related to safe thread management.

Provides low level thread control in a method that can be
called multiple times.


"""
from __future__ import print_function
import logging
from builtins import range
from Queue import Queue, Empty
import threading
from threading import Thread
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug("hello")

worker_threads = 10
work_queue = Queue()
results_queue = Queue()


file_names = ['file_{}'.format(i) for i in range(2)]


def read_file(i, work_queue, results_queue):
    while not work_queue.empty():
        logger.debug('%s: fetching next file', i)
        try:
            file_name = work_queue.get(block=False)
            logger.debug('%s: loading: %s', i, file_name)
            time.sleep(i + 2)
            results_queue.put((0, i, file_name))
            work_queue.task_done()
        except Empty:
            pass
    logger.debug('%s: exiting', i)


for file_name in file_names:
    work_queue.put(file_name)

workers = []
for i in range(worker_threads):
    worker = Thread(target=read_file, args=(i, work_queue, results_queue))
    workers.append(worker)
    worker.setDaemon(True)
    worker.start()


logger.debug('*** Main thread waiting ***')
work_queue.join()
while not results_queue.empty():
    result = results_queue.get()
    logger.debug('result: %s', result)

for worker in workers:
    worker.join(0)
logger.debug('active_threads: %s', threading.activeCount())

logger.debug('*** Done***')