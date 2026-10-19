#!/usr/bin/env python3
"""Build one lifecycle-gated catalog-bound ContentItem V2 HDL package.

The helper is local-only. It consumes one fresh dual-key receipt produced by
the registered Talent Catalog GET adapter, revalidates the checked-in 26C
provider contract, and emits one deterministic ZIP for a later Task Hook and
core.data-loader preview. It cannot authenticate, call Fusion, upload, or load.
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
CONTENT_ITEMS_DIR = SCRIPT_DIR.parent / "content-items"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(CONTENT_ITEMS_DIR / "scripts") not in sys.path:
    sys.path.insert(0, str(CONTENT_ITEMS_DIR / "scripts"))

from talent_content_item_catalog_adapter import (  # noqa: E402
    CATALOG_HDL_PROVIDER,
    ProviderContractError,
    load_catalog_hdl_provider,
)
from profile_content_library_fsm_evidence import (  # noqa: E402
    EvidenceContractError,
    IC_CONTENT_ITEM_MEMBER,
    IC_MEMBER,
    inspect_fsm_evidence,
)


SCHEMA_VERSION = "1.0"
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
ZIP_MEMBER = "ContentItem.dat"
MAX_INPUT_BYTES = 8 * 1024 * 1024
MAX_OUTPUT_BYTES = 32 * 1024 * 1024
MAX_EVIDENCE_WINDOW = timedelta(minutes=15)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
SAFE_ALIAS_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
SAFE_CODE_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9_]{0,79}$")
PROVIDER_CONTRACT_PATH = (
    CONTENT_ITEMS_DIR / "references" / "content-item-catalog-hdl-provider.json"
)

INPUT_KEYS = frozenset(
    {
        "schema_version",
        "operation",
        "provider_use",
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
RECEIPT_KEYS = frozenset(
    {
        "schema_version",
        "status",
        "source",
        "provider",
        "provider_contract_sha256",
        "provider_use",
        "provider_lifecycle",
        "target_environment",
        "fusion_release",
        "profile_mode",
        "captured_at",
        "valid_through",
        "complete",
        "content_type_context",
        "child_relation",
        "catalog_code",
        "catalog_name",
        "catalog_identity_sha256",
        "catalog_status",
        "exact_key",
        "exact_content_item_code_matches",
        "exact_content_item_name_matches",
        "seeded_content_item_manifest_sha256",
        "seeded_exact_code_matches",
        "seeded_exact_name_matches",
        "row_fields",
        "required_fields",
        "fixed_values",
        "ownership_restrictions",
        "evidence_sha256",
    }
)
REST_READBACK_KEYS = frozenset(
    {
        "schema_version",
        "status",
        "operation",
        "provider",
        "target_environment",
        "fusion_release",
        "profile_mode",
        "context_name",
        "child_relation",
        "coverage",
        "exact_provider_key",
        "catalog_count",
        "catalogs",
        "exact_code_match_count",
        "exact_name_match_count",
        "code_classification",
        "name_classification",
        "code_matches",
        "name_matches",
        "read_certification",
        "hdl_create_certification",
        "ownership_restrictions",
        "captured_at",
        "valid_through",
        "evidence_sha256",
    }
)


class CatalogHdlPackageContractError(ValueError):
    """Expected fail-closed catalog HDL package validation error."""

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
        raise CatalogHdlPackageContractError(f"{label} must be an object")
    supplied = set(value)
    if supplied != set(keys):
        missing = sorted(set(keys) - supplied)
        extra = sorted(supplied - set(keys))
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if extra:
            details.append("unexpected " + ", ".join(extra))
        raise CatalogHdlPackageContractError(
            f"{label} has invalid keys: {'; '.join(details)}"
        )
    return dict(value)


def _require_text(value: Any, label: str, *, max_length: int = 700) -> str:
    if not isinstance(value, str) or not value:
        raise CatalogHdlPackageContractError(f"{label} must be a nonblank string")
    if value != value.strip():
        raise CatalogHdlPackageContractError(
            f"{label} must not have leading or trailing whitespace"
        )
    if len(value) > max_length or any(
        char in value for char in ("|", "\r", "\n")
    ) or any(ord(char) < 32 for char in value):
        raise CatalogHdlPackageContractError(
            f"{label} contains unsupported characters or is too long"
        )
    return value


def _require_sha256(value: Any, label: str) -> str:
    text = _require_text(value, label, max_length=64)
    if not SHA256_PATTERN.fullmatch(text):
        raise CatalogHdlPackageContractError(
            f"{label} must be 64 lowercase hexadecimal characters"
        )
    return text


def _require_alias(value: Any, label: str) -> str:
    text = _require_text(value, label, max_length=64)
    if not SAFE_ALIAS_PATTERN.fullmatch(text):
        raise CatalogHdlPackageContractError(f"{label} contains unsupported characters")
    return text


def _require_code(value: Any, label: str) -> str:
    text = _require_text(value, label, max_length=80)
    if not SAFE_CODE_PATTERN.fullmatch(text):
        raise CatalogHdlPackageContractError(
            f"{label} must use uppercase letters, digits, and underscores only"
        )
    return text


def _parse_timestamp(value: Any, label: str) -> datetime:
    text = _require_text(value, label)
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise CatalogHdlPackageContractError(
            f"{label} must be an RFC 3339 timestamp"
        ) from error
    if parsed.tzinfo is None:
        raise CatalogHdlPackageContractError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _parse_as_of(value: str | None) -> datetime:
    return datetime.now(timezone.utc) if value is None else _parse_timestamp(value, "as_of")


def _validate_freshness(captured: Any, valid: Any, *, as_of: datetime) -> None:
    captured_at = _parse_timestamp(captured, "current_state_receipt.captured_at")
    valid_through = _parse_timestamp(valid, "current_state_receipt.valid_through")
    if captured_at > as_of or valid_through < as_of or valid_through < captured_at:
        raise CatalogHdlPackageContractError(
            "current_state_receipt is stale or future-dated",
            "catalog_or_metadata_mismatch",
        )
    if valid_through - captured_at > MAX_EVIDENCE_WINDOW:
        raise CatalogHdlPackageContractError(
            "current_state_receipt evidence window must not exceed 15 minutes",
            "catalog_or_metadata_mismatch",
        )


def _parse_iso_date(value: Any, label: str) -> str:
    text = _require_text(value, label, max_length=10)
    try:
        parsed = datetime.strptime(text, "%Y-%m-%d")
    except ValueError as error:
        raise CatalogHdlPackageContractError(f"{label} must use YYYY-MM-DD") from error
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
        raise CatalogHdlPackageContractError(f"{label} must be a safe project-relative path")
    root = project_root.resolve(strict=True)
    unresolved = root / supplied
    if unresolved.is_symlink():
        raise CatalogHdlPackageContractError(f"{label} must not be a symbolic link")
    target = unresolved.resolve()
    try:
        target.relative_to(root)
    except ValueError as error:
        raise CatalogHdlPackageContractError(f"{label} must remain inside project_root") from error
    if must_exist and not target.is_file():
        raise CatalogHdlPackageContractError(f"{label} must identify one readable file")
    return target


def _read_json(path: Path, label: str) -> Any:
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise CatalogHdlPackageContractError(f"{label} exceeds the size limit")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CatalogHdlPackageContractError(
            f"{label} is not readable UTF-8 JSON"
        ) from error


def _provider_context(provider: Mapping[str, Any], context_name: str) -> dict[str, Any]:
    matches = [
        entry for entry in provider["contexts"] if entry["context_name"] == context_name
    ]
    if len(matches) != 1:
        raise CatalogHdlPackageContractError(
            f"context {context_name} is not registered exactly once"
        )
    context = dict(matches[0])
    if context["builder_route"] != "catalog-provider":
        raise CatalogHdlPackageContractError(
            f"context {context_name} must use its separately registered provider route",
            "catalog_or_metadata_mismatch",
        )
    return context


def provider_rows_fingerprint(payload: Mapping[str, Any]) -> str:
    material = {key: payload[key] for key in sorted(INPUT_KEYS - {"provider_rows_fingerprint"})}
    return _sha256_bytes(_canonical_json(material))


def _validate_receipt(
    raw: Any,
    *,
    payload: Mapping[str, Any],
    receipt_sha256: str,
    provider_context: Mapping[str, Any],
    as_of: datetime,
) -> dict[str, Any]:
    receipt = _require_object(raw, RECEIPT_KEYS, "current_state_receipt")
    body = {key: receipt[key] for key in sorted(RECEIPT_KEYS - {"evidence_sha256"})}
    if _sha256_bytes(_canonical_json(body)) != receipt["evidence_sha256"]:
        raise CatalogHdlPackageContractError("current_state_receipt evidence fingerprint is invalid")
    if receipt["schema_version"] != SCHEMA_VERSION or receipt["status"] != "ready":
        raise CatalogHdlPackageContractError("current_state_receipt is not ready")
    if receipt["source"] != "talentContentItemCatalogs" or receipt["provider"] != CATALOG_HDL_PROVIDER:
        raise CatalogHdlPackageContractError("current_state_receipt provider is unsupported")
    if receipt["provider_contract_sha256"] != payload["provider_contract_sha256"]:
        raise CatalogHdlPackageContractError("current_state_receipt provider contract has changed")
    if receipt["provider_use"] != payload["provider_use"]:
        raise CatalogHdlPackageContractError("current_state_receipt provider_use has changed")
    if receipt["provider_lifecycle"] != provider_context["lifecycle"]["status"]:
        raise CatalogHdlPackageContractError("current_state_receipt lifecycle has changed")
    if receipt["target_environment"] != payload["target_environment"]:
        raise CatalogHdlPackageContractError("current_state_receipt target has changed")
    if receipt["profile_mode"] != "enhanced" or receipt["complete"] is not True:
        raise CatalogHdlPackageContractError("current_state_receipt must be complete enhanced-profile evidence")
    if receipt["content_type_context"] != provider_context["context_name"]:
        raise CatalogHdlPackageContractError("current_state_receipt context has changed")
    if receipt["child_relation"] != provider_context["child_relation"]:
        raise CatalogHdlPackageContractError("current_state_receipt child relation has changed")
    if receipt["catalog_code"] in provider_context["blocked_catalog_codes"]:
        raise CatalogHdlPackageContractError("current_state_receipt selected a blocked catalog")
    status = receipt["catalog_status"]
    if isinstance(status, str) and status.upper() in {"I", "INACTIVE"}:
        raise CatalogHdlPackageContractError("current_state_receipt selected an inactive catalog")
    for field in (
        "exact_content_item_code_matches",
        "exact_content_item_name_matches",
        "seeded_exact_code_matches",
        "seeded_exact_name_matches",
    ):
        if receipt[field] != 0:
            raise CatalogHdlPackageContractError(
                "current_state_receipt must prove zero exact code and name matches"
            )
    if receipt["row_fields"] != provider_context["row_fields"] or receipt["required_fields"] != provider_context["required_fields"] or receipt["fixed_values"] != provider_context["fixed_values"]:
        raise CatalogHdlPackageContractError("current_state_receipt row contract has changed")
    _validate_freshness(receipt["captured_at"], receipt["valid_through"], as_of=as_of)
    if _require_sha256(payload["current_state_receipt_sha256"], "current_state_receipt_sha256") != receipt_sha256:
        raise CatalogHdlPackageContractError("current_state_receipt file fingerprint has changed")
    return receipt


def _validate_row(
    raw: Any,
    *,
    provider_context: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, str]:
    row_fields = tuple(provider_context["row_fields"])
    row = _require_object(raw, frozenset(row_fields), "row")
    normalized = {
        field: _require_text(row[field], f"row.{field}") for field in row_fields
    }
    for field in ("ContentItemCode", "ContextName", "ContentSupplierCode", "RatingModelCode"):
        if field in normalized:
            normalized[field] = _require_code(normalized[field], f"row.{field}")
    normalized["DateFrom"] = _parse_iso_date(normalized["DateFrom"], "row.DateFrom")
    for field, fixed_value in provider_context["fixed_values"].items():
        if row[field] != fixed_value:
            raise CatalogHdlPackageContractError(f"row.{field} does not match the provider-defined fixed value")
    exact_key = receipt["exact_key"]
    expected_key = {
        "ContextName": row["ContextName"],
        "ContentItemCode": row["ContentItemCode"],
        "ContentItemValueSetName": row["ContentItemValueSetName"],
        "Name": row["Name"],
    }
    if exact_key != expected_key:
        raise CatalogHdlPackageContractError("current_state_receipt exact key does not match row")
    if row["ContentItemValueSetName"] != receipt["catalog_name"]:
        raise CatalogHdlPackageContractError("row catalog name does not match current_state_receipt")
    return normalized


def _dat_bytes(row: Mapping[str, str], row_fields: Sequence[str]) -> bytes:
    lines = [
        "METADATA|ContentItem|" + "|".join(row_fields),
        "MERGE|ContentItem|" + "|".join(row[field] for field in row_fields),
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
        raise CatalogHdlPackageContractError("generated HDL archive exceeds the size limit")
    with zipfile.ZipFile(io.BytesIO(value)) as archive:
        if archive.namelist() != [ZIP_MEMBER] or archive.read(ZIP_MEMBER) != dat_content:
            raise CatalogHdlPackageContractError(
                "generated HDL archive failed independent reopening validation",
                "artifact_persistence",
            )
    return value


def _atomic_create(path: Path, content: bytes) -> None:
    if path.exists():
        raise CatalogHdlPackageContractError(f"output already exists: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".catalog-content-item-", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if path.exists():
            raise CatalogHdlPackageContractError(f"output already exists: {path.name}")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root)
    input_path = _inside_project(project_root, args.input_json, "input_json", must_exist=True)
    output_path = _inside_project(project_root, args.output_zip, "output_zip")
    readiness_path = _inside_project(project_root, args.readiness_report, "readiness_report")
    if output_path == readiness_path or output_path.exists() or readiness_path.exists():
        raise CatalogHdlPackageContractError("output paths must differ and must not already exist")
    if output_path.suffix.lower() != ".zip" or readiness_path.suffix.lower() != ".json":
        raise CatalogHdlPackageContractError("output files must use .zip and .json extensions")

    payload = _require_object(_read_json(input_path, "input_json"), INPUT_KEYS, "input")
    if payload["schema_version"] != SCHEMA_VERSION or payload["operation"] != "create":
        raise CatalogHdlPackageContractError("input schema_version or operation is unsupported")
    if payload["task_code"] != TASK_CODE or payload["business_object"] != BUSINESS_OBJECT:
        raise CatalogHdlPackageContractError("task_code or business_object is unsupported")
    if payload["profile_mode"] != "enhanced":
        raise CatalogHdlPackageContractError("profile_mode must be enhanced")
    target = _require_alias(payload["target_environment"], "target_environment")
    release = _require_alias(payload["fusion_release"], "fusion_release")
    proposal_fingerprint = _require_sha256(payload["proposal_fingerprint"], "proposal_fingerprint")
    try:
        provider, provider_sha256 = load_catalog_hdl_provider(PROVIDER_CONTRACT_PATH)
    except ProviderContractError as error:
        raise CatalogHdlPackageContractError(str(error), error.failure_class) from error
    if _require_sha256(payload["provider_contract_sha256"], "provider_contract_sha256") != provider_sha256:
        raise CatalogHdlPackageContractError("catalog HDL provider contract fingerprint has changed")
    provider_use = _require_text(payload["provider_use"], "provider_use", max_length=32)
    raw_row = payload["row"]
    if not isinstance(raw_row, dict):
        raise CatalogHdlPackageContractError("row must be an object")
    context_name = _require_code(raw_row.get("ContextName"), "row.ContextName")
    provider_context = _provider_context(provider, context_name)
    lifecycle = provider_context["lifecycle"]["status"]
    if provider_use == "certification":
        if lifecycle not in {"certification-only", "verified"}:
            raise CatalogHdlPackageContractError("provider is not eligible for certification")
    elif provider_use == "general":
        if lifecycle != "verified":
            raise CatalogHdlPackageContractError(
                "provider general use is blocked until controlled certification is verified"
            )
    else:
        raise CatalogHdlPackageContractError("provider_use must be certification or general")

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
        provider_context=provider_context,
        as_of=_parse_as_of(args.as_of),
    )
    row = _validate_row(raw_row, provider_context=provider_context, receipt=receipt)
    expected_fingerprint = provider_rows_fingerprint(payload)
    if _require_sha256(payload["provider_rows_fingerprint"], "provider_rows_fingerprint") != expected_fingerprint:
        raise CatalogHdlPackageContractError(
            "provider_rows_fingerprint does not match the exact approved input"
        )

    dat_content = _dat_bytes(row, provider_context["row_fields"])
    archive_content = _zip_bytes(dat_content)
    archive_sha256 = _sha256_bytes(archive_content)
    dat_sha256 = _sha256_bytes(dat_content)
    readiness_material = {
        "schema_version": SCHEMA_VERSION,
        "task_code": TASK_CODE,
        "business_object": BUSINESS_OBJECT,
        "source_type": SOURCE_TYPE,
        "provider": CATALOG_HDL_PROVIDER,
        "provider_use": provider_use,
        "provider_lifecycle": lifecycle,
        "operation": "create",
        "target_environment": target,
        "fusion_release": release,
        "profile_mode": "enhanced",
        "context_name": context_name,
        "catalog_code": receipt["catalog_code"],
        "catalog_name": receipt["catalog_name"],
        "proposal_fingerprint": proposal_fingerprint,
        "provider_contract_sha256": provider_sha256,
        "current_state_receipt_sha256": receipt_sha256,
        "current_state_evidence_sha256": receipt["evidence_sha256"],
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
        "required_post_load_certification": {
            "catalog_rest": "fresh complete exact-code and exact-name readback",
            "item_catalog_fsm_export": "fresh complete unfiltered same-target parent and child readback",
            "duplicate_rerun": "the same create receipt must be blocked after readback",
            "lifecycle_promotion": "requires persisted controlled-load and both readback receipts",
        },
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
                "currentStateEvidenceSha256": receipt["evidence_sha256"],
                "provider": CATALOG_HDL_PROVIDER,
                "providerUse": provider_use,
                "providerLifecycle": lifecycle,
                "sourceType": SOURCE_TYPE,
                "businessObject": BUSINESS_OBJECT,
                "operation": "create",
                "contextName": context_name,
                "catalogCode": receipt["catalog_code"],
                "rowCount": 1,
            },
        },
    }
    _atomic_create(output_path, archive_content)
    try:
        _atomic_create(
            readiness_path,
            (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )
    except Exception:
        if output_path.exists():
            output_path.unlink()
        raise
    return report


def _approved_payload_for_readback(
    input_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str], str]:
    payload = _require_object(_read_json(input_path, "input_json"), INPUT_KEYS, "input")
    if payload["schema_version"] != SCHEMA_VERSION or payload["operation"] != "create":
        raise CatalogHdlPackageContractError("input schema_version or operation is unsupported")
    if payload["task_code"] != TASK_CODE or payload["business_object"] != BUSINESS_OBJECT:
        raise CatalogHdlPackageContractError("task_code or business_object is unsupported")
    if payload["profile_mode"] != "enhanced":
        raise CatalogHdlPackageContractError("profile_mode must be enhanced")
    if provider_rows_fingerprint(payload) != payload["provider_rows_fingerprint"]:
        raise CatalogHdlPackageContractError("approved provider_rows_fingerprint is invalid")
    try:
        provider, provider_sha256 = load_catalog_hdl_provider(PROVIDER_CONTRACT_PATH)
    except ProviderContractError as error:
        raise CatalogHdlPackageContractError(str(error), error.failure_class) from error
    if provider_sha256 != payload["provider_contract_sha256"]:
        raise CatalogHdlPackageContractError("catalog HDL provider contract fingerprint has changed")
    raw_row = payload["row"]
    if not isinstance(raw_row, dict):
        raise CatalogHdlPackageContractError("row must be an object")
    context_name = _require_code(raw_row.get("ContextName"), "row.ContextName")
    provider_context = _provider_context(provider, context_name)
    dummy_receipt = {
        "exact_key": {
            "ContextName": raw_row.get("ContextName"),
            "ContentItemCode": raw_row.get("ContentItemCode"),
            "ContentItemValueSetName": raw_row.get("ContentItemValueSetName"),
            "Name": raw_row.get("Name"),
        },
        "catalog_name": raw_row.get("ContentItemValueSetName"),
    }
    row = _validate_row(
        raw_row,
        provider_context=provider_context,
        receipt=dummy_receipt,
    )
    return payload, provider_context, row, provider_sha256


def _validate_rest_readback(
    raw: Any,
    *,
    payload: Mapping[str, Any],
    provider_context: Mapping[str, Any],
    row: Mapping[str, str],
    catalog_code: str,
    catalog_name: str,
    as_of: datetime,
) -> dict[str, Any]:
    readback = _require_object(raw, REST_READBACK_KEYS, "rest_readback")
    body = {key: readback[key] for key in sorted(REST_READBACK_KEYS - {"evidence_sha256"})}
    if _sha256_bytes(_canonical_json(body)) != readback["evidence_sha256"]:
        raise CatalogHdlPackageContractError("REST readback evidence fingerprint is invalid")
    expected_key = {
        "ContextName": row["ContextName"],
        "ContentItemCode": row["ContentItemCode"],
        "Name": row["Name"],
    }
    if (
        readback["schema_version"] != SCHEMA_VERSION
        or readback["status"] != "complete"
        or readback["operation"] != "read-only-exact-code-and-name-check"
        or readback["provider"] != "CATALOG_REST"
        or readback["coverage"] != "complete"
        or readback["profile_mode"] != "enhanced"
        or readback["exact_provider_key"] != expected_key
    ):
        raise CatalogHdlPackageContractError("REST readback contract is incomplete or mismatched")
    if (
        readback["target_environment"] != payload["target_environment"]
        or readback["context_name"] != row["ContextName"]
        or readback["child_relation"] != provider_context["child_relation"]
    ):
        raise CatalogHdlPackageContractError("REST readback target or context is mismatched")
    if (
        readback["exact_code_match_count"] != 1
        or readback["exact_name_match_count"] != 1
        or readback["code_classification"] != "exact"
        or readback["name_classification"] != "exact"
    ):
        raise CatalogHdlPackageContractError("REST readback did not return one exact code and name")
    code_matches = readback["code_matches"]
    name_matches = readback["name_matches"]
    if not isinstance(code_matches, list) or not isinstance(name_matches, list) or len(code_matches) != 1 or len(name_matches) != 1:
        raise CatalogHdlPackageContractError("REST readback exact rows are malformed")
    for observed in (code_matches[0], name_matches[0]):
        if not isinstance(observed, dict) or observed.get("ContentItemCode") != row["ContentItemCode"] or observed.get("Name") != row["Name"]:
            raise CatalogHdlPackageContractError("REST readback exact rows do not identify the approved item")
    catalogs = readback["catalogs"]
    if not isinstance(catalogs, list):
        raise CatalogHdlPackageContractError("REST readback catalogs are malformed")
    selected = [
        catalog
        for catalog in catalogs
        if isinstance(catalog, dict)
        and catalog.get("catalog_code") == catalog_code
        and catalog.get("catalog_name") == catalog_name
    ]
    if len(selected) != 1 or selected[0].get("exact_code_match_count") != 1 or selected[0].get("exact_name_match_count") != 1:
        raise CatalogHdlPackageContractError("REST readback did not locate the exact item in the approved catalog")
    _validate_freshness(readback["captured_at"], readback["valid_through"], as_of=as_of)
    return readback


def verify_readback(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root)
    input_path = _inside_project(project_root, args.input_json, "input_json", must_exist=True)
    rest_path = _inside_project(project_root, args.rest_readback_json, "rest_readback_json", must_exist=True)
    export_path = _inside_project(project_root, args.item_catalog_export_zip, "item_catalog_export_zip", must_exist=True)
    output_path = _inside_project(project_root, args.output_json, "output_json")
    if output_path.exists():
        raise CatalogHdlPackageContractError("output_json already exists; refusing to overwrite")
    payload, provider_context, row, provider_sha256 = _approved_payload_for_readback(input_path)
    target = _require_alias(args.target_environment, "target_environment")
    source = _require_alias(args.source_environment, "source_environment")
    release = _require_alias(args.fusion_release, "fusion_release")
    if target != payload["target_environment"] or source != target:
        raise CatalogHdlPackageContractError("readback environment is not the approved same target")
    as_of = _parse_as_of(args.as_of)
    _validate_freshness(args.captured_at, args.valid_through, as_of=as_of)
    rest = _validate_rest_readback(
        _read_json(rest_path, "rest_readback_json"),
        payload=payload,
        provider_context=provider_context,
        row=row,
        catalog_code=args.catalog_code,
        catalog_name=args.catalog_name,
        as_of=as_of,
    )
    try:
        evidence = inspect_fsm_evidence(
            export_path,
            task_code="ORA_MANAGE_PROFILE_ITEM_CATALOG",
            source_environment_alias=source,
            target_environment_alias=target,
            fusion_release=release,
            purpose="readback",
            unfiltered_task_export=args.unfiltered_task_export is True,
        )
    except EvidenceContractError as error:
        raise CatalogHdlPackageContractError(
            f"Item Catalog readback export is unusable: {error}",
            "catalog_or_metadata_mismatch",
        ) from error
    if not evidence.usable_for_readback:
        raise CatalogHdlPackageContractError(
            "Item Catalog readback export is incomplete, filtered, or target-mismatched",
            "catalog_or_metadata_mismatch",
        )
    catalog_rows = [
        item
        for item in evidence.records_by_member[IC_MEMBER]
        if item.get("ContextName") == row["ContextName"]
        and item.get("ContentValueSetCode") == args.catalog_code
        and item.get("ValueSetName") == args.catalog_name
    ]
    if len(catalog_rows) != 1:
        raise CatalogHdlPackageContractError("Item Catalog export did not return one exact approved catalog")
    item_rows = [
        item
        for item in evidence.records_by_member[IC_CONTENT_ITEM_MEMBER]
        if item.get("ORA_TALENT_PROFILE_ITEM_CATALOG.ContextName") == row["ContextName"]
        and item.get("ORA_TALENT_PROFILE_ITEM_CATALOG.ContentValueSetCode") == args.catalog_code
        and item.get("ContextName") == row["ContextName"]
        and item.get("ContentItemCode") == row["ContentItemCode"]
        and item.get("Name") == row["Name"]
    ]
    if len(item_rows) != 1:
        raise CatalogHdlPackageContractError("Item Catalog export did not return one exact approved item row")
    exported = item_rows[0]
    differences = []
    for field in provider_context["row_fields"]:
        if field == "ContentItemValueSetName":
            observed = catalog_rows[0].get("ValueSetName", "")
        else:
            observed = exported.get(field, "")
        expected = row[field]
        if observed != expected:
            differences.append(field)
    if differences:
        raise CatalogHdlPackageContractError(
            "Item Catalog export differs from the approved row: " + ", ".join(sorted(differences))
        )
    material = {
        "schema_version": SCHEMA_VERSION,
        "status": "verified",
        "provider": CATALOG_HDL_PROVIDER,
        "provider_lifecycle": provider_context["lifecycle"]["status"],
        "target_environment": target,
        "fusion_release": release,
        "profile_mode": "enhanced",
        "context_name": row["ContextName"],
        "catalog_code": args.catalog_code,
        "catalog_name": args.catalog_name,
        "provider_contract_sha256": provider_sha256,
        "approved_input_sha256": _sha256_file(input_path),
        "provider_rows_fingerprint": payload["provider_rows_fingerprint"],
        "rest_readback_sha256": _sha256_file(rest_path),
        "rest_evidence_sha256": rest["evidence_sha256"],
        "item_catalog_export_path": args.item_catalog_export_zip,
        "item_catalog_export_sha256": evidence.archive_sha256,
        "item_catalog_member_sha256": dict(sorted(evidence.member_sha256.items())),
        "captured_at": args.captured_at,
        "valid_through": args.valid_through,
        "exact_rest_code_matches": 1,
        "exact_rest_name_matches": 1,
        "exact_export_catalog_matches": 1,
        "exact_export_item_matches": 1,
        "differing_fields": [],
        "duplicate_rerun_expected_result": "blocked-existing-key",
        "lifecycle_promotion_state": "requires-controlled-load-receipt-and-duplicate-rerun-evidence",
    }
    report = {**material, "verification_fingerprint": _sha256_bytes(_canonical_json(material))}
    _atomic_create(
        output_path,
        (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    return report


def fingerprint_input(args: argparse.Namespace) -> str:
    project_root = Path(args.project_root)
    input_path = _inside_project(project_root, args.input_json, "input_json", must_exist=True)
    payload = _require_object(_read_json(input_path, "input_json"), INPUT_KEYS, "input")
    return provider_rows_fingerprint(payload)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    fingerprint_parser = subparsers.add_parser(
        "fingerprint", help="Print the canonical provider-row fingerprint."
    )
    fingerprint_parser.add_argument("--project-root", required=True)
    fingerprint_parser.add_argument("--input-json", required=True)
    prepare_parser = subparsers.add_parser(
        "prepare", help="Build one deterministic lifecycle-gated catalog HDL ZIP."
    )
    prepare_parser.add_argument("--project-root", required=True)
    prepare_parser.add_argument("--input-json", required=True)
    prepare_parser.add_argument("--output-zip", required=True)
    prepare_parser.add_argument("--readiness-report", required=True)
    prepare_parser.add_argument("--as-of")
    verify_parser = subparsers.add_parser(
        "verify-readback",
        help="Verify exact REST and complete Item Catalog export readback.",
    )
    verify_parser.add_argument("--project-root", required=True)
    verify_parser.add_argument("--input-json", required=True)
    verify_parser.add_argument("--rest-readback-json", required=True)
    verify_parser.add_argument("--item-catalog-export-zip", required=True)
    verify_parser.add_argument("--source-environment", required=True)
    verify_parser.add_argument("--target-environment", required=True)
    verify_parser.add_argument("--fusion-release", default="unknown", help="Optional informational metadata; not an eligibility gate.")
    verify_parser.add_argument("--catalog-code", required=True)
    verify_parser.add_argument("--catalog-name", required=True)
    verify_parser.add_argument("--captured-at", required=True)
    verify_parser.add_argument("--valid-through", required=True)
    verify_parser.add_argument(
        "--unfiltered-task-export",
        action="store_true",
        required=True,
    )
    verify_parser.add_argument("--output-json", required=True)
    verify_parser.add_argument("--as-of")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "fingerprint":
            print(fingerprint_input(args))
            return 0
        if args.command == "verify-readback":
            print(json.dumps(verify_readback(args), indent=2, sort_keys=True))
            return 0
        print(json.dumps(prepare(args), indent=2, sort_keys=True))
        return 0
    except (
        CatalogHdlPackageContractError,
        ProviderContractError,
        EvidenceContractError,
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
    ) as error:
        failure_class = getattr(error, "failure_class", "input_validation")
        print(
            json.dumps(
                {"status": "blocked", "failure_class": failure_class, "message": str(error)}
            ),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
