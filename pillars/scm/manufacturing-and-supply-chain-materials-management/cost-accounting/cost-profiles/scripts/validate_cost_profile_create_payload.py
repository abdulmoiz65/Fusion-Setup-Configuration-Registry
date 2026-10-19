#!/usr/bin/env python3
"""Fail closed when a Cost Profiles create payload omits required code/value pairs."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


REQUIRED_CREATE_PAIRS = (
    ("CostMethod", "CostMethodCode"),
    ("QuantityDepletionMethod", "QuantityDepletionMethodCode"),
    ("CostByUOM", "CostByUOMCode"),
    ("ProcessNegativeQuantity", "ProcessNegativeQuantityCode"),
    ("OperationScrapAccounting", "OperationScrapAccountingCode"),
    ("OperationScrapValuation", "OperationScrapValuationCode"),
    ("ReceiptWithoutCost", "ReceiptWithoutCostCode"),
    ("ReferencedRMACost", "ReferencedRMACostCode"),
    ("UnreferencedRMAReceiptCost", "UnreferencedRMAReceiptCostCode"),
    ("ProvisionalCompletions", "ProvisionalCompletionsCode"),
    ("ProcessProvisionalCompletionType", "ProcessProvisionalCompletionTypeCode"),
)

# These attributes are inapplicable when the Sheet1 source leaves both members
# blank (for example, operation-scrap and provisional-completion policies on a
# consigned profile). A supplied value must always be accompanied by its code.
CONDITIONALLY_REQUIRED_CREATE_PAIRS = {
    ("OperationScrapAccounting", "OperationScrapAccountingCode"),
    ("OperationScrapValuation", "OperationScrapValuationCode"),
    ("ProvisionalCompletions", "ProvisionalCompletionsCode"),
    ("ProcessProvisionalCompletionType", "ProcessProvisionalCompletionTypeCode"),
}


def populated(value: str | None) -> bool:
    return bool(value and value.strip())


def validate(source: Path) -> tuple[int, list[tuple[int, str]]]:
    """Return the source-row count and any fail-closed create-payload issues."""

    with source.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        rows = list(reader)

    missing_headers = [
        attribute
        for pair in REQUIRED_CREATE_PAIRS
        for attribute in pair
        if attribute not in headers
    ]
    issues: list[tuple[int, str]] = []
    if missing_headers:
        issues.append((0, "Missing required create columns: " + ", ".join(missing_headers)))

    for row_number, row in enumerate(rows, start=2):
        if (row.get("RestAction") or "").strip().upper() != "POST":
            continue
        profile = (row.get("CostProfileCode") or "<no CostProfileCode>").strip()
        for meaning_attribute, code_attribute in REQUIRED_CREATE_PAIRS:
            meaning = row.get(meaning_attribute)
            code = row.get(code_attribute)
            if (
                (row.get("ValuationStructureTypeCode") or "").strip().upper() == "CONSIGNED"
                and (meaning_attribute, code_attribute)
                in {
                    ("ReferencedRMACost", "ReferencedRMACostCode"),
                    ("UnreferencedRMAReceiptCost", "UnreferencedRMAReceiptCostCode"),
                }
                and not populated(meaning)
                and not populated(code)
            ):
                continue
            if (
                (meaning_attribute, code_attribute) in CONDITIONALLY_REQUIRED_CREATE_PAIRS
                and not populated(meaning)
                and not populated(code)
            ):
                continue
            if not populated(meaning) or not populated(code):
                missing = ", ".join(
                    attribute
                    for attribute, value in ((meaning_attribute, meaning), (code_attribute, code))
                    if not populated(value)
                )
                issues.append(
                    (row_number, f"{profile}: missing {missing} for POST."))

    return len(rows), issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate resolved code/value pairs in a Cost Profiles create CSV."
    )
    parser.add_argument("source", type=Path, help="Cost Profiles CSV source file.")
    args = parser.parse_args()

    try:
        row_count, issues = validate(args.source)
    except (OSError, csv.Error) as error:
        print(f"Payload preflight failed: {error}", file=sys.stderr)
        return 2

    if issues:
        print("## Cost Profile Create Payload Preflight Failed\n")
        print("| Row | Issue |\n|---:|---|")
        for row_number, message in issues:
            print(f"| {row_number or 'Header'} | {message} |")
        return 1

    print("## Cost Profile Create Payload Preflight Passed\n")
    print(f"Validated {row_count} source rows with all required create code/value pairs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
