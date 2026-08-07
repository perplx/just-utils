"""FIXME"""

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


def find_blocks(num_bytes: int, block_size: int) -> tuple[float, int]:
    if num_bytes < 0:
        raise ValueError("num_bytes {num_bytes} should be positive")
    num_blocks = 0
    while num_bytes >= block_size:
        num_bytes /= block_size
        num_blocks += 1
    return num_bytes, num_blocks


def format_bytes(num_bytes: int) -> str:
    if num_bytes < 0:
        raise ValueError("num_bytes {num_bytes} should be positive")
    num_bytes, num_blocks = find_blocks(num_bytes, 1024)
    if num_bytes < 10.0:
        bytes_str = f"{num_bytes:.1f}"
    else:
        bytes_str = f"{num_bytes:.0f}"
    return f"{bytes_str}{LS_UNITS[num_blocks]}"


def parse_bytes(num_bytes: str) -> int:
    raise NotImplementedError


def format_duration(num_seconds: float) -> str:
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

    print(format_bytes(1023))
    print(format_bytes(1024))
    print(format_bytes(1023 * 1024))
    print(format_bytes(1024 * 1024))

    raise SystemExit

    seconds = 100_000
    print(seconds)
    duration_str = format_duration(seconds)
    print(duration_str)
    duration_secs = parse_duration(duration_str)
    print(duration_secs)


if __name__ == "__main__":
    main()
