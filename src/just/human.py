"""FIXME"""

# standard imports
import datetime
import logging


logger = logging.getLogger(__name__)


def format_bytes(num_bytes: int) -> str:
    raise NotImplementedError


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

    seconds = 100_000
    print(seconds)
    duration_str = format_duration(seconds)
    print(duration_str)
    duration_secs = parse_duration(duration_str)
    print(duration_secs)


if __name__ == "__main__":
    main()
