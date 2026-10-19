#!/usr/bin/env python3
"""Validate the Adaptive Search publish contract before payload mapping."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_CONTRACT = Path(__file__).resolve().parents[1] / "ora-resource" / "ora_publish_contract.json"
EXPECTED = {
    "contract_id": "adaptive-search-selective-or-full-publish-v3",
    "method": "POST",
    "path": "/crmRestApi/searchResources/latest/custom-actions/queries/publish",
    "content_type": "application/json",
    "required_headers": {"Preference": "transient"},
}


def _error(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def _schema_is_selective(schema: Any) -> bool:
    return isinstance(schema, dict) and (
        schema.get("required") == ["entities", "publishType"]
        and schema.get("additionalProperties") is False
        and schema.get("properties", {}).get("publishType", {}).get("const") == "selective"
        and schema.get("properties", {}).get("entities", {}).get("type") == "array"
        and schema.get("properties", {}).get("entities", {}).get("minItems") == 1
        and schema.get("properties", {}).get("entities", {}).get("items", {}).get("type") == "string"
        and schema.get("properties", {}).get("entities", {}).get("items", {}).get("minLength") == 1
    )


def _schema_is_full(schema: Any) -> bool:
    return isinstance(schema, dict) and (
        schema.get("required") == ["entities"]
        and schema.get("additionalProperties") is False
        and schema.get("properties", {}).get("entities", {}).get("type") == "array"
        and schema.get("properties", {}).get("entities", {}).get("minItems") == 1
        and schema.get("properties", {}).get("entities", {}).get("items", {}).get("type") == "string"
        and schema.get("properties", {}).get("entities", {}).get("items", {}).get("minLength") == 1
        and "publishType" not in schema.get("properties", {})
    )


def validate(contract: Any) -> tuple[list[str], dict[str, Any] | None]:
    errors: list[str] = []
    _error(errors, isinstance(contract, dict), "Contract must be a JSON object.")
    if not isinstance(contract, dict):
        return errors, None
    for key, value in EXPECTED.items():
        _error(errors, contract.get(key) == value, f"Contract field {key!r} is invalid.")
    request_schema = contract.get("request_schema")
    schemas = request_schema.get("oneOf") if isinstance(request_schema, dict) else None
    _error(errors, isinstance(schemas, list) and len(schemas) == 2, "Contract must define exactly selective and full payload schemas.")
    if isinstance(schemas, list) and len(schemas) == 2:
        _error(errors, _schema_is_selective(schemas[0]), "Selective Publish schema is invalid.")
        _error(errors, _schema_is_full(schemas[1]), "Full Publish schema is invalid.")
    if errors:
        return errors, None
    return errors, {
        "contractId": contract["contract_id"],
        "method": contract["method"],
        "path": contract["path"],
        "contentType": contract["content_type"],
        "requiredHeaders": contract["required_headers"],
        "publishModes": ["selective", "full"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable validation result.")
    args = parser.parse_args()
    try:
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors, binding = [f"Contract cannot be read as JSON: {exc}"], None
    else:
        errors, binding = validate(contract)
    result = {"valid": not errors, "errors": errors, "contractBinding": binding}
    if args.json:
        print(json.dumps(result, sort_keys=True))
    elif errors:
        print("Contract validation failed: " + "; ".join(errors))
    else:
        print("Adaptive Search publish contract is valid.")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
