"""Shared validation for Run Book numeric identifiers."""

from typing import Any


MAX_INT64 = (1 << 63) - 1


def positive_int64(value: Any, field: str) -> int:
    """Return a positive signed 64-bit integer or raise ValueError."""

    if isinstance(value, bool):
        raise ValueError(f"{field} must be a positive 64-bit integer.")
    if isinstance(value, int):
        normalized = value
    elif isinstance(value, str) and value.isascii() and value.isdigit():
        normalized = int(value)
    else:
        raise ValueError(f"{field} must be a positive 64-bit integer.")
    if normalized < 1 or normalized > MAX_INT64:
        raise ValueError(f"{field} must be a positive 64-bit integer.")
    return normalized
