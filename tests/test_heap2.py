import unittest

from just.heap2 import Heap


class TestHeap2(unittest.TestCase):
    """Tests for class just.heap.Heap"""

    def setUp(self):
        # TEST_DATA is mutable!
        TEST_DATA = ["c", "bb", "aaa"]
        self.heap_test = Heap(TEST_DATA)

    def test_peek(self):
        self.assertEqual(self.heap_test.peek(), "aaa")

    def test_pop(self):
        self.assertEqual(self.heap_test.pop(), "aaa")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()
