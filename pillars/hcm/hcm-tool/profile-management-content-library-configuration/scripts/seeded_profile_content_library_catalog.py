#!/usr/bin/env python3
"""Validate and load skill-local Oracle-seeded Profile Content catalogs."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any, Mapping


SCHEMA_VERSION = "1.0"
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
SAFE_ADE_LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,255}$")
MAX_CATALOG_FILE_BYTES = 16 * 1024 * 1024

CONTENT_TYPE_HEADERS: Mapping[str, tuple[str, ...]] = {
    "content-types.csv": (
        "ContextName",
        "ContentTypeName",
        "ContentDescription",
        "FreeFormFlag",
    ),
    "content-type-properties.csv": (
        "ContextName",
        "FieldName",
        "AttributeLabel",
        "ColumnName",
        "DefaultValue",
        "RequiredFlag",
        "DisplayCode",
        "ViewAttrbName",
    ),
    "content-type-relationships.csv": (
        "ContentTypeContextName",
        "RelatedContentTypeContextName",
        "RelationshipCode",
        "DateFrom",
        "DateTo",
        "RatingInteractionType",
    ),
}
CONTENT_ITEM_HEADERS: Mapping[str, tuple[str, ...]] = {
    "content-items.csv": (
        "ContextName",
        "ContentItemCode",
        "Name",
        "ContentSupplierCode",
        "DateFrom",
        "DateTo",
    )
}
CONTENT_TYPE_KEYS: Mapping[str, tuple[str, ...]] = {
    "content-types.csv": ("ContextName",),
    "content-type-properties.csv": ("ContextName", "FieldName"),
    "content-type-relationships.csv": (
        "ContentTypeContextName",
        "RelatedContentTypeContextName",
        "RelationshipCode",
        "DateFrom",
    ),
}
CONTENT_ITEM_KEYS: Mapping[str, tuple[str, ...]] = {
    "content-items.csv": ("ContextName", "ContentItemCode")
}


class SeededCatalogError(ValueError):
    """Raised when a seeded catalog is missing, stale, or malformed."""


@dataclass(frozen=True)
class SeededCatalog:
    catalog_kind: str
    fusion_release: str
    ade_label: str
    generated_on: str
    manifest_sha256: str
    source_files: tuple[Mapping[str, str], ...]
    records_by_file: Mapping[str, tuple[Mapping[str, str], ...]]
    file_sha256: Mapping[str, str]

    def sanitized_summary(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "catalog_kind": self.catalog_kind,
            "fusion_release": self.fusion_release,
            "ade_label": self.ade_label,
            "generated_on": self.generated_on,
            "manifest_sha256": self.manifest_sha256,
            "row_counts": {
                name: len(rows) for name, rows in sorted(self.records_by_file.items())
            },
            "file_sha256": dict(sorted(self.file_sha256.items())),
        }


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require_exact_keys(value: Any, expected: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise SeededCatalogError(f"{label} must be a JSON object")
    actual = set(value)
    if actual != expected:
        raise SeededCatalogError(
            f"{label} keys are invalid; missing={sorted(expected - actual)}, "
            f"unexpected={sorted(actual - expected)}"
        )
    return value


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise SeededCatalogError(f"{label} must be a nonblank trimmed string")
    if any(character in value for character in ("\x00", "\r", "\n")):
        raise SeededCatalogError(f"{label} contains a prohibited control character")
    return value


def _validate_sha256(value: Any, label: str) -> str:
    text = _require_text(value, label)
    if not SHA256_PATTERN.fullmatch(text):
        raise SeededCatalogError(f"{label} must be a lowercase SHA-256 value")
    return text


def _read_csv(raw: bytes, header: tuple[str, ...], name: str) -> tuple[Mapping[str, str], ...]:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeError as exc:
        raise SeededCatalogError(f"{name} is not valid UTF-8") from exc
    if "\x00" in text:
        raise SeededCatalogError(f"{name} contains a NUL character")
    try:
        reader = csv.DictReader(io.StringIO(text, newline=""))
        if tuple(reader.fieldnames or ()) != header:
            raise SeededCatalogError(f"{name} header does not match its catalog contract")
        rows = tuple(dict(row) for row in reader)
    except csv.Error as exc:
        raise SeededCatalogError(f"{name} is malformed CSV") from exc
    if any(None in row or None in row.values() for row in rows):
        raise SeededCatalogError(f"{name} contains a malformed row")
    return rows


def _validate_source_files(value: Any) -> tuple[Mapping[str, str], ...]:
    if not isinstance(value, list) or not value:
        raise SeededCatalogError("manifest.source_files must be a nonempty array")
    result: list[Mapping[str, str]] = []
    paths: set[str] = set()
    for index, item in enumerate(value, start=1):
        source = _require_exact_keys(item, {"path", "sha256"}, f"source_files[{index}]")
        path_text = _require_text(source["path"], f"source_files[{index}].path")
        path = PurePosixPath(path_text)
        if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
            raise SeededCatalogError(f"source_files[{index}].path must be repository-relative")
        if path_text in paths:
            raise SeededCatalogError("manifest.source_files contains a duplicate path")
        paths.add(path_text)
        result.append(
            {
                "path": path_text,
                "sha256": _validate_sha256(
                    source["sha256"], f"source_files[{index}].sha256"
                ),
            }
        )
    return tuple(result)


def load_seeded_catalog(
    catalog_dir: Path,
    *,
    expected_kind: str,
    expected_release: str = "unknown",
) -> SeededCatalog:
    """Load one catalog only after its manifest, hashes, shape, and keys pass."""

    # Kept for caller compatibility only. Target release is not a catalog gate.
    root = catalog_dir.resolve()
    if not root.is_dir() or root.is_symlink():
        raise SeededCatalogError("seeded catalog directory is missing or unsafe")
    manifest_path = root / "manifest.json"
    try:
        manifest_raw = manifest_path.read_bytes()
        manifest = json.loads(manifest_raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SeededCatalogError("seeded catalog manifest is unreadable or malformed") from exc

    is_type = expected_kind == "oracle-seeded-profile-content-types"
    is_item = expected_kind == "oracle-seeded-profile-content-items"
    if not is_type and not is_item:
        raise SeededCatalogError("unsupported seeded catalog kind")
    expected_top = {
        "schema_version",
        "catalog_kind",
        "fusion_release",
        "ade_label",
        "generated_on",
        "source_files",
        "sanitization",
        "files",
        "key_fields",
    }
    if is_item:
        expected_top.add("usage_boundary")
    manifest = _require_exact_keys(manifest, expected_top, "manifest")
    if manifest["schema_version"] != SCHEMA_VERSION:
        raise SeededCatalogError("seeded catalog schema version is unsupported")
    if manifest["catalog_kind"] != expected_kind:
        raise SeededCatalogError("seeded catalog kind does not match the requested resolver")
    source_release = _require_text(manifest["fusion_release"], "manifest.fusion_release")
    ade_label = _require_text(manifest["ade_label"], "manifest.ade_label")
    if not SAFE_ADE_LABEL.fullmatch(ade_label):
        raise SeededCatalogError("manifest.ade_label contains unsafe characters")
    generated_on = _require_text(manifest["generated_on"], "manifest.generated_on")
    try:
        date.fromisoformat(generated_on)
    except ValueError as exc:
        raise SeededCatalogError("manifest.generated_on must use YYYY-MM-DD") from exc
    _require_text(manifest["sanitization"], "manifest.sanitization")
    if is_item:
        _require_text(manifest["usage_boundary"], "manifest.usage_boundary")
    source_files = _validate_source_files(manifest["source_files"])

    headers = CONTENT_TYPE_HEADERS if is_type else CONTENT_ITEM_HEADERS
    keys = CONTENT_TYPE_KEYS if is_type else CONTENT_ITEM_KEYS
    files = _require_exact_keys(manifest["files"], set(headers), "manifest.files")
    key_fields = _require_exact_keys(
        manifest["key_fields"], set(headers), "manifest.key_fields"
    )
    records_by_file: dict[str, tuple[Mapping[str, str], ...]] = {}
    file_sha256: dict[str, str] = {}
    for name, header in headers.items():
        details = _require_exact_keys(
            files[name], {"sha256", "row_count", "columns"}, f"manifest.files.{name}"
        )
        if details["columns"] != list(header):
            raise SeededCatalogError(f"manifest.files.{name}.columns are invalid")
        if not isinstance(details["row_count"], int) or details["row_count"] < 0:
            raise SeededCatalogError(f"manifest.files.{name}.row_count is invalid")
        if key_fields[name] != list(keys[name]):
            raise SeededCatalogError(f"manifest.key_fields.{name} is invalid")
        path = root / name
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise SeededCatalogError(f"seeded catalog file is unreadable: {name}") from exc
        if len(raw) > MAX_CATALOG_FILE_BYTES:
            raise SeededCatalogError(f"seeded catalog file exceeds the size limit: {name}")
        actual_sha = _sha256_bytes(raw)
        expected_sha = _validate_sha256(
            details["sha256"], f"manifest.files.{name}.sha256"
        )
        if actual_sha != expected_sha:
            raise SeededCatalogError(f"seeded catalog file hash does not match: {name}")
        rows = _read_csv(raw, header, name)
        if len(rows) != details["row_count"]:
            raise SeededCatalogError(f"seeded catalog row count does not match: {name}")
        provider_keys = [tuple(row[field] for field in keys[name]) for row in rows]
        if any(not all(key) for key in provider_keys):
            raise SeededCatalogError(f"seeded catalog contains a blank provider key: {name}")
        if len(provider_keys) != len(set(provider_keys)):
            raise SeededCatalogError(f"seeded catalog contains duplicate provider keys: {name}")
        records_by_file[name] = rows
        file_sha256[name] = actual_sha

    return SeededCatalog(
        catalog_kind=expected_kind,
        fusion_release=source_release,
        ade_label=ade_label,
        generated_on=generated_on,
        manifest_sha256=_sha256_bytes(manifest_raw),
        source_files=source_files,
        records_by_file=records_by_file,
        file_sha256=file_sha256,
    )


def load_seeded_content_types(catalog_dir: Path, *, expected_release: str = "unknown") -> SeededCatalog:
    return load_seeded_catalog(
        catalog_dir,
        expected_kind="oracle-seeded-profile-content-types",
        expected_release=expected_release,
    )


def load_seeded_content_items(catalog_dir: Path, *, expected_release: str = "unknown") -> SeededCatalog:
    return load_seeded_catalog(
        catalog_dir,
        expected_kind="oracle-seeded-profile-content-items",
        expected_release=expected_release,
    )
