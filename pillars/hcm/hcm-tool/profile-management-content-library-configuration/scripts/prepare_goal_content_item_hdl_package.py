#!/usr/bin/env python3
"""Inspect GOAL evidence and build one lifecycle-gated HDL package.

This helper is local-only. It reopens a complete, unfiltered Content Items FSM
export to establish both the GOAL code identity and V2 name user-key lock, then
builds one deterministic ContentItem.dat ZIP. It cannot authenticate, call a
network service, upload content, initiate a load, or poll Fusion.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Mapping, Sequence
import zipfile


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from profile_content_library_fsm_evidence import (  # noqa: E402
    CI_MEMBER,
    EvidenceContractError,
    inspect_fsm_evidence,
)
from seeded_profile_content_library_catalog import (  # noqa: E402
    SeededCatalogError,
    load_seeded_content_items,
)
from build_profile_content_library_preview import contains_sensitive  # noqa: E402


SCHEMA_VERSION = "1.0"
REPORT_SCHEMA_VERSION = "1.1"
FALLBACK_POLICY = "verified-goal-hdl-exception-v1"
TASK_CODE = "HRT_MANAGE_PROFILE_CONTENT_ITEMS"
TASK_NAME = "Content Items"
TASK_SKILL_PATH = (
    "pillars/hcm/hcm-tool/profile-management-content-library-configuration/"
    "content-items/SKILL.md"
)
OFFERING = "HCM Tool"
FUNCTIONAL_AREA = "Profile Management Content Library Configuration"
BUSINESS_OBJECT = "ContentItem"
SOURCE_TYPE = "HDL"
CONTEXT_NAME = "GOAL"
PROVIDER = "CONTENT_ITEM_V2_HDL"
EVIDENCE_PROVIDER = "FSM_EXPORT"
ZIP_MEMBER = "ContentItem.dat"
ROW_FIELDS = ("ContentItemCode", "ContextName", "Name", "DateFrom")
FORBIDDEN_FIELDS = (
    "ContentItemValueSetName",
    "ContentItemValueSetId",
    "ContentSupplierCode",
    "RatingModelCode",
    "SourceSystemOwner",
    "SourceSystemId",
    "ContentItemId",
    "ContentTypeId",
    "RatingModelId",
    "ContentItemRlat",
)
MAX_INPUT_BYTES = 8 * 1024 * 1024
MAX_OUTPUT_BYTES = 32 * 1024 * 1024
MAX_EVIDENCE_WINDOW = timedelta(minutes=15)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
SAFE_ALIAS_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
SAFE_CODE_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9_]{0,29}$")

PROVIDER_CONTRACT_PATH = (
    SCRIPT_DIR.parent
    / "content-items"
    / "references"
    / "content-item-goal-hdl-provider.json"
)
SEEDED_CONTENT_ITEMS_PATH = SCRIPT_DIR.parent / "assets" / "seeded-content-items"

PROVIDER_KEYS = frozenset(
    {
        "schema_version",
        "provider",
        "business_object",
        "task_code",
        "context_name",
        "content_type_id",
        "profile_mode",
        "source_fusion_releases",
        "lifecycle",
        "evidence_provider",
        "readback_provider",
        "user_key",
        "code_identity",
        "max_rows_per_package",
        "row_fields",
        "forbidden_fields",
        "date_format",
        "execution_route",
        "mutation_boundary",
    }
)
RECEIPT_KEYS = frozenset(
    {
        "schema_version",
        "status",
        "task_code",
        "source_environment",
        "target_environment",
        "fusion_release",
        "profile_mode",
        "provider",
        "provider_contract_sha256",
        "captured_at",
        "valid_through",
        "complete",
        "unfiltered_task_export",
        "archive_path",
        "archive_sha256",
        "row_counts",
        "member_sha256",
        "content_item_contexts",
        "exact_key",
        "customer_exact_code_matches",
        "customer_exact_name_matches",
        "seeded_exact_code_matches",
        "seeded_exact_name_matches",
        "normalized_name_warning_count",
        "matched_identifiers",
        "seeded_content_item_manifest_sha256",
        "evidence_fingerprint",
        "blockers",
    }
)
INPUT_KEYS = frozenset(
    {
        "schema_version",
        "operation",
        "provider_use",
        "fallback_selection",
        "task_code",
        "business_object",
        "target_environment",
        "fusion_release",
        "profile_mode",
        "proposal_fingerprint",
        "provider_contract_sha256",
        "current_state_receipt_path",
        "current_state_receipt_sha256",
        "provider_rows_fingerprint",
        "row",
    }
)


class GoalHdlPackageContractError(ValueError):
    """Expected fail-closed GOAL provider validation error."""

    def __init__(self, message: str, failure_class: str = "input_validation") -> None:
        super().__init__(message)
        self.failure_class = failure_class


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_object(value: Any, keys: frozenset[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise GoalHdlPackageContractError(f"{label} must be an object")
    supplied = set(value)
    if supplied != set(keys):
        missing = sorted(set(keys) - supplied)
        extra = sorted(supplied - set(keys))
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if extra:
            details.append("unexpected " + ", ".join(extra))
        raise GoalHdlPackageContractError(f"{label} has invalid keys: {'; '.join(details)}")
    return dict(value)


def _require_text(
    value: Any,
    label: str,
    *,
    max_length: int | None = None,
) -> str:
    if not isinstance(value, str) or not value:
        raise GoalHdlPackageContractError(f"{label} must be a nonblank string")
    if value != value.strip():
        raise GoalHdlPackageContractError(f"{label} must not have leading or trailing whitespace")
    if "|" in value or "\r" in value or "\n" in value or any(ord(char) < 32 for char in value):
        raise GoalHdlPackageContractError(
            f"{label} contains an unsupported delimiter or control character"
        )
    if max_length is not None and len(value) > max_length:
        raise GoalHdlPackageContractError(
            f"{label} exceeds the maximum length of {max_length} characters"
        )
    return value


def _require_sha256(value: Any, label: str) -> str:
    text = _require_text(value, label)
    if not SHA256_PATTERN.fullmatch(text):
        raise GoalHdlPackageContractError(
            f"{label} must be 64 lowercase hexadecimal characters"
        )
    return text


def _require_alias(value: Any, label: str) -> str:
    text = _require_text(value, label)
    if not SAFE_ALIAS_PATTERN.fullmatch(text):
        raise GoalHdlPackageContractError(f"{label} contains unsupported characters")
    return text


def _require_code(value: Any, label: str) -> str:
    text = _require_text(value, label, max_length=30)
    if not SAFE_CODE_PATTERN.fullmatch(text):
        raise GoalHdlPackageContractError(
            f"{label} must use at most 30 uppercase letters, digits, and underscores"
        )
    return text


def _parse_timestamp(value: Any, label: str) -> datetime:
    text = _require_text(value, label)
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise GoalHdlPackageContractError(f"{label} must be an RFC 3339 timestamp") from error
    if parsed.tzinfo is None:
        raise GoalHdlPackageContractError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _parse_as_of(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    return _parse_timestamp(value, "as_of")


def _validate_freshness(captured_value: Any, valid_value: Any, *, as_of: datetime) -> None:
    captured_at = _parse_timestamp(captured_value, "captured_at")
    valid_through = _parse_timestamp(valid_value, "valid_through")
    if captured_at > as_of or valid_through < as_of or valid_through < captured_at:
        raise GoalHdlPackageContractError("GOAL current-state evidence is stale or future-dated")
    if valid_through - captured_at > MAX_EVIDENCE_WINDOW:
        raise GoalHdlPackageContractError(
            "GOAL current-state evidence window must not exceed 15 minutes"
        )


def _parse_iso_date(value: Any, label: str) -> str:
    text = _require_text(value, label)
    try:
        parsed = datetime.strptime(text, "%Y-%m-%d")
    except ValueError as error:
        raise GoalHdlPackageContractError(f"{label} must use YYYY-MM-DD") from error
    return parsed.strftime("%Y/%m/%d")


def _inside_project(
    project_root: Path,
    relative: Any,
    label: str,
    *,
    must_exist: bool = False,
) -> Path:
    text = _require_text(relative, label)
    supplied = Path(text)
    if supplied.is_absolute() or any(part in {"", ".", ".."} for part in supplied.parts):
        raise GoalHdlPackageContractError(f"{label} must be a safe project-relative path")
    root = project_root.resolve(strict=True)
    unresolved = root / supplied
    if unresolved.is_symlink():
        raise GoalHdlPackageContractError(f"{label} must not be a symbolic link")
    target = unresolved.resolve()
    try:
        target.relative_to(root)
    except ValueError as error:
        raise GoalHdlPackageContractError(f"{label} must remain inside project_root") from error
    if must_exist and not target.is_file():
        raise GoalHdlPackageContractError(f"{label} must identify one readable file")
    return target


def _read_json(path: Path, label: str) -> Any:
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise GoalHdlPackageContractError(f"{label} exceeds the size limit")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise GoalHdlPackageContractError(f"{label} is not readable UTF-8 JSON") from error


def _load_provider_contract(expected_sha256: str | None = None) -> tuple[dict[str, Any], str]:
    try:
        raw = PROVIDER_CONTRACT_PATH.read_bytes()
        parsed = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise GoalHdlPackageContractError(
            "checked-in GOAL provider contract is unreadable",
            "artifact_persistence",
        ) from error
    actual_sha256 = _sha256_bytes(raw)
    if expected_sha256 is not None and _require_sha256(
        expected_sha256, "provider_contract_sha256"
    ) != actual_sha256:
        raise GoalHdlPackageContractError("GOAL provider contract fingerprint has changed")
    contract = _require_object(parsed, PROVIDER_KEYS, "GOAL provider contract")
    expected_values = {
        "schema_version": SCHEMA_VERSION,
        "provider": PROVIDER,
        "business_object": BUSINESS_OBJECT,
        "task_code": TASK_CODE,
        "context_name": CONTEXT_NAME,
        "content_type_id": 124,
        "profile_mode": "enhanced",
        "source_fusion_releases": ["26C"],
        "evidence_provider": EVIDENCE_PROVIDER,
        "readback_provider": EVIDENCE_PROVIDER,
        "user_key": ["ContextName", "Name"],
        "code_identity": ["ContextName", "ContentItemCode"],
        "max_rows_per_package": 1,
        "row_fields": list(ROW_FIELDS),
        "forbidden_fields": list(FORBIDDEN_FIELDS),
        "date_format": "YYYY/MM/DD",
        "execution_route": "core.data-loader",
        "mutation_boundary": "create-only-single-row",
    }
    for field, expected in expected_values.items():
        if contract[field] != expected:
            raise GoalHdlPackageContractError(
                f"checked-in GOAL provider contract has an unsupported {field}"
            )
    lifecycle = _require_object(
        contract["lifecycle"], frozenset({"status", "reason"}), "provider lifecycle"
    )
    if lifecycle["status"] not in {"certification-only", "verified"}:
        raise GoalHdlPackageContractError("GOAL provider lifecycle is unsupported")
    _require_text(lifecycle["reason"], "provider lifecycle reason", max_length=800)
    return contract, actual_sha256


def evidence_fingerprint(receipt: Mapping[str, Any]) -> str:
    material = {key: receipt[key] for key in sorted(RECEIPT_KEYS - {"evidence_fingerprint"})}
    return _sha256_bytes(_canonical_json(material))


def provider_rows_fingerprint(payload: Mapping[str, Any]) -> str:
    material = {key: payload[key] for key in sorted(INPUT_KEYS - {"provider_rows_fingerprint"})}
    return _sha256_bytes(_canonical_json(material))


def _validate_fallback_selection(raw: Any, lifecycle: str) -> dict[str, Any]:
    """Validate route selection, not submission approval or a live-state claim.

    The owning task supplies this from the complete reviewed request and its
    recorded execution history. All fields are bound by the input fingerprint.
    Missing/unknown or previously submitted mutations must never auto-fail over.
    """
    selection = _require_object(raw, frozenset({
        "policy", "explicitly_selected", "fsm_limitation", "mutation_state",
    }), "fallback_selection")
    if selection["policy"] != FALLBACK_POLICY:
        raise GoalHdlPackageContractError("fallback policy is unsupported; FSM-only does not select HDL")
    if selection["explicitly_selected"] is not True:
        raise GoalHdlPackageContractError("GOAL fallback must be explicitly selected")
    if selection["fsm_limitation"] != "enhanced-goal-companion-document":
        raise GoalHdlPackageContractError("fallback requires the registered GOAL FSM limitation")
    if selection["mutation_state"] != "not_submitted":
        raise GoalHdlPackageContractError("fallback is blocked after submission or unknown mutation state")
    if lifecycle != "verified":
        raise GoalHdlPackageContractError("fallback requires a verified provider lifecycle")
    return selection


def _evaluate_current_state(
    *,
    project_root: Path,
    archive_relative: str,
    source_environment: str,
    target_environment: str,
    fusion_release: str,
    captured_at: str,
    valid_through: str,
    content_item_code: str,
    name: str,
    as_of: datetime,
    provider_contract_sha256: str,
) -> dict[str, Any]:
    source = _require_alias(source_environment, "source_environment")
    target = _require_alias(target_environment, "target_environment")
    release = _require_alias(fusion_release, "fusion_release")
    code = _require_code(content_item_code, "ContentItemCode")
    goal_name = _require_text(name, "Name", max_length=700)
    _validate_freshness(captured_at, valid_through, as_of=as_of)
    archive_path = _inside_project(
        project_root, archive_relative, "current_state_zip", must_exist=True
    )
    if archive_path.suffix.lower() != ".zip":
        raise GoalHdlPackageContractError("current_state_zip must be a ZIP archive")
    try:
        evidence = inspect_fsm_evidence(
            archive_path,
            task_code=TASK_CODE,
            source_environment_alias=source,
            target_environment_alias=target,
            fusion_release=release,
            purpose="current-state",
            unfiltered_task_export=True,
        )
        seeded = load_seeded_content_items(
            SEEDED_CONTENT_ITEMS_PATH,
            expected_release=release,
        )
    except (EvidenceContractError, SeededCatalogError) as error:
        raise GoalHdlPackageContractError(
            f"GOAL current-state evidence is unusable: {error}",
            "catalog_or_metadata_mismatch",
        ) from error
    if not evidence.usable_for_duplicate_comparison:
        raise GoalHdlPackageContractError(
            "GOAL current-state evidence is incomplete or not bound to the exact target",
            "catalog_or_metadata_mismatch",
        )

    customer_rows = evidence.records_by_member[CI_MEMBER]
    seeded_rows = seeded.records_by_file["content-items.csv"]
    contexts = sorted({row.get("ContextName", "") for row in customer_rows})
    customer_code = [
        row
        for row in customer_rows
        if row.get("ContextName", "") == CONTEXT_NAME
        and row.get("ContentItemCode", "") == code
    ]
    customer_name = [
        row
        for row in customer_rows
        if row.get("ContextName", "") == CONTEXT_NAME and row.get("Name", "") == goal_name
    ]
    seeded_code = [
        row
        for row in seeded_rows
        if row.get("ContextName", "") == CONTEXT_NAME
        and row.get("ContentItemCode", "") == code
    ]
    seeded_name = [
        row
        for row in seeded_rows
        if row.get("ContextName", "") == CONTEXT_NAME and row.get("Name", "") == goal_name
    ]
    matched_identifiers = []
    for origin, rows in (("customer", customer_rows), ("seeded", seeded_rows)):
        for row in rows:
            if row.get("ContextName") != CONTEXT_NAME:
                continue
            matched_on = [field for field, requested in (
                ("ContentItemCode", code), ("Name", goal_name)
            ) if row.get(field) == requested]
            if matched_on:
                # Only actual identifiers, never proposed values or arbitrary
                # source columns. Keep every matched source row, including
                # duplicate rows and distinct Name/code collisions.
                matched_identifiers.append({
                    "source": origin, "matched_on": matched_on,
                    **{field: row[field] for field in (
                        "ContextName", "ContentItemCode", "Name"
                    ) if row.get(field)},
                })

    if contains_sensitive({"Name": goal_name, "matched_identifiers": matched_identifiers}):
        raise GoalHdlPackageContractError("GOAL exact evidence contains sensitive material")

    blockers: list[str] = []
    if contexts != [CONTEXT_NAME]:
        blockers.append("The complete Content Items export must contain GOAL item rows only.")
    if customer_code or seeded_code:
        blockers.append("The exact GOAL ContentItemCode already exists.")
    if customer_name or seeded_name:
        blockers.append("The exact GOAL ContentItem V2 name user key already exists.")

    receipt: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "status": "blocked" if blockers else "ready",
        "task_code": TASK_CODE,
        "source_environment": source,
        "target_environment": target,
        "fusion_release": release,
        "profile_mode": "enhanced",
        "provider": EVIDENCE_PROVIDER,
        "provider_contract_sha256": provider_contract_sha256,
        "captured_at": captured_at,
        "valid_through": valid_through,
        "complete": evidence.complete,
        "unfiltered_task_export": evidence.unfiltered_task_export,
        "archive_path": archive_relative,
        "archive_sha256": evidence.archive_sha256,
        "row_counts": dict(sorted(evidence.row_counts.items())),
        "member_sha256": dict(sorted(evidence.member_sha256.items())),
        "content_item_contexts": contexts,
        "exact_key": {
            "ContextName": CONTEXT_NAME,
            "ContentItemCode": code,
            "Name": goal_name,
        },
        "customer_exact_code_matches": len(customer_code),
        "customer_exact_name_matches": len(customer_name),
        "seeded_exact_code_matches": len(seeded_code),
        "seeded_exact_name_matches": len(seeded_name),
        "normalized_name_warning_count": 0,
        "matched_identifiers": matched_identifiers,
        "seeded_content_item_manifest_sha256": seeded.manifest_sha256,
        "evidence_fingerprint": "",
        "blockers": blockers,
    }
    receipt["evidence_fingerprint"] = evidence_fingerprint(receipt)
    return receipt


def inspect_current_state(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root)
    if _require_text(args.profile_mode, "profile_mode") != "enhanced":
        raise GoalHdlPackageContractError("profile_mode must be enhanced")
    if args.unfiltered_task_export is not True:
        raise GoalHdlPackageContractError(
            "current-state evidence must be explicitly attested as one complete, unfiltered task export",
            "catalog_or_metadata_mismatch",
        )
    _, provider_sha256 = _load_provider_contract()
    output_path = _inside_project(project_root, args.output_json, "output_json")
    if output_path.exists():
        raise GoalHdlPackageContractError("output_json already exists; refusing to overwrite")
    receipt = _evaluate_current_state(
        project_root=project_root,
        archive_relative=args.current_state_zip,
        source_environment=args.source_environment,
        target_environment=args.target_environment,
        fusion_release=args.fusion_release,
        captured_at=args.captured_at,
        valid_through=args.valid_through,
        content_item_code=args.content_item_code,
        name=args.name,
        as_of=_parse_as_of(args.as_of),
        provider_contract_sha256=provider_sha256,
    )
    _atomic_create(
        output_path,
        (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    return receipt


def _validate_receipt(
    raw: Any,
    *,
    payload: Mapping[str, Any],
    receipt_sha256: str,
    project_root: Path,
    as_of: datetime,
) -> dict[str, Any]:
    receipt = _require_object(raw, RECEIPT_KEYS, "current_state_receipt")
    if receipt["schema_version"] != REPORT_SCHEMA_VERSION:
        raise GoalHdlPackageContractError("current_state_receipt schema is unsupported")
    if evidence_fingerprint(receipt) != receipt["evidence_fingerprint"]:
        raise GoalHdlPackageContractError("current_state_receipt evidence fingerprint is invalid")
    _require_sha256(receipt["evidence_fingerprint"], "current_state_receipt.evidence_fingerprint")
    if receipt["status"] != "ready" or receipt["blockers"] != []:
        raise GoalHdlPackageContractError("current_state_receipt is blocked")
    if receipt["matched_identifiers"] != [] or receipt["normalized_name_warning_count"] != 0:
        raise GoalHdlPackageContractError("current_state_receipt exact reporting is inconsistent")
    if receipt["task_code"] != TASK_CODE or receipt["provider"] != EVIDENCE_PROVIDER:
        raise GoalHdlPackageContractError("current_state_receipt provider or task is invalid")
    if receipt["profile_mode"] != "enhanced":
        raise GoalHdlPackageContractError("current_state_receipt profile mode is invalid")
    if receipt["target_environment"] != payload["target_environment"]:
        raise GoalHdlPackageContractError("current_state_receipt target does not match input")
    if receipt["source_environment"] != receipt["target_environment"]:
        raise GoalHdlPackageContractError("current_state_receipt is not same-target evidence")
    if receipt["provider_contract_sha256"] != payload["provider_contract_sha256"]:
        raise GoalHdlPackageContractError("current_state_receipt provider contract has changed")
    if receipt["complete"] is not True or receipt["unfiltered_task_export"] is not True:
        raise GoalHdlPackageContractError("current_state_receipt must be complete and unfiltered")
    if receipt["content_item_contexts"] != [CONTEXT_NAME]:
        raise GoalHdlPackageContractError("current_state_receipt must have GOAL-only coverage")
    for field in (
        "customer_exact_code_matches",
        "customer_exact_name_matches",
        "seeded_exact_code_matches",
        "seeded_exact_name_matches",
    ):
        if receipt[field] != 0:
            raise GoalHdlPackageContractError(
                "current_state_receipt must prove zero exact code and name matches"
            )
    _validate_freshness(receipt["captured_at"], receipt["valid_through"], as_of=as_of)
    if _require_sha256(payload["current_state_receipt_sha256"], "current_state_receipt_sha256") != receipt_sha256:
        raise GoalHdlPackageContractError("current_state_receipt file fingerprint has changed")
    return receipt


def _validate_row(raw: Any) -> dict[str, str]:
    row = _require_object(raw, frozenset(ROW_FIELDS), "row")
    normalized = {
        "ContentItemCode": _require_code(row["ContentItemCode"], "row.ContentItemCode"),
        "ContextName": _require_text(row["ContextName"], "row.ContextName"),
        "Name": _require_text(row["Name"], "row.Name", max_length=700),
        "DateFrom": _parse_iso_date(row["DateFrom"], "row.DateFrom"),
    }
    if normalized["ContextName"] != CONTEXT_NAME:
        raise GoalHdlPackageContractError("row.ContextName must be GOAL")
    return normalized


def _dat_bytes(row: Mapping[str, str]) -> bytes:
    lines = [
        "METADATA|ContentItem|" + "|".join(ROW_FIELDS),
        "MERGE|ContentItem|" + "|".join(row[field] for field in ROW_FIELDS),
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")


def _zip_bytes(dat_content: bytes) -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        info = zipfile.ZipInfo(ZIP_MEMBER, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o600 << 16
        archive.writestr(info, dat_content)
    value = stream.getvalue()
    if len(value) > MAX_OUTPUT_BYTES:
        raise GoalHdlPackageContractError("generated GOAL HDL archive exceeds the size limit")
    with zipfile.ZipFile(io.BytesIO(value)) as archive:
        if archive.namelist() != [ZIP_MEMBER] or archive.read(ZIP_MEMBER) != dat_content:
            raise GoalHdlPackageContractError(
                "generated GOAL HDL archive failed independent reopening validation",
                "artifact_persistence",
            )
    return value


def _atomic_create(path: Path, content: bytes) -> None:
    if path.exists():
        raise GoalHdlPackageContractError(f"output already exists: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".goal-content-item-", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if path.exists():
            raise GoalHdlPackageContractError(f"output already exists: {path.name}")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root)
    input_path = _inside_project(project_root, args.input_json, "input_json", must_exist=True)
    output_path = _inside_project(project_root, args.output_zip, "output_zip")
    readiness_path = _inside_project(project_root, args.readiness_report, "readiness_report")
    if output_path == readiness_path:
        raise GoalHdlPackageContractError("output_zip and readiness_report must differ")
    if output_path.exists() or readiness_path.exists():
        raise GoalHdlPackageContractError("output files already exist; refusing to overwrite")
    if output_path.suffix.lower() != ".zip" or readiness_path.suffix.lower() != ".json":
        raise GoalHdlPackageContractError("output files must use .zip and .json extensions")

    payload = _require_object(_read_json(input_path, "input_json"), INPUT_KEYS, "input")
    if payload["schema_version"] != REPORT_SCHEMA_VERSION:
        raise GoalHdlPackageContractError(f"schema_version must be {REPORT_SCHEMA_VERSION}")
    if payload["operation"] != "create":
        raise GoalHdlPackageContractError("operation must be create")
    if payload["task_code"] != TASK_CODE or payload["business_object"] != BUSINESS_OBJECT:
        raise GoalHdlPackageContractError("task_code or business_object is unsupported")
    if payload["profile_mode"] != "enhanced":
        raise GoalHdlPackageContractError("profile_mode must be enhanced")
    target = _require_alias(payload["target_environment"], "target_environment")
    release = _require_alias(payload["fusion_release"], "fusion_release")
    proposal_fingerprint = _require_sha256(
        payload["proposal_fingerprint"], "proposal_fingerprint"
    )
    contract, provider_sha256 = _load_provider_contract(payload["provider_contract_sha256"])
    provider_use = _require_text(payload["provider_use"], "provider_use")
    lifecycle = contract["lifecycle"]["status"]
    if provider_use == "certification":
        if lifecycle not in {"certification-only", "verified"}:
            raise GoalHdlPackageContractError("GOAL provider is not eligible for certification")
    elif provider_use == "general":
        if lifecycle != "verified":
            raise GoalHdlPackageContractError(
                "GOAL provider general use is blocked until certification is verified"
            )
    else:
        raise GoalHdlPackageContractError("provider_use must be certification or general")

    fallback_selection = _validate_fallback_selection(payload["fallback_selection"], lifecycle)

    row = _validate_row(payload["row"])
    receipt_path = _inside_project(
        project_root,
        payload["current_state_receipt_path"],
        "current_state_receipt_path",
        must_exist=True,
    )
    receipt_sha256 = _sha256_file(receipt_path)
    receipt = _validate_receipt(
        _read_json(receipt_path, "current_state_receipt"),
        payload=payload,
        receipt_sha256=receipt_sha256,
        project_root=project_root,
        as_of=_parse_as_of(args.as_of),
    )
    if receipt["exact_key"] != {
        "ContextName": CONTEXT_NAME,
        "ContentItemCode": row["ContentItemCode"],
        "Name": row["Name"],
    }:
        raise GoalHdlPackageContractError("current_state_receipt exact key does not match row")
    recomputed = _evaluate_current_state(
        project_root=project_root,
        archive_relative=receipt["archive_path"],
        source_environment=receipt["source_environment"],
        target_environment=target,
        fusion_release=receipt["fusion_release"],
        captured_at=receipt["captured_at"],
        valid_through=receipt["valid_through"],
        content_item_code=row["ContentItemCode"],
        name=row["Name"],
        as_of=_parse_as_of(args.as_of),
        provider_contract_sha256=provider_sha256,
    )
    if recomputed != receipt:
        raise GoalHdlPackageContractError(
            "current_state_receipt no longer matches the exact archive and seeded evidence"
        )
    expected_fingerprint = provider_rows_fingerprint(payload)
    if _require_sha256(
        payload["provider_rows_fingerprint"], "provider_rows_fingerprint"
    ) != expected_fingerprint:
        raise GoalHdlPackageContractError(
            "provider_rows_fingerprint does not match the exact approved GOAL input"
        )

    dat_content = _dat_bytes(row)
    archive_content = _zip_bytes(dat_content)
    archive_sha256 = _sha256_bytes(archive_content)
    dat_sha256 = _sha256_bytes(dat_content)
    readiness_material = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "task_code": TASK_CODE,
        "business_object": BUSINESS_OBJECT,
        "source_type": SOURCE_TYPE,
        "provider": PROVIDER,
        "provider_use": provider_use,
        "fallback_selection": fallback_selection,
        "provider_lifecycle": lifecycle,
        "operation": "create",
        "target_environment": target,
        "fusion_release": release,
        "profile_mode": "enhanced",
        "proposal_fingerprint": proposal_fingerprint,
        "provider_contract_sha256": provider_sha256,
        "current_state_receipt_sha256": receipt_sha256,
        "current_state_evidence_fingerprint": receipt["evidence_fingerprint"],
        "provider_rows_fingerprint": payload["provider_rows_fingerprint"],
        "archive_sha256": archive_sha256,
        "dat_sha256": dat_sha256,
        "row_count": 1,
    }
    readiness_fingerprint = _sha256_bytes(_canonical_json(readiness_material))
    report = {
        **readiness_material,
        "status": "package_ready_for_core_data_loader_preview",
        "package_path": str(output_path.relative_to(project_root.resolve(strict=True))),
        "readiness_fingerprint": readiness_fingerprint,
        "data_loader_handoff": {
            "route": "core.data-loader",
            "source_type": SOURCE_TYPE,
            "business_object": BUSINESS_OBJECT,
            "approval_state": "not_requested",
            "task_context_requirements": {
                "task_code": TASK_CODE,
                "task_name": TASK_NAME,
                "skill_path": TASK_SKILL_PATH,
                "offering": OFFERING,
                "functional_area": FUNCTIONAL_AREA,
                "sequence": "select the exact positive sequence from persisted task context",
            },
            "task_hook_final_data": {
                "archiveSha256": archive_sha256,
                "packageReadinessFingerprint": readiness_fingerprint,
                "proposalFingerprint": proposal_fingerprint,
                "providerRowsFingerprint": payload["provider_rows_fingerprint"],
                "providerContractSha256": provider_sha256,
                "currentStateReceiptSha256": receipt_sha256,
                "currentStateEvidenceFingerprint": receipt["evidence_fingerprint"],
                "provider": PROVIDER,
                "providerUse": provider_use,
                "fallbackPolicy": FALLBACK_POLICY,
                "fallbackSelectionFingerprint": _sha256_bytes(_canonical_json(fallback_selection)),
                "providerLifecycle": lifecycle,
                "sourceType": SOURCE_TYPE,
                "businessObject": BUSINESS_OBJECT,
                "operation": "create",
                "contextName": CONTEXT_NAME,
                "rowCount": 1,
            },
        },
    }
    report_content = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    _atomic_create(output_path, archive_content)
    try:
        _atomic_create(readiness_path, report_content)
    except Exception:
        if output_path.exists():
            output_path.unlink()
        raise
    return report


def fingerprint_input(args: argparse.Namespace) -> str:
    project_root = Path(args.project_root)
    input_path = _inside_project(project_root, args.input_json, "input_json", must_exist=True)
    payload = _require_object(_read_json(input_path, "input_json"), INPUT_KEYS, "input")
    return provider_rows_fingerprint(payload)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser(
        "inspect", help="Create a sanitized dual-key GOAL current-state receipt."
    )
    inspect_parser.add_argument("--project-root", required=True)
    inspect_parser.add_argument("--current-state-zip", required=True)
    inspect_parser.add_argument("--source-environment", required=True)
    inspect_parser.add_argument("--target-environment", required=True)
    inspect_parser.add_argument("--fusion-release", default="unknown", help="Optional informational metadata; not an eligibility gate.")
    inspect_parser.add_argument("--profile-mode", required=True, choices=("enhanced",))
    inspect_parser.add_argument("--content-item-code", required=True)
    inspect_parser.add_argument("--name", required=True)
    inspect_parser.add_argument("--captured-at", required=True)
    inspect_parser.add_argument("--valid-through", required=True)
    inspect_parser.add_argument(
        "--unfiltered-task-export",
        action="store_true",
        required=True,
        help="Attest that the ZIP is the complete, unfiltered task export selected by the routed workflow.",
    )
    inspect_parser.add_argument("--output-json", required=True)
    inspect_parser.add_argument("--as-of")

    fingerprint_parser = subparsers.add_parser(
        "fingerprint", help="Print the canonical provider-row fingerprint."
    )
    fingerprint_parser.add_argument("--project-root", required=True)
    fingerprint_parser.add_argument("--input-json", required=True)

    prepare_parser = subparsers.add_parser(
        "prepare", help="Build one deterministic lifecycle-gated GOAL HDL ZIP."
    )
    prepare_parser.add_argument("--project-root", required=True)
    prepare_parser.add_argument("--input-json", required=True)
    prepare_parser.add_argument("--output-zip", required=True)
    prepare_parser.add_argument("--readiness-report", required=True)
    prepare_parser.add_argument("--as-of")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "inspect":
            result = inspect_current_state(args)
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0 if result["status"] == "ready" else 2
        if args.command == "fingerprint":
            print(fingerprint_input(args))
            return 0
        print(json.dumps(prepare(args), indent=2, sort_keys=True))
        return 0
    except (
        GoalHdlPackageContractError,
        EvidenceContractError,
        SeededCatalogError,
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
    ) as error:
        failure_class = getattr(error, "failure_class", "input_validation")
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "failure_class": failure_class,
                    "message": str(error),
                }
            ),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
