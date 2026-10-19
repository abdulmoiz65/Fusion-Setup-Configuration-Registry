#!/usr/bin/env python3
"""Remove payload and credential material from a core CX adapter result."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any


SENSITIVE_KEYS = {
    "authorization",
    "accesstoken",
    "access_token",
    "refreshtoken",
    "refresh_token",
    "clientsecret",
    "client_secret",
    "documentcontent",
    "content",
}


def sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if key.casefold() in SENSITIVE_KEYS else sanitize(child)
            for key, child in value.items()
        }
    if isinstance(value, list):
        return [sanitize(child) for child in value]
    return value


def atomic_write(path: Path, content: str, *, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise ValueError(f"Output already exists: {path}. Use --overwrite only after review.")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
            temporary_name = handle.name
        os.replace(temporary_name, path)
    finally:
        if temporary_name and Path(temporary_name).exists():
            Path(temporary_name).unlink()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sanitize a core CX import adapter JSON result.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def run(args: argparse.Namespace) -> dict[str, Any]:
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    sanitized = sanitize(payload)
    atomic_write(
        args.output,
        json.dumps(sanitized, indent=2, sort_keys=True) + "\n",
        overwrite=args.overwrite,
    )
    return {
        "status": "sanitized",
        "output": str(args.output.resolve()),
        "contentId": sanitized.get("contentId") if isinstance(sanitized, dict) else None,
        "importActivityId": sanitized.get("ImportActivityId") if isinstance(sanitized, dict) else None,
    }


def main(argv: list[str] | None = None) -> int:
    try:
        result = run(parse_args(argv))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({
            "status": "failed",
            "failureClass": "artifact_persistence",
            "message": str(exc),
        }))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
