"""Implementaton of a min-heap piority-queue class, based on the standard library `heapq` module.
see: https://docs.python.org/3/library/heapq.html
Now with type annotations.
"""

import heapq
from typing import Collection, Generic, TypeVar


T = TypeVar("T")


# FIXME support maxheap? (version of python: 3.14...)
# FIXME support key-function without type complications
# FIXME support pushpop, extra operations, __str__, etc.
# FIXME tests!!!!
# FIXME docstrings!!!
# FIXME link to youtube video?
class Heap(Generic[T]):
    """FIXME"""

    def __init__(self, data: Collection[T]):
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
        item = heapq.heappop(self._heap)  # FIXME return-type of heappop!?
        return item

    def push(self, item: T) -> None:
        """FIXME"""
        heapq.heappush(self._heap, item)

    def pushpop(self, item: T) -> T:
        """FIXME"""
        item = heapq.heappushpop(self._heap, item)
        return item

    def replace(self, item: T) -> T:
        """FIXME"""
        item = heapq.heapreplace(self._heap, item)
        return item


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
