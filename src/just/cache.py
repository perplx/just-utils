"""FIXME"""


import logging


logger = logging.getLogger(__name__)


def memoize(func):
    cache = dict()

    def wrapped_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapped_func


def main():
    """Simple test."""

    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s")

    @memoize
    def test_func():
        import time
        time.sleep(1)

    for i in range(5):
        logger.warning("test %d", i+1)
        test_func()


if __name__ == "__main__":
    main()
