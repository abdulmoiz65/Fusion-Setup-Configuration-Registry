#!/usr/bin/env python3
"""Generate one internal MessageDesignCode for a new Campaign template."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import io
from pathlib import Path
import re
import secrets
import zipfile


BASE32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
MAX_CODE_LENGTH = 32
NAME_STEM_LENGTH = 15
TIMESTAMP_LENGTH = 15  # YYMMDDHHMMSSmmm


def normalize_name(name: str) -> str:
    normalized = re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_")
    if not normalized:
        raise ValueError("Template name must contain at least one alphanumeric character.")
    return normalized


def generate_code(name: str, timestamp: str, nonce: str) -> str:
    if not re.fullmatch(r"\d{15}", timestamp):
        raise ValueError("Timestamp must use YYMMDDHHMMSSmmm format.")
    if nonce not in BASE32_ALPHABET:
        raise ValueError("Nonce must be one RFC 4648 Base32 character (A-Z or 2-7).")
    stem = normalize_name(name)[:NAME_STEM_LENGTH]
    code = f"{stem}_{timestamp}{nonce}"
    if len(code) > MAX_CODE_LENGTH:
        raise ValueError("Generated MessageDesignCode exceeds 32 characters.")
    return code


def read_exported_codes(target_export: Path) -> set[str]:
    """Read MessageDesignCode values from a fresh FSM export CSV or ZIP."""
    if not target_export.is_file():
        raise ValueError(f"Target export does not exist: {target_export}")
    if target_export.suffix.casefold() == ".zip":
        with zipfile.ZipFile(target_export) as archive:
            contents = [
                archive.read(member).decode("utf-8-sig")
                for member in archive.namelist()
                if member.casefold().endswith(".csv")
            ]
    elif target_export.suffix.casefold() == ".csv":
        contents = [target_export.read_text(encoding="utf-8-sig")]
    else:
        raise ValueError("Target export must be an FSM ZIP or exported CSV.")

    codes: set[str] = set()
    found_code_column = False
    for content in contents:
        reader = csv.DictReader(io.StringIO(content))
        if "MessageDesignCode" not in (reader.fieldnames or []):
            continue
        found_code_column = True
        for row in reader:
            code = (row.get("MessageDesignCode") or "").strip()
            if code:
                codes.add(code)
    if not found_code_column:
        raise ValueError("Target export has no CSV containing a MessageDesignCode column.")
    return codes


def generate_unique_code(name: str, timestamp: str, existing_codes: set[str], nonce: str | None) -> str:
    """Return a non-conflicting candidate, trying each Base32 nonce once."""
    first_nonce = nonce or secrets.choice(BASE32_ALPHABET)
    if first_nonce not in BASE32_ALPHABET:
        raise ValueError("Nonce must be one RFC 4648 Base32 character (A-Z or 2-7).")
    nonces = first_nonce + "".join(item for item in BASE32_ALPHABET if item != first_nonce)
    for candidate_nonce in nonces:
        candidate = generate_code(name, timestamp, candidate_nonce)
        if candidate not in existing_codes:
            return candidate
    raise ValueError(
        "Could not generate a unique MessageDesignCode: every Base32 nonce conflicts "
        "in the supplied fresh target export."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="Visible template name.")
    parser.add_argument("--timestamp", help="UTC timestamp in YYMMDDHHMMSSmmm format.")
    parser.add_argument("--nonce", help="Initial RFC 4648 Base32 character to try.")
    parser.add_argument(
        "--target-export",
        required=True,
        type=Path,
        help="Fresh target FSM export ZIP or CSV used to reject MessageDesignCode conflicts.",
    )
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    timestamp = args.timestamp or now.strftime("%y%m%d%H%M%S") + f"{now.microsecond // 1000:03d}"
    try:
        existing_codes = read_exported_codes(args.target_export)
        print(generate_unique_code(args.name, timestamp, existing_codes, args.nonce))
    except (OSError, UnicodeDecodeError, ValueError, zipfile.BadZipFile) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
