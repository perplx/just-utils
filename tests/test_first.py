#!/usr/bin/env python3

"""Unit-tests for just.first"""


# standard imports
import itertools
import unittest

# tested imports
from just.first import first, last, only


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


class TestOnly(unittest.TestCase):
    """test for `just.first.only`"""

    def test_only(self):
        """test `just.first.only` with no condition."""

        self.assertEqual(only([], default=None), None)
        self.assertEqual(only([0, 0, 0], default=None), None)
        self.assertEqual(only([0, 1, 0]), 1)
        self.assertEqual(only([5]), 5)

    def test_only_condition(self):
        """test `just.first.only` with condition."""

        self.assertEqual(only([1, 3, 8, 9], lambda x: x > 8), 9)
        self.assertEqual(only([None, 0, None], lambda x: x is not None), 0)

    def test_only_missing(self):
        """test `just.first.only` with no matching item."""

        with self.assertRaises(ValueError):
            only([])
        with self.assertRaises(ValueError):
            only([0, 0, 0])

    def test_only_several(self):
        """test `just.first.only` with more than one matching item."""

        with self.assertRaises(ValueError):
            only([1, 2])
        with self.assertRaises(ValueError):
            only([1, 3, 8, 5], lambda x: x % 3 == 2)

    def test_only_several_default(self):
        """test `just.first.only` raises on several items even given a `default`.

        A `default` answers "nothing matched", not "the input was ambiguous".
        """

        with self.assertRaises(ValueError):
            only([1, 2], default=None)

    def test_only_lazy(self):
        """test `just.first.only` stops at the second match."""

        counter = itertools.count()
        with self.assertRaises(ValueError):
            only(counter)
        # `only` gave up after the second match, it did not drain the iterator
        self.assertEqual(next(counter), 3)
