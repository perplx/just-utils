#!/usr/bin/env python3

"""Unit-tests for just.timing"""


# standard imports
import unittest
import io
import logging
import sys

# tested imports
from just.timing import timed, timing


class TestTimed(unittest.TestCase):
    """Tests for just.timing.timed decorator"""

    def setUp(self):
        self.OUTPUT_REGEX = r"func .*? args .*? kwargs .*? took .*? seconds"
        self.test_logger = logging.getLogger()

    # FIXME `timed` vs `timed()` should work either way
    def test_missing_call(self):
        """test that using `timed` instead of `timed()` raises TypeError"""

        @timed
        def test():
            pass

        with self.assertRaises(TypeError):
            test()

    def test_print(self):
        """test the stdout output contains the expected format"""

        # timed function outputs to stdout
        @timed(do_print=True, logger=None)
        def test():
            pass

        # capture the stdout of the decorated function
        capture = io.StringIO()
        sys.stdout = capture
        test()
        sys.stdout = sys.__stdout__

        # check captured value matches expected pattern
        self.assertRegex(capture.getvalue(), self.OUTPUT_REGEX)

    def test_logger_regex(self):
        """test the logger output contains the expected format"""

        @timed(do_print=False, logger=self.test_logger)
        def test():
            pass

        # ensure calling timed function produces logs with the expected format
        with self.assertLogs(self.test_logger, level=logging.INFO) as watcher:
            test()
            self.assertRegex(str(watcher.output), self.OUTPUT_REGEX)

    def test_logger_bad_type(self):
        """test the decorator raises a TypeError if the logger parameter isn't a logging.Logger object"""
        with self.assertRaises(TypeError):
            # declare timed function with bad type for logger
            @timed(logger="BOGUS")
            def test():
                pass

    def test_logger_bad_level(self):
        """test the decorator raises a ValueError if the log level isn't valid"""
        with self.assertRaises(ValueError):
            # declare timed function with bad value for log level
            @timed(logger=self.test_logger, level="BOGUS!")
            def test():
                pass


class TestTiming(unittest.TestCase):
    """Tests for just.timing.timing context-manager"""

    def setUp(self):
        self.OUTPUT_REGEX = r" took .*? seconds"
        self.test_logger = logging.getLogger()

    def test_print_output(self):
        """test the stdout output contains the expected format"""

        # capture the stdout of the function in the context-manager
        capture = io.StringIO()
        sys.stdout = capture
        MESSAGE = "print test"
        with timing(MESSAGE, do_print=True, logger=None):
            pass
        sys.stdout = sys.__stdout__

        # check captured value matches expected pattern
        self.assertRegex(capture.getvalue(), self.OUTPUT_REGEX)

    def test_logger_output(self):
        """test the logger output contains the expected format"""
        with self.assertLogs(self.test_logger, level=logging.INFO) as watcher:
            MESSAGE = "regex_test"
            with timing(MESSAGE, do_print=False, logger=self.test_logger):
                pass
            self.assertRegex(str(watcher.output), MESSAGE + self.OUTPUT_REGEX)

    def test_logger_bad_type(self):
        """test the context manager raises a TypeError if the logger parameter isn't a logging.Logger object"""
        with self.assertRaises(TypeError):
            with timing("bad_type", logger="BOGUS"):
                pass

    def test_logger_bad_level(self):
        """test the decorator raises a ValueError if the log level isn't valid"""
        with self.assertRaises(ValueError):
            with timing("bad_level", logger=self.test_logger, level="BOGUS"):
                pass
