#!/usr/bin/env python3


"""Unit-tests for just.heap"""


# standard imports
import unittest

# tested imports
from just.heap import Heap


class TestHeap(unittest.TestCase):
    """Tests for class just.heap.Heap"""

    def setUp(self):
        self.heap_empty = Heap()

        # TEST_DATA is mutable!
        TEST_DATA = ["c", "bb", "aaa"]
        self.heap_test = Heap(TEST_DATA)

        # mutable!
        key_data = [(key_func(d), d) for d in TEST_DATA]
        key_func = len
        print("key_data:", key_data)
        self.heap_key = Heap(key_data, key=key_func)

    def test_heap(self):
        """test without key"""

        h = Heap(["ccc", "bb", "a"])
        h.push("bbb")
        h.push("bbbbbb")
        self.assertEqual(len(h), 5)

        self.assertEqual(h.pop(), "a")
        self.assertEqual(h.pop(), "bb")
        self.assertEqual(h.pop(), "bbb")
        self.assertEqual(h.pop(), "bbbbbb")
        self.assertEqual(h.pop(), "ccc")
        self.assertEqual(len(h), 0)

    def test_heap_key(self):
        """test with key"""

        HEAP_ITEMS = ["", "sml", "long", "longer"]

        h = Heap([(len(item), item) for item in HEAP_ITEMS], key=len)
        h.push("even longer")
        h.push("medium")
        self.assertEqual(len(h), 6)

        self.assertEqual(h.pop(), "")
        self.assertEqual(h.pop(), "sml")
        self.assertEqual(h.pop(), "long")
        self.assertEqual(h.pop(), "longer")
        self.assertEqual(h.pop(), "medium")  # should come after "longer"
        self.assertEqual(h.pop(), "even longer")
        self.assertEqual(len(h), 0)

        # test popping an empty Heap
        with self.assertRaises(IndexError):
            h.pop()

    def test_data(self):
        """test Heap(data).heap is data"""
        HEAP_DATA = ["ccc", "bb", "a"]
        h = Heap(HEAP_DATA)
        self.assertIs(h.heap, HEAP_DATA)

    def test_data_empty(self):
        """test Heap().heap is []"""
        for h in [Heap(), Heap(None), Heap([]), Heap({}), Heap(dict())]:
            self.assertIsNotNone(h.heap)
            self.assertEqual(len(h.heap), 0)
            self.assertIsInstance(h.heap, list)
            self.assertListEqual(h.heap, [])

    # FIXME should it raise TypeError anyway when empty?
    def test_data_bad(self):
        """test Heap(x) where x is non empty non list raises TypeError"""
        with self.assertRaises(TypeError):
            _ = Heap(("a", "b"))
        with self.assertRaises(TypeError):
            _ = Heap({"b"})
        with self.assertRaises(TypeError):
            _ = Heap({"a": 2, "b": 5})

    def test_len_empty(self):
        """test len()"""
        self.assertEqual(len(self.heap_empty), 0)
        self.assertEqual(len(self.heap_empty), len(self.heap_empty.heap))

    def test_len_data(self):
        """test len()"""
        self.assertEqual(len(self.heap_test), len(self.heap_test.heap))
        self.assertEqual(len(self.heap_key), len(self.heap_key.heap))

    def test_peek(self):
        """test Heap.peek() returns top item with no key"""
        self.assertEqual(self.heap_test.peek(), "aaa")

    def test_peek_key(self):
        """test Heap.peek() returns top item with key"""
        self.assertEqual(self.heap_key.peek(), "c")

    def test_peek_empty(self):
        """test Heap.peek() on empty Heap raises IndexError"""
        with self.assertRaises(IndexError):
            _ = self.heap_empty.peek()

    def test_pop(self):
        """test pop"""
        self.assertEqual(self.heap_test.pop(), "aaa")

    def test_pop_key(self):
        """test pop with key"""
        self.assertEqual(self.heap_key.pop(), "c")

    def test_pop_empty(self):
        """test Heap.pop() on empty Heap raises IndexError"""
        with self.assertRaises(IndexError):
            _ = self.heap_empty.pop()

    def test_push(self):
        """test Heap.push(item)"""
        self.heap_test.push("a")
        self.assertEqual(self.heap_test.heap[0], "a")

    def test_push_key(self):
        """test Heap.push(item) with key"""
        self.heap_key.push("a")
        self.assertEqual(self.heap_key.heap[0], (1, "a"))

    def test_pushpop(self):
        """test Heap.pushpop(item)"""
        self.assertEqual(self.heap_test.pushpop("a"), "a")

    def test_pushpop_key(self):
        """test Heap.pushpop(item) with key"""
        self.assertEqual(self.heap_key.pushpop(""), "")

    def test_replace(self):
        """test Heap.replace(item)"""
        self.assertEqual(self.heap_test.replace(""), "aaa")

    def test_replace_key(self):
        """test Heap.replace(item) with key"""
        self.assertEqual(self.heap_key.replace("a"), "c")

    def test_replace_empty(self):
        """test Heap.replace(item) on empty Heap raises IndexError"""
        with self.assertRaises(IndexError):
            _ = self.heap_empty.replace("a")

    def test_size_empty(self):
        """test empty Heap .size() == 0"""
        self.assertEqual(len(self.heap_empty), 0)
        self.assertEqual(len(self.heap_empty.heap), 0)

    def test_size_input(self):
        """test Heap .size() matches size of input"""
        HEAP_DATA = ["ccc", "bb", "a"]
        heap = Heap(HEAP_DATA)
        self.assertEqual(len(heap), len(HEAP_DATA))

    def test_size_push(self):
        """test Heap.push() increments Heap.size()"""
        prev_len = len(self.heap_test)
        self.heap_test.push("d")
        self.assertEqual(len(self.heap_test), prev_len + 1)

    def test_size_push_key(self):
        """test Heap.push() increments Heap.size()"""
        prev_len = len(self.heap_key)
        self.heap_key.push("d")
        self.assertEqual(len(self.heap_key), prev_len + 1)

    def test_size_pop(self):
        """test Heap.pop() decrements Heap.size()"""
        prev_len = len(self.heap_test)
        _ = self.heap_test.pop()
        self.assertEqual(len(self.heap_test), prev_len - 1)

    def test_size_pop_key(self):
        """test Heap.pop() decrements Heap.size()"""
        prev_len = len(self.heap_key)
        _ = self.heap_key.pop()
        self.assertEqual(len(self.heap_key), prev_len - 1)

    def test_str(self):
        """test str(Heap)"""
        self.assertEqual(str(self.heap_test), "Heap(['aaa', 'bb', 'c'])")
        self.assertEqual(str(self.heap_test), "Heap(" + str(self.heap_test.heap) + ")")

    def test_str_key(self):
        """test str(Heap) with key"""
        self.assertEqual(str(self.heap_key), "Heap([(1, 'c'), (2, 'bb'), (3, 'aaa')])")
        self.assertEqual(str(self.heap_key), "Heap(" + str(self.heap_key.heap) + ")")

    def test_str_empty(self):
        """test str(Heap) on empty Heap"""
        self.assertEqual(str(self.heap_empty), "Heap([])")
        self.assertEqual(str(self.heap_empty.heap), "[]")
