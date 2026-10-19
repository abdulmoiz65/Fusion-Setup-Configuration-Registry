#!/usr/bin/env python3
"""Fail closed when a Product Management index request crosses index scopes."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile


BUSINESS_OBJECT = "productManagementESIndexedAttributes"
REQUEST_FIELDS = {
    "schema_version",
    "environment",
    "requested_index_name",
    "canonical_index_name",
    "attributes_to_add",
    "attributes_to_remove",
    "index_rebuild_requested",
}


class IndexScopeError(ValueError):
    """The request or its upload artifact is not single-index."""


def _nonblank(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise IndexScopeError(f"{field} must be one nonblank string.")
    return value.strip()


def validate_request(request: object) -> dict:
    if not isinstance(request, dict) or request.get("schema_version") != "1.0":
        raise IndexScopeError("The single-index request must be a schema_version 1.0 object.")
    if any(key in request for key in ("indexes", "index_names", "work_items", "active_work_item_id")):
        raise IndexScopeError("Multiple indexes or batch work items are not supported in one invocation.")
    unexpected = set(request) - REQUEST_FIELDS
    if unexpected:
        raise IndexScopeError("The single-index request contains unsupported fields.")
    _nonblank(request.get("environment"), "environment")
    _nonblank(request.get("requested_index_name"), "requested_index_name")
    canonical = request.get("canonical_index_name")
    if canonical is not None:
        _nonblank(canonical, "canonical_index_name")
    for field in ("attributes_to_add", "attributes_to_remove"):
        attributes = request.get(field)
        if not isinstance(attributes, list) or any(not isinstance(row, dict) for row in attributes):
            raise IndexScopeError(f"{field} must be an array of objects.")
        if any(
            key.casefold() in {"indexname", "index_name", "requested_index_name"}
            for row in attributes
            for key in row
        ):
            raise IndexScopeError(f"{field} rows must inherit the one requested index.")
    rebuild_requested = request.get("index_rebuild_requested")
    if not isinstance(rebuild_requested, bool):
        raise IndexScopeError("index_rebuild_requested must be boolean.")
    if not (request["attributes_to_add"] or request["attributes_to_remove"] or rebuild_requested):
        raise IndexScopeError("The request has no index operation.")
    return request


def validate_archive(archive_path: Path, canonical_index_name: str) -> tuple[int, str]:
    expected = _nonblank(canonical_index_name, "canonical_index_name")
    try:
        archive_bytes = archive_path.read_bytes()
        # Validate the exact snapshot being hashed, never a reopened source path.
        with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
            members = [name for name in archive.namelist() if not name.endswith("/")]
            if len(members) != 1 or Path(members[0]).name != f"{BUSINESS_OBJECT}.dat":
                raise IndexScopeError("The approved ZIP must contain exactly one indexed-attributes DAT.")
            if members[0] != f"{BUSINESS_OBJECT}.dat":
                raise IndexScopeError("The indexed-attributes DAT must be at the ZIP root.")
            lines = archive.read(members[0]).decode("utf-8-sig").splitlines()
    except (OSError, zipfile.BadZipFile, UnicodeDecodeError, RuntimeError) as error:
        raise IndexScopeError("The approved ZIP cannot be read as one UTF-8 DAT.") from error

    metadata: list[str] | None = None
    row_count = 0
    for line in lines:
        if not line.strip():
            continue
        fields = line.split("|")
        if len(fields) < 3 or fields[1] != BUSINESS_OBJECT:
            raise IndexScopeError("The DAT contains an unexpected section or malformed row.")
        if fields[0] == "METADATA":
            if metadata is not None or fields[2:].count("IndexName") != 1:
                raise IndexScopeError("The DAT must have one METADATA row with one IndexName column.")
            metadata = fields[2:]
            continue
        if fields[0] not in {"MERGE", "DELETE"} or metadata is None:
            raise IndexScopeError("The DAT has a data row before METADATA or an unsupported action.")
        if len(fields) != len(metadata) + 2:
            raise IndexScopeError("The DAT row does not match its METADATA columns.")
        actual = fields[metadata.index("IndexName") + 2]
        if actual != expected:
            raise IndexScopeError("The DAT contains a row for a different index.")
        row_count += 1
    if metadata is None or row_count == 0:
        raise IndexScopeError("The DAT must contain METADATA and at least one data row.")
    return row_count, hashlib.sha256(archive_bytes).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument(
        "--mutation-ready",
        action="store_true",
        help="Require the one requested index to have a resolved canonical name",
    )
    parser.add_argument("--archive", type=Path, help="Final immutable Data Loader ZIP to scope-check")
    args = parser.parse_args(argv)
    try:
        request = validate_request(json.loads(args.request.read_text(encoding="utf-8")))
        result = {
            "requested_index_name": request["requested_index_name"],
            "canonical_index_name": request.get("canonical_index_name"),
            "single_index_scope": True,
            "request_sha256": hashlib.sha256(
                json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
            ).hexdigest(),
        }
        if args.mutation_ready or args.archive is not None:
            _nonblank(request.get("canonical_index_name"), "canonical_index_name")
        if args.archive is not None:
            count, digest = validate_archive(args.archive, request["canonical_index_name"])
            result.update({"row_count": count, "archive_sha256": digest})
    except (OSError, json.JSONDecodeError, IndexScopeError) as error:
        print(f"Single-index request blocked: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
