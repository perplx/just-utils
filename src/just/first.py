#!/usr/bin/env python3

from typing import Callable, Iterable, TypeVar


DEFAULT_VALUE = None


T = TypeVar("T")
C = Callable[[T], bool]


def first_next(iter: Iterable[T]) -> T:
    return next((i for i in iter if i), None)


def first_condition(iter: Iterable[T], call: C) -> T:
    return next((i for i in iter if call(i)), None)


def main() -> None:
    TESTS = [
        [0, 0, 0],
        [0, 0, 0, 1, 0, 2],
        [1, 3, 8, 9],
    ]

    for test in TESTS:
        print(test)
        print(f"{first_next.__name__}: {first_next(test)}")
        print(f"{first_condition.__name__}: {first_condition(test, lambda x: x)}")
        print(f"{first_condition.__name__}: {first_condition(test, lambda x: int(x) % 3 == 2)}")
        print()

    TESTS = [
        [None, 0],
        [None, False],
        [None, 0, 0.0, False, dict(), list(), set(), 1],
    ]

    for test in TESTS:
        print(test)
        print(f"{first_next.__name__}: {first_next(test)}")
        print(f"{first_condition.__name__}: {first_condition(test, lambda x: x)}")
        print(f"{first_condition.__name__}: {first_condition(test, lambda x: x is not None)}")
        print()


if __name__ == "__main__":
    main()
