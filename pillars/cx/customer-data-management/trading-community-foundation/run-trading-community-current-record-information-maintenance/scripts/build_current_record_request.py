#!/usr/bin/env python3
"""Validate CurrentDateRecordSync parameters and build its fixed ESS payload."""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


APPLICATION = "CrmEss"
JOB_DEFINITION_ID = (
    "JobDefinition://oracle/apps/ess/cdm/foundation/parties/CurrentDateRecordSync"
)
PARAM_TYPE = "STRING"
CONTRACT_VERSION = 1

ARGUMENT_SPECS = (
    ("synchronization_type", "submit.argument1"),
    ("person_type", "submit.argument2"),
    ("from_date", "submit.argument3"),
    ("to_date", "submit.argument4"),
    ("person_numbers", "submit.argument5"),
)
CANONICAL_FIELDS = {field for field, _ in ARGUMENT_SPECS}

SYNCHRONIZATION_LABELS = {
    "ORA_PARTY_DENORM": "Party and location",
    "ORA_PERSON_SYNC": "Worker",
}
PERSON_TYPE_LABELS = {
    "EMP": "Employee",
    "CWK": "Contingent Worker",
    "PWK": "Pending Worker",
    "EX_EMP": "Ex-Employee",
    "EX_CWK": "Ex-Contingent Worker",
    "EX_PWK": "Ex-Pending Worker",
    "NONW": "Nonworker",
    "EX_NONW": "Ex-Nonworker",
    "PURGED": "Purged Worker",
}

SYNCHRONIZATION_ALIASES = {
    "party and location": "ORA_PARTY_DENORM",
    "party location": "ORA_PARTY_DENORM",
    "denormalize parties": "ORA_PARTY_DENORM",
    "worker": "ORA_PERSON_SYNC",
    "workers": "ORA_PERSON_SYNC",
    "hr persons": "ORA_PERSON_SYNC",
}
PERSON_TYPE_ALIASES = {
    "employee": "EMP",
    "contingent worker": "CWK",
    "pending worker": "PWK",
    "ex employee": "EX_EMP",
    "ex contingent worker": "EX_CWK",
    "ex pending worker": "EX_PWK",
    "nonworker": "NONW",
    "non worker": "NONW",
    "ex nonworker": "EX_NONW",
    "ex non worker": "EX_NONW",
    "purged worker": "PURGED",
}


class ContractError(ValueError):
    """Raised when canonical inputs do not satisfy the ESS contract."""


def _text(value: Any, field: str, *, required: bool = False) -> str | None:
    if value is None:
        if required:
            raise ContractError(f"Missing required field: {field}")
        return None
    if isinstance(value, bool) or isinstance(value, (dict, list)):
        raise ContractError(f"{field} must be a scalar value")
    normalized = str(value).strip()
    if not normalized:
        if required:
            raise ContractError(f"Missing required field: {field}")
        return None
    return normalized


def _alias_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def _fixed_code(
    value: Any,
    field: str,
    labels: dict[str, str],
    aliases: dict[str, str],
    *,
    required: bool = False,
) -> str | None:
    normalized = _text(value, field, required=required)
    if normalized is None:
        return None
    code = normalized.upper()
    if code in labels:
        return code
    mapped = aliases.get(_alias_key(normalized))
    if mapped is None:
        allowed = ", ".join(labels)
        raise ContractError(f"{field} must use one of these fixed codes: {allowed}")
    return mapped


def _iso_date(value: Any, field: str) -> str | None:
    normalized = _text(value, field)
    if normalized is None:
        return None
    try:
        parsed = date.fromisoformat(normalized)
    except ValueError as exc:
        raise ContractError(f"{field} must be a valid date in YYYY-MM-DD format") from exc
    if parsed.isoformat() != normalized:
        raise ContractError(f"{field} must use zero-padded YYYY-MM-DD format")
    return normalized


def _person_numbers(value: Any) -> str | None:
    normalized = _text(value, "person_numbers")
    if normalized is None:
        return None
    if ";" in normalized:
        raise ContractError(
            "person_numbers must be separated with commas or whitespace, not semicolons"
        )
    tokens = [token for token in re.split(r"[\s,]+", normalized) if token]
    if not tokens:
        raise ContractError("person_numbers must contain at least one person number")
    return ",".join(tokens)


def normalize_parameters(raw: dict[str, Any]) -> dict[str, str | None]:
    if not isinstance(raw, dict):
        raise ContractError("Canonical parameters must be a JSON object")

    unknown = sorted(set(raw) - CANONICAL_FIELDS)
    if unknown:
        raise ContractError(f"Unsupported canonical field(s): {', '.join(unknown)}")

    synchronization_type = _fixed_code(
        raw.get("synchronization_type"),
        "synchronization_type",
        SYNCHRONIZATION_LABELS,
        SYNCHRONIZATION_ALIASES,
        required=True,
    )
    person_type = _fixed_code(
        raw.get("person_type"),
        "person_type",
        PERSON_TYPE_LABELS,
        PERSON_TYPE_ALIASES,
    )
    from_date = _iso_date(raw.get("from_date"), "from_date")
    to_date = _iso_date(raw.get("to_date"), "to_date")
    person_numbers = _person_numbers(raw.get("person_numbers"))

    if (from_date is None) != (to_date is None):
        raise ContractError("from_date and to_date must both be supplied or both be blank")
    if from_date is not None and to_date is not None and from_date > to_date:
        raise ContractError("from_date cannot be later than to_date")

    assert synchronization_type is not None
    worker_filters = {
        "person_type": person_type,
        "from_date": from_date,
        "to_date": to_date,
        "person_numbers": person_numbers,
    }
    if synchronization_type == "ORA_PARTY_DENORM":
        supplied = [field for field, value in worker_filters.items() if value is not None]
        if supplied:
            raise ContractError(
                "Party and location synchronization requires Worker-only fields to be blank: "
                + ", ".join(supplied)
            )

    return {
        "synchronization_type": synchronization_type,
        "person_type": person_type,
        "from_date": from_date,
        "to_date": to_date,
        "person_numbers": person_numbers,
    }


def build_payload(
    normalized: dict[str, str | None], description: str | None = None
) -> dict[str, Any]:
    request_parameters: list[dict[str, str]] = []
    for field, argument_name in ARGUMENT_SPECS:
        parameter = {"name": argument_name, "paramType": PARAM_TYPE}
        value = normalized[field]
        if value is not None:
            parameter["value"] = value
        request_parameters.append(parameter)

    payload: dict[str, Any] = {
        "application": APPLICATION,
        "jobDefinitionId": JOB_DEFINITION_ID,
        "retries": 0,
        "requestParameters": request_parameters,
    }
    normalized_description = _text(description, "description")
    if normalized_description is not None:
        payload["description"] = normalized_description
    return payload


def _effective_selection(
    normalized: dict[str, str | None],
) -> tuple[dict[str, Any], list[dict[str, str]], list[str]]:
    synchronization_type = normalized["synchronization_type"]
    warnings: list[str] = []
    ignored_parameters: list[dict[str, str]] = []

    if synchronization_type == "ORA_PARTY_DENORM":
        return (
            {
                "mode": "PARTY_AND_LOCATION",
                "description": "Update current party and location records.",
            },
            ignored_parameters,
            warnings,
        )

    person_numbers = normalized["person_numbers"]
    if person_numbers is not None:
        for field in ("person_type", "from_date", "to_date"):
            value = normalized[field]
            if value is not None:
                ignored_parameters.append({"field": field, "value": value})
        if ignored_parameters:
            warnings.append(
                "Person Number takes precedence; supplied person type and date filters "
                "remain in the payload but are ignored by the process selection logic."
            )
        return (
            {
                "mode": "PERSON_NUMBERS",
                "description": "Synchronize the listed person numbers.",
                "person_numbers": person_numbers.split(","),
            },
            ignored_parameters,
            warnings,
        )

    if normalized["from_date"] is not None:
        warnings.append(
            "To Date is inclusive; Fusion internally adds one day while processing."
        )
    if normalized["person_type"] is None and normalized["from_date"] is None:
        warnings.append(
            "No Worker filters were supplied; the process can cover all applicable worker types."
        )
        mode = "ALL_APPLICABLE_WORKERS"
        description = "Synchronize all applicable worker types without a date filter."
    else:
        mode = "WORKER_FILTERS"
        description = "Synchronize workers using the supplied person type and date filters."
    return (
        {"mode": mode, "description": description},
        ignored_parameters,
        warnings,
    )


def build_document(raw: dict[str, Any], description: str | None = None) -> dict[str, Any]:
    normalized = normalize_parameters(raw)
    payload = build_payload(normalized, description)
    effective_selection, ignored_parameters, warnings = _effective_selection(normalized)
    fingerprint_source = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return {
        "contract_version": CONTRACT_VERSION,
        "normalized_job_parameters": normalized,
        "effective_selection": effective_selection,
        "ignored_parameters": ignored_parameters,
        "warnings": warnings,
        "verified_ess_identity": {
            "application": APPLICATION,
            "job_definition_id": JOB_DEFINITION_ID,
        },
        "ess_request_payload": payload,
        "payload_sha256": hashlib.sha256(fingerprint_source).hexdigest(),
        "approval_required": True,
        "live_execution_ready": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build the fixed five-position CrmEss CurrentDateRecordSync request "
            "from canonical parameters."
        )
    )
    parser.add_argument("--input", required=True, help="Canonical parameter JSON file.")
    parser.add_argument(
        "--description", help="Optional unique, non-sensitive ESS correlation description."
    )
    parser.add_argument(
        "--payload-output", help="Write only the executable ESS request payload."
    )
    parser.add_argument(
        "--report-output", help="Write the normalized preview and payload document."
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite outputs after explicit approval."
    )
    return parser.parse_args()


def _validate_output_paths(args: argparse.Namespace) -> None:
    input_path = Path(args.input).resolve()
    output_paths = [
        Path(value).resolve()
        for value in (args.payload_output, args.report_output)
        if value is not None
    ]
    if input_path in output_paths:
        raise ContractError("An output path must not replace the canonical input file")
    if len(output_paths) != len(set(output_paths)):
        raise ContractError("payload_output and report_output must use different paths")
    if not args.force:
        existing = [str(path) for path in output_paths if path.exists()]
        if existing:
            raise ContractError(
                "Output already exists; use a new path or approved --force: "
                + ", ".join(existing)
            )


def main() -> int:
    args = parse_args()
    try:
        _validate_output_paths(args)
        raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
        document = build_document(raw, args.description)
        if args.payload_output:
            Path(args.payload_output).write_text(
                json.dumps(document["ess_request_payload"], indent=2) + "\n",
                encoding="utf-8",
            )
        if args.report_output:
            Path(args.report_output).write_text(
                json.dumps(document, indent=2) + "\n", encoding="utf-8"
            )
        if not args.report_output:
            sys.stdout.write(json.dumps(document, indent=2) + "\n")
        return 0
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(f"Current record request validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
