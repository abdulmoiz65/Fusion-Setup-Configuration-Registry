#!/usr/bin/env python3
"""Generate sanitized, release-bound Profile Content Library seed catalogs.

The source inputs are Oracle Fusion seed-data XML files from an explicitly
selected ADE label. The generated catalogs contain only provider keys and
business fields needed for deterministic evidence resolution. They never
contain database identifiers, who columns, customer data, or credentials.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "1.0"
SAFE_RELEASE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
SAFE_ADE_LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,255}$")
SEED_AUTHORS = {"0", "SEED_DATA_FROM_APPLICATION"}

CONTENT_TYPE_SOURCE_PATH = (
    "fusionapps/hcm/hrt/db/data/HcmProfileTop/"
    "HcmProfileContentLibrary/ContentTypeSD.xml"
)
CONTENT_TYPE_RELATIONSHIP_SOURCE_PATH = (
    "fusionapps/hcm/hrt/db/data/HcmProfileTop/"
    "HcmProfileContentLibrary/ContentTypeRelationshipSD.xml"
)
CONTENT_ITEM_SOURCE_PATH = (
    "fusionapps/hcm/hrt/db/data/HcmProfileTop/"
    "HcmProfileContentLibrary/ContentItemSD.xml"
)

CONTENT_TYPE_HEADER = (
    "ContextName",
    "ContentTypeName",
    "ContentDescription",
    "FreeFormFlag",
)
CONTENT_TYPE_PROPERTY_HEADER = (
    "ContextName",
    "FieldName",
    "AttributeLabel",
    "ColumnName",
    "DefaultValue",
    "RequiredFlag",
    "DisplayCode",
    "ViewAttrbName",
)
CONTENT_TYPE_RELATIONSHIP_HEADER = (
    "ContentTypeContextName",
    "RelatedContentTypeContextName",
    "RelationshipCode",
    "DateFrom",
    "DateTo",
    "RatingInteractionType",
)
CONTENT_ITEM_HEADER = (
    "ContextName",
    "ContentItemCode",
    "Name",
    "ContentSupplierCode",
    "DateFrom",
    "DateTo",
)


class CatalogGenerationError(ValueError):
    """Raised when the source XML cannot prove one complete seed catalog."""


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _children(element: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in list(element) if _local_name(child.tag) == name]


def _text(element: ET.Element, name: str) -> str:
    matches = _children(element, name)
    if len(matches) != 1:
        raise CatalogGenerationError(
            f"{_local_name(element.tag)} must contain exactly one {name} element"
        )
    child = matches[0]
    if child.attrib.get("isNull", "").lower() == "true":
        return ""
    return (child.text or "").strip()


def _parse_xml(path: Path, expected_vo: str) -> tuple[ET.Element, bytes]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise CatalogGenerationError(f"source XML is unreadable: {path}") from exc
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise CatalogGenerationError(f"source XML contains a prohibited DTD or entity: {path}")
    try:
        root = ET.fromstring(raw.decode("utf-8-sig"))
    except (UnicodeError, ET.ParseError) as exc:
        raise CatalogGenerationError(f"source XML is not well-formed UTF-8: {path}") from exc
    if _local_name(root.tag) != "SEEDDATA" or root.attrib.get("vo") != expected_vo:
        raise CatalogGenerationError(f"source XML has an unexpected seed-data identity: {path}")
    return root, raw


def _validate_seed_authors(element: ET.Element) -> None:
    for field in ("CreatedBy", "LastUpdatedBy"):
        value = _text(element, field)
        if value not in SEED_AUTHORS:
            raise CatalogGenerationError(
                f"{_local_name(element.tag)} has non-seed {field}: {value!r}"
            )


def _validate_unique(
    rows: Sequence[Mapping[str, str]], fields: Sequence[str], label: str
) -> None:
    keys = [tuple(row[field] for field in fields) for row in rows]
    if len(keys) != len(set(keys)):
        raise CatalogGenerationError(f"{label} contains duplicate provider keys")


def _validate_date(value: str, label: str) -> None:
    if not value:
        return
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise CatalogGenerationError(f"{label} must use YYYY-MM-DD") from exc


def extract_catalogs(
    content_type_source: Path,
    relationship_source: Path,
    content_item_source: Path,
) -> tuple[
    dict[str, list[dict[str, str]]],
    dict[str, list[dict[str, str]]],
    dict[str, str],
]:
    type_root, type_raw = _parse_xml(content_type_source, "ContentType")
    relationship_root, relationship_raw = _parse_xml(
        relationship_source, "ContentTypeRelationship"
    )
    item_root, item_raw = _parse_xml(content_item_source, "ContentItem")

    content_types: list[dict[str, str]] = []
    properties: list[dict[str, str]] = []
    type_id_to_context: dict[str, str] = {}
    for element in _children(type_root, "ContentType"):
        _validate_seed_authors(element)
        content_type_id = _text(element, "ContentTypeId")
        context_name = _text(element, "ContextName")
        if not content_type_id or not context_name:
            raise CatalogGenerationError("ContentType requires ContentTypeId and ContextName")
        if content_type_id in type_id_to_context:
            raise CatalogGenerationError("ContentType source contains a duplicate ContentTypeId")
        type_id_to_context[content_type_id] = context_name
        content_types.append(
            {
                "ContextName": context_name,
                "ContentTypeName": _text(element, "ContentTypeName"),
                "ContentDescription": _text(element, "ContentDescription"),
                "FreeFormFlag": _text(element, "FreeFormFlag"),
            }
        )
        for prop in _children(element, "ContentTypeProperty"):
            _validate_seed_authors(prop)
            properties.append(
                {
                    "ContextName": context_name,
                    "FieldName": _text(prop, "FieldName"),
                    "AttributeLabel": _text(prop, "AttributeLabel"),
                    "ColumnName": _text(prop, "ColumnName"),
                    "DefaultValue": _text(prop, "DefaultValue"),
                    "RequiredFlag": _text(prop, "RequiredFlag"),
                    "DisplayCode": _text(prop, "DisplayCode"),
                    "ViewAttrbName": _text(prop, "ViewAttrbName"),
                }
            )

    relationships: list[dict[str, str]] = []
    for element in _children(relationship_root, "ContentTypeRelationship"):
        _validate_seed_authors(element)
        source_id = _text(element, "ContentTypeId")
        related_id = _text(element, "RelatedContentTypeId")
        if source_id not in type_id_to_context or related_id not in type_id_to_context:
            raise CatalogGenerationError(
                "ContentTypeRelationship references a ContentTypeId absent from ContentTypeSD.xml"
            )
        row = {
            "ContentTypeContextName": type_id_to_context[source_id],
            "RelatedContentTypeContextName": type_id_to_context[related_id],
            "RelationshipCode": _text(element, "RelationshipCode"),
            "DateFrom": _text(element, "DateFrom"),
            "DateTo": _text(element, "DateTo"),
            "RatingInteractionType": _text(element, "RatingInteractionType"),
        }
        _validate_date(row["DateFrom"], "ContentTypeRelationship.DateFrom")
        _validate_date(row["DateTo"], "ContentTypeRelationship.DateTo")
        relationships.append(row)

    content_items: list[dict[str, str]] = []
    for element in _children(item_root, "ContentItem"):
        _validate_seed_authors(element)
        content_type_id = _text(element, "ContentTypeId")
        if content_type_id not in type_id_to_context:
            raise CatalogGenerationError(
                "ContentItem references a ContentTypeId absent from ContentTypeSD.xml"
            )
        row = {
            "ContextName": type_id_to_context[content_type_id],
            "ContentItemCode": _text(element, "ContentItemCode"),
            "Name": _text(element, "Name"),
            "ContentSupplierCode": _text(element, "ContentSupplierCode"),
            "DateFrom": _text(element, "DateFrom"),
            "DateTo": _text(element, "DateTo"),
        }
        if not row["ContentItemCode"] or not row["Name"]:
            raise CatalogGenerationError("ContentItem requires ContentItemCode and Name")
        _validate_date(row["DateFrom"], "ContentItem.DateFrom")
        _validate_date(row["DateTo"], "ContentItem.DateTo")
        content_items.append(row)

    declared_type_rows = int(type_root.attrib.get("rowcount", "-1"))
    declared_relationship_rows = int(relationship_root.attrib.get("rowcount", "-1"))
    declared_item_rows = int(item_root.attrib.get("rowcount", "-1"))
    if declared_type_rows != len(content_types) + len(properties):
        raise CatalogGenerationError(
            "ContentTypeSD.xml rowcount does not equal Content Types plus nested properties"
        )
    if declared_relationship_rows != len(relationships):
        raise CatalogGenerationError("ContentTypeRelationshipSD.xml rowcount is inconsistent")
    if declared_item_rows != len(content_items):
        raise CatalogGenerationError("ContentItemSD.xml rowcount is inconsistent")

    _validate_unique(content_types, ("ContextName",), "Content Types")
    _validate_unique(properties, ("ContextName", "FieldName"), "Content Type properties")
    _validate_unique(
        relationships,
        (
            "ContentTypeContextName",
            "RelatedContentTypeContextName",
            "RelationshipCode",
            "DateFrom",
        ),
        "Content Type relationships",
    )
    _validate_unique(
        content_items,
        ("ContextName", "ContentItemCode"),
        "Content Items",
    )

    content_types.sort(key=lambda row: row["ContextName"])
    properties.sort(key=lambda row: (row["ContextName"], row["FieldName"]))
    relationships.sort(
        key=lambda row: (
            row["ContentTypeContextName"],
            row["RelatedContentTypeContextName"],
            row["RelationshipCode"],
            row["DateFrom"],
        )
    )
    content_items.sort(key=lambda row: (row["ContextName"], row["ContentItemCode"]))
    source_hashes = {
        CONTENT_TYPE_SOURCE_PATH: _sha256_bytes(type_raw),
        CONTENT_TYPE_RELATIONSHIP_SOURCE_PATH: _sha256_bytes(relationship_raw),
        CONTENT_ITEM_SOURCE_PATH: _sha256_bytes(item_raw),
    }
    return (
        {
            "content-types.csv": content_types,
            "content-type-properties.csv": properties,
            "content-type-relationships.csv": relationships,
        },
        {"content-items.csv": content_items},
        source_hashes,
    )


def _csv_bytes(rows: Sequence[Mapping[str, str]], header: Sequence[str]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer,
        fieldnames=list(header),
        extrasaction="raise",
        lineterminator="\n",
        quoting=csv.QUOTE_ALL,
    )
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def _manifest_bytes(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build_output_files(
    *,
    type_rows: Mapping[str, Sequence[Mapping[str, str]]],
    item_rows: Mapping[str, Sequence[Mapping[str, str]]],
    source_hashes: Mapping[str, str],
    fusion_release: str,
    ade_label: str,
    generated_on: str,
) -> dict[str, dict[str, bytes]]:
    headers = {
        "content-types.csv": CONTENT_TYPE_HEADER,
        "content-type-properties.csv": CONTENT_TYPE_PROPERTY_HEADER,
        "content-type-relationships.csv": CONTENT_TYPE_RELATIONSHIP_HEADER,
        "content-items.csv": CONTENT_ITEM_HEADER,
    }
    type_files = {
        name: _csv_bytes(rows, headers[name]) for name, rows in type_rows.items()
    }
    item_files = {
        name: _csv_bytes(rows, headers[name]) for name, rows in item_rows.items()
    }

    common = {
        "schema_version": SCHEMA_VERSION,
        "fusion_release": fusion_release,
        "ade_label": ade_label,
        "generated_on": generated_on,
        "sanitization": (
            "Retains only provider keys and business fields required for seeded evidence "
            "resolution; excludes database identifiers, who columns, customer data, and credentials."
        ),
    }
    type_manifest = dict(common)
    type_manifest.update(
        {
            "catalog_kind": "oracle-seeded-profile-content-types",
            "source_files": [
                {"path": path, "sha256": source_hashes[path]}
                for path in (
                    CONTENT_TYPE_RELATIONSHIP_SOURCE_PATH,
                    CONTENT_TYPE_SOURCE_PATH,
                )
            ],
            "files": {
                name: {
                    "sha256": _sha256_bytes(raw),
                    "row_count": len(type_rows[name]),
                    "columns": list(headers[name]),
                }
                for name, raw in sorted(type_files.items())
            },
            "key_fields": {
                "content-types.csv": ["ContextName"],
                "content-type-properties.csv": ["ContextName", "FieldName"],
                "content-type-relationships.csv": [
                    "ContentTypeContextName",
                    "RelatedContentTypeContextName",
                    "RelationshipCode",
                    "DateFrom",
                ],
            },
        }
    )
    item_manifest = dict(common)
    item_manifest.update(
        {
            "catalog_kind": "oracle-seeded-profile-content-items",
            "source_files": [
                {"path": path, "sha256": source_hashes[path]}
                for path in (CONTENT_ITEM_SOURCE_PATH, CONTENT_TYPE_SOURCE_PATH)
            ],
            "files": {
                name: {
                    "sha256": _sha256_bytes(raw),
                    "row_count": len(item_rows[name]),
                    "columns": list(headers[name]),
                }
                for name, raw in sorted(item_files.items())
            },
            "key_fields": {
                "content-items.csv": ["ContextName", "ContentItemCode"]
            },
            "usage_boundary": (
                "This identity catalog may prove seeded key presence or absence. It is not "
                "a provider-row template and must never be imported."
            ),
        }
    )
    type_files["manifest.json"] = _manifest_bytes(type_manifest)
    item_files["manifest.json"] = _manifest_bytes(item_manifest)
    return {
        "seeded-content-types": type_files,
        "seeded-content-items": item_files,
    }


def _write_outputs(output_root: Path, outputs: Mapping[str, Mapping[str, bytes]]) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".seeded-content-catalog-", dir=str(output_root)
    ) as temporary:
        stage_root = Path(temporary)
        for directory, files in outputs.items():
            stage = stage_root / directory
            stage.mkdir()
            for name, raw in files.items():
                (stage / name).write_bytes(raw)
        for directory, files in outputs.items():
            destination = output_root / directory
            destination.mkdir(parents=True, exist_ok=True)
            for name in files:
                os.replace(str(stage_root / directory / name), str(destination / name))


def _summary(outputs: Mapping[str, Mapping[str, bytes]]) -> dict[str, Any]:
    result: dict[str, Any] = {"schema_version": SCHEMA_VERSION, "catalogs": {}}
    for directory, files in sorted(outputs.items()):
        manifest = json.loads(files["manifest.json"].decode("utf-8"))
        result["catalogs"][directory] = {
            "catalog_kind": manifest["catalog_kind"],
            "fusion_release": manifest["fusion_release"],
            "files": {
                name: {
                    "sha256": details["sha256"],
                    "row_count": details["row_count"],
                }
                for name, details in sorted(manifest["files"].items())
            },
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate sanitized seeded Profile Content Library catalogs from ADE XML."
    )
    parser.add_argument("--content-type-source", required=True, type=Path)
    parser.add_argument("--relationship-source", required=True, type=Path)
    parser.add_argument("--content-item-source", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--fusion-release", required=True)
    parser.add_argument("--ade-label", required=True)
    parser.add_argument("--generated-on", required=True)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and summarize the catalogs without writing files.",
    )
    args = parser.parse_args()

    try:
        if not SAFE_RELEASE.fullmatch(args.fusion_release):
            raise CatalogGenerationError("fusion release must be a safe nonblank label")
        if not SAFE_ADE_LABEL.fullmatch(args.ade_label):
            raise CatalogGenerationError("ADE label must contain only safe label characters")
        date.fromisoformat(args.generated_on)
        type_rows, item_rows, source_hashes = extract_catalogs(
            args.content_type_source,
            args.relationship_source,
            args.content_item_source,
        )
        outputs = build_output_files(
            type_rows=type_rows,
            item_rows=item_rows,
            source_hashes=source_hashes,
            fusion_release=args.fusion_release,
            ade_label=args.ade_label,
            generated_on=args.generated_on,
        )
        if not args.dry_run:
            _write_outputs(args.output_root.resolve(), outputs)
        payload = _summary(outputs)
        payload["status"] = "validated" if args.dry_run else "written"
        payload["output_root"] = str(args.output_root)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    except (CatalogGenerationError, OSError, ValueError) as exc:
        print(
            json.dumps(
                {"schema_version": SCHEMA_VERSION, "status": "blocked", "error": str(exc)},
                indent=2,
                sort_keys=True,
            )
        )
        return 2


if __name__ == "__main__":
    sys.exit(main())
