"""Write a file atomically."""

import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Any, Generator, IO, Union


# FIXME add @overload for type annotations binary or text
# FIXME add parametrized `open`-like function?
# FIXME POSIX 0o600 permissions.
# FIXME A failed unlink hides the real error (use contextlib.suppress(OSError)).
# FIXME No encoding or newline passthrough.
# FIXME No temp file prefix/suffix.
# FIXME The module docstring is still """FIXME""".
# FIXME The test docstrings end in # FIXME.
# FIXME No tests for overwriting an existing file, binary writes, or a str path.
@contextmanager
def atomic_open(file_path: Union[Path, str], mode: str) -> Generator[IO[Any], None, None]:
    """Open the file atomically, so that the file only appears once it's closed.
    Open a temporary-file in the same directory as the `file_path`, and once that file is closed,
    move the temp-file to `file_path`. The mode must include "w", otherwise a `ValueError` is raised.
    Calls `os.fsync` on the file to ensure it is written to disk.

    ex::

        >>> import tempfile
        >>> with tempfile.TemporaryDirectory() as tmp:
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
        ['config.txt']

    :param file_path: the path of the file to open.
    :param mode: file modes, must include "w".
    :return: the open file-like object, pointing to the temporary file.
    :raise ValueError: when given a mode that doesn't contain "w".
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    # ensure mode has "w"
    if "w" not in mode:
        raise ValueError(f"mode {mode!r} not supported, must include 'w'")

    # create temp file in the same directory as the file path
    temp_dir_path = file_path.parent
    with NamedTemporaryFile(dir=temp_dir_path, mode=mode, delete=False) as temp_file:
        try:
            yield temp_file
            # ensure file is written to disk, unless file was closed by caller
            if not temp_file.closed:
                temp_file.flush()
                os.fsync(temp_file.fileno())
        except BaseException:
            # ensure file is deleted on an exception
            temp_file.close()
            os.unlink(temp_file.name)
            raise

    # move the temp-file to the file path, clean up temp file when move fails
    try:
        os.replace(temp_file.name, file_path)
    except BaseException:
        os.unlink(temp_file.name)
        raise


def main() -> None:
    """Simple test"""

    with TemporaryDirectory() as temp_dir:
        test_file_path = Path(temp_dir) / "test_file.txt"
        with atomic_open(test_file_path, "wt") as output_file:
            output_file.write("test!")


if __name__ == "__main__":
    main()
