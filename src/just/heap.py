#!/usr/bin/env python3

"""Priority Heap class using the standard `heaqp` module
see: https://youtu.be/o9pEzgHorH0?t=851
"""


# standard imports
import heapq


class Heap:
    """Priority Heap class using the standard `heaqp` module."""

    def __init__(self, data=None, key=None):
        """Create a new Heap.
        If `data` is given, use it as the item storage for this Heap.
        If `key` is given, use it to compute priority for each item.
        """
        self.heap = data or []
        heapq.heapify(self.heap)
        self.key = key

    def __len__(self) -> int:
        """Number of items in the Heap"""
        return len(self.heap)

    def __str__(self) -> str:
        """Shows the collection as a string like Heap([item0, item1, ...])"""
        return "Heap(%s)" % str(self.heap)

    def peek(self):
        """Show the top of the heap."""

        top = self.heap[0]
        if self.key:
            top = top[1]
        return top

    def push(self, item):
        """Add item into the Heap."""

        if self.key:
            item = (self.key(item), item)
        heapq.heappush(self.heap, item)

    def pop(self):
        """Remove from Heap item with highest priority."""

        item = heapq.heappop(self.heap)
        if self.key:
            item = item[1]
        return item

    def pushpop(self, item):
        """Push item on the heap, then pop and return the smallest item from the heap.
        The combined action runs more efficiently than heap.push() followed by a separate call to heap.pop().
        """
        # mostly taken from https://docs.python.org/3/library/heapq.html

        if self.key:
            item = (self.key(item), item)
        item = heapq.heappushpop(self.heap, item)
        if self.key:
            item = item[1]
        return item

    def replace(self, item):
        """Pop and return the smallest item from the heap, and also push the new item.
        The heap size doesn't change. If the heap is empty, IndexError is raised.

        This one step operation is more efficient than a heap.pop() followed by
        heap.push() and can be more appropriate when using a fixed-size heap.
        The pop/push combination always returns an element from the heap and
        replaces it with item.

        The value returned may be larger than the item added.
        If that isn't desired, consider using heap.pushpop() instead.
        Its push/pop combination returns the smaller of the two values,
        leaving the larger value on the heap.
        """
        # mostly taken from https://docs.python.org/3/library/heapq.html

        if self.key:
            item = (self.key(item), item)
        item = heapq.heapreplace(self.heap, item)
        if self.key:
            item = item[1]
        return item


def main() -> None:
    """Simple test."""

    # test without key
    heap = Heap(["ccc", "bb", "a"])
    print(heap)
    heap.push("bbb")
    heap.push("bbbbbb")
    print(heap)
    while len(heap):
        top = heap.pop()
        print("popped:", repr(top))
    print()

    # test with key FIXME
    heap = Heap([(3, "ccc"), (2, "bb"), (1, "a")], key=len)
    print(heap)
    heap.push("b")
    heap.push("bbbbbb")
    print(heap)
    while len(heap):
        top = heap.pop()
        print("popped:", repr(top))
    print()


if __name__ == "__main__":
    main()
