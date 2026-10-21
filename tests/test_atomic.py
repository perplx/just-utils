"""Tests for `just.atomic`."""

import os
import tempfile
import unittest
from pathlib import Path

from just.atomic import atomic_open

class TestAtomicOpen(unittest.TestCase):
    """Tests for `just.atomic.atomic_open`."""

    FILE_NAME = "test.txt"

    def test_atomic_open(self):
        """Test `just.atomic.atomic_open` opening."""  # FIXME

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_path = temp_path / self.FILE_NAME

            with atomic_open(file_path, "wb"):
                # after opening, the file doesn't exist yet
                self.assertFalse(file_path.exists())

            # after exiting the context, the file exists
            self.assertTrue(file_path.exists())

    def test_atomic_open_write(self):
        """Test `just.atomic.atomic_open` writing."""  # FIXME

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_path = temp_path / self.FILE_NAME

            with atomic_open(file_path, "wt") as atomic_file:
                # after opening, the file doesn't exist yet
                self.assertFalse(file_path.exists())

                # after writing, the file still doesn't exist
                atomic_file.write("test\n")
                atomic_file.flush()
                self.assertFalse(file_path.exists())

            # after exiting the context, the file exists and has the expected contents
            self.assertTrue(file_path.exists())
            self.assertEqual(file_path.read_text(), "test\n")

    def test_atomic_open_closed_by_caller(self):
        """Test `just.atomic.atomic_open` writing, where the caller calls `.close()` in the `atomic_open`.
        This is to ensure the `atomic_open` doesn't call `.flush()` or `os.fsync` on a closed file.
        """  # FIXME

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_path = temp_path / self.FILE_NAME

            with atomic_open(file_path, "wt") as atomic_file:
                # after opening, the file doesn't exist yet
                self.assertFalse(file_path.exists())

                # after writing, the file still doesn't exist
                atomic_file.write("test\n")
                atomic_file.close()  # not flush()!
                self.assertFalse(file_path.exists())

            # after exiting the context, the file exists and has the expected contents
            self.assertTrue(file_path.exists())
            self.assertEqual(file_path.read_text(), "test\n")

    def test_atomic_open_exception(self):
        """Test `just.atomic.atomic_open` writing with exception."""  # FIXME

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_path = temp_path / self.FILE_NAME
            file_path.write_text("original\n")

            with self.assertRaises(RuntimeError):
                with atomic_open(file_path, "wt") as atomic_file:
                    atomic_file.write("interrupted!\n")
                    raise RuntimeError("fail mid-write")

            # the original contents are intact, and no temp-file is left behind
            self.assertEqual(file_path.read_text(), "original\n")
            self.assertEqual(os.listdir(temp_dir), [self.FILE_NAME])

    def test_atomic_open_bad_mode(self):
        """Test `just.atomic.atomic_open` writing bad mode parameter.
        Ensure the failure from the mode doesn't afect any pre-existing file that would have been overwritten.
        """  # FIXME

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            file_path = temp_path / self.FILE_NAME
            file_path.write_text("original\n")

            for mode in ["a", "r", "x", "ab", "r+"]:
                with self.assertRaises(ValueError, msg=f"mode {mode!r}"):
                    with atomic_open(file_path, mode):
                        pass

            # the original contents are intact, and no temp-file is left behind
            self.assertEqual(file_path.read_text(), "original\n")
            self.assertEqual(os.listdir(temp_dir), [self.FILE_NAME])
