#!/usr/bin/env python3
"""Compare approved readable ProfileItem fields with documented Fusion LOV data.

Only ``talentProfileItemsLOV`` fields documented for model-profile item reads
are accepted. The helper is read-only and reports unreadable approved fields as
not verified rather than treating them as matches.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Callable


DATA_LOADER_SCRIPTS = Path(__file__).resolve().parents[5] / "core" / "data-loader" / "scripts"
SKILL_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(DATA_LOADER_SCRIPTS))
sys.path.insert(0, str(SKILL_SCRIPTS))

import data_loader_metadata as metadata  # noqa: E402
from profile_pagination import validated_page  # noqa: E402


PATH = "/hcmRestApi/resources/11.13.18.05/talentProfileItemsLOV"
READABLE_FIELDS = ("ProfileItemId", "ProfileId", "SectionId", "SectionName", "DisplayItemName", "FreeFormItemName")


def profile_items(config: dict[str, Any], profile_id: str, *, getter: Callable[..., Any] = metadata.get_json) -> list[dict[str, Any]]:
    """Read every documented ProfileItem LOV page for one model profile."""
    if not profile_id.strip().isdigit():
        raise ValueError("profile_id must be a numeric Fusion ProfileId")
    offset, results = 0, []
    while True:
        query = urllib.parse.urlencode({
            "finder": f"findByProfileId;ProfileId={profile_id.strip()}",
            "fields": ",".join(READABLE_FIELDS),
            "limit": "500",
            "offset": str(offset),
            "onlyData": "true",
        })
        response = getter(config["host"] + PATH + "?" + query, config["auth"], stage="profile-item-approved-versus-saved-readback")
        items, has_more = validated_page(
            response,
            offset=offset,
            label="Talent Profile Items LOV",
            stage="profile-item-approved-versus-saved-readback",
            data_load_error=metadata.DataLoadError,
        )
        results.extend(item for item in items if isinstance(item, dict))
        if not has_more:
            return results
        if not items:
            raise metadata.DataLoadError("profile-item-approved-versus-saved-readback", "Talent Profile Items LOV pagination did not advance.")
        offset += len(items)


def compare(expected: dict[str, Any], items: list[dict[str, Any]]) -> dict[str, Any]:
    """Require one item identity and compare only documented readable fields."""
    item_id = str(expected.get("ProfileItemId") or "").strip()
    if not item_id.isdigit():
        return {"status": "blocked", "message": "Approved comparison input requires numeric ProfileItemId."}
    matches = [item for item in items if str(item.get("ProfileItemId") or "") == item_id]
    if len(matches) != 1:
        return {"status": "blocked", "profileItemId": item_id, "matchCount": len(matches), "message": "Expected exactly one saved ProfileItem."}
    fields = []
    for field, expected_value in expected.items():
        if field not in READABLE_FIELDS:
            fields.append({"field": field, "expected": expected_value, "status": "not-readable-by-supported-readback"})
            continue
        actual = matches[0].get(field)
        fields.append({"field": field, "expected": expected_value, "actual": actual,
                       "status": "matched" if str(actual) == str(expected_value) else "mismatch"})
    verified = bool(fields) and all(field["status"] == "matched" for field in fields)
    return {"status": "verified" if verified else "not-verified", "profileItemId": item_id, "fields": fields,
            "message": "All approved readable ProfileItem fields match saved Fusion values." if verified else "One or more approved fields could not be compared or did not match."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile-id", required=True)
    parser.add_argument("--expected-json", required=True, type=Path, help="Approved readable field values, including ProfileItemId.")
    parser.add_argument("--properties", default="core/auth/fusionEnv.properties")
    parser.add_argument("--token-cache")
    parser.add_argument("--no-open-browser", action="store_true")
    args = parser.parse_args()
    try:
        expected = json.loads(args.expected_json.read_text(encoding="utf-8"))
        if not isinstance(expected, dict):
            raise ValueError("expected_json must contain one object")
        config = metadata.read_config(Path(args.properties), token_cache=args.token_cache, open_browser=not args.no_open_browser)
        print(json.dumps(compare(expected, profile_items(config, args.profile_id)), indent=2))
        return 0
    except (metadata.DataLoadError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "failed", "stage": "profile-item-approved-versus-saved-readback", "message": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
