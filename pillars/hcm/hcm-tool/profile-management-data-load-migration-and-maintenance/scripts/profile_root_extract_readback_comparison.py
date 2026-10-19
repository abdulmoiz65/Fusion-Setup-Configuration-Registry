#!/usr/bin/env python3
"""Compare an approved TalentProfile DAT with a read-only HCM Extract CSV.

This program never connects to Fusion. It consumes the CSV produced by the
approved ``FSCR_GROW_8164_AC6_MODEL_PROFILE_READBACK`` HCM Extract and fails
closed unless the extract contains exactly one row and every populated root
field in the approved DAT is present and equal.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


INTEGER_ID_FIELD = re.compile(r".+Id$")
INTEGER_VALUE = re.compile(r"[+-]?\d+")


def parse_talent_profile_dat(source: Path) -> dict[str, str]:
    """Return every populated field from exactly one TalentProfile DAT row."""
    rows = [line.strip().split("|") for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
    metadata_rows = [row for row in rows if len(row) > 2 and row[:2] == ["METADATA", "TalentProfile"]]
    merge_rows = [row for row in rows if len(row) > 2 and row[:2] == ["MERGE", "TalentProfile"]]
    if len(metadata_rows) != 1 or len(merge_rows) != 1:
        raise ValueError("DAT must contain exactly one TalentProfile METADATA and MERGE row")
    fields, values = metadata_rows[0][2:], merge_rows[0][2:]
    if len(fields) != len(values) or len(set(fields)) != len(fields):
        raise ValueError("TalentProfile DAT has invalid or duplicate field values")
    expected = {field: value for field, value in zip(fields, values, strict=True) if value != ""}
    if not expected.get("ProfileCode"):
        raise ValueError("TalentProfile DAT must contain a populated ProfileCode")
    return expected


def read_extract_csv(source: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Read a headered CSV while retaining enough structure to reject ambiguity."""
    with source.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError("extract CSV is empty") from exc
        header = [column.strip() for column in header]
        if not all(header) or len(set(header)) != len(header):
            raise ValueError("extract CSV header has blank or duplicate fields")
        rows: list[dict[str, str]] = []
        for row_number, row in enumerate(reader, start=2):
            if len(row) != len(header):
                raise ValueError(f"extract CSV row {row_number} does not match the header width")
            rows.append(dict(zip(header, row, strict=True)))
    return header, rows


def normalize(field: str, value: str) -> str:
    """Normalize only integer identifiers, whose documented extract types differ."""
    if INTEGER_ID_FIELD.fullmatch(field) and INTEGER_VALUE.fullmatch(value):
        return str(int(value))
    return value


def compare(expected: dict[str, str], header: list[str], rows: list[dict[str, str]]) -> dict[str, Any]:
    """Produce fail-closed field evidence for the approved-versus-saved contract."""
    profile_code = expected["ProfileCode"]
    matches = [row for row in rows if row.get("ProfileCode") == profile_code]
    if len(matches) != 1:
        return {
            "status": "blocked",
            "profileCode": profile_code,
            "matchCount": len(matches),
            "message": "Expected exactly one extract row for the approved ProfileCode.",
        }

    saved = matches[0]
    fields: list[dict[str, str]] = []
    for field, expected_value in expected.items():
        if field not in header:
            fields.append({"field": field, "expected": expected_value, "status": "missing-column"})
            continue
        actual_value = saved[field]
        if actual_value == "":
            fields.append({"field": field, "expected": expected_value, "status": "not-returned"})
        elif normalize(field, actual_value) == normalize(field, expected_value):
            fields.append({"field": field, "expected": expected_value, "actual": actual_value, "status": "matched"})
        else:
            fields.append({"field": field, "expected": expected_value, "actual": actual_value, "status": "mismatch"})
    verified = all(field["status"] == "matched" for field in fields)
    return {
        "status": "verified" if verified else "not-verified",
        "profileCode": profile_code,
        "matchCount": 1,
        "fields": fields,
        "message": "All populated approved DAT root fields match the HCM Extract." if verified else "One or more approved DAT root fields were missing, unreadable, or mismatched.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approved-dat", required=True, type=Path)
    parser.add_argument("--extract-csv", required=True, type=Path)
    args = parser.parse_args()
    try:
        expected = parse_talent_profile_dat(args.approved_dat)
        header, rows = read_extract_csv(args.extract_csv)
        result = compare(expected, header, rows)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "verified" else 2
    except (OSError, ValueError, csv.Error) as exc:
        print(json.dumps({"status": "failed", "stage": "hcm-extract-readback", "message": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
