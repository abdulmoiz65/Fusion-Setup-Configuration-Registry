#!/usr/bin/env python3
"""Compare Campaign template FSM ZIPs or build a new-only derived archive."""

from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path
import zipfile


PARENT_MEMBER = "ORA_IRC_EMP_CAMP_EMAIL_TEMPL_MSG_DESIGN.csv"
METADATA_MEMBER = "ORA_IRC_EMP_CAMP_EMAIL_TEMPL_MSG_DESIGN_METADATA.csv"
TYPES_MEMBER = "ORA_IRC_EMP_CAMP_EMAIL_TEMPL_MSG_DESIGN_TYPES.csv"
ASM_MEMBER = "ASM_SETUP_CSV_METADATA.xml"
REQUIRED_MEMBERS = (PARENT_MEMBER, METADATA_MEMBER, TYPES_MEMBER, ASM_MEMBER)


class ArchiveError(ValueError):
    """Raised when a source or target archive cannot safely be filtered."""


def read_csv_member(archive: zipfile.ZipFile, member: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        content = archive.read(member).decode("utf-8-sig")
    except KeyError as error:
        raise ArchiveError(f"Archive is missing required member {member}.") from error
    reader = csv.DictReader(io.StringIO(content))
    if not reader.fieldnames:
        raise ArchiveError(f"Archive member {member} has no CSV header.")
    return reader.fieldnames, list(reader)


def code_column(fieldnames: list[str], member: str) -> str:
    matches = [field for field in fieldnames if field == "MessageDesignCode" or field.endswith(".MessageDesignCode")]
    if len(matches) != 1:
        raise ArchiveError(f"Archive member {member} must contain exactly one MessageDesignCode column.")
    return matches[0]


def parent_identity(rows: list[dict[str, str]], *, label: str) -> tuple[set[str], set[str]]:
    names: set[str] = set()
    codes: set[str] = set()
    for row in rows:
        name = (row.get("DesignName") or "").strip()
        code = (row.get("MessageDesignCode") or "").strip()
        if not name or not code:
            raise ArchiveError(f"{label} parent CSV has a blank DesignName or MessageDesignCode.")
        if name in names or code in codes:
            raise ArchiveError(f"{label} parent CSV has a duplicate DesignName or MessageDesignCode.")
        names.add(name)
        codes.add(code)
    return names, codes


def render_csv(fieldnames: list[str], rows: list[dict[str, str]]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def compare_archives(source_archive: Path, target_export: Path) -> tuple[
    list[str], list[dict[str, str]], set[str], set[str], dict[str, object]
]:
    if not source_archive.is_file() or not target_export.is_file():
        raise ArchiveError("Source archive and fresh target export must both exist.")

    with zipfile.ZipFile(source_archive) as source, zipfile.ZipFile(target_export) as target:
        if len(source.namelist()) != len(set(source.namelist())):
            raise ArchiveError("Source archive contains duplicate member names.")
        missing = [member for member in REQUIRED_MEMBERS if member not in source.namelist()]
        if missing:
            raise ArchiveError("Source archive is missing required members: " + ", ".join(missing))

        source_parent_fields, source_parent_rows = read_csv_member(source, PARENT_MEMBER)
        target_parent_fields, target_parent_rows = read_csv_member(target, PARENT_MEMBER)
        if not {"DesignName", "MessageDesignCode"} <= set(source_parent_fields):
            raise ArchiveError("Source parent CSV is missing DesignName or MessageDesignCode.")
        if not {"DesignName", "MessageDesignCode"} <= set(target_parent_fields):
            raise ArchiveError("Target parent CSV is missing DesignName or MessageDesignCode.")
        target_names, target_codes = parent_identity(target_parent_rows, label="Target")
        parent_identity(source_parent_rows, label="Source")

    retained_parents = []
    conflicts = []
    for row in source_parent_rows:
        fields = []
        if row["DesignName"].strip() in target_names:
            fields.append("DesignName")
        if row["MessageDesignCode"].strip() in target_codes:
            fields.append("MessageDesignCode")
        if fields:
            conflicts.append({
                "DesignName": row["DesignName"].strip(),
                "MessageDesignCode": row["MessageDesignCode"].strip(),
                "conflict_fields": fields,
            })
        else:
            retained_parents.append(row)
    summary = {
        "source_archive": str(source_archive),
        "target_export": str(target_export),
        "new_template_names": [row["DesignName"].strip() for row in retained_parents],
        "conflicts": conflicts,
    }
    return source_parent_fields, retained_parents, target_names, target_codes, summary


def filter_archive(source_archive: Path, target_export: Path, output_archive: Path) -> dict[str, object]:
    if output_archive.resolve() in {source_archive.resolve(), target_export.resolve()}:
        raise ArchiveError("Derived archive path must differ from source archive and target export.")
    source_parent_fields, retained_parents, _, _, summary = compare_archives(source_archive, target_export)
    if not retained_parents:
        raise ArchiveError("No source templates are new to the target; no derived import archive was created.")
    retained_codes = {row["MessageDesignCode"].strip() for row in retained_parents}

    with zipfile.ZipFile(source_archive) as source:
        _, source_parent_rows = read_csv_member(source, PARENT_MEMBER)
        metadata_fields, metadata_rows = read_csv_member(source, METADATA_MEMBER)
        types_fields, types_rows = read_csv_member(source, TYPES_MEMBER)
        metadata_code_column = code_column(metadata_fields, METADATA_MEMBER)
        types_code_column = code_column(types_fields, TYPES_MEMBER)
        for member, rows, column in (
            (METADATA_MEMBER, metadata_rows, metadata_code_column),
            (TYPES_MEMBER, types_rows, types_code_column),
        ):
            orphans = sorted({(row.get(column) or "").strip() for row in rows if (row.get(column) or "").strip() not in {row["MessageDesignCode"].strip() for row in source_parent_rows}})
            if orphans:
                raise ArchiveError(f"{member} contains rows without a source parent: {', '.join(orphans)}")

        filtered_metadata = [row for row in metadata_rows if (row.get(metadata_code_column) or "").strip() in retained_codes]
        filtered_types = [row for row in types_rows if (row.get(types_code_column) or "").strip() in retained_codes]

        output_archive.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_archive, "w", compression=zipfile.ZIP_DEFLATED) as output:
            for member in source.namelist():
                if member == PARENT_MEMBER:
                    output.writestr(member, render_csv(source_parent_fields, retained_parents))
                elif member == METADATA_MEMBER:
                    output.writestr(member, render_csv(metadata_fields, filtered_metadata))
                elif member == TYPES_MEMBER:
                    output.writestr(member, render_csv(types_fields, filtered_types))
                else:
                    output.writestr(member, source.read(member))

    summary["output_archive"] = str(output_archive)
    summary["retained_template_names"] = summary.pop("new_template_names")
    summary["excluded_conflicting_template_names"] = [item["DesignName"] for item in summary["conflicts"]]
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-archive", type=Path, required=True)
    parser.add_argument("--target-export", type=Path, required=True)
    parser.add_argument("--output-archive", type=Path)
    parser.add_argument("--summary-json", type=Path)
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()
    try:
        if args.report_only:
            if args.output_archive:
                parser.error("--report-only cannot be combined with --output-archive.")
            summary = compare_archives(args.source_archive, args.target_export)[4]
        elif args.output_archive is None:
            parser.error("--output-archive is required unless --report-only is used.")
        else:
            summary = filter_archive(args.source_archive, args.target_export, args.output_archive)
    except (ArchiveError, OSError, UnicodeDecodeError, zipfile.BadZipFile) as error:
        parser.error(str(error))
    if args.summary_json:
        args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
