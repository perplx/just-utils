"""FIXME
see: https://lobste.rs/s/xhe7sr/python_cocktail_mix_context_manager
"""

import functools
import logging
import time
from typing import Callable, Optional, ParamSpec, Type, TypeVar


logger = logging.getLogger(__name__)


P = ParamSpec("P")
R = TypeVar("R")


# FIXME default value for error?
# FIXME support multiple exceptions in tuple? Union[Type[Exception], Tuple[Type[Exception], ...]]
# FIXME support logger as parameter?
def retry(error: Type[Exception], tries: int, delay: float = 0.0):
    def decorate(func: Callable[P, R]) -> Callable[P, R]:
        # preserves metadata (name, stack, etc.) of func when decorated
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            caught: Optional[Exception] = None
            for i in range(tries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except error as e:
                    logger.warning("cauget %s - retrying...", e)
                    caught = e
                    if delay > 0:
                        time.sleep(delay)
            raise caught
        return wrapper
    return decorate


def main() -> None:
    """Simple test."""

    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=logging.NOTSET)

    def flaky(failures: int) -> Callable[[], str]:
        """Return a function that will fail for `failures` times, then return OK."""

        def call() -> str:
            nonlocal failures
            if failures > 0:
                failures -= 1
                raise RuntimeError(f"{failures} failures left")
            return "ok"

        return call

    flaky_func = flaky(20)

    @retry(RuntimeError, tries=4, delay=0.1)
    def test_func() -> str:
        return flaky_func()

    print(test_func())


if __name__ == "__main__":
    main()
