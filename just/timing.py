#!/usr/bin/env python3


# standard imports
import contextlib
import functools
import logging
import time


# use a decorator factory
# https://stackoverflow.com/a/10176276
# FIXME when no arguments are provided, needs to be called with parentheses
#       i.e. `@timed()`, not just `@timed`
def timed(do_print=True, logger=None, level=logging.INFO):
    """Perform timing of the execution of the decorated function
    Output to stdout and to a given logger.
    """

    # validate parameters
    # FIXME is this the best way to check?
    if logger is not None and not isinstance(logger, logging.Logger):
        raise TypeError(f"logger is {type(logger)}, should be {type(logging.Logger)}")
    if level not in logging._levelToName:
        raise ValueError(f"logging level {repr(level)} not recognized, see {logging._levelToName}")

    def decorate(func):
        @functools.wraps(func) # preserves metadata (name, stack, etc.) of func when decorated
        def wrapped(*args, **kwargs):
            # start timing
            time_begin = time.perf_counter()

            # call the wrapped function
            result = func(*args, **kwargs)

            # finish timing
            time_end = time.perf_counter()
            time_taken = time_end - time_begin

            # output result
            if do_print:
                print("func %s args %r kwargs %r took %.3f seconds" % (func.__name__, args, kwargs, time_taken))
            if logger is not None:
                logger.info("func %s args %r kwargs %r took %.3f seconds", func.__name__, args, kwargs, time_taken)
            
            # return the result of the wrapped function
            return result

        # return the wrapped function
        return wrapped

    # return the decorator
    return decorate


@contextlib.contextmanager
def timing(message: str, do_print=True, logger=None, level=logging.INFO):
    """Perform timing of the execution of the given context
    Output to stdout and to a given logger.
    """

    # validate parameters
    # FIXME is this the best way to check?
    if level not in logging._levelToName:
        raise ValueError()
    if level not in logging._levelToName:
        raise ValueError(f"logging level {repr(level)} not recognized, see {logging._levelToName}")

    # start timing
    time_begin = time.perf_counter()

    # execute context
    yield

    # finish timing
    time_end = time.perf_counter()
    time_taken = time_end - time_begin

    # output result
    if do_print:
        print("%s took %.3f seconds" % (message, time_taken))
    if logger is not None:
        if isinstance(logger, logging.Logger):
            logger.log(level, "%s took %.3f seconds", message, time_taken)
        else:
            raise TypeError(f"logger is {type(logger)}, should be {logging.Logger}")
    

def main():
    @timed(level="jjj")
    def timing_test(arg1, arg2):
        for _ in range(1_000_000):
            pass
    
    timing_test("arg1", arg2="")

    with timing("timing context test"):
        for _ in range(1_000_000):
            pass


if __name__ == "__main__":
    main()