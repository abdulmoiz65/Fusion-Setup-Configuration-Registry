#!/usr/bin/env python3
"""Normalize the governed GROW-8154 XLSX intake workbook.

The parser accepts only the expected worksheet contract, rejects active or
external workbook content, and delegates row validation to the CSV normalizer.
It has no network or Fusion mutation route and retains no temporary source.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

import normalize_profile_content_library_intake as intake


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
MAX_ARCHIVE_BYTES = 20 * 1024 * 1024
MAX_UNCOMPRESSED_BYTES = 50 * 1024 * 1024
MAX_ROWS_PER_SHEET = 10000
SHEETS = {
    "Content Types": ("content_type", "HRT_MANAGE_PROFILE_CONTENT_TYPES"),
    "Content Type Properties": ("content_type_property", "HRT_MANAGE_PROFILE_CONTENT_TYPES"),
    "Content Type Relships": ("content_type_relationship", "HRT_MANAGE_PROFILE_CONTENT_TYPES"),
    "Content Items": ("content_item", "HRT_MANAGE_PROFILE_CONTENT_ITEMS"),
    "Item Rating Descriptions": ("content_item_proficiency_description", "HRT_MANAGE_PROFILE_CONTENT_ITEMS"),
    "Content Item Relships": ("content_item_relationship", "HRT_MANAGE_PROFILE_CONTENT_ITEMS"),
    "Item Catalogs": ("item_catalog", "ORA_MANAGE_PROFILE_ITEM_CATALOG"),
    "Catalog Content Items": ("item_catalog_membership", "ORA_MANAGE_PROFILE_ITEM_CATALOG"),
    "Catalog Rating Descriptions": ("item_catalog_rating_description", "ORA_MANAGE_PROFILE_ITEM_CATALOG"),
    "Instance Qualifiers": ("instance_qualifier", "HRT_MANAGE_INSTANCE_QUALIFIERS"),
    "Instance Qualifier Sets": ("instance_qualifier_set", "HRT_MANAGE_INSTANCE_QUALIFIERS"),
    "Educational Establishments": ("educational_establishment", "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS"),
    "Behavior Item Catalogs": ("behavior_item_catalog", "ORA_MANAGE_PROFILE_ITEM_CATALOG"),
    "Competency Behavior Relships": ("competency_behavior_relationship", "HRT_MANAGE_PROFILE_CONTENT_ITEMS"),
}
EXPECTED_SHEET_NAMES = ("Instructions",) + tuple(SHEETS)
ACTIVE_CONTENT = re.compile(
    r"(?:^|/)(?:vbaProject\.bin|externalLinks/|connections\.xml|queryTables/)",
    re.IGNORECASE,
)


class WorkbookContractError(ValueError):
    """Raised when a workbook cannot be treated as governed intake."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_archive(path: Path) -> zipfile.ZipFile:
    if path.stat().st_size > MAX_ARCHIVE_BYTES:
        raise WorkbookContractError("workbook exceeds the governed archive size limit")
    archive = zipfile.ZipFile(str(path), "r")
    total = 0
    seen = set()
    for info in archive.infolist():
        name = info.filename.replace("\\", "/")
        lowered = name.casefold()
        if name.startswith("/") or ".." in Path(name).parts:
            archive.close()
            raise WorkbookContractError("workbook contains an unsafe member path")
        if lowered in seen:
            archive.close()
            raise WorkbookContractError("workbook contains duplicate member names")
        if ACTIVE_CONTENT.search(name):
            archive.close()
            raise WorkbookContractError("active or external workbook content is not allowed")
        seen.add(lowered)
        total += info.file_size
        if total > MAX_UNCOMPRESSED_BYTES:
            archive.close()
            raise WorkbookContractError("workbook exceeds the uncompressed size limit")
    return archive


def _xml(archive: zipfile.ZipFile, member: str) -> ElementTree.Element:
    try:
        payload = archive.read(member)
    except KeyError as exc:
        raise WorkbookContractError("workbook is missing %s" % member) from exc
    if b"<!DOCTYPE" in payload.upper() or b"<!ENTITY" in payload.upper():
        raise WorkbookContractError("DTD and entity declarations are not allowed")
    try:
        return ElementTree.fromstring(payload)
    except ElementTree.ParseError as exc:
        raise WorkbookContractError("workbook XML is invalid") from exc


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = _xml(archive, "xl/sharedStrings.xml")
    values = []
    for item in root.findall("{%s}si" % MAIN_NS):
        values.append("".join(node.text or "" for node in item.iter("{%s}t" % MAIN_NS)))
    return values


def _column_index(reference: str) -> int:
    letters = "".join(character for character in reference if character.isalpha())
    if not letters:
        raise WorkbookContractError("worksheet cell reference is invalid")
    value = 0
    for character in letters.upper():
        value = value * 26 + ord(character) - 64
    return value - 1


def _cell_value(cell: ElementTree.Element, shared: list[str]) -> str:
    if cell.find("{%s}f" % MAIN_NS) is not None:
        raise WorkbookContractError("formulas are not allowed in the governed intake workbook")
    cell_type = cell.get("t", "")
    if cell_type == "inlineStr":
        inline = cell.find("{%s}is" % MAIN_NS)
        return "" if inline is None else "".join(
            node.text or "" for node in inline.iter("{%s}t" % MAIN_NS)
        )
    value = cell.findtext("{%s}v" % MAIN_NS, default="")
    if cell_type == "s":
        try:
            return shared[int(value)]
        except (ValueError, IndexError) as exc:
            raise WorkbookContractError("shared-string reference is invalid") from exc
    if cell_type in ("", "str", "n", "b"):
        return value
    raise WorkbookContractError("unsupported worksheet cell type %s" % cell_type)


def _sheet_map(archive: zipfile.ZipFile) -> list[tuple[str, str]]:
    workbook = _xml(archive, "xl/workbook.xml")
    relationships = _xml(archive, "xl/_rels/workbook.xml.rels")
    targets = {
        item.get("Id"): item.get("Target")
        for item in relationships.findall("{%s}Relationship" % PACKAGE_REL_NS)
        if item.get("Type", "").endswith("/worksheet")
    }
    result = []
    for sheet in workbook.findall("{%s}sheets/{%s}sheet" % (MAIN_NS, MAIN_NS)):
        name = sheet.get("name", "")
        relation = sheet.get("{%s}id" % REL_NS)
        target = targets.get(relation)
        if not target or target.startswith("/") or ".." in Path(target).parts:
            raise WorkbookContractError("worksheet relationship is missing or unsafe")
        member = "xl/" + target.lstrip("/")
        result.append((name, member))
    if tuple(name for name, _member in result) != EXPECTED_SHEET_NAMES:
        raise WorkbookContractError(
            "workbook sheets must exactly match the governed GROW-8154 template"
        )
    return result


def _sheet_rows(
    archive: zipfile.ZipFile, member: str, shared: list[str]
) -> list[tuple[int, list[str]]]:
    root = _xml(archive, member)
    rows = root.findall("{%s}sheetData/{%s}row" % (MAIN_NS, MAIN_NS))
    if len(rows) > MAX_ROWS_PER_SHEET:
        raise WorkbookContractError("worksheet exceeds the governed row limit")
    result = []
    for position, row in enumerate(rows, start=1):
        try:
            row_number = int(row.get("r", position))
        except ValueError as exc:
            raise WorkbookContractError("worksheet row reference is invalid") from exc
        values = [""] * len(intake.CONTRACT_COLUMNS)
        for cell in row.findall("{%s}c" % MAIN_NS):
            index = _column_index(cell.get("r", ""))
            if index >= len(values):
                raise WorkbookContractError("worksheet has columns outside the governed header")
            values[index] = _cell_value(cell, shared)
        result.append((row_number, values))
    return result


def normalize_workbook(path: Path) -> tuple[dict, int]:
    workbook_fingerprint = sha256_file(path)
    provenance = []
    combined_rows = []
    mapping_conflicts = {}
    archive = _safe_archive(path)
    try:
        shared = _shared_strings(archive)
        for sheet_name, member in _sheet_map(archive):
            if sheet_name == "Instructions":
                continue
            record_type, task_code = SHEETS[sheet_name]
            rows = _sheet_rows(archive, member, shared)
            if not rows or tuple(rows[0][1]) != intake.CONTRACT_COLUMNS:
                raise WorkbookContractError(
                    "%s header does not exactly match the governed template" % sheet_name
                )
            for row_number, values in rows[1:]:
                if not any(values):
                    continue
                row = dict(zip(intake.CONTRACT_COLUMNS, values))
                conflicts = [field for field, expected in (("record_type", record_type), ("task_code", task_code))
                             if row[field] not in ("", expected)]
                if conflicts:
                    # Keep supplied values. A readable conflict is review input,
                    # not authority to remap the row or discard the whole set.
                    mapping_conflicts[len(combined_rows) + 2] = conflicts
                else:
                    row["record_type"] = record_type
                    row["task_code"] = task_code
                if not row["source_reference"]:
                    row["source_reference"] = "%s!%d" % (sheet_name, row_number)
                combined_rows.append(row)
                provenance.append((sheet_name, row_number))
    finally:
        archive.close()

    # Screen via the shared normalizer without persisting raw workbook rows.
    with io.StringIO(newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=intake.CONTRACT_COLUMNS)
        writer.writeheader()
        writer.writerows(combined_rows)
        payload, exit_code = intake.normalize(Path("governed-intake.csv"), csv_text=handle.getvalue())

    payload["input_method"] = "blank_template" if not combined_rows else "spreadsheet"
    payload["source_file"] = path.name
    payload["source_fingerprint"] = workbook_fingerprint
    for record in payload.get("records", []) + payload.get("unmapped_records", []):
        csv_row = record.pop("csv_row")
        sheet_name, row_number = provenance[csv_row - 2]
        record["workbook_row"] = row_number
        record["source"] = {
            "file": path.name,
            "sheet": sheet_name,
            "row": row_number,
            "reference": record["values"]["source_reference"],
        }
        if csv_row in mapping_conflicts:
            record["mapping_readiness"] = "unmapped-requires-confirmation"
    if mapping_conflicts:
        payload["mapping_conflicts"] = [
            {"sheet": provenance[index - 2][0], "row": provenance[index - 2][1], "fields": fields}
            for index, fields in mapping_conflicts.items()
        ]
        payload["errors"].extend(
            "%s!%d %s conflicts with the governed sheet; confirm the mapping."
            % (provenance[index - 2][0], provenance[index - 2][1], field)
            for index, fields in mapping_conflicts.items() for field in fields
        )
        payload["status"], exit_code = "blocked", 2
        payload["mapping_results"] = [
            {"record_type": kind, "task_code": task, "readiness": readiness}
            for kind, task, readiness in sorted({
                (record["record_type"], record["task_code"], record["mapping_readiness"])
                for record in payload["records"]})
        ]
    if mapping_conflicts or payload.get("unmapped_records"):
        fingerprint_body = {
            "complete_set_ids": payload["complete_set_ids"],
            "task_scopes": payload["task_scopes"],
            "records": [{field: record[field] for field in
                         ("task_code", "record_type", "mapping_readiness", "values")}
                        for record in payload["records"]],
            "unmapped_records": payload["unmapped_records"],
            "mapping_conflicts": payload.get("mapping_conflicts", []),
        }
        payload["normalized_input_fingerprint"] = intake.canonical_sha256(fingerprint_body)
    return payload, exit_code


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Normalize the governed GROW-8154 multi-sheet XLSX intake workbook."
    )
    parser.add_argument("input_xlsx", type=Path)
    args = parser.parse_args(argv)
    path = args.input_xlsx.resolve()
    if not path.is_file() or path.suffix.lower() != ".xlsx":
        payload = {"schema_version": "1.0", "status": "blocked", "errors": ["Input XLSX is missing or invalid."], "blockers": []}
        exit_code = 2
    else:
        try:
            payload, exit_code = normalize_workbook(path)
        except (OSError, UnicodeError, zipfile.BadZipFile, WorkbookContractError) as exc:
            payload = {
                "schema_version": "1.0",
                "status": "blocked",
                "source_file": path.name,
                "errors": ["Workbook could not be read safely: %s" % exc],
                "blockers": [],
            }
            exit_code = 2
    print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
