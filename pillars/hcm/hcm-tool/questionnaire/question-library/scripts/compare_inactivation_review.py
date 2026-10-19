#!/usr/bin/env python3
"""Compare caller-verified Question inactivation reviews; no network or writes.

This compares business approval scope, not raw evidence-file hashes. The caller
owns live collection, freshness and recorded user approval. This is neither a
Fusion dependency resolver nor permission to upload a DAT.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED_ENDPOINTS = {"questionnaireQuestionsLOV", "questionnaireTemplates"}
DIAGNOSTIC_FIELDS = ("templates_checked", "placements_checked", "template_set_sha256")
SCOPE_FIELDS = (
    "environment", "release_evidence", "principal_evidence", "question_key",
    "current_state", "change", "changed_fields", "child_rows", "template",
    "preserved_values_sha256",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _sha(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(
        character in "0123456789abcdef" for character in value
    )


def _fingerprint(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")).hexdigest()


def approval_basis(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Validate the narrow route and project only material approval fields."""
    _require(isinstance(snapshot, dict), "review must be an object")
    _require(snapshot.get("review_schema") == 2, "review_schema must be 2")
    _require(snapshot.get("task") == "question-library" and
             snapshot.get("requested_operation") == "inactivate",
             "comparison applies only to Question Library inactivation")
    for field in SCOPE_FIELDS:
        _require(field in snapshot, f"missing approval field: {field}")
    for field in ("environment", "scan_id", "checked_at"):
        _require(isinstance(snapshot.get(field), str) and bool(snapshot[field]),
                 f"{field} must be a non-empty string")
    _require(_sha(snapshot["preserved_values_sha256"]),
             "preserved_values_sha256 must be a SHA-256")

    release = snapshot["release_evidence"]
    _require(isinstance(release, dict) and set(release) == {"status", "value"},
             "release_evidence must contain only status and value")
    _require(release.get("status") in {"verified", "unavailable"},
             "release_evidence.status must be verified or unavailable")
    if release["status"] == "verified":
        _require(isinstance(release.get("value"), str) and bool(release["value"]),
                 "verified release_evidence requires a non-empty value")
    else:
        _require(release.get("value") is None,
                 "unavailable release_evidence must use a null value")

    principal = snapshot["principal_evidence"]
    _require(isinstance(principal, dict) and set(principal) == {
        "status", "fingerprint_sha256"
    }, "principal_evidence must contain only status and fingerprint_sha256")
    _require(principal.get("status") in {"verified", "unavailable"},
             "principal_evidence.status must be verified or unavailable")
    if principal["status"] == "verified":
        _require(_sha(principal.get("fingerprint_sha256")),
                 "verified principal_evidence requires a SHA-256 fingerprint")
    else:
        _require(principal.get("fingerprint_sha256") is None,
                 "unavailable principal_evidence must use a null fingerprint")

    key = snapshot["question_key"]
    _require(isinstance(key, dict) and set(key) == {
        "SubscriberName", "QuestionCode", "QstnVersionNum"
    }, "question_key must contain the exact portable versioned key")
    _require(all(isinstance(key[field], str) and key[field]
                 for field in ("SubscriberName", "QuestionCode")),
             "subscriber and question code must be non-empty strings")
    version = key["QstnVersionNum"]
    _require(type(version) is int and version > 0,
             "QstnVersionNum must be a positive integer")
    state = snapshot["current_state"]
    _require(isinstance(state, dict) and state.get("Status") == "A" and
             state.get("LatestVersion") == "Y" and
             state.get("UpdateAllowedFlag") is True,
             "question must be active, latest and positively updateable")
    _require(snapshot.get("lifecycle_conflicts") == [],
             "lifecycle conflicts must be checked and absent")
    _require(snapshot["change"] == {"Status": {"from": "A", "to": "I"}} and
             snapshot["changed_fields"] == ["Status"] and
             type(snapshot["child_rows"]) is int and snapshot["child_rows"] == 0,
             "only Status A to I with no child rows is eligible")
    checks = snapshot.get("checks")
    _require(isinstance(checks, dict) and all(checks.get(field) is True for field in (
        "identity_exact", "fresh", "hdl_contract_validated", "inactive_status_validated",
        "preserved_values_verified", "lifecycle_state_checked",
    )), "live identity, freshness, contract, status, preservation and state checks must pass")
    template = snapshot["template"]
    _require(isinstance(template, dict) and set(template) == {
        "file", "sha256", "contract_sha256", "supported_operation"
    } and template["file"] == "Question.dat" and
             template["supported_operation"] == "MERGE" and
             _sha(template["sha256"]) and _sha(template["contract_sha256"]),
             "template must bind Question.dat, its schema contract and MERGE")

    usage = snapshot.get("visible_usage")
    _require(isinstance(usage, dict) and usage.get("coverage") == "partial",
             "visible usage must retain the partial coverage limitation")
    endpoints = usage.get("endpoints")
    _require(isinstance(endpoints, dict) and set(endpoints) == REQUIRED_ENDPOINTS,
             "both declared downstream endpoints must be checked")
    scopes = {}
    for name, result in endpoints.items():
        _require(isinstance(result, dict) and all(result.get(field) is True for field in (
            "success", "pagination_complete", "child_pagination_complete", "scope_verified",
        )), f"{name}: failed, incomplete or unverified scan")
        _require(result.get("matching_placements") == [],
                 f"{name}: visible question usage is present or unresolved")
        _require(_sha(result.get("request_scope_sha256")),
                 f"{name}: missing stable request scope fingerprint")
        scopes[name] = result["request_scope_sha256"]
    diagnostics = snapshot.get("scan_diagnostics")
    _require(isinstance(diagnostics, dict), "scan_diagnostics must be an object")
    for name in ("templates_checked", "placements_checked"):
        _require(type(diagnostics.get(name)) is int and diagnostics[name] >= 0,
                 f"scan_diagnostics.{name} must be a nonnegative integer")
    _require(_sha(diagnostics.get("template_set_sha256")),
             "scan_diagnostics must include a canonical template-set SHA-256")
    return {**{field: snapshot[field] for field in SCOPE_FIELDS},
            "review_schema": 2,
            "task": "question-library", "requested_operation": "inactivate",
            "coverage": "partial", "lookup_scopes": scopes}


def compare_reviews(current: dict[str, Any], approved: dict[str, Any] | None = None,
                    confirmation: dict[str, Any] | None = None) -> dict[str, Any]:
    """Retain an existing approval only for an unchanged, eligible business effect."""
    try:
        basis = approval_basis(current)
    except ValueError as exc:
        return {"status": "blocked", "reason": str(exc), "upload_authorized": False}
    result = {"approval_basis_sha256": _fingerprint(basis), "upload_authorized": False}
    if confirmation is not None:
        try:
            confirmed = approval_basis(confirmation)
        except ValueError as exc:
            return {**result, "status": "blocked", "reason": f"confirmation: {exc}"}
        prior_scan = approved.get("scan_id") if isinstance(approved, dict) else None
        if confirmation["scan_id"] in {prior_scan, current["scan_id"]}:
            return {**result, "status": "blocked", "reason": "confirmation must be a fresh scan"}
        if confirmed != basis:
            return {**result, "status": "blocked",
                    "reason": "question-specific evidence or scan scope did not stabilize"}
    if approved is None:
        return {**result, "status": "approval_required", "reason": "initial impact review"}
    try:
        previous = approval_basis(approved)
    except ValueError:
        return {**result, "status": "approval_required",
                "reason": "approved review lacks comparable verified scope; do not backfill evidence"}
    if previous != basis:
        return {**result, "status": "approval_required", "reason": "material scope changed",
                "changed_fields": sorted(field for field in basis if basis[field] != previous[field])}
    if current["scan_id"] == approved["scan_id"]:
        return {**result, "status": "blocked", "reason": "revalidation must be a fresh scan"}
    if any(approved["scan_diagnostics"][field] != current["scan_diagnostics"][field]
           for field in DIAGNOSTIC_FIELDS):
        if confirmation is None:
            return {**result, "status": "rescan_required",
                    "reason": "catalog diagnostics changed; repeat the read-only scan once"}
        result["warnings"] = ["Unrelated catalog diagnostics changed; complete repeat scan confirmed zero question usage."]
    return {**result, "status": "approval_retained",
            "reason": "question-specific scope and eligible status change are unchanged"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--current", required=True, type=Path)
    parser.add_argument("--approved", type=Path)
    parser.add_argument("--confirmation", type=Path)
    args = parser.parse_args(argv)
    try:
        def read(path: Path | None) -> Any:
            return json.loads(path.read_text(encoding="utf-8")) if path else None
        result = compare_reviews(read(args.current), read(args.approved), read(args.confirmation))
    except (OSError, ValueError):
        result = {"status": "blocked", "reason": "unable to read valid review JSON", "upload_authorized": False}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "approval_retained" else 2


if __name__ == "__main__":
    raise SystemExit(main())
