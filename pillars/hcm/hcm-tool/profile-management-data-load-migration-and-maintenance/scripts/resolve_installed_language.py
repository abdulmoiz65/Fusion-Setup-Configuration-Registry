#!/usr/bin/env python3
"""Resolve one supplied translation language to its installed Fusion LanguageCode.

This is a read-only preflight helper. It never prepares, uploads, or initiates
an HCM Data Loader archive.
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


LANGUAGES_PATH = "/fscmRestApi/resources/11.13.18.05/languagesLOV"
LANGUAGE_FIELDS = "LanguageCode,LanguageTag,Bcp47Tag,Description,InstalledFlag,ActivationStatus"


def installed_languages(config: dict[str, Any], *, getter=metadata.get_json) -> list[dict[str, Any]]:
    """Return the target's fully installed language records, sorted by code."""
    query = urllib.parse.urlencode(
        {
            "finder": "InstalledLanguageFinder",
            "fields": LANGUAGE_FIELDS,
            "limit": "500",
            "onlyData": "true",
        }
    )
    response = getter(
        config["host"] + LANGUAGES_PATH + "?" + query,
        config["auth"],
        stage="profile-translation-language-lookup",
    )
    items = response.get("items", []) if isinstance(response, dict) else []
    # InstalledLanguageFinder is the service contract that limits this response
    # to fully installed languages. InstalledFlag is an environment-specific
    # status value, not a portable Y/N Boolean, so do not reinterpret it.
    return sorted(
        [
            {
                key: item.get(key)
                for key in ("LanguageCode", "LanguageTag", "Bcp47Tag", "Description", "InstalledFlag", "ActivationStatus")
            }
            for item in items
            if isinstance(item, dict) and str(item.get("LanguageCode") or "").strip()
        ],
        key=lambda item: str(item.get("LanguageCode") or ""),
    )


def resolve_installed_language(
    config: dict[str, Any], language_code: str, *, getter=metadata.get_json
) -> dict[str, Any]:
    """Return one canonical installed language, or a safe blocking result.

    The InstalledLanguageFinder is intentionally queried without a code so the
    comparison is against the target's canonical values rather than a guessed
    case or locale representation.
    """
    supplied = language_code.strip()
    if not supplied:
        return {
            "status": "blocked",
            "suppliedLanguage": language_code,
            "message": "A translation language is required.",
        }

    sanitized_matches = [
        item
        for item in installed_languages(config, getter=getter)
        if str(item.get("LanguageCode") or "").casefold() == supplied.casefold()
    ]
    if len(sanitized_matches) != 1:
        return {
            "status": "blocked",
            "suppliedLanguage": supplied,
            "matchCount": len(sanitized_matches),
            "matches": sanitized_matches,
            "message": "The supplied language is not exactly one fully installed Fusion language.",
        }
    return {
        "status": "resolved",
        "suppliedLanguage": supplied,
        "canonicalLanguage": sanitized_matches[0]["LanguageCode"],
        "language": sanitized_matches[0],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--language-code")
    mode.add_argument("--list-installed", action="store_true")
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
        result = (
            {"status": "resolved", "languages": installed_languages(config)}
            if args.list_installed
            else resolve_installed_language(config, args.language_code)
        )
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "resolved" else 2
    except metadata.DataLoadError as exc:
        print(json.dumps({"status": "failed", "stage": exc.stage, "message": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
