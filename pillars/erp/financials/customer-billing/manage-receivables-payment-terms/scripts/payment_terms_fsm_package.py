#!/usr/bin/env python3
"""Build or validate a Receivables Payment Terms FSM ZIP entirely offline."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field, replace
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from xml.etree import ElementTree


TASK_CODE = "AR_MANAGE_RECEIVABLES_PAYMENT_TERMS"
METADATA = "ASM_SETUP_CSV_METADATA.xml"
HEADER_CSV = "AR_PAYMENT_TERM.csv"
LINE_CSV = "AR_PAYMENT_TERM_LINE.csv"
TRANSLATION_CSV = "AR_PAYMENT_TERM_TRANSLATION.csv"
DISCOUNT_CSV = "AR_PAYMENT_TERM_DISCOUNT.csv"
PAYMENT_TERM_CSVS = (HEADER_CSV, LINE_CSV, TRANSLATION_CSV, DISCOUNT_CSV)
PAYMENT_TERM_OBJECTS = {
    "AR_PAYMENT_TERM",
    "AR_PAYMENT_TERM_LINE",
    "AR_PAYMENT_TERM_TRANSLATION",
    "AR_PAYMENT_TERM_DISCOUNT",
}
PAYMENT_TERM_OBJECT_ORDER = [
    "AR_PAYMENT_TERM",
    "AR_PAYMENT_TERM_TRANSLATION",
    "AR_PAYMENT_TERM_DISCOUNT",
    "AR_PAYMENT_TERM_LINE",
]
OBJECT_TO_CSV = {
    "AR_PAYMENT_TERM": HEADER_CSV,
    "AR_PAYMENT_TERM_LINE": LINE_CSV,
    "AR_PAYMENT_TERM_TRANSLATION": TRANSLATION_CSV,
    "AR_PAYMENT_TERM_DISCOUNT": DISCOUNT_CSV,
}
EXPECTED_NODE_PATHS = {
    "AR_PAYMENT_TERM": "/PaymentTermVO/PaymentTermVORow",
    "AR_PAYMENT_TERM_LINE": "/PaymentTermVO/PaymentTermVORow/PaymentTermLine/PaymentTermLineVORow",
    "AR_PAYMENT_TERM_TRANSLATION": "/PaymentTermVO/PaymentTermVORow/PaymentTermTranslation/PaymentTermTranslationVORow",
    "AR_PAYMENT_TERM_DISCOUNT": "/PaymentTermVO/PaymentTermVORow/PaymentTermLine/PaymentTermLineVORow/PaymentTermLineDiscount/PaymentTermLineDiscountVORow",
}
RELATIONSHIP_FIELDS = {
    "AR_PAYMENT_TERM": {},
    "AR_PAYMENT_TERM_LINE": {
        "AR_PAYMENT_TERM.Name": "string",
        "AR_PAYMENT_TERM.SetCode": "string",
    },
    "AR_PAYMENT_TERM_TRANSLATION": {
        "AR_PAYMENT_TERM.Name": "string",
        "AR_PAYMENT_TERM.SetCode": "string",
    },
    "AR_PAYMENT_TERM_DISCOUNT": {
        "AR_PAYMENT_TERM.Name": "string",
        "AR_PAYMENT_TERM.SetCode": "string",
        "AR_PAYMENT_TERM_LINE.SequenceNum": "long",
    },
}
FLAG_FIELDS = {
    "CreditCheckFlag",
    "InUse",
    "PartialDiscountFlag",
    "PrepaymentFlag",
}
LOOKUP_VALUES = {
    "CalcDiscountOnLinesFlag": {"F", "I", "L", "T"},
    "DiscountBasisDateType": {"APPLICATION_DATE", "DEPOSIT_DATE", "RECEIPT_DATE"},
    "FirstInstallmentCode": {"ALLOCATE", "INCLUDE"},
}
INSTALLMENT_OPTION_LABELS = {
    "ALLOCATE": "Allocate tax and freight across all installments",
    "INCLUDE": "Include tax and freight in the first installment",
}
DISCOUNT_BASIS_LABELS = {
    "F": "Lines and tax, excluding freight",
    "I": "Invoice amount",
    "L": "Lines only",
    "T": "Lines, freight items, and tax",
}
CREATE_DEFAULTS = {
    "BaseAmount": "100",
    "CreditCheckFlag": "N",
    "DiscountBasisDateType": "APPLICATION_DATE",
    "InUse": "N",
    "PartialDiscountFlag": "N",
    "PrepaymentFlag": "N",
}
REQUIRED_HEADER_FIELDS = FLAG_FIELDS | {
    "DiscountBasisDateType",
}
CHILD_UPDATE_KEYS = {
    LINE_CSV: ("SequenceNum",),
    TRANSLATION_CSV: ("Language",),
    DISCOUNT_CSV: ("AR_PAYMENT_TERM_LINE.SequenceNum", "DiscountPercent"),
}
DFF_STRING_LIMITS = {
    "AttributeCategory": 30,
    **{f"Attribute{index}": 150 for index in range(1, 16)},
}
STRING_LENGTH_LIMITS = {
    HEADER_CSV: {
        "Name": 15,
        "Description": 240,
        "CreditCheckFlag": 1,
        "CalcDiscountOnLinesFlag": 1,
        "DiscountBasisDateType": 20,
        "FirstInstallmentCode": 12,
        "InUse": 1,
        "PartialDiscountFlag": 1,
        "PrepaymentFlag": 1,
        **DFF_STRING_LIMITS,
    },
    LINE_CSV: DFF_STRING_LIMITS,
    TRANSLATION_CSV: {
        "Name": 15,
        "Description": 240,
        "Language": 4,
        "SourceLang": 4,
    },
    DISCOUNT_CSV: DFF_STRING_LIMITS,
}
AUDIT_COLUMNS = {
    "LastUpdateDate",
    "LastUpdatedBy",
    "CreationDate",
    "CreatedBy",
    "LastUpdateLogin",
}
MAX_MEMBER_BYTES = 10 * 1024 * 1024
MAX_TOTAL_BYTES = 100 * 1024 * 1024
MAX_COMPRESSION_RATIO = 100
MAX_BLUEPRINT_BYTES = 1024 * 1024
MAX_BATCH_OPERATIONS = 100
BAD_STATUS = re.compile(r"ERROR|FAIL|CANCEL|ABORT", re.IGNORECASE)
SUCCESS_STATUS = re.compile(r"COMPLETE|SUCCESS|SUCCEED", re.IGNORECASE)


class PackageError(Exception):
    def __init__(self, code: str, message: str, **details: Any) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details


@dataclass
class Issue:
    code: str
    message: str
    entity: str = ""
    row: int | None = None
    field: str = ""

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.entity:
            result["entity"] = self.entity
        if self.row is not None:
            result["row"] = self.row
        if self.field:
            result["field"] = self.field
        return result


@dataclass
class PackageData:
    path: Path
    archive_members: list[str]
    metadata_member: str
    metadata_bytes: bytes
    headers: dict[str, list[str]]
    rows: dict[str, list[dict[str, str]]]
    other_csv_row_counts: dict[str, int]
    selected_tasks: list[str]
    task_codes: list[str]
    object_short_names: list[str]
    object_types: list[str]
    business_objects: list[str]
    process_statuses: list[str]
    process_envs: list[str]
    process_releases: list[str]
    process_types: list[str]
    object_contracts: dict[str, dict[str, Any]]
    sha256: str
    warnings: list[Issue] = field(default_factory=list)


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _first_descendant_text(element: ElementTree.Element, name: str) -> str:
    for child in element.iter():
        if _local_name(child.tag) == name:
            return (child.text or "").strip()
    return ""


def _all_text(root: ElementTree.Element, name: str) -> list[str]:
    values: list[str] = []
    for element in root.iter():
        if _local_name(element.tag) == name and (element.text or "").strip():
            values.append((element.text or "").strip())
    return list(dict.fromkeys(values))


def _safe_member_name(name: str) -> None:
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    if not normalized or normalized.startswith("/") or path.is_absolute():
        raise PackageError("unsafe_zip_member", f"Unsafe absolute ZIP member: {name}")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise PackageError("unsafe_zip_member", f"Unsafe ZIP member path: {name}")
    if path.parts and re.match(r"^[A-Za-z]:", path.parts[0]):
        raise PackageError("unsafe_zip_member", f"Unsafe drive-qualified ZIP member: {name}")


def _decode_text(raw: bytes, member: str) -> str:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise PackageError("invalid_encoding", f"{member} must be UTF-8 encoded.") from exc
    if "\x00" in text:
        raise PackageError("invalid_text", f"{member} contains NUL characters.")
    return text


def _csv_content(raw: bytes, member: str) -> tuple[list[str], list[dict[str, str]]]:
    text = _decode_text(raw, member)
    try:
        parsed = list(csv.reader(io.StringIO(text, newline="")))
    except csv.Error as exc:
        raise PackageError("invalid_csv", f"{member} is not valid CSV: {exc}") from exc
    if not parsed or not parsed[0] or any(not value for value in parsed[0]):
        raise PackageError("invalid_csv_header", f"{member} must have one nonblank header row.")
    headers = parsed[0]
    if len(headers) != len(set(headers)):
        raise PackageError("duplicate_csv_header", f"{member} contains duplicate column names.")
    rows: list[dict[str, str]] = []
    for index, values in enumerate(parsed[1:], start=2):
        if not any(value.strip() for value in values):
            continue
        if len(values) != len(headers):
            raise PackageError(
                "invalid_csv_row",
                f"{member} row {index} has {len(values)} values for {len(headers)} columns.",
            )
        rows.append(dict(zip(headers, values)))
    return headers, rows


def _member_map(archive: zipfile.ZipFile) -> dict[str, zipfile.ZipInfo]:
    by_basename: dict[str, list[zipfile.ZipInfo]] = {}
    total = 0
    for info in archive.infolist():
        _safe_member_name(info.filename)
        if info.is_dir():
            continue
        if info.flag_bits & 0x1:
            raise PackageError("encrypted_zip", f"Encrypted ZIP member is not supported: {info.filename}")
        if info.file_size > MAX_MEMBER_BYTES:
            raise PackageError("zip_member_too_large", f"ZIP member exceeds 10 MB: {info.filename}")
        if info.file_size and info.file_size / max(info.compress_size, 1) > MAX_COMPRESSION_RATIO:
            raise PackageError(
                "zip_compression_ratio_exceeded",
                f"ZIP member exceeds the maximum compression ratio of {MAX_COMPRESSION_RATIO}: {info.filename}",
            )
        total += info.file_size
        if total > MAX_TOTAL_BYTES:
            raise PackageError("zip_too_large", "ZIP uncompressed content exceeds 100 MB.")
        basename = PurePosixPath(info.filename.replace("\\", "/")).name
        by_basename.setdefault(basename, []).append(info)
    duplicates = sorted(name for name, infos in by_basename.items() if len(infos) > 1)
    if duplicates:
        raise PackageError("duplicate_zip_basename", "ZIP contains duplicate member basenames.", members=duplicates)
    return {name: infos[0] for name, infos in by_basename.items()}


def _read_package(path: Path) -> PackageData:
    path = path.resolve()
    if not path.is_file() or path.suffix.lower() != ".zip" or not zipfile.is_zipfile(path):
        raise PackageError("invalid_zip", f"A readable ZIP file is required: {path}")
    try:
        with zipfile.ZipFile(path) as archive:
            members = _member_map(archive)
            if METADATA not in members:
                raise PackageError("missing_metadata", f"ZIP must contain exactly one {METADATA}.")
            missing = [name for name in PAYMENT_TERM_CSVS if name not in members]
            if missing:
                raise PackageError("missing_payment_terms_csv", "ZIP is missing Payment Terms CSV members.", members=missing)
            metadata_info = members[METADATA]
            metadata_bytes = archive.read(metadata_info)
            try:
                root = ElementTree.fromstring(metadata_bytes)
            except ElementTree.ParseError as exc:
                raise PackageError("invalid_metadata_xml", f"{METADATA} is not valid XML.") from exc

            selected_tasks: list[str] = []
            task_codes: list[str] = []
            object_contracts: dict[str, dict[str, Any]] = {}
            for element in root.iter():
                if _local_name(element.tag) != "MigrationProcessTaskCSVMetadataVORow":
                    if _local_name(element.tag) == "MigrationProcessBusinessObjectCSVMetadataVORow":
                        object_name = _first_descendant_text(element, "BusinessObjectShortName")
                        if not object_name:
                            continue
                        if object_name in object_contracts:
                            raise PackageError(
                                "duplicate_metadata_business_object",
                                f"Metadata declares {object_name} more than once.",
                            )
                        attributes = [
                            value.strip()
                            for value in _first_descendant_text(element, "XmlAttributeList").split(",")
                            if value.strip()
                        ]
                        attribute_types = [
                            value.strip()
                            for value in _first_descendant_text(element, "XmlAttributeTypeList").split(",")
                            if value.strip()
                        ]
                        object_contracts[object_name] = {
                            "attributes": attributes,
                            "types": attribute_types,
                            "nodePath": _first_descendant_text(element, "XmlNodePath"),
                            "nodeSequence": _first_descendant_text(element, "NodeSequence"),
                        }
                    continue
                task = _first_descendant_text(element, "TaskShortName")
                flag = _first_descendant_text(element, "MigrateFlag").upper()
                if task:
                    task_codes.append(task)
                    if flag == "Y":
                        selected_tasks.append(task)

            headers: dict[str, list[str]] = {}
            rows: dict[str, list[dict[str, str]]] = {}
            for name in PAYMENT_TERM_CSVS:
                headers[name], rows[name] = _csv_content(archive.read(members[name]), name)
            other_csv_row_counts: dict[str, int] = {}
            for name, info in members.items():
                if name in PAYMENT_TERM_CSVS or not name.lower().endswith(".csv"):
                    continue
                _other_headers, other_rows = _csv_content(archive.read(info), name)
                other_csv_row_counts[name] = len(other_rows)

            return PackageData(
                path=path,
                archive_members=[info.filename for info in archive.infolist() if not info.is_dir()],
                metadata_member=metadata_info.filename,
                metadata_bytes=metadata_bytes,
                headers=headers,
                rows=rows,
                other_csv_row_counts=other_csv_row_counts,
                selected_tasks=list(dict.fromkeys(selected_tasks)),
                task_codes=list(dict.fromkeys(task_codes)),
                object_short_names=_all_text(root, "ObjectShortName"),
                object_types=_all_text(root, "ObjectType"),
                business_objects=_all_text(root, "BusinessObjectShortName"),
                process_statuses=_all_text(root, "ProcessStatus"),
                process_envs=_all_text(root, "ProcessEnv"),
                process_releases=_all_text(root, "ProcessRelease"),
                process_types=_all_text(root, "ProcessType"),
                object_contracts=object_contracts,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            )
    except zipfile.BadZipFile as exc:
        raise PackageError("invalid_zip", f"Unreadable ZIP file: {path}") from exc


def _task_scope_issues(package: PackageData, *, exact_task: bool) -> list[Issue]:
    issues: list[Issue] = []
    selected = package.selected_tasks
    task_codes = package.task_codes
    object_names = package.object_short_names
    has_task_definitions = bool(task_codes)
    identifies_task = TASK_CODE in selected if has_task_definitions else object_names == [TASK_CODE]
    if not identifies_task:
        issues.append(Issue("task_identity_mismatch", f"Metadata does not identify {TASK_CODE}."))
    if exact_task and has_task_definitions:
        if selected != [TASK_CODE]:
            issues.append(
                Issue(
                    "multi_task_package" if len(selected) > 1 else "task_selection_mismatch",
                    f"Task-level build requires only {TASK_CODE} selected for migration; found {len(selected)} selected tasks.",
                )
            )
        if task_codes != [TASK_CODE]:
            issues.append(
                Issue(
                    "broader_task_metadata",
                    f"Task-level build metadata must contain only {TASK_CODE}; found {len(task_codes)} task definitions.",
                )
            )
    if exact_task and not has_task_definitions:
        if object_names != [TASK_CODE]:
            issues.append(
                Issue(
                    "broader_task_metadata",
                    f"Task-level UI export metadata must identify only {TASK_CODE}; found {len(object_names)} object identities.",
                )
            )
        if package.object_types != ["TASK"]:
            issues.append(
                Issue(
                    "task_object_type_mismatch",
                    "Task-level UI export metadata must declare ObjectType TASK.",
                )
            )
    if exact_task and not package.process_statuses:
        issues.append(Issue("missing_process_status", "Task-level evidence must include a process status."))
    if exact_task and any(BAD_STATUS.search(status) for status in package.process_statuses):
        issues.append(
            Issue(
                "failed_package_evidence",
                "Task-level build evidence contains an error, failed, cancelled, or aborted process status.",
            )
        )
    if exact_task and any(not SUCCESS_STATUS.search(status) for status in package.process_statuses):
        issues.append(
            Issue(
                "incomplete_process_status",
                "Task-level build evidence must have a completed or successful process status.",
            )
        )
    if exact_task and len(package.process_envs) != 1:
        issues.append(Issue("invalid_process_environment", "Task-level evidence must identify exactly one target environment."))
    if exact_task and len(package.process_releases) != 1:
        issues.append(Issue("invalid_process_release", "Task-level evidence must identify exactly one Fusion release."))
    if exact_task and package.process_types != ["EXPORT"]:
        issues.append(Issue("invalid_process_type", "Task-level source metadata must declare ProcessType EXPORT."))
    missing_objects = sorted(PAYMENT_TERM_OBJECTS - set(package.business_objects))
    if missing_objects:
        issues.append(
            Issue(
                "missing_payment_terms_object",
                "Metadata is missing Payment Terms business-object declarations: " + ", ".join(missing_objects),
            )
        )
    if exact_task:
        unexpected_objects = sorted(set(package.business_objects) - PAYMENT_TERM_OBJECTS)
        if unexpected_objects:
            issues.append(
                Issue(
                    "unexpected_business_object",
                    "Task-level metadata contains unrelated business-object declarations: "
                    + ", ".join(unexpected_objects),
                )
            )
        if package.business_objects != PAYMENT_TERM_OBJECT_ORDER:
            issues.append(
                Issue(
                    "payment_terms_object_order_mismatch",
                    "Payment Terms business objects must retain the exact target metadata order.",
                )
            )
    for object_name, csv_name in OBJECT_TO_CSV.items():
        contract = package.object_contracts.get(object_name)
        if not contract:
            continue
        attributes = contract.get("attributes", [])
        attribute_types = contract.get("types", [])
        if not attributes or len(attributes) != len(attribute_types) or len(attributes) != len(set(attributes)):
            issues.append(
                Issue(
                    "invalid_metadata_field_contract",
                    f"Metadata field/type declarations are invalid for {object_name}.",
                    csv_name,
                )
            )
            continue
        declared = set(attributes) | set(RELATIONSHIP_FIELDS[object_name])
        actual = set(package.headers[csv_name])
        if declared != actual:
            missing = sorted(declared - actual)
            unexpected = sorted(actual - declared)
            issues.append(
                Issue(
                    "metadata_csv_field_mismatch",
                    f"{csv_name} does not match its metadata field contract; missing={missing}, unexpected={unexpected}.",
                    csv_name,
                )
            )
        supported_types = {"date", "dateTime", "decimal", "long", "string"}
        unknown_types = sorted(set(attribute_types) - supported_types)
        if unknown_types:
            issues.append(
                Issue(
                    "unsupported_metadata_type",
                    f"{object_name} declares unsupported field types: {unknown_types}.",
                    csv_name,
                )
            )
        expected_path = EXPECTED_NODE_PATHS.get(object_name)
        actual_path = contract.get("nodePath", "")
        if expected_path and actual_path != expected_path:
            issues.append(
                Issue(
                    "metadata_node_path_mismatch",
                    f"{object_name} XmlNodePath must be {expected_path}; found {actual_path or '<blank>'}.",
                    csv_name,
                )
            )
    return issues


def _decimal(value: str, entity: str, row: int, field_name: str, issues: list[Issue]) -> Decimal | None:
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        issues.append(Issue("invalid_number", f"{field_name} must be numeric.", entity, row, field_name))
        return None


def _integer(value: str, entity: str, row: int, field_name: str, issues: list[Issue]) -> int | None:
    number = _decimal(value, entity, row, field_name, issues)
    if number is None:
        return None
    integral = number.to_integral_value()
    if number != integral:
        issues.append(Issue("invalid_integer", f"{field_name} must be a whole number.", entity, row, field_name))
        return None
    return int(integral)


def _parse_date(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        pass
    for pattern in ("%Y-%m-%d", "%Y/%m/%d", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value.split(".", 1)[0], pattern)
        except ValueError:
            continue
    return None


def _canonical_import_date(value: str, value_type: str) -> str:
    """Return the Fusion-import-safe representation for a metadata date value.

    Task exports use slash-separated dates (for example, ``2026/10/01``),
    but the Payment Terms CSV loader rejects that representation when the row
    is submitted again.  Preserve the semantic value while converting emitted
    candidate rows to the ISO representation accepted by the loader.
    """
    parsed = _parse_date(value)
    if parsed is None:
        return value
    if value_type == "date":
        return parsed.date().isoformat()
    return parsed.isoformat(timespec="seconds")


def _normalize_import_dates(package: PackageData, rows: dict[str, list[dict[str, str]]]) -> None:
    type_maps = _metadata_type_map(package)
    for csv_name, csv_rows in rows.items():
        date_fields = {
            field_name: value_type
            for field_name, value_type in type_maps.get(csv_name, {}).items()
            if value_type in {"date", "dateTime"}
        }
        for row in csv_rows:
            for field_name, value_type in date_fields.items():
                value = row.get(field_name, "").strip()
                if value:
                    row[field_name] = _canonical_import_date(value, value_type)


def _reconciled_values_equal(value_type: str, expected: str, actual: str) -> bool:
    """Compare persisted values using their source-backed metadata type."""
    if expected == actual:
        return True
    if value_type not in {"date", "dateTime"} or not expected or not actual:
        return False
    expected_date = _parse_date(expected)
    actual_date = _parse_date(actual)
    return expected_date is not None and actual_date is not None and expected_date == actual_date


def _metadata_type_map(package: PackageData) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for object_name, csv_name in OBJECT_TO_CSV.items():
        contract = package.object_contracts.get(object_name, {})
        attributes = contract.get("attributes", [])
        attribute_types = contract.get("types", [])
        mapping = dict(zip(attributes, attribute_types)) if len(attributes) == len(attribute_types) else {}
        mapping.update(RELATIONSHIP_FIELDS[object_name])
        result[csv_name] = mapping
    return result


def _object_contracts_compatible(
    left: dict[str, dict[str, Any]],
    right: dict[str, dict[str, Any]],
) -> bool:
    """Compare the stable field contract while ignoring export-run ordering.

    Fusion can assign different NodeSequence values to otherwise identical
    template-only and current-data exports. The candidate keeps the template's
    metadata bytes, while attributes, types, and XmlNodePath establish the
    schema and parent-child contract used for local preparation and validation.
    """
    if set(left) != set(right):
        return False
    stable_fields = ("attributes", "types", "nodePath")
    return all(
        all(left[name].get(field_name) == right[name].get(field_name) for field_name in stable_fields)
        for name in left
    )


def _validate_metadata_types(package: PackageData) -> list[Issue]:
    issues: list[Issue] = []
    for csv_name, type_map in _metadata_type_map(package).items():
        for row_number, row in enumerate(package.rows[csv_name], start=2):
            for field_name, value_type in type_map.items():
                value = row.get(field_name, "").strip()
                if not value:
                    continue
                if value_type == "long":
                    _integer(value, csv_name, row_number, field_name, issues)
                elif value_type == "decimal":
                    _decimal(value, csv_name, row_number, field_name, issues)
                elif value_type in {"date", "dateTime"} and _parse_date(value) is None:
                    issues.append(Issue("invalid_date", f"{field_name} has an unsupported date format.", csv_name, row_number, field_name))
                elif value_type in {"date", "dateTime"} and value != _canonical_import_date(value, value_type):
                    issues.append(
                        Issue(
                            "noncanonical_import_date",
                            f"{field_name} must use the Fusion import-safe ISO date representation.",
                            csv_name,
                            row_number,
                            field_name,
                        )
                    )
    return issues


def _validate_string_lengths(package: PackageData) -> list[Issue]:
    """Apply the current Payment Terms entity/table string precisions."""
    issues: list[Issue] = []
    for csv_name, limits in STRING_LENGTH_LIMITS.items():
        for row_number, row in enumerate(package.rows[csv_name], start=2):
            for field_name, maximum in limits.items():
                value = row.get(field_name, "")
                if len(value) > maximum:
                    issues.append(
                        Issue(
                            "string_too_long",
                            f"{field_name} exceeds the supported maximum length of {maximum} characters.",
                            csv_name,
                            row_number,
                            field_name,
                        )
                    )
    return issues


def _validate_rows(
    package: PackageData,
    verified_evidence: dict[str, Any] | None = None,
) -> tuple[list[Issue], list[Issue]]:
    errors: list[Issue] = _validate_metadata_types(package)
    errors.extend(_validate_string_lengths(package))
    for csv_name in PAYMENT_TERM_CSVS:
        for row_number, row in enumerate(package.rows[csv_name], start=2):
            for field_name in sorted(AUDIT_COLUMNS):
                if row.get(field_name, "").strip():
                    errors.append(
                        Issue(
                            "nonblank_service_owned_audit_field",
                            f"{field_name} is service-owned and must be blank in a Payment Terms import candidate.",
                            csv_name,
                            row_number,
                            field_name,
                        )
                    )
    warnings: list[Issue] = []
    evidence = verified_evidence or {}
    headers = package.rows[HEADER_CSV]
    lines = package.rows[LINE_CSV]
    translations = package.rows[TRANSLATION_CSV]
    discounts = package.rows[DISCOUNT_CSV]

    parent_rows: dict[tuple[str, str], tuple[int, dict[str, str]]] = {}
    for row_number, row in enumerate(headers, start=2):
        key = (row.get("Name", "").strip(), row.get("SetCode", "").strip())
        if not all(key):
            errors.append(Issue("missing_header_identity", "Name and SetCode are required.", HEADER_CSV, row_number))
            continue
        if key in parent_rows:
            errors.append(Issue("duplicate_header_identity", "Name and SetCode must be unique in the package.", HEADER_CSV, row_number))
        else:
            parent_rows[key] = (row_number, row)
        base = _decimal(row.get("BaseAmount", ""), HEADER_CSV, row_number, "BaseAmount", errors)
        if base is not None and base <= 0:
            errors.append(Issue("nonpositive_base_amount", "BaseAmount must be positive.", HEADER_CSV, row_number, "BaseAmount"))
        start_value = row.get("StartDateActive", "").strip()
        end_value = row.get("EndDateActive", "").strip()
        if not start_value:
            errors.append(Issue("missing_start_date", "StartDateActive is required.", HEADER_CSV, row_number, "StartDateActive"))
        start = _parse_date(start_value) if start_value else None
        end = _parse_date(end_value) if end_value else None
        if start_value and start is None:
            errors.append(Issue("invalid_date", "StartDateActive has an unsupported date format.", HEADER_CSV, row_number, "StartDateActive"))
        if end_value and end is None:
            errors.append(Issue("invalid_date", "EndDateActive has an unsupported date format.", HEADER_CSV, row_number, "EndDateActive"))
        if start and end and end <= start:
            errors.append(Issue("invalid_effective_dates", "EndDateActive must be later than StartDateActive.", HEADER_CSV, row_number))
        for field_name in FLAG_FIELDS:
            value = row.get(field_name, "").strip().upper()
            if value and value not in {"N", "Y"}:
                errors.append(Issue("invalid_flag", f"{field_name} must be Y or N.", HEADER_CSV, row_number, field_name))
        for field_name in REQUIRED_HEADER_FIELDS:
            if not row.get(field_name, "").strip():
                errors.append(
                    Issue(
                        "missing_required_header_field",
                        f"{field_name} is required for every payment-term header.",
                        HEADER_CSV,
                        row_number,
                        field_name,
                    )
                )
        for field_name, choices in LOOKUP_VALUES.items():
            value = row.get(field_name, "").strip().upper()
            if value and value not in choices:
                errors.append(
                    Issue(
                        "invalid_lookup_code",
                        f"{field_name} must be one of {sorted(choices)}.",
                        HEADER_CSV,
                        row_number,
                        field_name,
                    )
                )
        cutoff_day = row.get("DueCutoffDay", "").strip()
        if cutoff_day:
            value = _integer(cutoff_day, HEADER_CSV, row_number, "DueCutoffDay", errors)
            if value is not None and not 1 <= value <= 31:
                errors.append(
                    Issue(
                        "due_cutoff_day_range",
                        "DueCutoffDay must be from 1 through 31 when supplied.",
                        HEADER_CSV,
                        row_number,
                        "DueCutoffDay",
                    )
                )
        if row.get("CycleName", "").strip() and row.get("CycleName", "").strip() not in evidence.get("billing_cycles", []):
            warnings.append(Issue("billing_cycle_verification_required", "Balance-forward billing cycle requires current target evidence.", HEADER_CSV, row_number, "CycleName"))
        if row.get("PartialDiscountFlag", "").strip().upper() in {"Y", "YES", "TRUE", "1"} and evidence.get("partial_discount_option_enabled") is not True:
            warnings.append(Issue("partial_discount_verification_required", "Partial-payment discount requires the current target Receivables System Options evidence.", HEADER_CSV, row_number, "PartialDiscountFlag"))

    line_keys: set[tuple[str, str, str]] = set()
    line_amounts: dict[tuple[str, str], Decimal] = {}
    for row_number, row in enumerate(lines, start=2):
        parent = (row.get("AR_PAYMENT_TERM.Name", "").strip(), row.get("AR_PAYMENT_TERM.SetCode", "").strip())
        sequence = row.get("SequenceNum", "").strip()
        if parent not in parent_rows:
            errors.append(Issue("missing_line_parent", "Payment line does not match a package header.", LINE_CSV, row_number))
        if row.get("SetCode", "").strip() != parent[1]:
            errors.append(Issue("line_set_mismatch", "Line SetCode must equal the parent SetCode.", LINE_CSV, row_number, "SetCode"))
        key = (*parent, sequence)
        if not sequence:
            errors.append(Issue("missing_line_sequence", "SequenceNum is required.", LINE_CSV, row_number, "SequenceNum"))
        elif key in line_keys:
            errors.append(Issue("duplicate_line_sequence", "SequenceNum must be unique within a payment term.", LINE_CSV, row_number, "SequenceNum"))
        else:
            sequence_number = _integer(sequence, LINE_CSV, row_number, "SequenceNum", errors)
            if sequence_number is not None and sequence_number <= 0:
                errors.append(Issue("nonpositive_line_sequence", "SequenceNum must be positive.", LINE_CSV, row_number, "SequenceNum"))
        line_keys.add(key)
        amount = _decimal(row.get("RelativeAmount", ""), LINE_CSV, row_number, "RelativeAmount", errors)
        if amount is not None:
            line_amounts[parent] = line_amounts.get(parent, Decimal("0")) + amount
            if amount <= 0:
                errors.append(Issue("nonpositive_relative_amount", "RelativeAmount must be positive.", LINE_CSV, row_number, "RelativeAmount"))
        due_fields = [field_name for field_name in ("DueDays", "DueDate", "DueDayOfMonth") if row.get(field_name, "").strip()]
        if len(due_fields) != 1:
            errors.append(Issue("invalid_due_method", "Populate exactly one of DueDays, DueDate, or DueDayOfMonth.", LINE_CSV, row_number))
        due_months = row.get("DueMonthsForward", "").strip()
        if due_months and "DueDayOfMonth" not in due_fields:
            errors.append(Issue("invalid_due_months_forward", "DueMonthsForward requires DueDayOfMonth.", LINE_CSV, row_number, "DueMonthsForward"))
        if "DueDayOfMonth" in due_fields and not due_months:
            errors.append(Issue("missing_due_months_forward", "DueMonthsForward is required with DueDayOfMonth.", LINE_CSV, row_number, "DueMonthsForward"))
        due_days = row.get("DueDays", "").strip()
        if due_days:
            value = _integer(due_days, LINE_CSV, row_number, "DueDays", errors)
            if value is not None and value < 0:
                errors.append(Issue("negative_due_days", "DueDays cannot be negative.", LINE_CSV, row_number, "DueDays"))
        due_day = row.get("DueDayOfMonth", "").strip()
        if due_day:
            value = _integer(due_day, LINE_CSV, row_number, "DueDayOfMonth", errors)
            if value is not None and not 1 <= value <= 31:
                errors.append(Issue("due_day_of_month_range", "DueDayOfMonth must be from 1 through 31.", LINE_CSV, row_number, "DueDayOfMonth"))
        if due_months:
            value = _integer(due_months, LINE_CSV, row_number, "DueMonthsForward", errors)
            if value is not None and value < 0:
                errors.append(Issue("negative_due_months_forward", "DueMonthsForward cannot be negative.", LINE_CSV, row_number, "DueMonthsForward"))

    for parent, (row_number, row) in parent_rows.items():
        if not row.get("CalcDiscountOnLinesFlag", "").strip():
            errors.append(
                Issue(
                    "missing_required_discount_basis",
                    "CalcDiscountOnLinesFlag is required for every payment-term header, including terms without discount rows.",
                    HEADER_CSV,
                    row_number,
                    "CalcDiscountOnLinesFlag",
                )
            )
        if not row.get("FirstInstallmentCode", "").strip():
            errors.append(
                Issue(
                    "missing_installment_option",
                    "FirstInstallmentCode is required for every payment-term header. For a single installment, INCLUDE is the product-backed behaviorally equivalent default.",
                    HEADER_CSV,
                    row_number,
                    "FirstInstallmentCode",
                )
            )
        matching_lines = [key for key in line_keys if key[:2] == parent]
        if not matching_lines:
            errors.append(Issue("missing_payment_line", "At least one payment line is required.", HEADER_CSV, row_number))
            continue
        try:
            base = Decimal(row.get("BaseAmount", ""))
        except InvalidOperation:
            continue
        total = line_amounts.get(parent, Decimal("0"))
        if total != base:
            errors.append(
                Issue(
                    "line_total_mismatch",
                    f"Payment-line RelativeAmount total {total} does not equal BaseAmount {base}.",
                    HEADER_CSV,
                    row_number,
                    "BaseAmount",
                )
            )
        matching_count = len(matching_lines)
        printing_lead_days = row.get("PrintingLeadDays", "").strip()
        if matching_count > 1:
            if not printing_lead_days:
                errors.append(
                    Issue(
                        "missing_printing_lead_days",
                        "PrintingLeadDays is required for a payment term with multiple installments.",
                        HEADER_CSV,
                        row_number,
                        "PrintingLeadDays",
                    )
                )
            else:
                value = _integer(printing_lead_days, HEADER_CSV, row_number, "PrintingLeadDays", errors)
                if value is not None and value <= 0:
                    errors.append(
                        Issue(
                            "invalid_printing_lead_days",
                            "PrintingLeadDays must be a positive whole number for a payment term with multiple installments.",
                            HEADER_CSV,
                            row_number,
                            "PrintingLeadDays",
                        )
                    )
        elif printing_lead_days:
            value = _integer(printing_lead_days, HEADER_CSV, row_number, "PrintingLeadDays", errors)
            if value is not None and value < 0:
                errors.append(
                    Issue(
                        "negative_printing_lead_days",
                        "PrintingLeadDays cannot be negative.",
                        HEADER_CSV,
                        row_number,
                        "PrintingLeadDays",
                    )
                )
        if row.get("CycleName", "").strip() and matching_count > 1:
            errors.append(
                Issue(
                    "billing_cycle_installments_incompatible",
                    "A balance-forward billing-cycle payment term cannot contain multiple installment lines.",
                    HEADER_CSV,
                    row_number,
                    "CycleName",
                )
            )

    translation_keys: set[tuple[str, str, str]] = set()
    translation_languages: dict[tuple[str, str], set[str]] = {}
    translation_sources: dict[tuple[str, str], set[str]] = {}
    verified_languages = set(evidence.get("languages", []))
    for row_number, row in enumerate(translations, start=2):
        parent = (row.get("AR_PAYMENT_TERM.Name", "").strip(), row.get("AR_PAYMENT_TERM.SetCode", "").strip())
        if parent not in parent_rows:
            errors.append(Issue("missing_translation_parent", "Translation does not match a package header.", TRANSLATION_CSV, row_number))
        language = row.get("Language", "").strip()
        source = row.get("SourceLang", "").strip()
        if not language or not source:
            errors.append(Issue("missing_translation_language", "Language and SourceLang are required.", TRANSLATION_CSV, row_number))
        if not row.get("Name", "").strip():
            errors.append(Issue("missing_translation_name", "Translation Name is required.", TRANSLATION_CSV, row_number, "Name"))
        key = (*parent, language)
        if key in translation_keys:
            errors.append(Issue("duplicate_translation", "Language must be unique within a payment term.", TRANSLATION_CSV, row_number, "Language"))
        translation_keys.add(key)
        translation_languages.setdefault(parent, set()).add(language)
        translation_sources.setdefault(parent, set()).add(source)
        if not verified_languages or language not in verified_languages or source not in verified_languages:
            warnings.append(Issue("translation_verification_required", "Translation language requires current target language evidence.", TRANSLATION_CSV, row_number, "Language"))

    for parent in parent_rows:
        sources = {value for value in translation_sources.get(parent, set()) if value}
        languages = {value for value in translation_languages.get(parent, set()) if value}
        if not languages:
            continue
        if len(sources) != 1:
            errors.append(Issue("ambiguous_source_language", "All translation rows for one payment term must use one base SourceLang.", TRANSLATION_CSV))
        elif next(iter(sources)) not in languages:
            errors.append(Issue("missing_base_language_row", "Translation rows must include the base SourceLang as a Language row.", TRANSLATION_CSV))

    discount_keys: set[tuple[str, str, str, str]] = set()
    discount_counts: dict[tuple[str, str, str], int] = {}
    for row_number, row in enumerate(discounts, start=2):
        parent = (row.get("AR_PAYMENT_TERM.Name", "").strip(), row.get("AR_PAYMENT_TERM.SetCode", "").strip())
        line_sequence = row.get("AR_PAYMENT_TERM_LINE.SequenceNum", "").strip()
        sequence = row.get("SequenceNum", "").strip()
        if (*parent, line_sequence) not in line_keys:
            errors.append(Issue("missing_discount_line", "Discount must reference an existing payment-line sequence.", DISCOUNT_CSV, row_number))
        if row.get("SetCode", "").strip() != parent[1]:
            errors.append(Issue("discount_set_mismatch", "Discount SetCode must equal the parent SetCode.", DISCOUNT_CSV, row_number, "SetCode"))
        if not sequence:
            errors.append(Issue("missing_discount_sequence", "Discount SequenceNum is required.", DISCOUNT_CSV, row_number, "SequenceNum"))
        else:
            sequence_number = _integer(sequence, DISCOUNT_CSV, row_number, "SequenceNum", errors)
            if sequence_number is not None and sequence_number <= 0:
                errors.append(Issue("nonpositive_discount_sequence", "SequenceNum must be positive.", DISCOUNT_CSV, row_number, "SequenceNum"))
        if line_sequence and sequence and sequence != line_sequence:
            errors.append(
                Issue(
                    "discount_sequence_mismatch",
                    "Discount SequenceNum must equal the referenced payment-line SequenceNum.",
                    DISCOUNT_CSV,
                    row_number,
                    "SequenceNum",
                )
            )
        count_key = (*parent, line_sequence)
        discount_counts[count_key] = discount_counts.get(count_key, 0) + 1
        percent = _decimal(row.get("DiscountPercent", ""), DISCOUNT_CSV, row_number, "DiscountPercent", errors)
        if percent is not None and not (Decimal("0") <= percent <= Decimal("100")):
            errors.append(Issue("discount_percent_range", "DiscountPercent must be from 0 through 100.", DISCOUNT_CSV, row_number, "DiscountPercent"))
        if percent is not None:
            discount_key = (*parent, line_sequence, str(percent.normalize()))
            if discount_key in discount_keys:
                errors.append(
                    Issue(
                        "duplicate_discount_combination",
                        "A payment line cannot contain the same DiscountPercent more than once.",
                        DISCOUNT_CSV,
                        row_number,
                        "DiscountPercent",
                    )
                )
            discount_keys.add(discount_key)
        date_fields = [field_name for field_name in ("DiscountDays", "DiscountDate", "DiscountDayOfMonth") if row.get(field_name, "").strip()]
        if len(date_fields) != 1:
            errors.append(Issue("invalid_discount_date_method", "Populate exactly one of DiscountDays, DiscountDate, or DiscountDayOfMonth.", DISCOUNT_CSV, row_number))
        discount_months = row.get("DiscountMonthsForward", "").strip()
        if discount_months and "DiscountDayOfMonth" not in date_fields:
            errors.append(Issue("invalid_discount_months_forward", "DiscountMonthsForward requires DiscountDayOfMonth.", DISCOUNT_CSV, row_number, "DiscountMonthsForward"))
        if "DiscountDayOfMonth" in date_fields and not discount_months:
            errors.append(Issue("missing_discount_months_forward", "DiscountMonthsForward is required with DiscountDayOfMonth.", DISCOUNT_CSV, row_number, "DiscountMonthsForward"))
        discount_days = row.get("DiscountDays", "").strip()
        if discount_days:
            value = _integer(discount_days, DISCOUNT_CSV, row_number, "DiscountDays", errors)
            if value is not None and value < 0:
                errors.append(Issue("negative_discount_days", "DiscountDays cannot be negative.", DISCOUNT_CSV, row_number, "DiscountDays"))
        discount_day = row.get("DiscountDayOfMonth", "").strip()
        if discount_day:
            value = _integer(discount_day, DISCOUNT_CSV, row_number, "DiscountDayOfMonth", errors)
            if value is not None and not 1 <= value <= 31:
                errors.append(Issue("discount_day_of_month_range", "DiscountDayOfMonth must be from 1 through 31.", DISCOUNT_CSV, row_number, "DiscountDayOfMonth"))
        if discount_months:
            value = _integer(discount_months, DISCOUNT_CSV, row_number, "DiscountMonthsForward", errors)
            if value is not None and value < 0:
                errors.append(Issue("negative_discount_months_forward", "DiscountMonthsForward cannot be negative.", DISCOUNT_CSV, row_number, "DiscountMonthsForward"))

    for (name, set_code, line_sequence), count in discount_counts.items():
        if count > 3:
            errors.append(
                Issue(
                    "too_many_discounts",
                    f"Payment line {line_sequence} for {name} in {set_code} has {count} discounts; at most three are supported.",
                    DISCOUNT_CSV,
                )
            )
    parents_with_discounts = {(row.get("AR_PAYMENT_TERM.Name", "").strip(), row.get("AR_PAYMENT_TERM.SetCode", "").strip()) for row in discounts}
    for parent in parents_with_discounts:
        parent_row = parent_rows.get(parent)
        if not parent_row:
            continue
        row_number, row = parent_row
        if not row.get("DiscountBasisDateType", "").strip():
            errors.append(
                Issue(
                    "missing_discount_basis_date",
                    "DiscountBasisDateType is required when discount rows are present.",
                    HEADER_CSV,
                    row_number,
                    "DiscountBasisDateType",
                )
            )

    if headers and not translations:
        warnings.append(Issue("no_translation_rows", "No translation rows are present; confirm whether the target template requires a base-language row."))
    for csv_name in (HEADER_CSV, LINE_CSV, DISCOUNT_CSV):
        for row_number, row in enumerate(package.rows[csv_name], start=2):
            dff_values = [name for name, value in row.items() if re.fullmatch(r"Attribute(?:[1-9]|1[0-5])", name) and value.strip()]
            context = row.get("AttributeCategory", "").strip()
            context_proven, proven_segments = _dff_evidence(evidence, csv_name, context)
            segments_proven = proven_segments is not None and set(dff_values) <= proven_segments
            if dff_values and (not context or not context_proven or not segments_proven):
                warnings.append(Issue("dff_context_verification_required", "Flexfield values require current target context and segment evidence.", csv_name, row_number, "AttributeCategory"))
    return errors, warnings


def validate_package(
    path: Path,
    *,
    exact_task: bool = True,
    source_evidence: bool = False,
    verified_evidence: dict[str, Any] | None = None,
    expected_baseline: PackageData | None = None,
    expected_blueprint: dict[str, Any] | None = None,
) -> dict[str, Any]:
    package = _read_package(path)
    errors = _task_scope_issues(package, exact_task=exact_task)
    warnings: list[Issue] = []
    if not source_evidence:
        row_errors, warnings = _validate_rows(package, verified_evidence)
        errors.extend(row_errors)
        if bool(expected_baseline) != bool(expected_blueprint):
            errors.append(
                Issue(
                    "incomplete_candidate_expectation",
                    "Candidate intent validation requires both the current baseline and normalized blueprint.",
                )
            )
        elif expected_baseline is not None and expected_blueprint is not None:
            errors.extend(_candidate_expectation_issues(package, expected_baseline, expected_blueprint))
    explicit_task_scope = package.selected_tasks == [TASK_CODE] and package.task_codes == [TASK_CODE]
    ui_task_scope = (
        not package.task_codes
        and not package.selected_tasks
        and package.object_short_names == [TASK_CODE]
        and package.object_types == ["TASK"]
    )
    package_scope = (
        "task"
        if explicit_task_scope or ui_task_scope
        else "multi-task"
        if package.task_codes or package.selected_tasks
        else "metadata-object"
    )
    task_level_candidate = not _task_scope_issues(package, exact_task=True)
    if not exact_task and package_scope != "task":
        warnings.append(Issue("broader_package_scope", "Package was reviewed as a broader package and is not a task-level Payment Terms candidate."))
    if not exact_task and any(BAD_STATUS.search(status) for status in package.process_statuses):
        warnings.append(Issue("failed_package_evidence", "Package metadata reports an error, failed, cancelled, or aborted process status."))
    if not exact_task and any(not SUCCESS_STATUS.search(status) for status in package.process_statuses):
        warnings.append(Issue("incomplete_package_evidence", "Package metadata does not report a completed or successful process status."))
    populated_other = {name: count for name, count in package.other_csv_row_counts.items() if count}
    if exact_task and populated_other:
        errors.append(Issue("non_payment_terms_data", "Task-level candidate contains populated non-Payment-Terms CSV files."))
    elif not exact_task and populated_other:
        warnings.append(Issue("broader_package_data", "Broader package contains populated non-Payment-Terms CSV files that this task skill did not validate."))
    status = (
        "ready"
        if not errors and not warnings and task_level_candidate
        else "reviewed"
        if not errors and not exact_task
        else "blocked"
    )
    return {
        "status": status,
        "mode": "offline_review",
        "validationProfile": "source_evidence" if source_evidence else "candidate",
        "taskCode": TASK_CODE,
        "package": str(package.path),
        "packageScope": package_scope,
        "processStatuses": package.process_statuses,
        "processEnvironments": package.process_envs,
        "processReleases": package.process_releases,
        "processTypes": package.process_types,
        "selectedTasks": package.selected_tasks,
        "objectShortNames": package.object_short_names,
        "objectTypes": package.object_types,
        "businessObjects": package.business_objects,
        "metadataFieldContracts": {
            object_name: {
                "attributeCount": len(contract.get("attributes", [])),
                "nodePath": contract.get("nodePath", ""),
                "nodeSequence": contract.get("nodeSequence", ""),
            }
            for object_name, contract in package.object_contracts.items()
        },
        "archiveMembers": package.archive_members,
        "rowCounts": {name: len(package.rows[name]) for name in PAYMENT_TERM_CSVS},
        "otherCsvRowCounts": package.other_csv_row_counts,
        "sha256": package.sha256,
        "taskLevelEvidence": task_level_candidate,
        "taskLevelCandidate": not source_evidence and task_level_candidate,
        "sourceEvidenceEligible": source_evidence and status == "ready",
        "importEligible": not source_evidence and status == "ready",
        "blueprintMatched": (
            not source_evidence
            and expected_baseline is not None
            and expected_blueprint is not None
            and not any(issue.code.startswith("candidate_") or issue.code.startswith("baseline_candidate_") for issue in errors)
        ),
        "errors": [issue.as_dict() for issue in errors],
        "warnings": [issue.as_dict() for issue in warnings],
        "externalCalls": 0,
        "mutationAuthorized": False,
    }


def _load_blueprint(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.stat().st_size > MAX_BLUEPRINT_BYTES:
        raise PackageError("invalid_blueprint", "Blueprint must be a readable JSON file no larger than 1 MB.")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PackageError("invalid_blueprint", f"Blueprint is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise PackageError("invalid_blueprint", "Blueprint root must be a JSON object.")
    allowed = {
        "task_code",
        "action",
        "header",
        "lines",
        "translations",
        "discounts",
        "operations",
        "evidence",
        "confirmation",
    }
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise PackageError("unknown_blueprint_key", "Blueprint contains unsupported top-level keys.", keys=unknown)
    if data.get("task_code", TASK_CODE) != TASK_CODE:
        raise PackageError("task_identity_mismatch", f"Blueprint task_code must be {TASK_CODE}.")
    operation_keys = {"action", "header", "lines", "translations", "discounts"}
    if "operations" in data:
        mixed_keys = sorted(operation_keys & set(data))
        if mixed_keys:
            raise PackageError(
                "mixed_blueprint_shapes",
                "Use either the legacy single-operation fields or operations, not both.",
                keys=mixed_keys,
            )
        operations = data["operations"]
        if not isinstance(operations, list) or not operations:
            raise PackageError("invalid_blueprint", "Blueprint operations must be a nonempty array.")
        if len(operations) > MAX_BATCH_OPERATIONS:
            raise PackageError(
                "batch_operation_limit",
                f"One Payment Terms package supports at most {MAX_BATCH_OPERATIONS} operations.",
                operationCount=len(operations),
                maximum=MAX_BATCH_OPERATIONS,
            )
        for index, operation in enumerate(operations, start=1):
            _validate_blueprint_operation(operation, f"operations[{index - 1}]")
    else:
        _validate_blueprint_operation(
            {key: data[key] for key in operation_keys if key in data},
            "blueprint",
        )
    evidence = data.get("evidence", {})
    if not isinstance(evidence, dict):
        raise PackageError("invalid_blueprint", "Blueprint evidence must be one JSON object.")
    evidence_allowed = {"reference_data_sets", "billing_cycles", "partial_discount_option_enabled", "languages", "dff_contexts"}
    unknown_evidence = sorted(set(evidence) - evidence_allowed)
    if unknown_evidence:
        raise PackageError("unknown_evidence_key", "Blueprint evidence contains unsupported keys.", keys=unknown_evidence)
    for key in ("reference_data_sets", "billing_cycles", "languages"):
        if key in evidence and (not isinstance(evidence[key], list) or any(not isinstance(value, str) for value in evidence[key])):
            raise PackageError("invalid_blueprint", f"Blueprint evidence.{key} must be an array of strings.")
    if "partial_discount_option_enabled" in evidence and not isinstance(evidence["partial_discount_option_enabled"], bool):
        raise PackageError("invalid_blueprint", "Blueprint evidence.partial_discount_option_enabled must be true or false.")
    if "dff_contexts" in evidence:
        contexts = evidence["dff_contexts"]
        valid = isinstance(contexts, dict)
        if valid:
            for csv_name, values in contexts.items():
                if csv_name not in PAYMENT_TERM_CSVS:
                    valid = False
                    break
                if isinstance(values, list):
                    valid = all(isinstance(value, str) for value in values)
                elif isinstance(values, dict):
                    valid = all(
                        isinstance(context, str)
                        and isinstance(segments, list)
                        and all(isinstance(segment, str) for segment in segments)
                        for context, segments in values.items()
                    )
                else:
                    valid = False
                if not valid:
                    break
        if not valid:
            raise PackageError(
                "invalid_blueprint",
                "Blueprint evidence.dff_contexts must map CSV names to context arrays or context-to-attribute maps.",
            )
    confirmation = data.get("confirmation")
    if confirmation is not None:
        if not isinstance(confirmation, dict):
            raise PackageError("invalid_blueprint", "Blueprint confirmation must be one JSON object.")
        unknown_confirmation = sorted(set(confirmation) - {"confirmed", "design_sha256"})
        if unknown_confirmation:
            raise PackageError("unknown_confirmation_key", "Blueprint confirmation contains unsupported keys.", keys=unknown_confirmation)
        if "confirmed" in confirmation and not isinstance(confirmation["confirmed"], bool):
            raise PackageError("invalid_blueprint", "Blueprint confirmation.confirmed must be true or false.")
        digest = confirmation.get("design_sha256", "")
        if digest and (not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest)):
            raise PackageError("invalid_blueprint", "Blueprint confirmation.design_sha256 must be a lowercase SHA-256 value.")
    return data


def _validate_blueprint_operation(operation: Any, location: str) -> None:
    if not isinstance(operation, dict):
        raise PackageError("invalid_blueprint", f"{location} must be one JSON object.")
    allowed = {"operation_id", "action", "header", "lines", "translations", "discounts"}
    unknown = sorted(set(operation) - allowed)
    if unknown:
        raise PackageError(
            "unknown_operation_key",
            f"{location} contains unsupported keys.",
            location=location,
            keys=unknown,
        )
    operation_id = operation.get("operation_id")
    if operation_id is not None and (
        not isinstance(operation_id, str) or not operation_id.strip() or len(operation_id) > 100
    ):
        raise PackageError(
            "invalid_blueprint",
            f"{location}.operation_id must be a nonempty string no longer than 100 characters.",
        )
    action = str(operation.get("action", "")).strip().lower()
    if action not in {"create", "update", "end-date"}:
        raise PackageError("ambiguous_action", f"{location}.action must be create, update, or end-date.")
    if not isinstance(operation.get("header"), dict):
        raise PackageError("invalid_blueprint", f"{location}.header must be one JSON object.")
    for key in ("lines", "translations", "discounts"):
        value = operation.get(key, [])
        if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
            raise PackageError("invalid_blueprint", f"{location}.{key} must be an array of JSON objects.")


def _blueprint_operations(blueprint: dict[str, Any]) -> list[dict[str, Any]]:
    """Return operation objects while preserving the legacy one-operation shape."""
    if "operations" in blueprint:
        return list(blueprint["operations"])
    return [
        {
            "action": blueprint["action"],
            "header": blueprint["header"],
            "lines": blueprint.get("lines", []),
            "translations": blueprint.get("translations", []),
            "discounts": blueprint.get("discounts", []),
        }
    ]


def _rows_for_parent(package: PackageData, name: str, set_code: str) -> dict[str, list[dict[str, str]]]:
    return {
        HEADER_CSV: [row.copy() for row in package.rows[HEADER_CSV] if row.get("Name") == name and row.get("SetCode") == set_code],
        LINE_CSV: [row.copy() for row in package.rows[LINE_CSV] if row.get("AR_PAYMENT_TERM.Name") == name and row.get("AR_PAYMENT_TERM.SetCode") == set_code],
        TRANSLATION_CSV: [row.copy() for row in package.rows[TRANSLATION_CSV] if row.get("AR_PAYMENT_TERM.Name") == name and row.get("AR_PAYMENT_TERM.SetCode") == set_code],
        DISCOUNT_CSV: [row.copy() for row in package.rows[DISCOUNT_CSV] if row.get("AR_PAYMENT_TERM.Name") == name and row.get("AR_PAYMENT_TERM.SetCode") == set_code],
    }


def _bounded(values: Iterable[str], limit: int = 10) -> tuple[list[str], int]:
    unique = sorted(set(value for value in values if value))
    return unique[:limit], max(0, len(unique) - limit)


def _dff_evidence(
    evidence: dict[str, Any],
    csv_name: str,
    context: str,
) -> tuple[bool, set[str] | None]:
    """Return exact context proof and its proven attribute columns."""
    configured = evidence.get("dff_contexts", {}).get(csv_name, {})
    if isinstance(configured, list):
        return context in configured, None
    if isinstance(configured, dict):
        segments = configured.get(context)
        return isinstance(segments, list), set(segments or [])
    return False, None


def _validate_blueprint_fields(blueprint: dict[str, Any], headers: dict[str, list[str]]) -> None:
    mapping = {
        "header": HEADER_CSV,
        "lines": LINE_CSV,
        "translations": TRANSLATION_CSV,
        "discounts": DISCOUNT_CSV,
    }
    for key, csv_name in mapping.items():
        values = [blueprint[key]] if key == "header" else blueprint.get(key, [])
        for row in values:
            unknown = sorted(set(row) - set(headers[csv_name]))
            if unknown:
                raise PackageError("unsupported_template_field", f"{key} contains fields absent from {csv_name}.", fields=unknown)


def _blank_row(headers: list[str], values: dict[str, Any]) -> dict[str, str]:
    return {header: "" if values.get(header) is None else str(values.get(header, "")) for header in headers}


def _child_key(row: dict[str, Any], csv_name: str, row_number: int) -> tuple[str, ...]:
    fields = CHILD_UPDATE_KEYS[csv_name]
    key = tuple(str(row.get(field_name, "")).strip() for field_name in fields)
    if not all(key):
        raise PackageError(
            "missing_update_child_identity",
            f"{csv_name} update row {row_number} must identify the existing or new child by {', '.join(fields)}.",
            entity=csv_name,
            row=row_number,
            fields=list(fields),
        )
    return key


def _merge_update_children(
    headers: list[str],
    current_rows: list[dict[str, str]],
    patches: list[dict[str, Any]],
    csv_name: str,
) -> list[dict[str, str]]:
    """Patch identified children and preserve every unspecified field and row."""
    if not patches:
        return [_blank_row(headers, row) for row in current_rows]

    merged = [_blank_row(headers, row) for row in current_rows]
    positions: dict[tuple[str, ...], int] = {}
    for row_number, row in enumerate(merged, start=1):
        key = _child_key(row, csv_name, row_number)
        if key in positions:
            raise PackageError(
                "ambiguous_baseline_child",
                f"Current evidence contains duplicate {csv_name} child identity {key}.",
                entity=csv_name,
                key=list(key),
            )
        positions[key] = row_number - 1

    seen_patches: set[tuple[str, ...]] = set()
    for row_number, patch in enumerate(patches, start=1):
        key = _child_key(patch, csv_name, row_number)
        if key in seen_patches:
            raise PackageError(
                "duplicate_update_child_patch",
                f"{csv_name} contains more than one update patch for child identity {key}.",
                entity=csv_name,
                row=row_number,
                key=list(key),
            )
        seen_patches.add(key)
        normalized_patch = {field_name: "" if value is None else str(value) for field_name, value in patch.items()}
        if key in positions:
            merged[positions[key]].update(normalized_patch)
            continue
        new_row = _blank_row(headers, normalized_patch)
        for column in AUDIT_COLUMNS:
            if column in new_row:
                new_row[column] = ""
        positions[key] = len(merged)
        merged.append(new_row)
    return merged


def _base_translation_row(rows: list[dict[str, str]]) -> tuple[dict[str, str] | None, str]:
    sources = {row.get("SourceLang", "").strip() for row in rows if row.get("SourceLang", "").strip()}
    if len(sources) != 1:
        return None, ""
    source = next(iter(sources))
    matches = [row for row in rows if row.get("Language", "").strip() == source]
    return (matches[0], source) if len(matches) == 1 else (None, source)


def _synchronize_translatable_fields(
    action: str,
    header_patch: dict[str, str],
    translation_patches: list[dict[str, Any]],
    header: dict[str, str],
    translations: list[dict[str, str]],
) -> None:
    """Keep the base-language TL row aligned with requested base text changes."""
    base_row, source_language = _base_translation_row(translations)
    description_requested = "Description" in header_patch
    base_patch = next(
        (
            row
            for row in translation_patches
            if str(row.get("Language", "")).strip()
            and str(row.get("Language", "")).strip() == str(row.get("SourceLang", source_language)).strip()
        ),
        None,
    )
    base_description_requested = base_patch is not None and "Description" in base_patch

    if description_requested or base_description_requested:
        if base_row is None:
            raise PackageError(
                "missing_base_translation_for_text_update",
                "A description update requires exactly one current base-language translation row.",
                sourceLanguage=source_language,
            )
        header_description = header_patch.get("Description", header.get("Description", ""))
        translation_description = (
            "" if base_patch is None or base_patch.get("Description") is None else str(base_patch.get("Description", ""))
        )
        if description_requested and base_description_requested and header_description != translation_description:
            raise PackageError(
                "conflicting_base_description",
                "Header and base-language translation descriptions must match.",
                headerDescription=header_description,
                translationDescription=translation_description,
                sourceLanguage=source_language,
            )
        resolved_description = header_description if description_requested else translation_description
        header["Description"] = resolved_description
        base_row["Description"] = resolved_description

    if base_row is not None:
        base_name = base_row.get("Name", "").strip()
        if base_name and base_name != header.get("Name", "").strip():
            raise PackageError(
                "base_translation_name_mismatch",
                "The base-language translation Name must equal the payment-term header Name.",
                headerName=header.get("Name", ""),
                translationName=base_name,
                sourceLanguage=source_language,
            )
        base_row["Name"] = header.get("Name", "")
    elif action == "create":
        raise PackageError(
            "missing_base_language_row",
            "Create requires exactly one translation row whose Language equals SourceLang.",
        )


def _csv_bytes(headers: list[str], rows: list[dict[str, str]]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=headers, extrasaction="raise", quoting=csv.QUOTE_ALL, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def _effective_evidence(baseline: PackageData, blueprint: dict[str, Any]) -> dict[str, Any]:
    supplied = blueprint.get("evidence", {})
    baseline_sets = {
        row.get("SetCode", "").strip()
        for row in baseline.rows[HEADER_CSV]
        if row.get("SetCode", "").strip()
    }
    baseline_languages = {
        row.get(field_name, "").strip()
        for row in baseline.rows[TRANSLATION_CSV]
        for field_name in ("Language", "SourceLang")
        if row.get(field_name, "").strip()
    }
    return {
        "reference_data_sets": sorted(
            baseline_sets
            | {value.strip() for value in supplied.get("reference_data_sets", []) if value.strip()}
        ),
        "languages": sorted(
            baseline_languages
            | {value.strip() for value in supplied.get("languages", []) if value.strip()}
        ),
        "billing_cycles": list(dict.fromkeys(value.strip() for value in supplied.get("billing_cycles", []) if value.strip())),
        "partial_discount_option_enabled": supplied.get("partial_discount_option_enabled"),
        "dff_contexts": supplied.get("dff_contexts", {}),
    }


def _prepare_rows(
    template: PackageData,
    baseline: PackageData,
    blueprint: dict[str, Any],
) -> tuple[dict[str, list[dict[str, str]]], dict[str, Any], dict[str, Any]]:
    _validate_blueprint_fields(blueprint, template.headers)
    action = blueprint["action"]
    header_values = {key: "" if value is None else str(value) for key, value in blueprint["header"].items()}
    applied_defaults: dict[str, str] = {}
    if action == "create":
        for field_name, default_value in CREATE_DEFAULTS.items():
            if field_name in template.headers[HEADER_CSV] and not header_values.get(field_name, "").strip():
                header_values[field_name] = default_value
                applied_defaults[field_name] = default_value
        if (
            not blueprint.get("discounts")
            and "CalcDiscountOnLinesFlag" in template.headers[HEADER_CSV]
            and not header_values.get("CalcDiscountOnLinesFlag", "").strip()
        ):
            # PaymentTermEO requires a non-null discount basis even when the
            # create request has no discount children. Invoice Amount is the
            # seeded create value and the value consistently present in the
            # current target export for otherwise non-discounted terms.
            header_values["CalcDiscountOnLinesFlag"] = "I"
            applied_defaults["CalcDiscountOnLinesFlag"] = "I"
    evidence = _effective_evidence(baseline, blueprint)
    name = header_values.get("Name", "").strip()
    if not name:
        raise PackageError("missing_payment_term_name", "Payment-term Name is required.")

    available_sets = evidence["reference_data_sets"]
    set_code = header_values.get("SetCode", "").strip()
    resolution = "supplied_exact"
    if not set_code:
        if len(available_sets) == 1:
            set_code = available_sets[0]
            header_values["SetCode"] = set_code
            resolution = "sole_current_candidate"
        else:
            choices, remaining = _bounded(available_sets)
            raise PackageError(
                "ambiguous_reference_data_set" if available_sets else "missing_reference_data_set_evidence",
                "Choose the business reference data set that should own this payment term.",
                matchCount=len(available_sets),
                choices=choices,
                additionalChoiceCount=remaining,
            )
    elif set_code not in available_sets:
        choices, remaining = _bounded(available_sets)
        raise PackageError(
            "reference_data_set_not_found",
            f"Reference data set {set_code} was not found in the current baseline.",
            matchCount=0,
            choices=choices,
            additionalChoiceCount=remaining,
        )

    cycle_name = header_values.get("CycleName", "").strip()
    if cycle_name and cycle_name not in evidence.get("billing_cycles", []):
        choices, remaining = _bounded(evidence.get("billing_cycles", []))
        raise PackageError(
            "billing_cycle_not_verified",
            f"Billing cycle {cycle_name} is not proven by current target evidence.",
            choices=choices,
            additionalChoiceCount=remaining,
        )
    if header_values.get("PartialDiscountFlag", "").strip().upper() in {"Y", "YES", "TRUE", "1"} and evidence.get("partial_discount_option_enabled") is not True:
        raise PackageError(
            "partial_discount_option_not_verified",
            "Allowing discounts on partial payments requires current evidence that the target Receivables System Option is enabled.",
        )

    translations = blueprint.get("translations", [])
    current_languages = set(evidence.get("languages", []))
    if action == "create" and not translations:
        choices, remaining = _bounded(current_languages)
        raise PackageError(
            "missing_base_language",
            "Choose the base language for this payment term before package generation.",
            choices=choices,
            additionalChoiceCount=remaining,
        )
    translation_sources = {
        str(row.get("SourceLang", "")).strip()
        for row in translations
        if str(row.get("SourceLang", "")).strip()
    }
    translation_languages = {
        str(row.get("Language", "")).strip()
        for row in translations
        if str(row.get("Language", "")).strip()
    }
    if len(translation_sources) > 1 or (action == "create" and translations and len(translation_sources) != 1):
        raise PackageError(
            "ambiguous_base_language",
            "All translation rows must use one selected base SourceLang.",
            choices=sorted(translation_sources),
        )
    if action == "create" and translation_sources and next(iter(translation_sources)) not in translation_languages:
        raise PackageError(
            "missing_base_language_row",
            "Include one translation row whose Language equals the selected base SourceLang.",
            value=next(iter(translation_sources)),
        )
    for row_number, row in enumerate(translations, start=1):
        for field_name in ("Language", "SourceLang"):
            value = str(row.get(field_name, "")).strip()
            if action != "create" and field_name == "SourceLang" and not value:
                continue
            if not value or value not in current_languages:
                choices, remaining = _bounded(current_languages)
                raise PackageError(
                    "translation_language_not_verified",
                    f"Translation row {row_number} {field_name} is not proven by current target language evidence.",
                    value=value,
                    choices=choices,
                    additionalChoiceCount=remaining,
                )

    for blueprint_key, csv_name in (("header", HEADER_CSV), ("lines", LINE_CSV), ("discounts", DISCOUNT_CSV)):
        values = [blueprint[blueprint_key]] if blueprint_key == "header" else blueprint.get(blueprint_key, [])
        for row_number, row in enumerate(values, start=1):
            has_dff = any(re.fullmatch(r"Attribute(?:[1-9]|1[0-5])", key) and str(value).strip() for key, value in row.items())
            if not has_dff:
                continue
            context = str(row.get("AttributeCategory", "")).strip()
            context_proven, proven_segments = _dff_evidence(evidence, csv_name, context)
            configured = evidence.get("dff_contexts", {}).get(csv_name, {})
            choices, remaining = _bounded(configured if isinstance(configured, list) else configured.keys())
            if not context or not context_proven:
                raise PackageError(
                    "dff_context_not_verified",
                    f"{blueprint_key} row {row_number} flexfield context is not proven by current target evidence.",
                    value=context,
                    choices=choices,
                    additionalChoiceCount=remaining,
                )
            requested_segments = {
                key
                for key, value in row.items()
                if re.fullmatch(r"Attribute(?:[1-9]|1[0-5])", key) and str(value).strip()
            }
            if proven_segments is None:
                raise PackageError(
                    "dff_segment_evidence_not_verified",
                    f"{blueprint_key} row {row_number} has no current target segment evidence for context {context}.",
                    value=context,
                    requestedSegments=sorted(requested_segments),
                )
            unsupported_segments = sorted(requested_segments - proven_segments)
            if unsupported_segments:
                raise PackageError(
                    "dff_segment_not_verified",
                    f"{blueprint_key} row {row_number} requests segments not proven for context {context}.",
                    value=context,
                    fields=unsupported_segments,
                    choices=sorted(proven_segments),
                )

    existing = _rows_for_parent(baseline, name, set_code)
    existing_count = len(existing[HEADER_CSV])
    if action == "create" and existing_count:
        raise PackageError(
            "duplicate_payment_term",
            f"{name} already exists in {set_code}; clarify whether this should be an update.",
            matchCount=existing_count,
        )
    if action in {"update", "end-date"} and existing_count != 1:
        raise PackageError(
            "payment_term_not_exact",
            f"{action} requires exactly one current {name} record in {set_code}.",
            matchCount=existing_count,
        )
    if action == "end-date" and any(blueprint.get(key) for key in ("lines", "translations", "discounts")):
        raise PackageError(
            "end_date_child_change_not_allowed",
            "An end-date package may change only the supported header end date and must preserve all child rows.",
        )

    prepared: dict[str, list[dict[str, str]]] = {name: [] for name in PAYMENT_TERM_CSVS}
    if action == "create":
        header = _blank_row(template.headers[HEADER_CSV], header_values)
        for column in AUDIT_COLUMNS:
            if column in header:
                header[column] = ""
        prepared[HEADER_CSV] = [header]
        for blueprint_key, csv_name in (("lines", LINE_CSV), ("translations", TRANSLATION_CSV), ("discounts", DISCOUNT_CSV)):
            prepared[csv_name] = [_blank_row(template.headers[csv_name], row) for row in blueprint.get(blueprint_key, [])]
    else:
        header = existing[HEADER_CSV][0]
        header.update(header_values)
        prepared[HEADER_CSV] = [_blank_row(template.headers[HEADER_CSV], header)]
        for blueprint_key, csv_name in (("lines", LINE_CSV), ("translations", TRANSLATION_CSV), ("discounts", DISCOUNT_CSV)):
            prepared[csv_name] = _merge_update_children(
                template.headers[csv_name],
                existing[csv_name],
                blueprint.get(blueprint_key, []),
                csv_name,
            )
        if action == "end-date" and not prepared[HEADER_CSV][0].get("EndDateActive", "").strip():
            raise PackageError("missing_end_date", "EndDateActive is required for an end-date request.")

    for row in prepared[LINE_CSV]:
        row["AR_PAYMENT_TERM.Name"] = name
        row["AR_PAYMENT_TERM.SetCode"] = set_code
        if "SetCode" in row:
            row["SetCode"] = set_code
    for csv_name in (TRANSLATION_CSV, DISCOUNT_CSV):
        for row in prepared[csv_name]:
            row["AR_PAYMENT_TERM.Name"] = name
            row["AR_PAYMENT_TERM.SetCode"] = set_code
            if "SetCode" in row:
                row["SetCode"] = set_code
            if csv_name == TRANSLATION_CSV and "Name" in row and not row["Name"].strip():
                row["Name"] = name
    for csv_name in PAYMENT_TERM_CSVS:
        for row in prepared[csv_name]:
            for column in AUDIT_COLUMNS:
                if column in row:
                    row[column] = ""

    _synchronize_translatable_fields(
        action,
        header_values,
        blueprint.get("translations", []),
        prepared[HEADER_CSV][0],
        prepared[TRANSLATION_CSV],
    )
    _normalize_import_dates(template, prepared)

    questions: list[dict[str, Any]] = []
    header = prepared[HEADER_CSV][0]
    if action == "create" and len(prepared[LINE_CSV]) == 1 and not header.get("FirstInstallmentCode", "").strip():
        # The entity requires this value even for one installment. INCLUDE is
        # the seeded product value and is behaviorally equivalent to ALLOCATE
        # when there is only one installment because that line is also first.
        header["FirstInstallmentCode"] = "INCLUDE"
        applied_defaults["FirstInstallmentCode"] = "INCLUDE"
    if len(prepared[LINE_CSV]) > 1:
        if not header.get("PrintingLeadDays", "").strip():
            questions.append(
                {
                    "field": "PrintingLeadDays",
                    "question": "How many print lead days should apply to this split payment term?",
                    "why": "Fusion requires a positive whole-number print lead value for multiple installments.",
                }
            )
        if not header.get("FirstInstallmentCode", "").strip():
            questions.append(
                {
                    "field": "FirstInstallmentCode",
                    "question": "How should tax and freight be allocated across the installments?",
                    "choices": INSTALLMENT_OPTION_LABELS,
                }
            )
    if prepared[DISCOUNT_CSV] and not header.get("CalcDiscountOnLinesFlag", "").strip():
        questions.append(
            {
                "field": "CalcDiscountOnLinesFlag",
                "question": "Which invoice amounts should be used to calculate the discount?",
                "choices": DISCOUNT_BASIS_LABELS,
            }
        )
    if questions:
        early_errors, _early_warnings = _validate_rows(replace(template, rows=prepared), evidence)
        decision_error_codes = {
            "missing_printing_lead_days",
            "missing_installment_option",
            "missing_required_discount_basis",
        }
        hard_errors = [issue for issue in early_errors if issue.code not in decision_error_codes]
        if hard_errors:
            raise PackageError(
                "candidate_design_invalid",
                "The Payment Terms design contains invalid values that must be corrected before missing business choices are requested.",
                errors=[issue.as_dict() for issue in hard_errors],
            )
    if questions:
        raise PackageError(
            "missing_business_decisions",
            "The Payment Terms design needs business choices before it can be previewed or packaged.",
            questions=questions,
        )

    return prepared, {
        "action": action,
        "name": name,
        "setCode": set_code,
        "setResolution": resolution,
        "baselineMatchCount": existing_count,
        "appliedDefaults": applied_defaults,
        "requestedHeaderFields": sorted(header_values),
        "requestedChildRows": {
            LINE_CSV: len(blueprint.get("lines", [])),
            TRANSLATION_CSV: len(blueprint.get("translations", [])),
            DISCOUNT_CSV: len(blueprint.get("discounts", [])),
        },
    }, evidence


def _operation_blueprint(blueprint: dict[str, Any], operation: dict[str, Any]) -> dict[str, Any]:
    """Create the legacy operation view used by the proven single-parent engine."""
    return {
        "task_code": TASK_CODE,
        "action": operation["action"],
        "header": operation["header"],
        "lines": operation.get("lines", []),
        "translations": operation.get("translations", []),
        "discounts": operation.get("discounts", []),
        "evidence": blueprint.get("evidence", {}),
    }


def _prepare_operations(
    template: PackageData,
    baseline: PackageData,
    blueprint: dict[str, Any],
) -> tuple[
    dict[str, list[dict[str, str]]],
    list[dict[str, Any]],
    dict[str, Any],
    list[dict[str, list[dict[str, str]]]],
]:
    """Prepare one or more distinct parents with all-or-nothing semantics."""
    combined = {csv_name: [] for csv_name in PAYMENT_TERM_CSVS}
    resolutions: list[dict[str, Any]] = []
    operation_rows: list[dict[str, list[dict[str, str]]]] = []
    identities: dict[tuple[str, str], int] = {}
    effective_evidence: dict[str, Any] | None = None
    operations = _blueprint_operations(blueprint)
    operation_ids: set[str] = set()
    operation_failures: list[dict[str, Any]] = []

    for index, operation in enumerate(operations, start=1):
        operation_id = str(operation.get("operation_id", "")).strip() or f"operation-{index}"
        if operation_id in operation_ids:
            raise PackageError(
                "duplicate_operation_id",
                "Every batch operation_id must be unique.",
                operationIndex=index,
                operationId=operation_id,
            )
        operation_ids.add(operation_id)
        try:
            prepared, resolution, evidence = _prepare_rows(
                template,
                baseline,
                _operation_blueprint(blueprint, operation),
            )
        except PackageError as exc:
            details = dict(exc.details)
            details.update({"operationIndex": index, "operationId": operation_id})
            if len(operations) == 1:
                raise PackageError(exc.code, exc.message, **details) from exc
            operation_failures.append(
                {
                    "operationIndex": index,
                    "operationId": operation_id,
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                }
            )
            continue

        identity = (resolution["name"], resolution["setCode"])
        if identity in identities:
            raise PackageError(
                "duplicate_batch_target",
                "A batch cannot contain more than one operation for the same payment-term Name and reference data set. Consolidate the requested changes into one operation.",
                name=identity[0],
                setCode=identity[1],
                firstOperationIndex=identities[identity],
                operationIndex=index,
                operationId=operation_id,
            )
        identities[identity] = index
        resolution = {"operationId": operation_id, "operationIndex": index, **resolution}
        resolutions.append(resolution)
        operation_rows.append(prepared)
        for csv_name in PAYMENT_TERM_CSVS:
            combined[csv_name].extend(prepared[csv_name])
        effective_evidence = evidence

    if operation_failures:
        raise PackageError(
            "batch_operations_blocked",
            "One or more Payment Terms operations are unresolved or invalid; the entire batch is blocked and no partial package can be generated.",
            failedOperationCount=len(operation_failures),
            failures=operation_failures,
        )

    return combined, resolutions, effective_evidence or {}, operation_rows


def _candidate_expectation_issues(
    candidate: PackageData,
    baseline: PackageData,
    blueprint: dict[str, Any],
) -> list[Issue]:
    issues: list[Issue] = []
    if candidate.process_envs != baseline.process_envs:
        issues.append(
            Issue(
                "baseline_candidate_environment_mismatch",
                "Candidate and current baseline identify different Fusion environments.",
            )
        )
    if candidate.process_releases != baseline.process_releases:
        issues.append(
            Issue(
                "baseline_candidate_release_mismatch",
                "Candidate and current baseline identify different Fusion releases.",
            )
        )
    if not _object_contracts_compatible(candidate.object_contracts, baseline.object_contracts):
        issues.append(
            Issue(
                "baseline_candidate_metadata_mismatch",
                "Candidate and current baseline Payment Terms field contracts differ.",
            )
        )
    for csv_name in PAYMENT_TERM_CSVS:
        if candidate.headers[csv_name] != baseline.headers[csv_name]:
            issues.append(
                Issue(
                    "baseline_candidate_header_mismatch",
                    f"{csv_name} headers differ between candidate and current baseline.",
                    csv_name,
                )
            )
    if issues:
        return issues

    try:
        expected_rows, _resolutions, _evidence, _operation_rows = _prepare_operations(candidate, baseline, blueprint)
    except PackageError as exc:
        return [
            Issue(
                "candidate_expectation_unresolved",
                f"Candidate could not be compared with the normalized request: {exc.code}: {exc.message}",
            )
        ]
    for csv_name in PAYMENT_TERM_CSVS:
        if candidate.rows[csv_name] != expected_rows[csv_name]:
            issues.append(
                Issue(
                    "candidate_blueprint_mismatch",
                    f"{csv_name} does not exactly match the normalized request and preserved current state.",
                    csv_name,
                )
            )
    return issues


def _design_sha256(
    template: PackageData,
    baseline: PackageData,
    blueprint: dict[str, Any],
    rows: dict[str, list[dict[str, str]]],
) -> str:
    payload = {
        "taskCode": TASK_CODE,
        "operations": [
            {
                "operationId": str(operation.get("operation_id", "")).strip() or f"operation-{index}",
                "action": operation["action"],
            }
            for index, operation in enumerate(_blueprint_operations(blueprint), start=1)
        ],
        "templateSha256": template.sha256,
        "baselineSha256": baseline.sha256,
        "rows": rows,
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _summary_key(csv_name: str, row: dict[str, str]) -> tuple[str, ...]:
    if csv_name == HEADER_CSV:
        return (row.get("Name", ""), row.get("SetCode", ""))
    if csv_name == LINE_CSV:
        return (row.get("SequenceNum", ""),)
    if csv_name == TRANSLATION_CSV:
        return (row.get("Language", ""),)
    return (row.get("AR_PAYMENT_TERM_LINE.SequenceNum", ""), row.get("DiscountPercent", ""))


def _change_summary(
    before: dict[str, list[dict[str, str]]],
    after: dict[str, list[dict[str, str]]],
) -> dict[str, Any]:
    changed: list[dict[str, Any]] = []
    added: list[dict[str, Any]] = []
    removed: list[dict[str, Any]] = []
    preserved_fields = 0
    for csv_name in PAYMENT_TERM_CSVS:
        before_by_key = {_summary_key(csv_name, row): row for row in before.get(csv_name, [])}
        after_by_key = {_summary_key(csv_name, row): row for row in after.get(csv_name, [])}
        for key in sorted(set(after_by_key) - set(before_by_key)):
            added.append({"entity": csv_name, "key": list(key)})
        for key in sorted(set(before_by_key) - set(after_by_key)):
            removed.append({"entity": csv_name, "key": list(key)})
        for key in sorted(set(before_by_key) & set(after_by_key)):
            old = before_by_key[key]
            new = after_by_key[key]
            for field_name in new:
                if field_name in AUDIT_COLUMNS:
                    continue
                before_value = old.get(field_name, "")
                after_value = new.get(field_name, "")
                if before_value == after_value:
                    preserved_fields += 1
                    continue
                changed.append(
                    {
                        "entity": csv_name,
                        "key": list(key),
                        "field": field_name,
                        "before": before_value,
                        "after": after_value,
                    }
                )
    return {
        "changedFields": changed,
        "addedRows": added,
        "removedRows": removed,
        "preservedFieldCount": preserved_fields,
    }


def _business_summary(
    rows: dict[str, list[dict[str, str]]],
    resolution: dict[str, Any],
    before: dict[str, list[dict[str, str]]],
) -> dict[str, Any]:
    header = rows[HEADER_CSV][0]
    lines: list[dict[str, str]] = []
    for row in rows[LINE_CSV]:
        due_method = next(
            (field_name for field_name in ("DueDays", "DueDate", "DueDayOfMonth") if row.get(field_name, "").strip()),
            "",
        )
        lines.append(
            {
                "sequence": row.get("SequenceNum", ""),
                "relativeAmount": row.get("RelativeAmount", ""),
                "dueMethod": due_method,
                "dueValue": row.get(due_method, "") if due_method else "",
                "dueMonthsForward": row.get("DueMonthsForward", ""),
            }
        )
    flexfields: dict[str, list[dict[str, str]]] = {}
    for csv_name in (HEADER_CSV, LINE_CSV, DISCOUNT_CSV):
        populated: list[dict[str, str]] = []
        for row in rows[csv_name]:
            values = {
                key: value
                for key, value in row.items()
                if re.fullmatch(r"Attribute(?:Category|[1-9]|1[0-5])", key) and value.strip()
            }
            if values:
                populated.append(values)
        if populated:
            flexfields[csv_name] = populated
    return {
        "operationId": resolution.get("operationId", "operation-1"),
        "operationIndex": resolution.get("operationIndex", 1),
        "action": resolution["action"],
        "name": resolution["name"],
        "setCode": resolution["setCode"],
        "description": header.get("Description", ""),
        "startDateActive": header.get("StartDateActive", ""),
        "endDateActive": header.get("EndDateActive", ""),
        "baseAmount": header.get("BaseAmount", ""),
        "baseAmountMeaning": "Ratio denominator for installment RelativeAmount values; not a transaction currency amount.",
        "printingLeadDays": header.get("PrintingLeadDays", ""),
        "installmentOption": {
            "code": header.get("FirstInstallmentCode", ""),
            "meaning": INSTALLMENT_OPTION_LABELS.get(header.get("FirstInstallmentCode", ""), ""),
        },
        "billingCycle": header.get("CycleName", ""),
        "creditCheck": header.get("CreditCheckFlag", ""),
        "prepayment": header.get("PrepaymentFlag", ""),
        "allowDiscountOnPartialPayments": header.get("PartialDiscountFlag", ""),
        "discountBasis": {
            "code": header.get("CalcDiscountOnLinesFlag", ""),
            "meaning": DISCOUNT_BASIS_LABELS.get(header.get("CalcDiscountOnLinesFlag", ""), ""),
        },
        "discountBasisDateType": header.get("DiscountBasisDateType", ""),
        "lines": lines,
        "translations": [
            {
                "language": row.get("Language", ""),
                "sourceLanguage": row.get("SourceLang", ""),
                "name": row.get("Name", ""),
                "description": row.get("Description", ""),
            }
            for row in rows[TRANSLATION_CSV]
        ],
        "discounts": [
            {
                "lineSequence": row.get("AR_PAYMENT_TERM_LINE.SequenceNum", ""),
                "sequence": row.get("SequenceNum", ""),
                "percent": row.get("DiscountPercent", ""),
                "days": row.get("DiscountDays", ""),
                "date": row.get("DiscountDate", ""),
                "dayOfMonth": row.get("DiscountDayOfMonth", ""),
                "monthsForward": row.get("DiscountMonthsForward", ""),
            }
            for row in rows[DISCOUNT_CSV]
        ],
        "flexfields": flexfields,
        "appliedDefaults": resolution.get("appliedDefaults", {}),
        "changeSummary": _change_summary(before, rows),
    }


def _batch_business_summary(operation_summaries: list[dict[str, Any]]) -> dict[str, Any]:
    action_counts: dict[str, int] = {}
    row_counts = {csv_name: 0 for csv_name in PAYMENT_TERM_CSVS}
    for summary in operation_summaries:
        action = summary["action"]
        action_counts[action] = action_counts.get(action, 0) + 1
        row_counts[HEADER_CSV] += 1
        row_counts[LINE_CSV] += len(summary["lines"])
        row_counts[TRANSLATION_CSV] += len(summary["translations"])
        row_counts[DISCOUNT_CSV] += len(summary["discounts"])
    return {
        "operationCount": len(operation_summaries),
        "actionCounts": action_counts,
        "packageGenerationAtomic": True,
        "fusionTransactionAtomicity": "Not asserted; live processing and fresh-export reconciliation must check every operation.",
        "operations": operation_summaries,
        "rowCounts": row_counts,
        "baseAmountMeaning": "Each operation's BaseAmount is the ratio denominator for its installment RelativeAmount values; it is not a transaction currency amount.",
    }


def _annotated_issues(
    issues: list[Issue],
    rows: dict[str, list[dict[str, str]]],
    resolutions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Attach a stable batch operation identity to row-level validation findings."""
    by_identity = {
        (resolution["name"], resolution["setCode"]): resolution
        for resolution in resolutions
    }
    annotated: list[dict[str, Any]] = []
    for issue in issues:
        item = issue.as_dict()
        if issue.entity in rows and issue.row is not None:
            index = issue.row - 2
            if 0 <= index < len(rows[issue.entity]):
                row = rows[issue.entity][index]
                if issue.entity == HEADER_CSV:
                    identity = (row.get("Name", ""), row.get("SetCode", ""))
                else:
                    identity = (
                        row.get("AR_PAYMENT_TERM.Name", ""),
                        row.get("AR_PAYMENT_TERM.SetCode", ""),
                    )
                resolution = by_identity.get(identity)
                if resolution:
                    item.update(
                        {
                            "operationId": resolution["operationId"],
                            "operationIndex": resolution["operationIndex"],
                            "name": resolution["name"],
                            "setCode": resolution["setCode"],
                        }
                    )
        annotated.append(item)
    return annotated


def _prepare_design(
    template_path: Path,
    baseline_path: Path,
    blueprint_path: Path,
) -> tuple[PackageData, PackageData, dict[str, Any], dict[str, list[dict[str, str]]], dict[str, Any], dict[str, Any], str, dict[str, Any]]:
    template = _read_package(template_path)
    template_issues = _task_scope_issues(template, exact_task=True)
    for csv_name in PAYMENT_TERM_CSVS:
        if template.rows[csv_name]:
            template_issues.append(Issue("nonblank_template", f"Build template {csv_name} contains data rows."))
    populated_other = {name: count for name, count in template.other_csv_row_counts.items() if count}
    if populated_other:
        template_issues.append(Issue("nonblank_template", "Build template contains populated non-Payment-Terms CSV files."))
    if template_issues:
        raise PackageError("invalid_task_template", "Template is not a clean successful task-level Payment Terms template.", errors=[issue.as_dict() for issue in template_issues])

    baseline = _read_package(baseline_path)
    baseline_issues = _task_scope_issues(baseline, exact_task=True)
    populated_other_baseline = {name: count for name, count in baseline.other_csv_row_counts.items() if count}
    if populated_other_baseline:
        baseline_issues.append(Issue("unrelated_baseline_data", "Baseline contains populated non-Payment-Terms CSV files."))
    if baseline_issues:
        raise PackageError("invalid_task_baseline", "Baseline is not a successful task-level Payment Terms export.", errors=[issue.as_dict() for issue in baseline_issues])
    if template.process_envs != baseline.process_envs:
        raise PackageError(
            "template_baseline_environment_mismatch",
            "Template and baseline were exported from different Fusion environments.",
            templateEnvironment=template.process_envs,
            baselineEnvironment=baseline.process_envs,
        )
    if template.process_releases != baseline.process_releases:
        raise PackageError(
            "template_baseline_release_mismatch",
            "Template and baseline were exported from different Fusion releases.",
            templateRelease=template.process_releases,
            baselineRelease=baseline.process_releases,
        )
    if not _object_contracts_compatible(template.object_contracts, baseline.object_contracts):
        raise PackageError("template_baseline_metadata_mismatch", "Template and baseline Payment Terms field contracts differ.")
    for csv_name in PAYMENT_TERM_CSVS:
        if template.headers[csv_name] != baseline.headers[csv_name]:
            raise PackageError("template_baseline_mismatch", f"{csv_name} headers differ between template and baseline.")

    blueprint = _load_blueprint(blueprint_path)
    rows, resolutions, evidence, operation_rows = _prepare_operations(template, baseline, blueprint)
    design_package = replace(template, rows=rows)
    design_errors, design_warnings = _validate_rows(design_package, evidence)
    if design_errors or design_warnings:
        raise PackageError(
            "candidate_design_invalid",
            "Normalized Payment Terms design has unresolved validation findings.",
            errors=_annotated_issues(design_errors, rows, resolutions),
            warnings=_annotated_issues(design_warnings, rows, resolutions),
        )
    digest = _design_sha256(template, baseline, blueprint, rows)
    operation_summaries = [
        _business_summary(
            prepared,
            resolution,
            _rows_for_parent(baseline, resolution["name"], resolution["setCode"]),
        )
        for prepared, resolution in zip(operation_rows, resolutions)
    ]
    if len(resolutions) == 1:
        resolution: dict[str, Any] = resolutions[0]
        summary = operation_summaries[0]
    else:
        resolution = {
            "operationCount": len(resolutions),
            "packageGenerationAtomic": True,
            "operations": resolutions,
        }
        summary = _batch_business_summary(operation_summaries)
    return template, baseline, blueprint, rows, resolution, evidence, digest, summary


def preview_package(template_path: Path, baseline_path: Path, blueprint_path: Path) -> dict[str, Any]:
    template, baseline, _blueprint, rows, resolution, _evidence, digest, summary = _prepare_design(
        template_path,
        baseline_path,
        blueprint_path,
    )
    return {
        "status": "confirmation_required",
        "mode": "offline_preview",
        "taskCode": TASK_CODE,
        "resolution": resolution,
        "businessSummary": summary,
        "rowCounts": {name: len(rows[name]) for name in PAYMENT_TERM_CSVS},
        "designSha256": digest,
        "templateSha256": template.sha256,
        "baselineSha256": baseline.sha256,
        "confirmationInstruction": "Show the business summary and ask the customer to reply exactly confirm before generating the local ZIP.",
        "externalCalls": 0,
        "mutationAuthorized": False,
    }


def _write_candidate(template_path: Path, output_path: Path, rows: dict[str, list[dict[str, str]]], headers: dict[str, list[str]]) -> None:
    output_path = output_path.resolve()
    if output_path.suffix.lower() != ".zip":
        raise PackageError("invalid_output", "Output path must end in .zip.")
    if output_path in {template_path.resolve()}:
        raise PackageError("unsafe_output", "Output ZIP must not overwrite the template.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    replacement = {name: _csv_bytes(headers[name], rows[name]) for name in PAYMENT_TERM_CSVS}
    with tempfile.NamedTemporaryFile(prefix=f".{output_path.name}.", suffix=".tmp", dir=output_path.parent, delete=False) as temp:
        temp_path = Path(temp.name)
    try:
        with zipfile.ZipFile(template_path) as source, zipfile.ZipFile(temp_path, "w") as target:
            members = _member_map(source)
            replacement_paths = {members[name].filename: replacement[name] for name in PAYMENT_TERM_CSVS}
            for info in source.infolist():
                if info.is_dir():
                    target.writestr(info, b"")
                    continue
                target.writestr(info, replacement_paths.get(info.filename, source.read(info)))
        if not zipfile.is_zipfile(temp_path) or temp_path.stat().st_size == 0:
            raise PackageError("artifact_persistence", "Generated candidate is not a valid nonempty ZIP.")
        os.replace(temp_path, output_path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def build_package(template_path: Path, baseline_path: Path, blueprint_path: Path, output_path: Path) -> dict[str, Any]:
    output_path = output_path.resolve()
    protected_inputs = {template_path.resolve(), baseline_path.resolve(), blueprint_path.resolve()}
    if output_path in protected_inputs:
        raise PackageError("unsafe_output", "Output ZIP must not overwrite the template, baseline, or blueprint input.")
    if output_path.exists():
        raise PackageError("output_exists", f"Refusing to overwrite an existing candidate ZIP: {output_path}")
    template, baseline, blueprint, rows, resolution, evidence, digest, summary = _prepare_design(
        template_path,
        baseline_path,
        blueprint_path,
    )
    confirmation = blueprint.get("confirmation", {})
    if confirmation.get("confirmed") is not True or confirmation.get("design_sha256") != digest:
        raise PackageError(
            "design_confirmation_required",
            "Show the normalized business summary and obtain a standalone confirm response before generating the local ZIP.",
            designSha256=digest,
            businessSummary=summary,
        )
    _write_candidate(template.path, output_path, rows, template.headers)
    validation = validate_package(
        output_path,
        exact_task=True,
        verified_evidence=evidence,
        expected_baseline=baseline,
        expected_blueprint=blueprint,
    )
    if validation["status"] != "ready":
        output_path.unlink(missing_ok=True)
        raise PackageError(
            "candidate_validation_failed",
            "Generated candidate failed Payment Terms validation.",
            errors=validation["errors"],
            warnings=validation["warnings"],
        )
    with tempfile.TemporaryDirectory(prefix="payment-terms-repeat-") as repeat_directory:
        repeated_path = Path(repeat_directory) / "candidate-repeat.zip"
        _write_candidate(template.path, repeated_path, rows, template.headers)
        repeated_sha256 = hashlib.sha256(repeated_path.read_bytes()).hexdigest()
    if repeated_sha256 != validation["sha256"]:
        output_path.unlink(missing_ok=True)
        raise PackageError(
            "nondeterministic_candidate",
            "Repeated generation did not produce identical candidate bytes.",
            firstSha256=validation["sha256"],
            repeatedSha256=repeated_sha256,
        )
    return {
        "status": "ready",
        "mode": "offline_prepare",
        "taskCode": TASK_CODE,
        "taskName": "Manage Receivables Payment Terms",
        "targetEnvironment": template.process_envs[0],
        "targetRelease": template.process_releases[0],
        "output": str(output_path.resolve()),
        "resolution": resolution,
        "businessSummary": summary,
        "designSha256": digest,
        "confirmationVerified": True,
        "rowCounts": validation["rowCounts"],
        "archiveMembers": validation["archiveMembers"],
        "sha256": validation["sha256"],
        "repeatedSha256": repeated_sha256,
        "deterministic": True,
        "uploadHandoff": {
            "fileName": output_path.name,
            "sha256": validation["sha256"],
            "taskCode": TASK_CODE,
            "taskName": "Manage Receivables Payment Terms",
            "requiredSurface": "Open the exact Manage Receivables Payment Terms setup task and use its Import from CSV File action.",
            "wrongSurfaceWarning": "Do not upload this task-level ZIP from an offering-level or functional-area-level import page.",
            "approvalState": "Not approved or uploaded by offline preparation.",
        },
        "warnings": validation["warnings"],
        "externalCalls": 0,
        "mutationAuthorized": False,
    }


def reconcile_package(candidate_path: Path, export_path: Path) -> dict[str, Any]:
    """Compare every approved candidate parent with a fresh successful task export."""
    candidate = _read_package(candidate_path)
    exported = _read_package(export_path)
    errors = _task_scope_issues(exported, exact_task=True)
    if candidate.process_envs != exported.process_envs:
        errors.append(Issue("candidate_export_environment_mismatch", "Candidate and fresh export identify different Fusion environments."))
    if candidate.process_releases != exported.process_releases:
        errors.append(Issue("candidate_export_release_mismatch", "Candidate and fresh export identify different Fusion releases."))
    if not _object_contracts_compatible(candidate.object_contracts, exported.object_contracts):
        errors.append(Issue("candidate_export_metadata_mismatch", "Candidate and fresh export Payment Terms contracts differ."))
    export_languages = sorted(
        {
            row.get(field_name, "").strip()
            for row in exported.rows[TRANSLATION_CSV]
            for field_name in ("Language", "SourceLang")
            if row.get(field_name, "").strip()
        }
    )
    candidate_validation = validate_package(
        candidate.path,
        exact_task=True,
        verified_evidence={"languages": export_languages},
    )
    errors.extend(Issue(item["code"], item["message"], item.get("entity", ""), item.get("row"), item.get("field", "")) for item in candidate_validation["errors"])
    if candidate_validation["warnings"]:
        errors.append(Issue("candidate_has_unresolved_warnings", "Candidate still has unresolved warnings and cannot be reconciled as verified."))
    if not candidate.rows[HEADER_CSV]:
        errors.append(Issue("candidate_header_count", "Reconciliation requires at least one candidate payment-term header."))

    candidate_types = _metadata_type_map(candidate)

    mismatches: list[dict[str, Any]] = []
    additional_translation_languages: list[str] = []
    persisted_row_counts = {csv_name: 0 for csv_name in PAYMENT_TERM_CSVS}
    terms: list[dict[str, Any]] = []
    for candidate_header in candidate.rows[HEADER_CSV]:
        name = candidate_header.get("Name", "")
        set_code = candidate_header.get("SetCode", "")
        expected = _rows_for_parent(candidate, name, set_code)
        target = _rows_for_parent(exported, name, set_code)
        term_mismatches: list[dict[str, Any]] = []
        term_additional_languages: list[str] = []
        if len(target[HEADER_CSV]) != 1:
            term_mismatches.append(
                {
                    "entity": HEADER_CSV,
                    "code": "persisted_header_not_exact",
                    "expected": 1,
                    "actual": len(target[HEADER_CSV]),
                }
            )
        for csv_name in PAYMENT_TERM_CSVS:
            persisted_row_counts[csv_name] += len(target[csv_name])
            expected_by_key = {_summary_key(csv_name, row): row for row in expected[csv_name]}
            actual_by_key = {_summary_key(csv_name, row): row for row in target[csv_name]}
            for key in sorted(set(expected_by_key) - set(actual_by_key)):
                term_mismatches.append({"entity": csv_name, "code": "persisted_row_missing", "key": list(key)})
            extra_keys = sorted(set(actual_by_key) - set(expected_by_key))
            if csv_name == TRANSLATION_CSV:
                term_additional_languages.extend(key[0] for key in extra_keys if key and key[0])
            else:
                for key in extra_keys:
                    term_mismatches.append({"entity": csv_name, "code": "unexpected_persisted_row", "key": list(key)})
            for key in sorted(set(expected_by_key) & set(actual_by_key)):
                expected_row = expected_by_key[key]
                actual_row = actual_by_key[key]
                for field_name, expected_value in expected_row.items():
                    if field_name in AUDIT_COLUMNS:
                        continue
                    actual_value = actual_row.get(field_name, "")
                    value_type = candidate_types.get(csv_name, {}).get(field_name, "")
                    if not _reconciled_values_equal(value_type, expected_value, actual_value):
                        term_mismatches.append(
                            {
                                "entity": csv_name,
                                "code": "persisted_field_mismatch",
                                "key": list(key),
                                "field": field_name,
                                "expected": expected_value,
                                "actual": actual_value,
                            }
                        )
        for mismatch in term_mismatches:
            mismatch["name"] = name
            mismatch["setCode"] = set_code
        mismatches.extend(term_mismatches)
        additional_translation_languages.extend(term_additional_languages)
        terms.append(
            {
                "name": name,
                "setCode": set_code,
                "candidateRowCounts": {csv_name: len(expected[csv_name]) for csv_name in PAYMENT_TERM_CSVS},
                "persistedRowCounts": {csv_name: len(target[csv_name]) for csv_name in PAYMENT_TERM_CSVS},
                "additionalSystemTranslationLanguages": sorted(set(term_additional_languages)),
                "mismatches": term_mismatches,
                "verified": not term_mismatches,
            }
        )

    status = "verified" if not errors and not mismatches else "blocked"
    single_term = terms[0] if len(terms) == 1 else {}
    return {
        "status": status,
        "mode": "offline_persisted_state_reconciliation",
        "taskCode": TASK_CODE,
        "taskName": "Manage Receivables Payment Terms",
        "targetEnvironment": exported.process_envs[0] if exported.process_envs else "",
        "targetRelease": exported.process_releases[0] if exported.process_releases else "",
        "name": single_term.get("name", ""),
        "setCode": single_term.get("setCode", ""),
        "operationCount": len(terms),
        "terms": terms,
        "candidateSha256": candidate.sha256,
        "freshExportSha256": exported.sha256,
        "candidateRowCounts": {csv_name: len(candidate.rows[csv_name]) for csv_name in PAYMENT_TERM_CSVS},
        "persistedRowCounts": persisted_row_counts,
        "additionalSystemTranslationLanguages": sorted(set(additional_translation_languages)),
        "errors": [issue.as_dict() for issue in errors],
        "mismatches": mismatches,
        "externalCalls": 0,
        "mutationAuthorized": False,
    }


def _emit(result: dict[str, Any], *, stream: Any = sys.stdout) -> None:
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True), file=stream)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    preview = subparsers.add_parser("preview", help="Resolve and validate a design summary without creating a ZIP.")
    preview.add_argument("--template", type=Path, required=True)
    preview.add_argument("--baseline", type=Path, required=True)
    preview.add_argument("--blueprint", type=Path, required=True)

    build = subparsers.add_parser("build", help="Build and validate a candidate ZIP without external calls.")
    build.add_argument("--template", type=Path, required=True)
    build.add_argument("--baseline", type=Path, required=True)
    build.add_argument("--blueprint", type=Path, required=True)
    build.add_argument("--output", type=Path, required=True)

    validate = subparsers.add_parser("validate", help="Validate an existing ZIP without external calls.")
    validate.add_argument("--package", type=Path, required=True)
    validate.add_argument(
        "--allow-broader-review",
        action="store_true",
        help="Report a broader package without treating it as a task-level candidate.",
    )
    validate.add_argument(
        "--source-evidence",
        action="store_true",
        help="Validate an exported template or current-data package as source evidence without applying candidate-row rules.",
    )
    validate.add_argument("--baseline", type=Path, help="Current task export used to verify candidate lookup evidence.")
    validate.add_argument("--blueprint", type=Path, help="Normalized blueprint containing any additional verified evidence.")

    reconcile = subparsers.add_parser(
        "reconcile",
        help="Compare every parent in a candidate ZIP with a fresh successful task export without external calls.",
    )
    reconcile.add_argument("--candidate", type=Path, required=True)
    reconcile.add_argument("--export", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "preview":
            result = preview_package(args.template, args.baseline, args.blueprint)
        elif args.command == "build":
            result = build_package(args.template, args.baseline, args.blueprint, args.output)
        elif args.command == "reconcile":
            result = reconcile_package(args.candidate, args.export)
        else:
            if bool(args.baseline) != bool(args.blueprint):
                raise PackageError(
                    "incomplete_validation_evidence",
                    "Candidate validation requires both --baseline and --blueprint when either is supplied.",
                )
            verified_evidence = None
            expected_baseline = None
            expected_blueprint = None
            if args.baseline and args.blueprint:
                expected_baseline = _read_package(args.baseline)
                expected_blueprint = _load_blueprint(args.blueprint)
                verified_evidence = _effective_evidence(expected_baseline, expected_blueprint)
            result = validate_package(
                args.package,
                exact_task=not args.allow_broader_review,
                source_evidence=args.source_evidence,
                verified_evidence=verified_evidence,
                expected_baseline=expected_baseline,
                expected_blueprint=expected_blueprint,
            )
    except PackageError as exc:
        result = {
            "status": "blocked",
            "taskCode": TASK_CODE,
            "error": {"code": exc.code, "message": exc.message, **exc.details},
            "externalCalls": 0,
            "mutationAuthorized": False,
        }
        _emit(result, stream=sys.stderr)
        return 2
    _emit(result)
    return 0 if result.get("status") in {"ready", "reviewed", "confirmation_required", "verified"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
