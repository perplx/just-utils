"""FIXME"""


import unittest
from typing import Callable


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
    def setUp(self):
        self._flaky_func = flaky(3)

    def test_retry_success(self):
        raise NotImplementedError

    def test_retry_failure(self):
        raise NotImplementedError

    def test_retry_invalid(self):
        raise NotImplementedError


