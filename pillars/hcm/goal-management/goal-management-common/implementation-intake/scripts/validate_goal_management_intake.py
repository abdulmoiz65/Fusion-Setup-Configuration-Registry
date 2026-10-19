#!/usr/bin/env python3
"""Validate date facts extracted from Goal Management implementation sources."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any


ACTION_WINDOW_ROLES = {"action_window_start", "action_window_end"}


def _parse_date(value: Any, label: str) -> date:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an ISO date string")
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{label} must use YYYY-MM-DD") from error


def validate(payload: dict[str, Any], as_of: date) -> dict[str, Any]:
    facts = payload.get("facts")
    if not isinstance(facts, list):
        raise ValueError("Input must contain a facts array")
    ranges: dict[str, dict[str, dict[str, Any]]] = {}
    for fact in facts:
        if not isinstance(fact, dict):
            raise ValueError("Each fact must be an object")
        range_id, role = fact.get("range_id"), fact.get("date_role")
        if not isinstance(range_id, str) or not range_id.strip() or role not in {"start", "end"}:
            raise ValueError("Each date fact requires range_id and date_role start or end")
        _parse_date(fact.get("value"), f"date fact {range_id}")
        ranges.setdefault(range_id, {})[role] = fact

    findings = []
    for range_id, values in sorted(ranges.items()):
        start, end = values.get("start"), values.get("end")
        if not start or not end:
            findings.append({"rule_id": "DATE_RANGE_INCOMPLETE", "status": "consultant_confirmation_required", "range_id": range_id, "message": "A date range needs both start and end values.", "source_references": [item.get("source_reference") for item in values.values()]})
            continue
        start_date, end_date = _parse_date(start["value"], range_id), _parse_date(end["value"], range_id)
        references = [start.get("source_reference"), end.get("source_reference")]
        semantic_role = end.get("semantic_role")
        if start_date > end_date:
            findings.append({"rule_id": "DATE_RANGE_INVALID", "status": "error", "range_id": range_id, "message": f"Start date {start_date} is after end date {end_date}.", "source_references": references})
        elif semantic_role in ACTION_WINDOW_ROLES and end_date < as_of:
            object_name = str(end.get("object_type") or "This configuration")
            field_name = str(end.get("field") or "end date")
            findings.append({"rule_id": "DATE_ACTION_WINDOW_ENDED", "status": "consultant_confirmation_required", "range_id": range_id, "object_type": object_name, "field": field_name, "value": end["value"], "source_references": references, "question": f"The {object_name} {field_name} is {end['value']}, which is before today {as_of.isoformat()}. Is this intentional historical/backfill configuration, or should the source be corrected? If corrected, provide the new start and end dates in YYYY-MM-DD format."})
        elif start_date < as_of:
            findings.append({"rule_id": "DATE_START_IN_PAST", "status": "informational", "range_id": range_id, "message": f"Start date {start_date} is before the evaluation date {as_of}; no correction is required when the range remains active.", "source_references": references})
    statuses = {finding["status"] for finding in findings}
    return {"schema_version": "1.0", "evaluated_at": as_of.isoformat(), "source": payload.get("source", {}), "findings": findings, "status": "review_required" if "consultant_confirmation_required" in statuses or "error" in statuses else "clear", "recheck_policy": "every_run"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Structured date-fact JSON")
    parser.add_argument("--output", type=Path, required=True, help="Input-quality report JSON")
    parser.add_argument("--as-of", help="ISO evaluation date; defaults to today")
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Input must be a JSON object")
        report = validate(payload, _parse_date(args.as_of, "--as-of") if args.as_of else date.today())
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
