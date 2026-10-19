"""Validate and reconcile the supported Wage Basis Rules HDL contract offline.

Canonical policy lives in ../ora-resource. Inputs are supplied by the governed
caller, not discovered here. The helper validates an immutable TaxabilityRule
DAT against an independently resolved expectation, or compares complete
normalized before/after histories with the requested business effect.

It does not perform LOV discovery, infer intent, authenticate, call Fusion,
prepare or submit a live archive, grant approval, or establish loader success.
JSON output contains classifications and counts only.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, timedelta
import json
from pathlib import Path
import re


# Native and REST field contracts ---------------------------------------------

# These are the only mutation effects backed by the current verified contract.
OPERATIONS = ("create", "update", "correct", "delete_record_and_history")
CONTEXT = tuple(f"Context{i}" for i in range(1, 7))
STORED_CONTEXT = tuple(f"ContextValue{i}" for i in range(1, 7))
FOREIGN_IDS = ("ClassificationId", "SecondaryClassificationId",
               "DeductionTypeId", "LegislativeDataGroupId")
DATES = ("EffectiveStartDate", "EffectiveEndDate")
EXISTING = ("TaxabilityRulesId", *DATES, *FOREIGN_IDS, *CONTEXT)
CREATE_BASE = ("EffectiveStartDate", "LegislativeDataGroupName",
               "PayrollComponent", "PrimaryClassification", "SecondaryClassification")
OPEN_END = "4712-12-31"


# Sanitized primitive validation ----------------------------------------------

class ContractError(ValueError):
    """Error code only: never include an input value in an exception."""


def require(condition, code):
    """Raise a sanitized contract code without echoing supplied data."""
    if not condition:
        raise ContractError(code)


def parse_date(value, separator="-"):
    """Parse one full-year date using the explicitly required separator."""
    require(isinstance(value, str), "DATE_TYPE")
    pattern = rf"[0-9]{{4}}{separator}[0-9]{{2}}{separator}[0-9]{{2}}"
    require(re.fullmatch(pattern, value) is not None, "DATE_FORMAT")
    try:
        return date.fromisoformat(value.replace(separator, "-"))
    except ValueError:
        raise ContractError("DATE_INVALID") from None


def identifier(value, optional=False):
    """Normalize a positive numeric identifier while rejecting booleans."""
    if optional and value in (None, ""):
        return ""
    require(not isinstance(value, bool) and isinstance(value, (str, int)), "ID_TYPE")
    value = str(value)
    require(re.fullmatch(r"[0-9]+", value) is not None and int(value) > 0, "ID_INVALID")
    return str(int(value))


# Immutable native DAT validation ---------------------------------------------

def validate_dat(text, operation, expected_rows):
    """Validate prepared DAT bytes against exact, independently resolved rows.

    This function checks representation and equality only. It never derives the
    expected rows from the DAT under test and never authorizes submission.
    """
    require(operation in OPERATIONS, "OPERATION_UNSUPPORTED")
    require(isinstance(text, str) and "\x00" not in text, "DAT_ENCODING")
    require(not text.startswith("\ufeff"), "DAT_BOM")
    lines = text.splitlines()
    require(bool(lines) and all(lines), "DAT_EMPTY_LINE")
    if operation in ("update", "correct"):
        require(lines[0] == "SET PURGE_FUTURE_CHANGES N", "PURGE_CONTROL")
        lines = lines[1:]
    require(len(lines) >= 2, "DAT_NO_ROWS")
    header = lines[0].split("|")
    require(header[:2] == ["METADATA", "TaxabilityRule"], "HEADER_DISCRIMINATOR")
    fields = tuple(header[2:])
    if operation == "create":
        # Create can omit inactive trailing context columns, but active columns
        # must remain ordered and contiguous from Context1.
        shapes = [(*CREATE_BASE, *CONTEXT[:n], "UsageType") for n in range(7)]
        require(fields in shapes, "HEADER_SHAPE")
    else:
        shape = EXISTING + (() if operation == "delete_record_and_history" else ("UsageType",))
        require(fields == shape, "HEADER_SHAPE")
        require(len(lines) == 2, "ONE_LOGICAL_TARGET_REQUIRED")
    instruction = "DELETE" if operation == "delete_record_and_history" else "MERGE"
    rows = []
    for line in lines[1:]:
        cells = line.split("|")  # split preserves every trailing empty cell.
        require(len(cells) == len(header), "FIELD_COUNT")
        require(cells[:2] == [instruction, "TaxabilityRule"], "ROW_INSTRUCTION")
        row = dict(zip(fields, cells[2:]))
        start = parse_date(row["EffectiveStartDate"], "/")
        if "EffectiveEndDate" in row:
            require(start <= parse_date(row["EffectiveEndDate"], "/"), "DATE_RANGE")
        if "UsageType" in row:
            require(row["UsageType"] in ("P", "N"), "USAGE_INVALID")
        if operation == "create":
            require(all(row[f].strip() for f in CREATE_BASE[1:4]), "BUSINESS_KEY_MISSING")
        else:
            for field in ("TaxabilityRulesId", *FOREIGN_IDS):
                identifier(row[field], optional=field == "SecondaryClassificationId")
        rows.append(row)
    if operation == "create":
        # Effective start and inclusion are effects, not identity discriminators;
        # changing either cannot turn a duplicate logical rule into a new rule.
        keys = [tuple(row[f] for f in fields if f not in ("EffectiveStartDate", "UsageType"))
                for row in rows]
        require(len(set(keys)) == len(keys), "DUPLICATE_LOGICAL_KEY")
    require(isinstance(expected_rows, list) and bool(expected_rows), "EXPECTED_ROWS_MISSING")
    require(all(isinstance(row, dict) and set(row) == set(fields)
                and all(isinstance(value, str) for value in row.values())
                for row in expected_rows), "EXPECTED_ROWS_SHAPE")
    require(rows == expected_rows, "EXPECTED_VALUES_MISMATCH")
    return {"status": "PASS", "operation": operation, "rows": len(rows),
            "scope": "offline_contract_only"}


# REST history normalization and expected effects -----------------------------

def normalize_slice(row, new=False):
    """Normalize one complete REST-style slice into comparison-safe strings."""
    require(isinstance(row, dict), "SLICE_SHAPE")
    required = {*DATES, *FOREIGN_IDS, *STORED_CONTEXT, "UsageType"}
    if not new:
        required.add("TaxabilityRulesId")
    require(required.issubset(row), "SLICE_FIELDS_MISSING")
    if new:
        require("TaxabilityRulesId" not in row, "CREATE_ID_SUPPLIED")
    result = {}
    for field in FOREIGN_IDS:
        result[field] = identifier(row[field], optional=field == "SecondaryClassificationId")
    if not new:
        result["TaxabilityRulesId"] = identifier(row["TaxabilityRulesId"])
    for field in DATES:
        result[field] = parse_date(row[field]).isoformat()
    require(result[DATES[0]] <= result[DATES[1]], "DATE_RANGE")
    require(row["UsageType"] in ("P", "N"), "USAGE_INVALID")
    result["UsageType"] = row["UsageType"]
    for field in STORED_CONTEXT:
        value = row[field]
        require(value is None or (not isinstance(value, bool)
                                 and isinstance(value, (str, int))), "CONTEXT_TYPE")
        result[field] = "" if value is None else str(value)
    return result


def logical_key(row):
    """Return the stable logical identity shared by all dated versions."""
    return tuple(row[field] for field in (*FOREIGN_IDS, *STORED_CONTEXT))


def normalize_history(rows):
    """Normalize complete history and reject identity drift or overlapping slices."""
    require(isinstance(rows, list), "HISTORY_NOT_ARRAY")
    result = [normalize_slice(row) for row in rows]
    identities, ids, versions = {}, {}, {}
    for row in result:
        key, target = logical_key(row), row["TaxabilityRulesId"]
        require(identities.setdefault(target, key) == key, "ID_IDENTITY_CHANGED")
        require(ids.setdefault(key, target) == target, "DUPLICATE_LOGICAL_IDENTITY")
        versions.setdefault(target, []).append(row)
    for timeline in versions.values():
        timeline.sort(key=lambda row: row[DATES[0]])
        for previous, current in zip(timeline, timeline[1:]):
            require(previous[DATES[1]] < current[DATES[0]], "OVERLAPPING_HISTORY")
    return result


def expected_history(operation, before, change):
    """Calculate a supported business effect, not Fusion transport behavior."""
    require(operation in OPERATIONS, "OPERATION_UNSUPPORTED")
    require(isinstance(change, dict), "CHANGE_SHAPE")
    if operation == "create":
        require(set(change) == {"rows"}, "CHANGE_FIELDS")
        require(isinstance(change["rows"], list) and bool(change["rows"]), "CREATE_ROWS_MISSING")
        created = [normalize_slice(row, new=True) for row in change["rows"]]
        keys = [logical_key(row) for row in created]
        require(len(set(keys)) == len(keys), "DUPLICATE_LOGICAL_KEY")
        require(not set(keys).intersection(logical_key(row) for row in before), "CREATE_CONFLICT")
        require(all(row[DATES[1]] == OPEN_END for row in created), "FINITE_CREATE_PENDING")
        return before + created
    allowed = {"target_id", "whole_history"} if operation == "delete_record_and_history" else {
        "target_id", "date" if operation == "update" else "start", "usage"}
    require(set(change) == allowed, "CHANGE_FIELDS")
    target = identifier(change["target_id"])
    selected = [row for row in before if row["TaxabilityRulesId"] == target]
    require(bool(selected), "TARGET_NOT_FOUND")
    others = [row.copy() for row in before if row["TaxabilityRulesId"] != target]
    if operation == "delete_record_and_history":
        require(change["whole_history"] is True, "WHOLE_HISTORY_INTENT_REQUIRED")
        return others
    require(change["usage"] in ("P", "N"), "USAGE_INVALID")
    selected = sorted((row.copy() for row in selected), key=lambda row: row[DATES[0]])
    if operation == "update":
        # Only the last open-ended slice can be split by the verified Update
        # contract. Existing future changes require a different proven shape.
        boundary = parse_date(change["date"])
        last = selected[-1]
        require(last[DATES[1]] == OPEN_END, "UPDATE_SHAPE_PENDING")
        require(parse_date(last[DATES[0]]) < boundary <= parse_date(OPEN_END), "UPDATE_BOUNDARY")
        require(last["UsageType"] != change["usage"], "NO_CHANGE")
        new = last.copy()
        last[DATES[1]] = (boundary - timedelta(days=1)).isoformat()
        new[DATES[0]], new["UsageType"] = boundary.isoformat(), change["usage"]
        selected.append(new)
    else:
        # Correction selects an actual physical version start; an interior
        # as-of date must be resolved to that start before this helper is called.
        start = parse_date(change["start"]).isoformat()
        matches = [row for row in selected if row[DATES[0]] == start]
        require(len(matches) == 1, "CORRECTION_SLICE_NOT_FOUND")
        require(matches[0]["UsageType"] != change["usage"], "NO_CHANGE")
        matches[0]["UsageType"] = change["usage"]
    return others + selected


def reconcile(evidence):
    """Compare complete successful readback with the independently expected history."""
    require(isinstance(evidence, dict), "EVIDENCE_SHAPE")
    require(evidence.get("complete") is True, "INCOMPLETE_READBACK")
    require(evidence.get("loader_success") is True, "LOADER_SUCCESS_UNPROVEN")
    require({"operation", "before", "after", "change"}.issubset(evidence), "EVIDENCE_MISSING")
    before = normalize_history(evidence["before"])
    after = normalize_history(evidence["after"])
    expected = expected_history(evidence["operation"], before, evidence["change"])
    old_keys = {logical_key(row) for row in before}
    if evidence["operation"] == "create":
        old_ids = {row["TaxabilityRulesId"] for row in before}
        require(not any(row["TaxabilityRulesId"] in old_ids and logical_key(row) not in old_keys
                        for row in after), "CREATE_ID_REUSED")

    def signature(row):
        copy = row.copy()
        if evidence["operation"] == "create" and logical_key(row) not in old_keys:
            # New IDs are server assigned, so a Create match is based on the
            # full business identity, dates, contexts, and inclusion instead.
            copy.pop("TaxabilityRulesId", None)
        return tuple(sorted(copy.items()))

    matched = Counter(map(signature, expected)) == Counter(map(signature, after))
    return {"status": "PASS" if matched else "CONTRACT_INCOMPLETE",
            "operation": evidence["operation"], "expected_slices": len(expected),
            "observed_slices": len(after), "scope": "offline_comparison_only"}


# Non-networking command-line adapter -----------------------------------------

def read_json(path):
    """Read one UTF-8 JSON fixture supplied by the governed caller."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    """Expose the two offline checks as a small non-networking CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("validate-dat", help="Check supplied immutable DAT against expected rows")
    check.add_argument("--operation", required=True, choices=OPERATIONS)
    check.add_argument("--dat", required=True)
    check.add_argument("--expected", required=True)
    compare = commands.add_parser("reconcile", help="Compare supplied complete normalized histories")
    compare.add_argument("--evidence", required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate-dat":
            result = validate_dat(Path(args.dat).read_text(encoding="utf-8"), args.operation,
                                  read_json(args.expected))
        else:
            result = reconcile(read_json(args.evidence))
    except ContractError as error:
        result = {"status": "FAILED", "code": str(error)}
    except (OSError, UnicodeError, ValueError, TypeError, KeyError):
        result = {"status": "FAILED", "code": "INVALID_OR_UNREADABLE_INPUT"}
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
