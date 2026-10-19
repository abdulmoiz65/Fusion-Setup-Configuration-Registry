#!/usr/bin/env python3
"""Select one enabled and effective lookup code from Apps Common output.

The caller must obtain ``lookupCodes`` through
``core.fusion-api.apps-common.lookups``.  This task-local helper deliberately
does not accept credentials, invoke REST, or own foundation lookup transport.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def is_effective(row: dict[str, Any], as_of: date) -> bool:
    if str(row.get("EnabledFlag", "")).upper() != "Y":
        return False
    start = str(row.get("StartDateActive") or "0001-01-01")[:10]
    end = str(row.get("EndDateActive") or "4712-12-31")[:10]
    try:
        return date.fromisoformat(start) <= as_of <= date.fromisoformat(end)
    except ValueError:
        return False


def effective_codes(payload: dict[str, Any], as_of: date) -> list[dict[str, str]]:
    rows = payload.get("lookupCodes")
    if not isinstance(rows, list):
        return []
    return [
        {
            "code": str(row.get("LookupCode", "")),
            "meaning": str(row.get("Meaning", "")),
            "start_date": str(row.get("StartDateActive") or ""),
            "end_date": str(row.get("EndDateActive") or ""),
        }
        for row in rows
        if isinstance(row, dict) and row.get("LookupCode") and is_effective(row, as_of)
    ]


def select_code(candidates: list[dict[str, str]], *, code: str | None, meaning: str | None) -> dict[str, str]:
    if bool(code) == bool(meaning):
        raise ValueError("Provide exactly one of code or meaning.")
    key, probe = ("code", code) if code else ("meaning", meaning)
    matches = [candidate for candidate in candidates if normalized(candidate[key]) == normalized(str(probe))]
    if not matches:
        raise LookupError(f"No current effective code matches {key} {probe!r}.")
    if len(matches) != 1:
        raise LookupError(f"Multiple current effective codes match {key} {probe!r}.")
    return matches[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lookup-type", required=True)
    parser.add_argument("--payload", type=Path, required=True, help="Apps Common lookup response JSON.")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--code")
    selector.add_argument("--meaning")
    parser.add_argument("--as-of", default=date.today().isoformat())
    args = parser.parse_args()
    try:
        as_of = date.fromisoformat(args.as_of)
        payload = json.loads(args.payload.read_text(encoding="utf-8"))
        candidates = effective_codes(payload, as_of)
        selected = select_code(candidates, code=args.code, meaning=args.meaning)
    except (OSError, ValueError, json.JSONDecodeError, LookupError) as exc:
        print(json.dumps({"lookup_type": args.lookup_type, "error": str(exc)}))
        return 2
    print(json.dumps({"lookup_type": args.lookup_type, "as_of": as_of.isoformat(), "selected": selected, "candidates": candidates}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
