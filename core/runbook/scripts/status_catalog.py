"""Shared Run Book status definitions and helpers."""

from dataclasses import dataclass
import json
from typing import Any, Dict


@dataclass(frozen=True)
class StatusDefinition:
    """Display and summary behavior for one Oracle Fusion task status."""

    display: str
    complete: bool


STATUS_DEFINITIONS: Dict[str, StatusDefinition] = {
    "INI": StatusDefinition("Not Started", False),
    "INP": StatusDefinition("In Progress", False),
    "RFR": StatusDefinition("Ready for Review", False),
    "DEP": StatusDefinition("Dependent", False),
    "COM": StatusDefinition("Completed", True),
    "CWE": StatusDefinition("Completed with Exceptions", True),
    "TOH": StatusDefinition("Error", False),
    "REJ": StatusDefinition("Not Applicable", True),
}

UPDATE_STATUS_CODES = {
    "open": "INI",
    "in-progress": "INP",
    "ready-for-review": "RFR",
    "completed": "COM",
    "rejected": "REJ",
    "not-applicable": "REJ",
}


def normalize_status(value: Any) -> str:
    """Return an Oracle Fusion status as a trimmed uppercase code."""

    return str(value or "").strip().upper()


def display_status(value: Any) -> str:
    """Return the agreed display label without discarding unknown codes."""

    code = normalize_status(value)
    definition = STATUS_DEFINITIONS.get(code)
    if definition:
        return definition.display
    return code or "Unknown"


def is_complete(value: Any) -> bool:
    """Return whether a status counts as completed."""

    definition = STATUS_DEFINITIONS.get(normalize_status(value))
    return bool(definition and definition.complete)


def update_code(alias: str) -> str:
    """Map a supported user-facing update alias to its Oracle Fusion code."""

    return UPDATE_STATUS_CODES[alias]


def safe_unknown_label(value: Any) -> str:
    """Escape control characters before displaying an unknown status."""

    code = normalize_status(value) or "missing"
    return json.dumps(code, ensure_ascii=False)[1:-1]
