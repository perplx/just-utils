#!/usr/bin/env python3

"""Unit-tests for just.first"""


# standard imports
import unittest
import logging

# tested imports
from just.first import first_condition, first_next


class TestFirst(unittest.TestCase):
    """test for `just.first`"""

    def test_first_next(self):
        """test `just.first.first_next`"""

        self.assertEqual(first_next([]), None)
        self.assertEqual(first_next([0, 0, 0]), None)
        self.assertEqual(first_next([0, 1, 0]), 1)

    def test_first_condition(self):
        """test `just.first.first_condition`"""

        self.assertEqual(first_condition([0, 1, 2, 3], lambda x: x), 1)
        self.assertEqual(first_condition([0, 1, 2, 3], lambda x: x % 3 == 2), 2)
        self.assertEqual(first_condition([None, 0, 1], lambda x: x is not None), 0)
