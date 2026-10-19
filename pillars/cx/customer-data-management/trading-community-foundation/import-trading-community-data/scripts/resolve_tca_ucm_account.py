#!/usr/bin/env python3
"""Validate and normalize a Trading Community object's UCM account metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class MetadataError(ValueError):
    """Raise when object metadata cannot produce one authoritative UCM account."""


def normalize_ucm_account(value: str) -> str:
    segments = [segment for segment in value.strip().split("/") if segment]
    if not segments:
        raise MetadataError("Object metadata returned an unusable UcmAccount value.")
    if any("$" in segment for segment in segments):
        if all(segment.endswith("$") and "$" not in segment[:-1] for segment in segments):
            return "/".join(segments)
        raise MetadataError("Object metadata returned malformed UCM $ account syntax.")
    return "$/".join(segments) + "$"


def extract_ucm_account(payload: Any) -> str:
    candidates: list[Any] = []
    if isinstance(payload, dict):
        if "UcmAccount" in payload:
            candidates.append(payload.get("UcmAccount"))
        items = payload.get("items")
        if isinstance(items, list):
            candidates.extend(
                item.get("UcmAccount")
                for item in items
                if isinstance(item, dict) and "UcmAccount" in item
            )
    usable = [candidate.strip() for candidate in candidates if isinstance(candidate, str) and candidate.strip()]
    unique = list(dict.fromkeys(usable))
    if len(unique) != 1:
        raise MetadataError(
            f"Expected one nonblank UcmAccount in exact object metadata; found {len(unique)}."
        )
    return unique[0]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize UcmAccount from an exact CX objectMetadata GET response."
    )
    parser.add_argument("--metadata-json", type=Path, required=True)
    parser.add_argument("--object-code", required=True)
    return parser.parse_args(argv)


def run(args: argparse.Namespace) -> dict[str, str]:
    payload = json.loads(args.metadata_json.read_text(encoding="utf-8"))
    raw_account = extract_ucm_account(payload)
    return {
        "status": "resolved",
        "objectCode": args.object_code,
        "ucmDocumentAccount": normalize_ucm_account(raw_account),
    }


def main(argv: list[str] | None = None) -> int:
    try:
        result = run(parse_args(argv))
    except (OSError, json.JSONDecodeError, MetadataError) as exc:
        print(json.dumps({
            "status": "failed",
            "failureClass": "catalog_or_metadata_mismatch",
            "message": str(exc),
        }))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
