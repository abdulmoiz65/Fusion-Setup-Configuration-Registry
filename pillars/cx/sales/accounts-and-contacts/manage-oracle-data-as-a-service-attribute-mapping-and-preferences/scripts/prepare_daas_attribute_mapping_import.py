#!/usr/bin/env python3
"""Build a selected-row FSM import package for DaaS attribute mappings."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import sys
import zipfile
import xml.etree.ElementTree as ET


TASK_CODE = "ORA_ZCM_DAAS_ATTRIBUTE_MAPPING_PREFERENCES"
CSV_MEMBERS = (
    "ORA_ZCM_DATA_CLOUD_ENRICH_PREFERENCE.csv",
    "ORA_ZCM_DATA_CLOUD_MAPPING_PREFERENCE.csv",
)
METADATA_MEMBER = "ASM_SETUP_CSV_METADATA.xml"
KEY_FIELDS = ("AttributeCategory", "DaasAttributeName")
EDITABLE_FIELDS = {
    "AutofillBlank",
    "AutoupdateNonBlank",
    "FusionAttributeName",
    "FusionObjectName",
}
BOOLEAN_FIELDS = {"AutofillBlank", "AutoupdateNonBlank"}
MAPPING_FIELDS = {"FusionAttributeName", "FusionObjectName"}
DEFAULT_BASELINE = Path(__file__).resolve().parents[1] / "assets" / "seeded-attribute-mappings.csv"


class PackageError(ValueError):
    """Raised when the selected-row package cannot be built safely."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare a task-level FSM ZIP containing only explicitly selected "
            "DaaS attribute-mapping rows."
        )
    )
    parser.add_argument("--export-zip", type=Path, required=True, help="Fresh task-level FSM export ZIP.")
    parser.add_argument("--changes", type=Path, required=True, help="JSON file containing a nonempty changes array.")
    parser.add_argument("--output-zip", type=Path, required=True, help="Destination for the prepared import ZIP.")
    parser.add_argument("--preview", type=Path, help="Preview JSON path; defaults beside the output ZIP.")
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE, help="Sanitized complete seeded-row catalog.")
    parser.add_argument(
        "--fusion-attributes",
        action="append",
        default=[],
        metavar="OBJECT=JSON",
        help=(
            "Fresh target-pod objectMetadata attributes response for one FusionObjectName. "
            "Repeat for every effective object in a requested mapping change."
        ),
    )
    parser.add_argument(
        "--target-environment",
        help="Sanitized target-environment identifier recorded with live attribute validation.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and preview without writing the output ZIP.")
    return parser.parse_args(argv)


def _safe_member_name(name: str) -> None:
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or not path.name:
        raise PackageError(f"unsafe ZIP member path: {name!r}")


def _read_csv_bytes(data: bytes, label: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise PackageError(f"{label} is not UTF-8 CSV") from exc
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if not reader.fieldnames:
        raise PackageError(f"{label} has no CSV header")
    if len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise PackageError(f"{label} has duplicate CSV headers")
    rows = [dict(row) for row in reader]
    return list(reader.fieldnames), rows


def _row_key(row: dict[str, str], label: str) -> tuple[str, str]:
    values = tuple((row.get(field) or "").strip() for field in KEY_FIELDS)
    if not all(values):
        raise PackageError(f"{label} has a row with a blank key field")
    return values[0], values[1]


def _index_rows(rows: list[dict[str, str]], label: str) -> dict[tuple[str, str], dict[str, str]]:
    indexed: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = _row_key(row, label)
        if key in indexed:
            raise PackageError(f"{label} contains duplicate row key {key!r}")
        indexed[key] = row
    return indexed


def load_baseline(path: Path) -> tuple[list[str], dict[tuple[str, str], dict[str, str]]]:
    if not path.is_file():
        raise PackageError(f"baseline CSV does not exist: {path}")
    manifest_path = path.with_suffix(".json")
    if not manifest_path.is_file():
        raise PackageError(f"baseline manifest does not exist: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PackageError(f"baseline manifest is not valid UTF-8 JSON: {manifest_path}") from exc
    if not isinstance(manifest, dict):
        raise PackageError("baseline manifest must be a JSON object")

    baseline_bytes = path.read_bytes()
    actual_sha256 = hashlib.sha256(baseline_bytes).hexdigest()
    if manifest.get("task_code") != TASK_CODE:
        raise PackageError("baseline manifest task code does not match this skill")
    if manifest.get("csv_sha256") != actual_sha256:
        raise PackageError("baseline CSV SHA-256 does not match its manifest")
    if manifest.get("required_output_members") != list(CSV_MEMBERS):
        raise PackageError("baseline manifest output members do not match this skill")

    headers, rows = _read_csv_bytes(baseline_bytes, str(path))
    missing = [field for field in KEY_FIELDS if field not in headers]
    if missing:
        raise PackageError(f"baseline CSV is missing key fields: {', '.join(missing)}")
    if manifest.get("row_count") != len(rows) or manifest.get("column_count") != len(headers):
        raise PackageError("baseline CSV row or column count does not match its manifest")
    if manifest.get("key_fields") != list(KEY_FIELDS):
        raise PackageError("baseline manifest key fields do not match this skill")
    return headers, _index_rows(rows, "baseline CSV")


def load_changes(path: Path) -> list[dict[str, object]]:
    if not path.is_file():
        raise PackageError(f"changes JSON does not exist: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PackageError(f"changes file is not valid UTF-8 JSON: {path}") from exc
    changes = payload.get("changes") if isinstance(payload, dict) else None
    if not isinstance(changes, list) or not changes:
        raise PackageError("changes JSON must contain a nonempty 'changes' array")

    seen: set[tuple[str, str]] = set()
    normalized: list[dict[str, object]] = []
    for position, item in enumerate(changes, start=1):
        if not isinstance(item, dict):
            raise PackageError(f"change {position} must be an object")
        key = tuple(str(item.get(field, "")).strip() for field in KEY_FIELDS)
        if not all(key):
            raise PackageError(f"change {position} must provide {', '.join(KEY_FIELDS)}")
        if key in seen:
            raise PackageError(f"changes JSON repeats row key {key!r}")
        seen.add(key)
        updates = item.get("set")
        if not isinstance(updates, dict) or not updates:
            raise PackageError(f"change {position} must contain a nonempty 'set' object")
        unknown = sorted(set(updates) - EDITABLE_FIELDS)
        if unknown:
            raise PackageError(f"change {position} attempts non-editable fields: {', '.join(unknown)}")
        clean_updates: dict[str, str] = {}
        for field, value in updates.items():
            if value is None or isinstance(value, (dict, list)):
                raise PackageError(f"change {position} field {field} must be a scalar string value")
            clean_value = str(value).strip()
            if field in BOOLEAN_FIELDS and clean_value not in {"Y", "N"}:
                raise PackageError(f"change {position} field {field} must be Y or N")
            clean_updates[field] = clean_value
        normalized.append(
            {
                "key": {KEY_FIELDS[0]: key[0], KEY_FIELDS[1]: key[1]},
                "key_tuple": key,
                "set": clean_updates,
            }
        )
    return normalized


def parse_attribute_metadata_args(values: list[str]) -> dict[str, Path]:
    metadata: dict[str, Path] = {}
    for value in values:
        object_name, separator, path_value = value.partition("=")
        object_name = object_name.strip()
        path_value = path_value.strip()
        if not separator or not object_name or not path_value:
            raise PackageError("--fusion-attributes must use OBJECT=JSON syntax")
        if object_name in metadata:
            raise PackageError(f"duplicate Fusion attribute metadata for object {object_name!r}")
        metadata[object_name] = Path(path_value)
    return metadata


def load_attribute_metadata(
    paths: dict[str, Path],
) -> tuple[dict[str, set[str]], dict[str, dict[str, object]]]:
    catalogs: dict[str, set[str]] = {}
    evidence: dict[str, dict[str, object]] = {}
    for object_name, path in paths.items():
        if not path.is_file():
            raise PackageError(f"Fusion attribute metadata does not exist for {object_name!r}: {path}")
        try:
            raw_bytes = path.read_bytes()
            payload = json.loads(raw_bytes.decode("utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PackageError(
                f"Fusion attribute metadata for {object_name!r} must be readable UTF-8 JSON"
            ) from exc
        if not isinstance(payload, dict):
            raise PackageError(f"Fusion attribute metadata for {object_name!r} must be a JSON object")
        items = payload.get("items")
        count = payload.get("count")
        total_results = payload.get("totalResults")
        has_more = payload.get("hasMore")
        if not isinstance(items, list):
            raise PackageError(f"Fusion attribute metadata for {object_name!r} has no items array")
        if isinstance(count, bool) or not isinstance(count, int):
            raise PackageError(f"Fusion attribute metadata for {object_name!r} has no integer count")
        if isinstance(total_results, bool) or not isinstance(total_results, int):
            raise PackageError(
                f"Fusion attribute metadata for {object_name!r} has no integer totalResults"
            )
        if has_more is not False or count != total_results or count != len(items):
            raise PackageError(
                f"Fusion attribute metadata for {object_name!r} is incomplete: "
                f"count={count!r}, totalResults={total_results!r}, "
                f"hasMore={has_more!r}, items={len(items)}"
            )
        attribute_codes: set[str] = set()
        for position, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                raise PackageError(
                    f"Fusion attribute metadata for {object_name!r} item {position} must be an object"
                )
            attribute_code = item.get("AttributeCode")
            if not isinstance(attribute_code, str) or not attribute_code.strip():
                raise PackageError(
                    f"Fusion attribute metadata for {object_name!r} item {position} "
                    "has no nonblank AttributeCode"
                )
            attribute_code = attribute_code.strip()
            if attribute_code in attribute_codes:
                raise PackageError(
                    f"Fusion attribute metadata for {object_name!r} repeats "
                    f"AttributeCode {attribute_code!r}"
                )
            attribute_codes.add(attribute_code)
        catalogs[object_name] = attribute_codes
        evidence[object_name] = {
            "attribute_count": len(attribute_codes),
            "metadata_sha256": hashlib.sha256(raw_bytes).hexdigest(),
            "source_file": str(path.resolve()),
        }
    return catalogs, evidence


def validate_fusion_mapping(
    row: dict[str, str],
    key: tuple[str, str],
    member: str,
    attribute_catalogs: dict[str, set[str]],
) -> dict[str, object]:
    object_name = (row.get("FusionObjectName") or "").strip()
    attribute_name = (row.get("FusionAttributeName") or "").strip()
    if attribute_name and not object_name:
        raise PackageError(
            f"requested row {key!r} in {member} has FusionAttributeName "
            f"{attribute_name!r} without FusionObjectName"
        )
    if not object_name:
        return {
            "status": "validated_unmapped",
            "FusionObjectName": "",
            "FusionAttributeName": "",
        }
    attributes = attribute_catalogs.get(object_name)
    if attributes is None:
        raise PackageError(
            f"requested row {key!r} requires fresh Fusion attribute metadata "
            f"for FusionObjectName {object_name!r}"
        )
    if attribute_name and attribute_name not in attributes:
        raise PackageError(
            f"requested row {key!r} has invalid FusionAttributeName {attribute_name!r} "
            f"for FusionObjectName {object_name!r}"
        )
    return {
        "status": "validated" if attribute_name else "validated_no_attribute",
        "FusionObjectName": object_name,
        "FusionAttributeName": attribute_name,
    }


def _validate_metadata(data: bytes) -> None:
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise PackageError("FSM metadata XML is invalid") from exc
    object_names = [(node.text or "").strip() for node in root.iter("ObjectShortName")]
    if object_names != [TASK_CODE]:
        raise PackageError(f"metadata task binding must be exactly {TASK_CODE}; found {object_names!r}")
    business_objects = {
        (node.text or "").strip()
        for node in root.iter("BusinessObjectShortName")
        if (node.text or "").strip()
    }
    expected = {Path(member).stem for member in CSV_MEMBERS}
    if business_objects != expected:
        raise PackageError(
            "metadata business-object members do not match the required task package: "
            f"expected {sorted(expected)!r}, found {sorted(business_objects)!r}"
        )


def _write_csv(headers: list[str], rows: list[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=headers, extrasaction="raise", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def build_package(
    export_zip: Path,
    baseline_path: Path,
    changes_path: Path,
    attribute_metadata_paths: dict[str, Path] | None = None,
    target_environment: str | None = None,
) -> tuple[bytes, dict[str, object]]:
    if not export_zip.is_file():
        raise PackageError(f"export ZIP does not exist: {export_zip}")
    baseline_headers, baseline_rows = load_baseline(baseline_path)
    changes = load_changes(changes_path)
    mapping_change_requested = any(
        bool(set(change["set"]) & MAPPING_FIELDS)
        for change in changes
        if isinstance(change.get("set"), dict)
    )
    if mapping_change_requested and not (target_environment or "").strip():
        raise PackageError("mapping changes require --target-environment")
    attribute_catalogs, attribute_evidence = load_attribute_metadata(attribute_metadata_paths or {})

    try:
        source = zipfile.ZipFile(export_zip)
    except (OSError, zipfile.BadZipFile) as exc:
        raise PackageError(f"not a readable ZIP archive: {export_zip}") from exc

    with source:
        infos = source.infolist()
        names = [info.filename for info in infos]
        for name in names:
            _safe_member_name(name)
        if len(names) != len(set(names)):
            raise PackageError("export ZIP contains duplicate member names")
        required = {*CSV_MEMBERS, METADATA_MEMBER}
        missing = sorted(required - set(names))
        if missing:
            raise PackageError(f"export ZIP is missing required members: {', '.join(missing)}")
        unexpected = sorted(set(names) - required)
        if unexpected:
            raise PackageError(f"export ZIP contains unexpected members: {', '.join(unexpected)}")
        if [Path(name).name for name in names].count(METADATA_MEMBER) != 1:
            raise PackageError("export ZIP must contain exactly one FSM metadata member")
        _validate_metadata(source.read(METADATA_MEMBER))

        member_rows: dict[str, list[dict[str, str]]] = {}
        member_headers: dict[str, list[str]] = {}
        member_indexes: dict[str, dict[tuple[str, str], dict[str, str]]] = {}
        baseline_set = set(baseline_headers)
        for member in CSV_MEMBERS:
            headers, rows = _read_csv_bytes(source.read(member), member)
            if set(headers) != baseline_set:
                raise PackageError(f"{member} headers do not match the sanitized baseline schema")
            member_headers[member] = headers
            member_indexes[member] = _index_rows(rows, member)
            member_rows[member] = []

        preview_rows: list[dict[str, object]] = []
        for change in changes:
            key = change["key_tuple"]
            assert isinstance(key, tuple)
            if key not in baseline_rows:
                raise PackageError(f"requested row is not present in the complete seeded baseline: {key!r}")
            updates = change["set"]
            assert isinstance(updates, dict)
            per_member: dict[str, object] = {}
            for member in CSV_MEMBERS:
                live_row = member_indexes[member].get(key)
                source_row = live_row if live_row is not None else baseline_rows[key]
                final_row = dict(source_row)
                before = {field: final_row.get(field, "") for field in updates}
                for field, value in updates.items():
                    final_row[field] = value
                if _row_key(final_row, member) != key:
                    raise PackageError(f"requested change altered the immutable row key {key!r}")
                mapping_validation = None
                if set(updates) & MAPPING_FIELDS:
                    mapping_validation = validate_fusion_mapping(
                        final_row,
                        key,
                        member,
                        attribute_catalogs,
                    )
                member_rows[member].append({header: final_row.get(header, "") for header in member_headers[member]})
                per_member[member] = {
                    "row_source": "fresh_export" if live_row is not None else "seeded_baseline",
                    "before": before,
                    "after": {field: final_row.get(field, "") for field in updates},
                }
                if mapping_validation is not None:
                    per_member[member]["fusion_mapping_validation"] = mapping_validation
            preview_rows.append({"key": change["key"], "set": updates, "members": per_member})

        output_stream = io.BytesIO()
        with zipfile.ZipFile(output_stream, "w") as target:
            for info in infos:
                data = (
                    _write_csv(member_headers[info.filename], member_rows[info.filename])
                    if info.filename in CSV_MEMBERS
                    else source.read(info.filename)
                )
                target.writestr(info, data)

    package_bytes = output_stream.getvalue()
    preview: dict[str, object] = {
        "status": "validated",
        "task_code": TASK_CODE,
        "source_export_zip": str(export_zip.resolve()),
        "baseline_csv": str(baseline_path.resolve()),
        "selected_row_count": len(changes),
        "csv_members": list(CSV_MEMBERS),
        "rows": preview_rows,
        "output_sha256": hashlib.sha256(package_bytes).hexdigest(),
    }
    if mapping_change_requested:
        preview["fusion_attribute_validation"] = {
            "status": "validated",
            "target_environment": target_environment.strip() if target_environment else "",
            "objects": attribute_evidence,
        }
    return package_bytes, preview


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    preview_path = args.preview or args.output_zip.with_suffix(args.output_zip.suffix + ".preview.json")
    try:
        attribute_metadata_paths = parse_attribute_metadata_args(args.fusion_attributes)
        package_bytes, preview = build_package(
            args.export_zip,
            args.baseline,
            args.changes,
            attribute_metadata_paths,
            args.target_environment,
        )
        preview["dry_run"] = bool(args.dry_run)
        preview["output_zip"] = str(args.output_zip.resolve())
        preview_path.parent.mkdir(parents=True, exist_ok=True)
        preview_path.write_text(json.dumps(preview, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if not args.dry_run:
            args.output_zip.parent.mkdir(parents=True, exist_ok=True)
            args.output_zip.write_bytes(package_bytes)
    except (OSError, PackageError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(preview, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
