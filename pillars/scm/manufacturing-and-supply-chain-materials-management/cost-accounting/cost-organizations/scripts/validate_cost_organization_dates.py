#!/usr/bin/env python3
"""Fail closed on unsupported Cost Organizations effective-date values."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path


def validate(source: Path) -> list[str]:
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "EffectiveStartDate" not in reader.fieldnames:
            return []

        errors: list[str] = []
        for row_number, row in enumerate(reader, start=2):
            value = (row.get("EffectiveStartDate") or "").strip()
            if not value:
                continue
            try:
                parsed = date.fromisoformat(value)
            except ValueError:
                errors.append(
                    f"Row {row_number}: EffectiveStartDate {value!r} must be a real YYYY-MM-DD calendar date."
                )
                continue
            if parsed.isoformat() != value:
                errors.append(
                    f"Row {row_number}: EffectiveStartDate {value!r} must use zero-padded YYYY-MM-DD format."
                )
        return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate supplied EffectiveStartDate values for Cost Organizations CSV imports."
    )
    parser.add_argument("source", type=Path, help="Cost Organizations CSV source file")
    args = parser.parse_args()

    if not args.source.is_file():
        parser.error(f"CSV source does not exist or is not a file: {args.source}")

    try:
        errors = validate(args.source)
    except (OSError, csv.Error) as error:
        print(f"Unable to read CSV source: {error}", file=sys.stderr)
        return 2

    if errors:
        print("Cost Organizations date validation failed:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("Cost Organizations date validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
