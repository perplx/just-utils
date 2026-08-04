"""FIXME
see: https://www.bitecode.dev/p/python-cocktail-mix-a-context-manager
see: https://lobste.rs/s/xhe7sr/python_cocktail_mix_context_manager'
"""

import functools
import logging
import time
from typing import Callable, ParamSpec, Type, TypeVar


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
            for i in range(1, tries+1):
                try:
                    return func(*args, **kwargs)
                except error as e:
                    if i >= tries:
                        logger.error("caught %s - aborting %d / %d ...", e, i, tries)
                        raise  # last attempt: the caller gets the exception
                    logger.warning("caught %s - retrying %d / %d ...", e, i, tries)
                    if delay > 0:
                        time.sleep(delay)
            raise ValueError(f"tries must be at least 1, got {tries}")
        return wrapper
    return decorate


class RetryContext:

    def __init__(self, success: Callable, attempt: int):
        self._success = success
        self._attempt = attempt

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            logger.warning("failed attempt %d", self._attempt)
        else:
            self._success()
        return True  # FIXME swallow exception?


class RetryIterator:
    def __init__(self, attempts: int):
        self._max_attempts = attempts
        self._success = False

    def __iter__(self):
        for i in range(self._max_attempts):
            yield RetryContext(self.succeed, i+1)
            if self._success:
                break
            else:
                logger.warning("caught something - retrying %d / %d ...", i+1, self._max_attempts)

    def succeed(self):
        self._success = True


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

    # test decorator

    flaky_func = flaky(3)

    @retry(RuntimeError, tries=4, delay=0.1)
    def test_func() -> str:
        return flaky_func()

    print(test_func())

    # test context-manager

    flaky_func = flaky(30)

    for attempt in RetryIterator(attempts=5):
        with attempt:
            print(flaky_func())


if __name__ == "__main__":
    main()
