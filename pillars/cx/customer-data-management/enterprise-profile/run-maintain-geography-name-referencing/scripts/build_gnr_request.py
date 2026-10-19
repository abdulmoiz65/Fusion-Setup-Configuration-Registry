#!/usr/bin/env python3
"""Validate canonical GNR parameters and build the fixed ESS request payload."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys
from typing import Any


APPLICATION = "CrmEss"
JOB_DEFINITION_ID = "JobDefinition://oracle/apps/ess/cdm/foundation/geographies/HZ-HZGNR"
PARAM_TYPE = "STRING"

ARGUMENT_SPECS = (
    ("location_table_name", "submit.argument1"),
    ("run_type", "submit.argument2"),
    ("usage_code", "submit.argument3"),
    ("country_code", "submit.argument4"),
    ("from_location_id", "submit.argument5"),
    ("to_location_id", "submit.argument6"),
    ("start_date", "submit.argument7"),
    ("end_date", "submit.argument8"),
)
CANONICAL_FIELDS = {field for field, _ in ARGUMENT_SPECS}
REQUIRED_FIELDS = {"location_table_name", "run_type"}
LOCATION_TABLES = {"HZ_LOCATIONS", "PER_ADDRESSES_F"}
RUN_TYPES = {"ALL", "ERROR", "NEW"}
USAGE_CODES = {"GEOGRAPHY", "TAX"}
COUNTRY_CODE_PATTERN = re.compile(r"^[A-Z]{2}$")
POSITIVE_INTEGER_FIELDS = (
    "from_location_id",
    "to_location_id",
)


class ContractError(ValueError):
    """Raised when canonical parameters do not satisfy the GNR contract."""


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


def _positive_integer(value: Any, field: str) -> str | None:
    normalized = _text(value, field)
    if normalized is None:
        return None
    if not normalized.isdigit() or int(normalized) <= 0:
        raise ContractError(f"{field} must be a positive integer")
    return str(int(normalized))


def _date(value: Any, field: str) -> str | None:
    normalized = _text(value, field)
    if normalized is None:
        return None
    try:
        datetime.strptime(normalized, "%Y/%m/%d")
    except ValueError as exc:
        raise ContractError(f"{field} must use YYYY/MM/DD and be a valid date") from exc
    return normalized


def normalize_parameters(raw: dict[str, Any]) -> dict[str, str | None]:
    if not isinstance(raw, dict):
        raise ContractError("Canonical parameters must be a JSON object")

    unknown = sorted(set(raw) - CANONICAL_FIELDS)
    if unknown:
        raise ContractError(f"Unsupported canonical field(s): {', '.join(unknown)}")

    missing = sorted(field for field in REQUIRED_FIELDS if _text(raw.get(field), field) is None)
    if missing:
        raise ContractError(f"Missing required field(s): {', '.join(missing)}")

    location_table = _text(raw.get("location_table_name"), "location_table_name", required=True)
    run_type = _text(raw.get("run_type"), "run_type", required=True)
    assert location_table is not None
    assert run_type is not None
    location_table = location_table.upper()
    run_type = run_type.upper()
    if location_table not in LOCATION_TABLES:
        raise ContractError(
            "location_table_name must be HZ_LOCATIONS or PER_ADDRESSES_F"
        )
    if run_type not in RUN_TYPES:
        raise ContractError("run_type must be ALL, ERROR, or NEW")

    usage_code = _text(raw.get("usage_code"), "usage_code")
    if usage_code is not None:
        usage_code = usage_code.upper()
        if usage_code not in USAGE_CODES:
            raise ContractError("usage_code must be GEOGRAPHY or TAX")

    country_code = _text(raw.get("country_code"), "country_code")
    if country_code is not None:
        country_code = country_code.upper()
        if not COUNTRY_CODE_PATTERN.fullmatch(country_code):
            raise ContractError("country_code must contain exactly two ASCII letters")

    normalized: dict[str, str | None] = {
        "location_table_name": location_table,
        "run_type": run_type,
        "usage_code": usage_code,
        "country_code": country_code,
    }
    for field in POSITIVE_INTEGER_FIELDS:
        normalized[field] = _positive_integer(raw.get(field), field)
    normalized["start_date"] = _date(raw.get("start_date"), "start_date")
    normalized["end_date"] = _date(raw.get("end_date"), "end_date")

    if location_table == "PER_ADDRESSES_F" and usage_code == "GEOGRAPHY":
        raise ContractError(
            "PER_ADDRESSES_F supports TAX usage, not GEOGRAPHY address validation"
        )

    from_id = normalized["from_location_id"]
    to_id = normalized["to_location_id"]
    if from_id is not None and to_id is not None and int(from_id) >= int(to_id):
        raise ContractError("from_location_id must be less than to_location_id")

    start_date = normalized["start_date"]
    end_date = normalized["end_date"]
    if start_date is not None and end_date is not None:
        start = datetime.strptime(start_date, "%Y/%m/%d")
        end = datetime.strptime(end_date, "%Y/%m/%d")
        if start >= end:
            raise ContractError("start_date must be earlier than end_date")

    return {field: normalized.get(field) for field, _ in ARGUMENT_SPECS}


def build_payload(
    normalized: dict[str, str | None], description: str | None = None
) -> dict[str, Any]:
    request_parameters: list[dict[str, str]] = []
    for field, argument_name in ARGUMENT_SPECS:
        parameter = {"name": argument_name, "paramType": PARAM_TYPE}
        value = normalized.get(field)
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


def build_document(raw: dict[str, Any], description: str | None = None) -> dict[str, Any]:
    normalized = normalize_parameters(raw)
    warnings: list[str] = []
    approval_required = False
    if normalized["run_type"] == "ALL":
        warnings.append("ALL can take considerable time to complete.")
        if normalized["country_code"] is None:
            warnings.append("ALL without country_code can process a broad cross-country scope.")
            approval_required = True
    return {
        "contract_version": 2,
        "normalized_job_parameters": normalized,
        "warnings": warnings,
        "approval_required": approval_required,
        "ess_request_payload": build_payload(normalized, description),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the fixed CrmEss HZ-HZGNR request from canonical parameters."
    )
    parser.add_argument("--input", required=True, help="Canonical parameter JSON file.")
    parser.add_argument("--description", help="Optional unique ESS correlation description.")
    parser.add_argument(
        "--payload-output", help="Write only the executable ESS request payload to this file."
    )
    parser.add_argument(
        "--report-output", help="Write the complete normalized preview and payload document."
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing output files after approval."
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
        rendered = json.dumps(document, indent=2, sort_keys=False) + "\n"
        if args.payload_output:
            payload_rendered = (
                json.dumps(document["ess_request_payload"], indent=2, sort_keys=False)
                + "\n"
            )
            Path(args.payload_output).write_text(payload_rendered, encoding="utf-8")
        if args.report_output:
            Path(args.report_output).write_text(rendered, encoding="utf-8")
        if not args.report_output:
            sys.stdout.write(rendered)
        return 0
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(f"GNR request validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
