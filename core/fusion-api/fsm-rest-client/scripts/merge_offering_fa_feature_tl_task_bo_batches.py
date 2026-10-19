#!/usr/bin/env python3
"""Merge deduplicated offering-task-BO batch CSVs."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

FIELDS = [
    "OFFERING", "FA_FEATURE", "PRODUCT_FAMILY", "PRODUCT", "CLASSIFICATION",
    "TASK_LIST_NAME", "TASK_NAME", "BUSINESS_OBJECT_NAME", "PATH",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("inputs", nargs="+")
    args = parser.parse_args()
    seen: set[tuple[str, ...]] = set()
    rows: list[dict[str, str]] = []
    for input_name in args.inputs:
        with Path(input_name).open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != FIELDS:
                raise ValueError(f"Unexpected CSV schema: {input_name}")
            for row in reader:
                item = {field: row.get(field, "") for field in FIELDS}
                key = tuple(item[field] for field in FIELDS)
                if key not in seen:
                    seen.add(key)
                    rows.append(item)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {target} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
