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
    """Lock-file context-manager."""

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
