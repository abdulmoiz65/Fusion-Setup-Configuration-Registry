"""Thin local adapter for the shared Data Loader DAT and schema primitives.

Importing this module and exporting an existing schema need only Python's
standard library. DAT operations and loading a contract also need the normal
local ``fusionEnv.properties`` file because core resolves its repository during
import. These functions never
read authentication values, request a token, make a network call, or upload data.
Business relationships and provenance/freshness checks belong to the caller.
"""

from __future__ import annotations

import importlib
import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
LINE_BREAKS = "\r\n\v\f\x1c\x1d\x1e\x85\u2028\u2029"


class SourceContractError(ValueError):
    """The supplied local contract or DAT cannot be used safely."""


def core_modules() -> tuple[Any, Any]:
    """Lazily load unchanged core modules after the local config prerequisite."""
    scripts = REPOSITORY_ROOT / "core" / "data-loader" / "scripts"
    properties = REPOSITORY_ROOT / "core" / "auth" / "fusionEnv.properties"
    if not (scripts / "data_loader_metadata.py").is_file():
        raise SourceContractError("The shared core/data-loader scripts are missing from this repository.")
    if not properties.is_file():
        raise SourceContractError(
            "Core Data Loader requires local core/auth/fusionEnv.properties before import. "
            "Complete the repository's local configuration prerequisite; offline tests may "
            "use a blank non-secret fixture. This helper does not authenticate or call Fusion."
        )
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    for name in ("data_loader_metadata", "generate_sample_dat"):
        existing = sys.modules.get(name)
        if existing is not None and Path(existing.__file__).resolve() != (scripts / (name + ".py")).resolve():
            raise SourceContractError("A different repository's Data Loader module is already imported.")
    try:
        return (
            importlib.import_module("data_loader_metadata"),
            importlib.import_module("generate_sample_dat"),
        )
    except (ImportError, RuntimeError) as error:
        raise SourceContractError("Unable to import the repository's core Data Loader primitives.") from error


def _text(value: Any, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise SourceContractError(f"{label} must be a {'possibly empty ' if allow_empty else 'nonblank '}string.")
    if any(character in value for character in "|\x00" + LINE_BREAKS):
        raise SourceContractError(f"{label} contains a DAT delimiter, line break, or NUL.")
    return value


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SourceContractError("The contract contains a duplicate JSON object key.")
        result[key] = value
    return result


def export_contract(schema: Any) -> dict[str, Any]:
    """Serialize a schema already obtained by the routed core metadata step.

    Preserve registered raw headers/order and native attribute/component data.
    This pure exporter neither imports core nor obtains or refreshes metadata.
    The workflow persists its result through the existing artifact mechanism
    and retains environment/freshness evidence separately.
    """
    business_object = _text(schema.discriminator, "businessObject")
    if schema.schema_source not in {"UCM_TEMPLATE", "dat-template"}:
        raise SourceContractError("Only a registered UCM DAT template schema can be exported.")
    sections: dict[str, list[str]] = {}
    for section in schema.sections:
        name = _text(section.discriminator, "Section discriminator")
        if name in sections:
            raise SourceContractError("The schema contains a duplicate section discriminator.")
        headers = [_text(attribute.raw_name, "Registered header") for attribute in section.attributes]
        if not headers or len(set(section.attribute_names)) != len(headers):
            raise SourceContractError("The schema contains empty or duplicate registered headers.")
        sections[name] = headers
    if not sections or next(iter(sections)) != business_object:
        raise SourceContractError("Registered sections must begin with the root business object.")
    contract = {
        "businessObject": business_object,
        "schemaSource": schema.schema_source,
        "businessObjectId": schema.business_object_id,
        "uiName": schema.ui_name,
        "ucmContentId": schema.ucm_content_id,
        "templateFileName": schema.template_file_name,
        "sections": sections,
        "attributes": schema.attributes,
        "components": schema.components,
    }
    try:
        # JSON round-trip makes native tuples arrays and detaches nested values;
        # no caller can mutate the captured schema by editing the returned dict.
        return json.loads(json.dumps(contract, allow_nan=False))
    except (TypeError, ValueError) as error:
        raise SourceContractError("Registered schema metadata is not JSON serializable.") from error


def load_contract(path: Path | str) -> Any:
    """Load a captured registered DAT contract as core's BusinessObjectSchema.

    Required JSON keys are ``businessObject`` and ``sections``. Sections map
    discriminators to ordered header arrays; ``attributes`` maps discriminators
    to arrays of native metadata dictionaries. ``components`` is the native
    discriminator-to-metadata dictionary. This is parsing, not live verification.
    """
    try:
        contract = json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise SourceContractError("Unable to read the local contract JSON.") from error
    if not isinstance(contract, dict):
        raise SourceContractError("The contract must be a JSON object.")
    business_object = _text(contract.get("businessObject"), "businessObject")
    sections = contract.get("sections")
    if not isinstance(sections, dict) or not sections or next(iter(sections)) != business_object:
        raise SourceContractError("Contract sections must begin with the named root business object.")
    source = contract.get("schemaSource", contract.get("schema_source", "UCM_TEMPLATE"))
    if source not in {"UCM_TEMPLATE", "dat-template"}:
        raise SourceContractError("A registered UCM DAT template contract is required; synthesized schemas are unsupported.")
    lines: list[str] = []
    for discriminator, headers in sections.items():
        _text(discriminator, "Section discriminator")
        if not isinstance(headers, list) or not headers:
            raise SourceContractError("Every contract section must have an ordered, nonempty header array.")
        for header in headers:
            _text(header, "Contract header")
        lines.append("METADATA|" + discriminator + "|" + "|".join(headers))
    attributes = contract.get("attributes", {})
    components = contract.get("components", {})
    if not isinstance(attributes, dict) or not isinstance(components, dict):
        raise SourceContractError("Contract attributes and components must be objects keyed by discriminator.")
    if set(attributes) - set(sections) or set(components) - set(sections):
        raise SourceContractError("Contract metadata refers to an unknown section.")
    for values in attributes.values():
        if not isinstance(values, list) or any(not isinstance(value, dict) for value in values):
            raise SourceContractError("Each attributes entry must be an array of native metadata objects.")
        for value in values:
            _text(value.get("AttributeName"), "Native metadata AttributeName")
    if any(not isinstance(value, dict) for value in components.values()):
        raise SourceContractError("Each components entry must be a native metadata object.")
    metadata, _generator = core_modules()
    try:
        parsed = metadata.parse_template(("\n".join(lines) + "\n").encode("utf-8"))
        schema = metadata.BusinessObjectSchema(
            business_object_id=str(contract.get("businessObjectId", "")),
            discriminator=business_object,
            ui_name=str(contract.get("uiName", business_object)),
            ucm_content_id=str(contract.get("ucmContentId", "")),
            template_file_name=str(contract.get("templateFileName", business_object + ".dat")),
            sections=parsed,
            components=components,
            attributes={name: tuple(values) for name, values in attributes.items()},
            schema_source=source,
        )
        metadata.validate_source_sections(
            tuple(metadata.SourceSection(section.discriminator, section.attribute_names) for section in parsed), schema
        )
    except metadata.DataLoadError as error:
        raise SourceContractError(error.message) from error
    return schema


def read_rows(content: bytes) -> dict[str, list[dict[str, str]]]:
    """Parse exact DAT rows, retaining metadata-only sections as empty lists.

    Core validates header shape; this bounded reader adds record widths,
    section ordering, duplicate columns, and directive/action consistency.
    """
    if not isinstance(content, bytes) or not content:
        raise SourceContractError("DAT content must be nonempty bytes.")
    metadata, _generator = core_modules()
    try:
        parsed = metadata.parse_source_sections(content, source_name="absence source")
        text = content.decode("utf-8-sig")
    except (metadata.DataLoadError, UnicodeError) as error:
        raise SourceContractError("Invalid DAT section headers or encoding.") from error
    if any(character in text.replace("\r\n", "") for character in "\x00" + LINE_BREAKS.replace("\n", "")):
        raise SourceContractError("DAT content contains an embedded line separator or NUL.")
    headers = {section.discriminator: section.attributes for section in parsed}
    if any(len(set(values)) != len(values) for values in headers.values()):
        raise SourceContractError("DAT contains duplicate attribute columns.")
    result = {section.discriminator: [] for section in parsed}
    current: str | None = None
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line:
            continue
        parts = line.split("|")
        if parts[0] == "METADATA":
            if len(parts) < 3:
                raise SourceContractError(f"Malformed DAT header at line {line_number}.")
            current = parts[1]
            if current not in headers or tuple(parts[2:]) != headers[current]:
                raise SourceContractError(f"Noncanonical DAT header at line {line_number}.")
            continue
        if parts[0] not in {"MERGE", "DELETE"} or len(parts) < 2 or parts[1] != current:
            raise SourceContractError(f"Unexpected DAT record or section order at line {line_number}.")
        names = headers[current]
        if len(parts) != len(names) + 2:
            raise SourceContractError(f"DAT record width differs from its header at line {line_number}.")
        row = dict(zip(names, parts[2:]))
        expected = "DELETE" if row.get("RestAction") == "DELETE" else "MERGE"
        if parts[0] != expected:
            raise SourceContractError(f"DAT directive differs from RestAction at line {line_number}.")
        result[current].append(row)
    return result


def validate_rows(content: bytes, schema: Any) -> dict[str, list[dict[str, str]]]:
    """Validate the exact bytes against a captured schema and return their rows."""
    rows = read_rows(content)
    metadata, _generator = core_modules()
    try:
        metadata.validate_source_sections(metadata.parse_source_sections(content, source_name="absence source"), schema)
    except metadata.DataLoadError as error:
        raise SourceContractError(error.message) from error
    return rows


def render_rows(schema: Any, sections: dict[str, list[dict[str, str]]]) -> bytes:
    """Render resolved rows using core's single-row formatter, then validate bytes.

    Only supplied sections/columns are emitted. Every row in a section must
    supply the same field set: a DAT header cannot represent per-row omission.
    Columns follow the registered template order; an empty section emits its
    RestAction metadata marker.
    The caller must supply any required identity/default/date values explicitly.
    """
    if not isinstance(sections, dict) or not sections:
        raise SourceContractError("Resolved sections must be a nonempty object.")
    if schema.discriminator not in sections:
        raise SourceContractError("Resolved sections must include the root section, even when metadata-only.")
    if set(sections) - set(schema.sections_by_discriminator):
        raise SourceContractError("Resolved rows contain a section absent from the contract.")
    metadata, generator = core_modules()
    output: list[str] = []
    for section in schema.sections:
        if section.discriminator not in sections:
            continue
        records = sections[section.discriminator]
        if not isinstance(records, list) or any(not isinstance(row, dict) or not row for row in records):
            raise SourceContractError("Each resolved section must contain an array of nonempty row objects.")
        if records and any(set(row) != set(records[0]) for row in records[1:]):
            raise SourceContractError(
                f"Rows in DAT section {section.discriminator} must supply identical field sets; "
                "implicit blank values could clear unspecified fields. Resolve every field through "
                "the task's supported preparation rules. Use separately reviewed archives only for "
                "independent operations the task explicitly permits splitting; never split a new "
                "absence type hierarchy merely to bypass this check."
            )
        selected: set[str] = set()
        for row in records:
            for name, value in row.items():
                _text(name, "Resolved attribute")
                _text(value, "Resolved value", allow_empty=True)
                selected.add(name)
        if not records:
            selected = {"RestAction"}
        if selected - set(section.attribute_names):
            raise SourceContractError("Resolved row attributes are absent from the captured section contract.")
        header = tuple(name for name in section.attribute_names if name in selected)
        single_section = replace(schema, sections=(section,))
        for index, row in enumerate(records or [None]):
            values = None if row is None else tuple(row[name] for name in header)
            rendered = generator.render_dat(single_section, {section.discriminator: (header, values)})
            rendered_lines = rendered.splitlines()
            output.extend(rendered_lines if index == 0 else rendered_lines[1:])
    content = ("\n".join(output) + "\n").encode("utf-8")
    validate_rows(content, schema)
    return content
