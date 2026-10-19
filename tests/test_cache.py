"""Unit-tests for just.cache"""

# standard imports
import unittest
import logging
import time

# tested imports
from just.cache import memoize, ttl_cache


class TestMemoize(unittest.TestCase):
    """test `just.cache.memoize`."""

    def setUp(self):
        self._logger = logging.getLogger(__name__)

    def test_memoize(self):
        """test `just.cache.memoize`."""

        @memoize
        def test_func() -> None:
            self._logger.debug("calling `test_func`")

        with self.assertLogs(self._logger, level=logging.DEBUG) as watcher:
            # access cache every 1 second
            for i in range(3):
                self._logger.debug("test %d", i + 1)
                test_func()

            # check DEBUG logs for TTL behavior
            self.assertEqual(watcher.records[0].getMessage(), "test 1")
            self.assertEqual(watcher.records[1].getMessage(), "calling `test_func`")
            self.assertEqual(watcher.records[2].getMessage(), "test 2")
            self.assertEqual(watcher.records[3].getMessage(), "test 3")

class TestTTLCache(unittest.TestCase):
    """test `just.cache.ttl_cachw`."""

    def setUp(self):
        self._logger = logging.getLogger(__name__)

    def test_ttl_cache(self):
        """test `just.cache.ttl_cachw`."""

        @ttl_cache(2.5)
        def test_func() -> None:
            self._logger.debug("calling `test_func`")

        with self.assertLogs(self._logger, level=logging.DEBUG) as watcher:
            # access cache every 1 second
            for i in range(5):
                self._logger.debug("test %d", i + 1)
                test_func()
                time.sleep(1)

            # check DEBUG logs for TTL behavior
            self.assertEqual(watcher.records[0].getMessage(), "test 1")
            self.assertEqual(watcher.records[1].getMessage(), "calling `test_func`")
            self.assertEqual(watcher.records[2].getMessage(), "test 2")
            self.assertEqual(watcher.records[3].getMessage(), "test 3")
            self.assertEqual(watcher.records[4].getMessage(), "test 4")
            self.assertEqual(watcher.records[5].getMessage(), "calling `test_func`")
            self.assertEqual(watcher.records[6].getMessage(), "test 5")
