"""
.. module::  pandas_io.test_performance
   :synopsis:  Check basic pandas io performance.




"""
import unittest
import pandas as pd
import numpy as np
from common import utils


logger = utils.create_and_init_logger(__name__)


def save_dataframe(df, file_name=None):
    file_name = file_name or 'test.csv'
    df.to_csv(file_name, mode='w')
    return file_name


def read_dataframe(file_name=None):
    file_name = file_name or 'test.csv'
    return pd.read_csv(file_name, index_col=0)


def create_dataframe(row_count=None):
    row_count = row_count or 1000000
    return pd.DataFrame(np.random.randn(row_count, 2), columns=list('AB'))


class PandasCSVPerformanceTestCase(unittest.TestCase):

    def test_csv_write_single_process(self):
        df = create_dataframe()
        total_ms = 0
        write_count = 10
        for _ in xrange(write_count):
            with utils.Timer('csv_write', logger=logger) as tm:
                save_dataframe(df)
            total_ms += tm.msecs
        logger.debug('csv write total time(ms): %d avg(ms): %f',
                     total_ms,
                     float(total_ms)/write_count)

    def test_csv_read(self):
        df = create_dataframe()
        file_name = save_dataframe(df)
        total_ms = 0
        read_count = 10
        for _ in xrange(read_count):
            with utils.Timer('csv_read', logger=logger) as tm:
                read_dataframe(file_name)
            total_ms += tm.msecs
        logger.debug('csv read total time(ms): %d avg(ms): %f',
                     total_ms,
                     float(total_ms)/read_count)
