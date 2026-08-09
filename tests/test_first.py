#!/usr/bin/env python3

"""Unit-tests for just.first"""


# standard imports
import unittest

# tested imports
from just.first import first


class TestFirst(unittest.TestCase):
    """test for `just.first`"""

    def test_first(self):
        """test `just.first.first` with no condition."""

        self.assertEqual(first([], default=None), None)
        self.assertEqual(first([0, 0, 0], default=None), None)
        self.assertEqual(first([0, 1, 0], default=None), 1)

    def test_first_condition(self):
        """test `just.first.first` with condition."""

        self.assertEqual(first([0, 1, 2, 3], lambda x: x), 1)
        self.assertEqual(first([0, 1, 2, 3], lambda x: x % 3 == 2), 2)
        self.assertEqual(first([None, 0, 1], lambda x: x is not None), 0)

    def test_first_missing(self):
        """test `just.first.first` with no matching item."""

        with self.assertRaises(ValueError):
            self.assertEqual(first([]), None)
        with self.assertRaises(ValueError):
            self.assertEqual(first([0, 0, 0]), None)

