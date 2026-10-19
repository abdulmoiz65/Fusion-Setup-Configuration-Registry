#!/usr/bin/env python3
"""Resolve supplied Library Goal names against VO evidence and live HDL fields."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
from typing import Any

from hdl_dat_validator import HdlDatValidationError


CROSSWALK = Path(__file__).resolve().parents[1] / "hdl-mappings" / "library-goal-vo-crosswalk.json"
TECHNICAL = {"SourceSystemOwner", "SourceSystemId", "DateFrom", "ContextName"}
TYPES = {"string", "date", "integer", "decimal"}


def _token(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def load_crosswalk() -> dict[str, Any]:
    value = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    if (not isinstance(value, dict) or value.get("component") != "ContentItem" or
            value.get("context") != "GOAL" or not isinstance(value.get("fields"), dict) or
            not isinstance(value.get("serverManaged"), dict) or
            not isinstance(value.get("joinedDisplayFields"), list)):
        raise HdlDatValidationError("VO_CROSSWALK_INVALID: Library Goal crosswalk is incomplete.")
    mapped: set[str] = set()
    for name, spec in value["fields"].items():
        if (not isinstance(name, str) or not isinstance(spec, dict) or
                not isinstance(spec.get("field"), str) or not spec["field"] or
                spec.get("type") not in TYPES or spec["field"] in mapped):
            raise HdlDatValidationError("VO_CROSSWALK_INVALID: duplicate or malformed field mapping.")
        mapped.add(spec["field"])
    return value


def _metadata_type(attribute: dict[str, Any], field: str) -> str:
    raw = str(attribute.get("DataType", "")).casefold()
    if raw in {"string", "varchar", "varchar2", "char"}:
        return "string"
    if raw in {"date", "datetime"}:
        return "date"
    if raw in {"number", "integer", "int"}:
        try:
            scale = int(attribute.get("DataScale") or 0)
        except (TypeError, ValueError) as exc:
            raise HdlDatValidationError(f"HDL_METADATA_INVALID: numeric scale for {field}.") from exc
        if field.startswith("ItemDecimal") or scale > 0:
            return "decimal"
        return "integer"
    raise HdlDatValidationError(f"MAPPING_UNSUPPORTED: {field} has no supported HDL datatype.")


def resolve_rows(
    rows: list[dict[str, Any]], catalog: dict[str, Any],
    attributes: dict[str, dict[str, Any]], template: set[str],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Normalize only supplied columns; retained catalog fields stay unchanged."""
    crosswalk = load_crosswalk()
    fields = catalog["fields"]
    candidates: dict[str, set[str]] = {}
    specifications: dict[str, dict[str, Any]] = {}

    def alias(name: str, semantic: str) -> None:
        candidates.setdefault(_token(name), set()).add(semantic)

    for semantic, spec in fields.items():
        alias(semantic, semantic)
        alias(spec["field"], semantic)
        specifications[semantic] = deepcopy(spec)
    for semantic, spec in crosswalk["fields"].items():
        if semantic in specifications:
            if specifications[semantic]["field"] != spec["field"]:
                raise HdlDatValidationError("VO_CROSSWALK_INVALID: crosswalk conflicts with the established catalog.")
            continue
        if spec["field"] in {item["field"] for item in specifications.values()}:
            raise HdlDatValidationError("VO_CROSSWALK_INVALID: crosswalk overlaps the established catalog.")
        alias(semantic, semantic)
        alias(spec["field"], semantic)
        specifications[semantic] = {**deepcopy(spec), "source": "vo-crosswalk"}
    for field, attribute in attributes.items():
        label = attribute.get("AttributeLabel")
        if field in template and isinstance(label, str) and label.strip():
            if _token(label) in {"priority", "prioritycode"}:
                alias(label, "PriorityCode")
                alias(field, "PriorityCode")
                continue
            matching = [semantic for semantic, spec in specifications.items() if spec["field"] == field]
            alias(label, matching[0] if matching else field)
    for name in TECHNICAL:
        alias(name, name)

    excluded = {_token(name) for name in crosswalk["joinedDisplayFields"]}
    excluded.update(_token(name) for name in crosswalk["serverManaged"])
    excluded.update(_token(name) for name in crosswalk["serverManaged"].values())
    normalized_rows: list[dict[str, Any]] = []
    additions: dict[str, dict[str, Any]] = {}
    for source in rows:
        if not isinstance(source, dict):
            raise HdlDatValidationError("BUSINESS_ROWS_REQUIRED: every Library Goal row must be an object.")
        normalized: dict[str, Any] = {}
        physical: set[str] = set()
        for supplied_name, supplied_value in source.items():
            if not isinstance(supplied_name, str) or not supplied_name.strip():
                raise HdlDatValidationError("MAPPING_UNSUPPORTED: blank Library Goal column.")
            key = _token(supplied_name)
            if key in excluded:
                raise HdlDatValidationError(f"MAPPING_UNSUPPORTED: {supplied_name} is not an HDL create input.")
            choices = candidates.get(key, set())
            if len(choices) > 1:
                raise HdlDatValidationError(f"MAPPING_AMBIGUOUS: {supplied_name} matches multiple HDL fields.")
            if choices:
                semantic = next(iter(choices))
            elif supplied_name in template and supplied_name in attributes:
                semantic = supplied_name
            else:
                raise HdlDatValidationError(f"MAPPING_UNSUPPORTED: {supplied_name} has no confirmed HDL field.")
            if semantic in TECHNICAL:
                field = semantic
            else:
                spec = specifications.get(semantic)
                if spec is None:
                    spec = {"field": semantic, "type": _metadata_type(attributes[semantic], semantic),
                            "source": "current-hdl-metadata"}
                    if semantic.startswith("ItemNumber"):
                        spec["requiresValueEvidence"] = True
                    specifications[semantic] = spec
                field = spec["field"]
                if semantic == "PriorityCode" and (field not in template or field not in attributes):
                    # The established priority resolver can replace ItemText2
                    # with a uniquely proved target-specific attribute.
                    normalized[semantic] = supplied_value
                    physical.add(field)
                    continue
                if field not in template or field not in attributes:
                    raise HdlDatValidationError(f"CATALOG_METADATA_MISMATCH: {supplied_name} is absent from the current ContentItem HDL template.")
                attr = attributes[field]
                if attr.get("readOnly") is True or attr.get("createable") is False or attr.get("serverGenerated") is True:
                    raise HdlDatValidationError(f"MAPPING_UNSUPPORTED: {supplied_name} is not writable for HDL create.")
                actual = _metadata_type(attr, field)
                if actual != spec["type"]:
                    raise HdlDatValidationError(f"CATALOG_METADATA_MISMATCH: datatype for {supplied_name}.")
                if semantic not in fields:
                    additions[semantic] = spec
            if semantic in normalized or field in physical:
                raise HdlDatValidationError(f"MAPPING_AMBIGUOUS: more than one supplied column resolves to {field}.")
            normalized[semantic] = supplied_value
            physical.add(field)
        normalized_rows.append(normalized)
    return normalized_rows, additions
