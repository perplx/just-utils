"""Memoization decorator that caches results keyed on the call arguments.

Arguments must be hashable, the same constraint `functools.lru_cache` imposes.
"""

import functools
import logging
import time
from typing import Any, Callable, Dict, ParamSpec, Tuple, TypeVar


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


def ttl_cache(ttl: float):
    def decorate(func: Callable[P, R]) -> Callable[P, R]:
        # cache the results of the decorated function
        # key is the arguments to the function, encoded as a tuple
        # value is the result of the function and the ttl.
        cache: Dict[Any, Tuple[R, float]] = {}

        # preserves metadata (name, stack, etc.) of func when decorated
        @functools.wraps(func)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            # encode parameters to use as the key of the cache
            key = (args, tuple(sorted(kwargs.items())))

            # find the result in the cache and check the ttl
            if key in cache:
                cached_result, cached_ttl  = cache[key]
                if time.time() < cached_ttl:
                    logger.debug("using cached")
                    return cached_result
                else:
                    logger.debug("cache expired")

            # call the function and store the result and ttl
            logger.debug("cache missing")
            called_result = func(*args, **kwargs)
            called_ttl = time.time() + ttl
            cache[key] = (called_result, called_ttl)
            return called_result

        # return the wrapped function
        return wrapped

    # return the decorator
    return decorate


def main() -> None:
    """Simple test."""

    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=logging.NOTSET)

    @memoize
    def test_func() -> None:
        time.sleep(1)

    for i in range(5):
        logger.warning("test %d", i + 1)
        test_func()

    @ttl_cache(3)
    def test_func_ttl() -> None:
        logger.debug("calling `test_func`")

    for i in range(5):
        logger.warning("test %d", i + 1)
        test_func_ttl()
        time.sleep(1)


if __name__ == "__main__":
    main()
