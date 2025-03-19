#!/usr/bin/env python3

"""Like ``any()`` but returns the first element."""


# standard imports
from typing import Callable, Iterable, Optional, TypeVar


# global constants
DEFAULT_VALUE = None


# type definitions
T = TypeVar("T")
C = Callable[[T], bool]


# FIXME raise IndexError if none are found?
def first_next(iter: Iterable[T]) -> Optional[T]:
    """Return the first item in ``iter`` that is true, or ``None`` if no item such is in ``iter``.

    ex::

        >>> first_next([0, 0, 0])
        None
        >>> first_next([0, 0, 0, 1, 0, 2])
        1
        >>> first_next([None, 0, {}, [], 1])
        1

    :param iter: an ``Iterable`` of items of type ``T``
    :return: the first item in ``iter`` that is true.
    """
    return next((i for i in iter if i), None)


# FIXME raise IndexError if none are found?
def first_condition(iter: Iterable[T], call: C) -> Optional[T]:
    """Return the first item in ``iter`` for which ``call(item)`` is true, or ``None`` if no such item is in ``iter``.

    ex::

        >>> first_condition([1, 3, 8, 9], lambda x: x > 10000)
        None
        >>> first_condition([1, 3, 8, 9], lambda x: int(x) % 3 == 2)
        8
        >>> first_condition([None, 0, {}, [], 1], lambda x: x is not None)
        0

    :param iter: an ``Iterable`` of items of type ``T``
    :param call: returns whether the item is true.
    :return: the first item in ``iter`` that is true.
    """
    return next((i for i in iter if call(i)), None)


def main() -> None:
    """Simple test."""

    # test `first_next` and `first_condition` on integers
    TESTS_INT = [
        [0, 0, 0],
        [0, 0, 0, 1, 0, 2],
        [1, 3, 8, 9],
    ]
    for test in TESTS_INT:
        print(test)
        print(f"{first_next.__name__}: {first_next(test)}")
        print(f"{first_condition.__name__}: {first_condition(test, lambda x: x)}")
        print(f"{first_condition.__name__} (> 10000): {first_condition(test, lambda x: x > 10000)}")
        print(f"{first_condition.__name__} (% 3 == 2): {first_condition(test, lambda x: x % 3 == 2)}")
        print()

    # test `first_next` and `first_condition` on false objects
    TESTS_FALSE = [
        [None, 0],
        [None, False],
        [None, 0, 0.0, False, dict(), list(), set(), 1],
    ]
    for test in TESTS_FALSE:
        print(test)
        print(f"{first_next.__name__}: {first_next(test)}")
        print(f"{first_condition.__name__}: {first_condition(test, lambda x: x)}")
        print(f"{first_condition.__name__} (not None): {first_condition(test, lambda x: x is not None)}")
        print()


if __name__ == "__main__":
    main()
