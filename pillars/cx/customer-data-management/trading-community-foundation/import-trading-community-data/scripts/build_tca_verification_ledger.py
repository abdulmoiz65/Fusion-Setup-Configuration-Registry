#!/usr/bin/env python3
"""Build a redacted, request-instance verification ledger for TCA imports."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


STATUSES = {
    "completed_and_verified",
    "failed_no_record_created",
    "deferred",
    "not_submitted",
    "unknown_requires_reconciliation",
}
MUTATIONS = {"created", "updated", "deleted", "inactivated", "none"}


class LedgerError(ValueError):
    """Raised when request or verification evidence violates the contract."""


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LedgerError(f"Cannot read valid JSON from {path}: {exc}") from exc


def _nonempty(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def _require(mapping: dict[str, Any], field: str, context: str) -> Any:
    value = mapping.get(field)
    if not _nonempty(value):
        raise LedgerError(f"{context} requires non-empty {field}")
    return value


def load_requests(payload: Any) -> tuple[str | None, list[dict[str, Any]]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("requests"), list):
        raise LedgerError("Request manifest must contain a requests array")
    environment = payload.get("environment")
    requests: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(payload["requests"], start=1):
        if not isinstance(item, dict):
            raise LedgerError(f"Request {index} must be an object")
        request_id = str(_require(item, "request_id", f"Request {index}"))
        if request_id in seen:
            raise LedgerError(f"Duplicate request_id: {request_id}")
        seen.add(request_id)
        object_code = str(_require(item, "object_code", f"Request {request_id}"))
        intended_mutation = str(_require(item, "intended_mutation", f"Request {request_id}"))
        if intended_mutation not in MUTATIONS - {"none"}:
            raise LedgerError(f"Request {request_id} has invalid intended_mutation: {intended_mutation}")
        expected_default = 0 if intended_mutation == "deleted" else 1
        expected = item.get("expected_match_count", expected_default)
        if not isinstance(expected, int) or isinstance(expected, bool) or expected < 0:
            raise LedgerError(f"Request {request_id} expected_match_count must be a nonnegative integer")
        if intended_mutation == "deleted" and expected != 0:
            raise LedgerError(f"Request {request_id} deletion expected_match_count must be 0")
        if intended_mutation != "deleted" and expected < 1:
            raise LedgerError(f"Request {request_id} expected_match_count must be a positive integer")
        requests.append({
            "request_id": request_id,
            "object_code": object_code,
            "intended_mutation": intended_mutation,
            "expected_match_count": expected,
            "parent_ref": item.get("parent_ref"),
            "source_reference_supplied": bool(item.get("source_reference_supplied", False)),
        })
    if not requests:
        raise LedgerError("Request manifest must contain at least one request")
    return environment, requests


def load_outcomes(payloads: list[Any]) -> dict[str, dict[str, Any]]:
    outcomes: dict[str, dict[str, Any]] = {}
    for payload in payloads:
        items = payload.get("outcomes") if isinstance(payload, dict) and "outcomes" in payload else [payload]
        if not isinstance(items, list):
            raise LedgerError("outcomes must be an array")
        for item in items:
            if not isinstance(item, dict):
                raise LedgerError("Each outcome must be an object")
            request_id = str(_require(item, "request_id", "Outcome"))
            if request_id in outcomes:
                raise LedgerError(f"Duplicate outcome for request_id: {request_id}")
            outcomes[request_id] = item
    return outcomes


def validate_outcome(request: dict[str, Any], raw: dict[str, Any]) -> dict[str, Any]:
    request_id = request["request_id"]
    object_code = str(_require(raw, "object_code", f"Outcome {request_id}"))
    if object_code != request["object_code"]:
        raise LedgerError(
            f"Outcome {request_id} object_code {object_code!r} does not match requested "
            f"{request['object_code']!r}; semantically different objects cannot substitute for one another"
        )
    status = str(_require(raw, "status", f"Outcome {request_id}"))
    mutation = str(_require(raw, "mutation", f"Outcome {request_id}"))
    if status not in STATUSES:
        raise LedgerError(f"Outcome {request_id} has invalid status: {status}")
    if mutation not in MUTATIONS:
        raise LedgerError(f"Outcome {request_id} has invalid mutation: {mutation}")

    verification = raw.get("verification") or {}
    if not isinstance(verification, dict):
        raise LedgerError(f"Outcome {request_id} verification must be an object")
    match_count = verification.get("exact_match_count")
    target_ids = verification.get("target_record_ids") or []

    if status == "completed_and_verified":
        if mutation != request["intended_mutation"]:
            raise LedgerError(
                f"Outcome {request_id} mutation {mutation!r} does not match intended "
                f"{request['intended_mutation']!r}"
            )
        _require(raw, "import_activity_id", f"Completed outcome {request_id}")
        _require(raw, "ucm_content_id", f"Completed outcome {request_id}")
        counts = _require(raw, "process_counts", f"Completed outcome {request_id}")
        if not isinstance(counts, dict):
            raise LedgerError(f"Completed outcome {request_id} process_counts must be an object")
        loaded = counts.get("loaded")
        errors = counts.get("errors")
        if not isinstance(loaded, int) or isinstance(loaded, bool) or loaded < 1 or errors != 0:
            raise LedgerError(f"Completed outcome {request_id} requires loaded >= 1 and errors == 0")
        if match_count != request["expected_match_count"]:
            raise LedgerError(
                f"Completed outcome {request_id} exact_match_count must equal "
                f"{request['expected_match_count']}"
            )
        if not isinstance(target_ids, list) or len(target_ids) != request["expected_match_count"]:
            raise LedgerError(f"Completed outcome {request_id} requires one target_record_id per exact match")
        _require(verification, "state", f"Completed outcome {request_id} verification")
        if _nonempty(request.get("parent_ref")):
            _require(verification, "parent_identity", f"Completed child outcome {request_id} verification")
        if request["source_reference_supplied"]:
            _require(verification, "source_reference", f"Completed outcome {request_id} verification")
    elif status == "failed_no_record_created":
        if mutation != "none" or match_count != 0:
            raise LedgerError(f"Failed outcome {request_id} requires mutation none and exact_match_count 0")
        _require(raw, "reason", f"Failed outcome {request_id}")
    else:
        if mutation != "none":
            raise LedgerError(f"Outcome {request_id} with status {status} requires mutation none")
        _require(raw, "reason", f"Outcome {request_id}")
        if status == "not_submitted" and (
            _nonempty(raw.get("import_activity_id")) or _nonempty(raw.get("ucm_content_id"))
        ):
            raise LedgerError(f"Not-submitted outcome {request_id} cannot contain activity or UCM IDs")

    return {
        "request_id": request_id,
        "object_code": object_code,
        "intended_mutation": request["intended_mutation"],
        "status": status,
        "mutation": mutation,
        "expected_match_count": request["expected_match_count"],
        "parent_ref": request.get("parent_ref"),
        "import_activity_id": raw.get("import_activity_id"),
        "ucm_content_id": raw.get("ucm_content_id"),
        "process_counts": raw.get("process_counts"),
        "verification": verification,
        "reason": raw.get("reason"),
    }


def build_ledger(manifest: Any, outcome_payloads: list[Any]) -> dict[str, Any]:
    environment, requests = load_requests(manifest)
    outcomes = load_outcomes(outcome_payloads)
    request_ids = {item["request_id"] for item in requests}
    extras = sorted(set(outcomes) - request_ids)
    if extras:
        raise LedgerError(f"Outcomes reference unknown request_id values: {', '.join(extras)}")

    records: list[dict[str, Any]] = []
    for request in requests:
        raw = outcomes.get(request["request_id"])
        if raw is None:
            raw = {
                "request_id": request["request_id"],
                "object_code": request["object_code"],
                "status": "unknown_requires_reconciliation",
                "mutation": "none",
                "reason": "No outcome was supplied for this requested record instance.",
            }
        records.append(validate_outcome(request, raw))

    status_counts = Counter(item["status"] for item in records)
    mutation_counts = Counter(item["mutation"] for item in records)
    if status_counts["unknown_requires_reconciliation"]:
        campaign_status = "requires_reconciliation"
    elif status_counts["completed_and_verified"] == len(records):
        campaign_status = "complete"
    else:
        campaign_status = "complete_with_terminal_exceptions"

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[record["object_code"]].append(record)
    object_summary = []
    for object_code in sorted(grouped):
        group = grouped[object_code]
        completed = sum(item["status"] == "completed_and_verified" for item in group)
        if completed == len(group):
            coverage_status = "complete"
        elif completed:
            coverage_status = "partial"
        else:
            coverage_status = "not_completed"
        object_summary.append({
            "object_code": object_code,
            "requested": len(group),
            "completed_and_verified": completed,
            "coverage_status": coverage_status,
        })

    return {
        "schema_version": 1,
        "environment": environment,
        "campaign_status": campaign_status,
        "summary": {
            "requested": len(records),
            "by_status": {key: status_counts.get(key, 0) for key in sorted(STATUSES)},
            "by_mutation": {key: mutation_counts.get(key, 0) for key in sorted(MUTATIONS)},
        },
        "object_summary": object_summary,
        "record_outcomes": records,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request-manifest", type=Path, required=True)
    parser.add_argument("--outcome", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.output.exists() and not args.overwrite:
        raise LedgerError(f"Output already exists: {args.output}; pass --overwrite to replace it")
    ledger = build_ledger(_load_json(args.request_manifest), [_load_json(path) for path in args.outcome])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "campaign_status": ledger["campaign_status"],
        "output": str(args.output),
        "requested": ledger["summary"]["requested"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
