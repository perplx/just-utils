import unittest

from just.heap2 import Heap, KeyHeap


class TestHeap2(unittest.TestCase):
    """Tests for class just.heap.Heap"""

    def setUp(self):
        # TEST_DATA is mutable!
        TEST_DATA = ["c", "bb", "aaa"]
        self.heap_test = Heap[int](TEST_DATA)

    def test_bool(self):
        self.assertTrue(self.heap_test)
        self.assertFalse(Heap([]))

    def test_len(self):
        self.assertEqual(len(self.heap_test), 3)

    def test_str(self):
        self.assertEqual(str(self.heap_test), "Heap(['aaa', 'bb', 'c'])")

    def test_peek(self):
        self.assertEqual(self.heap_test.peek(), "aaa")

    def test_pop(self):
        self.assertEqual(self.heap_test.pop(), "aaa")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_push(self):
        self.heap_test.push("b2")
        self.assertEqual(self.heap_test._heap, ["aaa", "b2", "c", "bb"])
        self.assertEqual(self.heap_test.pop(), "aaa")
        self.assertEqual(self.heap_test.pop(), "b2")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_pushpop_middle(self):
        self.assertEqual(self.heap_test.pushpop("b2"), "aaa")
        self.assertEqual(self.heap_test.pop(), "b2")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_pushpop_top(self):
        self.assertEqual(self.heap_test.pushpop("a1"), "a1")
        self.assertEqual(self.heap_test.pop(), "aaa")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_replace_middle(self):
        self.assertEqual(self.heap_test.replace("c3"), "aaa")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c")
        self.assertEqual(self.heap_test.pop(), "c3")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_replace_top(self):
        self.assertEqual(self.heap_test.replace("a1"), "aaa")
        self.assertEqual(self.heap_test.pop(), "a1")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()


class TestKeyHeap(unittest.TestCase):
    """Tests for class just.heap.KeyHeap, ordered by `len`.

    Identical to TestHeap2, but priority is the string length instead of the
    natural string ordering, so the expected order is reversed accordingly.
    """

    def setUp(self):
        # TEST_DATA is mutable!
        TEST_DATA = ["c", "bb", "aaa"]
        self.heap_test = KeyHeap[int, str](TEST_DATA, key=len)

    def test_bool(self):
        self.assertTrue(self.heap_test)
        self.assertFalse(KeyHeap([], key=len))

    def test_len(self):
        self.assertEqual(len(self.heap_test), 3)

    def test_str(self):
        self.assertEqual(str(self.heap_test), "KeyHeap(['c', 'bb', 'aaa'])")

    def test_peek(self):
        self.assertEqual(self.heap_test.peek(), "c")

    def test_pop(self):
        self.assertEqual(self.heap_test.pop(), "c")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "aaa")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_push(self):
        self.heap_test.push("b2")
        self.assertEqual(
            self.heap_test._heap,
            [(1, "c"), (2, "b2"), (3, "aaa"), (2, "bb")],
        )
        self.assertEqual(self.heap_test.pop(), "c")
        self.assertEqual(self.heap_test.pop(), "b2")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "aaa")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_pushpop_middle(self):
        self.assertEqual(self.heap_test.pushpop("b2"), "c")
        self.assertEqual(self.heap_test.pop(), "b2")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "aaa")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_pushpop_top(self):
        self.assertEqual(self.heap_test.pushpop("a1"), "c")
        self.assertEqual(self.heap_test.pop(), "a1")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "aaa")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_replace_middle(self):
        self.assertEqual(self.heap_test.replace("c3"), "c")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c3")
        self.assertEqual(self.heap_test.pop(), "aaa")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_replace_top(self):
        self.assertEqual(self.heap_test.replace("a1"), "c")
        self.assertEqual(self.heap_test.pop(), "a1")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "aaa")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()
