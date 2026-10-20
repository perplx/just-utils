#!/usr/bin/env python3

"""Open files transparently whether or not they are compressed."""

# standard imports
import bz2
import gzip
import lzma
import os
from pathlib import Path
from typing import Any, IO, Union


# FIXME add @overload for type annotations binary or text
def ezopen(file_path: Union[Path, str], mode: str = "r") -> IO[Any]:
    """Open a file whether it's compressed or not.
    Open archive files using the appropriate compression based on the file extension.
    Open file normally if no extension matches.
    Supports .bz2 .gz and .xz file-extensions.

    :param file_path: the path to the file being opened.
    :param mode: the mode-string for opening the file.
    :return: the opened file-object.

    ex::

        >>> ezopen("./tests/data/test_data.txt", mode="rt").read()
        'test\\n'
        >>> ezopen("./tests/data/test_data.txt.gz", mode="rt").read()
        'test\\n'
        >>> ezopen("./tests/data/test_data.txt.bz2", mode="rt").read()
        'test\\n'
        >>> ezopen("./tests/data/test_data.txt.xz", mode="rt").read()
        'test\\n'
    """

    # support Path objects
    file_path = os.fspath(file_path)  # PathLike -> str

    # open compressed files based on their extensions
    if file_path.endswith(".bz2"):
        return bz2.open(file_path, mode=mode)
    if file_path.endswith(".gz"):
        return gzip.open(file_path, mode=mode)
    if file_path.endswith(".xz"):
        return lzma.open(file_path, mode=mode)

    # open file normally
    return open(file_path, mode=mode)


def main() -> None:
    """Simple test."""

    # test data
    text_file_path = Path("./tests/data/test_data.txt").absolute()
    bz2_file_path = Path("./tests/data/test_data.txt.bz2").absolute()
    gz_file_path = Path("./tests/data/test_data.txt.gz").absolute()
    xz_file_path = Path("./tests/data/test_data.txt.xz").absolute()

    # test each case
    with ezopen(text_file_path, "rt") as text_file:
        print(text_file.read())
    with ezopen(bz2_file_path, "rt") as bz2_file:
        print(bz2_file.read())
    with ezopen(gz_file_path, "rt") as gz_file:
        print(gz_file.read())
    with ezopen(xz_file_path, "rt") as xz_file:
        print(xz_file.read())


if __name__ == "__main__":
    main()
