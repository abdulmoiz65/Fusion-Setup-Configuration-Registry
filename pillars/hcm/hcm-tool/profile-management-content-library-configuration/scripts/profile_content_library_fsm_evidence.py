#!/usr/bin/env python3
"""Inspect and compare GROW-8154 FSM export evidence without side effects.

The module uses only the Python standard library. It never writes an archive,
calls a network service, authenticates to Fusion, or invokes Data Loader. The
CLI emits a sanitized evidence summary; business rows remain in memory only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import stat
import sys
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from seeded_profile_content_library_catalog import (  # noqa: E402
    SeededCatalog,
    SeededCatalogError,
    load_seeded_content_items,
    load_seeded_content_types,
)
from build_profile_content_library_preview import contains_sensitive  # noqa: E402


METADATA_MEMBER = "ASM_SETUP_CSV_METADATA.xml"
MAX_ARCHIVE_MEMBERS = 32
MAX_MEMBER_BYTES = 32 * 1024 * 1024
MAX_ARCHIVE_UNCOMPRESSED_BYTES = 64 * 1024 * 1024
SAFE_LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
SENSITIVE_ARCHIVE_NAME = re.compile(
    r"(?i)(?:https?(?:%3A|:)|@|[A-Za-z0-9.-]+\.(?:oraclecloud|oracle)\.com)"
)
HEADER_ONLY_BLOCKER = (
    "Header-only evidence is schema evidence and cannot prove target current-state completeness."
)
DEFAULT_SEEDED_CONTENT_TYPE_CATALOG = (
    SCRIPT_DIR.parent / "assets" / "seeded-content-types"
)
DEFAULT_SEEDED_CONTENT_ITEM_CATALOG = (
    SCRIPT_DIR.parent / "assets" / "seeded-content-items"
)


class EvidenceContractError(ValueError):
    """Raised when an archive or comparison input violates the local contract."""


@dataclass(frozen=True)
class TaskContract:
    task_code: str
    headers: Mapping[str, tuple[str, ...]]

    @property
    def expected_members(self) -> frozenset[str]:
        return frozenset((METADATA_MEMBER, *self.headers.keys()))


CONTENT_TYPE_HEADER = (
    "ContextName",
    "ViewInstanceName",
    "GroupingKey",
    "ContentTypeName",
    "ContentDescription",
    "FreeFormFlag",
    "ModuleId",
    "ContentTypeId",
)

CONTENT_TYPE_PROPERTY_HEADER = (
    "HRT_CONTENT_TYPES_B.ContextName",
    "FieldName",
    "ContextName",
    "ViewInstanceName",
    "GroupingKey",
    "AttributeLabel",
    "ColumnName",
    "DefaultValue",
    "RequiredFlag",
    "DisplayCode",
    "ViewAttrbName",
    "ModuleId",
    "ContentTypePropId",
    "ContentTypeId",
)

CONTENT_TYPE_RELATIONSHIP_HEADER = (
    "ContentTypeContextName",
    "RelatedContentTypeContextName",
    "ViewInstanceName",
    "GroupingKey",
    "ContextName",
    "RelationshipCode",
    "ModuleId",
    "ContextName1",
    "DateFrom",
    "DateTo",
    "RatingInteractionType",
    "SGUID",
    "ContentTypeRlatId",
    "ContentTypeId",
    "RelatedContentTypeId",
    "ContentTypeId1",
    "ContentTypeId2",
)

CONTENT_ITEM_HEADER = (
    "ContextName",
    "Name",
    "ViewInstanceName",
    "GroupingKey",
    "ContentItemCode",
    "ItemDescription",
    "DateFrom",
    "DateTo",
    "ContentSupplierCode",
    "ContentKeyflexId",
    *(f"ItemTextTl{index}" for index in range(1, 16)),
    "ItemDescrlong",
    *(f"ItemNumber{index}" for index in range(1, 11)),
    *(f"ItemDate{index}" for index in range(1, 11)),
    *(f"ItemText{index}" for index in range(1, 31)),
    "ModuleId",
    "CountryCountryCode",
    "RatingModelCode",
    "ItemClobTl2",
    "ContentItemId",
    "ContentTypeId",
    "RatingModelId",
    "CountryId",
)

CONTENT_ITEM_RELATIONSHIP_HEADER = (
    "Name",
    "ContextName",
    "RelatedContentTypeContextName",
    "RelatedContentItemName",
    "ViewInstanceName",
    "GroupingKey",
    "DateFrom",
    "DateTo",
    "RelationshipCode",
    "MandatoryFlag",
    "ContentItemName",
    "ContentTypeContextName",
    "ContentItemRlatId",
    "ContentTypeId",
    "ContentItemId",
    "RelatedContentTypeId",
    "RelatedContentItemId",
)

EDUCATIONAL_ESTABLISHMENT_HEADER = (
    "SchoolCode",
    "ViewInstanceName",
    "GroupingKey",
    "Description",
    "Location",
    "Name",
    "PartyId",
    "CountryCountryCode",
    "CountryGeographyCode",
    "StateCountryCode",
    "StateGeographyCode",
    "CountryId",
    "EstablishmentId",
    "StateProvinceId",
)

ITEM_CATALOG_HEADER = (
    "ContentValueSetCode",
    "ContextName",
    "ViewInstanceName",
    "GroupingKey",
    "ModuleId",
    "SeedDataSource",
    "ValueSetDescription",
    "ValueSetName",
    "ContentTypeId",
    "ContentValueSetId",
)

ITEM_CATALOG_CONTENT_ITEM_HEADER = (
    "ORA_TALENT_PROFILE_ITEM_CATALOG.ContentValueSetCode",
    "ORA_TALENT_PROFILE_ITEM_CATALOG.ContextName",
    "ContentValueSetCode",
    "Name",
    "ContextName",
    "ViewInstanceName",
    "GroupingKey",
    "ContentContextNameTransient",
    "ContentItemCode",
    "ContentKeyflexId",
    "ContentSupplierCode",
    "DateFrom",
    "DateTo",
    "ItemDate1",
    "ItemDate10",
    "ItemDate2",
    "ItemDate3",
    "ItemDate4",
    "ItemDate5",
    "ItemDate6",
    "ItemDate7",
    "ItemDate8",
    "ItemDate9",
    "ItemDescription",
    "ItemDescrlong",
    "ItemNumber1",
    "ItemNumber10",
    "ItemNumber2",
    "ItemNumber3",
    "ItemNumber4",
    "ItemNumber5",
    "ItemNumber6",
    "ItemNumber7",
    "ItemNumber8",
    "ItemNumber9",
    "ItemText1",
    "ItemText10",
    "ItemText11",
    "ItemText12",
    "ItemText13",
    "ItemText14",
    "ItemText15",
    "ItemText16",
    "ItemText17",
    "ItemText18",
    "ItemText19",
    "ItemText2",
    "ItemText20",
    "ItemText21",
    "ItemText22",
    "ItemText23",
    "ItemText24",
    "ItemText25",
    "ItemText26",
    "ItemText27",
    "ItemText28",
    "ItemText29",
    "ItemText3",
    "ItemText30",
    "ItemText4",
    "ItemText5",
    "ItemText6",
    "ItemText7",
    "ItemText8",
    "ItemText9",
    "ItemTextTl1",
    "ItemTextTl10",
    "ItemTextTl11",
    "ItemTextTl12",
    "ItemTextTl13",
    "ItemTextTl14",
    "ItemTextTl15",
    "ItemTextTl2",
    "ItemTextTl3",
    "ItemTextTl4",
    "ItemTextTl5",
    "ItemTextTl6",
    "ItemTextTl7",
    "ItemTextTl8",
    "ItemTextTl9",
    "ModuleId",
    "RatingModelCode",
    "CountryCountryCode",
    "CountryGeographyCode",
    "StateCountryCode",
    "StateGeographyCode",
    "ContentItemId",
    "ContentTypeId",
    "ContentValueSetId",
    "CountryId",
    "RatingModelId",
    "StateProvinceId",
)

ITEM_CATALOG_RATING_DESCRIPTION_HEADER = (
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
    "RatingLevelId",
    "ContentItemId",
    "ContentTypeId",
    "ContentRatingDescId",
    "ContentValueSetId",
    "RatingModelId",
)


TASK_CONTRACTS: Mapping[str, TaskContract] = {
    "HRT_MANAGE_PROFILE_CONTENT_TYPES": TaskContract(
        task_code="HRT_MANAGE_PROFILE_CONTENT_TYPES",
        headers={
            "HRT_CONTENT_TYPES_B.csv": CONTENT_TYPE_HEADER,
            "ORA_HRT_CONTENT_PROPERTY.csv": CONTENT_TYPE_PROPERTY_HEADER,
            "ORA_HRT_CONTENT_TYPE_RLAT.csv": CONTENT_TYPE_RELATIONSHIP_HEADER,
        },
    ),
    "HRT_MANAGE_PROFILE_CONTENT_ITEMS": TaskContract(
        task_code="HRT_MANAGE_PROFILE_CONTENT_ITEMS",
        headers={
            "HRT_CONTENT_ITEMS_B.csv": CONTENT_ITEM_HEADER,
            "ORA_HRT_CONTENT_ITEM_RLAT.csv": CONTENT_ITEM_RELATIONSHIP_HEADER,
        },
    ),
    "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS": TaskContract(
        task_code="HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS",
        headers={"HRT_SCHOOL.csv": EDUCATIONAL_ESTABLISHMENT_HEADER},
    ),
    "ORA_MANAGE_PROFILE_ITEM_CATALOG": TaskContract(
        task_code="ORA_MANAGE_PROFILE_ITEM_CATALOG",
        headers={
            "ORA_TALENT_PROFILE_ITEM_CATALOG.csv": ITEM_CATALOG_HEADER,
            "ORA_TALENT_CATALOG_CONTENT_ITEM.csv": ITEM_CATALOG_CONTENT_ITEM_HEADER,
            "ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv": (
                ITEM_CATALOG_RATING_DESCRIPTION_HEADER
            ),
        },
    ),
}


@dataclass(frozen=True)
class EvidenceEnvelope:
    task_code: str
    archive_name: str
    archive_sha256: str
    source_environment_alias: str
    target_environment_alias: str | None
    fusion_release: str
    purpose: str
    unfiltered_task_export: bool
    classification: str
    status: str
    complete: bool
    row_counts: Mapping[str, int]
    member_sha256: Mapping[str, str]
    blockers: tuple[str, ...]
    records_by_member: Mapping[str, tuple[Mapping[str, str], ...]]

    @property
    def same_target(self) -> bool:
        return bool(
            self.target_environment_alias
            and self.source_environment_alias == self.target_environment_alias
        )

    @property
    def usable_for_duplicate_comparison(self) -> bool:
        return self.status == "ready" and self.purpose == "current-state" and self.same_target

    @property
    def usable_for_readback(self) -> bool:
        return self.status == "ready" and self.purpose == "readback" and self.same_target

    def sanitized_summary(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "status": self.status,
            "task_code": self.task_code,
            "archive_name": self.archive_name,
            "archive_sha256": self.archive_sha256,
            "source_environment_alias": self.source_environment_alias,
            "target_environment_alias": self.target_environment_alias,
            "fusion_release": self.fusion_release,
            "purpose": self.purpose,
            "unfiltered_task_export": self.unfiltered_task_export,
            "classification": self.classification,
            "complete": self.complete,
            "row_counts": dict(sorted(self.row_counts.items())),
            "member_sha256": dict(sorted(self.member_sha256.items())),
            "usable_for_duplicate_comparison": self.usable_for_duplicate_comparison,
            "usable_for_readback": self.usable_for_readback,
            "blockers": list(self.blockers),
        }


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sanitized_archive_name(name: str) -> str:
    return "sanitized-fsm-evidence.zip" if SENSITIVE_ARCHIVE_NAME.search(name) else name


def _validate_label(value: str | None, field: str, *, required: bool = True) -> None:
    if value is None or value == "":
        if required:
            raise EvidenceContractError(f"{field} is required")
        return
    if not SAFE_LABEL.fullmatch(value):
        raise EvidenceContractError(
            f"{field} must be a non-sensitive alias using letters, numbers, dot, underscore, or hyphen"
        )


def _validate_member(info: zipfile.ZipInfo) -> None:
    name = info.filename
    path = PurePosixPath(name)
    if not name or name.endswith("/"):
        raise EvidenceContractError("directory entries are not allowed in the FSM evidence archive")
    if "\\" in name or path.is_absolute() or len(path.parts) != 1:
        raise EvidenceContractError(f"unsafe or nested archive member: {name!r}")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise EvidenceContractError(f"unsafe archive member: {name!r}")
    mode = info.external_attr >> 16
    if mode and stat.S_ISLNK(mode):
        raise EvidenceContractError(f"symbolic-link archive member is not allowed: {name!r}")
    if info.flag_bits & 0x1:
        raise EvidenceContractError(f"encrypted archive member is not allowed: {name!r}")
    if info.file_size > MAX_MEMBER_BYTES:
        raise EvidenceContractError(f"archive member exceeds the size limit: {name!r}")


def _parse_metadata(raw: bytes, task_code: str) -> None:
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise EvidenceContractError("FSM metadata must not contain a DTD or entity declaration")
    try:
        text = raw.decode("utf-8-sig")
        ET.fromstring(text)
    except (UnicodeError, ET.ParseError) as exc:
        raise EvidenceContractError("FSM metadata is not well-formed UTF-8 XML") from exc
    pattern = rf"(?<![A-Z0-9_]){re.escape(task_code)}(?![A-Z0-9_])"
    if not re.search(pattern, text):
        raise EvidenceContractError(f"FSM metadata does not identify task {task_code}")


def _parse_csv(raw: bytes, expected_header: Sequence[str], member: str) -> tuple[Mapping[str, str], ...]:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeError as exc:
        raise EvidenceContractError(f"{member} is not valid UTF-8 CSV") from exc
    if "\x00" in text:
        raise EvidenceContractError(f"{member} contains a NUL character")
    try:
        reader = csv.reader(io.StringIO(text, newline=""))
        rows = list(reader)
    except csv.Error as exc:
        raise EvidenceContractError(f"{member} could not be parsed as CSV") from exc
    if not rows:
        raise EvidenceContractError(f"{member} is empty and has no header")
    header = tuple(rows[0])
    if header != tuple(expected_header):
        raise EvidenceContractError(f"{member} header does not match the approved evidence contract")
    records: list[Mapping[str, str]] = []
    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(header):
            raise EvidenceContractError(
                f"{member} row {row_number} has {len(row)} values; expected {len(header)}"
            )
        records.append(dict(zip(header, row)))
    return tuple(records)


def inspect_fsm_evidence(
    archive_path: Path,
    *,
    task_code: str,
    source_environment_alias: str,
    fusion_release: str,
    purpose: str = "schema",
    target_environment_alias: str | None = None,
    unfiltered_task_export: bool = False,
) -> EvidenceEnvelope:
    """Validate an FSM export and return an in-memory evidence envelope."""

    contract = TASK_CONTRACTS.get(task_code)
    if contract is None:
        raise EvidenceContractError(f"unsupported GROW-8154 task code: {task_code}")
    if purpose not in {"schema", "current-state", "readback"}:
        raise EvidenceContractError("purpose must be schema, current-state, or readback")
    _validate_label(source_environment_alias, "source_environment_alias")
    _validate_label(fusion_release, "fusion_release")
    _validate_label(
        target_environment_alias,
        "target_environment_alias",
        required=purpose in {"current-state", "readback"},
    )

    path = archive_path.resolve()
    if not path.is_file() or path.suffix.lower() != ".zip":
        raise EvidenceContractError("archive_path must identify one readable ZIP file")

    try:
        archive = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        raise EvidenceContractError("archive_path is not a readable ZIP archive") from exc

    with archive:
        infos = archive.infolist()
        if not infos or len(infos) > MAX_ARCHIVE_MEMBERS:
            raise EvidenceContractError("FSM evidence archive has an unsupported member count")
        for info in infos:
            _validate_member(info)
        names = [info.filename for info in infos]
        if len({name.casefold() for name in names}) != len(names):
            raise EvidenceContractError("FSM evidence archive contains duplicate member names")
        total_size = sum(info.file_size for info in infos)
        if total_size > MAX_ARCHIVE_UNCOMPRESSED_BYTES:
            raise EvidenceContractError("FSM evidence archive exceeds the uncompressed size limit")

        actual_members = frozenset(names)
        missing = sorted(contract.expected_members - actual_members)
        unexpected = sorted(actual_members - contract.expected_members)
        if missing:
            raise EvidenceContractError(f"FSM evidence archive is missing members: {', '.join(missing)}")
        if unexpected:
            raise EvidenceContractError(
                "FSM evidence archive contains members outside the approved contract: "
                + ", ".join(unexpected)
            )

        raw_by_member = {name: archive.read(name) for name in names}

    _parse_metadata(raw_by_member[METADATA_MEMBER], task_code)
    records_by_member = {
        member: _parse_csv(raw_by_member[member], header, member)
        for member, header in contract.headers.items()
    }
    row_counts = {member: len(records) for member, records in records_by_member.items()}
    has_business_rows = any(row_counts.values())
    blockers: list[str] = []
    if purpose in {"current-state", "readback"}:
        if source_environment_alias != target_environment_alias:
            blockers.append(
                "Alternate-environment evidence may define schema but cannot classify target duplicates or readback."
            )
        if not has_business_rows:
            blockers.append(HEADER_ONLY_BLOCKER)
    classification = "schema-only" if purpose == "schema" or not has_business_rows else purpose
    return EvidenceEnvelope(
        task_code=task_code,
        archive_name=_sanitized_archive_name(path.name),
        archive_sha256=_sha256_file(path),
        source_environment_alias=source_environment_alias,
        target_environment_alias=target_environment_alias,
        fusion_release=fusion_release,
        purpose=purpose,
        unfiltered_task_export=unfiltered_task_export,
        classification=classification,
        status="blocked" if blockers else "ready",
        complete=True,
        row_counts=row_counts,
        member_sha256={name: _sha256_bytes(raw) for name, raw in raw_by_member.items()},
        blockers=tuple(blockers),
        records_by_member=records_by_member,
    )


def _normalized_guard(value: str) -> str:
    return " ".join(value.split()).casefold()


def _differing_fields(
    approved: Mapping[str, str], current: Mapping[str, str], fields: Iterable[str]
) -> list[str]:
    def comparable(field: str, value: str) -> str:
        if field not in {"DateFrom", "DateTo"} or not value:
            return value
        for format_string in ("%Y-%m-%d", "%Y/%m/%d"):
            try:
                return datetime.strptime(value, format_string).date().isoformat()
            except ValueError:
                continue
        return value

    return sorted(
        field
        for field in fields
        if comparable(field, approved.get(field, ""))
        != comparable(field, current.get(field, ""))
    )


def _validate_iso_date_range(record: Mapping[str, str], start_field: str, end_field: str) -> list[str]:
    issues: list[str] = []
    parsed: dict[str, date] = {}
    for field in (start_field, end_field):
        value = record.get(field, "")
        if not value:
            continue
        try:
            parsed_date = date.fromisoformat(value)
            if parsed_date.isoformat() != value:
                raise ValueError("Noncanonical supplied date")
            parsed[field] = parsed_date
        except ValueError:
            issues.append(f"{field} must use YYYY-MM-DD")
    if start_field in parsed and end_field in parsed and parsed[end_field] < parsed[start_field]:
        issues.append(f"{end_field} must not precede {start_field}")
    return issues


def _blocked_comparison(message: str, issues: Sequence[str] = ()) -> dict[str, Any]:
    return {
        "status": "blocked",
        "classification": "evidence-unavailable",
        "match_count": 0,
        "differing_fields": [],
        "issues": [message, *issues],
    }


def customer_layer_issues(
    evidence: EvidenceEnvelope,
    task_code: str,
    *,
    allow_header_only_with_seed: bool = False,
) -> list[str]:
    """Return blockers that prevent treating an export as the customer layer.

    A header-only, same-target, unfiltered task export is a valid empty customer
    layer only when it is combined with an integrity-validated seeded catalog. It is
    still not complete standalone evidence, so EvidenceEnvelope.status remains
    blocked and legacy callers keep their fail-closed behavior.
    """

    issues: list[str] = []
    if evidence.task_code != task_code:
        issues.append("Evidence belongs to another setup task.")
    if evidence.purpose != "current-state":
        issues.append("Evidence must have current-state purpose.")
    if not evidence.same_target:
        issues.append("Evidence is not bound to the exact target environment.")
    if not evidence.complete:
        issues.append("Evidence archive validation is incomplete.")
    if not evidence.unfiltered_task_export:
        issues.append("Customer-layer evidence must be an unfiltered task export.")
    issues.extend(
        blocker
        for blocker in evidence.blockers
        if not (allow_header_only_with_seed and blocker == HEADER_ONLY_BLOCKER)
    )
    return issues


def _load_seeded_types_for_evidence(
    evidence: EvidenceEnvelope,
    catalog_dir: Path | None,
) -> SeededCatalog:
    return load_seeded_content_types(
        catalog_dir or DEFAULT_SEEDED_CONTENT_TYPE_CATALOG,
        expected_release=evidence.fusion_release,
    )


def _load_seeded_items_for_evidence(
    evidence: EvidenceEnvelope,
    catalog_dir: Path | None,
) -> SeededCatalog:
    return load_seeded_content_items(
        catalog_dir or DEFAULT_SEEDED_CONTENT_ITEM_CATALOG,
        expected_release=evidence.fusion_release,
    )


def _content_item_field_name(field_name: str) -> str | None:
    direct = {
        "CONTENT_ITEM_ID": None,
        "CONTENT_SUPPLIER_CODE": "ContentSupplierCode",
        "CONTENT_TYPE_ID": "ContextName",
        "DATE_FROM": "DateFrom",
        "DATE_TO": "DateTo",
        "ITEM_DESCRIPTION": "ItemDescription",
        "ITEM_DESCRLONG": "ItemDescrlong",
        "NAME": "Name",
        "RATING_MODEL_ID": "RatingModelCode",
    }
    if field_name in direct:
        return direct[field_name]
    match = re.fullmatch(r"ITEM_TEXT_TL_(\d+)", field_name)
    if match:
        return f"ItemTextTl{match.group(1)}"
    match = re.fullmatch(r"ITEM_TEXT_(\d+)", field_name)
    if match:
        return f"ItemText{match.group(1)}"
    match = re.fullmatch(r"ITEM_NUMBER_(\d+)", field_name)
    if match:
        return f"ItemNumber{match.group(1)}"
    match = re.fullmatch(r"ITEM_DATE_(\d+)", field_name)
    if match:
        return f"ItemDate{match.group(1)}"
    return None


def content_item_requirements_from_properties(
    properties: Iterable[Mapping[str, str]],
) -> dict[str, list[str]]:
    """Translate required Content Type properties to create-row inputs.

    Fusion generates ContentItemId, while ContentTypeId and RatingModelId are
    represented in an FSM create row by ContextName and RatingModelCode.
    Returning both source and input names keeps that translation auditable.
    """

    source_required_fields = sorted(
        {
            row.get("FieldName", "")
            for row in properties
            if row.get("RequiredFlag", "") == "Y" and row.get("FieldName", "")
        }
    )
    input_required_fields = sorted(
        {
            mapped
            for field_name in source_required_fields
            for mapped in (_content_item_field_name(field_name),)
            if mapped
        }
    )
    return {
        "source_required_fields": source_required_fields,
        "input_required_fields": input_required_fields,
    }


def _overlay_rows(
    seeded: Iterable[Mapping[str, str]],
    fresh: Iterable[Mapping[str, str]],
    *,
    key_fields: Sequence[str],
) -> list[dict[str, str]]:
    """Overlay complete fresh rows on seed rows by one stable provider key."""

    rows: dict[tuple[str, ...], dict[str, str]] = {
        tuple(row.get(field, "") for field in key_fields): dict(row) for row in seeded
    }
    for row in fresh:
        key = tuple(row.get(field, "") for field in key_fields)
        if key in rows:
            rows[key].update(row)
        else:
            rows[key] = dict(row)
    return [rows[key] for key in sorted(rows)]


def resolve_content_type_context(
    evidence: EvidenceEnvelope,
    context_name: str,
    *,
    catalog_dir: Path | None = None,
) -> dict[str, Any]:
    """Resolve one Content Type from fresh customer data, then seed data."""

    if not context_name or context_name != context_name.strip():
        return _blocked_comparison("ContextName must be a nonblank trimmed value.")
    issues = customer_layer_issues(
        evidence,
        "HRT_MANAGE_PROFILE_CONTENT_TYPES",
        allow_header_only_with_seed=True,
    )
    if issues:
        return _blocked_comparison("Customer Content Types evidence is unusable.", issues)
    try:
        catalog = _load_seeded_types_for_evidence(evidence, catalog_dir)
    except SeededCatalogError as exc:
        return _blocked_comparison("Seeded Content Types catalog is unusable.", [str(exc)])

    fresh_headers = [
        row
        for row in evidence.records_by_member["HRT_CONTENT_TYPES_B.csv"]
        if row.get("ContextName", "") == context_name
    ]
    seeded_headers = [
        row
        for row in catalog.records_by_file["content-types.csv"]
        if row.get("ContextName", "") == context_name
    ]
    if len(fresh_headers) > 1 or len(seeded_headers) > 1:
        return {
            "status": "blocked",
            "classification": "multiple-exact",
            "match_source": None,
            "route_outcome": "multiple_exact",
            "match_count": len(fresh_headers) + len(seeded_headers),
            "differing_fields": [],
            "issues": ["Multiple Content Types share the proposed exact ContextName."],
        }
    if not fresh_headers and not seeded_headers:
        return {
            "status": "ready",
            "classification": "not-found",
            "match_source": None,
            "route_outcome": "not_found",
            "match_count": 0,
            "evidence_source": "fresh-customer-export-plus-seeded-catalog",
            "context_name": context_name,
            "evidence_fingerprints": [evidence.archive_sha256, catalog.manifest_sha256],
            "issues": [],
            "warnings": [],
        }

    fresh_properties = [
        {
            "ContextName": context_name,
            "FieldName": row.get("FieldName", ""),
            "AttributeLabel": row.get("AttributeLabel", ""),
            "ColumnName": row.get("ColumnName", ""),
            "DefaultValue": row.get("DefaultValue", ""),
            "RequiredFlag": row.get("RequiredFlag", ""),
            "DisplayCode": row.get("DisplayCode", ""),
            "ViewAttrbName": row.get("ViewAttrbName", ""),
        }
        for row in evidence.records_by_member["ORA_HRT_CONTENT_PROPERTY.csv"]
        if row.get("HRT_CONTENT_TYPES_B.ContextName", "") == context_name
    ]
    seeded_properties = [
        row
        for row in catalog.records_by_file["content-type-properties.csv"]
        if row.get("ContextName", "") == context_name
    ]
    fresh_relationships = [
        {
            "ContentTypeContextName": context_name,
            "RelatedContentTypeContextName": row.get("RelatedContentTypeContextName", ""),
            "RelationshipCode": row.get("RelationshipCode", ""),
            "DateFrom": row.get("DateFrom", ""),
            "DateTo": row.get("DateTo", ""),
            "RatingInteractionType": row.get("RatingInteractionType", ""),
        }
        for row in evidence.records_by_member["ORA_HRT_CONTENT_TYPE_RLAT.csv"]
        if row.get("ContentTypeContextName", "") == context_name
    ]
    seeded_relationships = [
        row
        for row in catalog.records_by_file["content-type-relationships.csv"]
        if row.get("ContentTypeContextName", "") == context_name
    ]

    if fresh_headers:
        header = dict(seeded_headers[0]) if seeded_headers else {}
        header.update(
            {
                "ContextName": context_name,
                "ContentTypeName": fresh_headers[0].get("ContentTypeName", ""),
                "ContentDescription": fresh_headers[0].get("ContentDescription", ""),
                "FreeFormFlag": fresh_headers[0].get("FreeFormFlag", ""),
            }
        )
        classification = "exact"
        match_source = "customer"
        evidence_source = (
            "fresh-customer-override-plus-seeded-catalog"
            if seeded_headers
            else "fresh-customer-export"
        )
    else:
        header = dict(seeded_headers[0])
        classification = "exact"
        match_source = "seeded"
        evidence_source = "seeded-catalog"

    properties = _overlay_rows(
        seeded_properties,
        fresh_properties,
        key_fields=("ContextName", "FieldName"),
    )
    relationships = _overlay_rows(
        seeded_relationships,
        fresh_relationships,
        key_fields=(
            "ContentTypeContextName",
            "RelatedContentTypeContextName",
            "RelationshipCode",
            "DateFrom",
        ),
    )
    mapped_properties = [
        (_content_item_field_name(row.get("FieldName", "")), row)
        for row in properties
    ]
    requirements = content_item_requirements_from_properties(properties)
    applicable_dynamic_fields = sorted(
        field
        for field, _row in mapped_properties
        if field and field in CONTENT_ITEM_DYNAMIC_FIELDS
    )
    return {
        "status": "ready",
        "classification": classification,
        "match_source": match_source,
        "route_outcome": "exact_from_%s" % match_source,
        "match_count": 1,
        "evidence_source": evidence_source,
        "context_name": context_name,
        "header": header,
        "properties": properties,
        "relationships": relationships,
        "source_required_fields": requirements["source_required_fields"],
        "required_item_fields": requirements["input_required_fields"],
        "applicable_dynamic_fields": applicable_dynamic_fields,
        "evidence_fingerprints": [evidence.archive_sha256, catalog.manifest_sha256],
        "catalog_summary": catalog.sanitized_summary(),
        "issues": [],
        "warnings": [],
    }


def classify_content_item_with_seeded_catalog(
    evidence: EvidenceEnvelope,
    proposed: Mapping[str, str],
    *,
    applicable_dynamic_fields: Iterable[str] | None = None,
    verified_rating_model_codes: Iterable[str] | None = None,
    catalog_dir: Path | None = None,
) -> dict[str, Any]:
    """Classify an item against fresh customer rows, then seeded identities."""

    issues = validate_content_item(
        proposed,
        applicable_dynamic_fields=applicable_dynamic_fields,
        verified_rating_model_codes=verified_rating_model_codes,
    )
    if issues:
        return _blocked_comparison("Content Item input is invalid.", issues)
    customer_issues = customer_layer_issues(
        evidence,
        "HRT_MANAGE_PROFILE_CONTENT_ITEMS",
        allow_header_only_with_seed=True,
    )
    if customer_issues:
        return _blocked_comparison("Customer Content Items evidence is unusable.", customer_issues)
    try:
        catalog = _load_seeded_items_for_evidence(evidence, catalog_dir)
    except SeededCatalogError as exc:
        return _blocked_comparison("Seeded Content Items catalog is unusable.", [str(exc)])

    fresh_candidates = _content_item_identity_candidates(evidence.records_by_member[CI_MEMBER], proposed)
    if len(fresh_candidates) > 1:
        return {
            "status": "blocked",
            "classification": "multiple-exact",
            "match_source": None,
            "route_outcome": "multiple_exact",
            "match_count": len(fresh_candidates),
            "matched_identifiers": _content_item_matched_identifiers(fresh_candidates),
            "differing_fields": [],
            "issues": ["Multiple customer rows share the exact Content Item key."],
        }
    fields = (*CONTENT_ITEM_BASE_FIELDS, *sorted(applicable_dynamic_fields or ()))
    if fresh_candidates:
        differences = _differing_fields(proposed, fresh_candidates[0], fields)
        return {
            "status": "ready" if not differences else "blocked",
            "classification": "exact",
            "match_source": "customer",
            "route_outcome": "exact_from_customer",
            "match_count": 1,
            "evidence_source": "fresh-customer-export",
            "matched_identifiers": _content_item_matched_identifiers(fresh_candidates),
            "differing_fields": differences,
            "issues": []
            if not differences
            else ["The exact customer item key exists with different applicable values."],
            "warnings": [],
            "evidence_fingerprints": [evidence.archive_sha256, catalog.manifest_sha256],
        }

    seeded_candidates = _content_item_identity_candidates(
        catalog.records_by_file["content-items.csv"], proposed
    )
    if len(seeded_candidates) > 1:
        return {
            "status": "blocked",
            "classification": "multiple-exact",
            "match_source": None,
            "route_outcome": "multiple_exact",
            "match_count": len(seeded_candidates),
            "matched_identifiers": _content_item_matched_identifiers(seeded_candidates),
            "evidence_source": "seeded-catalog",
            "create_eligible": False,
            "comparison_complete": False,
            "differing_fields": [],
            "issues": [
                "Multiple seeded rows match the Content Item Name or code; create is not allowed.",
                "The seeded identity catalog is not a complete reuse/readback row source.",
            ],
            "warnings": [],
            "evidence_fingerprints": [evidence.archive_sha256, catalog.manifest_sha256],
        }
    if seeded_candidates:
        comparison_fields = (
            "ContextName",
            "ContentItemCode",
            "Name",
            "ContentSupplierCode",
            "DateFrom",
            "DateTo",
        )
        differences = _differing_fields(proposed, seeded_candidates[0], comparison_fields)
        return {
            "status": "blocked",
            "classification": "exact",
            "match_source": "seeded",
            "route_outcome": "exact_from_seeded",
            "match_count": len(seeded_candidates),
            "matched_identifiers": _content_item_matched_identifiers(seeded_candidates),
            "evidence_source": "seeded-catalog",
            "create_eligible": False,
            "comparison_complete": False,
            "differing_fields": differences,
            "issues": [
                "The exact Content Item key is Oracle-seeded, so create is not allowed.",
                "The seeded identity catalog is not a complete reuse/readback row source.",
            ],
            "warnings": [],
            "evidence_fingerprints": [evidence.archive_sha256, catalog.manifest_sha256],
        }

    return {
        "status": "ready",
        "classification": "not-found",
        "match_source": None,
        "route_outcome": "not_found",
        "match_count": 0,
        "evidence_source": "fresh-customer-export-plus-seeded-catalog",
        "create_eligible": True,
        "differing_fields": [],
        "issues": [],
        "warnings": [],
        "evidence_fingerprints": [evidence.archive_sha256, catalog.manifest_sha256],
        "catalog_summary": catalog.sanitized_summary(),
    }


IC_MEMBER = "ORA_TALENT_PROFILE_ITEM_CATALOG.csv"
IC_CONTENT_ITEM_MEMBER = "ORA_TALENT_CATALOG_CONTENT_ITEM.csv"
IC_RATING_DESCRIPTION_MEMBER = "ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv"
ITEM_CATALOG_BUSINESS_FIELDS = (
    "ContentValueSetCode",
    "ContextName",
    "ValueSetName",
    "ValueSetDescription",
)
ITEM_CATALOG_CONTENT_ITEM_FIELDS = (
    "ContentValueSetCode",
    "ContextName",
    "Name",
    "ContentItemCode",
    "ItemDescription",
    "DateFrom",
    "DateTo",
    "ContentSupplierCode",
    "ViewInstanceName",
    "GroupingKey",
    "ContentContextNameTransient",
)
ITEM_CATALOG_CONTENT_ITEM_CODE_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")


def validate_item_catalog(record: Mapping[str, str]) -> list[str]:
    """Validate the portable catalog identity and source-backed derived fields."""
    issues: list[str] = []
    for field in ("ContentValueSetCode", "ContextName", "ValueSetName"):
        value = record.get(field, "")
        if not value:
            issues.append(f"{field} is required")
        elif value != value.strip():
            issues.append(f"{field} must not contain surrounding whitespace")
    view_instance = record.get("ViewInstanceName", "")
    if view_instance and view_instance != "ContentTypeValueSet":
        issues.append("ViewInstanceName must equal ContentTypeValueSet")
    grouping_key = record.get("GroupingKey", "")
    expected_grouping = "%s,%s" % (
        record.get("ContextName", ""),
        record.get("ContentValueSetCode", ""),
    )
    if grouping_key and grouping_key != expected_grouping:
        issues.append(
            "GroupingKey must equal ContextName,ContentValueSetCode"
        )
    return issues


def classify_item_catalog(
    evidence: EvidenceEnvelope, proposed: Mapping[str, str]
) -> dict[str, Any]:
    """Classify one Item Catalog using the product migration user key."""
    issues = validate_item_catalog(proposed)
    if issues:
        return _blocked_comparison("Item Catalog input is invalid.", issues)
    if evidence.task_code != "ORA_MANAGE_PROFILE_ITEM_CATALOG":
        return _blocked_comparison("Evidence belongs to another setup task.")
    if not evidence.usable_for_duplicate_comparison:
        return _blocked_comparison(
            "Evidence is not usable for same-target duplicate comparison.",
            evidence.blockers,
        )
    records = evidence.records_by_member[IC_MEMBER]
    key = proposed["ContextName"], proposed["ContentValueSetCode"]
    candidates = [
        row
        for row in records
        if (row.get("ContextName", ""), row.get("ContentValueSetCode", "")) == key
    ]
    if len(candidates) > 1:
        return {
            "status": "blocked",
            "classification": "multiple-exact",
            "match_count": len(candidates),
            "differing_fields": [],
            "issues": ["Multiple Item Catalog rows share the exact provider key."],
            "warnings": [],
        }
    if len(candidates) == 1:
        differences = _differing_fields(
            proposed, candidates[0], ITEM_CATALOG_BUSINESS_FIELDS
        )
        return {
            "status": "ready" if not differences else "blocked",
            "classification": "exact",
            "match_count": 1,
            "differing_fields": differences,
            "issues": (
                []
                if not differences
                else ["The exact Item Catalog key exists with different business values."]
            ),
            "warnings": [],
        }
    name_guard = (
        proposed["ContextName"],
        _normalized_guard(proposed["ValueSetName"]),
    )
    name_collisions = [
        row
        for row in records
        if (
            row.get("ContextName", ""),
            _normalized_guard(row.get("ValueSetName", "")),
        )
        == name_guard
    ]
    if name_collisions:
        return {
            "status": "blocked",
            "classification": "not-found",
            "match_count": 0,
            "name_collision_count": len(name_collisions),
            "differing_fields": [],
            "issues": [
                "The Item Catalog name already exists for this Content Type under another code."
            ],
            "warnings": [],
        }
    return {
        "status": "ready",
        "classification": "not-found",
        "match_count": 0,
        "name_collision_count": 0,
        "differing_fields": [],
        "issues": [],
        "warnings": [],
    }


def verify_item_catalog_readback(
    evidence: EvidenceEnvelope, approved: Mapping[str, str]
) -> dict[str, Any]:
    """Compare one approved catalog against a fresh full task export."""
    issues = validate_item_catalog(approved)
    if issues:
        return {"status": "blocked", "verification": "unavailable", "issues": issues}
    if (
        evidence.task_code != "ORA_MANAGE_PROFILE_ITEM_CATALOG"
        or not evidence.usable_for_readback
    ):
        return {
            "status": "blocked",
            "verification": "unavailable",
            "issues": [
                "Evidence is not usable for same-target Item Catalog readback.",
                *evidence.blockers,
            ],
        }
    key = approved["ContextName"], approved["ContentValueSetCode"]
    candidates = [
        row
        for row in evidence.records_by_member[IC_MEMBER]
        if (row.get("ContextName", ""), row.get("ContentValueSetCode", "")) == key
    ]
    if len(candidates) != 1:
        return {
            "status": "blocked",
            "verification": "missing" if not candidates else "multiple",
            "issues": [
                "Readback did not return exactly one Item Catalog row for the approved provider key."
            ],
        }
    differences = _differing_fields(
        approved, candidates[0], ITEM_CATALOG_BUSINESS_FIELDS
    )
    return {
        "status": "verified" if not differences else "mismatch",
        "verification": (
            "verified-with-derived-fields" if not differences else "mismatch"
        ),
        "differing_fields": differences,
        "issues": (
            []
            if not differences
            else ["Item Catalog readback differs from the approved business values."]
        ),
    }


def validate_item_catalog_content_item(record: Mapping[str, str]) -> list[str]:
    """Validate the portable, phase-one Item Catalog Content Item contract."""
    issues: list[str] = []
    for field in ("ContentValueSetCode", "ContextName", "Name", "ContentItemCode", "ContentSupplierCode"):
        value = record.get(field, "")
        if not value:
            issues.append(f"{field} is required")
        elif value != value.strip():
            issues.append(f"{field} must not contain surrounding whitespace")
    issues.extend(_validate_iso_date_range(record, "DateFrom", "DateTo"))
    code = record.get("ContentItemCode", "")
    if code and (len(code) > 30 or not ITEM_CATALOG_CONTENT_ITEM_CODE_PATTERN.fullmatch(code)):
        issues.append("ContentItemCode must contain only letters, digits, or underscores and be at most 30 characters")
    name = record.get("Name", "")
    if name and len(name) > 700:
        issues.append("Name must be at most 700 characters")
    context = record.get("ContextName", "")
    catalog = record.get("ContentValueSetCode", "")
    view_instance = record.get("ViewInstanceName", "")
    if view_instance and view_instance != "ContentItem":
        issues.append("ViewInstanceName must equal ContentItem")
    grouping_key = record.get("GroupingKey", "")
    expected_grouping = "%s,%s,%s" % (name, context, catalog)
    if grouping_key and grouping_key != expected_grouping:
        issues.append("GroupingKey must equal Name,ContextName,ContentValueSetCode")
    transient_context = record.get("ContentContextNameTransient", "")
    if transient_context and transient_context != context:
        issues.append("ContentContextNameTransient must equal ContextName")
    return issues


def classify_item_catalog_content_item(
    evidence: EvidenceEnvelope,
    proposed: Mapping[str, str],
    *,
    approved_parent_catalog: Mapping[str, str],
) -> dict[str, Any]:
    """Classify a create-only catalog child and its required exact parent anchor."""
    issues = validate_item_catalog_content_item(proposed)
    issues.extend(validate_item_catalog(approved_parent_catalog))
    if issues:
        return _blocked_comparison("Item Catalog Content Item input is invalid.", issues)
    if evidence.task_code != "ORA_MANAGE_PROFILE_ITEM_CATALOG":
        return _blocked_comparison("Evidence belongs to another setup task.")
    if not evidence.usable_for_duplicate_comparison:
        return _blocked_comparison(
            "Evidence is not usable for same-target Item Catalog Content Item duplicate comparison.",
            evidence.blockers,
        )
    context = proposed["ContextName"]
    catalog = proposed["ContentValueSetCode"]
    if (
        approved_parent_catalog["ContextName"] != context
        or approved_parent_catalog["ContentValueSetCode"] != catalog
    ):
        return _blocked_comparison(
            "The supplied parent-catalog anchor does not match the proposed Content Item context and catalog."
        )
    parent_candidates = [
        row
        for row in evidence.records_by_member[IC_MEMBER]
        if (row.get("ContextName", ""), row.get("ContentValueSetCode", ""))
        == (context, catalog)
    ]
    if len(parent_candidates) != 1:
        return {
            "status": "blocked",
            "classification": "parent-missing" if not parent_candidates else "parent-multiple",
            "match_count": 0,
            "parent_match_count": len(parent_candidates),
            "differing_fields": [],
            "issues": ["The Content Item parent-catalog anchor did not resolve exactly."],
            "warnings": [],
        }
    parent_differences = _differing_fields(
        approved_parent_catalog, parent_candidates[0], ITEM_CATALOG_BUSINESS_FIELDS
    )
    if parent_differences:
        return {
            "status": "blocked",
            "classification": "parent-mismatch",
            "match_count": 0,
            "parent_match_count": 1,
            "differing_fields": parent_differences,
            "issues": ["The current parent-catalog anchor differs from approved business values."],
            "warnings": [],
        }
    records = evidence.records_by_member[IC_CONTENT_ITEM_MEMBER]
    key = context, proposed["Name"], catalog
    candidates = [
        row
        for row in records
        if (row.get("ContextName", ""), row.get("Name", ""), row.get("ContentValueSetCode", ""))
        == key
    ]
    if len(candidates) > 1:
        return {
            "status": "blocked",
            "classification": "multiple-exact",
            "match_count": len(candidates),
            "parent_match_count": 1,
            "differing_fields": [],
            "issues": ["Multiple Content Items share the exact Item Catalog provider key."],
            "warnings": [],
        }
    code_collisions = [
        row
        for row in records
        if row.get("ContentItemCode", "").casefold()
        == proposed["ContentItemCode"].casefold()
    ]
    if code_collisions and not candidates:
        return {
            "status": "blocked",
            "classification": "code-collision",
            "match_count": 0,
            "parent_match_count": 1,
            "code_collision_count": len(code_collisions),
            "differing_fields": [],
            "issues": ["ContentItemCode already exists in the current Item Catalog export."],
            "warnings": [],
        }
    normalized_name = _normalized_guard(proposed["Name"])
    name_collisions = [
        row
        for row in records
        if (
            row.get("ContextName", "") == context
            and row.get("ContentValueSetCode", "") == catalog
            and _normalized_guard(row.get("Name", "")) == normalized_name
        )
    ]
    if name_collisions and not candidates:
        return {
            "status": "blocked",
            "classification": "name-collision",
            "match_count": 0,
            "parent_match_count": 1,
            "name_collision_count": len(name_collisions),
            "differing_fields": [],
            "issues": ["A case-insensitive Content Item name collision exists in the parent catalog."],
            "warnings": [],
        }
    if len(candidates) == 1:
        differences = _differing_fields(proposed, candidates[0], ITEM_CATALOG_CONTENT_ITEM_FIELDS)
        return {
            "status": "ready" if not differences else "blocked",
            "classification": "exact",
            "match_count": 1,
            "parent_match_count": 1,
            "differing_fields": differences,
            "issues": [] if not differences else ["The exact Content Item key exists with different business values."],
            "warnings": [],
        }
    return {
        "status": "ready",
        "classification": "not-found",
        "match_count": 0,
        "parent_match_count": 1,
        "code_collision_count": 0,
        "name_collision_count": 0,
        "differing_fields": [],
        "issues": [],
        "warnings": [],
    }


def verify_item_catalog_parent_no_drift(
    evidence: EvidenceEnvelope, approved_parent_catalog: Mapping[str, str]
) -> dict[str, Any]:
    """Verify the exact parent-catalog business values after a child import."""
    return verify_item_catalog_readback(evidence, approved_parent_catalog)


def verify_item_catalog_set_readback(
    evidence: EvidenceEnvelope, approved_rows: Mapping[str, Sequence[Mapping[str, str]]]
) -> dict[str, Any]:
    """Compare a complete new catalog graph; caller owns process/approval/freshness gates.

    Full export must expose the approved portable fields. A blank exported code
    is missing evidence, not a wildcard; obtain the declared registered-child
    readback through the owning workflow rather than substituting approval data.
    """
    parents = approved_rows.get(IC_MEMBER, ())
    children = approved_rows.get(IC_CONTENT_ITEM_MEMBER, ())
    rating_member = "ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv"
    if (set(approved_rows) != {IC_MEMBER, IC_CONTENT_ITEM_MEMBER, rating_member}
            or len(parents) != 1 or not children or approved_rows[rating_member]):
        return _blocked_comparison("Expected one new catalog and all supplied portable children.")
    if evidence.task_code != "ORA_MANAGE_PROFILE_ITEM_CATALOG" or not evidence.usable_for_readback:
        return _blocked_comparison("Complete same-target Item Catalog readback is required.")
    parent = parents[0]
    key = (parent.get("ContextName"), parent.get("ContentValueSetCode"))
    child_keys = [(r.get("ContextName"), r.get("Name"), r.get("ContentValueSetCode")) for r in children]
    if len(set(child_keys)) != len(child_keys) or any((k[0], k[2]) != key for k in child_keys):
        return _blocked_comparison("Approved child identities are duplicate or belong to another parent.")
    parent_result = verify_item_catalog_readback(evidence, parent)
    def belongs(row):
        return ((row.get("ContextName"), row.get("ContentValueSetCode")) == key
                or (row.get("ORA_TALENT_PROFILE_ITEM_CATALOG.ContextName"),
                    row.get("ORA_TALENT_PROFILE_ITEM_CATALOG.ContentValueSetCode")) == key)
    observed = [r for r in evidence.records_by_member[IC_CONTENT_ITEM_MEMBER] if belongs(r)]
    ratings = [r for r in evidence.records_by_member[rating_member] if belongs(r)]
    results = [verify_item_catalog_content_item_readback(
        evidence, child, approved_parent_catalog=parent) for child in children]
    issues = []
    if len(observed) != len(children):
        issues.append("Saved child count differs from the complete approved set.")
    if ratings:
        issues.append("Unapproved scoped rating-description rows are present.")
    # Compare every other supplied/omitted column, not only the portable subset.
    # Only provider-generated row identities and ModuleId are ignored; a new
    # rating, location or dynamic value is not an approved generated row ID.
    generated = {"ContentItemId", "ContentTypeId", "ContentValueSetId", "ModuleId"}
    for index, child in enumerate(children):
        matches = [r for r in observed if (r.get("ContextName"), r.get("Name"),
                                           r.get("ContentValueSetCode")) == child_keys[index]]
        if len(matches) == 1:
            differences = _differing_fields(child, matches[0], tuple(sorted(set(child) - generated)))
            if differences:
                issues.append("Child row %d differs in approved or omitted columns: %s" %
                              (index + 1, ", ".join(differences)))
    verified = parent_result["status"] == "verified" and not issues and all(
        result["status"] == "verified" for result in results)
    return {"status": "verified" if verified else "mismatch",
            "verification": "complete-catalog-set-comparison" if verified else "mismatch",
            "parent_readback": parent_result, "child_readbacks": results,
            "expected_child_count": len(children), "observed_child_count": len(observed),
            "issues": issues, "automatic_correction": False,
            "runtime_completion": "Requires separate successful process and immutable package binding evidence."}


def verify_item_catalog_content_item_readback(
    evidence: EvidenceEnvelope,
    approved: Mapping[str, str],
    *,
    approved_parent_catalog: Mapping[str, str],
) -> dict[str, Any]:
    """Verify the child row and confirm that its parent catalog did not drift."""
    issues = validate_item_catalog_content_item(approved)
    issues.extend(validate_item_catalog(approved_parent_catalog))
    if issues:
        return {"status": "blocked", "verification": "unavailable", "issues": issues}
    if evidence.task_code != "ORA_MANAGE_PROFILE_ITEM_CATALOG" or not evidence.usable_for_readback:
        return {
            "status": "blocked",
            "verification": "unavailable",
            "issues": [
                "Evidence is not usable for same-target Item Catalog Content Item readback.",
                *evidence.blockers,
            ],
        }
    parent = verify_item_catalog_parent_no_drift(evidence, approved_parent_catalog)
    if parent["status"] != "verified":
        return {
            "status": "blocked",
            "verification": "parent-" + parent.get("verification", "unavailable"),
            "parent_readback": parent,
            "issues": ["Parent Item Catalog readback is missing, ambiguous, or mismatched."],
        }
    key = approved["ContextName"], approved["Name"], approved["ContentValueSetCode"]
    candidates = [
        row
        for row in evidence.records_by_member[IC_CONTENT_ITEM_MEMBER]
        if (row.get("ContextName", ""), row.get("Name", ""), row.get("ContentValueSetCode", ""))
        == key
    ]
    if len(candidates) != 1:
        return {
            "status": "blocked",
            "verification": "missing" if not candidates else "multiple",
            "parent_readback": parent,
            "issues": ["Readback did not return exactly one Item Catalog Content Item for the approved provider key."],
        }
    differences = _differing_fields(approved, candidates[0], ITEM_CATALOG_CONTENT_ITEM_FIELDS)
    return {
        "status": "verified" if not differences else "mismatch",
        "verification": "verified-with-parent-no-drift" if not differences else "mismatch",
        "parent_readback": parent,
        "differing_fields": differences,
        "issues": [] if not differences else ["Item Catalog Content Item readback differs from approved business values."],
    }


EE_MEMBER = "HRT_SCHOOL.csv"
EE_BUSINESS_FIELDS = (
    "SchoolCode",
    "Name",
    "Description",
    "Location",
    "CountryCountryCode",
    "CountryGeographyCode",
    "StateCountryCode",
    "StateGeographyCode",
)


def validate_educational_establishment(record: Mapping[str, str]) -> list[str]:
    issues: list[str] = []
    for field in ("SchoolCode", "Name"):
        if not record.get(field, ""):
            issues.append(f"{field} is required")
    country_pair = bool(record.get("CountryCountryCode", "")), bool(
        record.get("CountryGeographyCode", "")
    )
    state_pair = bool(record.get("StateCountryCode", "")), bool(
        record.get("StateGeographyCode", "")
    )
    if country_pair[0] != country_pair[1]:
        issues.append("country code and country geography code must be supplied together")
    if state_pair[0] != state_pair[1]:
        issues.append("state country code and state geography code must be supplied together")
    if any(state_pair) and not all(country_pair):
        issues.append("state geography references require explicit country geography references")
    return issues


def classify_educational_establishment(
    evidence: EvidenceEnvelope, proposed: Mapping[str, str]
) -> dict[str, Any]:
    issues = validate_educational_establishment(proposed)
    if issues:
        return _blocked_comparison("Educational Establishment input is invalid.", issues)
    if evidence.task_code != "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS":
        return _blocked_comparison("Evidence belongs to another setup task.")
    if not evidence.usable_for_duplicate_comparison:
        return _blocked_comparison("Evidence is not usable for same-target duplicate comparison.", evidence.blockers)
    records = evidence.records_by_member[EE_MEMBER]
    candidates = [row for row in records if row.get("SchoolCode", "") == proposed["SchoolCode"]]
    if len(candidates) > 1:
        return {
            "status": "blocked",
            "classification": "multiple-exact",
            "match_count": len(candidates),
            "differing_fields": [],
            "issues": ["Multiple records share the proposed exact SchoolCode."],
        }
    if len(candidates) == 1:
        differences = _differing_fields(proposed, candidates[0], EE_BUSINESS_FIELDS)
        return {
            "status": "ready" if not differences else "blocked",
            "classification": "exact",
            "match_count": 1,
            "differing_fields": differences,
            "issues": [] if not differences else ["The exact code exists with different business values."],
            "warnings": [],
        }
    return {
        "status": "ready",
        "classification": "not-found",
        "match_count": 0,
        "differing_fields": [],
        "issues": [],
        "warnings": [],
    }


def verify_educational_establishment_readback(
    evidence: EvidenceEnvelope, approved: Mapping[str, str]
) -> dict[str, Any]:
    issues = validate_educational_establishment(approved)
    if issues:
        return {"status": "blocked", "verification": "unavailable", "issues": issues}
    if evidence.task_code != "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS" or not evidence.usable_for_readback:
        return {
            "status": "blocked",
            "verification": "unavailable",
            "issues": ["Evidence is not usable for same-target readback.", *evidence.blockers],
        }
    candidates = [
        row
        for row in evidence.records_by_member[EE_MEMBER]
        if row.get("SchoolCode", "") == approved["SchoolCode"]
    ]
    if len(candidates) != 1:
        return {
            "status": "blocked",
            "verification": "missing" if not candidates else "multiple",
            "issues": ["Readback did not return exactly one record for the approved SchoolCode."],
        }
    differences = _differing_fields(approved, candidates[0], EE_BUSINESS_FIELDS)
    return {
        "status": "verified" if not differences else "mismatch",
        "verification": "verified-with-derived-fields" if not differences else "mismatch",
        "differing_fields": differences,
        "issues": [] if not differences else ["Readback differs from the approved business values."],
    }


CI_MEMBER = "HRT_CONTENT_ITEMS_B.csv"
CI_REL_MEMBER = "ORA_HRT_CONTENT_ITEM_RLAT.csv"
CONTENT_ITEM_BASE_FIELDS = (
    "ContextName",
    "ContentItemCode",
    "Name",
    "ItemDescription",
    "DateFrom",
    "DateTo",
    "ContentSupplierCode",
    "CountryCountryCode",
    "RatingModelCode",
)
CONTENT_ITEM_DYNAMIC_FIELDS = frozenset(
    field
    for field in CONTENT_ITEM_HEADER
    if field.startswith(("ItemTextTl", "ItemNumber", "ItemDate", "ItemText"))
    or field in {"ItemDescrlong", "ItemClobTl2"}
)
CONTENT_ITEM_RELATIONSHIP_FIELDS = (
    "ContentTypeContextName",
    "ContentItemName",
    "RelatedContentTypeContextName",
    "RelatedContentItemName",
    "RelationshipCode",
    "MandatoryFlag",
    "DateFrom",
    "DateTo",
    "Name",
    "ContextName",
)


def validate_content_item(
    record: Mapping[str, str],
    *,
    applicable_dynamic_fields: Iterable[str] | None = None,
    verified_rating_model_codes: Iterable[str] | None = None,
) -> list[str]:
    issues: list[str] = []
    for field in ("ContextName", "ContentItemCode", "Name"):
        if not record.get(field, ""):
            issues.append(f"{field} is required")
    issues.extend(_validate_iso_date_range(record, "DateFrom", "DateTo"))
    supplied_dynamic = {field for field in CONTENT_ITEM_DYNAMIC_FIELDS if record.get(field, "")}
    if supplied_dynamic and applicable_dynamic_fields is None:
        issues.append("owning Content Type evidence is required for dynamic item attributes")
    elif supplied_dynamic:
        applicable = set(applicable_dynamic_fields or ())
        unsupported = sorted(supplied_dynamic - applicable)
        if unsupported:
            issues.append("dynamic fields are not enabled by the owning Content Type: " + ", ".join(unsupported))
    rating_code = record.get("RatingModelCode", "")
    if rating_code:
        if verified_rating_model_codes is None:
            issues.append("RatingModelCode requires verified read-only dependency evidence")
        elif rating_code not in set(verified_rating_model_codes):
            issues.append("RatingModelCode does not resolve exactly in the supplied dependency evidence")
    return issues


def _content_item_identity_candidates(
    records: Iterable[Mapping[str, str]], proposed: Mapping[str, str]
) -> list[Mapping[str, str]]:
    """Legacy FSM UserKey is ContextName,Name; retain the exact code guard.

    No generic case or whitespace normalization is introduced here. The
    catalog-backed enhanced provider has its own separate collision semantics.
    """
    return [
        row for row in records
        if row.get("ContextName", "") == proposed["ContextName"]
        and (row.get("Name", "") == proposed["Name"]
             or row.get("ContentItemCode", "") == proposed["ContentItemCode"])
    ]


def _content_item_matched_identifiers(
    candidates: Iterable[Mapping[str, str]]
) -> list[dict[str, str]]:
    fields = ("ContextName", "Name", "ContentItemCode", "ContentItemId")
    identifiers = [{field: row[field] for field in fields if row.get(field, "")} for row in candidates]
    if contains_sensitive(identifiers):
        raise EvidenceContractError("Sensitive material is not allowed in matched Content Item identifiers")
    return identifiers


def classify_content_item(
    evidence: EvidenceEnvelope,
    proposed: Mapping[str, str],
    *,
    applicable_dynamic_fields: Iterable[str] | None = None,
    verified_rating_model_codes: Iterable[str] | None = None,
) -> dict[str, Any]:
    issues = validate_content_item(
        proposed,
        applicable_dynamic_fields=applicable_dynamic_fields,
        verified_rating_model_codes=verified_rating_model_codes,
    )
    if issues:
        return _blocked_comparison("Content Item input is invalid.", issues)
    if evidence.task_code != "HRT_MANAGE_PROFILE_CONTENT_ITEMS":
        return _blocked_comparison("Evidence belongs to another setup task.")
    if not evidence.usable_for_duplicate_comparison:
        return _blocked_comparison("Evidence is not usable for same-target duplicate comparison.", evidence.blockers)
    records = evidence.records_by_member[CI_MEMBER]
    candidates = _content_item_identity_candidates(records, proposed)
    if len(candidates) > 1:
        return {
            "status": "blocked",
            "classification": "multiple-exact",
            "match_count": len(candidates),
            "matched_identifiers": _content_item_matched_identifiers(candidates),
            "differing_fields": [],
            "issues": ["Multiple records match the exact Content Item provider identity or code guard."],
        }
    fields = (*CONTENT_ITEM_BASE_FIELDS, *sorted(applicable_dynamic_fields or ()))
    if len(candidates) == 1:
        differences = _differing_fields(proposed, candidates[0], fields)
        return {
            "status": "ready" if not differences else "blocked",
            "classification": "exact",
            "match_count": 1,
            "differing_fields": differences,
            "matched_identifiers": _content_item_matched_identifiers(candidates),
            "issues": [] if not differences else ["The exact item key exists with different applicable values."],
            "warnings": [],
        }
    return {
        "status": "ready",
        "classification": "not-found",
        "match_count": 0,
        "differing_fields": [],
        "issues": [],
        "warnings": [],
    }


def _content_item_relationship_key(record: Mapping[str, str]) -> tuple[str, ...]:
    # Resolved endpoint IDs form the source EO alternate key, not RelationshipCode.
    return tuple(record.get(field, "") for field in CONTENT_ITEM_RELATIONSHIP_FIELDS[:4])


def validate_content_item_relationship(
    record: Mapping[str, str],
    *,
    endpoint_keys: Iterable[tuple[str, str]],
    content_type_relationship_keys: Iterable[tuple[str, str, str]],
) -> list[str]:
    issues: list[str] = []
    for field in CONTENT_ITEM_RELATIONSHIP_FIELDS[:5]:
        if not record.get(field, ""):
            issues.append(f"{field} is required")
    issues.extend(_validate_iso_date_range(record, "DateFrom", "DateTo"))
    if record.get("MandatoryFlag", "") not in {"", "Y", "N"}:
        issues.append("MandatoryFlag must be blank, Y, or N")
    endpoints = set(endpoint_keys)
    source = record.get("ContentTypeContextName", ""), record.get("ContentItemName", "")
    related = record.get("RelatedContentTypeContextName", ""), record.get("RelatedContentItemName", "")
    for alias, expected in (("ContextName", source[0]), ("Name", source[1])):
        if alias in record and record[alias] != expected:
            issues.append(f"{alias} conflicts with the source endpoint identity")
    if source not in endpoints:
        issues.append("source Content Item endpoint does not resolve exactly")
    if related not in endpoints:
        issues.append("related Content Item endpoint does not resolve exactly")
    type_key = (
        record.get("ContentTypeContextName", ""),
        record.get("RelatedContentTypeContextName", ""),
        record.get("RelationshipCode", ""),
    )
    if type_key not in set(content_type_relationship_keys):
        issues.append("corresponding Content Type relationship does not resolve exactly")
    return issues


def classify_content_item_relationship(
    evidence: EvidenceEnvelope,
    proposed: Mapping[str, str],
    *,
    endpoint_keys: Iterable[tuple[str, str]],
    content_type_relationship_keys: Iterable[tuple[str, str, str]],
) -> dict[str, Any]:
    issues = validate_content_item_relationship(
        proposed,
        endpoint_keys=endpoint_keys,
        content_type_relationship_keys=content_type_relationship_keys,
    )
    if issues:
        return _blocked_comparison("Content Item relationship input is invalid.", issues)
    if evidence.task_code != "HRT_MANAGE_PROFILE_CONTENT_ITEMS" or not evidence.usable_for_duplicate_comparison:
        return _blocked_comparison("Evidence is not usable for Content Item relationship comparison.", evidence.blockers)
    key = _content_item_relationship_key(proposed)
    candidates = [
        row for row in evidence.records_by_member[CI_REL_MEMBER] if _content_item_relationship_key(row) == key
    ]
    if len(candidates) > 1:
        return {
            "status": "blocked",
            "classification": "multiple-exact",
            "match_count": len(candidates),
            "differing_fields": [],
            "issues": ["Multiple exact Content Item relationships were found."],
        }
    if len(candidates) == 1:
        differences = _differing_fields(proposed, candidates[0], CONTENT_ITEM_RELATIONSHIP_FIELDS)
        return {
            "status": "ready" if not differences else "blocked",
            "classification": "exact",
            "match_count": 1,
            "differing_fields": differences,
            "issues": [] if not differences else ["The relationship key exists with different attributes."],
            "warnings": [],
        }
    return {
        "status": "ready",
        "classification": "not-found",
        "match_count": 0,
        "differing_fields": [],
        "issues": [],
        "warnings": [],
    }


def verify_content_item_relationship_readback(
    evidence: EvidenceEnvelope,
    approved: Mapping[str, str],
    *,
    endpoint_keys: Iterable[tuple[str, str]],
    content_type_relationship_keys: Iterable[tuple[str, str, str]],
) -> dict[str, Any]:
    issues = validate_content_item_relationship(
        approved,
        endpoint_keys=endpoint_keys,
        content_type_relationship_keys=content_type_relationship_keys,
    )
    if issues:
        return {"status": "blocked", "verification": "unavailable", "issues": issues}
    if evidence.task_code != "HRT_MANAGE_PROFILE_CONTENT_ITEMS" or not evidence.usable_for_readback:
        return {
            "status": "blocked",
            "verification": "unavailable",
            "issues": ["Evidence is not usable for same-target Content Item relationship readback.", *evidence.blockers],
        }
    key = _content_item_relationship_key(approved)
    candidates = [
        row for row in evidence.records_by_member[CI_REL_MEMBER] if _content_item_relationship_key(row) == key
    ]
    if len(candidates) != 1:
        return {
            "status": "blocked",
            "verification": "missing" if not candidates else "multiple",
            "issues": ["Readback did not return exactly one Content Item relationship for the approved key."],
        }
    differences = _differing_fields(approved, candidates[0], CONTENT_ITEM_RELATIONSHIP_FIELDS)
    return {
        "status": "verified" if not differences else "mismatch",
        "verification": "verified-with-derived-fields" if not differences else "mismatch",
        "differing_fields": differences,
        "issues": [] if not differences else ["Readback differs from the approved relationship values."],
    }


def verify_content_item_readback(
    evidence: EvidenceEnvelope,
    approved: Mapping[str, str],
    *,
    applicable_dynamic_fields: Iterable[str] | None = None,
    verified_rating_model_codes: Iterable[str] | None = None,
) -> dict[str, Any]:
    issues = validate_content_item(
        approved,
        applicable_dynamic_fields=applicable_dynamic_fields,
        verified_rating_model_codes=verified_rating_model_codes,
    )
    if issues:
        return {"status": "blocked", "verification": "unavailable", "issues": issues}
    if evidence.task_code != "HRT_MANAGE_PROFILE_CONTENT_ITEMS" or not evidence.usable_for_readback:
        return {
            "status": "blocked",
            "verification": "unavailable",
            "issues": ["Evidence is not usable for same-target Content Item readback.", *evidence.blockers],
        }
    candidates = _content_item_identity_candidates(evidence.records_by_member[CI_MEMBER], approved)
    if len(candidates) != 1:
        return {
            "status": "blocked",
            "verification": "missing" if not candidates else "multiple",
            "issues": ["Readback did not return exactly one Content Item for the approved key."],
        }
    fields = (*CONTENT_ITEM_BASE_FIELDS, *sorted(applicable_dynamic_fields or ()))
    differences = _differing_fields(approved, candidates[0], fields)
    return {
        "status": "verified" if not differences else "mismatch",
        "verification": "verified-with-derived-fields" if not differences else "mismatch",
        "differing_fields": differences,
        "issues": [] if not differences else ["Readback differs from the approved Content Item values."],
    }


CT_MEMBER = "HRT_CONTENT_TYPES_B.csv"
CT_PROPERTY_MEMBER = "ORA_HRT_CONTENT_PROPERTY.csv"
CT_REL_MEMBER = "ORA_HRT_CONTENT_TYPE_RLAT.csv"
CONTENT_TYPE_FIELDS = ("ContextName", "ContentTypeName", "ContentDescription", "FreeFormFlag")
CONTENT_TYPE_PROPERTY_FIELDS = (
    "HRT_CONTENT_TYPES_B.ContextName",
    "ContextName",
    "FieldName",
    "AttributeLabel",
    "ColumnName",
    "DefaultValue",
    "RequiredFlag",
    "DisplayCode",
    "ViewAttrbName",
)
CONTENT_TYPE_RELATIONSHIP_FIELDS = (
    "ContentTypeContextName",
    "RelatedContentTypeContextName",
    "ContextName",
    "ContextName1",
    "RelationshipCode",
    "DateFrom",
    "DateTo",
    "RatingInteractionType",
)
PROVIDER_DERIVED_FIELDS = ("ViewInstanceName", "GroupingKey", "ModuleId")


def validate_content_type_graph(
    proposal: Mapping[str, Any],
    *,
    known_content_type_contexts: Iterable[str],
    allowed_property_pairs: Iterable[tuple[str, str]] | None = None,
) -> list[str]:
    header = proposal.get("header", {})
    properties = proposal.get("properties", ())
    relationships = proposal.get("relationships", ())
    issues: list[str] = []
    for field in ("ContextName", "ContentTypeName"):
        if not header.get(field, ""):
            issues.append(f"header.{field} is required")
    if header.get("FreeFormFlag", "") not in {"", "Y", "N"}:
        issues.append("header.FreeFormFlag must be blank, Y, or N")
    for field in PROVIDER_DERIVED_FIELDS:
        if header.get(field, ""):
            issues.append(f"header.{field} is provider-derived and must not be guessed")

    context = header.get("ContextName", "")
    allowed_pairs = set(allowed_property_pairs or ())
    property_keys: set[tuple[str, str]] = set()
    for index, prop in enumerate(properties, start=1):
        if prop.get("HRT_CONTENT_TYPES_B.ContextName", "") != context:
            issues.append(f"property {index} does not reference the proposed Content Type")
        if "ContextName" in prop and prop["ContextName"] != context:
            issues.append(f"property {index} ContextName conflicts with its containing parent")
        key = context, prop.get("FieldName", "")
        if key in property_keys:
            issues.append(f"property {index} has a duplicate ContextName/FieldName provider identity")
        property_keys.add(key)
        if not prop.get("FieldName", "") or not prop.get("ColumnName", ""):
            issues.append(f"property {index} requires FieldName and ColumnName")
        if prop.get("RequiredFlag", "") not in {"", "Y", "N"}:
            issues.append(f"property {index} RequiredFlag must be blank, Y, or N")
        if allowed_property_pairs is None:
            issues.append(f"property {index} requires an approved FieldName/ColumnName contract")
        elif (prop.get("FieldName", ""), prop.get("ColumnName", "")) not in allowed_pairs:
            issues.append(f"property {index} FieldName/ColumnName combination is not approved")
        for field in PROVIDER_DERIVED_FIELDS:
            if prop.get(field, ""):
                issues.append(f"property {index} {field} is provider-derived and must not be guessed")

    known_contexts = set(known_content_type_contexts) | ({context} if context else set())
    relationship_keys: set[tuple[str, str]] = set()
    for index, relationship in enumerate(relationships, start=1):
        source = relationship.get("ContentTypeContextName", "")
        related = relationship.get("RelatedContentTypeContextName", "")
        key = source, related
        if key in relationship_keys:
            issues.append(f"relationship {index} has a duplicate endpoint provider identity")
        relationship_keys.add(key)
        for alias, expected in (("ContextName", source), ("ContextName1", related)):
            if alias in relationship and relationship[alias] != expected:
                issues.append(f"relationship {index} {alias} conflicts with its endpoint")
        if source != context:
            issues.append(f"relationship {index} does not use the proposed Content Type as source")
        if related not in known_contexts:
            issues.append(f"relationship {index} related Content Type does not resolve exactly")
        if not relationship.get("RelationshipCode", ""):
            issues.append(f"relationship {index} RelationshipCode is required")
        if not relationship.get("DateFrom", ""):
            issues.append(f"relationship {index} DateFrom is required; do not infer a provider default")
        issues.extend(
            f"relationship {index} {issue}"
            for issue in _validate_iso_date_range(relationship, "DateFrom", "DateTo")
        )
        for field in PROVIDER_DERIVED_FIELDS:
            if relationship.get(field, ""):
                issues.append(f"relationship {index} {field} is provider-derived and must not be guessed")
    return issues


def _canonical_children(rows: Iterable[Mapping[str, str]], fields: Sequence[str]) -> list[tuple[str, ...]]:
    return sorted(tuple(row.get(field, "") for field in fields) for row in rows)


def _content_type_graph_differences(
    approved: Mapping[str, Any],
    current_header: Mapping[str, str],
    current_properties: Sequence[Mapping[str, str]],
    current_relationships: Sequence[Mapping[str, str]],
) -> list[str]:
    differences = _differing_fields(approved["header"], current_header, CONTENT_TYPE_FIELDS)
    if _canonical_children(approved.get("properties", ()), CONTENT_TYPE_PROPERTY_FIELDS) != _canonical_children(
        current_properties, CONTENT_TYPE_PROPERTY_FIELDS
    ):
        differences.append("properties")
    if _canonical_children(
        approved.get("relationships", ()), CONTENT_TYPE_RELATIONSHIP_FIELDS
    ) != _canonical_children(current_relationships, CONTENT_TYPE_RELATIONSHIP_FIELDS):
        differences.append("relationships")
    return sorted(set(differences))


def classify_content_type_graph(
    evidence: EvidenceEnvelope,
    proposal: Mapping[str, Any],
    *,
    known_content_type_contexts: Iterable[str],
    allowed_property_pairs: Iterable[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    issues = validate_content_type_graph(
        proposal,
        known_content_type_contexts=known_content_type_contexts,
        allowed_property_pairs=allowed_property_pairs,
    )
    if issues:
        return _blocked_comparison("Content Type graph input is invalid.", issues)
    if evidence.task_code != "HRT_MANAGE_PROFILE_CONTENT_TYPES":
        return _blocked_comparison("Evidence belongs to another setup task.")
    if not evidence.usable_for_duplicate_comparison:
        return _blocked_comparison("Evidence is not usable for same-target Content Type comparison.", evidence.blockers)
    context = proposal["header"]["ContextName"]
    headers = [row for row in evidence.records_by_member[CT_MEMBER] if row.get("ContextName", "") == context]
    if len(headers) > 1:
        return {
            "status": "blocked",
            "classification": "multiple-exact",
            "match_count": len(headers),
            "differing_fields": [],
            "issues": ["Multiple Content Types share the proposed exact ContextName."],
        }
    if len(headers) == 1:
        properties = [
            row
            for row in evidence.records_by_member[CT_PROPERTY_MEMBER]
            if row.get("HRT_CONTENT_TYPES_B.ContextName", "") == context
        ]
        relationships = [
            row
            for row in evidence.records_by_member[CT_REL_MEMBER]
            if row.get("ContentTypeContextName", "") == context
        ]
        differences = _content_type_graph_differences(proposal, headers[0], properties, relationships)
        return {
            "status": "ready" if not differences else "blocked",
            "classification": "exact",
            "match_count": 1,
            "differing_fields": differences,
            "issues": [] if not differences else ["The exact Content Type key exists with a different graph."],
            "warnings": [],
        }
    return {
        "status": "ready",
        "classification": "not-found",
        "match_count": 0,
        "differing_fields": [],
        "issues": [],
        "warnings": [],
    }


def verify_content_type_readback(
    evidence: EvidenceEnvelope,
    approved: Mapping[str, Any],
    *,
    known_content_type_contexts: Iterable[str],
    allowed_property_pairs: Iterable[tuple[str, str]] | None = None,
) -> dict[str, Any]:
    issues = validate_content_type_graph(
        approved,
        known_content_type_contexts=known_content_type_contexts,
        allowed_property_pairs=allowed_property_pairs,
    )
    if issues:
        return {"status": "blocked", "verification": "unavailable", "issues": issues}
    if evidence.task_code != "HRT_MANAGE_PROFILE_CONTENT_TYPES" or not evidence.usable_for_readback:
        return {
            "status": "blocked",
            "verification": "unavailable",
            "issues": ["Evidence is not usable for same-target Content Type readback.", *evidence.blockers],
        }
    context = approved["header"]["ContextName"]
    headers = [row for row in evidence.records_by_member[CT_MEMBER] if row.get("ContextName", "") == context]
    if len(headers) != 1:
        return {
            "status": "blocked",
            "verification": "missing" if not headers else "multiple",
            "issues": ["Readback did not return exactly one Content Type for the approved context."],
        }
    properties = [
        row
        for row in evidence.records_by_member[CT_PROPERTY_MEMBER]
        if row.get("HRT_CONTENT_TYPES_B.ContextName", "") == context
    ]
    relationships = [
        row
        for row in evidence.records_by_member[CT_REL_MEMBER]
        if row.get("ContentTypeContextName", "") == context
    ]
    differences = _content_type_graph_differences(approved, headers[0], properties, relationships)
    return {
        "status": "verified" if not differences else "mismatch",
        "verification": "verified-with-derived-fields" if not differences else "mismatch",
        "differing_fields": differences,
        "issues": [] if not differences else ["Readback differs from the approved Content Type graph."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect one GROW-8154 FSM export ZIP and emit a sanitized evidence summary."
    )
    parser.add_argument("archive", type=Path)
    parser.add_argument("--task-code", required=True, choices=sorted(TASK_CONTRACTS))
    parser.add_argument("--source-environment-alias", required=True)
    parser.add_argument("--target-environment-alias")
    parser.add_argument("--fusion-release", default="unknown", help="Optional informational metadata; not an eligibility gate.")
    parser.add_argument("--purpose", choices=("schema", "current-state", "readback"), default="schema")
    parser.add_argument(
        "--unfiltered-task-export",
        action="store_true",
        help="Assert that the workflow created this archive without export criteria.",
    )
    args = parser.parse_args()
    try:
        evidence = inspect_fsm_evidence(
            args.archive,
            task_code=args.task_code,
            source_environment_alias=args.source_environment_alias,
            target_environment_alias=args.target_environment_alias,
            fusion_release=args.fusion_release,
            purpose=args.purpose,
            unfiltered_task_export=args.unfiltered_task_export,
        )
        payload = evidence.sanitized_summary()
        exit_code = 0 if evidence.status == "ready" else 2
    except EvidenceContractError as exc:
        payload = {
            "schema_version": "1.0",
            "status": "blocked",
            "task_code": args.task_code,
            "archive_name": _sanitized_archive_name(args.archive.name),
            "blockers": [str(exc)],
        }
        exit_code = 2
    print(json.dumps(payload, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
