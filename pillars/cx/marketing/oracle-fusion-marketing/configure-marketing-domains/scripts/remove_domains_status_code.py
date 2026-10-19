#!/usr/bin/env python3
"""Prepare a sparse Domains update workbook from a generated template.

The FMK Domain business object defines a module-managed string ``status`` but
does not define ``$statusCode``.  The latter can appear in a Data Loader
template as framework response metadata; it must not be sent in a Domains
update source.
"""

from __future__ import annotations

import argparse
import os
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS = {"x": MAIN_NS}
CHANGED_FIELDS = frozenset({
    "emailDomainPreference", "micrositeDomainPreference", "senderName",
    "senderEmail", "replyToName", "replyToEmail", "bounceBackEmail",
})


def _column(cell_ref: str) -> str:
    return "".join(character for character in cell_ref if character.isalpha())


def _column_name(index: int) -> str:
    result = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def _cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    if cell.get("t") == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(".//x:t", NS))
    value = cell.find("x:v", NS)
    if value is None or value.text is None:
        return ""
    if cell.get("t") == "s":
        return shared_strings[int(value.text)]
    return value.text


def _set_inline_value(cell: ET.Element, value: str) -> None:
    cell.set("t", "str")
    for child in list(cell):
        cell.remove(child)
    value_element = ET.SubElement(cell, f"{{{MAIN_NS}}}v")
    value_element.text = value


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return ["".join(item.itertext()) for item in root.findall("x:si", NS)]


def prepare_sparse_update(source: Path, destination: Path, changed_fields: set[str]) -> None:
    if source.suffix.lower() != ".xlsx":
        raise ValueError("The Domains source must be an .xlsx workbook.")
    if source.resolve() == destination.resolve():
        raise ValueError("The Domains source and destination must be different paths.")
    if not changed_fields:
        raise ValueError("Specify at least one supported changed field.")
    unsupported = changed_fields - CHANGED_FIELDS
    if unsupported:
        raise ValueError("Unsupported changed fields: " + ", ".join(sorted(unsupported)))

    with zipfile.ZipFile(source) as source_archive:
        shared_strings = _shared_strings(source_archive)
        sheet_member = "xl/worksheets/sheet1.xml"
        root = ET.fromstring(source_archive.read(sheet_member))
        header = root.find("x:sheetData/x:row[@r='1']", NS)
        if header is None:
            raise ValueError("The Domains workbook has no header row.")
        headers = {
            _column(cell.get("r", "")): _cell_value(cell, shared_strings)
            for cell in header.findall("x:c", NS)
        }
        required = {"domains_id", "$operation"}
        missing = (required | changed_fields) - set(headers.values())
        if missing:
            raise ValueError("The Domains workbook is missing required columns: " + ", ".join(sorted(missing)))
        keep = required | changed_fields
        kept_columns = [column for column, name in headers.items() if name in keep]
        sheet_data = root.find("x:sheetData", NS)
        record_count = 0
        for row in sheet_data.findall("x:row", NS):
            cells_by_column = {_column(cell.get("r", "")): cell for cell in row.findall("x:c", NS)}
            is_header = row is header
            if not is_header:
                values_by_column = {
                    column: _cell_value(cell, shared_strings)
                    for column, cell in cells_by_column.items()
                }
                if not any(value.strip() for value in values_by_column.values()):
                    sheet_data.remove(row)
                    continue
                blank_fields = [
                    headers[column] for column in kept_columns
                    if headers[column] != "$operation" and not values_by_column.get(column, "").strip()
                ]
                if blank_fields:
                    raise ValueError(
                        "The Domains workbook contains blank identity or changed fields in row "
                        + row.get("r", "") + ": " + ", ".join(sorted(blank_fields))
                    )
                record_count += 1
            for cell in list(row.findall("x:c", NS)):
                row.remove(cell)
            for index, column in enumerate(kept_columns, start=1):
                cell = cells_by_column.get(column)
                if cell is None:
                    cell = ET.Element(f"{{{MAIN_NS}}}c")
                cell.set("r", _column_name(index) + row.get("r", ""))
                if headers[column] == "$operation" and not is_header:
                    _set_inline_value(cell, "MERGE")
                row.append(cell)
        if not record_count:
            raise ValueError("The Domains workbook must contain at least one nonempty record.")

        ET.register_namespace("", MAIN_NS)
        rewritten_sheet = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        if destination.exists() or destination.is_symlink():
            raise FileExistsError("The Domains destination already exists: " + str(destination))
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=".xlsx", delete=False) as temporary:
            temporary_path = Path(temporary.name)
        try:
            with zipfile.ZipFile(temporary_path, "w", zipfile.ZIP_DEFLATED) as target_archive:
                for info in source_archive.infolist():
                    target_archive.writestr(
                        info,
                        rewritten_sheet if info.filename == sheet_member else source_archive.read(info.filename),
                    )
            # Both paths share a filesystem. Linking publishes the complete file
            # atomically and fails if another writer has created the destination.
            os.link(temporary_path, destination)
        finally:
            temporary_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a sparse Domains XLSX update source.")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--changed-field", action="append", required=True)
    args = parser.parse_args()
    prepare_sparse_update(args.source, args.destination, set(args.changed_field))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
