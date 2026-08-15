#!/usr/bin/env python3

"""Like ``any()`` but returns the first element."""


# standard imports
from typing import Any, Callable, Iterable, List, Optional, TypeVar


# type definitions
T = TypeVar("T")

# sentinel value
_MISSING = object()


def first(iterable: Iterable[T], condition: Callable[[T], Any] = bool, default=_MISSING) -> Optional[T]:
    """Return the first item in ``iterable`` for which ``condition(item)`` is true.
    If no condition is provided, ``bool()`` is used, it check the truth-value of ``item``.
    If no item is found to satisfy the condition, raise ``ValueError``.

    no condition given
    ex::

        >>> first([0, 0, 0], default=None)
        None
        >>> first([0, 0, 0, 1, 0, 2])
        1
        >>> first([None, 0, {}, [], 1])
        1

    condition given
    ex::
        >>> first([1, 3, 8, 9], lambda x: x > 10000, default=None)
        None
        >>> first([1, 3, 8, 9], lambda x: int(x) % 3 == 2)
        8
        >>> first([None, 0, {}, [], 1], lambda x: x is not None)
        0

    :param iterable: an ``Iterable`` of items of type ``T``
    :param condition: returns whether the item is true.
    :return: the first item in ``iterable`` that is true.
    :raise ValueError: when no item is found to satisfy the condition
    """
    item = next((i for i in iterable if condition(i)), default)
    if item is _MISSING:
        raise ValueError(f"no item found to satisfy condition: {condition}")
    return item


def last(iterable: Iterable[T], condition: Callable[[T], Any] = bool, default=_MISSING) -> Optional[T]:
    item = default
    for i in iterable:
        if condition(i):
            item = i
    if item is _MISSING:
        raise ValueError(f"no item found to satisfy condition: {condition}")
    return item


def only(iterable: Iterable[T], condition: Callable[[T], Any] = bool, default=_MISSING) -> Optional[T]:
    # A single iterator, so the second `next()` resumes where the first one stopped.
    matches = filter(condition, iterable)
    item = next(matches, _MISSING)
    if item is _MISSING:
        if default is _MISSING:
            raise ValueError(f"no item found to satisfy condition: {condition}")
        return default
    if next(matches, _MISSING) is not _MISSING:
        raise ValueError(f"more than one item found to satisfy condition: {condition}")
    return item


def main() -> None:
    """Simple test."""

    # test `first_next` and `first_condition` on integers
    TESTS_INT: List[List[int]] = [
        [0, 0, 0],
        [0, 0, 0, 1, 0, 2],
        [1, 3, 8, 9],
    ]
    for items in TESTS_INT:
        print(items)
        print(f"{first.__name__}: {first(items, default=None)}")
        print(f"{first.__name__}: {first(items, lambda x: x, default=None)}")
        print(f"{first.__name__} (> 10000): {first(items, lambda x: x > 10000, default=None)}")
        print(f"{first.__name__} (% 3 == 2): {first(items, lambda x: x % 3 == 2, default=None)}")
        print()

    # test `first_next` and `first_condition` on false objects
    TESTS_FALSE: List[List[Any]] = [
        [None, 0],
        [None, False],
        [None, 0, 0.0, False, dict(), list(), set(), 1],
    ]
    for items in TESTS_FALSE:
        print(items)
        print(f"{first.__name__}: {first(items, default=None)}")
        print(f"{first.__name__}: {first(items, lambda x: x, default=None)}")
        print(f"{first.__name__} (not None): {first(items, lambda x: x is not None, default=None)}")
        print()

if __name__ == "__main__":
    main()
