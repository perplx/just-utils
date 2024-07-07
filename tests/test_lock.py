"""Unit-tests for just-lock"""

# standard imports
import os
import tempfile
import unittest

# local imports
import just.lock


# global constants
LOCK_FILE_PATH = "bogusbogusbogusbogus"


class TestLock(unittest.TestCase):
    """test for just.utils.lock_file"""

    def setUp(self):
        """Create the temp-dir where the tested lock-file exists."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.lock_file = os.path.join(self.temp_dir.name, "LOCK_FILE")

    def tearDown(self):
        """Cleanup the temp-dir where the tested lock-file exists."""
        self.temp_dir.cleanup()

    def test_lock_exists(self):
        """Test the lock-file only exists in the locked context."""
        self.assertFalse(os.path.isfile(self.lock_file))
        with just.lock.lock_file(self.lock_file):
            self.assertTrue(os.path.isfile(self.lock_file))
        self.assertFalse(os.path.isfile(self.lock_file))

    def test_lock_error(self):
        """Test that locking the same file twice causes a FileExistsError."""
        with self.assertRaises(FileExistsError):
            with just.lock.lock_file(self.lock_file):
                with just.lock.lock_file(self.lock_file):
                    pass

    def test_lock_exception(self):
        """Test that raising an Exception when the file lock is locked will unlock the file."""
        with self.assertRaises(RuntimeError):
            with just.lock.lock_file(self.lock_file):
                raise RuntimeError(f"Exception when file {self.lock_file} locked!")

        self.assertFalse(os.path.isfile(self.lock_file), f"lock-file {self.lock_file} still exists")
