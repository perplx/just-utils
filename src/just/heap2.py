"""Implementaton of a min-heap piority-queue class, based on the standard library `heapq` module.
Now with type annotations.

- see: https://docs.python.org/3/library/heapq.html
- see: https://youtu.be/o9pEzgHorH0?t=851
"""

import heapq
from typing import Any, Callable, Generic, Iterable, Iterator, Protocol, TypeVar


class SupportsLessThan(Protocol):
    """A type that can be ordered with `<`, as required by `heapq`."""

    def __lt__(self, other: Any) -> bool:
        """Return whether `self` sorts before `other`."""


T = TypeVar("T", bound=SupportsLessThan)
K = TypeVar("K", bound=SupportsLessThan)


# FIXME support maxheap? (version of python: 3.14...)
# FIXME link to youtube video?
class Heap(Generic[T]):
    """FIXME"""

    def __init__(self, data: Iterable[T]):
        """Build a heap from `data`."""
        self._heap = list(data)
        heapq.heapify(self._heap)

    def __len__(self) -> int:
        """Number of items in the `Heap`."""
        return len(self._heap)

    def __repr__(self) -> str:
        """Show the stored items."""
        return f"{type(self).__name__}({self._heap!r})"

    # low-level functions derived from `heapq`

    def peek(self) -> T:
        """Return the smallest item without removing it.

        :return: the smallest item.
        :raise IndexError: when the `Heap` is empty.
        """
        return self._heap[0]

    def pop(self) -> T:
        """Remove and return the smallest item.

        :return: the smallest item.
        :raise IndexError: when the `Heap` is empty.
        """
        return heapq.heappop(self._heap)

    def push(self, item: T) -> None:
        """Add `item` to the heap.

        :param item: the item to add.
        """
        heapq.heappush(self._heap, item)

    def pushpop(self, item: T) -> T:
        """Push `item`, then pop and return the smallest item.
        Quicker than `push` followed by `pop`.

        :param item: the item to add.
        :return: the smallest of `item` and the items in the `Heap`.
        """
        return heapq.heappushpop(self._heap, item)

    def replace(self, item: T) -> T:
        """Pop and return the smallest item, then push `item`.
        Quicker than `pop` followed by `push`.

        :param item: the item to add.
        :return: the smallest item before `Heap.replace()` was called, possibly larger than `item`.
        :raise IndexError: when the `Heap` is empty.
        """
        return heapq.heapreplace(self._heap, item)

    # high-level functions

    def clear(self) -> None:
        """Remove all items from the `Heap`."""
        self._heap.clear()

    def drain(self) -> Iterator[T]:
        """Create an `Iterator` to pop out each item in the `Heap` in order.

        :return: an `Iterator` that will empty the heap as it iterates over items.

        ex::

            >>> heap = Heap(["c", "bb", "aaa"])
            >>> list(heap.drain())
            ['aaa', 'bb', 'c']
        """
        while self._heap:
            yield self.pop()


class KeyHeap(Generic[K, T]):
    """A min-heap ordered by a key-function, the way `key=` orders `sorted()`.

    Internally stores `(key(item), item)` tuples so ordering follows the key,
    while the public API accepts and returns the original items of type `T`.

    Note: if two items produce keys that compare equal, `heapq` falls back to
    comparing the items themselves, so `T` must be orderable in that case (or
    keys must be unique). This matches the classic `(priority, item)` idiom.
    """

    def __init__(self, data: Iterable[T], key: Callable[[T], K]):
        """Build a heap from `data`, prioritised by `key`."""
        self._key = key
        self._heap: list[tuple[K, T]] = [(key(item), item) for item in data]
        heapq.heapify(self._heap)

    def __len__(self) -> int:
        """Number of items in the `KeyHeap`."""
        return len(self._heap)

    def __str__(self) -> str:
        """Show the stored items (not their keys)."""
        return f"{type(self).__name__}({[item for _, item in self._heap]})"

    def __repr__(self) -> str:
        """Show the stored keys and items."""
        return f"{type(self).__name__}({self._heap!r}, key={self._key!r})"

    # low-level functions derived from `heapq`

    def peek(self) -> T:
        """Return the item with the smallest key without removing it.

        :return: the item with the smallest key.
        :raise IndexError: when the `KeyHeap` is empty.
        """
        return self._heap[0][1]

    def pop(self) -> T:
        """Remove and return the item with the smallest key.

        :return: the item with the smallest key.
        :raise IndexError: when the `KeyHeap` is empty.
        """
        return heapq.heappop(self._heap)[1]

    def push(self, item: T) -> None:
        """Add `item` to the heap, using the `key` function to compute its key.

        :param item: the item to add.
        """
        heapq.heappush(self._heap, (self._key(item), item))

    def pushpop(self, item: T) -> T:
        """Push `item`, then pop and return the item with the smallest key.
        Quicker than `push` followed by `pop`.

        :param item: the item to add.
        :return: the item with the smallest key between `item` and the items in the `KeyHeap`.
        """
        return heapq.heappushpop(self._heap, (self._key(item), item))[1]

    def replace(self, item: T) -> T:
        """Pop and return the item with the smallest key, then push `item`.
        Quicker than `pop` followed by `push`.

        :param item: the item to add.
        :return: the item with the smallest key before `KeyHeap.replace()` was called, possibly larger than `item`.
        :raise IndexError: when the `KeyHeap` is empty.
        """
        return heapq.heapreplace(self._heap, (self._key(item), item))[1]

    # high-level functions

    def clear(self) -> None:
        """Remove all items from the `KeyHeap`. Keep the `key` function unchanged."""
        self._heap.clear()

    def drain(self) -> Iterator[T]:
        """Create an `Iterator` to pop out each item in the `KeyHeap` in order of key.

        :return: an `Iterator` that will empty the heap as it iterates over items in order of key.

        ex::

            >>> heap = KeyHeap(["aaa", "bb", "c"], key=len)
            >>> list(heap.drain())
            ['c', 'bb', 'aaa']
        """
        while self._heap:
            yield self.pop()


def main() -> None:
    """Simple test."""
    data = [1, 2, 6, 3, 4, 1, 7, 9]
    heap = Heap(data)
    print(f"heap: {heap}")
    while len(heap) > 0:
        top = heap.pop()
        print(f"{top} <- {heap}")


if __name__ == "__main__":
    main()
