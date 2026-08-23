"""Memoization decorator that caches results keyed on the call arguments.

Arguments must be hashable, the same constraint `functools.lru_cache` imposes.
"""

import functools
import logging
from typing import Any, Callable, Dict, ParamSpec, TypeVar


logger = logging.getLogger(__name__)


P = ParamSpec("P")
R = TypeVar("R")


def memoize(func: Callable[P, R]) -> Callable[P, R]:
    cache: Dict[Any, R] = {}

    @functools.wraps(func)
    def wrapped_func(*args: P.args, **kwargs: P.kwargs) -> R:
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapped_func


def main() -> None:
    """Simple test."""

    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s")

    @memoize
    def test_func() -> None:
        import time

        time.sleep(1)

    for i in range(5):
        logger.warning("test %d", i + 1)
        test_func()


if __name__ == "__main__":
    main()
