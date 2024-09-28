#!/usr/bin/env python3

import bz2
import gzip
import os


def ezopen(file_path: str, mode: str = ""):
    if file_path.endswith(".bz2"):
        return bz2.open(file_path, mode=mode)
    if file_path.endswith(".gz"):
        return gzip.open(file_path, mode=mode)

    return open(file_path, mode=mode)


def main() -> None:
    text_file_path = os.path.abspath("./data/test_data.txt")
    bz2_file_path = os.path.abspath("./data/test_data.txt.bz2")
    gz_file_path = os.path.abspath("./data/test_data.txt.gz")

    with ezopen(text_file_path, "rt") as text_file:
        print(text_file.read())
    with ezopen(bz2_file_path, "rt") as bz2_file:
        print(bz2_file.read())
    with ezopen(gz_file_path, "rt") as gz_file:
        print(gz_file.read())


if __name__ == "__main__":
    main()
