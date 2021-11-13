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
        # TODO validate format?
        self.format = format_str

    def __call__(self, date_str):
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
             raise argparse.ArgumentTypeError("mode %s of type %s not recognized; should be str" % (repr(mode), mode.__class__.__name__))
        ALLOWED_MODES = ["r", "w"] # TODO other modes? "x"?
        for m in mode:
            if m not in ALLOWED_MODES:
                raise argparse.ArgumentTypeError("mode \"%s\" not recognized; should be one of: %s" % (m, ALLOWED_MODES) )

        # store mode
        self.mode = mode 

        # TODO normalize mode?
        # self.mode = "".join(sorted(set(mode)))

    def __call__(self, dir_path):
        """check dir_path is a directory that satisfies DirectoryArg.mode """
        # TODO create non-existent directory?
        if not os.path.exists(dir_path):
            raise argparse.ArgumentTypeError("dir-path \"%s\" does not exist!" % dir_path)
        if not os.path.isdir(dir_path):
            raise argparse.ArgumentTypeError("dir-path \"%s\" is not a directory!" % dir_path)
        if "r" in self.mode and not os.access(dir_path, os.R_OK):
            raise argparse.ArgumentTypeError("dir-path \"%s\" cannot be read!" % dir_path)
        if "w" in self.mode and not os.access(dir_path, os.W_OK):
            raise argparse.ArgumentTypeError("dir-path \"%s\" cannot be written!" % dir_path)

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

    # get the constant with the given name in upper-case from the logging module
    # e.g. "debug" becomes logging.DEBUG
    log_level = getattr(logging, log_level_name.upper(), None)
    if log_level is None:
        raise argparse.ArgumentTypeError("unrecognized log-level name: \"%s\"" % log_level_name)
    return log_level


def main():
    """simple test"""

    # define command-line parameters to test
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--date-time", type=DateTimeArg("%Y-%m-%d %H:%M:%S.%f"))
    arg_parser.add_argument("--directory", type=DirectoryArg("rw"))
    arg_parser.add_argument("--log-level", type=LogLevelArg)

    # test the new command-line parameter-types with these:
    TEST_ARGS = [
        "--date-time", "2020-02-29 12:34:56.789",
        "--directory", ".",
        "--log-level", "DEBUG"
    ]
    args = arg_parser.parse_args(TEST_ARGS)
    print(args)


if __name__ == "__main__":
    main()
