#!/usr/bin/env python3
"""Validate a Data Loader source file without uploading it to Fusion."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import data_loader_metadata as metadata
    import data_loader_report
    import upload_and_initiate as loader
except ModuleNotFoundError:
    from scripts import data_loader_metadata as metadata
    from scripts import data_loader_report
    from scripts import upload_and_initiate as loader


def validate_data_load_file(
    source_path: Path,
    config_path: Path = loader.DEFAULT_CONFIG,
    *,
    auth_options: dict[str, Any] | None = None,
    business_object: str | None = None,
) -> tuple[dict[str, Any], loader.PreparedArchive]:
    """Run local and live validation without making a POST request."""
    suffix = loader.validate_local_source(source_path)
    if business_object and suffix not in {".csv", ".xlsx"}:
        raise metadata.DataLoadError(
            "source-selection",
            "--business-object is supported only for a single CSV or XLSX source.",
        )

    config = loader.read_config(config_path, **(auth_options or {}))
    schema: metadata.BusinessObjectSchema | None = None
    converted_content: bytes | None = None
    source_type: str | None = None
    if suffix == ".zip":
        source_type = loader.archive_source_type(source_path)
        if source_type == loader.FSM_SOURCE_TYPE:
            schemas: tuple[metadata.BusinessObjectSchema, ...] = ()
        else:
            schemas = loader.validate_zip_business_objects(source_path, config)
    else:
        schema = loader.validate_file_discriminator(
            source_path, config, business_object=business_object
        )
        converted_content = loader.validate_source_attributes(
            source_path, suffix, schema, business_object=business_object
        )
        schemas = (schema,)
    prepared = loader.prepare_archive(
        source_path,
        xlsx_member_discriminator=(schema.discriminator if suffix == ".xlsx" and schema else None),
        csv_member_discriminator=(schema.discriminator if suffix == ".csv" and schema else None),
        schema=schema,
        converted_content=converted_content,
    )
    result = {
        "fileName": source_path.name,
        "UIName": schema.ui_name if schema else "Validated ZIP archive",
        "BusObjTopDiscriminator": schema.discriminator if schema else "",
        "archiveName": prepared.file_name,
        "archiveSha256": loader.archive_sha256(prepared.content),
        "sections": [section.discriminator for section in schema.sections] if schema else [],
    }
    return (
        result,
        prepared,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a Fusion Data Loader source file without uploading or initiating a load."
    )
    parser.add_argument("source_path", type=Path)
    metadata.add_oauth_arguments(parser)
    parser.add_argument(
        "--business-object",
        help=(
            "Exact registered Data Loader business-object discriminator for a single CSV or XLSX source; "
            "for an ambiguous 30-character XLSX root prefix, selects the intended longer discriminator."
        ),
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        help="Optional initialized project/<project_id> fallback when the source directory cannot hold the validated ZIP.",
    )
    parser.add_argument("--output-zip", type=Path)
    parser.add_argument(
        "--inline-output",
        type=Path,
        help="Deprecated compatibility option; inline HTML rendering is disabled.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result, prepared = validate_data_load_file(
            args.source_path,
            args.properties,
            auth_options=metadata.oauth_kwargs(args),
            business_object=args.business_object,
        )
        output_zip = args.output_zip or (args.source_path.parent / prepared.file_name)
        if output_zip.suffix.lower() != ".zip":
            raise metadata.DataLoadError("file-validation", "--output-zip must use a .zip filename.")
        if args.output_zip:
            prepared = loader.PreparedArchive(output_zip.name, prepared.content)
        project_review_directory = (
            loader.project_review_archive_directory(args.project_root)
            if args.project_root is not None and args.output_zip is None
            else None
        )
        output_path = loader.persist_prepared_archive(
            prepared,
            output_zip.parent,
            project_review_directory=project_review_directory,
        )
        result["archiveName"] = output_path.name
        result["outputPath"] = str(output_path)
    except metadata.DataLoadError as exc:
        data_loader_report.emit_inline_or_markdown(
            exc,
            "error",
            args.inline_output,
            data_loader_report.render_error_report,
            stream=sys.stderr,
        )
        return 1

    data_loader_report.emit_inline_or_markdown(
        result,
        "validation",
        args.inline_output,
        data_loader_report.render_validation_report,
        stream=sys.stdout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
