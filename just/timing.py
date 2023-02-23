#!/usr/bin/env python3

"""Timing functions"""


# standard imports
import contextlib
import functools
import logging
import time
from typing import Optional


# use a decorator factory
# https://stackoverflow.com/a/10176276
# FIXME when no arguments are provided, needs to be called with parentheses
#       i.e. `@timed()`, not just `@timed`
def timed(do_print: bool = True, logger: Optional[logging.Logger] = None, level: int = logging.INFO):
    """Perform timing of the execution of the decorated function.
    Output to stdout and to a given logger.

    :param do_print: whether to output to stdout
    :param logger: the ``Logger`` where messages will be sent
    :param level: the log-level at which messages will be logged.
    """

    # validate parameters
    if logger is not None and not isinstance(logger, logging.Logger):
        raise TypeError(f"logger is {type(logger)}, should be {type(logging.Logger)}")
    if level not in logging._levelToName:
        raise ValueError(f"logging level {repr(level)} not recognized, see {logging._levelToName}")

    def decorate(func):
        # preserves metadata (name, stack, etc.) of func when decorated
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            # time the call to the wrapped function
            time_begin = time.perf_counter()
            result = func(*args, **kwargs)
            time_end = time.perf_counter()
            time_taken = time_end - time_begin

            # output result
            if do_print:
                print(f"func {func.__name__} args {args} kwargs {kwargs} took {time_taken:.3f} seconds")
            if logger is not None:
                logger.info("func %s args %r kwargs %r took %.3f seconds", func.__name__, args, kwargs, time_taken)

            # return the result of the wrapped function
            return result

        # return the wrapped function
        return wrapped

    # return the decorator
    return decorate


@contextlib.contextmanager
def timing(message: str, do_print: bool = True, logger: Optional[logging.Logger] = None, level: int = logging.INFO):
    """Perform timing of the execution of the given context
    Output to stdout and to a given logger.

    :param message: the message identifying what was timed
    :param do_print: whether to output to stdout
    :param logger: the ``Logger`` where messages will be sent
    :param level: the log-level at which messages will be logged.
    """

    # validate parameters
    if logger is not None and not isinstance(logger, logging.Logger):
        raise TypeError(f"logger is {type(logger)}, should be {logging.Logger}")
    if level not in logging._levelToName:
        raise ValueError(f"logging level {repr(level)} not recognized, see {logging._levelToName}")

    # time the execution of the context
    time_begin = time.perf_counter()
    yield  # execute context
    time_end = time.perf_counter()
    time_taken = time_end - time_begin

    # output result
    if do_print:
        print("%s took %.3f seconds" % (message, time_taken))
    if logger is not None:
        logger.log(level, "%s took %.3f seconds", message, time_taken)


def main() -> None:
    """Simple test"""

    logging.basicConfig(format=r"%(asctime)s %(levelname)-8s : %(message)s", level=logging.DEBUG)
    logger = logging.getLogger("timing")

    # test @timed() decorator
    @timed(logger=logger, level=logging.WARNING)
    def timing_test(arg1, arg2):
        for _ in range(1_000_000):
            pass

    timing_test("arg1", arg2="")

    # test timing() context manager
    with timing("timing context test", logger=logger, level=logging.FATAL):
        for _ in range(1_000_000):
            pass


if __name__ == "__main__":
    main()
