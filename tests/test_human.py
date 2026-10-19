"""FIXME"""

# standard imports
import unittest

# tested imports
from just.human import format_bytes, format_duration, parse_bytes, parse_duration


class TestByteSize(unittest.TestCase):
    def test_format_bytes(self):
        self.assertEqual(format_bytes(0), "0B")
        self.assertEqual(format_bytes(1), "1B")
        self.assertEqual(format_bytes(10), "10B")
        self.assertEqual(format_bytes(100), "100B")
        self.assertEqual(format_bytes(1000), "1000B")
        self.assertEqual(format_bytes(1023), "1023B")
        self.assertEqual(format_bytes(1024), "1.0K")
        self.assertEqual(format_bytes(1024 * 10), "10.0K")
        self.assertEqual(format_bytes(1024 * 100), "100K")
        self.assertEqual(format_bytes(1024 * 1000), "1000K")
        self.assertEqual(format_bytes((1024 * 1024) - 1), "1024K")  # FIXME
        self.assertEqual(format_bytes(1024 * 1024), "1.0M")

    def test_bormat_bytes_invalid_num_bytes(self):
        with self.assertRaises(ValueError):
            _ = format_bytes(-1)

    def test_parse_bytes(self):
        self.assertEqual(parse_bytes("1000B"), 1000)
        self.assertEqual(parse_bytes("1023B"), 1023)
        self.assertEqual(parse_bytes("1.0K"), 1024)

    def test_parse_bytes_invalid_str(self):
        with self.assertRaises(ValueError):
            _ = parse_bytes("BOGUS")


class TestDuration(unittest.TestCase):
    def test_format_duration(self):
        self.assertEqual(format_duration(0), "")
        self.assertEqual(format_duration(1), "1s")
        self.assertEqual(format_duration(60), "1m")
        self.assertEqual(format_duration(60 * 60), "1h")
        self.assertEqual(format_duration(60 * 60 * 24), "1d")

    def test_parse_duration(self):
        self.assertEqual(parse_duration(""), 0)
        self.assertEqual(parse_duration("1s"), 1)
        self.assertEqual(parse_duration("1m"), 60)
        self.assertEqual(parse_duration("1h"), 60 * 60)
        self.assertEqual(parse_duration("1d"), 60 * 60 * 24)
