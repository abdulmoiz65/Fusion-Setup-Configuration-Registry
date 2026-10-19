#!/usr/bin/env python3
"""Perform a read-only exact ProfileCode lookup for a model-profile load."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Callable

DATA_LOADER_SCRIPTS = Path(__file__).resolve().parents[5] / "core" / "data-loader" / "scripts"
sys.path.insert(0, str(DATA_LOADER_SCRIPTS))

import data_loader_metadata as metadata  # noqa: E402


def exact_match(
    config: dict[str, Any], profile_code: str, *, getter: Callable[..., Any] = metadata.get_json
) -> dict[str, Any]:
    """Return canonical exact-target evidence for one supplied ProfileCode."""
    supplied_code = profile_code.strip()
    if not supplied_code:
        raise ValueError("profile_code must not be blank")
    query = urllib.parse.urlencode(
        {
            "q": f"ProfileCode='{supplied_code}'",
            "fields": "ProfileId,ProfileCode",
            "totalResults": "true",
            "onlyData": "true",
            "limit": "500",
        }
    )
    response = getter(
        config["host"] + "/hcmRestApi/resources/11.13.18.05/profilesLov?" + query,
        config["auth"],
        stage="profile-exact-match",
    )
    if not isinstance(response, dict) or not isinstance(response.get("items"), list):
        raise metadata.DataLoadError(
            "profile-exact-match", "Profile exact-match lookup returned a malformed response."
        )
    items = response["items"]
    matches = [
        {
            "ProfileId": item.get("ProfileId"),
            "ProfileCode": item.get("ProfileCode"),
        }
        for item in items
        if isinstance(item, dict) and item.get("ProfileCode") == supplied_code
    ]
    status = "not-found" if not matches else "exactly-one" if len(matches) == 1 else "ambiguous"
    return {
        "status": status,
        "profileCode": supplied_code,
        "matchCount": len(matches),
        "matches": matches,
        "createAllowed": status == "not-found",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile-code", required=True)
    parser.add_argument("--properties", default="core/auth/fusionEnv.properties")
    parser.add_argument("--token-cache")
    parser.add_argument("--no-open-browser", action="store_true")
    args = parser.parse_args()
    try:
        config = metadata.read_config(
            Path(args.properties),
            token_cache=args.token_cache,
            open_browser=not args.no_open_browser,
        )
        print(json.dumps(exact_match(config, args.profile_code), indent=2))
        return 0
    except metadata.DataLoadError as exc:
        print(json.dumps({"status": "failed", "stage": exc.stage, "message": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
