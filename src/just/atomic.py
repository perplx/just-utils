"""FIXME"""

import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryFile


@contextmanager
def atomic_open(file_path: Path | str, mode: str):
    if isinstance(file_path, str):
        file_path = Path(file_path)

    temp_dir_path = file_path.parent
    with TemporaryFile(dir=temp_dir_path, mode=mode) as temp_file:
        yield from temp_file

    os.replace(temp_file.name, file_path)


def main():
    """Simple test"""

    test_file_path = Path(os.getcwd()) / "test_file.txt"
    with atomic_open(test_file_path, "wt"):
        atomic_open.write("test!")


if __name__ == "__main__":
    main()


