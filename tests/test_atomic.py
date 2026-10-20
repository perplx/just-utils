"""Tests for `just.atomic`."""

import tempfile
import unittest
from pathlib import Path

from just.atomic import atomic_open

class TestAtomicOpen(unittest.TestCase):
    """Tests for `just.atomic.atomic_open`."""

    def test_atomic_open(self):
        file_name = "test.txt"
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_path = temp_path / file_name

            with atomic_open(file_path, "wb"):
                # after opening, the file doesn't exist yet
                self.assertFalse(file_path.exists())

            # after exting the context, the file exists
            self.assertTrue(file_path.exists())

    def test_atomic_open_write(self):
        file_name = "test.txt"
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_path = temp_path / file_name

            with atomic_open(file_path, "wt") as atomic_file:
                # after opening, the file doesn't exist yet
                self.assertFalse(file_path.exists())

                # after writing, the file still doesn't exist
                atomic_file.write("test\n")
                atomic_file.flush()
                self.assertFalse(file_path.exists())

            # after exting the context, the file exists and has the expected contents
            self.assertTrue(file_path.exists())
            self.assertEqual(file_path.read_text(), "test\n")

    def test_atomic_open_exception(self):
        raise NotImplementedError
