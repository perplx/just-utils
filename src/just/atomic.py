"""FIXME"""

import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Generator, IO, Union


# FIXME add @overload for type annotations binary or text
# FIXME add parametrized `open`-like function?
@contextmanager
def atomic_open(file_path: Union[Path, str], mode: str) -> Generator[IO[Any], None, None]:
    """Open the file atomically, so that the file only appears once it's closed.
    Open a temporary-file in the same directory as the `file_path`, and once that file is closed,
    move the temp-file to `filepath`.

    ex::

        >>> import os
        >>> import tempfile
        >>> with tempfile.TemporaryDirectory() as tmp:  # doctest: +ELLIPSIS
        ...     path = Path(tmp) / "config.txt"
        ...     with atomic_open(path, "w") as f:
        ...         _ = f.write("version 1\\n")
        ...         print(path.exists())          # not visible until closed
        ...     try:
        ...         with atomic_open(path, "w") as f:
        ...             _ = f.write("version 2, half-wri")
        ...             raise RuntimeError("crash mid-write")
        ...     except RuntimeError:
        ...         pass
        ...     print(path.read_text(), end="")   # the failed write left it intact
        ...     print(os.listdir(tmp))            # and no temp-file left behind
        False
        version 1
        [...]

    :param file_path: the path of the file to open
    :param mode: FIXME describe this!
    :return: the open file-like object, pointing to the temporary file.
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    temp_dir_path = file_path.parent
    with NamedTemporaryFile(dir=temp_dir_path, mode=mode, delete=False) as temp_file:
        yield temp_file

    os.replace(temp_file.name, file_path)


def main():
    """Simple test"""

    # FIXME use tempfile
    test_file_path = Path(os.getcwd()) / "test_file.txt"
    with atomic_open(test_file_path, "wt") as output_file:
        output_file.write("test!")


if __name__ == "__main__":
    main()
