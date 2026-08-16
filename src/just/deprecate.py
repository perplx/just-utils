#!/usr/bin/env python3

"""Deprecation decorator"""


# standard imports
import functools
import warnings
from typing import Callable


def deprecated(arg=None, since=None):  # FIXME return type annotation?
    """Decorator to mark a function as deprecated.
    Emit ``DeprecationWarning`` when a decorated function is called.

    ex::

        The warning goes to stderr, so the examples below capture it with
        ``warnings.catch_warnings(record=True)`` rather than printing it.

        >>> import warnings

        without parentheses

        >>> @deprecated
        ... def deprecated_func_1():
        ...     return None
        >>> with warnings.catch_warnings(record=True) as caught:
        ...     warnings.simplefilter("always")
        ...     deprecated_func_1()
        >>> caught[0].category.__name__
        'DeprecationWarning'
        >>> str(caught[0].message)
        'deprecated: deprecated_func_1'

        with parentheses

        >>> @deprecated()
        ... def deprecated_func_2():
        ...     return None
        >>> with warnings.catch_warnings(record=True) as caught:
        ...     warnings.simplefilter("always")
        ...     deprecated_func_2()
        >>> str(caught[0].message)
        'deprecated: deprecated_func_2'

        with a version

        >>> @deprecated(since="0.3")
        ... def deprecated_func_3():
        ...     return None
        >>> with warnings.catch_warnings(record=True) as caught:
        ...     warnings.simplefilter("always")
        ...     deprecated_func_3()
        >>> str(caught[0].message)
        'deprecated: deprecated_func_3 (since version: 0.3)'
    """

    def decorator(func: Callable):
        # preserve the metadata (name, docstring, etc.) of the wrapped function
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # save and restore warnings filter
            with warnings.catch_warnings():
                # enable warnings filter for DeprecationWarning
                # it should be enabled by default, but this ensures it works
                warnings.simplefilter("always", DeprecationWarning)

                # make the deprecation message
                message = f"deprecated: {func.__name__}"
                if since:
                    message += f" (since version: {since})"

                # warnings module is preferrable to logging module for the problems
                # that stem from incorrect implementation (not runtime problems)
                # stacklevel=2 shows the call to deprecated function on the stack
                warnings.warn(message, category=DeprecationWarning, stacklevel=2)

            # evaluate the wrapped function
            return func(*args, **kwargs)

        return wrapper

    # make it work with or without parentheses
    # see: https://stackoverflow.com/a/35572746
    if callable(arg):
        return decorator(arg)  # return 'wrapper'
    else:
        return decorator  # ... or 'decorator'


def main() -> None:
    """Simple test."""

    # capture `warnings` messages into `logging` messages
    import logging

    # configure logging to capture warnings
    logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-8s %(message)s", level=logging.DEBUG)
    logging.captureWarnings(True)

    # declare deprecated function without parentheses
    @deprecated
    def deprecated_func_1():
        return None

    # declare deprecated function with parentheses
    @deprecated()
    def deprecated_func_2():
        return None

    # declare deprecated function with parameters
    @deprecated(since="0.3")
    def deprecated_func_3():
        return None

    # call deprecated function to show warning and log message
    deprecated_func_1()
    deprecated_func_2()
    deprecated_func_3()


if __name__ == "__main__":
    main()
