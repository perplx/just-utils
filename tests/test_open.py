#!/usr/bin/env python3

"""Unit-tests for just.timing"""


# standard imports
import unittest

# tested imports
import just.open


class TestOpen(unittest.TestCase):
    """Tests for just.open.my_open"""

    TEST_TEXT = "test\n"

    def test_open_bzip2(self):
        gz_file_path = "./data/test_data.txt.bz2"
        with just.open.ezopen(gz_file_path, mode="rt") as test_file:
            self.assertEqual(test_file.read(), self.TEST_TEXT)

    def test_open_gzip(self):
        gz_file_path = "./data/test_data.txt.gz"
        with just.open.ezopen(gz_file_path, mode="rt") as test_file:
            self.assertEqual(test_file.read(), self.TEST_TEXT)

    def test_open_text(self):
        gz_file_path = "./data/test_data.txt"
        with just.open.ezopen(gz_file_path, mode="rt") as test_file:
            self.assertEqual(test_file.read(), self.TEST_TEXT)
