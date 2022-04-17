#!/usr/bin/env python3

"""Some argument-parsers for argparse."""


# standard imports
import argparse
import datetime
import logging
import os


class DateTimeArg():
    """Type parser for directory paths for argparse.ArgumentParser.
    Checks if path is directory, has given mode ("r", "w", "rw")
    ex:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--date-time", type=DateTimeArg("%Y-%m-%d %H:%M:%S.%f"))
    arg_parser.parse_args(["--date-time", "2020-02-29 12:34:56.789"])
    """

    def __init__(self, format_str):
        """Prepare to parse with the format format_str"""
        # TODO validate format?
        self.format = format_str

    def __call__(self, date_str):
        """Create a datetime.datetime obj from the command-line arg string"""
        try:
            return datetime.datetime.strptime(date_str, self.format)
        except ValueError as e:
            raise argparse.ArgumentTypeError(e)


# FIXME what about the path module? would that work intead?
class DirectoryArg():
    """Type parser for directory paths for argparse.ArgumentParser.
    Checks if path is directory, has given mode ("r", "w", "rw")
    ex:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--directory", type=DirectoryArg("rw"))
    arg_parser.parse_args(["--directory", "."])
    """

    def __init__(self, mode):
        # validate mode
        if not isinstance(mode, str):
             raise argparse.ArgumentTypeError(f"mode {repr(mode)} of type {type(mode)} not recognized; should be {str}")
        ALLOWED_MODES = ["r", "w"] # TODO other modes? "x"?
        for m in mode:
            if m not in ALLOWED_MODES:
                raise argparse.ArgumentTypeError(f"mode {m} not recognized; should be one of: {ALLOWED_MODES}")

        # store mode
        self.mode = mode 

        # TODO normalize mode?
        # self.mode = "".join(sorted(set(mode)))

    def __call__(self, dir_path):
        """check dir_path is a directory that satisfies DirectoryArg.mode """
        # TODO create non-existent directory?
        if not os.path.exists(dir_path):
            raise argparse.ArgumentTypeError(f"dir-path \"{dir_path}\" does not exist!")
        if not os.path.isdir(dir_path):
            raise argparse.ArgumentTypeError(f"dir-path \"{dir_path}\" is not a directory!")
        if "r" in self.mode and not os.access(dir_path, os.R_OK):
            raise argparse.ArgumentTypeError(f"dir-path \"{dir_path}\" cannot be read!")
        if "w" in self.mode and not os.access(dir_path, os.W_OK):
            raise argparse.ArgumentTypeError(f"dir-path \"{dir_path}\" cannot be written!")

        return dir_path


def LogLevelArg(log_level_name):
    """Type parser for directory paths for argparse.ArgumentParser.
    Checks if level is a log-level constant in the standard logging module,
    i.e. CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET.
    Check is case-insensitive.
    ex:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--log-level", type=LogLevelArg)
    arg_parser.parse_args(["--log-level", "DEBUG"])
    """

    # preconditions
    assert isinstance(log_level_name, str)

    # get the level for the given level-name
    try:
        return logging._nameToLevel[log_level_name.upper()]
    except KeyError:
        raise argparse.ArgumentTypeError(f"unrecognized log-level name: {repr(log_level_name)}")


def main():
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
    TEST_ARGS = [
        "--date-time", "2020-02-29 12:34:56.789",
        "--directory", ".",
        "--log-level", "DEBUG"
    ]
    args = arg_parser.parse_args(TEST_ARGS)
    print("args:", args)


if __name__ == "__main__":
    main()
