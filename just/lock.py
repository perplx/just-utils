#!/usr/bin/env python3

"""Lock-file"""


# standard imports
import contextlib
import logging
import os


# global logger
logger = logging.getLogger(__name__)


@contextlib.contextmanager
def lock_file(file_path: str):

    logger.debug("opening lock-file %r", file_path)

    try:
        with open(file_path, mode="x"):
            yield
    except FileExistsError as e:
        logger.critical("lock-file %r already exists!", file_path)
        raise

    logger.debug("closing lock-file %r", file_path)
    os.unlink(file_path)


def main() -> None:
    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=logging.NOTSET)
    with lock_file("a"):
        with lock_file("a"):
            print("bad...")


if __name__ == "__main__":
    main()
