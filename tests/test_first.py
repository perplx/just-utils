#!/usr/bin/env python3

"""Unit-tests for just.first"""


# standard imports
import unittest

# tested imports
from just.first import first, last


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


class TestLast(unittest.TestCase):
    """test for `just.first.last`"""

    def test_last(self):
        """test `just.first.last` with no condition."""

        self.assertEqual(last([], default=None), None)
        self.assertEqual(last([0, 0, 0], default=None), None)
        self.assertEqual(last([0, 1, 0], default=None), 1)
        self.assertEqual(last([1, 2, 3]), 3)
        self.assertEqual(last([0, 0, 0, 1, 0, 2]), 2)

    def test_last_condition(self):
        """test `just.first.last` with condition."""

        self.assertEqual(last([0, 1, 2, 3], lambda x: x), 3)
        self.assertEqual(last([0, 1, 2, 3], lambda x: x % 3 == 2), 2)
        self.assertEqual(last([1, None, 0, None], lambda x: x is not None), 0)

    def test_last_missing(self):
        """test `just.first.last` with no matching item."""

        with self.assertRaises(ValueError):
            last([])
        with self.assertRaises(ValueError):
            last([0, 0, 0])
        with self.assertRaises(ValueError):
            last([1, 3, 8, 9], lambda x: x > 10000)

    def test_last_iterator(self):
        """test `just.first.last` consumes an iterator, without storing it."""

        self.assertEqual(last(iter([1, 2, 3])), 3)
        self.assertEqual(last(i for i in range(10) if i % 3 == 2), 8)
