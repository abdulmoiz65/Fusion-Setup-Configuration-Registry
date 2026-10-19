#!/usr/bin/env python3
"""Performance Library Goal wrapper for the shared safe create contract."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


COMMON = Path(__file__).resolve().parents[3] / "goal-management-common" / "scripts" / "library_goal_create_payload.py"
SPEC = importlib.util.spec_from_file_location("goal_management_library_goal_create", COMMON)
assert SPEC and SPEC.loader
_SHARED = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(_SHARED)

PayloadValidationError = _SHARED.PayloadValidationError
attributes = _SHARED.attributes
external_id_suggestion = _SHARED.external_id_suggestion
has_default_value_expression = _SHARED.has_default_value_expression
uses_server_external_id_derivation = _SHARED.uses_server_external_id_derivation
approval_is_current = _SHARED.approval_is_current
verify_created_goal = _SHARED.verify_created_goal
classify_existing_goal = _SHARED.classify_existing_goal
def build_update_execution_preview(operations, **kwargs):
    for operation in operations:
        if operation.get("row", {}).get("TypeCode") != "PERFORMANCE":
            raise PayloadValidationError("Selected Library Goal belongs to a different variant")
    return _SHARED.build_update_execution_preview(operations, **kwargs)


def build_status_update_preview(row, **kwargs):
    if row.get("TypeCode") != "PERFORMANCE":
        raise PayloadValidationError("Selected Library Goal belongs to a different variant")
    return _SHARED.build_status_update_preview(row, **kwargs)


def prepare_create_payload(
    payload: dict[str, Any], metadata: dict[str, Any], *, allow_active_create: bool = False
) -> dict[str, Any]:
    return _SHARED.prepare_create_payload(
        payload, metadata, variant="PERFORMANCE", allow_active_create=allow_active_create
    )


def validate_create(
    payload: dict[str, Any], metadata: dict[str, Any], *, duplicate_risk_acknowledged: bool = False
) -> list[dict[str, str]]:
    return _SHARED.validate_create(
        payload,
        metadata,
        variant="PERFORMANCE",
        duplicate_risk_acknowledged=duplicate_risk_acknowledged,
    )


def approval_preview(
    payload: dict[str, Any], environment: str, metadata: dict[str, Any],
    *, duplicate_risk_acknowledged: bool = False, request_path: str = "/libraryGoals",
    allow_active_create: bool = False,
) -> dict[str, Any]:
    return _SHARED.approval_preview(
        payload, environment, variant="PERFORMANCE", metadata=metadata,
        duplicate_risk_acknowledged=duplicate_risk_acknowledged,
        request_path=request_path,
        allow_active_create=allow_active_create,
    )


def main() -> int:
    return _SHARED.main(variant="PERFORMANCE")


if __name__ == "__main__":
    raise SystemExit(main())
