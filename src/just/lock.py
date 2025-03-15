#!/usr/bin/env python3

"""Lock-file"""


# standard imports
import contextlib
import logging
import os


# global logger
logger = logging.getLogger(__name__)


class LockFileExistsError(FileExistsError):
    pass


@contextlib.contextmanager
def lock_file(file_path: str):
    """Lock-file context-manager. Defines a scope of code protected by a lock-file.
    The lock-file at the given path is created when entering the context, and deleted when exiting the context.
    The context can only be entered if the lock-file does not already exist.

    ex::

        with lock_file("/tmp/example.lock"):
            # ensure that only one process can call `access_something_sensitive()`
            access_something_sensitive()

    :param file_path: the path to the lock-file.
    :raise LockFileExistsError: when the lock-file already exists
    :return: a ``ContextManager``
    """

    logger.debug("opening lock-file %r", file_path)
    try:
        open(file_path, mode="x").close()  # create the empty lock-file
    except FileExistsError as e:
        logger.critical("lock-file %r already exists!", file_path)
        raise LockFileExistsError(e)

    try:
        yield
    except Exception as e:
        logger.debug("exiting lock-file %r on error %r", file_path, e)
        raise
    else:
        logger.debug("exiting lock-file %r normally", file_path)
        pass
    finally:
        os.unlink(file_path)
        logger.debug("removed lock-file %r", file_path)


def main() -> None:
    """Simple test."""

    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=logging.NOTSET)

    LOCK_FILE_PATH = "LOCK_FILE"
    logger.debug("lock-file exists: %s", os.path.isfile(LOCK_FILE_PATH))

    with lock_file(LOCK_FILE_PATH):
        try:
            with lock_file(LOCK_FILE_PATH):
                pass
        except LockFileExistsError:
            logger.info("file %r was locked!", LOCK_FILE_PATH)


if __name__ == "__main__":
    main()
