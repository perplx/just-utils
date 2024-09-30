#!/usr/bin/env python3

"""Unit-tests for just.timing"""


# standard imports
import unittest
from pathlib import Path

# tested imports
import just.open


class TestOpen(unittest.TestCase):
    """Tests for just.open.my_open"""

    DATA_PATH = Path(__file__).absolute().parent / "data"
    TEST_TEXT = "test\n"

    def test_open_bzip2(self):
        test_file_path = self.DATA_PATH / "test_data.txt.bz2"
        with just.open.ezopen(test_file_path, mode="rt") as test_file:
            self.assertEqual(test_file.read(), self.TEST_TEXT)

    def test_open_gzip(self):
        test_file_path = self.DATA_PATH / "test_data.txt.gz"
        with just.open.ezopen(test_file_path, mode="rt") as test_file:
            self.assertEqual(test_file.read(), self.TEST_TEXT)

    def test_open_text(self):
        test_file_path = self.DATA_PATH / "test_data.txt"
        with just.open.ezopen(test_file_path, mode="rt") as test_file:
            self.assertEqual(test_file.read(), self.TEST_TEXT)
