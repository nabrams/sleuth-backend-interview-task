from typing import Any

DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default
