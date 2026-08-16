"""FIXME"""

# standard imports
import unittest

# tested imports
import just.human


class TestByteSize(unittest.TestCase):
    def test_format_bytes(self):
        self.assertEqual(just.human.format_bytes(1000), "1000B")
        self.assertEqual(just.human.format_bytes(1023), "1023B")
        self.assertEqual(just.human.format_bytes(1024), "1.0K")

    def test_parse_bytes(self):
        self.assertEqual(just.human.parse_bytes("1000B"), 1000)
        self.assertEqual(just.human.parse_bytes("1023B"), 1023)
        self.assertEqual(just.human.parse_bytes("1.0K"), 1024)


class TestDuration(unittest.TestCase):
    def test_format_duration(self):
        self.assertEqual(just.human.format_duration(0), "")
        self.assertEqual(just.human.format_duration(1), "1s")
        self.assertEqual(just.human.format_duration(60), "1m")
        self.assertEqual(just.human.format_duration(60 * 60), "1h")
        self.assertEqual(just.human.format_duration(60 * 60 * 24), "1d")

    def test_parse_duration(self):
        self.assertEqual(just.human.parse_duration(""), 0)
        self.assertEqual(just.human.parse_duration("1s"), 1)
        self.assertEqual(just.human.parse_duration("1m"), 60)
        self.assertEqual(just.human.parse_duration("1h"), 60 * 60)
        self.assertEqual(just.human.parse_duration("1d"), 60 * 60 * 24)
