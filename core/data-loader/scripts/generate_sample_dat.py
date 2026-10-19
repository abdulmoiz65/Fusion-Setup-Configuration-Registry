#!/usr/bin/env python3
"""Generate a live-metadata-grounded XLSX or explicitly requested DAT sample."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import urllib.parse
from pathlib import Path
from typing import Any, Iterable

try:
    import data_loader_report
    import data_loader_metadata as metadata
    import rest_sample_data
    import xlsx_sample_workbook
except ModuleNotFoundError:  # Imported by tests from the skill root.
    from scripts import data_loader_report
    from scripts import data_loader_metadata as metadata
    from scripts import rest_sample_data
    from scripts import xlsx_sample_workbook

def _attribute_details(
    schema: metadata.BusinessObjectSchema, discriminator: str
) -> dict[str, dict[str, Any]]:
    return {
        metadata.normalize_attribute_name(str(attribute["AttributeName"])): attribute
        for attribute in schema.attributes.get(discriminator, ())
    }


def _selected_attribute_names(
    schema: metadata.BusinessObjectSchema, section: metadata.TemplateSection
) -> tuple[str, ...]:
    details = _attribute_details(schema, section.discriminator)
    if not details:
        return section.attribute_names

    selected: list[str] = []
    for name in section.attribute_names:
        detail = details.get(name)
        if (
            (detail is not None and (metadata.is_mandatory(detail) or metadata.is_key_attribute(detail)))
            or name == "RestAction"
            or (section.discriminator != schema.discriminator and name == "ParentIdentifier")
        ):
            selected.append(name)
    if not selected and section.attribute_names:
        selected.append(section.attribute_names[0])
    return tuple(selected)


def _key_field_attribute_names(
    schema: metadata.BusinessObjectSchema, section: metadata.TemplateSection
) -> tuple[str, ...]:
    """Select the create keys needed by the reduced XLSX sample worksheet."""
    details = _attribute_details(schema, section.discriminator)
    # Template-only sections have no component metadata to classify. Keep their
    # template fields visible rather than producing an invalid empty worksheet.
    if not details:
        return section.attribute_names
    selected: list[str] = []
    for name in section.attribute_names:
        detail = details.get(name)
        if (
            (detail is not None and (
                metadata.is_surrogate_id_attribute(detail)
                or metadata.is_mandatory(detail)
                or metadata.is_required_for_create(detail)
                or metadata.is_key_attribute(detail)
                or metadata.is_foreign_key_attribute(detail)
            ))
            or name == "RestAction"
            or (section.discriminator != schema.discriminator and name == "ParentIdentifier")
        ):
            selected.append(name)

    present_attributes = set(selected)
    retained: list[str] = []
    for name in selected:
        detail = details.get(name)
        removable_id = detail is not None and (
            metadata.is_mandatory(detail) or metadata.is_foreign_key_attribute(detail)
        )
        if (
            removable_id
            and not metadata.is_surrogate_id_attribute(detail)
            and metadata.mandatory_id_has_user_key_alternative(
                name, detail, present_attributes
            )
        ):
            continue
        retained.append(name)
    return tuple(retained)


def _bounded(value: str, detail: dict[str, Any] | None) -> str:
    if detail is None:
        return value
    raw_length = detail.get("DataLength")
    try:
        length = int(raw_length) if raw_length not in (None, "") else None
    except (TypeError, ValueError):
        length = None
    if length is not None and length > 0:
        return value[:length]
    return value


def _number_value(detail: dict[str, Any] | None) -> str:
    precision = None
    if detail is not None:
        raw_precision = detail.get("NumberPrecision") or detail.get("DataLength")
        try:
            precision = int(raw_precision) if raw_precision not in (None, "") else None
        except (TypeError, ValueError):
            precision = None
    digits = "100000000000001"
    if precision is not None and precision > 0:
        digits = digits[:precision]
    return digits or "1"


def placeholder_value(
    name: str, detail: dict[str, Any] | None, *, object_type: str = ""
) -> str:
    lowered = name.lower()
    data_type = str((detail or {}).get("DataType") or "").lower()
    if name == "RestAction":
        return "POST"
    if name == "ParentIdentifier":
        return _bounded("PARENT_1", detail)
    if name == "SourceRefTableName":
        return _bounded("SAMPLE_SOURCE", detail)
    if name.startswith("SourceRef"):
        return _bounded("ROW_1", detail)
    if name.startswith("FLEX:"):
        return "Global Data Elements"
    if data_type == "date" and object_type != "ADF_VO":
        return _bounded("SAMPLE_VALUE", detail)
    if data_type == "date":
        return _bounded("2026/01/01", detail)
    if "timestamp" in lowered or "datetime" in lowered:
        return _bounded("2026-01-01T00:00:00Z", detail)
    if object_type == "ADF_VO" and (lowered.endswith("date") or "date" in lowered):
        return _bounded("2026/01/01", detail)
    if lowered.endswith("flag") or str((detail or {}).get("DataLength") or "") == "1":
        return "Y"
    if "subinventory" in lowered:
        return _bounded("SAMPLE_SUB", detail)
    if lowered == "organizationcode":
        return _bounded("SAMPLE_ORG", detail)
    if lowered == "organizationname":
        return _bounded("Sample Inventory Organization", detail)
    if data_type == "number" or lowered.endswith("id") or " + " in name:
        return _number_value(detail)
    if lowered.endswith("code"):
        return _bounded("SAMPLE_CODE", detail)
    if lowered.endswith("name"):
        return _bounded("Sample Name", detail)
    return _bounded("SAMPLE_VALUE", detail)


def _sample_header_name(section: metadata.TemplateSection, name: str) -> str:
    return section.raw_name_for(name)


def _registered_rest_results(
    schema: metadata.BusinessObjectSchema,
    config: dict[str, str],
    *,
    getter: metadata.Getter,
) -> dict[str, rest_sample_data.RestSampleResult]:
    """Probe registered sections parent-first and preserve one REST item lineage."""
    results: dict[str, rest_sample_data.RestSampleResult] = {}
    item_paths: dict[str, str] = {}
    sections = schema.sections_by_discriminator
    ordered_discriminators = metadata._ordered_component_discriminators(
        schema.components, schema.discriminator
    )

    for discriminator in ordered_discriminators:
        section = sections.get(discriminator)
        if section is None:
            continue

        if discriminator == schema.discriminator:
            encoded = urllib.parse.quote(schema.discriminator, safe="")
            collection_path = (
                f"/fscmRestApi/resources/{rest_sample_data.REST_API_VERSION}/{encoded}"
            )
        else:
            component = schema.components[discriminator]
            parent_discriminator = str(
                component.get("ParentBusObjFileDiscriminator")
                or schema.discriminator
            ).strip()
            parent_item_path = item_paths.get(parent_discriminator)
            if parent_item_path is None:
                results[discriminator] = rest_sample_data.RestSampleResult(
                    discriminator,
                    False,
                    {},
                    reason=(
                        "parent REST item route was unavailable for "
                        + parent_discriminator
                    ),
                )
                continue
            encoded = urllib.parse.quote(discriminator, safe="")
            collection_path = parent_item_path + "/child/" + encoded

        result = rest_sample_data.probe_rest_sample(
            config,
            discriminator,
            collection_path,
            _selected_attribute_names(schema, section),
            _attribute_details(schema, discriminator),
            object_type=schema.object_type,
            getter=getter,
        )
        results[discriminator] = result
        if result.item_key is not None:
            encoded_key = urllib.parse.quote(result.item_key, safe="")
            item_paths[discriminator] = collection_path.rstrip("/") + "/" + encoded_key

    return results


def render_sample(
    schema: metadata.BusinessObjectSchema,
    config: dict[str, str],
    *,
    operation: str = "update",
    include_all_template_attributes: bool = False,
    key_fields_only: bool = False,
    omit_standard_who_columns: bool = False,
    blank_fallback_children: bool = False,
    include_data_loader_action: bool = False,
    getter: metadata.Getter = metadata.get_json,
) -> tuple[
    dict[str, tuple[tuple[str, ...], tuple[str, ...] | None]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    rows: dict[str, tuple[tuple[str, ...], tuple[str, ...] | None]] = {}
    section_summaries: list[dict[str, Any]] = []
    enriched_sections: list[dict[str, Any]] = []
    fallback_sections: list[dict[str, Any]] = []
    rest_results = (
        _registered_rest_results(schema, config, getter=getter)
        if operation == "update"
        else {}
    )
    for section in schema.sections:
        if include_all_template_attributes:
            output_names = section.attribute_names
        elif key_fields_only:
            output_names = _key_field_attribute_names(schema, section)
        else:
            output_names = _selected_attribute_names(schema, section)
        details = _attribute_details(schema, section.discriminator)
        if omit_standard_who_columns:
            output_names = tuple(
                name for name in output_names if not metadata.is_standard_who_column(name)
            )
        output_names = metadata.generated_attribute_order(output_names, details)
        rest_result = rest_results.get(
            section.discriminator,
            rest_sample_data.RestSampleResult(
                section.discriminator,
                False,
                {},
                reason="section has no registered BusObjFileDiscriminator REST route",
            ),
        )
        header_names = [_sample_header_name(section, name) for name in output_names]
        emit_blank_child_sheet = (
            blank_fallback_children
            and section.discriminator != schema.discriminator
            and not rest_result.enriched
        )
        if emit_blank_child_sheet:
            values = None
        else:
            values = []
            for name in output_names:
                if name == "RestAction":
                    values.append("PATCH" if rest_result.enriched else "POST")
                else:
                    values.append(
                        rest_result.values.get(
                            name, placeholder_value(
                                name, details.get(name), object_type=schema.object_type
                            )
                        )
                    )
            if operation in {"create", "delete"}:
                rest_action = "POST" if operation == "create" else "DELETE"
                values = [
                    rest_action if name == "RestAction" else placeholder_value(
                        name, details.get(name), object_type=schema.object_type
                    )
                    for name in output_names
                ]
        if include_data_loader_action and schema.object_type == "ADF_VO":
            header_names.append("DataLoaderAction")
            if values is not None:
                values.append("DELETE" if operation == "delete" else "MERGE")
        rows[section.discriminator] = (
            tuple(header_names),
            None if values is None else tuple(values),
        )
        section_summaries.append(
            {
                "discriminator": section.discriminator,
                "fieldCount": len(output_names),
                "restValueCount": len(rest_result.values),
            }
        )
        if rest_result.enriched:
            enriched_sections.append(
                {
                    "discriminator": section.discriminator,
                    "restValueCount": len(rest_result.values),
                }
            )
        else:
            fallback: dict[str, Any] = {
                "discriminator": section.discriminator,
                "reason": rest_result.reason,
            }
            if rest_result.http_status is not None:
                fallback["httpStatus"] = rest_result.http_status
            fallback_sections.append(fallback)
    return (
        rows,
        section_summaries,
        enriched_sections,
        fallback_sections,
    )


def render_dat(
    schema: metadata.BusinessObjectSchema,
    rows: dict[str, tuple[tuple[str, ...], tuple[str, ...] | None]],
    *,
    operation: str = "create",
) -> str:
    """Render the selected live-template fields as one deterministic DAT record set."""
    lines: list[str] = []
    for section in schema.sections:
        header, values = rows[section.discriminator]
        lines.append("METADATA|" + section.discriminator + "|" + "|".join(header))
        if values is None:
            continue
        lines.append(
            (("DELETE" if operation == "delete" else "MERGE") if schema.object_type == "ADF_VO"
             else xlsx_sample_workbook.dat_record_directive(header, values))
            + "|"
            + section.discriminator
            + "|"
            + "|".join(values)
        )
    return "\n".join(lines) + "\n"


def populate_sample_rows(
    schema: metadata.BusinessObjectSchema,
    sample_rows: dict[str, tuple[tuple[str, ...], tuple[str, ...] | None]],
    population: dict[str, list[dict[str, Any]]],
    mapping_overrides: dict[tuple[str, str], str | None],
) -> dict[str, tuple[tuple[str, ...], Any]]:
    """Return full editable rows populated only from reviewed user values."""
    unknown_sections = sorted(set(population) - set(schema.sections_by_discriminator))
    if unknown_sections:
        raise metadata.DataLoadError("mapping", "Unknown populated section: " + ", ".join(unknown_sections))
    metadata.set_mapping_overrides(mapping_overrides)
    try:
        populated: dict[str, tuple[tuple[str, ...], Any]] = {}
        review_errors: list[str] = []
        for section in schema.sections:
            header, sample_values = sample_rows[section.discriminator]
            source_rows = population.get(section.discriminator, [])
            if not isinstance(source_rows, list) or any(not isinstance(row, dict) for row in source_rows):
                raise metadata.DataLoadError("mapping", f"Populated rows for {section.discriminator} must be a JSON array of objects.")
            source_headers: list[str] = []
            for row in source_rows:
                for source in row:
                    if not isinstance(source, str) or not source.strip():
                        raise metadata.DataLoadError("mapping", f"Populated rows for {section.discriminator} must use nonblank field names.")
                    if metadata.normalized_name(source) == "dataloaderaction" and (
                        source != "DataLoaderAction" or schema.object_type != "ADF_VO"
                    ):
                        raise metadata.DataLoadError("mapping", "DataLoaderAction requires the exact header on an ADF_VO workbook.")
                    if source not in source_headers:
                        source_headers.append(source)
            if not source_headers:
                populated[section.discriminator] = (header, None)
                continue
            mapped_headers = [source for source in source_headers if source != "DataLoaderAction"]
            mapped, indexes, audit = metadata.map_source_headers(section.discriminator, mapped_headers, schema)
            review = [
                f"{item.source_column} -> {item.target_attribute or 'unmapped'}"
                for item in audit
                if item.status in {"fuzzy", "unmapped"}
            ]
            if review:
                review_errors.append(f"{section.discriminator}: " + ", ".join(review))
                continue
            positions = {name: index for index, name in enumerate(header)}
            values_by_row: list[tuple[str, ...]] = []
            for source_row in source_rows:
                values = ["" for _name in header]
                if "DataLoaderAction" in positions and sample_values is not None:
                    values[positions["DataLoaderAction"]] = sample_values[positions["DataLoaderAction"]]
                for target, source_index in zip(mapped, indexes):
                    if target in positions:
                        raw_value = source_row.get(mapped_headers[source_index], "")
                        values[positions[target]] = "" if raw_value is None else str(raw_value)
                if "DataLoaderAction" in positions and "DataLoaderAction" in source_row:
                    raw_action = source_row["DataLoaderAction"]
                    values[positions["DataLoaderAction"]] = "" if raw_action is None else str(raw_action)
                values_by_row.append(tuple(values))
            populated[section.discriminator] = (header, tuple(values_by_row))
        if review_errors:
            raise metadata.DataLoadError(
                "mapping",
                "Mapping review required for: " + "; ".join(review_errors)
                + ". Use --mapping-edit SECTION/SOURCE=ATTRIBUTE or SECTION/SOURCE=exclude.",
            )
        return populated
    finally:
        metadata.set_mapping_overrides({})


def preview_values(values: Any) -> list[str] | None:
    if values is None:
        return None
    if values and isinstance(values[0], tuple):
        return list(values[0])
    return list(values)


def generate_sample(
    business_object: str,
    output_dir: Path = Path.cwd(),
    config_path: Path = metadata.DEFAULT_CONFIG,
    *,
    auth_options: dict[str, Any] | None = None,
    operation: str = "create",
    output_format: str = "xlsx",
    populated_rows: dict[str, list[dict[str, Any]]] | None = None,
    mapping_overrides: dict[tuple[str, str], str | None] | None = None,
    getter: metadata.Getter = metadata.get_json,
    byte_getter: metadata.ByteGetter = metadata.get_bytes,
) -> dict[str, Any]:
    config = metadata.read_config(config_path, **(auth_options or {}))
    schema = metadata.load_business_object_schema(
        business_object,
        config,
        allow_aliases=True,
        sample_attribute_lookup=True,
        getter=getter,
        byte_getter=byte_getter,
        allow_attribute_schema_fallback=True,
    )
    if operation not in {"create", "update", "delete"}:
        raise metadata.DataLoadError("sample-generation", "Operation must be create, update, or delete.")
    if output_format not in {"xlsx", "dat"}:
        raise metadata.DataLoadError("sample-generation", "Output format must be xlsx or dat.")
    if populated_rows is not None and output_format != "xlsx":
        raise metadata.DataLoadError("sample-generation", "Populated workbook generation supports XLSX output only.")
    rows, sections, enriched_sections, fallback_sections = render_sample(
        schema,
        config,
        operation=operation,
        include_all_template_attributes=output_format == "xlsx",
        omit_standard_who_columns=output_format == "xlsx",
        blank_fallback_children=output_format == "xlsx",
        include_data_loader_action=output_format == "xlsx",
        getter=getter,
    )
    output_path = output_dir.expanduser() / (schema.discriminator + "." + output_format)
    attribute_details_path = output_dir.expanduser() / (
        schema.discriminator + "_attribute-details.xlsx"
    )
    key_fields_path = output_dir.expanduser() / (
        schema.discriminator + "_key-fields.xlsx"
    )
    try:
        product_metadata = rest_sample_data.product_attribute_metadata(
            config,
            schema.discriminator,
            tuple(section.discriminator for section in schema.sections),
            getter=getter,
        )
        xlsx_sample_workbook.write_attribute_details_workbook(
            schema, attribute_details_path, product_metadata
        )
        if output_format == "xlsx":
            if populated_rows is not None:
                rows = populate_sample_rows(schema, rows, populated_rows, mapping_overrides or {})
            xlsx_sample_workbook.write_sample_workbook(schema, rows, output_path)
            _content, source_sections = xlsx_sample_workbook.xlsx_to_dat(
                output_path,
                root_discriminator=schema.discriminator,
                section_discriminators=tuple(section.discriminator for section in schema.sections),
                object_type=schema.object_type,
            )
            metadata.validate_source_sections(source_sections, schema)
            key_field_rows, _, _, _ = render_sample(
                schema,
                config,
                operation=operation,
                key_fields_only=True,
                omit_standard_who_columns=True,
                blank_fallback_children=True,
                include_data_loader_action=True,
                getter=getter,
            )
            xlsx_sample_workbook.write_sample_workbook(
                schema, key_field_rows, key_fields_path
            )
            _content, source_sections = xlsx_sample_workbook.xlsx_to_dat(
                key_fields_path,
                root_discriminator=schema.discriminator,
                section_discriminators=tuple(section.discriminator for section in schema.sections),
                object_type=schema.object_type,
            )
            metadata.validate_source_sections(source_sections, schema)
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(render_dat(schema, rows, operation=operation), encoding="utf-8")
    except OSError as exc:
        raise metadata.DataLoadError(
            "sample-generation", f"Unable to write sample {output_format.upper()} file {output_path}: {exc}"
        ) from exc
    result = {
        "fileName": output_path.name,
        "outputPath": str(output_path.resolve()),
        "BusinessObjectId": schema.business_object_id,
        "BusObjTopDiscriminator": schema.discriminator,
        "UIName": schema.ui_name,
        "UcmContentId": schema.ucm_content_id,
        "schemaSource": schema.schema_source,
        "sectionCount": len(sections),
        "sections": sections,
        "previewRows": [
            {
                "section": section.discriminator,
                "headers": list(rows[section.discriminator][0]),
                "values": preview_values(rows[section.discriminator][1]),
            }
            for section in schema.sections
        ],
        "restHost": config["host"],
        "restApiVersion": rest_sample_data.REST_API_VERSION,
        "restEnrichedSectionCount": len(enriched_sections),
        "restEnrichedSections": enriched_sections,
        "restFallbackSectionCount": len(fallback_sections),
        "restFallbackSections": fallback_sections,
        "uploaded": False,
    }
    result["attributeDetailsFile"] = {
        "fileName": attribute_details_path.name,
        "outputPath": str(attribute_details_path.resolve()),
        "sections": [section.discriminator for section in schema.sections],
    }
    if output_format == "xlsx":
        result["keyFieldsFile"] = {
            "fileName": key_fields_path.name,
            "outputPath": str(key_fields_path.resolve()),
            "sections": [section.discriminator for section in schema.sections],
        }
    return result


def _section_names(result: dict[str, Any]) -> list[str]:
    return [
        str(section.get("discriminator") or "")
        if isinstance(section, dict)
        else str(section)
        for section in result.get("sections") or []
    ]


def _publish_sample_batch(
    staged_files: Iterable[tuple[Path, Path]], output_dir: Path
) -> None:
    """Publish a validated batch and restore prior targets after a failed commit."""
    pairs = tuple(staged_files)
    targets = [target for _source, target in pairs]
    if len(targets) != len(set(targets)):
        raise metadata.DataLoadError(
            "sample-generation", "Generated sample files have duplicate output paths."
        )
    for source, target in pairs:
        if not source.is_file():
            raise metadata.DataLoadError(
                "sample-generation", f"Staged sample file is missing: {source.name}"
            )
        if target.exists() and not target.is_file():
            raise metadata.DataLoadError(
                "artifact-persistence", f"Sample output target is not a file: {target}"
            )

    backup_dir = Path(tempfile.mkdtemp(prefix=".data-loader-backup-", dir=output_dir))
    backups: dict[Path, Path] = {}
    published: list[Path] = []
    preserve_backup = False
    try:
        for _source, target in pairs:
            if target.exists():
                backup = backup_dir / target.name
                os.replace(target, backup)
                backups[target] = backup
        for source, target in pairs:
            os.replace(source, target)
            published.append(target)
    except OSError as exc:
        rollback_errors: list[str] = []
        for target in reversed(published):
            try:
                if target.exists():
                    target.unlink()
            except OSError as rollback_exc:
                rollback_errors.append(str(rollback_exc))
        for target, backup in backups.items():
            try:
                if backup.exists():
                    os.replace(backup, target)
            except OSError as rollback_exc:
                rollback_errors.append(str(rollback_exc))
        preserve_backup = bool(rollback_errors)
        details = (
            f" Rollback issues: {'; '.join(rollback_errors)}. Recoverable backups remain at {backup_dir}"
            if rollback_errors
            else ""
        )
        raise metadata.DataLoadError(
            "artifact-persistence",
            f"Unable to publish the complete sample batch: {exc}.{details}",
        ) from exc
    finally:
        if not preserve_backup:
            shutil.rmtree(backup_dir, ignore_errors=True)


def generate_samples(
    business_objects: Iterable[str],
    output_dir: Path = Path.cwd(),
    config_path: Path = metadata.DEFAULT_CONFIG,
    *,
    auth_options: dict[str, Any] | None = None,
    operation: str = "create",
    output_format: str = "xlsx",
    getter: metadata.Getter = metadata.get_json,
    byte_getter: metadata.ByteGetter = metadata.get_bytes,
) -> dict[str, Any]:
    """Generate and atomically publish an ordered multi-RESTBO sample batch."""
    requested = tuple(business_objects)
    if not requested:
        raise metadata.DataLoadError(
            "sample-generation", "Supply at least one registered business object."
        )
    if len(requested) == 1:
        return generate_sample(
            requested[0],
            output_dir,
            config_path,
            auth_options=auth_options,
            operation=operation,
            output_format=output_format,
            getter=getter,
            byte_getter=byte_getter,
        )

    destination = output_dir.expanduser()
    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise metadata.DataLoadError(
            "artifact-persistence", f"Unable to create output directory {destination}: {exc}"
        ) from exc

    with tempfile.TemporaryDirectory(prefix=".data-loader-samples-", dir=destination) as root:
        staging = Path(root)
        generated = [
            generate_sample(
                business_object,
                staging,
                config_path,
                auth_options=auth_options,
                operation=operation,
                output_format=output_format,
                getter=getter,
                byte_getter=byte_getter,
            )
            for business_object in requested
        ]

        discriminators = [str(item["BusObjTopDiscriminator"]) for item in generated]
        if len(discriminators) != len(set(discriminators)):
            duplicates = sorted(
                discriminator
                for discriminator in set(discriminators)
                if discriminators.count(discriminator) > 1
            )
            raise metadata.DataLoadError(
                "sample-generation",
                "Multiple requested business objects resolved to the same discriminator: "
                + ", ".join(duplicates),
            )

        staged_files: list[tuple[Path, Path]] = []
        batch_files: list[dict[str, str]] = []
        business_object_results: list[dict[str, Any]] = []
        for item in generated:
            discriminator = str(item["BusObjTopDiscriminator"])
            files: list[dict[str, str]] = []
            sample = Path(str(item["outputPath"]))
            sample_target = destination / sample.name
            staged_files.append((sample, sample_target))
            files.append(
                {
                    "type": "DAT sample" if output_format == "dat" else "Editable sample",
                    "fileName": sample_target.name,
                    "outputPath": str(sample_target.resolve()),
                }
            )
            attribute = Path(str(item["attributeDetailsFile"]["outputPath"]))
            attribute_target = destination / attribute.name
            staged_files.append((attribute, attribute_target))
            files.append(
                {"type": "Attribute details", "fileName": attribute_target.name, "outputPath": str(attribute_target.resolve())}
            )
            if output_format == "xlsx":
                key_fields = Path(str(item["keyFieldsFile"]["outputPath"]))
                key_target = destination / key_fields.name
                staged_files.append((key_fields, key_target))
                files.append(
                    {"type": "Key fields", "fileName": key_target.name, "outputPath": str(key_target.resolve())}
                )
            batch_files.extend(
                {**file, "businessObject": discriminator} for file in files
            )
            business_object_results.append(
                {
                    "BusObjTopDiscriminator": discriminator,
                    "UIName": item.get("UIName"),
                    "sections": _section_names(item),
                    "files": files,
                }
            )

        _publish_sample_batch(staged_files, destination)
        return {
            "reportType": "sample-batch",
            "outputFormat": output_format,
            "operation": operation,
            "businessObjects": business_object_results,
            "files": batch_files,
            "uploaded": False,
        }


def generate_attribute_details(
    business_object: str,
    output_dir: Path = Path.cwd(),
    config_path: Path = metadata.DEFAULT_CONFIG,
    *,
    auth_options: dict[str, Any] | None = None,
    getter: metadata.Getter = metadata.get_json,
    byte_getter: metadata.ByteGetter = metadata.get_bytes,
) -> dict[str, Any]:
    """Create only the live-metadata attribute-details workbook."""
    config = metadata.read_config(config_path, **(auth_options or {}))
    schema = metadata.load_business_object_schema(
        business_object,
        config,
        allow_aliases=True,
        sample_attribute_lookup=True,
        getter=getter,
        byte_getter=byte_getter,
        allow_attribute_schema_fallback=True,
    )
    output_path = output_dir.expanduser() / (
        schema.discriminator + "_attribute-details.xlsx"
    )
    try:
        product_metadata = rest_sample_data.product_attribute_metadata(
            config,
            schema.discriminator,
            tuple(section.discriminator for section in schema.sections),
            getter=getter,
        )
        xlsx_sample_workbook.write_attribute_details_workbook(
            schema, output_path, product_metadata
        )
    except OSError as exc:
        raise metadata.DataLoadError(
            "sample-generation",
            f"Unable to write attribute-details workbook {output_path}: {exc}",
        ) from exc
    return {
        "reportType": "attribute-details",
        "fileName": output_path.name,
        "outputPath": str(output_path.resolve()),
        "BusObjTopDiscriminator": schema.discriminator,
        "UIName": schema.ui_name,
        "sectionCount": len(schema.sections),
        "sections": [section.discriminator for section in schema.sections],
        "sectionSummaries": [
            {
                "section": section.discriminator,
                "attributeCount": len(section.attribute_names),
            }
            for section in schema.sections
        ],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a sample Fusion Data Loader XLSX workbook or DAT file from live business-object metadata without uploading it."
    )
    parser.add_argument(
        "business_objects",
        nargs="+",
        help="One or more business-object discriminators, UI names, or template filenames.",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path.cwd(),
        help="Destination directory; XLSX output includes editable, attribute-details, and key-fields workbooks.",
    )
    parser.add_argument("--format", choices=("xlsx", "dat"), default="xlsx", help="Sample format; DAT is emitted only when explicitly requested.")
    parser.add_argument("--operation", choices=("create", "update", "delete"), default="create", help="Sample operation; defaults to create (POST). Use delete for a DELETE template.")
    parser.add_argument(
        "--attribute-details-only",
        action="store_true",
        help="Create only the attribute-details workbook; incompatible with --format dat or a non-create operation.",
    )
    parser.add_argument(
        "--populate-json",
        type=Path,
        help="JSON object of section names to row arrays. Creates populated editable, attribute-details, and key-fields XLSX workbooks.",
    )
    parser.add_argument(
        "--mapping-edit",
        action="append",
        default=[],
        metavar="SECTION/SOURCE=ATTRIBUTE|exclude",
        help="Resolve one populated field mapping after review.",
    )
    metadata.add_oauth_arguments(parser)
    parser.add_argument(
        "--inline-output",
        type=Path,
        help="Deprecated compatibility option; inline HTML rendering is disabled.",
    )
    return parser.parse_args(argv)


def parse_mapping_edits(edits: list[str]) -> dict[tuple[str, str], str | None]:
    overrides: dict[tuple[str, str], str | None] = {}
    for edit in edits:
        if "=" not in edit or "/" not in edit.split("=", 1)[0]:
            raise metadata.DataLoadError("mapping", "Mapping edits must use SECTION/SOURCE=ATTRIBUTE or SECTION/SOURCE=exclude.")
        left, target = edit.split("=", 1)
        section, source = (part.strip() for part in left.split("/", 1))
        target = target.strip()
        if not section or not source or not target:
            raise metadata.DataLoadError("mapping", "Mapping edits must contain a section, source attribute, and target or exclude.")
        overrides[(section.casefold(), source.casefold())] = None if target.casefold() == "exclude" else target
    return overrides


def load_population(path: Path) -> dict[str, list[dict[str, Any]]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise metadata.DataLoadError("mapping", f"Unable to read populated values JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise metadata.DataLoadError("mapping", "Populated values JSON must be an object keyed by section discriminator.")
    return payload


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        output_dir = args.output_dir
        if args.attribute_details_only:
            if len(args.business_objects) != 1:
                raise metadata.DataLoadError(
                    "sample-generation",
                    "--attribute-details-only accepts exactly one business object.",
                )
            if (
                args.format != "xlsx"
                or args.operation != "create"
                or args.populate_json is not None
            ):
                raise metadata.DataLoadError(
                    "sample-generation",
                    "--attribute-details-only cannot be combined with --populate-json, --format dat, or a non-create operation.",
                )
            result = generate_attribute_details(
                args.business_objects[0],
                output_dir,
                args.properties,
                auth_options=metadata.oauth_kwargs(args),
            )
        else:
            populated_rows = load_population(args.populate_json) if args.populate_json is not None else None
            if len(args.business_objects) > 1 and (
                populated_rows is not None or args.mapping_edit
            ):
                raise metadata.DataLoadError(
                    "mapping",
                    "--populate-json and --mapping-edit accept exactly one business object.",
                )
            generator = generate_sample if len(args.business_objects) == 1 else generate_samples
            generator_input: str | list[str] = (
                args.business_objects[0]
                if len(args.business_objects) == 1
                else args.business_objects
            )
            if len(args.business_objects) == 1:
                result = generator(
                    generator_input,
                    output_dir,
                    args.properties,
                    auth_options=metadata.oauth_kwargs(args),
                    operation=args.operation,
                    output_format=args.format,
                    populated_rows=populated_rows,
                    mapping_overrides=parse_mapping_edits(args.mapping_edit),
                )
            else:
                result = generator(
                    generator_input,
                    output_dir,
                    args.properties,
                    auth_options=metadata.oauth_kwargs(args),
                    operation=args.operation,
                    output_format=args.format,
                )
    except metadata.DataLoadError as exc:
        data_loader_report.emit_inline_or_markdown(
            exc,
            "error",
            args.inline_output,
            data_loader_report.render_error_report,
            stream=sys.stderr,
        )
        return 1
    if args.attribute_details_only:
        data_loader_report.emit_inline_or_markdown(
            result,
            "attribute-details",
            args.inline_output,
            data_loader_report.render_attribute_details_report,
            stream=sys.stdout,
        )
    else:
        renderer = (
            data_loader_report.render_sample_batch_report
            if result.get("reportType") == "sample-batch"
            else data_loader_report.render_sample_report
        )
        data_loader_report.emit_inline_or_markdown(
            result,
            "sample",
            args.inline_output,
            renderer,
            stream=sys.stdout,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
