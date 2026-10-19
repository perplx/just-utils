"""Format and parse quantities in human-readable formats."""

# standard imports
import datetime
import logging

logger = logging.getLogger(__name__)


IEC_UNITS = [
    "B",
    "KiB",  # kibibyte 1024^1
    "MiB",  # mebibyte 1024^2
    "GiB",  # gibibyte 1024^3
    "TiB",  # tebibyte 1024^4
    "PiB",  # pebibyte 1024^5
    "EiB",  # exbibyte 1024^6
    "ZiB",  # zebibyte 1024^7
    "YiB",  # yobibyte 1024^8
]

LS_UNITS = ["B", "K", "M", "G", "T", "P", "E", "Z", "Y"]


def _find_blocks(num_bytes: int, block_size: int) -> tuple[float, int]:
    if num_bytes < 0:
        raise ValueError("num_bytes {num_bytes} should be positive")
    num_blocks = 0
    while num_bytes >= block_size:
        num_bytes /= block_size
        num_blocks += 1
    return num_bytes, num_blocks


def format_bytes(num_bytes: int) -> str:
    """Format a number of bytes `num_bytes` as a human-readable `str`.

    ex::

        >>> format_bytes(0)
        '0B'
        >>> format_bytes(1)
        '1B'
        >>> format_bytes(10)
        '10B'
        >>> format_bytes(100)
        '100B'
        >>> format_bytes(1000)
        '1000B'
        >>> format_bytes(1024)
        '1.0K'
        >>> format_bytes(1024 * 1024)
        '1.0M'
    """
    if num_bytes < 0:
        raise ValueError("num_bytes {num_bytes} should be positive")
    num_bytes, num_blocks = _find_blocks(num_bytes, 1024)
    if num_bytes < 100.0 and num_blocks > 0:
        bytes_str = f"{num_bytes:.1f}"
    else:
        bytes_str = f"{num_bytes:.0f}"
    return f"{bytes_str}{LS_UNITS[num_blocks]}"


def parse_bytes(num_bytes: str) -> int:
    """Parse a human-readable `num_bytes` as a `int`."""
    value_str = num_bytes[:-1]
    unit_str = num_bytes[-1]
    unit_pos = LS_UNITS.index(unit_str)
    unit_mul = 1024**unit_pos
    value_num = float(value_str)
    return value_num * unit_mul


def format_duration(num_seconds: float) -> str:
    """Format a duraton `num_seconds` as a human-readable `str`."""

    minutes, seconds = divmod(num_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds:
        parts.append(f"{seconds}s")

    logger.debug(parts)

    return " ".join(parts)


def parse_duration(duration: str) -> int:
    """Parse a human-readable `duration` to a number of seconds."""

    parts = duration.split()

    days = 0
    hours = 0
    minutes = 0
    seconds = 0

    for part in parts:
        if part.endswith("d"):
            days = int(part[:-1])
        if part.endswith("h"):
            hours = int(part[:-1])
        if part.endswith("m"):
            minutes = int(part[:-1])
        if part.endswith("s"):
            seconds = int(part[:-1])

    total_seconds = 0
    total_seconds += days * 24 * 60 * 60
    total_seconds += hours * 60 * 60
    total_seconds += minutes * 60
    total_seconds += seconds

    return total_seconds


def main() -> None:
    """Simple test."""

    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=logging.NOTSET)

    TESTS = [
        0,
        1,
        10,
        100,
        1000,
        1023,
        1024,
        1024 * 20,
        1024 * 300,
        (1024**2) - 100,  # FIXME returns '1024K'
        (1024**2) - 1,  # FIXME returns '1024K'
        (1024**2) + 1,  # FIXME returns '1024K'
        (1024**2) + 1,  # FIXME returns '1024K'
        1024**2,
        1024**3,
        1024**4,
        1024**5,
    ]
    for num_bytes in TESTS:
        print(f"{format_bytes(num_bytes):>5} {num_bytes:>16}")

    raise SystemExit

    seconds = 100_000
    print(seconds)
    duration_str = format_duration(seconds)
    print(duration_str)
    duration_secs = parse_duration(duration_str)
    print(duration_secs)


if __name__ == "__main__":
    main()
