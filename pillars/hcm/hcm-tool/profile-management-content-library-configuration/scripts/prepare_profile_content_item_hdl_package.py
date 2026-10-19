#!/usr/bin/env python3
"""Build one deterministic, create-only HDL ContentItem V2 package.

The helper is local-only. It accepts sanitized, target-bound Item Catalog
evidence and approved Content Item rows, validates the enhanced-profile route,
and emits one immutable ZIP for a later core.data-loader preview. It has no
OAuth, REST, UCM, Data Loader, or Fusion mutation capability.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Mapping, Sequence
import zipfile


SCHEMA_VERSION = "1.0"
TASK_CODE = "HRT_MANAGE_PROFILE_CONTENT_ITEMS"
TASK_NAME = "Content Items"
BUSINESS_OBJECT = "ContentItem"
SOURCE_TYPE = "HDL"
ZIP_MEMBER = "ContentItem.dat"
MAX_INPUT_BYTES = 8 * 1024 * 1024
MAX_OUTPUT_BYTES = 32 * 1024 * 1024
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
SAFE_ALIAS_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
SAFE_CODE_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9_]{0,79}$")
SUPPORTED_CONTEXTS = frozenset({"COMPETENCY"})
TOP_LEVEL_KEYS = frozenset(
    {
        "schema_version",
        "operation",
        "task_code",
        "business_object",
        "target_environment",
        "fusion_release",
        "profile_mode",
        "proposal_fingerprint",
        "provider_rows_fingerprint",
        "item_catalog_evidence",
        "rows",
    }
)
CATALOG_EVIDENCE_KEYS = frozenset(
    {
        "source",
        "target_environment",
        "fusion_release",
        "captured_at",
        "valid_through",
        "complete",
        "content_type_context",
        "catalog_code",
        "catalog_name",
        "exact_content_item_matches",
        "evidence_sha256",
    }
)
ROW_FIELDS = (
    "ContentItemCode",
    "ContextName",
    "ContentItemValueSetName",
    "Name",
    "DateFrom",
    "ContentSupplierCode",
    "RatingModelCode",
)


class HdlPackageContractError(ValueError):
    """Expected fail-closed HDL package validation error."""

    def __init__(self, message: str, failure_class: str = "input_validation") -> None:
        super().__init__(message)
        self.failure_class = failure_class


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require_object(value: Any, keys: frozenset[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise HdlPackageContractError(f"{label} must be an object")
    supplied = set(value)
    if supplied != set(keys):
        missing = sorted(set(keys) - supplied)
        extra = sorted(supplied - set(keys))
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if extra:
            details.append("unexpected " + ", ".join(extra))
        raise HdlPackageContractError(f"{label} has invalid keys: {'; '.join(details)}")
    return dict(value)


def _require_text(value: Any, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise HdlPackageContractError(f"{label} must be a string")
    if not allow_empty and not value:
        raise HdlPackageContractError(f"{label} must not be empty")
    if value != value.strip():
        raise HdlPackageContractError(f"{label} must not have leading or trailing whitespace")
    if "|" in value or "\r" in value or "\n" in value or any(ord(char) < 32 for char in value):
        raise HdlPackageContractError(f"{label} contains an unsupported delimiter or control character")
    return value


def _require_sha256(value: Any, label: str) -> str:
    text = _require_text(value, label)
    if not SHA256_PATTERN.fullmatch(text):
        raise HdlPackageContractError(f"{label} must be 64 lowercase hexadecimal characters")
    return text


def _require_code(value: Any, label: str) -> str:
    text = _require_text(value, label)
    if not SAFE_CODE_PATTERN.fullmatch(text):
        raise HdlPackageContractError(
            f"{label} must use uppercase letters, digits, and underscores only"
        )
    return text


def _parse_timestamp(value: Any, label: str) -> datetime:
    text = _require_text(value, label)
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise HdlPackageContractError(f"{label} must be an RFC 3339 timestamp") from error
    if parsed.tzinfo is None:
        raise HdlPackageContractError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _parse_as_of(value: str | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    return _parse_timestamp(value, "as_of")


def _parse_iso_date(value: str, label: str) -> str:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError as error:
        raise HdlPackageContractError(f"{label} must use YYYY-MM-DD") from error
    return parsed.strftime("%Y/%m/%d")


def provider_rows_fingerprint(payload: Mapping[str, Any]) -> str:
    material = {
        key: payload[key]
        for key in (
            "schema_version",
            "operation",
            "task_code",
            "business_object",
            "target_environment",
            "fusion_release",
            "profile_mode",
            "proposal_fingerprint",
            "item_catalog_evidence",
            "rows",
        )
    }
    return _sha256_bytes(_canonical_json(material))


def validate_payload(raw: Any, *, as_of: datetime) -> tuple[dict[str, Any], tuple[dict[str, str], ...]]:
    payload = _require_object(raw, TOP_LEVEL_KEYS, "input")
    if payload["schema_version"] != SCHEMA_VERSION:
        raise HdlPackageContractError(f"schema_version must be {SCHEMA_VERSION}")
    if payload["operation"] != "create":
        raise HdlPackageContractError("operation must be create")
    if payload["task_code"] != TASK_CODE:
        raise HdlPackageContractError(f"task_code must be {TASK_CODE}")
    if payload["business_object"] != BUSINESS_OBJECT:
        raise HdlPackageContractError(f"business_object must be {BUSINESS_OBJECT}")
    if payload["profile_mode"] != "enhanced":
        raise HdlPackageContractError("profile_mode must be enhanced")
    target = _require_text(payload["target_environment"], "target_environment")
    if not SAFE_ALIAS_PATTERN.fullmatch(target):
        raise HdlPackageContractError("target_environment contains unsupported characters")
    release = _require_text(payload["fusion_release"], "fusion_release")
    if not SAFE_ALIAS_PATTERN.fullmatch(release):
        raise HdlPackageContractError("fusion_release contains unsupported characters")
    _require_sha256(payload["proposal_fingerprint"], "proposal_fingerprint")

    evidence = _require_object(
        payload["item_catalog_evidence"], CATALOG_EVIDENCE_KEYS, "item_catalog_evidence"
    )
    if evidence["source"] != "talentContentItemCatalogs":
        raise HdlPackageContractError(
            "item_catalog_evidence.source must be talentContentItemCatalogs"
        )
    if evidence["target_environment"] != target:
        raise HdlPackageContractError("item_catalog_evidence target does not match input")
    captured_at = _parse_timestamp(evidence["captured_at"], "item_catalog_evidence.captured_at")
    valid_through = _parse_timestamp(
        evidence["valid_through"], "item_catalog_evidence.valid_through"
    )
    if captured_at > as_of or valid_through < as_of or valid_through < captured_at:
        raise HdlPackageContractError("item_catalog_evidence is stale or has an invalid time window")
    if evidence["complete"] is not True:
        raise HdlPackageContractError("item_catalog_evidence.complete must be true")
    context = _require_code(
        evidence["content_type_context"], "item_catalog_evidence.content_type_context"
    )
    if context not in SUPPORTED_CONTEXTS:
        raise HdlPackageContractError("item_catalog_evidence uses an unsupported content type")
    _require_code(evidence["catalog_code"], "item_catalog_evidence.catalog_code")
    catalog_name = _require_text(evidence["catalog_name"], "item_catalog_evidence.catalog_name")
    match_count = evidence["exact_content_item_matches"]
    if isinstance(match_count, bool) or not isinstance(match_count, int) or match_count != 0:
        raise HdlPackageContractError(
            "item_catalog_evidence must prove zero exact Content Item matches for create-only loading"
        )
    _require_sha256(evidence["evidence_sha256"], "item_catalog_evidence.evidence_sha256")

    raw_rows = payload["rows"]
    if not isinstance(raw_rows, list) or not raw_rows:
        raise HdlPackageContractError("rows must be a non-empty array")
    rows: list[dict[str, str]] = []
    identities: set[tuple[str, str]] = set()
    for index, raw_row in enumerate(raw_rows, start=1):
        row = _require_object(raw_row, frozenset(ROW_FIELDS), f"rows[{index}]")
        normalized = {
            field: _require_text(row[field], f"rows[{index}].{field}") for field in ROW_FIELDS
        }
        for field in (
            "ContentItemCode",
            "ContextName",
            "ContentSupplierCode",
            "RatingModelCode",
        ):
            normalized[field] = _require_code(normalized[field], f"rows[{index}].{field}")
        if normalized["ContextName"] != context:
            raise HdlPackageContractError(f"rows[{index}].ContextName does not match catalog evidence")
        if normalized["ContentItemValueSetName"] != catalog_name:
            raise HdlPackageContractError(
                f"rows[{index}].ContentItemValueSetName does not match catalog evidence"
            )
        normalized["DateFrom"] = _parse_iso_date(
            normalized["DateFrom"], f"rows[{index}].DateFrom"
        )
        identity = normalized["ContextName"], normalized["ContentItemCode"]
        if identity in identities:
            raise HdlPackageContractError("rows contain duplicate Content Item keys")
        identities.add(identity)
        rows.append(normalized)

    expected_fingerprint = provider_rows_fingerprint(payload)
    supplied_fingerprint = _require_sha256(
        payload["provider_rows_fingerprint"], "provider_rows_fingerprint"
    )
    if supplied_fingerprint != expected_fingerprint:
        raise HdlPackageContractError(
            "provider_rows_fingerprint does not match the exact approved HDL input"
        )
    return payload, tuple(rows)


def _dat_bytes(rows: Sequence[Mapping[str, str]]) -> bytes:
    lines = ["METADATA|ContentItem|" + "|".join(ROW_FIELDS)]
    for row in rows:
        lines.append("MERGE|ContentItem|" + "|".join(row[field] for field in ROW_FIELDS))
    return ("\n".join(lines) + "\n").encode("utf-8")


def _zip_bytes(dat_content: bytes) -> bytes:
    import io

    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        info = zipfile.ZipInfo(ZIP_MEMBER, date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o600 << 16
        archive.writestr(info, dat_content)
    value = stream.getvalue()
    if len(value) > MAX_OUTPUT_BYTES:
        raise HdlPackageContractError("generated HDL archive exceeds the size limit")
    return value


def _inside_project(project_root: Path, relative: str, label: str) -> Path:
    supplied = Path(relative)
    if supplied.is_absolute():
        raise HdlPackageContractError(f"{label} must be relative to project_root")
    root = project_root.resolve(strict=True)
    target = (root / supplied).resolve()
    try:
        target.relative_to(root)
    except ValueError as error:
        raise HdlPackageContractError(f"{label} must remain inside project_root") from error
    return target


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".content-item-hdl-", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root)
    input_path = _inside_project(project_root, args.input_json, "input_json")
    output_path = _inside_project(project_root, args.output_zip, "output_zip")
    readiness_path = _inside_project(project_root, args.readiness_report, "readiness_report")
    if input_path.stat().st_size > MAX_INPUT_BYTES:
        raise HdlPackageContractError("input_json exceeds the size limit")
    try:
        raw = json.loads(input_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise HdlPackageContractError("input_json is not readable UTF-8 JSON") from error
    as_of = _parse_as_of(args.as_of)
    payload, rows = validate_payload(raw, as_of=as_of)
    content = _zip_bytes(_dat_bytes(rows))
    package_sha256 = _sha256_bytes(content)
    readiness_material = {
        "schema_version": SCHEMA_VERSION,
        "task_code": TASK_CODE,
        "business_object": BUSINESS_OBJECT,
        "source_type": SOURCE_TYPE,
        "operation": "create",
        "target_environment": payload["target_environment"],
        "fusion_release": payload["fusion_release"],
        "profile_mode": payload["profile_mode"],
        "proposal_fingerprint": payload["proposal_fingerprint"],
        "provider_rows_fingerprint": payload["provider_rows_fingerprint"],
        "item_catalog_evidence_sha256": payload["item_catalog_evidence"]["evidence_sha256"],
        "archive_sha256": package_sha256,
        "row_count": len(rows),
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
            },
            "task_hook_final_data": {
                "archiveSha256": package_sha256,
                "packageReadinessFingerprint": readiness_fingerprint,
                "proposalFingerprint": payload["proposal_fingerprint"],
                "providerRowsFingerprint": payload["provider_rows_fingerprint"],
                "sourceType": SOURCE_TYPE,
                "businessObject": BUSINESS_OBJECT,
                "operation": "create",
            },
        },
    }
    _atomic_write(output_path, content)
    _atomic_write(
        readiness_path,
        (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    return report


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-zip", required=True)
    parser.add_argument("--readiness-report", required=True)
    parser.add_argument("--as-of")
    parser.add_argument(
        "--print-provider-rows-fingerprint",
        action="store_true",
        help="Print the canonical provider-row fingerprint and do not write output files.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.print_provider_rows_fingerprint:
            input_path = _inside_project(Path(args.project_root), args.input_json, "input_json")
            raw = json.loads(input_path.read_text(encoding="utf-8"))
            _require_object(raw, TOP_LEVEL_KEYS, "input")
            print(provider_rows_fingerprint(raw))
            return 0
        print(json.dumps(prepare(args), indent=2, sort_keys=True))
        return 0
    except (HdlPackageContractError, OSError, UnicodeError, json.JSONDecodeError) as error:
        failure_class = getattr(error, "failure_class", "input_validation")
        print(json.dumps({"status": "blocked", "failure_class": failure_class, "message": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
