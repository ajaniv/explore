"""
.. module::  multisthreading.thread_file_reader_class
   :synopsis:  Manage a set of threads.

Provides low level thread control in a method that can be
called multiple times.


"""
import threading
from threading import Thread
import Queue

from common import utils
from common import file_handling

logger = utils.create_and_init_logger(__name__)


class ThreadingFileHandler(object):
    """Base class for threaded file handling"""
    def __init__(self, work_items, thread_count, target=None):
        self.work_items = work_items
        self.thread_count = thread_count
        self.work_queue = Queue.Queue()
        self.results_queue = Queue.Queue()
        self.workers = []
        self.target = target

    def _create_threads(self):
        workers = self.workers
        work_queue = self.work_queue
        results_queue = self.results_queue
        for i in range(self.thread_count):
            worker = Thread(
                target=self.target,
                args=(i, work_queue, results_queue))
            worker.setDaemon(True)
            workers.append(worker)
        logger.debug("created %s threads", len(self.workers))

    def _start_threads(self):
        for worker in self.workers:
            worker.start()
        logger.debug("started %s threads", len(self.workers))

    def _build_work_queue(self):
        work_queue = self.work_queue
        for work_item in self.work_items:
            work_queue.put(work_item)

    def _join_threads(self):
        for worker in self.workers:
            worker.join()
        logger.debug("joined %s threads", len(self.workers))

    def _results(self):
        results = []
        self.work_queue.join()
        results_queue = self.results_queue
        while not self.results_queue.empty():
            result = results_queue.get()
            results.append(result)

        logger.debug("fetched %s results", len(results))
        return results

    def run(self):
        start_active_threads = threading.activeCount()
        logger.debug('start active_threads: %s', start_active_threads)
        self._create_threads()
        self._build_work_queue()
        self._start_threads()
        self._join_threads()
        results = self._results()
        if len(results) != len(self.work_items):
            logger.error('missing %s results',
                         len(self.work_items) - len(results))
        end_active_threads = threading.activeCount()
        logger.debug('end active_threads: %s', end_active_threads)
        if start_active_threads != end_active_threads:
            logger.warning(
                'potential zombie threads count: %s',
                end_active_threads - start_active_threads)


class ThreadingFileReader(ThreadingFileHandler):
    """File reader thread manager"""
    def __init__(self, work_items, thread_count, target=None):
        super(ThreadingFileReader, self).__init__(work_items, thread_count)
        self.target = target or file_handling.read_file_using_queues


if __name__ == "__main__":
    file_names = ("file_1", "file_2")
    thread_count = 10
    for _ in range(5):
        reader = ThreadingFileReader(file_names, thread_count)
        reader.run()
