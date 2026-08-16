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


class TestDuration:
    pass
