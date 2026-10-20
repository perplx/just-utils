import unittest

from just.heap2 import Heap, KeyHeap


class TestHeap(unittest.TestCase):
    """Tests for class `just.heap2.Heap`."""

    def setUp(self):
        # TEST_DATA is mutable!
        TEST_DATA = ["c", "bb", "aaa"]
        self.heap_test = Heap[str](TEST_DATA)
        self.heap_empty = Heap[str]([])

    def test_bool(self):
        """Test `bool(just.heap2.Heap)` falls back to calling `__len__`."""
        self.assertTrue(self.heap_test)
        self.assertFalse(self.heap_empty)

    def test_len(self):
        """Test `len(just.heap2.Heap)`."""
        self.assertEqual(len(self.heap_test), 3)

    def test_str(self):
        """Test `str(just.heap2.Heap)`."""
        self.assertEqual(str(self.heap_test), "Heap(['aaa', 'bb', 'c'])")

    def test_repr(self):
        """Test `repr(just.heap2.Heap)`."""
        self.assertEqual(repr(self.heap_test), "Heap(['aaa', 'bb', 'c'])")

    def test_peek(self):
        """Test `just.heap2.Heap.peek()`."""
        self.assertEqual(self.heap_test.peek(), "aaa")

    def test_peek_empty(self):
        """Test `just.heap2.Heap.peek()` on an empty `Heap`."""
        with self.assertRaises(IndexError):
            _ = self.heap_empty.peek()

    def test_pop(self):
        """Test `just.heap2.Heap.pop()`."""
        self.assertEqual(self.heap_test.pop(), "aaa")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c")
        self.assertEqual(len(self.heap_test), 0)
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_pop_empty(self):
        """Test `just.heap2.Heap.pop()` on an empty `Heap`."""
        with self.assertRaises(IndexError):
            _ = self.heap_empty.pop()

    def test_push(self):
        """Test `just.heap2.Heap.push()`."""
        self.heap_test.push("b2")
        self.assertEqual(self.heap_test._heap, ["aaa", "b2", "c", "bb"])
        self.assertEqual(self.heap_test.pop(), "aaa")
        self.assertEqual(self.heap_test.pop(), "b2")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_pushpop_middle(self):
        """Test `just.heap2.Heap.pushpop(item)` where item goes to the middle of the heap."""
        self.assertEqual(self.heap_test.pushpop("b2"), "aaa")
        self.assertEqual(self.heap_test.pop(), "b2")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_pushpop_top(self):
        """Test `just.heap2.Heap.pushpop(item)` where item goes to the top of the heap."""
        self.assertEqual(self.heap_test.pushpop("a1"), "a1")
        self.assertEqual(self.heap_test.pop(), "aaa")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_replace_middle(self):
        """Test `just.heap2.Heap.replace(item)` where item goes to the middle of the heap."""
        self.assertEqual(self.heap_test.replace("c3"), "aaa")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c")
        self.assertEqual(self.heap_test.pop(), "c3")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_replace_top(self):
        """Test `just.heap2.Heap.replace(item)` where item goes to the top of the heap."""
        self.assertEqual(self.heap_test.replace("a1"), "aaa")
        self.assertEqual(self.heap_test.pop(), "a1")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_replace_empty(self):
        """Test `just.heap2.Heap.replace()` on an empty `Heap`."""
        with self.assertRaises(IndexError):
            _ = self.heap_empty.replace("BOGUS")

    def test_clear(self):
        """Test `just.heap2.Heap.clear()`."""

        # test clearing works
        self.assertGreater(len(self.heap_test), 0)
        self.heap_test.clear()
        self.assertEqual(len(self.heap_test), 0)

        # test item order still works
        self.heap_test.push("b")
        self.heap_test.push("aa")
        self.assertEqual(self.heap_test.pop(), "aa")
        self.assertEqual(self.heap_test.pop(), "b")

    def test_drain(self):
        """Test `just.heap2.Heap.drain()`."""
        heap_iter = self.heap_test.drain()
        self.assertEqual(next(heap_iter), "aaa")
        self.assertEqual(next(heap_iter), "bb")
        self.assertEqual(next(heap_iter), "c")
        with self.assertRaises(StopIteration):
            _ = next(heap_iter)
        self.assertEqual(len(self.heap_test), 0)


class TestKeyHeap(unittest.TestCase):
    """Tests for class `just.heap2.KeyHeap`, stores `str` objects ordered by `len`.

    Identical to TestHeap, but priority is the string length instead of the
    natural string ordering, so the expected order is reversed accordingly.
    """

    def setUp(self):
        # TEST_DATA is mutable!
        TEST_DATA = ["c", "bb", "aaa"]
        self.heap_test = KeyHeap[int, str](TEST_DATA, key=len)
        self.heap_empty = KeyHeap[int, str]([], key=len)

    def test_bool(self):
        """Test `bool(just.heap2.KeyHeap)` falls back to calling `__len__`."""
        self.assertTrue(self.heap_test)
        self.assertFalse(self.heap_empty)

    def test_len(self):
        """Test `len(just.heap2.KeyHeap)`."""
        self.assertEqual(len(self.heap_test), 3)
        self.assertEqual(len(self.heap_empty), 0)

    def test_str(self):
        """Test `str(just.heap2.KeyHeap)`."""
        self.assertEqual(str(self.heap_test), "KeyHeap(['c', 'bb', 'aaa'])")

    def test_repr(self):
        """Test `repr(just.heap2.KeyHeap)`."""
        self.assertEqual(
            repr(self.heap_test), "KeyHeap([(1, 'c'), (2, 'bb'), (3, 'aaa')], key=<built-in function len>)"
        )

    def test_peek(self):
        """Test `just.heap2.KeyHeap.peek()`."""
        self.assertEqual(self.heap_test.peek(), "c")

    def test_peek_empty(self):
        """Test `just.heap2.KeyHeap.peek()` on an empty `KeyHeap`."""
        with self.assertRaises(IndexError):
            _ = self.heap_empty.peek()

    def test_pop(self):
        """Test `just.heap2.KeyHeap.pop()`."""
        self.assertEqual(self.heap_test.pop(), "c")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "aaa")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_pop_empty(self):
        """Test `just.heap2.KeyHeap.pop()` on an empty `KeyHeap`."""
        with self.assertRaises(IndexError):
            _ = self.heap_empty.pop()

    def test_push(self):
        """Test `just.heap2.KeyHeap.push()`."""
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
        """Test `just.heap2.KeyHeap.pushpop(item)` where item goes to the middle of the heap."""
        self.assertEqual(self.heap_test.pushpop("b2"), "c")
        self.assertEqual(self.heap_test.pop(), "b2")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "aaa")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_pushpop_top(self):
        """Test `just.heap2.KeyHeap.pushpop(item)` where item goes to the top of the heap."""
        self.assertEqual(self.heap_test.pushpop("a1"), "c")
        self.assertEqual(self.heap_test.pop(), "a1")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "aaa")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_replace_middle(self):
        """Test `just.heap2.KeyHeap.replace(item)` where item goes to the middle of the heap."""
        self.assertEqual(self.heap_test.replace("c3"), "c")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "c3")
        self.assertEqual(self.heap_test.pop(), "aaa")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_replace_top(self):
        """Test `just.heap2.KeyHeap.replace(item)` where item goes to the top of the heap."""
        self.assertEqual(self.heap_test.replace("a1"), "c")
        self.assertEqual(self.heap_test.pop(), "a1")
        self.assertEqual(self.heap_test.pop(), "bb")
        self.assertEqual(self.heap_test.pop(), "aaa")
        with self.assertRaises(IndexError):
            _ = self.heap_test.pop()

    def test_replace_empty(self):
        """Test `just.heap2.KeyHeap.replace()` on an empty `KeyHeap`."""
        with self.assertRaises(IndexError):
            _ = self.heap_empty.replace("BOGUS")

    def test_clear(self):
        """Test `just.heap2.KeyHeap.clear()`."""

        # test clearing works
        self.assertGreater(len(self.heap_test), 0)
        self.heap_test.clear()
        self.assertEqual(len(self.heap_test), 0)

        # test key order still works
        self.heap_test.push("aa")
        self.heap_test.push("b")
        self.assertEqual(self.heap_test.pop(), "b")
        self.assertEqual(self.heap_test.pop(), "aa")

    def test_drain(self):
        """Test `just.heap2.KeyHeap.drain()`."""
        heap_iter = self.heap_test.drain()
        self.assertEqual(next(heap_iter), "c")
        self.assertEqual(next(heap_iter), "bb")
        self.assertEqual(next(heap_iter), "aaa")
        with self.assertRaises(StopIteration):
            _ = next(heap_iter)
        self.assertEqual(len(self.heap_test), 0)
