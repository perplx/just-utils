#!/usr/bin/env python3

"""Deprecation decorator"""


# standard imports
import functools
import warnings


# TODO message
# TODO version parameters, deprecated_since, removed-in, etc.
# TODO invocation file, line
def deprecated(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        # save and restore warnings filter
        with warnings.catch_warnings():
            # enable warnings filter for DeprecationWarning
            # it's enabled by default, but this ensures it works
            warnings.simplefilter("always", DeprecationWarning)

            # warnings module is preferrable to logging module for the problems
            # that stem from incorrect implementation (not runtime problems)
            warnings.warn(f"deprecated: {func.__name__}", category=DeprecationWarning, stacklevel=2)

        # evaluate the wrapped function
        return func(*args, **kwargs)

    # return the decorated function
    return wrapped_func


def main():
    """simple test"""

    # capture `warnings` messages into `logging` messages
    import logging

    logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-8s %(message)s", level=logging.DEBUG)
    logging.captureWarnings(True)

    # declare deprecated function
    @deprecated
    def deprecated_func():
        return None

    # call deprecated function to show warning and log message
    deprecated_func()


if __name__ == "__main__":
    main()
