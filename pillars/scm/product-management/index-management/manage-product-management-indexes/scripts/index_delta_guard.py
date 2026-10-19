#!/usr/bin/env python3
"""Require a persisted, index-matched delta before Data Loader preparation."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
from typing import Any
import zipfile


class DeltaGuardError(ValueError):
    """Raised when a calculated index delta is missing or unsafe to use."""


def _read_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise DeltaGuardError(f"Unable to read {label}.") from error
    if not isinstance(value, dict):
        raise DeltaGuardError(f"{label} must be a JSON object.")
    return value


def _nonblank(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DeltaGuardError(f"{field} must be one nonblank string.")
    return value.strip()


def _rows(value: object, field: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
        raise DeltaGuardError(f"{field} must be an array of objects.")
    return value


def _identity(row: dict[str, Any], label: str) -> tuple[str, str, str]:
    return tuple(_nonblank(row.get(field), f"{label} {field}") for field in
                 ("attribute_code", "group_code", "object_code"))


def _request_digest(request: dict[str, Any]) -> str:
    encoded = json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _request_field(row: dict[str, Any], field: str) -> Any:
    aliases = {
        "attribute_name": "AttributeName",
        "group_name": "GroupName",
        "object_name": "ObjectName",
        "group_code": "GroupCode",
        "object_code": "ObjectCode",
        "attribute_id": "AttributeId",
    }
    return row.get(field, row.get(aliases[field]))


def _archive_rows(path: Path) -> tuple[list[dict[str, str]], str]:
    try:
        payload = path.read_bytes()
        # Validate the exact snapshot being hashed, never a reopened source path.
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            if archive.namelist() != ["productManagementESIndexedAttributes.dat"]:
                raise DeltaGuardError("The final ZIP must contain one root indexed-attributes DAT.")
            lines = archive.read("productManagementESIndexedAttributes.dat").decode("utf-8-sig").splitlines()
    except (OSError, zipfile.BadZipFile, UnicodeDecodeError, RuntimeError) as error:
        raise DeltaGuardError("Unable to read the final indexed-attributes ZIP.") from error
    header: list[str] | None = None
    rows: list[dict[str, str]] = []
    for line in lines:
        if not line.strip():
            continue
        parts = line.split("|")
        if len(parts) < 3 or parts[1] != "productManagementESIndexedAttributes":
            raise DeltaGuardError("The final DAT has an unexpected section.")
        if parts[0] == "METADATA":
            if header is not None:
                raise DeltaGuardError("The final DAT has multiple METADATA rows.")
            header = parts[2:]
            continue
        if header is None or parts[0] not in {"MERGE", "DELETE"} or len(parts) != len(header) + 2:
            raise DeltaGuardError("The final DAT has a malformed data row.")
        rows.append(dict(zip(header, parts[2:])) | {"_dat_action": parts[0]})
    if header is None or not rows:
        raise DeltaGuardError("The final DAT has no data rows.")
    return rows, hashlib.sha256(payload).hexdigest()


def validate_delta(
    request: dict[str, Any], delta: dict[str, Any], *, require_data_loader: bool,
    archive: Path | None = None,
) -> dict[str, Any]:
    """Validate the delta evidence required before loader artifact preparation."""

    canonical = _nonblank(request.get("canonical_index_name"), "canonical_index_name")
    if delta.get("schema_version") != "1.0":
        raise DeltaGuardError("index_attribute_delta must be a schema_version 1.0 object.")
    if _nonblank(delta.get("canonical_index_name"), "delta canonical_index_name") != canonical:
        raise DeltaGuardError("The delta belongs to a different canonical index.")
    if delta.get("environment") != request.get("environment"):
        raise DeltaGuardError("The delta was calculated for a different environment.")
    if delta.get("request_sha256") != _request_digest(request):
        raise DeltaGuardError("The delta does not match the current single-index request.")

    additions = _rows(delta.get("attributes_to_add"), "attributes_to_add")
    removals = _rows(delta.get("attributes_to_remove"), "attributes_to_remove")
    resolved = _rows(delta.get("resolved_requested_additions"), "resolved_requested_additions")
    seeded = _rows(delta.get("seeded_identities"), "seeded_identities")
    existing = _rows(delta.get("existing_identities"), "existing_identities")
    validated_seeded = _rows(delta.get("validated_seeded_additions"), "validated_seeded_additions")
    requested_additions = _rows(request.get("attributes_to_add"), "request attributes_to_add")
    requested_removals = _rows(request.get("attributes_to_remove"), "request attributes_to_remove")
    if len(resolved) != len(requested_additions):
        raise DeltaGuardError("Every requested addition must have one resolved identity.")
    resolved_ids: list[tuple[str, str, str]] = []
    for index, (source, target) in enumerate(zip(requested_additions, resolved)):
        if target.get("request_index") != index:
            raise DeltaGuardError("Resolved addition order does not match the request.")
        if _nonblank(target.get("attribute_name"), "resolved attribute_name").casefold() != _nonblank(
            _request_field(source, "attribute_name"), "requested attribute_name"
        ).casefold():
            raise DeltaGuardError("Resolved addition does not match the requested attribute.")
        for field in ("group_code", "object_code"):
            supplied = _request_field(source, field)
            if supplied is not None and supplied != target.get(field):
                raise DeltaGuardError("Resolved addition scope differs from the request.")
        resolved_ids.append(_identity(target, "resolved addition"))
    seeded_ids = [_identity(row, "seeded identity") for row in seeded]
    existing_ids = [_identity(row, "existing identity") for row in existing]
    if len(set(seeded_ids)) != len(seeded_ids) or len(set(existing_ids)) != len(existing_ids):
        raise DeltaGuardError("Seeded or existing identities contain duplicates.")
    validated_seeded_ids = [_identity(row, "validated seeded addition") for row in validated_seeded]
    if len(set(validated_seeded_ids)) != len(validated_seeded_ids) or set(validated_seeded_ids) != (
        set(seeded_ids) - set(existing_ids)
    ):
        raise DeltaGuardError("Validated seeded additions do not match missing seeded identities.")
    expected_additions = set(seeded_ids + resolved_ids) - set(existing_ids)
    actual_additions = [_identity(row, "addition") for row in additions]
    if len(set(actual_additions)) != len(actual_additions) or set(actual_additions) != expected_additions:
        raise DeltaGuardError("POST rows do not equal the calculated addition delta.")
    source_by_identity: dict[tuple[str, str, str], tuple[str, str, str]] = {}
    for source_row in validated_seeded + resolved:
        identity = _identity(source_row, "validated addition source")
        names = tuple(_nonblank(source_row.get(field), f"validated source {field}") for field in
                      ("attribute_name", "group_name", "object_name"))
        if identity in source_by_identity and source_by_identity[identity] != names:
            raise DeltaGuardError("Validated sources disagree on one addition identity.")
        source_by_identity[identity] = names
    if len(removals) != len(requested_removals):
        raise DeltaGuardError("DELETE rows do not match the requested removals.")
    data_loader_required = delta.get("data_loader_required")
    if not isinstance(data_loader_required, bool):
        raise DeltaGuardError("data_loader_required must be boolean.")
    if data_loader_required != bool(additions or removals):
        raise DeltaGuardError("data_loader_required must match the persisted change rows.")
    if require_data_loader and not data_loader_required:
        raise DeltaGuardError("No calculated Data Loader change set is available for preparation.")

    for row in additions:
        if row.get("rest_action") != "POST":
            raise DeltaGuardError("Every calculated addition must use RestAction POST.")
        for field in ("attribute_code", "group_code", "object_code"):
            _nonblank(row.get(field), f"addition {field}")
        if row.get("attribute_id") not in (None, ""):
            raise DeltaGuardError("A calculated addition must leave attribute_id blank.")
        _nonblank(row.get("attribute_name"), "addition attribute_name")
        _nonblank(row.get("group_name"), "addition group_name")
        _nonblank(row.get("object_name"), "addition object_name")
        names = tuple(row[field] for field in ("attribute_name", "group_name", "object_name"))
        if names != source_by_identity[_identity(row, "addition")]:
            raise DeltaGuardError("POST row names differ from the validated source.")
    for index, (source, row) in enumerate(zip(requested_removals, removals)):
        if row.get("rest_action") != "DELETE":
            raise DeltaGuardError("Every calculated removal must use RestAction DELETE.")
        _nonblank(row.get("attribute_id"), "removal attribute_id")
        if row.get("request_index") != index:
            raise DeltaGuardError("DELETE row order does not match the request.")
        for field in ("attribute_name", "group_name", "object_name"):
            if _nonblank(row.get(field), f"removal {field}").casefold() != _nonblank(
                _request_field(source, field), f"requested removal {field}"
            ).casefold():
                raise DeltaGuardError("DELETE row identity differs from the request.")
        supplied_id = _request_field(source, "attribute_id")
        if supplied_id is not None and str(supplied_id) != str(row["attribute_id"]):
            raise DeltaGuardError("DELETE AttributeId differs from the request.")
        matches = [
            existing_row for existing_row in existing
            if all(str(existing_row.get(field, "")).casefold() == str(row[field]).casefold()
                   for field in ("attribute_name", "group_name", "object_name"))
        ]
        if len(matches) != 1 or str(matches[0].get("attribute_id")) != str(row["attribute_id"]):
            raise DeltaGuardError("DELETE row does not match one existing backend record.")

    archive_digest = None
    if archive is not None:
        rows, archive_digest = _archive_rows(archive)
        expected = [
            ("POST", row["attribute_name"], row["group_name"], row["object_name"], "")
            for row in additions
        ] + [
            ("DELETE", row["attribute_name"], row["group_name"], row["object_name"], str(row["attribute_id"]))
            for row in removals
        ]
        actual = []
        for row in rows:
            if row.get("IndexName") != canonical:
                raise DeltaGuardError("The final DAT contains another index.")
            if row.get("RestAction") not in {"POST", "DELETE"}:
                raise DeltaGuardError("The final DAT has an unsupported RestAction.")
            actual.append(tuple(row.get(field, "") for field in
                                ("RestAction", "AttributeName", "GroupName", "ObjectName", "AttributeId")))
        if actual != expected:
            raise DeltaGuardError("The final DAT rows do not match the persisted delta.")

    return {
        "canonical_index_name": canonical,
        "addition_count": len(additions),
        "removal_count": len(removals),
        "data_loader_required": data_loader_required,
        "request_sha256": _request_digest(request),
        "archive_sha256": archive_digest,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--delta", required=True, type=Path)
    parser.add_argument("--archive", type=Path, help="Final immutable ZIP to bind to the calculated delta.")
    parser.add_argument(
        "--require-data-loader",
        action="store_true",
        help="Block unless the persisted delta has at least one Data Loader change row.",
    )
    args = parser.parse_args(argv)
    try:
        request = _read_object(args.request, "single-index request")
        delta = _read_object(args.delta, "index_attribute_delta")
        print(json.dumps(validate_delta(request, delta, require_data_loader=args.require_data_loader, archive=args.archive), sort_keys=True))
    except DeltaGuardError as error:
        print(f"Index delta guard blocked: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
