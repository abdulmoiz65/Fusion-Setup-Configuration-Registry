#!/usr/bin/env python3
"""Compare one approved synthetic Talent Profile DAT row with Fusion readback.

The helper performs a read-only exact ProfileCode query.  It never uploads,
initiates, or updates Fusion data.  A comparison is verified only when Fusion
returns exactly one matching record and every approved field is readable and
identical.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from pathlib import Path
from typing import Any


DATA_LOADER_SCRIPTS = Path(__file__).resolve().parents[5] / "core" / "data-loader" / "scripts"
sys.path.insert(0, str(DATA_LOADER_SCRIPTS))

import data_loader_metadata as metadata  # noqa: E402


# Official profilesLov readback schema is intentionally narrow. Do not send
# HDL-only attributes to it: Fusion returns HTTP 400 rather than a partial row.
READBACK_FIELDS = ("ProfileId", "ProfileCode", "Description", "Summary")


def parse_talent_profile_dat(source: Path) -> dict[str, str]:
    """Read the single TalentProfile metadata/merge pair from an approved DAT."""
    rows = [line.strip().split("|") for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
    metadata_row = next((row for row in rows if len(row) > 2 and row[0] == "METADATA" and row[1] == "TalentProfile"), None)
    merge_row = next((row for row in rows if len(row) > 2 and row[0] == "MERGE" and row[1] == "TalentProfile"), None)
    if not metadata_row or not merge_row:
        raise ValueError("DAT must contain one TalentProfile METADATA and MERGE row")
    fields, values = metadata_row[2:], merge_row[2:]
    if len(fields) != len(values) or not values[0].strip():
        raise ValueError("TalentProfile DAT has incomplete field values")
    return dict(zip(fields, values, strict=True))


def profile_readback(config: dict[str, Any], profile_code: str, *, getter=metadata.get_json) -> list[dict[str, Any]]:
    collection_query = urllib.parse.urlencode({
        "q": f"ProfileCode='{profile_code}'",
        "fields": "ProfileId,ProfileCode",
        "totalResults": "true",
        "onlyData": "true",
    })
    collection = getter(
        config["host"] + "/hcmRestApi/resources/11.13.18.05/profilesLov?" + collection_query,
        config["auth"],
        stage="profile-approved-versus-saved-readback",
    )
    items = collection.get("items", []) if isinstance(collection, dict) else []
    matches = [item for item in items if isinstance(item, dict) and item.get("ProfileCode") == profile_code]
    if len(matches) != 1 or matches[0].get("ProfileId") is None:
        return matches
    item_query = urllib.parse.urlencode({"fields": ",".join(READBACK_FIELDS), "onlyData": "true"})
    item = getter(
        config["host"] + "/hcmRestApi/resources/11.13.18.05/profilesLov/" + urllib.parse.quote(str(matches[0]["ProfileId"]), safe="") + "?" + item_query,
        config["auth"],
        stage="profile-approved-versus-saved-readback",
    )
    return [item] if isinstance(item, dict) else []


def compare(expected: dict[str, str], matches: list[dict[str, Any]]) -> dict[str, Any]:
    profile_code = expected["ProfileCode"]
    if len(matches) != 1:
        return {
            "status": "blocked",
            "profileCode": profile_code,
            "matchCount": len(matches),
            "message": "Expected exactly one saved Talent Profile for approved-versus-saved comparison.",
        }
    saved = matches[0]
    fields = []
    for field, expected_value in expected.items():
        if field not in READBACK_FIELDS:
            fields.append({"field": field, "expected": expected_value, "status": "not-readable-by-supported-readback"})
            continue
        actual_value = saved.get(field)
        if actual_value is None:
            fields.append({"field": field, "expected": expected_value, "status": "not-returned"})
        elif str(actual_value) == str(expected_value):
            fields.append({"field": field, "expected": expected_value, "actual": actual_value, "status": "matched"})
        else:
            fields.append({"field": field, "expected": expected_value, "actual": actual_value, "status": "mismatch"})
    verified = all(field["status"] == "matched" for field in fields)
    return {
        "status": "verified" if verified else "not-verified",
        "profileCode": profile_code,
        "profileId": saved.get("ProfileId"),
        "fields": fields,
        "message": "All approved fields match saved Fusion values." if verified else "One or more approved fields could not be compared or did not match.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approved-dat", required=True, type=Path)
    parser.add_argument("--properties", default="core/auth/fusionEnv.properties")
    parser.add_argument("--token-cache")
    parser.add_argument("--no-open-browser", action="store_true")
    args = parser.parse_args()
    try:
        expected = parse_talent_profile_dat(args.approved_dat)
        config = metadata.read_config(Path(args.properties), token_cache=args.token_cache, open_browser=not args.no_open_browser)
        print(json.dumps(compare(expected, profile_readback(config, expected["ProfileCode"])), indent=2))
        return 0
    except (metadata.DataLoadError, ValueError) as exc:
        stage = getattr(exc, "stage", "approved-versus-saved-readback")
        print(json.dumps({"status": "failed", "stage": stage, "message": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
