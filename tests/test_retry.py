#!/usr/bin/env python3

"""Unit-tests for just.retry"""


# standard imports
import logging
import unittest
from typing import Callable
from unittest import mock

# tested imports
from just.retry import retry


# name of the logger used by `just.retry`, where the retry-messages are logged
LOGGER_NAME = "just.retry"

# number of times `self._flaky_func` fails before it succeeds
FAILURES = 3


def flaky(failures: int) -> Callable[[], str]:
    """Return a function that will fail for `failures` times, then return OK."""

    def call() -> str:
        nonlocal failures
        if failures > 0:
            failures -= 1
            raise RuntimeError(f"{failures} failures left")
        return "ok"

    return call


class TestRetry(unittest.TestCase):
    """test for `just.retry.retry`"""

    def setUp(self):
        self._flaky_func = flaky(FAILURES)

    def test_retry_success(self):
        """test that enough tries let the flaky function succeed, and that every retry is logged"""

        # one try for each failure, plus the try that finally succeeds
        decorated = retry(RuntimeError, tries=FAILURES + 1)(self._flaky_func)

        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            self.assertEqual(decorated(), "ok")

        # every failed try is logged as a retry, the successful try is not logged
        self.assertEqual(
            cm.output,
            [
                f"WARNING:{LOGGER_NAME}:caught 2 failures left - retrying 1 / 4 ...",
                f"WARNING:{LOGGER_NAME}:caught 1 failures left - retrying 2 / 4 ...",
                f"WARNING:{LOGGER_NAME}:caught 0 failures left - retrying 3 / 4 ...",
            ],
        )

    def test_retry_failure(self):
        """test that too few tries let the last exception reach the caller, and that giving up is logged"""

        # one try short of the number of failures, so the flaky function never gets to succeed
        decorated = retry(RuntimeError, tries=FAILURES)(self._flaky_func)

        with self.assertLogs(LOGGER_NAME, level=logging.WARNING) as cm:
            with self.assertRaises(RuntimeError) as caught:
                decorated()

        # the exception of the last try is the one that propagates
        self.assertEqual(str(caught.exception), "0 failures left")

        # the last failure is logged as an abort instead of a retry, at a higher level
        self.assertEqual(
            cm.output,
            [
                f"WARNING:{LOGGER_NAME}:caught 2 failures left - retrying 1 / 3 ...",
                f"WARNING:{LOGGER_NAME}:caught 1 failures left - retrying 2 / 3 ...",
                f"ERROR:{LOGGER_NAME}:caught 0 failures left - aborting 3 / 3 ...",
            ],
        )

    def test_retry_invalid(self):
        """test that a number of tries that allows no try at all is rejected when the function is called"""

        for tries in (0, -1):
            with self.subTest(tries=tries):
                # a mock, so that the test can check the decorated function was never called
                func = mock.Mock(return_value="ok")
                decorated = retry(RuntimeError, tries=tries)(func)

                # nothing was tried, so there is no failure to log
                with self.assertNoLogs(LOGGER_NAME, level=logging.DEBUG):
                    with self.assertRaises(ValueError) as caught:
                        decorated()

                self.assertEqual(str(caught.exception), f"tries must be at least 1, got {tries}")
                func.assert_not_called()
