#!/usr/bin/env python3
"""Prepare deterministic create-only FSM packages for GROW-8154 tasks.

This helper is deliberately local-only. It validates approved proposal rows,
fresh current-state evidence, and an export-derived package baseline, then
writes one immutable FSM ZIP plus a sanitized readiness receipt. It has no
OAuth, network, UCM, Data Loader, or Fusion mutation capability.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import stat
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from xml.etree import ElementTree


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from profile_content_library_fsm_evidence import (  # noqa: E402
    CONTENT_ITEM_DYNAMIC_FIELDS,
    DEFAULT_SEEDED_CONTENT_ITEM_CATALOG,
    DEFAULT_SEEDED_CONTENT_TYPE_CATALOG,
    METADATA_MEMBER,
    TASK_CONTRACTS,
    EvidenceContractError,
    content_item_requirements_from_properties,
    customer_layer_issues,
    inspect_fsm_evidence,
)
from seeded_profile_content_library_catalog import (  # noqa: E402
    SeededCatalog,
    SeededCatalogError,
    load_seeded_content_items,
    load_seeded_content_types,
)


SCHEMA_VERSION = "1.0"
MAX_PROPOSAL_BYTES = 8 * 1024 * 1024
MAX_MEMBER_BYTES = 32 * 1024 * 1024
MAX_ARCHIVE_BYTES = 64 * 1024 * 1024
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
SAFE_ALIAS_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
SAFE_RELEASE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._ -]{0,63}$")
ITEM_CATALOG_CONTENT_ITEM_CODE_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")
ITEM_CATALOG_CONTENT_ITEM_PROVIDER_REGISTRY = (
    SCRIPT_DIR.parent
    / "item-catalogs"
    / "references"
    / "catalog-content-item-fsm-provider.json"
)


class PackageContractError(ValueError):
    """Expected fail-closed task-package contract error."""

    def __init__(self, message: str, failure_class: str = "input_validation") -> None:
        super().__init__(message)
        self.failure_class = failure_class


@dataclass(frozen=True)
class PackageTaskContract:
    task_code: str
    task_name: str
    skill_id: str
    skill_path: str
    primary_member: str
    required_fields: Mapping[str, tuple[str, ...]]
    generated_empty_fields: Mapping[str, tuple[str, ...]]
    metadata_business_objects: frozenset[str]
    metadata_batch_names: frozenset[str]

    @property
    def headers(self) -> Mapping[str, tuple[str, ...]]:
        return TASK_CONTRACTS[self.task_code].headers


CT = "HRT_MANAGE_PROFILE_CONTENT_TYPES"
CI = "HRT_MANAGE_PROFILE_CONTENT_ITEMS"
EE = "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS"
IC = "ORA_MANAGE_PROFILE_ITEM_CATALOG"

PACKAGE_CONTRACTS: Mapping[str, PackageTaskContract] = {
    CT: PackageTaskContract(
        task_code=CT,
        task_name="Content Types",
        skill_id="hcm.hcm-tool.profile-management-content-library-configuration.content-types",
        skill_path=(
            "pillars/hcm/hcm-tool/profile-management-content-library-configuration/"
            "content-types/SKILL.md"
        ),
        primary_member="HRT_CONTENT_TYPES_B.csv",
        required_fields={
            "HRT_CONTENT_TYPES_B.csv": (
                "ContextName",
                "ViewInstanceName",
                "GroupingKey",
                "ContentTypeName",
            ),
            "ORA_HRT_CONTENT_PROPERTY.csv": (
                "HRT_CONTENT_TYPES_B.ContextName",
                "FieldName",
                "ContextName",
                "ViewInstanceName",
                "GroupingKey",
                "ColumnName",
            ),
            "ORA_HRT_CONTENT_TYPE_RLAT.csv": (
                "ContentTypeContextName",
                "RelatedContentTypeContextName",
                "ViewInstanceName",
                "GroupingKey",
                "ContextName",
                "RelationshipCode",
                "ContextName1",
                "DateFrom",
            ),
        },
        generated_empty_fields={
            "HRT_CONTENT_TYPES_B.csv": ("ModuleId", "ContentTypeId"),
            "ORA_HRT_CONTENT_PROPERTY.csv": ("ModuleId", "ContentTypePropId", "ContentTypeId"),
            "ORA_HRT_CONTENT_TYPE_RLAT.csv": (
                "ModuleId",
                "SGUID",
                "ContentTypeRlatId",
                "ContentTypeId",
                "RelatedContentTypeId",
                "ContentTypeId1",
                "ContentTypeId2",
            ),
        },
        metadata_business_objects=frozenset(
            {"HRT_CONTENT_TYPES_B", "ORA_HRT_CONTENT_PROPERTY", "ORA_HRT_CONTENT_TYPE_RLAT"}
        ),
        metadata_batch_names=frozenset(),
    ),
    CI: PackageTaskContract(
        task_code=CI,
        task_name="Content Items",
        skill_id="hcm.hcm-tool.profile-management-content-library-configuration.content-items",
        skill_path=(
            "pillars/hcm/hcm-tool/profile-management-content-library-configuration/"
            "content-items/SKILL.md"
        ),
        primary_member="HRT_CONTENT_ITEMS_B.csv",
        required_fields={
            "HRT_CONTENT_ITEMS_B.csv": (
                "ContextName",
                "Name",
                "ViewInstanceName",
                "GroupingKey",
                "ContentItemCode",
                "DateFrom",
            ),
            "ORA_HRT_CONTENT_ITEM_RLAT.csv": (
                "Name",
                "ContextName",
                "RelatedContentTypeContextName",
                "RelatedContentItemName",
                "ViewInstanceName",
                "GroupingKey",
                "RelationshipCode",
                "ContentItemName",
                "ContentTypeContextName",
                "DateFrom",
            ),
        },
        generated_empty_fields={
            "HRT_CONTENT_ITEMS_B.csv": (
                "ContentKeyflexId",
                "ModuleId",
                "ContentItemId",
                "ContentTypeId",
                "RatingModelId",
                "CountryId",
            ),
            "ORA_HRT_CONTENT_ITEM_RLAT.csv": (
                "ContentItemRlatId",
                "ContentTypeId",
                "ContentItemId",
                "RelatedContentTypeId",
                "RelatedContentItemId",
            ),
        },
        metadata_business_objects=frozenset(
            {"HRT_CONTENT_ITEMS_B", "ORA_HRT_CONTENT_ITEM_RDESC", "ORA_HRT_CONTENT_ITEM_RLAT"}
        ),
        metadata_batch_names=frozenset({"ContentItem"}),
    ),
    EE: PackageTaskContract(
        task_code=EE,
        task_name="Educational Establishments",
        skill_id="hcm.hcm-tool.profile-management-content-library-configuration.educational-establishments",
        skill_path=(
            "pillars/hcm/hcm-tool/profile-management-content-library-configuration/"
            "educational-establishments/SKILL.md"
        ),
        primary_member="HRT_SCHOOL.csv",
        required_fields={
            "HRT_SCHOOL.csv": (
                "SchoolCode",
                "ViewInstanceName",
                "GroupingKey",
                "Description",
                "Name",
            )
        },
        generated_empty_fields={
            "HRT_SCHOOL.csv": ("PartyId", "CountryId", "EstablishmentId", "StateProvinceId")
        },
        metadata_business_objects=frozenset({"HRT_SCHOOL"}),
        metadata_batch_names=frozenset({"EstablishmentVO"}),
    ),
    IC: PackageTaskContract(
        task_code=IC,
        task_name="Item Catalogs",
        skill_id="hcm.hcm-tool.profile-management-content-library-configuration.item-catalogs",
        skill_path=(
            "pillars/hcm/hcm-tool/profile-management-content-library-configuration/"
            "item-catalogs/SKILL.md"
        ),
        primary_member="ORA_TALENT_PROFILE_ITEM_CATALOG.csv",
        required_fields={
            "ORA_TALENT_PROFILE_ITEM_CATALOG.csv": (
                "ContentValueSetCode",
                "ContextName",
                "ViewInstanceName",
                "GroupingKey",
                "ValueSetName",
            ),
            "ORA_TALENT_CATALOG_CONTENT_ITEM.csv": (
                "ORA_TALENT_PROFILE_ITEM_CATALOG.ContentValueSetCode",
                "ORA_TALENT_PROFILE_ITEM_CATALOG.ContextName",
                "ContentValueSetCode",
                "Name",
                "ContextName",
                "ViewInstanceName",
                "GroupingKey",
                "ContentContextNameTransient",
                "ContentItemCode",
                "ContentSupplierCode",
                "DateFrom",
            ),
            "ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv": (
                "ORA_TALENT_PROFILE_ITEM_CATALOG.ContentValueSetCode",
                "ORA_TALENT_PROFILE_ITEM_CATALOG.ContextName",
                "ORA_TALENT_CATALOG_CONTENT_ITEM.ContentValueSetCode",
                "ORA_TALENT_CATALOG_CONTENT_ITEM.Name",
                "ORA_TALENT_CATALOG_CONTENT_ITEM.ContextName",
                "ContentValueSetCode",
                "Name",
                "ContextName",
                "RatingModelCode",
                "RatingLevelCode",
                "ViewInstanceName",
                "GroupingKey",
                "ReviewRatingDescr",
            ),
        },
        generated_empty_fields={
            "ORA_TALENT_PROFILE_ITEM_CATALOG.csv": (
                "ModuleId",
                "SeedDataSource",
                "ContentTypeId",
                "ContentValueSetId",
            ),
            "ORA_TALENT_CATALOG_CONTENT_ITEM.csv": (
                "ContentKeyflexId",
                "ModuleId",
                "ContentItemId",
                "ContentTypeId",
                "ContentValueSetId",
                "CountryId",
                "RatingModelId",
                "StateProvinceId",
            ),
            "ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv": (
                "RatingLevelId",
                "ContentItemId",
                "ContentTypeId",
                "ContentRatingDescId",
                "ContentValueSetId",
                "RatingModelId",
            ),
        },
        metadata_business_objects=frozenset(
            {
                "ORA_TALENT_PROFILE_ITEM_CATALOG",
                "ORA_TALENT_CATALOG_CONTENT_ITEM",
                "ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC",
            }
        ),
        metadata_batch_names=frozenset({"ContentTypeValueSet"}),
    ),
}

TOP_LEVEL_KEYS = {
    "schema_version",
    "operation",
    "task_code",
    "proposal_fingerprint",
    "provider_rows_fingerprint",
    "target_environment",
    "fusion_release",
    "current_state_receipt",
    "package_baseline_receipt",
    "dependency_evidence",
    "rows",
}
CURRENT_RECEIPT_KEYS = {
    "task_code",
    "target_environment",
    "fusion_release",
    "sha256",
    "captured_at",
    "valid_through",
    "complete",
    "unfiltered_task_export",
}
BASELINE_RECEIPT_KEYS = {
    "task_code",
    "target_environment",
    "fusion_release",
    "sha256",
    "captured_at",
    "valid_through",
    "kind",
}


@dataclass(frozen=True)
class CsvShape:
    rows: tuple[dict[str, str], ...]
    newline: str
    has_bom: bool


@dataclass(frozen=True)
class ArchiveShape:
    path: Path
    infos: tuple[zipfile.ZipInfo, ...]
    archive_comment: bytes
    raw_by_member: Mapping[str, bytes]
    csv_by_member: Mapping[str, CsvShape]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def provider_rows_fingerprint(value: Mapping[str, Any]) -> str:
    """Bind exact provider rows and dependency evidence to package approval."""
    material = {
        "schema_version": value.get("schema_version"),
        "operation": value.get("operation"),
        "task_code": value.get("task_code"),
        "proposal_fingerprint": value.get("proposal_fingerprint"),
        "target_environment": value.get("target_environment"),
        "fusion_release": value.get("fusion_release"),
        "dependency_evidence": value.get("dependency_evidence"),
        "rows": value.get("rows"),
    }
    if "catalog_set_contract" in value:
        material["catalog_set_contract"] = value["catalog_set_contract"]
    receipt = value.get("current_state_receipt")
    if isinstance(receipt, dict) and "status" in receipt:
        material["current_state_receipt"] = receipt
    return sha256_bytes(canonical_json_bytes(material))


def require_exact_keys(value: Any, expected: Iterable[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PackageContractError(f"{label} must be a JSON object")
    expected_set = set(expected)
    actual = set(value)
    if actual != expected_set:
        raise PackageContractError(
            f"{label} keys are invalid; missing={sorted(expected_set - actual)}, "
            f"unexpected={sorted(actual - expected_set)}"
        )
    return value


def require_text(value: Any, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise PackageContractError(f"{label} must be a string")
    if any(character in value for character in ("\x00", "\r", "\n")):
        raise PackageContractError(f"{label} contains a prohibited control character")
    if not allow_empty and not value:
        raise PackageContractError(f"{label} must not be empty")
    return value


def require_sha256(value: Any, label: str) -> str:
    text = require_text(value, label)
    if not SHA256_PATTERN.fullmatch(text):
        raise PackageContractError(f"{label} must contain 64 lowercase hexadecimal characters")
    return text


def parse_rfc3339(value: Any, label: str) -> datetime:
    text = require_text(value, label)
    try:
        parsed = datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text)
    except ValueError as exc:
        raise PackageContractError(f"{label} must be a valid RFC 3339 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise PackageContractError(f"{label} must include a timezone")
    return parsed


def resolve_project_path(project_root: Path, supplied: str, label: str, *, must_exist: bool) -> Path:
    candidate = Path(supplied).expanduser()
    if not candidate.is_absolute():
        candidate = project_root / candidate
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(project_root)
    except ValueError as exc:
        raise PackageContractError(
            f"{label} must resolve inside the selected project workspace", "artifact_persistence"
        ) from exc
    if must_exist and (not resolved.is_file() or resolved.is_symlink()):
        raise PackageContractError(
            f"{label} must be an existing regular project-local file", "artifact_persistence"
        )
    return resolved


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _validate_metadata(raw: bytes, contract: PackageTaskContract) -> None:
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise PackageContractError(
            "FSM metadata must not contain a DTD or entity declaration", "catalog_or_metadata_mismatch"
        )
    try:
        root = ElementTree.fromstring(raw.decode("utf-8-sig"))
    except (UnicodeError, ElementTree.ParseError) as exc:
        raise PackageContractError("FSM metadata is malformed", "catalog_or_metadata_mismatch") from exc

    def nonblank_values(name: str) -> set[str]:
        return {
            (element.text or "").strip()
            for element in root.iter()
            if _local_name(element.tag) == name and (element.text or "").strip()
        }

    if nonblank_values("ObjectShortName") != {contract.task_code}:
        raise PackageContractError("FSM metadata task identity is invalid", "catalog_or_metadata_mismatch")
    if nonblank_values("BusinessObjectShortName") != set(contract.metadata_business_objects):
        raise PackageContractError(
            "FSM metadata business-object identities are invalid", "catalog_or_metadata_mismatch"
        )
    if nonblank_values("BatchName") != set(contract.metadata_batch_names):
        raise PackageContractError("FSM metadata batch identities are invalid", "catalog_or_metadata_mismatch")


def _validate_zip_info(info: zipfile.ZipInfo, expected_members: frozenset[str]) -> None:
    if info.filename not in expected_members:
        raise PackageContractError("archive contains an unexpected member", "catalog_or_metadata_mismatch")
    if info.filename != Path(info.filename).name or "\\" in info.filename:
        raise PackageContractError("archive member is not at the root", "catalog_or_metadata_mismatch")
    if info.is_dir() or info.flag_bits & 0x1:
        raise PackageContractError(
            "archive contains a directory or encrypted member", "catalog_or_metadata_mismatch"
        )
    mode = (info.external_attr >> 16) & 0xFFFF
    if mode and stat.S_ISLNK(mode):
        raise PackageContractError("archive contains a symbolic-link member", "catalog_or_metadata_mismatch")
    if info.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}:
        raise PackageContractError("archive uses unsupported compression", "catalog_or_metadata_mismatch")
    if info.file_size > MAX_MEMBER_BYTES:
        raise PackageContractError("archive member exceeds the size limit", "catalog_or_metadata_mismatch")


def _parse_csv_shape(raw: bytes, header: Sequence[str], member: str) -> CsvShape:
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeError as exc:
        raise PackageContractError(f"{member} is not UTF-8", "catalog_or_metadata_mismatch") from exc
    if "\x00" in text:
        raise PackageContractError(f"{member} contains a NUL character", "catalog_or_metadata_mismatch")
    first_line = text.splitlines(keepends=True)[0] if text else ""
    if first_line.endswith("\r\n"):
        newline, header_text = "\r\n", first_line[:-2]
    elif first_line.endswith("\n"):
        newline, header_text = "\n", first_line[:-1]
    else:
        raise PackageContractError(f"{member} header must end with a newline", "catalog_or_metadata_mismatch")
    expected_header_text = ",".join(f'"{column}"' for column in header)
    if header_text != expected_header_text:
        raise PackageContractError(
            f"{member} header spelling, order, or quoting is invalid", "catalog_or_metadata_mismatch"
        )
    try:
        parsed = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as exc:
        raise PackageContractError(f"{member} is malformed", "catalog_or_metadata_mismatch") from exc
    if not parsed or tuple(parsed[0]) != tuple(header):
        raise PackageContractError(f"{member} header is invalid", "catalog_or_metadata_mismatch")
    rows: list[dict[str, str]] = []
    for row_number, row in enumerate(parsed[1:], start=2):
        if len(row) != len(header):
            raise PackageContractError(
                f"{member} row {row_number} has the wrong column count", "catalog_or_metadata_mismatch"
            )
        rows.append(dict(zip(header, row)))
    return CsvShape(tuple(rows), newline, has_bom)


def inspect_archive(path: Path, contract: PackageTaskContract) -> ArchiveShape:
    if path.stat().st_size > MAX_ARCHIVE_BYTES:
        raise PackageContractError("archive exceeds the local size limit", "catalog_or_metadata_mismatch")
    expected_members = frozenset((METADATA_MEMBER, *contract.headers.keys()))
    try:
        with zipfile.ZipFile(path, "r") as archive:
            infos = tuple(archive.infolist())
            names = [info.filename for info in infos]
            if frozenset(names) != expected_members or len(names) != len(expected_members):
                raise PackageContractError(
                    "archive member inventory does not match the task contract", "catalog_or_metadata_mismatch"
                )
            if len({name.casefold() for name in names}) != len(names):
                raise PackageContractError("archive has duplicate member names", "catalog_or_metadata_mismatch")
            for info in infos:
                _validate_zip_info(info, expected_members)
            bad_member = archive.testzip()
            if bad_member is not None:
                raise PackageContractError("archive integrity validation failed", "catalog_or_metadata_mismatch")
            raw_by_member = {name: archive.read(name) for name in names}
            archive_comment = archive.comment
    except (OSError, zipfile.BadZipFile) as exc:
        raise PackageContractError("archive is unreadable or corrupt", "artifact_persistence") from exc
    _validate_metadata(raw_by_member[METADATA_MEMBER], contract)
    csv_by_member = {
        member: _parse_csv_shape(raw_by_member[member], header, member)
        for member, header in contract.headers.items()
    }
    return ArchiveShape(path, infos, archive_comment, raw_by_member, csv_by_member)


def _validate_receipt(
    value: Any,
    expected_keys: set[str],
    label: str,
    *,
    contract: PackageTaskContract,
    actual_sha256: str,
    target: str,
    release: str,
    as_of: datetime,
) -> dict[str, Any]:
    receipt = require_exact_keys(value, expected_keys, label)
    if receipt["task_code"] != contract.task_code:
        raise PackageContractError(f"{label}.task_code does not match the selected task")
    if receipt["target_environment"] != target:
        raise PackageContractError(f"{label} is not bound to the selected target")
    if require_sha256(receipt["sha256"], f"{label}.sha256") != actual_sha256:
        raise PackageContractError(f"{label}.sha256 does not match the supplied archive")
    captured_at = parse_rfc3339(receipt["captured_at"], f"{label}.captured_at")
    valid_through = parse_rfc3339(receipt["valid_through"], f"{label}.valid_through")
    if captured_at > as_of or as_of > valid_through or captured_at > valid_through:
        raise PackageContractError(f"{label} is stale or has an invalid freshness window")
    return receipt


def _string_list(value: Any, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise PackageContractError(f"{label} must be an array")
    result = tuple(require_text(item, f"{label}[]") for item in value)
    if len(set(result)) != len(result):
        raise PackageContractError(f"{label} contains duplicate values")
    return result


def _tuple_list(value: Any, width: int, label: str) -> tuple[tuple[str, ...], ...]:
    if not isinstance(value, list):
        raise PackageContractError(f"{label} must be an array")
    result: list[tuple[str, ...]] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, list) or len(item) != width:
            raise PackageContractError(f"{label}[{index}] must contain exactly {width} strings")
        result.append(tuple(require_text(cell, f"{label}[{index}][]") for cell in item))
    if len(set(result)) != len(result):
        raise PackageContractError(f"{label} contains duplicate values")
    return tuple(result)


def _load_item_catalog_content_item_provider_registry(
    *,
    fusion_release: str,
) -> tuple[str, Mapping[str, Mapping[str, Any]]]:
    """Load the task-bound FSM contract; release labels are provenance only."""
    try:
        raw = ITEM_CATALOG_CONTENT_ITEM_PROVIDER_REGISTRY.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PackageContractError(
            "the Item Catalog Content Item FSM provider registry is unavailable",
            "catalog_or_metadata_mismatch",
        ) from exc
    if not isinstance(value, dict):
        raise PackageContractError(
            "the Item Catalog Content Item FSM provider registry is invalid",
            "catalog_or_metadata_mismatch",
        )
    expected = {
        "schema_version",
        "task_code",
        "task_name",
        "fusion_release",
        "provider",
        "parent_catalog_strategy",
        "source_product_releases",
        "supported_child_scope",
        "providers",
        "source_evidence",
    }
    if set(value) != expected or value["schema_version"] != "1.0":
        raise PackageContractError(
            "the Item Catalog Content Item FSM provider registry schema is invalid",
            "catalog_or_metadata_mismatch",
        )
    product_releases = _string_list(value["source_product_releases"], "source_product_releases")
    if not product_releases or any(
        not re.fullmatch(r"[0-9]+(?:\.[0-9]+){4}", release) for release in product_releases
    ):
        raise PackageContractError(
            "the Item Catalog FSM product-release contract is invalid",
            "catalog_or_metadata_mismatch",
        )
    if value["task_code"] != IC:
        raise PackageContractError(
            "the Item Catalog Content Item FSM provider registry is not bound to the selected task",
            "catalog_or_metadata_mismatch",
        )
    if value["parent_catalog_strategy"] != "existing-catalog-anchor":
        raise PackageContractError(
            "the Item Catalog Content Item FSM parent-catalog strategy is not supported",
            "catalog_or_metadata_mismatch",
        )
    if not isinstance(value["providers"], list):
        raise PackageContractError(
            "the Item Catalog Content Item FSM provider registry has no providers",
            "catalog_or_metadata_mismatch",
        )
    providers: dict[str, Mapping[str, Any]] = {}
    for index, provider in enumerate(value["providers"], start=1):
        if not isinstance(provider, dict) or set(provider) != {
            "context_name",
            "lifecycle",
            "allowed_supplier_codes",
        }:
            raise PackageContractError(
                "the Item Catalog Content Item FSM provider registry has an invalid provider entry",
                "catalog_or_metadata_mismatch",
            )
        context = require_text(provider["context_name"], f"provider[{index}].context_name")
        lifecycle = require_text(provider["lifecycle"], f"provider[{index}].lifecycle")
        if lifecycle not in {"certification-only", "verified"}:
            raise PackageContractError(
                "the Item Catalog Content Item FSM provider lifecycle is invalid",
                "catalog_or_metadata_mismatch",
            )
        supplier_codes = _string_list(
            provider["allowed_supplier_codes"],
            f"provider[{index}].allowed_supplier_codes",
        )
        if not supplier_codes or context in providers:
            raise PackageContractError(
                "the Item Catalog Content Item FSM provider registry contains duplicate or incomplete contexts",
                "catalog_or_metadata_mismatch",
            )
        providers[context] = {
            "lifecycle": lifecycle,
            "allowed_supplier_codes": supplier_codes,
        }
    return sha256_bytes(raw), providers


def _validate_dependency_evidence(task_code: str, value: Any, *, current_unavailable: bool = False) -> dict[str, Any]:
    if task_code == CT:
        evidence = require_exact_keys(
            value,
            {"known_content_type_contexts", "allowed_property_pairs", "evidence_fingerprints"},
            "dependency_evidence",
        )
        evidence["known_content_type_contexts"] = _string_list(
            evidence["known_content_type_contexts"], "dependency_evidence.known_content_type_contexts"
        )
        evidence["allowed_property_pairs"] = _tuple_list(
            evidence["allowed_property_pairs"], 2, "dependency_evidence.allowed_property_pairs"
        )
    elif task_code == CI:
        evidence = require_exact_keys(
            value,
            {
                "profile_mode",
                "content_type_contexts",
                "content_type_relationships",
                "rating_model_codes",
                "content_supplier_codes",
                "applicable_dynamic_fields_by_context",
                "evidence_fingerprints",
            },
            "dependency_evidence",
        )
        evidence["profile_mode"] = require_text(
            evidence["profile_mode"], "dependency_evidence.profile_mode"
        ).casefold()
        if evidence["profile_mode"] not in {"legacy", "enhanced"}:
            raise PackageContractError(
                "dependency_evidence.profile_mode must be legacy or enhanced"
            )
        evidence["content_type_contexts"] = _string_list(
            evidence["content_type_contexts"], "dependency_evidence.content_type_contexts"
        )
        evidence["content_type_relationships"] = _tuple_list(
            evidence["content_type_relationships"], 3, "dependency_evidence.content_type_relationships"
        )
        evidence["rating_model_codes"] = _string_list(
            evidence["rating_model_codes"], "dependency_evidence.rating_model_codes"
        )
        evidence["content_supplier_codes"] = _string_list(
            evidence["content_supplier_codes"],
            "dependency_evidence.content_supplier_codes",
        )
        dynamic = evidence["applicable_dynamic_fields_by_context"]
        if not isinstance(dynamic, dict):
            raise PackageContractError(
                "dependency_evidence.applicable_dynamic_fields_by_context must be an object"
            )
        normalized_dynamic: dict[str, tuple[str, ...]] = {}
        for context, fields in dynamic.items():
            context_name = require_text(context, "dynamic-field context")
            values = _string_list(fields, f"applicable_dynamic_fields_by_context.{context_name}")
            unknown = sorted(set(values) - set(CONTENT_ITEM_DYNAMIC_FIELDS))
            if unknown:
                raise PackageContractError("dependency evidence contains unsupported dynamic fields: " + ", ".join(unknown))
            normalized_dynamic[context_name] = values
        evidence["applicable_dynamic_fields_by_context"] = normalized_dynamic
    elif task_code == IC:
        evidence = require_exact_keys(
            value,
            {
                "content_type_contexts",
                "content_type_evidence_fingerprints",
                "profile_v2_evidence_sha256",
                "item_catalog_content_item_contexts",
                "content_supplier_codes",
                "item_catalog_content_item_provider_sha256",
                "item_catalog_content_item_provider_use",
                "evidence_fingerprints",
            },
            "dependency_evidence",
        )
        evidence["content_type_contexts"] = _string_list(
            evidence["content_type_contexts"],
            "dependency_evidence.content_type_contexts",
        )
        evidence["content_type_evidence_fingerprints"] = _string_list(
            evidence["content_type_evidence_fingerprints"],
            "dependency_evidence.content_type_evidence_fingerprints",
        )
        evidence["item_catalog_content_item_contexts"] = _string_list(
            evidence["item_catalog_content_item_contexts"],
            "dependency_evidence.item_catalog_content_item_contexts",
        )
        evidence["content_supplier_codes"] = _string_list(
            evidence["content_supplier_codes"],
            "dependency_evidence.content_supplier_codes",
        )
        if not evidence["content_type_contexts"]:
            raise PackageContractError(
                "dependency_evidence.content_type_contexts must contain at least one approved context"
            )
        if not evidence["content_type_evidence_fingerprints"]:
            raise PackageContractError(
                "dependency_evidence.content_type_evidence_fingerprints must contain approved evidence"
            )
        if not current_unavailable or evidence["profile_v2_evidence_sha256"] is not None:
            require_sha256(
                evidence["profile_v2_evidence_sha256"],
                "dependency_evidence.profile_v2_evidence_sha256",
            )
        require_sha256(
            evidence["item_catalog_content_item_provider_sha256"],
            "dependency_evidence.item_catalog_content_item_provider_sha256",
        )
        provider_use = require_text(
            evidence["item_catalog_content_item_provider_use"],
            "dependency_evidence.item_catalog_content_item_provider_use",
        )
        if provider_use not in {
            "not-applicable",
            "controlled-certification",
            "general-use",
        }:
            raise PackageContractError(
                "dependency_evidence.item_catalog_content_item_provider_use is invalid"
            )
        evidence["item_catalog_content_item_provider_use"] = provider_use
        for index, fingerprint in enumerate(
            evidence["content_type_evidence_fingerprints"], start=1
        ):
            require_sha256(
                fingerprint,
                "dependency_evidence.content_type_evidence_fingerprints[%d]" % index,
            )
    else:
        evidence = require_exact_keys(value, {"evidence_fingerprints"}, "dependency_evidence")
    evidence["evidence_fingerprints"] = _string_list(
        evidence["evidence_fingerprints"], "dependency_evidence.evidence_fingerprints"
    )
    for index, fingerprint in enumerate(evidence["evidence_fingerprints"], start=1):
        require_sha256(fingerprint, f"dependency_evidence.evidence_fingerprints[{index}]")
    return evidence


def _validate_date_fields(row: Mapping[str, str], label: str) -> None:
    parsed: dict[str, date] = {}
    for field in ("DateFrom", "DateTo"):
        if field not in row or not row[field]:
            continue
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", row[field]):
            raise PackageContractError(f"{label}.{field} must use YYYY-MM-DD")
        try:
            parsed[field] = date.fromisoformat(row[field])
        except ValueError as exc:
            raise PackageContractError(f"{label}.{field} must use YYYY-MM-DD") from exc
    if "DateFrom" in parsed and "DateTo" in parsed and parsed["DateTo"] < parsed["DateFrom"]:
        raise PackageContractError(f"{label}.DateTo must not precede DateFrom")


def _validate_rows(
    contract: PackageTaskContract,
    raw_rows: Any,
) -> dict[str, tuple[dict[str, str], ...]]:
    rows_object = require_exact_keys(raw_rows, contract.headers.keys(), "rows")
    result: dict[str, tuple[dict[str, str], ...]] = {}
    for member, header in contract.headers.items():
        member_rows = rows_object[member]
        if not isinstance(member_rows, list):
            raise PackageContractError(f"rows.{member} must be an array")
        validated: list[dict[str, str]] = []
        for index, raw in enumerate(member_rows, start=1):
            row = require_exact_keys(raw, header, f"rows.{member}[{index}]")
            normalized = {
                field: require_text(row[field], f"rows.{member}[{index}].{field}", allow_empty=True)
                for field in header
            }
            for field in contract.required_fields[member]:
                if not normalized[field] or normalized[field] != normalized[field].strip():
                    raise PackageContractError(
                        f"rows.{member}[{index}].{field} must be nonblank with no surrounding whitespace"
                    )
            for field in contract.generated_empty_fields[member]:
                if normalized[field]:
                    raise PackageContractError(
                        f"rows.{member}[{index}].{field} is generated by Fusion and must be empty"
                    )
            _validate_date_fields(normalized, f"rows.{member}[{index}]")
            if contract.task_code == IC and member == "ORA_TALENT_CATALOG_CONTENT_ITEM.csv":
                # The reviewed business input remains ISO-8601.  The FSM provider
                # serializes Item Catalog child dates in its export format.
                for field in ("DateFrom", "DateTo"):
                    if normalized[field]:
                        normalized[field] = normalized[field].replace("-", "/")
            validated.append(normalized)
        result[member] = tuple(validated)
    if not result[contract.primary_member]:
        raise PackageContractError(f"rows.{contract.primary_member} must contain at least one create row")
    return result


def _reject_duplicate_keys(rows: Sequence[Mapping[str, str]], fields: Sequence[str], label: str) -> None:
    keys = [tuple(row[field] for field in fields) for row in rows]
    if len(set(keys)) != len(keys):
        raise PackageContractError(f"{label} contains duplicate create keys")


def _validate_content_types(
    rows: Mapping[str, tuple[dict[str, str], ...]],
    current: Mapping[str, tuple[Mapping[str, str], ...]],
    dependencies: Mapping[str, Any],
    seeded_content_types: SeededCatalog,
) -> None:
    headers = rows["HRT_CONTENT_TYPES_B.csv"]
    properties = rows["ORA_HRT_CONTENT_PROPERTY.csv"]
    relationships = rows["ORA_HRT_CONTENT_TYPE_RLAT.csv"]
    _reject_duplicate_keys(headers, ("ContextName",), "Content Types")
    _reject_duplicate_keys(
        properties,
        ("ContextName", "FieldName"),
        "Content Type properties",
    )
    _reject_duplicate_keys(
        relationships,
        ("ContentTypeContextName", "RelatedContentTypeContextName"),
        "Content Type relationships",
    )
    proposed_contexts = {row["ContextName"] for row in headers}
    current_contexts = {row.get("ContextName", "") for row in current["HRT_CONTENT_TYPES_B.csv"]}
    seeded_contexts = {
        row.get("ContextName", "")
        for row in seeded_content_types.records_by_file["content-types.csv"]
    }
    for row in headers:
        if row["FreeFormFlag"] not in {"", "Y", "N"}:
            raise PackageContractError("Content Type FreeFormFlag must be blank, Y, or N")
        if row["ContextName"] in current_contexts or row["ContextName"] in seeded_contexts:
            raise PackageContractError(
                "a proposed Content Type matches the fresh-or-seeded duplicate lock"
            )
    allowed_pairs = set(dependencies["allowed_property_pairs"])
    for row in properties:
        if row["HRT_CONTENT_TYPES_B.ContextName"] not in proposed_contexts:
            raise PackageContractError("every Content Type property must belong to a proposed Content Type")
        if row["ContextName"] != row["HRT_CONTENT_TYPES_B.ContextName"]:
            raise PackageContractError("a Content Type property ContextName conflicts with its containing parent")
        if (row["FieldName"], row["ColumnName"]) not in allowed_pairs:
            raise PackageContractError("a Content Type property pair is not present in approved dependency evidence")
        if row["RequiredFlag"] not in {"", "Y", "N"}:
            raise PackageContractError("Content Type property RequiredFlag must be blank, Y, or N")
    dependency_contexts = set(dependencies["known_content_type_contexts"])
    unresolved_dependencies = dependency_contexts - current_contexts - seeded_contexts
    if unresolved_dependencies:
        raise PackageContractError(
            "a dependency Content Type is absent from fresh and seeded evidence"
        )
    known_contexts = dependency_contexts | proposed_contexts
    for row in relationships:
        if (row["ContextName"], row["ContextName1"]) != (
            row["ContentTypeContextName"], row["RelatedContentTypeContextName"]
        ):
            raise PackageContractError("Content Type relationship context aliases conflict with their endpoints")
        if row["ContentTypeContextName"] not in proposed_contexts:
            raise PackageContractError("every Content Type relationship source must be a proposed Content Type")
        if row["RelatedContentTypeContextName"] not in known_contexts:
            raise PackageContractError("a related Content Type does not resolve in approved dependency evidence")


def _validate_content_items(
    rows: Mapping[str, tuple[dict[str, str], ...]],
    current: Mapping[str, tuple[Mapping[str, str], ...]],
    dependencies: Mapping[str, Any],
    seeded_content_types: SeededCatalog,
    seeded_content_items: SeededCatalog,
) -> None:
    items = rows["HRT_CONTENT_ITEMS_B.csv"]
    relationships = rows["ORA_HRT_CONTENT_ITEM_RLAT.csv"]
    _reject_duplicate_keys(items, ("ContextName", "ContentItemCode"), "Content Items")
    # Legacy ContentItemVO UserKey is ContextName,Name; code is a separate guard.
    _reject_duplicate_keys(items, ("ContextName", "Name"), "Content Item provider identities")
    relationship_key = (
        "ContentTypeContextName",
        "ContentItemName",
        "RelatedContentTypeContextName",
        "RelatedContentItemName",
    )
    _reject_duplicate_keys(relationships, relationship_key, "Content Item relationships")
    known_contexts = set(dependencies["content_type_contexts"])
    allowed_rating_models = set(dependencies["rating_model_codes"])
    allowed_supplier_codes = set(dependencies["content_supplier_codes"])
    dynamic_by_context = dependencies["applicable_dynamic_fields_by_context"]
    current_items = current["HRT_CONTENT_ITEMS_B.csv"]
    current_keys = {(row.get("ContextName", ""), row.get("ContentItemCode", "")) for row in current_items}
    seeded_items = seeded_content_items.records_by_file["content-items.csv"]
    seeded_keys = {
        (row.get("ContextName", ""), row.get("ContentItemCode", ""))
        for row in seeded_items
    }
    existing_name_keys = {
        (row.get("ContextName", ""), row.get("Name", ""))
        for row in (*current_items, *seeded_items)
    }
    seeded_type_properties = seeded_content_types.records_by_file[
        "content-type-properties.csv"
    ]
    proposed_endpoints: set[tuple[str, str]] = set()
    if dependencies["profile_mode"] == "enhanced":
        if any(row["ContextName"] != "GOAL" for row in items):
            raise PackageContractError(
                "the FSM Content Item provider supports only GOAL rows when "
                "enhanced profiles are enabled; this failure does not authorize "
                "an alternate route and current V1 has no HDL/HSDL fallback",
                "catalog_or_metadata_mismatch",
            )
        raise PackageContractError(
            "the enhanced-profile GOAL FSM Content Item provider is blocked because "
            "the exported two-member package shape failed its companion-document "
            "transformation contract; require a corrected or independently certified "
            "provider before package construction",
            "catalog_or_metadata_mismatch",
        )
    for row in items:
        context = row["ContextName"]
        if row["ViewInstanceName"] != "ContentItem":
            raise PackageContractError(
                "Content Item ViewInstanceName must follow the approved task contract"
            )
        if row["GroupingKey"] != f"{row['Name']},{context}":
            raise PackageContractError(
                "Content Item GroupingKey must follow the approved task contract"
            )
        if context not in known_contexts:
            raise PackageContractError("a Content Item owning Content Type is not in approved dependency evidence")
        key = context, row["ContentItemCode"]
        if (key in current_keys or key in seeded_keys
                or (context, row["Name"]) in existing_name_keys):
            raise PackageContractError(
                "a proposed Content Item matches the fresh-or-seeded duplicate identity or code lock"
            )
        properties = [
            prop
            for prop in seeded_type_properties
            if prop.get("ContextName", "") == context
        ]
        required_inputs = content_item_requirements_from_properties(properties)[
            "input_required_fields"
        ]
        missing_required = sorted(field for field in required_inputs if not row[field])
        if missing_required:
            raise PackageContractError(
                "a Content Item omits fields required by its seeded Content Type: "
                + ", ".join(missing_required)
            )
        rating_model = row["RatingModelCode"]
        if rating_model and rating_model not in allowed_rating_models:
            raise PackageContractError("a Content Item RatingModelCode is not in approved dependency evidence")
        supplier_code = row["ContentSupplierCode"]
        if supplier_code and supplier_code not in allowed_supplier_codes:
            raise PackageContractError(
                "a Content Item ContentSupplierCode is not in approved dependency evidence"
            )
        allowed_dynamic = set(dynamic_by_context.get(context, ()))
        supplied_dynamic = {field for field in CONTENT_ITEM_DYNAMIC_FIELDS if row[field]}
        if supplied_dynamic - allowed_dynamic:
            raise PackageContractError("a Content Item supplies dynamic fields not enabled by its Content Type")
        proposed_endpoints.add((context, row["Name"]))
    current_endpoints = {
        (row.get("ContextName", ""), row.get("Name", "")) for row in current_items if row.get("Name", "")
    }
    seeded_endpoints = {
        (row.get("ContextName", ""), row.get("Name", ""))
        for row in seeded_items
        if row.get("Name", "")
    }
    endpoints = proposed_endpoints | current_endpoints | seeded_endpoints
    type_relationships = set(dependencies["content_type_relationships"])
    current_relationship_keys = {
        tuple(row.get(field, "") for field in relationship_key)
        for row in current["ORA_HRT_CONTENT_ITEM_RLAT.csv"]
    }
    for row in relationships:
        if row["MandatoryFlag"] not in {"", "Y", "N"}:
            raise PackageContractError("Content Item relationship MandatoryFlag must be blank, Y, or N")
        source = row["ContentTypeContextName"], row["ContentItemName"]
        related = row["RelatedContentTypeContextName"], row["RelatedContentItemName"]
        if (row["ContextName"], row["Name"]) != source:
            raise PackageContractError("Content Item relationship aliases conflict with the source endpoint identity")
        if source not in endpoints or related not in endpoints:
            raise PackageContractError("a Content Item relationship endpoint does not resolve exactly")
        type_key = (
            row["ContentTypeContextName"],
            row["RelatedContentTypeContextName"],
            row["RelationshipCode"],
        )
        if type_key not in type_relationships:
            raise PackageContractError("the corresponding Content Type relationship is not approved")
        if tuple(row[field] for field in relationship_key) in current_relationship_keys:
            raise PackageContractError("a proposed Content Item relationship already exists")


def _validate_educational_establishments(
    rows: Mapping[str, tuple[dict[str, str], ...]],
    current: Mapping[str, tuple[Mapping[str, str], ...]],
) -> None:
    establishments = rows["HRT_SCHOOL.csv"]
    _reject_duplicate_keys(establishments, ("SchoolCode",), "Educational Establishments")
    current_rows = current["HRT_SCHOOL.csv"]
    current_codes = {row.get("SchoolCode", "") for row in current_rows}
    for row in establishments:
        if row["ViewInstanceName"] != "EstablishmentVO" or row["GroupingKey"] != row["SchoolCode"]:
            raise PackageContractError(
                "Educational Establishment ViewInstanceName and GroupingKey must follow the approved task contract"
            )
        country_pair = bool(row["CountryCountryCode"]), bool(row["CountryGeographyCode"])
        state_pair = bool(row["StateCountryCode"]), bool(row["StateGeographyCode"])
        if country_pair[0] != country_pair[1] or state_pair[0] != state_pair[1]:
            raise PackageContractError("Educational Establishment geography codes must be supplied in pairs")
        if any(state_pair) and not all(country_pair):
            raise PackageContractError("state geography requires explicit country geography")
        code = row["SchoolCode"]
        if code in current_codes:
            raise PackageContractError(
                "a proposed Educational Establishment matches the fresh current-state duplicate lock"
            )


def _validate_item_catalogs(
    rows: Mapping[str, tuple[dict[str, str], ...]],
    current: Mapping[str, tuple[Mapping[str, str], ...]],
    dependencies: Mapping[str, Any],
    current_sha256: str | None,
    fusion_release: str,
    *,
    candidate_new_set: bool = False,
    complete_new_set: bool = False,
    existing_skill_canary: bool = False,
) -> None:
    catalogs = rows["ORA_TALENT_PROFILE_ITEM_CATALOG.csv"]
    content_items = rows["ORA_TALENT_CATALOG_CONTENT_ITEM.csv"]
    rating_descriptions = rows["ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv"]
    has_content_item = bool(content_items)
    if existing_skill_canary and current_sha256 is None:
        raise PackageContractError("existing SKILL certification requires supplied current parent evidence; do not automatically export",
                                   "catalog_or_metadata_mismatch")
    if rating_descriptions:
        raise PackageContractError(
            "Item Catalog Content Item FSM phase 1 blocks rating-description rows",
            "catalog_or_metadata_mismatch",
        )
    if candidate_new_set and (len(catalogs) != 1 or not content_items):
        raise PackageContractError("catalog-set validation requires one new catalog and supplied children")
    if has_content_item and not candidate_new_set and (len(catalogs) != 1 or len(content_items) != 1):
        raise PackageContractError(
            "Item Catalog Content Item FSM phase 1 requires exactly one parent-catalog anchor and one Content Item row",
            "catalog_or_metadata_mismatch",
        )
    _reject_duplicate_keys(
        catalogs,
        ("ContextName", "ContentValueSetCode"),
        "Item Catalogs",
    )
    normalized_names = [
        (row["ContextName"], " ".join(row["ValueSetName"].split()).casefold())
        for row in catalogs
    ]
    if len(set(normalized_names)) != len(normalized_names):
        raise PackageContractError(
            "Item Catalogs contain duplicate catalog names for one Content Type"
        )
    if current_sha256 is not None and dependencies["profile_v2_evidence_sha256"] != current_sha256:
        raise PackageContractError(
            "Profile V2 readiness evidence is not bound to the fresh current-state export",
            "catalog_or_metadata_mismatch",
        )
    evidence_fingerprints = set(dependencies["evidence_fingerprints"])
    required_fingerprints = set(dependencies["content_type_evidence_fingerprints"])
    if dependencies["profile_v2_evidence_sha256"] is not None:
        required_fingerprints.add(dependencies["profile_v2_evidence_sha256"])
    if not required_fingerprints.issubset(evidence_fingerprints):
        raise PackageContractError(
            "dependency evidence omits Profile V2 or Content Type evidence fingerprints",
            "catalog_or_metadata_mismatch",
        )
    current_catalogs = current["ORA_TALENT_PROFILE_ITEM_CATALOG.csv"]
    if current_sha256 is not None and not current_catalogs:
        raise PackageContractError(
            "a populated current Item Catalog export is required as indirect Profile V2 readiness evidence",
            "catalog_or_metadata_mismatch",
        )
    approved_contexts = set(dependencies["content_type_contexts"])
    current_keys = {
        (row.get("ContextName", ""), row.get("ContentValueSetCode", ""))
        for row in current_catalogs
    }
    current_names = {
        (
            row.get("ContextName", ""),
            " ".join(row.get("ValueSetName", "").split()).casefold(),
        )
        for row in current_catalogs
    }
    for row in catalogs:
        context = row["ContextName"]
        if context not in approved_contexts:
            raise PackageContractError(
                "an Item Catalog owning Content Type is not in approved dependency evidence"
            )
        if row["ViewInstanceName"] != "ContentTypeValueSet":
            raise PackageContractError(
                "Item Catalog ViewInstanceName must follow the approved task contract"
            )
        if row["GroupingKey"] != f"{context},{row['ContentValueSetCode']}":
            raise PackageContractError(
                "Item Catalog GroupingKey must follow the approved task contract"
            )
        key = context, row["ContentValueSetCode"]
        if key in current_keys and (not has_content_item or candidate_new_set):
            raise PackageContractError(
                "a proposed Item Catalog matches the fresh current-state provider-key duplicate lock"
            )
        name_key = context, " ".join(row["ValueSetName"].split()).casefold()
        if name_key in current_names and (not has_content_item or candidate_new_set):
            raise PackageContractError(
                "a proposed Item Catalog name already exists for the owning Content Type"
            )
    if not has_content_item:
        if dependencies["item_catalog_content_item_provider_use"] != "not-applicable":
            raise PackageContractError(
                "a catalog-only package must declare Item Catalog Content Item provider use as not-applicable",
                "catalog_or_metadata_mismatch",
            )
        return

    provider_sha, providers = _load_item_catalog_content_item_provider_registry(
        fusion_release=fusion_release
    )
    if dependencies["item_catalog_content_item_provider_sha256"] != provider_sha:
        raise PackageContractError(
            "Item Catalog Content Item provider evidence is not bound to the current provider registry",
            "catalog_or_metadata_mismatch",
        )
    parent = catalogs[0]
    context = parent["ContextName"]
    if context not in set(dependencies["item_catalog_content_item_contexts"]):
        raise PackageContractError(
            "the Content Item context is absent from approved Item Catalog FSM provider evidence",
            "catalog_or_metadata_mismatch",
        )
    provider = providers.get(context)
    if existing_skill_canary:
        from item_catalog_set_contract import registry
        candidate, _ = registry(existing_skill=True)
        provider = ({"context_name": context, "lifecycle": candidate["lifecycle"],
                     "allowed_supplier_codes": candidate["allowed_supplier_codes"]}
                    if context in candidate["contexts"] else None)
    if provider is None and complete_new_set:
        # New-set certification has an independent allowlist. It must not
        # promote a context into the verified existing-parent child route.
        from item_catalog_set_contract import registry as new_set_registry
        new_provider, _ = new_set_registry()
        if context in new_provider["contexts"]:
            provider = {"context_name": context, "lifecycle": new_provider["lifecycle"],
                        "allowed_supplier_codes": new_provider["allowed_supplier_codes"]}
    if provider is None:
        raise PackageContractError(
            "the Content Item context has no registered Item Catalog FSM provider",
            "catalog_or_metadata_mismatch",
        )
    if provider["lifecycle"] not in {"certification-only", "verified"}:
        raise PackageContractError(
            "the Item Catalog FSM provider lifecycle is not eligible for controlled creation",
            "catalog_or_metadata_mismatch",
        )
    provider_use = dependencies["item_catalog_content_item_provider_use"]
    if provider["lifecycle"] == "certification-only" and provider_use != "controlled-certification":
        raise PackageContractError(
            "a certification-only Item Catalog FSM provider requires controlled-certification use",
            "approval_blocker",
        )
    if provider["lifecycle"] == "verified" and provider_use not in {
        "controlled-certification",
        "general-use",
    }:
        raise PackageContractError(
            "a verified Item Catalog FSM provider requires controlled-certification or general-use",
            "approval_blocker",
        )
    parent_key = context, parent["ContentValueSetCode"]
    current_parent = [
        row
        for row in current_catalogs
        if (row.get("ContextName", ""), row.get("ContentValueSetCode", "")) == parent_key
    ]
    if current_sha256 is not None and not candidate_new_set and len(current_parent) != 1:
        raise PackageContractError(
            "the Content Item parent-catalog anchor must resolve to exactly one current Item Catalog row",
            "catalog_or_metadata_mismatch",
        )
    parent_business_fields = (
        "ContentValueSetCode",
        "ContextName",
        "ValueSetName",
        "ValueSetDescription",
    )
    differing_parent_fields = [
        field
        for field in parent_business_fields
        if current_sha256 is not None and not candidate_new_set and parent[field] != current_parent[0].get(field, "")
    ]
    if differing_parent_fields:
        raise PackageContractError(
            "the Content Item parent-catalog anchor differs from current evidence: "
            + ", ".join(differing_parent_fields),
            "catalog_or_metadata_mismatch",
        )

    names = [" ".join(item["Name"].split()).casefold() for item in content_items]
    codes = [item["ContentItemCode"].casefold() for item in content_items]
    if len(names) != len(set(names)) or len(codes) != len(set(codes)):
        raise PackageContractError("supplied catalog children contain duplicate Name or ContentItemCode identities")
    for item in content_items:
        _validate_item_catalog_child(item, parent, context, provider, dependencies, current)


def _validate_item_catalog_child(item, parent, context, provider, dependencies, current):
    """Shared portable child checks; caller owns existing/new parent policy."""
    if (
        item["ORA_TALENT_PROFILE_ITEM_CATALOG.ContentValueSetCode"]
        != parent["ContentValueSetCode"]
        or item["ORA_TALENT_PROFILE_ITEM_CATALOG.ContextName"] != context
        or item["ContentValueSetCode"] != parent["ContentValueSetCode"]
        or item["ContextName"] != context
        or item["ContentContextNameTransient"] != context
    ):
        raise PackageContractError(
            "the Content Item must reference the exact anchored Item Catalog and context",
            "catalog_or_metadata_mismatch",
        )
    if item["ViewInstanceName"] != "ContentItem":
        raise PackageContractError(
            "Item Catalog Content Item ViewInstanceName must equal ContentItem",
            "catalog_or_metadata_mismatch",
        )
    if item["GroupingKey"] != "%s,%s,%s" % (
        item["Name"],
        context,
        parent["ContentValueSetCode"],
    ):
        raise PackageContractError(
            "Item Catalog Content Item GroupingKey must equal Name,ContextName,ContentValueSetCode",
            "catalog_or_metadata_mismatch",
        )
    if len(item["ContentItemCode"]) > 30 or not ITEM_CATALOG_CONTENT_ITEM_CODE_PATTERN.fullmatch(
        item["ContentItemCode"]
    ):
        raise PackageContractError(
            "Item Catalog ContentItemCode must contain only letters, digits, or underscores and be at most 30 characters",
            "input_validation",
        )
    if item["Name"] != item["Name"].strip() or len(item["Name"]) > 700:
        raise PackageContractError(
            "Item Catalog Content Item Name must be trimmed and at most 700 characters",
            "input_validation",
        )
    if item["ContentSupplierCode"] not in set(dependencies["content_supplier_codes"]):
        raise PackageContractError(
            "Item Catalog ContentSupplierCode is not in approved dependency evidence",
            "catalog_or_metadata_mismatch",
        )
    if item["ContentSupplierCode"] not in set(provider["allowed_supplier_codes"]):
        raise PackageContractError(
            "Item Catalog ContentSupplierCode is not supported by the registered FSM provider",
            "catalog_or_metadata_mismatch",
        )
    allowed_item_fields = {
        "ORA_TALENT_PROFILE_ITEM_CATALOG.ContentValueSetCode",
        "ORA_TALENT_PROFILE_ITEM_CATALOG.ContextName",
        "ContentValueSetCode",
        "Name",
        "ContextName",
        "ViewInstanceName",
        "GroupingKey",
        "ContentContextNameTransient",
        "ContentItemCode",
        "ContentSupplierCode",
        "DateFrom",
        "DateTo",
        "ItemDescription",
    }
    unsupported_fields = sorted(
        field for field, value in item.items() if value and field not in allowed_item_fields
    )
    if unsupported_fields:
        raise PackageContractError(
            "Item Catalog Content Item FSM phase 1 blocks dynamic, rating, translation, and generated fields: "
            + ", ".join(unsupported_fields),
            "catalog_or_metadata_mismatch",
        )
    current_items = current["ORA_TALENT_CATALOG_CONTENT_ITEM.csv"]
    item_key = context, item["Name"], parent["ContentValueSetCode"]
    exact_items = [
        row
        for row in current_items
        if (
            row.get("ContextName", ""),
            row.get("Name", ""),
            row.get("ContentValueSetCode", ""),
        )
        == item_key
    ]
    if exact_items:
        raise PackageContractError(
            "a proposed Item Catalog Content Item matches the fresh current-state provider-key duplicate lock",
            "catalog_or_metadata_mismatch",
        )
    normalized_name = " ".join(item["Name"].split()).casefold()
    name_collisions = [
        row
        for row in current_items
        if (
            row.get("ContextName", "") == context
            and row.get("ContentValueSetCode", "") == parent["ContentValueSetCode"]
            and " ".join(row.get("Name", "").split()).casefold() == normalized_name
        )
    ]
    if name_collisions:
        raise PackageContractError(
            "a proposed Item Catalog Content Item has a case-insensitive name collision in the anchored catalog",
            "catalog_or_metadata_mismatch",
        )
    code_collisions = [
        row
        for row in current_items
        if row.get("ContentItemCode", "").casefold()
        == item["ContentItemCode"].casefold()
    ]
    if code_collisions:
        raise PackageContractError(
            "a proposed Item Catalog ContentItemCode already exists in the current Item Catalog export",
            "catalog_or_metadata_mismatch",
        )


def validate_export_omission(receipt: Any, task_code: str, target: str) -> dict[str, Any]:
    """Record an optional export honestly; absence never means an empty target."""
    receipt = require_exact_keys(receipt, {"status", "task_code", "target_environment", "diagnostic_reference"},
                                 "current_state_receipt")
    if task_code != IC or receipt["task_code"] != IC or receipt["target_environment"] != target:
        raise PackageContractError("optional current-state export applies only to the selected Item Catalog target")
    if not isinstance(receipt["status"], str) or receipt["status"] not in {"skipped", "failed"}:
        raise PackageContractError("optional current-state export status must be skipped or failed")
    reference = receipt["diagnostic_reference"]
    if reference is not None and (not isinstance(reference, str) or not SAFE_ALIAS_PATTERN.fullmatch(reference)):
        raise PackageContractError("export diagnostic_reference must be a sanitized artifact alias")
    if receipt["status"] == "failed" and reference is None:
        raise PackageContractError("failed export requires a diagnostic_reference")
    return receipt


def validate_proposal(
    proposal: Any,
    *,
    contract: PackageTaskContract,
    supplied_fingerprint: str,
    supplied_provider_rows_fingerprint: str,
    current_sha256: str | None,
    baseline_sha256: str,
    as_of: datetime,
    current_records: Mapping[str, tuple[Mapping[str, str], ...]],
    seeded_content_types: SeededCatalog | None = None,
    seeded_content_items: SeededCatalog | None = None,
    candidate_new_catalog_set: bool = False,
    complete_new_catalog_set: bool = False,
    existing_skill_canary: bool = False,
) -> tuple[dict[str, Any], dict[str, tuple[dict[str, str], ...]]]:
    expected_keys = TOP_LEVEL_KEYS | ({"catalog_set_contract"} if complete_new_catalog_set or existing_skill_canary else set())
    root = require_exact_keys(proposal, expected_keys, "proposal")
    if complete_new_catalog_set or existing_skill_canary:
        if (contract.task_code != IC
                or (existing_skill_canary and (complete_new_catalog_set or candidate_new_catalog_set))
                or (complete_new_catalog_set and not candidate_new_catalog_set)):
            raise PackageContractError("select one compatible Item Catalog certification mode")
        from item_catalog_set_contract import validate_binding
        try:
            validate_binding(root, existing_skill=existing_skill_canary)
        except (ValueError, KeyError, TypeError) as exc:
            raise PackageContractError("invalid catalog certification binding: " + str(exc)) from exc
    if candidate_new_catalog_set and contract.task_code != IC:
        raise PackageContractError("catalog-set candidate validation applies only to Item Catalogs")
    if root["schema_version"] != SCHEMA_VERSION or root["operation"] != "create":
        raise PackageContractError("only schema 1.0 create proposals are supported")
    if root["task_code"] != contract.task_code:
        raise PackageContractError("proposal.task_code does not match the selected task")
    fingerprint = require_sha256(root["proposal_fingerprint"], "proposal.proposal_fingerprint")
    if fingerprint != supplied_fingerprint:
        raise PackageContractError("proposal fingerprint does not match the approved fingerprint")
    row_fingerprint = require_sha256(
        root["provider_rows_fingerprint"], "proposal.provider_rows_fingerprint"
    )
    if row_fingerprint != supplied_provider_rows_fingerprint:
        raise PackageContractError(
            "provider-row fingerprint does not match the separately approved fingerprint"
        )
    if row_fingerprint != provider_rows_fingerprint(root):
        raise PackageContractError(
            "provider rows or dependency evidence changed after fingerprint approval"
        )
    target = require_text(root["target_environment"], "proposal.target_environment")
    release = require_text(root["fusion_release"], "proposal.fusion_release")
    if not SAFE_ALIAS_PATTERN.fullmatch(target):
        raise PackageContractError("target_environment must be a safe non-sensitive alias")
    if not SAFE_RELEASE_PATTERN.fullmatch(release):
        raise PackageContractError("fusion_release contains unsupported characters")
    if current_sha256 is None:
        validate_export_omission(root["current_state_receipt"], contract.task_code, target)
        if any(current_records.values()):
            raise PackageContractError("unavailable export cannot supply purported current-state rows")
    else:
        current_receipt = _validate_receipt(
            root["current_state_receipt"], CURRENT_RECEIPT_KEYS, "current_state_receipt",
            contract=contract, actual_sha256=current_sha256, target=target, release=release, as_of=as_of,
        )
        if current_receipt["complete"] is not True:
            raise PackageContractError("current_state_receipt.complete must be true")
        if current_receipt["unfiltered_task_export"] is not True:
            raise PackageContractError("current_state_receipt.unfiltered_task_export must be true")
    if contract.task_code == IC and isinstance(root["package_baseline_receipt"], dict) and root["package_baseline_receipt"].get("kind") == "reviewed-template":
        baseline_receipt = require_exact_keys(root["package_baseline_receipt"],
            {"kind", "task_code", "target_environment", "sha256"}, "package_baseline_receipt")
        if (baseline_receipt["task_code"] != IC or baseline_receipt["target_environment"] != target
                or require_sha256(baseline_receipt["sha256"], "package_baseline_receipt.sha256") != baseline_sha256):
            raise PackageContractError("reviewed template must match the selected task, target and archive")
    else:
        baseline_receipt = _validate_receipt(
            root["package_baseline_receipt"], BASELINE_RECEIPT_KEYS, "package_baseline_receipt",
            contract=contract, actual_sha256=baseline_sha256, target=target, release=release, as_of=as_of,
        )
        if baseline_receipt["kind"] not in {"template-only", "complete-export"}:
            raise PackageContractError("package_baseline_receipt.kind must be template-only or complete-export")
    dependencies = _validate_dependency_evidence(contract.task_code, root["dependency_evidence"],
                                               current_unavailable=current_sha256 is None)
    required_catalog_fingerprints: set[str] = set()
    if contract.task_code in {CT, CI}:
        if seeded_content_types is None:
            raise PackageContractError(
                "the integrity-validated seeded Content Types catalog is required",
                "catalog_or_metadata_mismatch",
            )
        required_catalog_fingerprints.add(seeded_content_types.manifest_sha256)
    if contract.task_code == CI:
        if seeded_content_items is None:
            raise PackageContractError(
                "the integrity-validated seeded Content Items catalog is required",
                "catalog_or_metadata_mismatch",
            )
        required_catalog_fingerprints.add(seeded_content_items.manifest_sha256)
    missing_catalog_fingerprints = required_catalog_fingerprints - set(
        dependencies["evidence_fingerprints"]
    )
    if missing_catalog_fingerprints:
        raise PackageContractError(
            "dependency evidence omits a required seeded catalog manifest fingerprint",
            "catalog_or_metadata_mismatch",
        )
    rows = _validate_rows(contract, root["rows"])
    if contract.task_code == CT:
        assert seeded_content_types is not None
        _validate_content_types(rows, current_records, dependencies, seeded_content_types)
    elif contract.task_code == CI:
        assert seeded_content_types is not None and seeded_content_items is not None
        _validate_content_items(
            rows,
            current_records,
            dependencies,
            seeded_content_types,
            seeded_content_items,
        )
    elif contract.task_code == IC:
        _validate_item_catalogs(
            rows,
            current_records,
            dependencies,
            current_sha256,
            root["fusion_release"],
            candidate_new_set=candidate_new_catalog_set,
            complete_new_set=complete_new_catalog_set,
            existing_skill_canary=existing_skill_canary,
        )
    else:
        _validate_educational_establishments(rows, current_records)
    return root, rows


def _encode_csv(rows: Sequence[Mapping[str, str]], header: Sequence[str], shape: CsvShape) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=header, quoting=csv.QUOTE_ALL, lineterminator=shape.newline)
    writer.writeheader()
    writer.writerows(rows)
    encoded = stream.getvalue().encode("utf-8")
    if shape.has_bom:
        encoded = b"\xef\xbb\xbf" + encoded
    if len(encoded) > MAX_MEMBER_BYTES:
        raise PackageContractError("generated CSV exceeds the member size limit")
    return encoded


def _clone_info(info: zipfile.ZipInfo) -> zipfile.ZipInfo:
    cloned = zipfile.ZipInfo(info.filename, date_time=info.date_time)
    cloned.compress_type = info.compress_type
    cloned.comment = info.comment
    cloned.extra = info.extra
    cloned.internal_attr = info.internal_attr
    cloned.external_attr = info.external_attr
    cloned.create_system = info.create_system
    cloned.create_version = info.create_version
    cloned.extract_version = info.extract_version
    cloned.flag_bits = info.flag_bits & 0x800
    return cloned


def _create_temp_path(parent: Path, suffix: str) -> Path:
    parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix=".profile-content-fsm-", suffix=suffix, dir=parent)
    os.close(descriptor)
    return Path(name)


def _write_zip(
    path: Path,
    baseline: ArchiveShape,
    generated_csv: Mapping[str, bytes],
) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.comment = baseline.archive_comment
        for info in baseline.infos:
            content = generated_csv.get(info.filename, baseline.raw_by_member[info.filename])
            archive.writestr(_clone_info(info), content)


def _publish_temp(temp_path: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if not destination.is_file() or destination.is_symlink():
            raise PackageContractError("output destination is not a regular file", "artifact_persistence")
        if sha256_file(destination) != sha256_file(temp_path):
            raise PackageContractError("output overwrite conflict; existing bytes differ", "artifact_persistence")
        temp_path.unlink()
        return
    os.replace(temp_path, destination)


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    modes = [bool(getattr(args, name, False)) for name in
             ("validate_new_catalog_set", "preview_new_catalog_set", "prepare_new_catalog_set")]
    skill_modes = [bool(getattr(args, name, False)) for name in
                   ("preview_existing_skill_canary", "prepare_existing_skill_canary")]
    if sum(modes + skill_modes) > 1:
        raise PackageContractError("select only one catalog certification mode")
    new_set_mode = modes[1] or modes[2]
    existing_skill_canary = any(skill_modes)
    controlled_mode = new_set_mode or existing_skill_canary
    project_root = Path(args.project_root).expanduser().resolve(strict=True)
    if not project_root.is_dir():
        raise PackageContractError(
            "project_root must be an existing project workspace", "artifact_persistence"
        )
    proposal_path = resolve_project_path(project_root, args.proposal_json, "proposal_json", must_exist=True)
    current_path = (resolve_project_path(project_root, args.current_state_zip, "current_state_zip", must_exist=True)
                    if args.current_state_zip else None)
    baseline_path = resolve_project_path(project_root, args.baseline_zip, "baseline_zip", must_exist=True)
    output_path = resolve_project_path(project_root, args.output_zip, "output_zip", must_exist=False)
    report_path = resolve_project_path(
        project_root, args.readiness_report, "readiness_report", must_exist=False
    )
    if output_path.suffix.lower() != ".zip" or report_path.suffix.lower() != ".json":
        raise PackageContractError(
            "output_zip must end in .zip and readiness_report must end in .json", "artifact_persistence"
        )
    paths = [proposal_path, baseline_path, output_path, report_path]
    if current_path is not None:
        paths.append(current_path)
    if len(set(paths)) != len(paths):
        raise PackageContractError("input and output paths must be distinct", "artifact_persistence")
    contract = PACKAGE_CONTRACTS.get(args.task_code)
    if contract is None:
        raise PackageContractError("unsupported GROW-8154 task code")
    supplied_fingerprint = require_sha256(args.proposal_fingerprint, "proposal_fingerprint")
    supplied_provider_rows_fingerprint = require_sha256(
        args.provider_rows_fingerprint, "provider_rows_fingerprint"
    )
    as_of = parse_rfc3339(args.as_of, "as_of")
    if proposal_path.stat().st_size > MAX_PROPOSAL_BYTES:
        raise PackageContractError("proposal JSON exceeds the size limit")
    try:
        proposal_bytes = proposal_path.read_bytes()
        proposal = json.loads(proposal_bytes.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PackageContractError("proposal JSON is unreadable or malformed", "artifact_persistence") from exc

    if current_path is None:
        validate_export_omission(proposal.get("current_state_receipt"), contract.task_code,
                                 proposal.get("target_environment"))
    current_sha = sha256_file(current_path) if current_path is not None else None
    baseline_sha = sha256_file(baseline_path)
    current_records = {member: () for member in contract.headers}
    try:
        current_evidence = inspect_fsm_evidence(
            current_path,
            task_code=contract.task_code,
            source_environment_alias=proposal.get("target_environment", ""),
            target_environment_alias=proposal.get("target_environment", ""),
            fusion_release=proposal.get("fusion_release", ""),
            purpose="current-state",
            unfiltered_task_export=(
                proposal.get("current_state_receipt", {}).get(
                    "unfiltered_task_export"
                )
                is True
            ),
        ) if current_path is not None else None
        baseline_evidence = inspect_fsm_evidence(
            baseline_path,
            task_code=contract.task_code,
            source_environment_alias=proposal.get("target_environment", ""),
            fusion_release=proposal.get("fusion_release", ""),
            purpose="schema",
        )
    except EvidenceContractError as exc:
        raise PackageContractError(str(exc), "catalog_or_metadata_mismatch") from exc
    customer_issues = customer_layer_issues(
        current_evidence,
        contract.task_code,
        allow_header_only_with_seed=contract.task_code in {CT, CI},
    ) if current_evidence is not None else []
    if customer_issues:
        raise PackageContractError(
            "current-state archive is not usable as an unfiltered same-target customer layer: "
            + "; ".join(customer_issues),
            "catalog_or_metadata_mismatch",
        )
    if baseline_evidence.status != "ready":
        raise PackageContractError("package baseline schema is not ready", "catalog_or_metadata_mismatch")
    if current_path is not None:
        inspect_archive(current_path, contract)
        current_records = current_evidence.records_by_member
    baseline = inspect_archive(baseline_path, contract)
    if (current_path is not None and sha256_file(current_path) != current_sha) or sha256_file(baseline_path) != baseline_sha:
        raise PackageContractError(
            "current-state or baseline archive changed during validation",
            "artifact_persistence",
        )
    seeded_content_types: SeededCatalog | None = None
    seeded_content_items: SeededCatalog | None = None
    try:
        if contract.task_code in {CT, CI}:
            seeded_content_types = load_seeded_content_types(
                DEFAULT_SEEDED_CONTENT_TYPE_CATALOG,
                expected_release=proposal.get("fusion_release", ""),
            )
        if contract.task_code == CI:
            seeded_content_items = load_seeded_content_items(
                DEFAULT_SEEDED_CONTENT_ITEM_CATALOG,
                expected_release=proposal.get("fusion_release", ""),
            )
    except SeededCatalogError as exc:
        raise PackageContractError(str(exc), "catalog_or_metadata_mismatch") from exc
    proposal, rows = validate_proposal(
        proposal,
        contract=contract,
        supplied_fingerprint=supplied_fingerprint,
        supplied_provider_rows_fingerprint=supplied_provider_rows_fingerprint,
        current_sha256=current_sha,
        baseline_sha256=baseline_sha,
        as_of=as_of,
        current_records=current_records,
        seeded_content_types=seeded_content_types,
        seeded_content_items=seeded_content_items,
        candidate_new_catalog_set=any(modes),
        complete_new_catalog_set=new_set_mode,
        existing_skill_canary=existing_skill_canary,
    )
    if proposal["package_baseline_receipt"]["kind"] == "template-only" and any(
        shape.rows for shape in baseline.csv_by_member.values()
    ):
        raise PackageContractError(
            "template-only baseline contains business rows", "catalog_or_metadata_mismatch"
        )

    new_set_fingerprint = None
    export_checks = {
        "pre_import_export": proposal["current_state_receipt"] if current_path is None else {"status": "completed", "sha256": current_sha},
        "unverified_checks": ["target_duplicates", "existing_parent_no_drift", "profile_v2_export_preflight"] if current_path is None else [],
    }
    if controlled_mode:
        from item_catalog_set_contract import preview, require_approval
        try:
            if modes[1] or skill_modes[0]:
                result = preview(proposal, existing_skill=existing_skill_canary)
                result.update(export_checks)
                return result
            approval_arg = "existing_skill_canary_approval" if existing_skill_canary else "new_catalog_set_approval"
            new_set_fingerprint = require_approval(proposal, getattr(args, approval_arg, None), existing_skill=existing_skill_canary)
        except (ValueError, KeyError, TypeError) as exc:
            raise PackageContractError("catalog certification package approval failed: " + str(exc), "approval_blocker") from exc

    if modes[0]:
        # Deliberately return before any temporary ZIP/report is created. The
        # existing verified registry and task rules do NOT certify this shape.
        return {
            "schema_version": SCHEMA_VERSION,
            "status": "candidate_validation_only",
            "task_code": IC,
            "target_environment": proposal["target_environment"],
            "proposal_fingerprint": supplied_fingerprint,
            "provider_rows_fingerprint": supplied_provider_rows_fingerprint,
            "current_state_sha256": current_sha,
            "package_baseline_sha256": baseline_sha,
            "row_counts": {member: len(rows[member]) for member in contract.headers},
            "package_created": False,
            "creation_authorized": False,
            "execution_blockers": [
                "New-parent/multiple-child task-rule and provider lifecycle approval is outstanding.",
                "Independent complete new-catalog-set runtime readback is unproven.",
            ],
            "side_effects": [],
        }

    generated_csv = {
        member: _encode_csv(rows[member], header, baseline.csv_by_member[member])
        for member, header in contract.headers.items()
    }
    temp_zip = _create_temp_path(output_path.parent, ".zip")
    temp_report: Path | None = None
    try:
        _write_zip(temp_zip, baseline, generated_csv)
        final = inspect_archive(temp_zip, contract)
        if final.raw_by_member[METADATA_MEMBER] != baseline.raw_by_member[METADATA_MEMBER]:
            raise PackageContractError(
                "final metadata bytes differ from the approved baseline", "catalog_or_metadata_mismatch"
            )
        if [info.filename for info in final.infos] != [info.filename for info in baseline.infos]:
            raise PackageContractError(
                "final archive member order differs from the baseline", "catalog_or_metadata_mismatch"
            )
        for member in contract.headers:
            if final.csv_by_member[member].rows != rows[member]:
                raise PackageContractError(
                    f"final {member} rows differ from the approved proposal", "catalog_or_metadata_mismatch"
                )
        package_sha = sha256_file(temp_zip)
        row_counts = {member: len(rows[member]) for member in contract.headers}
        header_sha256 = {}
        for member in contract.headers:
            header_source = generated_csv[member]
            if header_source.startswith(b"\xef\xbb\xbf"):
                header_source = header_source[3:]
            header_sha256[member] = sha256_bytes(header_source.splitlines()[0])
        validation_basis = {
            "task_code": contract.task_code,
            "proposal_fingerprint": supplied_fingerprint,
            "provider_rows_fingerprint": supplied_provider_rows_fingerprint,
            "target_environment": proposal["target_environment"],
            "fusion_release": proposal["fusion_release"],
            "current_state_sha256": current_sha,
            "package_baseline_sha256": baseline_sha,
            "package_sha256": package_sha,
            "row_counts": row_counts,
            "members": [info.filename for info in final.infos],
            "seeded_catalog_manifest_sha256": sorted(
                catalog.manifest_sha256
                for catalog in (seeded_content_types, seeded_content_items)
                if catalog is not None
            ),
        }
        if contract.task_code == IC:
            validation_basis.update(export_checks)
            validation_basis["item_catalog_content_item_provider_sha256"] = proposal[
                "dependency_evidence"
            ]["item_catalog_content_item_provider_sha256"]
            validation_basis["item_catalog_content_item_provider_use"] = proposal[
                "dependency_evidence"
            ]["item_catalog_content_item_provider_use"]
        if controlled_mode:
            validation_basis["catalog_set_fingerprint"] = new_set_fingerprint
            validation_basis["catalog_set_contract"] = proposal["catalog_set_contract"]
        report: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "status": "package_ready_for_core_data_loader_preview",
            "failure_class": None,
            "skill_id": contract.skill_id,
            "task_code": contract.task_code,
            "task_name": contract.task_name,
            "target_environment": proposal["target_environment"],
            "fusion_release": proposal["fusion_release"],
            "as_of": args.as_of,
            "operation": "create",
            "proposal_fingerprint": supplied_fingerprint,
            "provider_rows_fingerprint": supplied_provider_rows_fingerprint,
            "proposal_input_sha256": sha256_bytes(proposal_bytes),
            "current_state_sha256": current_sha,
            "package_baseline_sha256": baseline_sha,
            "package_baseline_kind": proposal["package_baseline_receipt"]["kind"],
            "package_path": output_path.relative_to(project_root).as_posix(),
            "package_sha256": package_sha,
            "metadata_sha256": sha256_bytes(final.raw_by_member[METADATA_MEMBER]),
            "csv_header_sha256": dict(sorted(header_sha256.items())),
            "member_order": [info.filename for info in final.infos],
            "row_counts": dict(sorted(row_counts.items())),
            "dependency_evidence_count": len(proposal["dependency_evidence"]["evidence_fingerprints"]),
            "seeded_catalogs": [
                catalog.sanitized_summary()
                for catalog in (seeded_content_types, seeded_content_items)
                if catalog is not None
            ],
            "metadata_preserved": True,
            "final_archive_reopened_and_validated": True,
            "validation_fingerprint": sha256_bytes(canonical_json_bytes(validation_basis)),
            "data_loader_handoff": {
                "route": "core.data-loader",
                "source_type": "FSM",
                "task_hook_required": True,
                "task_name": contract.task_name,
                "task_context_requirements": {
                    "task_code": contract.task_code,
                    "task_name": contract.task_name,
                    "skill_path": contract.skill_path,
                    "offering": "HCM Tool",
                    "functional_area": "Profile Management Content Library Configuration",
                    "sequence": "select the exact positive sequence from persisted task context",
                },
                "task_hook_final_data": {
                    "archiveSha256": package_sha,
                    "packageReadinessFingerprint": sha256_bytes(canonical_json_bytes(validation_basis)),
                    "proposalFingerprint": supplied_fingerprint,
                    "providerRowsFingerprint": supplied_provider_rows_fingerprint,
                    "sourceType": "FSM",
                    "operation": "create",
                },
                "approval_state": "not_requested",
            },
            "side_effects": ["project-local immutable package and readiness report only"],
            "next_action": (
                "Start a separate core.data-loader preview for this exact package SHA-256. "
                "Do not upload until Task Hook validation passes and the user separately approves the preview."
            ),
        }
        if contract.task_code == IC:
            report.update(export_checks)
            report["data_loader_handoff"]["task_hook_final_data"].update(
                preImportExport=export_checks["pre_import_export"],
                unverifiedChecks=export_checks["unverified_checks"],
            )
            report["item_catalog_content_item_provider_sha256"] = proposal[
                "dependency_evidence"
            ]["item_catalog_content_item_provider_sha256"]
            report["item_catalog_content_item_provider_use"] = proposal[
                "dependency_evidence"
            ]["item_catalog_content_item_provider_use"]
            report["item_catalog_content_item_scope"] = (
                "one new catalog with all supplied portable children"
                if new_set_mode else "one create-only child row with one exact existing-catalog anchor"
                if rows["ORA_TALENT_CATALOG_CONTENT_ITEM.csv"]
                else "catalog-row-only"
            )
        if controlled_mode:
            report["catalog_set_fingerprint"] = new_set_fingerprint
            report["catalog_set_capability"] = proposal["catalog_set_contract"]["capability_id"]
            report["catalog_set_registry_sha256"] = proposal["catalog_set_contract"]["registry_sha256"]
            report["catalog_set_lifecycle"] = "certification-only"
            report["runtime_verified"] = False
            report["data_loader_handoff"]["task_hook_final_data"].update(
                catalogSetFingerprint=new_set_fingerprint,
                catalogSetCapability=report["catalog_set_capability"],
                catalogSetRegistrySha256=report["catalog_set_registry_sha256"],
                catalogSetUse="controlled-certification",
            )
        report_bytes = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n"
        temp_report = _create_temp_path(report_path.parent, ".json")
        temp_report.write_bytes(report_bytes)
        if report_path.exists() and (
            not report_path.is_file()
            or report_path.is_symlink()
            or sha256_file(report_path) != sha256_file(temp_report)
        ):
            raise PackageContractError(
                "readiness report overwrite conflict; existing bytes differ", "artifact_persistence"
            )
        _publish_temp(temp_zip, output_path)
        _publish_temp(temp_report, report_path)
        temp_report = None
        return report
    finally:
        if temp_zip.exists():
            temp_zip.unlink()
        if temp_report is not None and temp_report.exists():
            temp_report.unlink()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--task-code", required=True, choices=sorted(PACKAGE_CONTRACTS))
    parser.add_argument("--proposal-json", required=True)
    parser.add_argument("--proposal-fingerprint", required=True)
    parser.add_argument("--provider-rows-fingerprint", required=True)
    parser.add_argument("--current-state-zip", help="Omit for ordinary Item Catalog imports with a skipped receipt; supplied current evidence is required for existing SKILL certification and other tasks")
    parser.add_argument("--baseline-zip", required=True, help="Validated package/template metadata; Item Catalogs may reuse a reviewed template without exporting")
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--output-zip", required=True)
    parser.add_argument("--readiness-report", required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--validate-new-catalog-set", action="store_true",
        help="Validate a new catalog and supplied children locally; creates no ZIP or readiness file and grants no import authority",
    )
    mode.add_argument("--preview-new-catalog-set", action="store_true",
                      help="Validate and display the complete new-set package preview; no files written")
    mode.add_argument("--prepare-new-catalog-set", action="store_true",
                      help="Prepare one new catalog and all supplied portable children for controlled certification")
    mode.add_argument("--preview-existing-skill-canary", action="store_true",
                      help="Preview one SKILL child in an evidenced existing custom catalog; no files or Fusion calls")
    mode.add_argument("--prepare-existing-skill-canary", action="store_true",
                      help="Prepare one approved non-production existing-catalog SKILL certification package")
    parser.add_argument("--existing-skill-canary-approval",
                        help="Exact PREPARE EXISTING SKILL CANARY statement; local preparation only")
    parser.add_argument("--new-catalog-set-approval",
                        help="Exact PREPARE CATALOG SET statement from the complete package preview; not upload approval")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = prepare(args)
    except PackageContractError as exc:
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "failure_class": exc.failure_class,
                    "message": str(exc),
                    "side_effects": [],
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1
    except (OSError, ValueError) as exc:
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "failure_class": "artifact_persistence",
                    "message": f"local artifact operation failed: {type(exc).__name__}",
                    "side_effects": [],
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
