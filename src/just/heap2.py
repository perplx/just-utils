"""Implementaton of a min-heap piority-queue class, based on the standard library `heapq` module.
see: https://docs.python.org/3/library/heapq.html
Now with type annotations.
"""

import heapq
from typing import Callable, Generic, Iterable, Protocol, TypeVar


T = TypeVar("T")


class SupportsLessThan(Protocol):
    """A type that can be ordered with `<`, as required by `heapq`."""

    def __lt__(self, other: object) -> bool: ...


K = TypeVar("K", bound=SupportsLessThan)


# FIXME support maxheap? (version of python: 3.14...)
# FIXME support key-function without type complications
# FIXME support pushpop, extra operations, __str__, etc.
# FIXME tests!!!!
# FIXME docstrings!!!
# FIXME link to youtube video?
class Heap(Generic[T]):
    """FIXME"""

    def __init__(self, data: Iterable[T]):
        """FIXME"""
        self._heap = list(data)  # FIXME copy or take>
        heapq.heapify(self._heap)

    def __len__(self) -> int:
        """Number of items in the `Heap`."""
        return len(self._heap)

    def __str__(self) -> str:
        """FIXME"""
        return f"Heap({self._heap})"

    def peek(self) -> T:
        """FIXME"""
        top = self._heap[0]
        return top

    def pop(self) -> T:
        """FIXME"""
        top: T = heapq.heappop(self._heap)
        return top

    def push(self, item: T) -> None:
        """FIXME"""
        heapq.heappush(self._heap, item)

    def pushpop(self, item: T) -> T:
        """FIXME"""
        top: T = heapq.heappushpop(self._heap, item)
        return top

    def replace(self, item: T) -> T:
        """FIXME"""
        top: T = heapq.heapreplace(self._heap, item)
        return top


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
        return f"KeyHeap({[item for _, item in self._heap]})"

    def peek(self) -> T:
        """Return the item with the smallest key without removing it."""
        return self._heap[0][1]

    def pop(self) -> T:
        """Remove and return the item with the smallest key."""
        return heapq.heappop(self._heap)[1]

    def push(self, item: T) -> None:
        """Add `item` to the heap."""
        heapq.heappush(self._heap, (self._key(item), item))

    def pushpop(self, item: T) -> T:
        """Push `item`, then pop and return the item with the smallest key."""
        return heapq.heappushpop(self._heap, (self._key(item), item))[1]

    def replace(self, item: T) -> T:
        """Pop and return the item with the smallest key, then push `item`."""
        return heapq.heapreplace(self._heap, (self._key(item), item))[1]


def main() -> None:
    """Simple test."""
    l = [1, 2, 6, 3, 4, 1, 7, 9]
    heap = Heap(l)
    print(f"heap: {heap}")
    while len(heap) > 0:
        top = heap.pop()
        print(f"{top} <- {heap}")


if __name__ == "__main__":
    main()
