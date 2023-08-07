#!/usr/bin/env python3

"""Argument-parsers for argparse"""


# standard imports
import argparse
import datetime
import logging
import os


class DateTimeArg:
    """Type parser for datetime strings for argparse.ArgumentParser.

    ex::

        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("--date-time", type=DateTimeArg("%Y-%m-%d %H:%M:%S.%f"))
        arg_parser.parse_args(["--date-time", "2020-02-29 12:34:56.789"])
    """

    def __init__(self, format_str: str):
        # TODO validate format?
        self.format = format_str

    def __call__(self, date_str: str) -> datetime.datetime:
        """Create a datetime.datetime obj from the command-line arg string"""
        try:
            return datetime.datetime.strptime(date_str, self.format)
        except ValueError as e:
            raise argparse.ArgumentTypeError(e)


# FIXME what about the path module? would that work intead?
class DirectoryArg:
    """Type parser for directory paths for argparse.ArgumentParser.
    Checks if path is directory, has given mode ("r", "w", "rw")

    ex::

        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("--directory", type=DirectoryArg("rw"))
        arg_parser.parse_args(["--directory", "."])
    """

    def __init__(self, mode: str):
        # validate mode
        if not isinstance(mode, str):
            raise argparse.ArgumentTypeError(f"mode {repr(mode)} of type {type(mode)} not recognized; should be {str}")
        ALLOWED_MODES = ["r", "w"]  # TODO other modes? "x"?
        for m in mode:
            if m not in ALLOWED_MODES:
                raise argparse.ArgumentTypeError(f"mode {m} not recognized; should be one of: {ALLOWED_MODES}")

        # store mode after normalization
        self.mode = "".join(sorted(set(mode)))

        # log mode being normalized
        if len(self.mode) != len(mode):
            logger = logging.getLogger(__name__)
            logger.warning("log-level arg %r normalized to %r", mode, self.mode)

    def __call__(self, dir_path: str) -> str:
        """check dir_path is a directory that satisfies DirectoryArg.mode"""
        # TODO create non-existent directory?
        if not os.path.exists(dir_path):
            raise argparse.ArgumentTypeError(f"dir-path {repr(dir_path)} does not exist!")
        if not os.path.isdir(dir_path):
            raise argparse.ArgumentTypeError(f"dir-path {repr(dir_path)} is not a directory!")
        if "r" in self.mode and not os.access(dir_path, os.R_OK):
            raise argparse.ArgumentTypeError(f"dir-path {repr(dir_path)} cannot be read!")
        if "w" in self.mode and not os.access(dir_path, os.W_OK):
            raise argparse.ArgumentTypeError(f"dir-path {repr(dir_path)} cannot be written!")

        return dir_path


def LogLevelArg(level_name: str) -> int:
    """Translate a log-level name to its actual integer representation.
    Supports any log-level name in a case-insensitive fashion, including aliases
    (i.e. "debug" -> ``DEBUG``, "warn" -> ``WARNING``, "fatal" -> ``CRITICAL``).
    Can be used as the value for the `type` parameter of an argument in
    `argparse.ArgumentParser`, enabling parameters like `--log-level FATAL`.
    Will raise an `argparse.ArgumentTypeError` for unsupported values, so that
    `argparse` will show useful error-messages to the user on the command-line.

    ex::

        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("--log-level", type=LogLevelArg)
        arg_parser.parse_args(["--log-level", "DEBUG"])

    :param level_name: any supported log-level name from the `logging` module.
    :raise argparse.ArgumentTypeError: for an unsupported value to `argparse`
    :return: the log-level int corresponfding to the log-level name str.
    """

    # preconditions
    assert isinstance(level_name, str)

    try:
        return logging._nameToLevel[level_name.upper()]
    except KeyError:
        level_names = ",".join(logging._nameToLevel.keys())
        raise argparse.ArgumentTypeError(f"unrecognized level-name {level_name}, should be one of: {level_names}")


def main() -> None:
    """Simple test"""

    # define command-line parameters to test
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument("--date-time", type=DateTimeArg("%Y-%m-%d %H:%M:%S.%f"))
    arg_parser.add_argument("--directory", type=DirectoryArg("rw"))
    arg_parser.add_argument("--log-level", type=LogLevelArg)

    # print command-line help
    arg_parser.print_help()
    print()

    # test the new command-line parameter-types with these:
    # fmt: off
    TEST_ARGS = [
        "--date-time", "2020-02-29 12:34:56.789",
        "--directory", ".",
        "--log-level", "DEBUG"
    ]
    # fmt: on
    args = arg_parser.parse_args(TEST_ARGS)
    print("args:", args)


if __name__ == "__main__":
    main()
