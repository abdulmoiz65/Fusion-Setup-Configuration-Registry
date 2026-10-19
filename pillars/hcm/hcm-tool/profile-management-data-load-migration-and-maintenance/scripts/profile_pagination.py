"""Validate paginated read-only Fusion responses for this skill only."""

from __future__ import annotations

from typing import Any, Callable


def validated_page(
    response: Any,
    *,
    offset: int,
    label: str,
    stage: str,
    data_load_error: Callable[..., Exception],
) -> tuple[list[Any], bool]:
    """Return a validated Fusion response page without extending Core's API."""
    if not isinstance(response, dict):
        raise data_load_error(stage, f"{label} returned a malformed response object.")
    items = response.get("items")
    has_more = response.get("hasMore")
    if not isinstance(items, list) or not isinstance(has_more, bool):
        raise data_load_error(
            stage,
            f"{label} response must contain an items array and boolean hasMore value.",
            response={"offset": offset},
        )
    return items, has_more
