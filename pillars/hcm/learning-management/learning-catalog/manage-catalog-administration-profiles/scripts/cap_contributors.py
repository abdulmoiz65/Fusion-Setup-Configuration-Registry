"""Pure, ephemeral CAP contributor intake; NOT a Fusion attachment converter.

The explicit local CSV contract is UTF-8, one column named personNumber or
email. No HTTP, person lookup, role grant or persistence is performed here.
"""
from __future__ import annotations

import csv
import hashlib
import io
import re


def parse_csv(content: bytes, kind: str, *, max_bytes=1048576, max_rows=10000):
    if kind not in {"personNumber", "email"} or not isinstance(content, bytes):
        raise ValueError("Select the documented local personNumber or email CSV format")
    if type(max_bytes) is not int or not 1 <= max_bytes <= 1048576 or type(max_rows) is not int or not 1 <= max_rows <= 10000:
        raise ValueError("Invalid bounded intake budget")
    if len(content) > max_bytes:
        raise ValueError("Contributor input exceeds the local byte budget")
    try:
        decoded = content.decode("utf-8-sig")
        reader = csv.reader(io.StringIO(decoded, newline=""), strict=True)
        if next(reader, None) != [kind]:
            raise ValueError("Expected exactly the selected local header")
        identifiers, seen, invalid = [], set(), []
        raw_count = duplicates = 0
        for line, row in enumerate(reader, 2):
            raw_count += 1
            if raw_count > max_rows:
                raise ValueError("Contributor input exceeds the local row budget")
            value = row[0] if len(row) == 1 else ""
            # No trimming or case-folding that could change a product identity.
            valid = (re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", value)
                     if kind == "personNumber" else
                     re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,63}", value))
            if not valid or len(value) > 254:
                invalid.append(line)
            elif value in seen:
                duplicates += 1
            else:
                seen.add(value)
                identifiers.append(value)
    except (UnicodeError, csv.Error) as error:
        raise ValueError("Unreadable UTF-8 or malformed local CSV; supply a readable export") from error
    return {"format": "cap-local-contributors-v1", "kind": kind,
            "source_sha256": hashlib.sha256(content).hexdigest(),
            "raw_rows": raw_count, "syntax_valid_rows": raw_count - len(invalid),
            "duplicate_rows": duplicates, "unique_identifiers": len(identifiers),
            "invalid_rows": invalid, "identifiers": identifiers,
            "resolved_unique_people": None, "effective_contributors": None,
            "status": "invalid" if invalid else "empty" if not raw_count else "syntax_valid",
            "write_eligible": False}


def summarize(parsed):
    """Only this redacted/count-only view may enter a project record."""
    return {key: value for key, value in parsed.items() if key != "identifiers"}


def resolution_counts(parsed, resolutions):
    """Consume evidence from a separately supported people resolver; never resolve.

    resolutions maps each exact input to zero/one/many canonical text identities.
    An absent entry is unverified, not a known missing person. The return value
    contains no roster. Cross-alias dedup requires the same canonical identity.
    """
    if parsed["status"] != "syntax_valid" or not isinstance(resolutions, dict):
        raise ValueError("Resolve only validated, nonempty intake")
    if set(resolutions) - set(parsed["identifiers"]):
        raise ValueError("Resolution evidence contains an unrequested identifier")
    resolved, unverified, unresolved, ambiguous = set(), 0, 0, 0
    for value in parsed["identifiers"]:
        if value not in resolutions:
            unverified += 1
            continue
        candidates = resolutions[value]
        if not isinstance(candidates, list) or any(not isinstance(p, str) or not p for p in candidates) or len(candidates) != len(set(candidates)):
            raise ValueError("Invalid canonical person evidence")
        if not candidates:
            unresolved += 1
        elif len(candidates) > 1:
            ambiguous += 1
        else:
            resolved.add(candidates[0])
    return {"resolved_unique_people": len(resolved), "unverified_identifiers": unverified,
            "unresolved_identifiers": unresolved, "ambiguous_identifiers": ambiguous,
            "complete": not (unverified or unresolved or ambiguous),
            "effective_contributors": None, "write_eligible": False}
