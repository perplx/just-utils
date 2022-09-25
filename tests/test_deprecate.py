#!/usr/bin/env python3

"""Unit-tests for just.deprecate"""


# standard imports
import unittest
import logging

# tested imports
from just.deprecate import deprecated


class TestDeprecate(unittest.TestCase):
    """test for `just.deprecate.deprecated`"""

    def test_deprecated_function(self):
        """test that a deprecated function emits a warning when called"""

        # define deprecated function
        @deprecated
        def deprecated_func():
            return None

        # test deprecated function
        with self.assertWarns(DeprecationWarning):
            deprecated_func()

    def test_deprecated_method(self):
        """test that a deprecated method emits a warning when called"""

        # define class with deprecated method
        class DeprecatedClass:
            @deprecated
            def deprecated_method(self):
                return None

        # test deprecated method
        instance = DeprecatedClass()
        with self.assertWarns(DeprecationWarning):
            instance.deprecated_method()

    def test_deprecated_logging(self):
        """test that a deprecated call produces a log message when warnings are captured by logging"""

        # define deprecated function
        @deprecated
        def deprecated_func():
            return None

        # logging to receive warnings
        logging.captureWarnings(True)

        # expected line prefix when using default format
        LOG_PREFIX = "WARNING:py.warnings:"

        with self.assertLogs("py.warnings", level=logging.WARNING) as cm:
            # call the deprecated function
            deprecated_func()

            # ensure log output contains 1 line
            self.assertEqual(len(cm.output), 1)
            output_line = cm.output[0]

            # ensure log output contains LOG_PREFIX
            self.assertIn(LOG_PREFIX, output_line)

            # ensure log output starts with LOG_PREFIX
            self.assertTrue(output_line.startswith(LOG_PREFIX))
