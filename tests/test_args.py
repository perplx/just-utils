#!/usr/bin/env python3


"""Unit-tests for just.args"""


# standard imports
import unittest
import argparse
import datetime
import logging
import sys

# tested imports
from just.args import DateTimeArg, DirectoryArg, LogLevelArg


class TestDateTimeArg(unittest.TestCase):
    """test for class just.args.DateTimeArg"""

    def setUp(self):
        """define command-line parameter --date-time to test DateTimeArg"""
        self.arg_parser = argparse.ArgumentParser()
        self.arg_parser.add_argument("--date-time", type=DateTimeArg("%Y-%m-%d %H:%M:%S.%f"))

    def test_date_format_bad(self):
        self.arg_parser.add_argument("--bad-format", type=DateTimeArg("%Y-%m-%d %H:%M:%S.%f %e")) # %e is a bad directive
        with self.assertRaises(SystemExit):
            _ = self.arg_parser.parse_args(["--bad-format", "2020-02-29 12:34:56.789"])

    def test_date_time(self):
        """test the new date-time parameter-type"""
        args = self.arg_parser.parse_args(["--date-time", "2020-02-29 12:34:56.789"])
        self.assertEqual(args.date_time, datetime.datetime(2020, 2, 29, 12, 34, 56, 789000))

    def test_date_time_bad(self):
        """test an incorrect date-time for the format; causes ArgumentParser to exit()"""
        with self.assertRaises(SystemExit):
            _ = self.arg_parser.parse_args(["--date-time", "BOGUS! 2020-02-29 12:34:56.789"])


class TestDirectoryArg(unittest.TestCase):
    """test for class just.args.DirectoryArg"""

    def setUp(self):
        """define command-line parameter --directory to test DirectoryArg"""
        self.arg_parser = argparse.ArgumentParser()
        self.arg_parser.add_argument("--directory", type=DirectoryArg("rw"))

    def test_dir_path(self):
        """test dir-path parameter-type"""
        args = self.arg_parser.parse_args(["--directory", "."])
        self.assertEqual(args.directory, ".")

    def test_dir_path_bad(self):
        """test an incorrect dir-path; causes ArgumentParser to exit()"""
        with self.assertRaises(SystemExit):
            _ = self.arg_parser.parse_args(["--directory", "BOGUS!"])

    def test_mode(self):
        """test every valid mode-string"""
        for mode in ["", "r", "w", "rw"]:
            arg = DirectoryArg(mode)
            self.assertEqual(arg.mode, mode)

    def test_mode_norm(self):
        """test mode normalization"""
        self.assertEquals(DirectoryArg("rwwrw").mode, "rw")

    def test_mode_norm_log(self):
        """test mode normalization emits a log warning"""
        with self.assertLogs(level=logging.WARNING):
            self.assertEquals(DirectoryArg("rwwrw").mode, "rw")

    # FIXME causes problems with permissions in the temp-dir on Windows,
    #       since os.chmod() does nothing on Windows!
    @unittest.skipIf(sys.platform == "win32", "os.chmod() does nothing on Windows")
    def test_mode_access(self):
        """test argument with unavailable mode"""
        import os
        import stat
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir_path:
            # create subdirectory
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

                with self.assertRaises(SystemExit):
                    _ = self.arg_parser.parse_args(["--directory", temp_dir_path])

            finally:
                # reset mode to writable so test can clean-up temp-dir
                os.chmod(temp_dir_path, temp_dir_mode)

    def test_mode_bad(self):
        """test an incorrect mode"""
        with self.assertRaises(argparse.ArgumentTypeError):
            self.arg_parser.add_argument("--directory", type=DirectoryArg("BOGUS!"))

    def test_mode_exec(self):
        """test unsupported mode "x" """
        with self.assertRaises(argparse.ArgumentTypeError):
            self.arg_parser.add_argument("--directory", type=DirectoryArg("rx"))

    def test_mode_none(self):
        """test unsupported mode None"""
        with self.assertRaises(argparse.ArgumentTypeError):
            self.arg_parser.add_argument("--directory", type=DirectoryArg(None))


class TestLogLevelArg(unittest.TestCase):
    """test for class just.args.LogLevelArg"""

    def setUp(self):
        """define command-line parameter --log-level to test LogLevelArg"""
        self.arg_parser = argparse.ArgumentParser()
        self.arg_parser.add_argument("--log-level", type=LogLevelArg)

    def test_name(self):
        """test log-level parameter-type"""
        args = self.arg_parser.parse_args(["--log-level", "NOTSET"])
        self.assertEqual(args.log_level, logging.NOTSET)
        args = self.arg_parser.parse_args(["--log-level", "DEBUG"])
        self.assertEqual(args.log_level, logging.DEBUG)
        args = self.arg_parser.parse_args(["--log-level", "INFO"])
        self.assertEqual(args.log_level, logging.INFO)
        args = self.arg_parser.parse_args(["--log-level", "WARNING"])
        self.assertEqual(args.log_level, logging.WARNING)
        args = self.arg_parser.parse_args(["--log-level", "ERROR"])
        self.assertEqual(args.log_level, logging.ERROR)
        args = self.arg_parser.parse_args(["--log-level", "CRITICAL"])
        self.assertEqual(args.log_level, logging.CRITICAL)

    def test_name_variants(self):
        """test log-level case-insensitive matching, alternate names"""
        args = self.arg_parser.parse_args(["--log-level", "warn"])
        self.assertEqual(args.log_level, logging.WARNING)
        args = self.arg_parser.parse_args(["--log-level", "fatal"])
        self.assertEqual(args.log_level, logging.CRITICAL)

    def test_name_bad(self):
        """test incorrect log-level; causes ArgumentParser to exit()"""
        with self.assertRaises(SystemExit):
            _ = self.arg_parser.parse_args(["--log-level", "BOGUS!"])
