#!/usr/bin/env python3

"""Unit-tests for just.args"""


# standard imports
import unittest
import argparse
import datetime
import logging
import os
import stat
import sys
import tempfile

# tested imports
from just.args import DateTimeArg, DirectoryArg, LogLevelArg


class TestDateTimeArg(unittest.TestCase):
    """test for class just.args.DateTimeArg"""

    def setUp(self):
        """define command-line parameter DateTimeArg"""
        self.arg = DateTimeArg("%Y-%m-%d %H:%M:%S.%f")

    def test_date_format_bad(self):
        """test an incorrect format for the datetime; raises argparse.ArgumentTypeError"""
        # %e is a bad directive
        arg = DateTimeArg("%Y-%m-%d %H:%M:%S.%f %e")
        with self.assertRaises(argparse.ArgumentTypeError):
            _ = arg("2020-02-29 12:34:56.789")

    def test_date_time(self):
        """test the new date-time parameter-type"""
        arg = self.arg("2020-02-29 12:34:56.789")
        self.assertEqual(arg, datetime.datetime(2020, 2, 29, 12, 34, 56, 789000))

    def test_date_time_bad(self):
        """test an incorrect date-time for the format; raises argparse.ArgumentTypeError"""
        with self.assertRaises(argparse.ArgumentTypeError):
            _ = self.arg("BOGUS! 2020-02-29 12:34:56.789")


class TestDirectoryArg(unittest.TestCase):
    """test for class just.args.DirectoryArg"""

    def setUp(self):
        """define command-line parameter DirectoryArg"""
        self.arg = DirectoryArg("rw")

    def test_dir_path(self):
        """test dir-path parameter-type"""
        self.assertEqual(self.arg("."), ".")

    def test_dir_path_bad(self):
        """test an incorrect dir-path; raises argparse.ArgumentTypeError"""
        # create and delete temp dir, creating a path to a missing directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = temp_dir
        # now that the temp dir has been deleted, try to use it as a parameter
        with self.assertRaises(argparse.ArgumentTypeError):
            _ = self.arg(temp_dir_path)

    def test_dir_path_file(self):
        """test a dir-path ponting to a file; raises argparse.ArgumentTypeError"""
        with tempfile.NamedTemporaryFile("r") as temp_file:
            with self.assertRaises(argparse.ArgumentTypeError):
                _ = self.arg(temp_file.name)

    def test_mode(self):
        """test every valid mode-string"""
        for mode in ["", "r", "w", "rw"]:
            arg = DirectoryArg(mode)
            self.assertEqual(arg.mode, mode)

    def test_mode_norm(self):
        """test mode normalization"""
        self.assertEqual(DirectoryArg("rwwrw").mode, "rw")

    def test_mode_norm_log(self):
        """test mode normalization emits a log warning"""
        with self.assertLogs(level=logging.WARNING):
            self.assertEqual(DirectoryArg("rwwrw").mode, "rw")

    def test_mode_bad(self):
        """test an incorrect mode"""
        with self.assertRaises(ValueError):
            _ = DirectoryArg("BOGUS!")

    def test_mode_exec(self):
        """test unsupported mode "x" """
        with self.assertRaises(ValueError):
            _ = DirectoryArg("rx")

    def test_mode_none(self):
        """test unsupported mode None"""
        with self.assertRaises(TypeError):
            _ = DirectoryArg(None)

    # FIXME causes problems with permissions in the temp-dir on Windows,
    #       since os.chmod() does nothing on Windows!
    @unittest.skipIf(sys.platform == "win32", "os.chmod() does nothing on Windows")
    def test_mode_read_only(self):
        """test mode "w" non-writable directory raises argparse.ArgumentTypeError"""

        with tempfile.TemporaryDirectory() as temp_dir_path:
            temp_dir_path = os.path.join(temp_dir_path, "temp")
            os.makedirs(temp_dir_path)

            # ensure temp directory exists
            self.assertTrue(os.path.isdir(temp_dir_path))

            # get previous mode to reset later
            temp_dir_mode = os.stat(temp_dir_path).st_mode

            try:
                # make directory non-writable so it can be tested
                mask = 0o777 ^ (stat.S_IWRITE | stat.S_IWGRP | stat.S_IWOTH)
                os.chmod(temp_dir_path, temp_dir_mode & mask)

                # ensure access fails on non-writable file
                # FIXME fails on Windows because os.chmod doesn't work
                self.assertTrue(os.access(temp_dir_path, os.R_OK))
                self.assertFalse(os.access(temp_dir_path, os.W_OK))

                with self.assertRaises(argparse.ArgumentTypeError):
                    arg = DirectoryArg("w")
                    _ = arg(temp_dir_path)

            finally:
                # reset mode to writable so test can clean-up temp-dir
                os.chmod(temp_dir_path, temp_dir_mode)

    # FIXME causes problems with permissions in the temp-dir on Windows,
    #       since os.chmod() does nothing on Windows!
    @unittest.skipIf(sys.platform == "win32", "os.chmod() does nothing on Windows")
    def test_mode_write_only(self):
        """test mode "r" non-readable directory raises argparse.ArgumentTypeError"""

        with tempfile.TemporaryDirectory() as temp_dir_path:
            temp_dir_path = os.path.join(temp_dir_path, "temp")
            os.makedirs(temp_dir_path)

            # ensure temp directory exists
            self.assertTrue(os.path.isdir(temp_dir_path))

            # get previous mode to reset later
            temp_dir_mode = os.stat(temp_dir_path).st_mode

            try:
                # make directory non-readable so it can be tested
                mask = 0o777 ^ (stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
                os.chmod(temp_dir_path, temp_dir_mode & mask)

                # ensure access fails on non-writable file
                # FIXME fails on Windows because os.chmod doesn't work
                self.assertFalse(os.access(temp_dir_path, os.R_OK))
                self.assertTrue(os.access(temp_dir_path, os.W_OK))

                with self.assertRaises(argparse.ArgumentTypeError):
                    arg = DirectoryArg("r")
                    _ = arg(temp_dir_path)

            finally:
                # reset mode to writable so test can clean-up temp-dir
                os.chmod(temp_dir_path, temp_dir_mode)


class TestLogLevelArg(unittest.TestCase):
    """test for class just.args.LogLevelArg"""

    def setUp(self):
        """define command-line parameter LogLevelArg"""
        self.arg = LogLevelArg

    def test_name(self):
        """test log-level parameter-type"""
        self.assertEqual(self.arg("NOTSET"), logging.NOTSET)
        self.assertEqual(self.arg("DEBUG"), logging.DEBUG)
        self.assertEqual(self.arg("INFO"), logging.INFO)
        self.assertEqual(self.arg("WARNING"), logging.WARNING)
        self.assertEqual(self.arg("NOTSET"), logging.NOTSET)
        self.assertEqual(self.arg("CRITICAL"), logging.CRITICAL)

    def test_name_variants(self):
        """test log-level case-insensitive matching, alternate names"""
        self.assertEqual(self.arg("warn"), logging.WARNING)
        self.assertEqual(self.arg("fatal"), logging.CRITICAL)

    def test_name_bad(self):
        """test incorrect log-level; raises argparse.ArgumentTypeError"""
        with self.assertRaises(argparse.ArgumentTypeError):
            _ = self.arg("BOGUS!")
