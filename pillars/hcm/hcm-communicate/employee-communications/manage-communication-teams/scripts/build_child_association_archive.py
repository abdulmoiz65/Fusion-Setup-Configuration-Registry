#!/usr/bin/env python3
"""Build a HCM Communicate child-only archive with its required root header.

The generic XLSX-to-DAT converter omits a blank root worksheet.  For
``communicateUICommTeams`` child loads, Fusion still requires the root metadata
line even though no parent record may be included.  This task-local builder
copies the exact root header from a current generated workbook and prepends it
to a validated child-only archive.  It never creates, updates, or deletes a
parent team record.
"""

from __future__ import annotations

import argparse
import posixpath
from pathlib import Path
import xml.etree.ElementTree as etree
import zipfile


ROOT = "communicateUICommTeams"
DAT_MEMBER = f"{ROOT}.dat"
MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


class ArchiveError(ValueError):
    """Raised when a task-local child archive cannot be built safely."""


def _qualified(namespace: str, name: str) -> str:
    return f"{{{namespace}}}{name}"


def root_header_from_workbook(workbook_path: Path) -> tuple[str, ...]:
    """Read the exact root-sheet header from the current generated workbook."""
    if not workbook_path.is_file():
        raise ArchiveError("Current generated workbook does not exist.")
    try:
        with zipfile.ZipFile(workbook_path) as workbook:
            workbook_xml = etree.fromstring(workbook.read("xl/workbook.xml"))
            sheets = workbook_xml.find(_qualified(MAIN_NS, "sheets"))
            if sheets is None:
                raise ArchiveError("Generated workbook has no worksheets.")
            first_sheet = sheets.find(_qualified(MAIN_NS, "sheet"))
            if first_sheet is None or first_sheet.get("name") != ROOT:
                raise ArchiveError(f"The first generated worksheet must be {ROOT}.")
            relation_id = first_sheet.get(_qualified(REL_NS, "id"))
            if not relation_id:
                raise ArchiveError("Generated workbook root worksheet has no relationship ID.")
            relationships = etree.fromstring(workbook.read("xl/_rels/workbook.xml.rels"))
            target = next(
                (
                    relation.get("Target")
                    for relation in relationships.findall(_qualified(PACKAGE_REL_NS, "Relationship"))
                    if relation.get("Id") == relation_id
                ),
                None,
            )
            if not target:
                raise ArchiveError("Generated workbook root worksheet relationship is missing.")
            # Fusion's generated workbook uses package-absolute relationship
            # targets (for example, ``/xl/worksheets/sheet1.xml``).  Support
            # both those and standard workbook-relative targets.
            sheet_member = (
                target.lstrip("/")
                if target.startswith("/")
                else posixpath.normpath(posixpath.join("xl", target))
            )
            sheet_xml = etree.fromstring(workbook.read(sheet_member))
    except (OSError, zipfile.BadZipFile, KeyError, etree.ParseError) as error:
        raise ArchiveError("Current generated workbook cannot be read.") from error

    sheet_data = sheet_xml.find(_qualified(MAIN_NS, "sheetData"))
    if sheet_data is None:
        raise ArchiveError("Generated root worksheet has no data rows.")
    rows = sheet_data.findall(_qualified(MAIN_NS, "row"))
    if len(rows) != 1:
        raise ArchiveError("Generated root worksheet must contain only its header row.")
    header: list[str] = []
    for cell in rows[0].findall(_qualified(MAIN_NS, "c")):
        value = cell.findtext(_qualified(MAIN_NS, "v"))
        if value is None or not value:
            raise ArchiveError("Generated root worksheet contains a blank header.")
        header.append(value)
    if not header or header[0] != "TeamId" or "RestAction" not in header:
        raise ArchiveError("Generated root worksheet does not expose the required TeamId and RestAction header.")
    if any("|" in value or "\r" in value or "\n" in value for value in header):
        raise ArchiveError("Generated root worksheet header contains an unsafe character.")
    return tuple(header)


def build_archive(source_archive: Path, root_workbook: Path, output_archive: Path) -> None:
    """Prepend a root metadata line to a validated child-only archive."""
    if not source_archive.is_file():
        raise ArchiveError("Validated child archive does not exist.")
    if output_archive.resolve() == source_archive.resolve():
        raise ArchiveError("Output archive must differ from the validated child archive.")
    header = root_header_from_workbook(root_workbook)
    try:
        with zipfile.ZipFile(source_archive) as source:
            members = source.namelist()
            if len(members) != len(set(members)) or members != [DAT_MEMBER]:
                raise ArchiveError(f"Validated child archive must contain only {DAT_MEMBER}.")
            dat = source.read(DAT_MEMBER).decode("utf-8")
    except (OSError, zipfile.BadZipFile, UnicodeDecodeError, KeyError) as error:
        raise ArchiveError("Validated child archive cannot be read.") from error

    lines = [line for line in dat.splitlines() if line]
    if not lines:
        raise ArchiveError("Validated child archive has no DAT content.")
    root_metadata = f"METADATA|{ROOT}|"
    if any(line.startswith(root_metadata) or f"|{ROOT}|" in line for line in lines):
        raise ArchiveError("Validated child archive must not contain a root metadata or parent data row.")
    if not any(line.startswith("MERGE|") for line in lines):
        raise ArchiveError("Validated child archive has no child data row.")
    if any("\r" in line for line in lines):
        raise ArchiveError("Validated child archive contains carriage returns.")

    rendered = root_metadata + "|".join(header) + "\n" + "\n".join(lines) + "\n"
    output_archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_archive, "w", compression=zipfile.ZIP_DEFLATED) as candidate:
        candidate.writestr(DAT_MEMBER, rendered.encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validated-child-archive", type=Path, required=True)
    parser.add_argument("--current-root-workbook", type=Path, required=True)
    parser.add_argument("--output-archive", type=Path, required=True)
    args = parser.parse_args()
    try:
        build_archive(args.validated_child_archive, args.current_root_workbook, args.output_archive)
    except ArchiveError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
