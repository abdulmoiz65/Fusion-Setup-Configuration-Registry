#!/usr/bin/env python3
"""Prepare Territory Geography domain CSV data for the native core Data Loader."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


CSV_HEADERS = (
    "GeographyOrZoneName",
    "LanguageCode",
    "SourceId",
    "ParentSourceId",
    "GeographyOrZoneType",
    "ZoneCode",
    "CountryName",
    "GeoParentName1",
    "GeoParentName2",
    "GeoParentName3",
    "GeoParentName4",
    "GeoParentName5",
)
LEGACY_CSV_HEADERS = CSV_HEADERS[:-1]
SUPPORTED_CSV_HEADERS = (LEGACY_CSV_HEADERS, CSV_HEADERS)
REQUIRED_FIELDS = (
    "GeographyOrZoneName",
    "LanguageCode",
    "SourceId",
    "GeographyOrZoneType",
)
OBJECT_CODE = "GeoTerritoryInterface"
DEFAULT_OUTPUT_FILE = "territory-geographies.csv"
VALIDATION_FILE = "territory-geographies-validation.json"
HANDOFF_FILE = "territory-geographies-data-loader-handoff.json"
METADATA_VALIDATION_FILE = "territory-geographies-import-metadata-validation.json"
METADATA_ENDPOINT = (
    "/crmRestApi/resources/11.13.18.05/importExportObjectMetadata/"
    "GeoTerritoryInterface"
)
SOURCE_ID_PATTERN = re.compile(r"^[0-9]+$")
MAX_SOURCE_ID = 9_223_372_036_854_775_807


class TerritoryValidationError(ValueError):
    """Raised when one or more local source validation checks fail."""

    def __init__(self, issues: Iterable[dict[str, Any]]):
        self.issues = list(issues)
        super().__init__(f"Territory Geography validation failed with {len(self.issues)} issue(s)")


class TerritoryMetadataMismatch(TerritoryValidationError):
    """Raised when target import metadata differs from the reviewed contract."""


def issue(code: str, message: str, row: int | None = None, field: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"code": code, "message": message}
    if row is not None:
        result["row"] = row
    if field is not None:
        result["field"] = field
    return result


def normalize_scalar(value: Any, *, row_number: int, field: str) -> str:
    if value is None:
        return ""
    if isinstance(value, bool) or isinstance(value, (list, dict)):
        raise TerritoryValidationError(
            [issue("invalid_value_type", "Use a string or number for every CSV value", row_number, field)]
        )
    if isinstance(value, (str, int, float)):
        return str(value)
    raise TerritoryValidationError(
        [issue("invalid_value_type", f"Unsupported value type: {type(value).__name__}", row_number, field)]
    )


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise TerritoryValidationError([issue("source_not_found", f"CSV file does not exist: {path}")])

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        actual_headers = tuple(reader.fieldnames or ())
        if actual_headers not in SUPPORTED_CSV_HEADERS:
            raise TerritoryValidationError(
                [
                    issue(
                        "invalid_headers",
                        "CSV headers must match the Territory Geography contract and order, with optional GeoParentName5",
                    ),
                    issue(
                        "expected_headers",
                        f"{','.join(LEGACY_CSV_HEADERS)} or {','.join(CSV_HEADERS)}",
                    ),
                    issue("actual_headers", ",".join(actual_headers)),
                ]
            )

        rows: list[dict[str, str]] = []
        issues: list[dict[str, Any]] = []
        for row_number, source_row in enumerate(reader, start=2):
            if None in source_row:
                issues.append(
                    issue("extra_columns", "Row contains more values than the header contract", row_number)
                )
                continue
            row = {header: source_row.get(header) or "" for header in CSV_HEADERS}
            if not any(row.values()):
                issues.append(issue("empty_row", "Remove the empty data row", row_number))
                continue
            rows.append(row)

    if issues:
        raise TerritoryValidationError(issues)
    return rows


def read_json_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise TerritoryValidationError([issue("source_not_found", f"JSON file does not exist: {path}")])

    data = json.loads(path.read_text(encoding="utf-8"))
    records = data.get("records") if isinstance(data, dict) else data
    if not isinstance(records, list):
        raise TerritoryValidationError(
            [issue("invalid_json_shape", "JSON input must be an array or an object with a records array")]
        )

    rows: list[dict[str, str]] = []
    issues: list[dict[str, Any]] = []
    for row_number, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            issues.append(issue("invalid_record", "Every records entry must be an object", row_number))
            continue
        unknown = sorted(set(record) - set(CSV_HEADERS))
        if unknown:
            issues.append(
                issue("unknown_fields", f"Unknown fields: {', '.join(unknown)}", row_number)
            )
            continue
        try:
            rows.append(
                {
                    header: normalize_scalar(record.get(header), row_number=row_number, field=header)
                    for header in CSV_HEADERS
                }
            )
        except TerritoryValidationError as exc:
            issues.extend(exc.issues)

    if issues:
        raise TerritoryValidationError(issues)
    return rows


def validate_rows(rows: list[dict[str, str]]) -> dict[str, Any]:
    if not rows:
        raise TerritoryValidationError([issue("no_rows", "Provide at least one Territory Geography row")])

    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    root_ids: list[str] = []
    type_counts: Counter[str] = Counter()

    for index, row in enumerate(rows, start=2):
        for field in CSV_HEADERS:
            value = row.get(field, "")
            if "\x00" in value or "\n" in value or "\r" in value:
                errors.append(
                    issue("invalid_control_character", "Embedded NUL or line-break characters are not supported", index, field)
                )
            if value != value.strip():
                errors.append(
                    issue("surrounding_whitespace", "Remove surrounding whitespace; values are not silently trimmed", index, field)
                )

        for field in REQUIRED_FIELDS:
            if not row.get(field, ""):
                errors.append(issue("missing_required_value", "Required value is blank", index, field))

        source_id = row.get("SourceId", "")
        parent_id = row.get("ParentSourceId", "")
        geography_type = row.get("GeographyOrZoneType", "").upper()
        type_counts[geography_type or "<blank>"] += 1

        if source_id:
            if not SOURCE_ID_PATTERN.fullmatch(source_id) or int(source_id) > MAX_SOURCE_ID:
                errors.append(
                    issue(
                        "invalid_source_id",
                        "SourceId must be an unsigned integer within the Oracle Long range",
                        index,
                        "SourceId",
                    )
                )
            if source_id in seen_ids:
                errors.append(issue("duplicate_source_id", f"Duplicate SourceId: {source_id}", index, "SourceId"))
            else:
                seen_ids.add(source_id)

        if parent_id:
            if not SOURCE_ID_PATTERN.fullmatch(parent_id) or int(parent_id) > MAX_SOURCE_ID:
                errors.append(
                    issue(
                        "invalid_parent_source_id",
                        "ParentSourceId must be an unsigned integer within the Oracle Long range",
                        index,
                        "ParentSourceId",
                    )
                )
            if parent_id == source_id:
                errors.append(issue("self_parent", "A row cannot reference itself as parent", index, "ParentSourceId"))
            elif parent_id not in seen_ids:
                errors.append(
                    issue(
                        "missing_or_forward_parent",
                        f"ParentSourceId {parent_id} must identify an earlier row in the same file",
                        index,
                        "ParentSourceId",
                    )
                )
        else:
            root_ids.append(source_id)

        if index > 2 and not parent_id:
            errors.append(issue("non_root_without_parent", "Every non-root row requires ParentSourceId", index, "ParentSourceId"))

        name = row.get("GeographyOrZoneName", "")
        if geography_type == "POSTAL CODE" and name.isdigit() and len(name) < 5:
            warnings.append(
                issue(
                    "short_numeric_postal_code",
                    "Preserved exactly; verify whether leading zeroes were lost before this input reached the skill",
                    index,
                    "GeographyOrZoneName",
                )
            )

    if len(root_ids) != 1:
        errors.append(issue("invalid_root_count", f"Expected exactly one root row; found {len(root_ids)}"))
    elif rows[0].get("SourceId") != root_ids[0]:
        errors.append(issue("root_not_first", "The single root row must be the first data row"))

    if errors:
        raise TerritoryValidationError(errors)

    return {
        "status": "validated",
        "rowCount": len(rows),
        "rootSourceId": root_ids[0],
        "countsByGeographyOrZoneType": dict(sorted(type_counts.items())),
        "warnings": warnings,
        "dataLoaderContract": {
            "executionRoute": "core.data-loader",
            "sourceType": "ORA_CX_IMPORT",
            "cxImportObjectCode": OBJECT_CODE,
            "ucmAccountSource": "target_import_metadata",
            "newRecordIntent": True,
            "serverCreateOnlyGuaranteed": False,
        },
    }


def validate_import_metadata(payload: Any) -> dict[str, Any]:
    record = payload
    if isinstance(payload, dict) and "items" in payload:
        items = payload.get("items")
        if not isinstance(items, list) or len(items) != 1:
            raise TerritoryMetadataMismatch(
                [issue("metadata_match_count", "Expected exactly one import metadata record")]
            )
        record = items[0]

    if not isinstance(record, dict):
        raise TerritoryMetadataMismatch(
            [issue("invalid_metadata_shape", "Import metadata response must be one JSON object")]
        )

    expected = {
        "ObjectCode": OBJECT_CODE,
        "ImportSupport": "Y",
    }
    mismatches = [
        issue(
            "metadata_value_mismatch",
            f"Expected {field}={value!r}; target returned {record.get(field)!r}",
            field=field,
        )
        for field, value in expected.items()
        if record.get(field) != value
    ]
    if mismatches:
        raise TerritoryMetadataMismatch(mismatches)

    account = record.get("UcmAccount")
    if (not isinstance(account, str) or not account
            or any(segment in {".", ".."} for segment in account.split("/"))
            or not re.fullmatch(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*", account)):
        raise TerritoryMetadataMismatch(
            [issue("invalid_ucm_account", "Target UcmAccount must be a nonempty slash-separated account path", field="UcmAccount")]
        )

    return {
        "status": "validated",
        "sourceEndpoint": METADATA_ENDPOINT,
        "objectCode": record["ObjectCode"],
        "canonicalUcmAccount": account,
        "erpUcmAccount": "$/".join(account.split("/")) + "$",
        "importSupport": record["ImportSupport"],
    }


def validate_output_file_name(file_name: str) -> str:
    if Path(file_name).name != file_name or not file_name.lower().endswith(".csv"):
        raise TerritoryValidationError(
            [issue("invalid_output_file_name", "Output file name must be a base name ending in .csv")]
        )
    return file_name


def build_handoff(*, file_name: str, sha256: str, row_count: int) -> dict[str, Any]:
    """Describe a source; only Data Loader can validate and authorize submission."""
    return {
        "status": "source_prepared",
        "executionRoute": "core.data-loader",
        "approvalOwner": "core.data-loader.task-hook",
        "cxImportObjectCode": OBJECT_CODE,
        "newRecordIntent": True,
        "serverCreateOnlyGuaranteed": False,
        "submissionAuthorized": False,
        "source": {"fileName": file_name, "sha256": sha256, "rowCount": row_count},
        "nextAction": "Run native CX Data Loader preflight, then Task Hook validation and preview for the final immutable archive before approval.",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_HEADERS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def refuse_existing(paths: Iterable[Path], overwrite: bool) -> None:
    existing = [str(path) for path in paths if path.exists()]
    if existing and not overwrite:
        raise TerritoryValidationError(
            [issue("output_exists", f"Refusing to overwrite existing output: {path}") for path in existing]
        )


def command_template(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.output).expanduser().resolve()
    refuse_existing([output], args.overwrite)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(CSV_HEADERS)
    return {"status": "created", "template": str(output), "headers": list(CSV_HEADERS)}


def command_prepare(args: argparse.Namespace) -> dict[str, Any]:
    rows = read_csv_rows(Path(args.input_csv).expanduser().resolve()) if args.input_csv else read_json_rows(
        Path(args.records_json).expanduser().resolve()
    )
    validation = validate_rows(rows)
    file_name = validate_output_file_name(args.output_file_name)
    if args.dry_run:
        return {"status": "validated", "dryRun": True, "rowCount": len(rows),
                "warnings": validation["warnings"], "executionRoute": "core.data-loader"}
    output_dir = Path(args.output_dir).expanduser().resolve()
    csv_path = output_dir / file_name
    validation_path = output_dir / VALIDATION_FILE
    handoff_path = output_dir / HANDOFF_FILE
    refuse_existing([csv_path, validation_path, handoff_path], args.overwrite)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(csv_path, rows)
    checksum = file_sha256(csv_path)
    validation["source"] = {
        "inputType": "csv" if args.input_csv else "records_json",
        "normalizedFile": str(csv_path), "sha256": checksum,
    }
    handoff = build_handoff(file_name=file_name, sha256=checksum, row_count=len(rows))
    write_json(validation_path, validation)
    write_json(handoff_path, handoff)
    return {
        "status": "prepared", "csv": str(csv_path), "validation": str(validation_path),
        "handoff": str(handoff_path), "rowCount": len(rows),
        "warningCount": len(validation["warnings"]), "sha256": checksum,
    }


def command_validate_metadata(args: argparse.Namespace) -> dict[str, Any]:
    input_path = Path(args.input_json).expanduser().resolve()
    if not input_path.is_file():
        raise TerritoryValidationError(
            [issue("source_not_found", f"Metadata JSON file does not exist: {input_path}")]
        )
    result = validate_import_metadata(json.loads(input_path.read_text(encoding="utf-8")))
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        refuse_existing([output_path], args.overwrite)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        write_json(output_path, result)
        result["output"] = str(output_path)
    return result


def command_finalize_preview(args: argparse.Namespace) -> dict[str, Any]:
    raise TerritoryValidationError([issue(
        "retired_execution_route",
        "Direct Import Activities payload finalization is retired. Use core.data-loader native CX preflight and Task Hook approval; legacy staged files require supported reconciliation.",
    )])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare Territory Geography CSV data for core Data Loader (local only)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    template = subparsers.add_parser("template", help="Write the exact header-only CSV template.")
    template.add_argument("--output", required=True)
    template.add_argument("--overwrite", action="store_true")
    template.set_defaults(handler=command_template)

    prepare = subparsers.add_parser("prepare", help="Validate input and write CSV, validation, and Data Loader handoff artifacts.")
    source = prepare.add_mutually_exclusive_group(required=True)
    source.add_argument("--input-csv")
    source.add_argument("--records-json")
    prepare.add_argument("--output-dir", required=True)
    prepare.add_argument("--output-file-name", default=DEFAULT_OUTPUT_FILE)
    prepare.add_argument("--dry-run", action="store_true", help="Validate without writing artifacts.")
    prepare.add_argument("--overwrite", action="store_true")
    prepare.set_defaults(handler=command_prepare)

    metadata = subparsers.add_parser(
        "validate-metadata",
        help="Validate target GeoTerritoryInterface metadata before approval or upload.",
    )
    metadata.add_argument("--input-json", required=True)
    metadata.add_argument("--output")
    metadata.add_argument("--overwrite", action="store_true")
    metadata.set_defaults(handler=command_validate_metadata)

    finalize = subparsers.add_parser(
        "finalize-preview",
        help="Retired direct-import command; always fails without side effects.",
    )
    finalize.add_argument("--preview", required=True)
    finalize.add_argument("--approval", required=True)
    finalize.add_argument("--staging-result", required=True)
    finalize.add_argument("--output", required=True)
    finalize.add_argument("--overwrite", action="store_true")
    finalize.set_defaults(handler=command_finalize_preview)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.handler(args)
    except TerritoryMetadataMismatch as exc:
        print(
            json.dumps(
                {
                    "status": "failed",
                    "failureClass": "catalog_or_metadata_mismatch",
                    "issues": exc.issues,
                },
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1
    except TerritoryValidationError as exc:
        print(json.dumps({"status": "failed", "failureClass": "input_validation", "issues": exc.issues}, indent=2), file=sys.stderr)
        return 1
    except (OSError, UnicodeError, json.JSONDecodeError, csv.Error) as exc:
        print(
            json.dumps(
                {"status": "failed", "failureClass": "input_validation", "issues": [issue("source_error", str(exc))]},
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
