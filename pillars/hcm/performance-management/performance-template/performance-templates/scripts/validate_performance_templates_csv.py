#!/usr/bin/env python3
"""Pre-import validator for Performance Templates FSM CSV archives.

The validator intentionally checks only the archive invariants that can be
verified locally: documented GroupingKey composition, parent references, and
the forbidden literal ``#null``.  It does not replace task-level validation or
the Data Loader approval workflow.
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Mapping, Sequence


TEMPLATE = ("template_name", "template_date_from", "template_date_to")
ROLE = ("RoleTypeCode", "RoleName", "RoleDateFrom", "RoleDateTo")
SECTION = (
    "SectionDefnName",
    "SectionDefnDescription",
    "SectionDefnDateFrom",
    "SectionDefnDateTo",
)

GROUPING_KEY_FIELDS: Mapping[str, Sequence[object]] = {
    "HRA_TEMPLATE.csv": (TEMPLATE,),
    "HRA_TEMPLATE_TRANSLATION.csv": (TEMPLATE,),
    "HRA_TEMPLATE_ROLE.csv": (TEMPLATE, ROLE),
    "HRA_TEMPLATE_SECTION.csv": (TEMPLATE, SECTION),
    "HRA_TEMPL_SEC_ITEMS.csv": (TEMPLATE, SECTION, "CiName", "CiContextName"),
    "HRA_PROCESS_STEP_ALERTS.csv": (TEMPLATE, "StepCode"),
    "HRA_TMPL_PERIODS.csv": ("CustomaryName",),
    "HRA_TMPL_PERIODS_TRANSLATION.csv": ("CustomaryName",),
    "HRA_TMPL_PERIOD_DATES.csv": ("CustomaryName", "StepCode"),
    "ORA_TMPL_PERIOD_ELIGIBILITY_PROFILE.csv": (
        "CustomaryName",
        "EligibilityProfileName",
    ),
    "ORA_HRA_TMPL_PERIOD_QSTNR.csv": (
        "CustomaryName",
        "UserRoleTypeCode",
        "RoleName",
        "RoleDateFrom",
        "RoleDateTo",
    ),
    "ORA_HRA_TEMPLATE_ROLE_ACTION.csv": (TEMPLATE, ROLE, SECTION),
    # The document-type entity is parent-resolved and must not have a key.
    "ORA_HRA_TMPL_PERIOD_DOCUMENT_TYPE.csv": (),
}

PARENT_MEMBER: Mapping[str, str] = {
    "HRA_PROCESS_STEP_ALERTS.csv": "HRA_TEMPLATE.csv",
    "HRA_TEMPLATE_ROLE.csv": "HRA_TEMPLATE.csv",
    "HRA_TEMPLATE_TRANSLATION.csv": "HRA_TEMPLATE.csv",
    "HRA_TEMPLATE_SECTION.csv": "HRA_TEMPLATE.csv",
    "HRA_TEMPL_SEC_ITEMS.csv": "HRA_TEMPLATE_SECTION.csv",
    "ORA_HRA_TEMPLATE_ROLE_ACTION.csv": "HRA_TEMPLATE_SECTION.csv",
    "HRA_TMPL_PERIODS.csv": "HRA_TEMPLATE.csv",
    "HRA_TMPL_PERIODS_TRANSLATION.csv": "HRA_TMPL_PERIODS.csv",
    "HRA_TMPL_PERIOD_DATES.csv": "HRA_TMPL_PERIODS.csv",
    "ORA_HRA_TMPL_PERIOD_DOCUMENT_TYPE.csv": "HRA_TMPL_PERIODS.csv",
    "ORA_HRA_TMPL_PERIOD_QSTNR.csv": "HRA_TMPL_PERIODS.csv",
    "ORA_TMPL_PERIOD_ELIGIBILITY_PROFILE.csv": "HRA_TMPL_PERIODS.csv",
}


@dataclass(frozen=True)
class CsvRow:
    member: str
    line: int
    values: Mapping[str, str]


@dataclass(frozen=True)
class Issue:
    code: str
    member: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.member}:{self.line}: {self.code}: {self.message}"


def normalized_member_name(name: str) -> str:
    """Return a CSV member's base name, regardless of ZIP folder layout."""
    return Path(name).name


def read_csv_members(source: Path) -> tuple[dict[str, list[CsvRow]], list[Issue]]:
    """Read CSV files from an extracted archive directory or a ZIP file."""
    contents: list[tuple[str, str]] = []
    if source.is_dir():
        contents = [
            (str(path.relative_to(source)), path.read_text(encoding="utf-8-sig"))
            for path in source.rglob("*.csv")
        ]
    elif zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as archive:
            contents = [
                (name, archive.read(name).decode("utf-8-sig"))
                for name in archive.namelist()
                if name.lower().endswith(".csv")
            ]
    else:
        return {}, [Issue("INPUT", str(source), 0, "expected a directory or ZIP archive")]

    members: dict[str, list[CsvRow]] = {}
    issues: list[Issue] = []
    for source_name, text in contents:
        member = normalized_member_name(source_name)
        if member in members:
            issues.append(
                Issue("DUPLICATE_MEMBER", member, 0, "archive contains multiple CSV members with this name")
            )
            continue
        reader = csv.DictReader(io.StringIO(text, newline=""))
        if not reader.fieldnames:
            issues.append(Issue("EMPTY_MEMBER", member, 0, "CSV member has no header row"))
            continue
        members[member] = [
            CsvRow(member, row_number, {key: value or "" for key, value in row.items() if key})
            for row_number, row in enumerate(reader, start=2)
        ]
    return members, issues


def value_for(row: CsvRow, field: str, *, scope: str = "") -> str | None:
    """Get a field, accepting the documented qualified parent-reference forms."""
    candidates = {
        "template_name": (
            "Name",
            "HRA_TEMPLATE.Name",
            "TmplDefnName",
            "HRA_TMPL_PERIODS.TmplDefnName",
            "HRA_TEMPLATE_SECTION.TmplDefnName",
        ),
        "template_date_from": (
            "DateFrom",
            "HRA_TEMPLATE.DateFrom",
            "TmplDefnDateFrom",
            "HRA_TMPL_PERIODS.TmplDefnDateFrom",
            "HRA_TEMPLATE_SECTION.TmplDefnDateFrom",
        ),
        "template_date_to": (
            "DateTo",
            "HRA_TEMPLATE.DateTo",
            "TmplDefnDateTo",
            "HRA_TMPL_PERIODS.TmplDefnDateTo",
            "HRA_TEMPLATE_SECTION.TmplDefnDateTo",
        ),
        # Oracle's exported role-action rows use UserRoleTypeCode rather than
        # the RoleTypeCode field used by template-role rows.  They represent
        # the same business-key component in their respective CSV members.
        "RoleTypeCode": ("RoleTypeCode", "UserRoleTypeCode"),
        # Period children normally carry their parent as a qualified field.
        # Accept that exported form when validating their GroupingKey.
        "CustomaryName": ("CustomaryName", "HRA_TMPL_PERIODS.CustomaryName"),
    }.get(field, (field,))
    if scope == "root_template":
        candidates = {"template_name": ("Name",), "template_date_from": ("DateFrom",), "template_date_to": ("DateTo",)}.get(field, candidates)
    for candidate in candidates:
        if candidate in row.values:
            return row.values[candidate]
    return None


def format_key_value(field: str, value: str) -> str:
    if "date" not in field.lower():
        return value
    for pattern in ("%Y/%m/%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, pattern).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return value


def key_components(row: CsvRow, specification: Sequence[object]) -> tuple[list[str] | None, list[str]]:
    values: list[str] = []
    missing: list[str] = []
    for item in specification:
        fields = item if isinstance(item, tuple) else (item,)
        for field in fields:
            value = value_for(row, field, scope="root_template" if row.member == "HRA_TEMPLATE.csv" else "")
            if value is None or value == "":
                missing.append(str(field))
            else:
                values.append(format_key_value(str(field), value))
    return (None if missing else values), missing


def root_identity(row: CsvRow) -> tuple[str, str, str] | None:
    components, missing = key_components(row, TEMPLATE)
    return tuple(components) if not missing and components else None  # type: ignore[return-value]


def period_identity(row: CsvRow) -> tuple[str, str, str, str] | None:
    root = root_identity(row)
    customary_name = value_for(row, "CustomaryName")
    if root is None or not customary_name:
        return None
    return (*root, customary_name)


def section_identity(row: CsvRow) -> tuple[str, ...] | None:
    root = root_identity(row)
    section, missing = key_components(row, SECTION)
    if root is None or missing or section is None:
        return None
    return (*root, *section)


def parent_reference(row: CsvRow, parent_member: str) -> tuple[str, ...] | None:
    if parent_member == "HRA_TEMPLATE.csv":
        if row.member == "HRA_TEMPLATE_TRANSLATION.csv" and all(
            field in row.values for field in ("TmplDefnName", "TmplDefnDateFrom", "TmplDefnDateTo")
        ):
            return (
                row.values["TmplDefnName"],
                format_key_value("template_date_from", row.values["TmplDefnDateFrom"]),
                format_key_value("template_date_to", row.values["TmplDefnDateTo"]),
            )
        values, missing = key_components(row, TEMPLATE)
        return tuple(values) if values is not None and not missing else None
    if parent_member == "HRA_TMPL_PERIODS.csv":
        # Period document-type children also carry their own unqualified
        # Name/DateFrom/DateTo fields.  Prefer the qualified period-parent
        # reference so those child fields cannot be mistaken for the root
        # template identity.
        parent_name = (
            row.values.get("HRA_TMPL_PERIODS.TmplDefnName")
            or row.values.get("TmplDefnName")
            or row.values.get("HRA_TEMPLATE.Name")
            or row.values.get("Name")
        )
        parent_from = (
            row.values.get("HRA_TMPL_PERIODS.TmplDefnDateFrom")
            or row.values.get("TmplDefnDateFrom")
            or row.values.get("HRA_TEMPLATE.DateFrom")
            or row.values.get("DateFrom")
        )
        parent_to = (
            row.values.get("HRA_TMPL_PERIODS.TmplDefnDateTo")
            or row.values.get("TmplDefnDateTo")
            or row.values.get("HRA_TEMPLATE.DateTo")
            or row.values.get("DateTo")
        )
        customary_name = value_for(row, "HRA_TMPL_PERIODS.CustomaryName") or value_for(row, "CustomaryName")
        if not parent_name or not parent_from or not parent_to or not customary_name:
            return None
        return (
            parent_name,
            format_key_value("template_date_from", parent_from),
            format_key_value("template_date_to", parent_to),
            customary_name,
        )
    if parent_member == "HRA_TEMPLATE_SECTION.csv":
        root, root_missing = key_components(row, TEMPLATE)
        section, section_missing = key_components(row, SECTION)
        if root is None or section is None or root_missing or section_missing:
            return None
        return (*root, *section)
    raise ValueError(f"No parent-reference resolver for {parent_member}")


def validate_grouping_keys(members: Mapping[str, list[CsvRow]]) -> list[Issue]:
    issues: list[Issue] = []
    for member, rows in members.items():
        if member not in GROUPING_KEY_FIELDS:
            continue
        specification = GROUPING_KEY_FIELDS[member]
        for row in rows:
            actual = row.values.get("GroupingKey")
            if not specification:
                if actual:
                    issues.append(Issue("GROUPING_KEY_MUST_BE_BLANK", member, row.line, "this record is parent-resolved"))
                continue
            components, missing = key_components(row, specification)
            if missing:
                issues.append(Issue("MISSING_KEY_COMPONENT", member, row.line, f"missing {', '.join(missing)}"))
                continue
            expected = ",".join(components or [])
            if actual != expected:
                issues.append(Issue("GROUPING_KEY_MISMATCH", member, row.line, f"expected {expected!r}; found {actual!r}"))
    return issues


def validate_parent_references(members: Mapping[str, list[CsvRow]]) -> list[Issue]:
    issues: list[Issue] = []
    parent_identities = {
        "HRA_TEMPLATE.csv": {identity for row in members.get("HRA_TEMPLATE.csv", []) if (identity := root_identity(row))},
        "HRA_TMPL_PERIODS.csv": {identity for row in members.get("HRA_TMPL_PERIODS.csv", []) if (identity := period_identity(row))},
        "HRA_TEMPLATE_SECTION.csv": {identity for row in members.get("HRA_TEMPLATE_SECTION.csv", []) if (identity := section_identity(row))},
    }
    for member, parent_member in PARENT_MEMBER.items():
        rows = members.get(member, [])
        if rows and parent_member not in members:
            issues.append(Issue("MISSING_PARENT_MEMBER", member, 0, f"requires {parent_member}"))
            continue
        for row in rows:
            reference = parent_reference(row, parent_member)
            if reference is None:
                issues.append(Issue("MISSING_PARENT_REFERENCE", member, row.line, f"cannot form {parent_member} identity"))
            elif reference not in parent_identities[parent_member]:
                issues.append(Issue("STALE_PARENT_REFERENCE", member, row.line, f"does not resolve to a {parent_member} row"))
    return issues


def validate_forbidden_nulls(members: Mapping[str, list[CsvRow]]) -> list[Issue]:
    return [
        Issue("FORBIDDEN_HASH_NULL", member, row.line, f"{field} contains #null; leave generated IDs empty")
        for member, rows in members.items()
        for row in rows
        for field, value in row.values.items()
        if value.strip().lower() == "#null"
    ]


def validate_fsm_section_types(members: Mapping[str, list[CsvRow]]) -> list[Issue]:
    """Reject REST/export-only section type codes that FSM does not accept."""
    return [
        Issue(
            "NONCANONICAL_FSM_SECTION_TYPE",
            row.member,
            row.line,
            "SectionTypeCode GOALS is a REST/export value; use the FSM lookup code GOAL",
        )
        for row in members.get("HRA_TEMPLATE_SECTION.csv", [])
        if row.values.get("SectionTypeCode") == "GOALS"
    ]


def validate(source: Path) -> list[Issue]:
    """Return all locally detectable validation issues for *source*."""
    members, issues = read_csv_members(source)
    if issues and not members:
        return issues
    return [
        *issues,
        *validate_forbidden_nulls(members),
        *validate_fsm_section_types(members),
        *validate_grouping_keys(members),
        *validate_parent_references(members),
    ]


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="extracted FSM archive directory or ZIP file")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    issues = validate(args.archive)
    if not issues:
        print("PASS: FSM section-type, GroupingKey, parent-reference, and #null checks passed.")
        return 0
    for issue in issues:
        print(f"ERROR: {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
