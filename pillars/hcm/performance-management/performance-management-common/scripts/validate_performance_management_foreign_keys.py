#!/usr/bin/env python3
"""Validate declared foreign-key and parent-reference tuples in an FSM archive.

This is a Performance Management pillar pre-import gate.  The supplied
reference bundle must declare every applicable external foreign key from a
fresh export or documented lookup; the script fails closed when that evidence
does not cover the requested task or archive shape.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


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
        location = f"{self.member}:{self.line}" if self.line else self.member
        return f"{location}: {self.code}: {self.message}"


def _member_name(value: str) -> str:
    return Path(value).name


def _read_archive(source: Path) -> tuple[dict[str, list[CsvRow]], list[Issue]]:
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
        return {}, [Issue("INPUT", str(source), 0, "expected an extracted archive directory or ZIP file")]

    members: dict[str, list[CsvRow]] = {}
    issues: list[Issue] = []
    for source_name, text in contents:
        member = _member_name(source_name)
        if member in members:
            issues.append(Issue("DUPLICATE_MEMBER", member, 0, "multiple CSV members share this name"))
            continue
        reader = csv.DictReader(io.StringIO(text, newline=""))
        if not reader.fieldnames:
            issues.append(Issue("EMPTY_MEMBER", member, 0, "CSV member has no header row"))
            continue
        members[member] = [
            CsvRow(member, line, {key: value or "" for key, value in row.items() if key})
            for line, row in enumerate(reader, start=2)
        ]
    return members, issues


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    if path.is_file():
        with path.open("rb") as source:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()
    for csv_path in sorted(path.rglob("*.csv"), key=lambda item: str(item.relative_to(path)).casefold()):
        digest.update(str(csv_path.relative_to(path)).replace("\\", "/").encode("utf-8"))
        digest.update(b"\0")
        digest.update(csv_path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _read_bundle(path: Path, task_code: str) -> tuple[dict[str, Any] | None, list[Issue]]:
    try:
        bundle = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return None, [Issue("REFERENCE_BUNDLE", str(path), 0, f"cannot read JSON reference bundle: {error}")]
    if not isinstance(bundle, dict):
        return None, [Issue("REFERENCE_BUNDLE", str(path), 0, "reference bundle must be a JSON object")]
    if bundle.get("schema_version") != "1.0":
        return None, [Issue("REFERENCE_BUNDLE", str(path), 0, "schema_version must be 1.0")]
    if bundle.get("task_code") != task_code:
        return None, [Issue("TASK_CODE_MISMATCH", str(path), 0, "reference bundle task_code does not match --task-code")]
    if bundle.get("coverage") != "all-foreign-keys":
        return None, [Issue("INCOMPLETE_REFERENCE_COVERAGE", str(path), 0, "coverage must be all-foreign-keys")]
    for collection in ("foreign_key_checks", "parent_reference_checks"):
        if not isinstance(bundle.get(collection), list):
            return None, [Issue("REFERENCE_BUNDLE", str(path), 0, f"{collection} must be an array")]
    return bundle, []


def _columns(row: CsvRow, columns: Sequence[Any]) -> tuple[str, ...] | None:
    if not all(isinstance(column, str) and column for column in columns):
        return None
    if any(column not in row.values for column in columns):
        return None
    return tuple(row.values[column] for column in columns)


def _key_value(column: str, value: str) -> str:
    if "date" not in column.lower():
        return value
    for pattern in ("%Y/%m/%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, pattern).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return value


def _validate_foreign_keys(members: Mapping[str, list[CsvRow]], bundle: Mapping[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    for index, check in enumerate(bundle["foreign_key_checks"], start=1):
        if not isinstance(check, dict):
            issues.append(Issue("REFERENCE_BUNDLE", "foreign_key_checks", index, "check must be an object"))
            continue
        member = check.get("member")
        columns = check.get("columns")
        allowed = check.get("allowed_tuples")
        if not isinstance(member, str) or not isinstance(columns, list) or not isinstance(allowed, list) or not allowed:
            issues.append(Issue("REFERENCE_BUNDLE", "foreign_key_checks", index, "member, columns, and nonempty allowed_tuples are required"))
            continue
        rows = members.get(_member_name(member))
        if rows is None:
            issues.append(Issue("MISSING_FOREIGN_KEY_MEMBER", _member_name(member), 0, "declared foreign-key member is absent"))
            continue
        allowed_tuples = {
            tuple(str(value) for value in item)
            for item in allowed
            if isinstance(item, list) and len(item) == len(columns)
        }
        if len(allowed_tuples) != len(allowed):
            issues.append(Issue("REFERENCE_BUNDLE", "foreign_key_checks", index, "allowed_tuples must contain one value for every column"))
            continue
        grouping_key_columns = check.get("grouping_key_columns")
        if grouping_key_columns is not None and not isinstance(grouping_key_columns, list):
            issues.append(Issue("REFERENCE_BUNDLE", "foreign_key_checks", index, "grouping_key_columns must be an array when supplied"))
            continue
        for row in rows:
            actual = _columns(row, columns)
            if actual is None:
                issues.append(Issue("MISSING_FOREIGN_KEY_COLUMN", row.member, row.line, f"missing one of: {', '.join(columns)}"))
                continue
            if actual not in allowed_tuples:
                issues.append(Issue("FOREIGN_KEY_MISMATCH", row.member, row.line, f"{check.get('name', member)} does not match a trusted reference tuple"))
            if grouping_key_columns is not None:
                key_values = _columns(row, grouping_key_columns)
                if key_values is None or "GroupingKey" not in row.values:
                    issues.append(Issue("MISSING_GROUPING_KEY_COMPONENT", row.member, row.line, "cannot derive GroupingKey from grouping_key_columns"))
                    continue
                expected = ",".join(_key_value(column, value) for column, value in zip(grouping_key_columns, key_values))
                if row.values["GroupingKey"] != expected:
                    issues.append(Issue("GROUPING_KEY_MISMATCH", row.member, row.line, f"expected {expected!r}; found {row.values['GroupingKey']!r}"))
    return issues


def _validate_parent_references(members: Mapping[str, list[CsvRow]], bundle: Mapping[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    for index, check in enumerate(bundle["parent_reference_checks"], start=1):
        if not isinstance(check, dict):
            issues.append(Issue("REFERENCE_BUNDLE", "parent_reference_checks", index, "check must be an object"))
            continue
        child_member = check.get("child_member")
        parent_member = check.get("parent_member")
        child_columns = check.get("child_columns")
        parent_columns = check.get("parent_columns")
        if not all(isinstance(value, str) for value in (child_member, parent_member)) or not isinstance(child_columns, list) or not isinstance(parent_columns, list) or len(child_columns) != len(parent_columns) or not child_columns:
            issues.append(Issue("REFERENCE_BUNDLE", "parent_reference_checks", index, "parent/child members and equal nonempty column lists are required"))
            continue
        children = members.get(_member_name(child_member))
        parents = members.get(_member_name(parent_member))
        if children is None:
            issues.append(Issue("MISSING_PARENT_REFERENCE_MEMBER", _member_name(child_member), 0, "declared child member is absent"))
            continue
        if parents is None:
            issues.append(Issue("MISSING_PARENT_MEMBER", _member_name(child_member), 0, f"requires {_member_name(parent_member)}"))
            continue
        identities = {_columns(parent, parent_columns) for parent in parents}
        identities.discard(None)
        for child in children:
            reference = _columns(child, child_columns)
            if reference is None:
                issues.append(Issue("MISSING_PARENT_REFERENCE_COLUMN", child.member, child.line, f"missing one of: {', '.join(child_columns)}"))
            elif reference not in identities:
                issues.append(Issue("STALE_PARENT_REFERENCE", child.member, child.line, f"does not resolve to {_member_name(parent_member)}"))
    return issues


def validate(archive: Path, task_code: str, reference_bundle: Path) -> tuple[list[Issue], dict[str, str]]:
    members, issues = _read_archive(archive)
    bundle, bundle_issues = _read_bundle(reference_bundle, task_code)
    issues.extend(bundle_issues)
    evidence = {"archive_sha256": _sha256(archive), "reference_bundle_sha256": _sha256(reference_bundle)}
    if bundle is None:
        return issues, evidence
    issues.extend(_validate_foreign_keys(members, bundle))
    issues.extend(_validate_parent_references(members, bundle))
    return issues, evidence


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="final extracted FSM archive directory or ZIP")
    parser.add_argument("--task-code", required=True, help="exact Oracle setup task code")
    parser.add_argument("--reference-bundle", required=True, type=Path, help="fresh reference evidence in the documented JSON format")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    try:
        issues, evidence = validate(args.archive, args.task_code, args.reference_bundle)
    except OSError as error:
        print(f"ERROR: INPUT: {error}")
        return 1
    print(f"Archive SHA-256: {evidence['archive_sha256']}")
    print(f"Reference bundle SHA-256: {evidence['reference_bundle_sha256']}")
    if not issues:
        print("PASS: all declared foreign-key and parent-reference checks passed.")
        return 0
    for issue in issues:
        print(f"ERROR: {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
