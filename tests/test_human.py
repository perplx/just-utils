"""FIXME"""

# standard imports
import unittest

# tested imports
from just.human import _find_blocks, format_bytes, format_duration, parse_bytes, parse_duration


class TestByteSize(unittest.TestCase):

    def test_find_blocks(self):
        self.assertEqual(_find_blocks(0, 1024), (0, 0))
        self.assertEqual(_find_blocks(1, 1024), (1, 0))
        self.assertEqual(_find_blocks(10, 1024), (10, 0))
        self.assertEqual(_find_blocks(100, 1024), (100, 0))
        self.assertEqual(_find_blocks(1000, 1024), (1000, 0))
        self.assertEqual(_find_blocks(1023, 1024), (1023, 0))
        self.assertEqual(_find_blocks(1024, 1024), (1, 1))
        self.assertEqual(_find_blocks(1024 * 10, 1024), (10, 1))
        self.assertEqual(_find_blocks(1024 * 100, 1024), (100, 1))
        self.assertEqual(_find_blocks(1024 * 1000, 1024), (1000, 1))
        self.assertEqual(_find_blocks((1024 * 1024) - 1, 1024), (1023.9990234375, 1))
        self.assertEqual(_find_blocks(1024 * 1024, 1024), (1, 2))

    def test_find_blocks_invalid_num_bytes(self):
        with self.assertRaises(ValueError):
            _ = _find_blocks(-1, 1024)

    def test_find_blocks_invalid_block_size(self):
        with self.assertRaises(ValueError):
            _ = _find_blocks(1, -1)
        with self.assertRaises(ValueError):
            _ = _find_blocks(1, 0)
        with self.assertRaises(ValueError):
            _ = _find_blocks(1, 1)

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

    def test_format_bytes_invalid_num_bytes(self):
        with self.assertRaises(ValueError):
            _ = format_bytes(-1)

    def test_parse_bytes(self):
        self.assertEqual(parse_bytes("1000B"), 1000)
        self.assertEqual(parse_bytes("1023B"), 1023)
        self.assertEqual(parse_bytes("1.0K"), 1024)
        self.assertEqual(parse_bytes("3.2G"), 3435973836)

    def test_parse_bytes_units(self):
        self.assertEqual(parse_bytes("1B"), 1)
        self.assertEqual(parse_bytes("1K"), 1024)
        self.assertEqual(parse_bytes("1M"), 1024**2)
        self.assertEqual(parse_bytes("1G"), 1024**3)
        self.assertEqual(parse_bytes("1T"), 1024**4)
        self.assertEqual(parse_bytes("1P"), 1024**5)
        self.assertEqual(parse_bytes("1E"), 1024**6)
        self.assertEqual(parse_bytes("1Z"), 1024**7)
        self.assertEqual(parse_bytes("1Y"), 1024**8)

    def test_parse_bytes_returns_int(self):
        self.assertIsInstance(parse_bytes("1B"), int)
        self.assertIsInstance(parse_bytes("3.2G"), int)

    def test_parse_bytes_invalid_str(self):
        with self.assertRaises(ValueError):
            _ = parse_bytes("BOGUS")

    def test_parse_bytes_empty_str(self):
        with self.assertRaises(IndexError):  # FIXME should be ValueError
            _ = parse_bytes("")


class TestDuration(unittest.TestCase):
    def test_format_duration(self):
        self.assertEqual(format_duration(0), "")
        self.assertEqual(format_duration(1), "1s")
        self.assertEqual(format_duration(60), "1m")
        self.assertEqual(format_duration(60 * 60), "1h")
        self.assertEqual(format_duration(60 * 60 * 24), "1d")

    def test_format_duration_combined(self):
        self.assertEqual(format_duration(1000), "16m 40s")
        self.assertEqual(format_duration(3661), "1h 1m 1s")
        self.assertEqual(format_duration(90061), "1d 1h 1m 1s")
        self.assertEqual(format_duration(1_000_000), "11d 13h 46m 40s")

    def test_parse_duration(self):
        self.assertEqual(parse_duration(""), 0)
        self.assertEqual(parse_duration("1s"), 1)
        self.assertEqual(parse_duration("1m"), 60)
        self.assertEqual(parse_duration("1h"), 60 * 60)
        self.assertEqual(parse_duration("1d"), 60 * 60 * 24)

    def test_parse_duration_combined(self):
        self.assertEqual(parse_duration("16m 40s"), 1000)
        self.assertEqual(parse_duration("1h 1m 1s"), 3661)
        self.assertEqual(parse_duration("1d 12h 5m 5s"), 129905)
        self.assertEqual(parse_duration("5s 1m"), 65)

    def test_duration_round_trip(self):
        for num_seconds in (1, 60, 1000, 3661, 90061, 1_000_000):
            self.assertEqual(parse_duration(format_duration(num_seconds)), num_seconds)
