#!/usr/bin/env python3
"""Build a review-only HRT_MANAGE_PROFILE_TYPES FSM ZIP from REST metadata.

This module performs no Fusion calls and reads no authentication material. The
calling skill must obtain complete GET responses through the shared core REST
client, keep raw responses in a safe temporary location, and pass them here.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from datetime import date
from pathlib import Path
from typing import Any


PROFILE_TYPES = {
    1: "PERSON",
    2: "JOB",
    3: "POSITION",
    4: "ORGANIZATION",
    5: "TEMPLATE",
    10: "REQUISITION",
    11: "PREREQUISITE",
    12: "GUIDE",
}
PERSON_PROFILE_TYPE_ID = 1
TEMPLATE_PROFILE_TYPE_ID = 5

METADATA_MEMBER = "ASM_SETUP_CSV_METADATA.xml"
PROFILE_MEMBER = "HRT_PROFILE_TYPES_B.csv"
SECTION_MEMBER = "ORA_HRT_PROFILE_TYPE_SECTIONS.csv"
PROPERTY_MEMBER = "ORA_HRT_PROFILE_TYPE_SECTION_PROPS.csv"
SECTION_TRANSLATION_MEMBER = "ORA_HRT_PROFILE_TYPE_SECTIONS_TRANSLATION.csv"
PROPERTY_TRANSLATION_MEMBER = "ORA_HRT_PROFILE_TYPE_SECTION_PROPS_TRANSLATION.csv"
CONTENT_SOURCE_MEMBER = "ORA_HRT_PROFILE_TYPE_CONTENT_SOURCE.csv"

BASE_MEMBERS = (
    PROFILE_MEMBER,
    SECTION_MEMBER,
    PROPERTY_MEMBER,
    SECTION_TRANSLATION_MEMBER,
    PROPERTY_TRANSLATION_MEMBER,
)

PROFILE_KEY = "HRT_PROFILE_TYPES_B.ProfileTypeCode"
SECTION_PARENT_PREFIX = "ORA_HRT_PROFILE_TYPE_SECTIONS."
PROPERTY_PARENT_PREFIX = "ORA_HRT_PROFILE_TYPE_SECTION_PROPS."
SAFE_CONTEXT = re.compile(r"^[A-Z][A-Z0-9_]{0,299}$")
SECRET_TEXT = re.compile(
    r"(?:authorization\s*[:=]|bearer\s+[a-z0-9._-]+|cookie\s*[:=]|xsrf-token)",
    flags=re.IGNORECASE,
)

DISPLAY_CODES = {
    "S": "S",
    "SUMMARY": "S",
    "D": "D",
    "DETAIL": "D",
    "DETAILS": "D",
    "B": "B",
    "BOTH": "B",
    "N": "N",
    "H": "N",
    "HIDE": "N",
    "HIDDEN": "N",
}

INPUT_TYPE_CODES = {
    "CLOB": "CLOB",
    "CHARACTER LARGE OBJECT": "CLOB",
    "DATE": "DATE",
    "DECIMAL": "DECIMAL",
    "ITEM VALUE SET": "VALUESET",
    "ITEM_VALUE_SET": "VALUESET",
    "VALUE SET": "VALUESET",
    "VALUESET": "VALUESET",
    "LIST OF VALUES": "LOV",
    "LIST_OF_VALUES": "LOV",
    "LOV": "LOV",
    "LOOKUP": "LOOKUP",
    "NUMBER": "NUMBER",
    "TEXT": "TEXT",
}


class PreparationError(ValueError):
    """A fail-closed input, metadata, or package-contract error."""

    def __init__(self, message: str, failure_class: str = "input_validation"):
        super().__init__(message)
        self.failure_class = failure_class


def require(condition: bool, message: str, failure_class: str = "input_validation") -> None:
    if not condition:
        raise PreparationError(message, failure_class)


def _nonblank(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _positive_int(value: Any, label: str) -> int:
    require(
        not isinstance(value, bool) and re.fullmatch(r"[1-9][0-9]*", _nonblank(value)) is not None,
        f"{label} must be a positive integer.",
    )
    return int(value)


def _boolean(value: Any, label: str, default: bool | None = None) -> bool:
    if value is None and default is not None:
        return default
    if isinstance(value, bool):
        return value
    text = _nonblank(value).upper()
    if text in {"Y", "YES", "TRUE", "1"}:
        return True
    if text in {"N", "NO", "FALSE", "0"}:
        return False
    raise PreparationError(f"{label} must be a boolean or Y/N value.")


def _flag(value: Any, label: str, default: bool | None = None) -> str:
    return "Y" if _boolean(value, label, default) else "N"


def _load_json(path: Path, label: str) -> Any:
    require(path.is_file(), f"{label} file does not exist: {path}")
    text = path.read_text(encoding="utf-8")
    require(not SECRET_TEXT.search(text), f"{label} appears to contain authentication or cookie material.")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise PreparationError(f"{label} is not valid JSON: {exc}") from exc


def _collection_items(payload: Any, label: str) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        rows = payload
    else:
        require(isinstance(payload, dict), f"{label} must be a JSON object or array.")
        require(
            payload.get("hasMore") is False,
            f"{label} must prove complete pagination with hasMore=false.",
            "catalog_or_metadata_mismatch",
        )
        rows = payload.get("items")
    require(isinstance(rows, list), f"{label} must contain an items array.")
    require(all(isinstance(row, dict) for row in rows), f"{label} items must be JSON objects.")
    return [dict(row) for row in rows]


def _complete_property_items(payload: Any, label: str) -> list[dict[str, Any]]:
    require(
        isinstance(payload, dict) and "items" in payload,
        f"{label} must be a complete REST collection object.",
        "catalog_or_metadata_mismatch",
    )
    return _collection_items(payload, label)


def _profile_items(payload: Any) -> list[dict[str, Any]]:
    if payload is None:
        return []
    if isinstance(payload, dict) and "items" not in payload:
        return [dict(payload)]
    return _collection_items(payload, "profile types response")


def validate_request(request: Any) -> dict[str, Any]:
    require(isinstance(request, dict), "Request must be a JSON object.")
    allowed = {
        "target_profile_type_id",
        "target_profile_type_code",
        "template_name",
        "content_type_id",
        "content_type_context_name",
        "section_name",
        "section_context",
        "description",
        "active",
        "approval_required",
        "default_section",
        "section_item_required",
        "display_order",
        "section_layout",
        "linkedin_enabled",
        "skill_recommend_enabled",
        "person_section_id",
        "person_section_context",
        "property_overrides",
        "subscribers",
        "translations",
        "source_language",
    }
    unknown = sorted(set(request) - allowed)
    require(not unknown, "Unsupported request fields: " + ", ".join(unknown))

    result = dict(request)
    profile_type_id = _positive_int(result.get("target_profile_type_id"), "target_profile_type_id")
    profile_type_code = _nonblank(result.get("target_profile_type_code")).upper()
    require(PROFILE_TYPES.get(profile_type_id) == profile_type_code, "The target profile type ID/code pair is invalid.")

    for field, maximum in (("template_name", 240), ("section_name", 240), ("description", 4000)):
        value = _nonblank(result.get(field))
        require(value, f"{field} is required.")
        require(len(value) <= maximum, f"{field} exceeds {maximum} characters.")
        result[field] = value

    context = _nonblank(result.get("section_context")).upper()
    require(SAFE_CONTEXT.fullmatch(context) is not None, "section_context must use uppercase letters, digits, and underscores.")
    result["section_context"] = context

    if result.get("content_type_id") is not None:
        result["content_type_id"] = _positive_int(result["content_type_id"], "content_type_id")
    if result.get("content_type_context_name") is not None:
        content_context = _nonblank(result["content_type_context_name"]).upper()
        require(SAFE_CONTEXT.fullmatch(content_context) is not None, "content_type_context_name is invalid.")
        result["content_type_context_name"] = content_context

    for field, default in (
        ("active", True),
        ("approval_required", False),
        ("default_section", False),
        ("section_item_required", False),
        ("linkedin_enabled", False),
        ("skill_recommend_enabled", False),
    ):
        result[field] = _boolean(result.get(field), field, default)

    if result.get("display_order") is not None:
        result["display_order"] = _positive_int(result["display_order"], "display_order")
    result["section_layout"] = _nonblank(result.get("section_layout") or "TABLE").upper()
    require(result["section_layout"] in {"TABLE", "LIST"}, "section_layout must be TABLE or LIST.")

    if profile_type_id != PERSON_PROFILE_TYPE_ID:
        require(
            result.get("person_section_id") is not None or _nonblank(result.get("person_section_context")),
            "A non-Person section requires person_section_id or person_section_context.",
        )
        if result.get("person_section_id") is not None:
            result["person_section_id"] = _positive_int(result["person_section_id"], "person_section_id")
        if result.get("person_section_context") is not None:
            parent_context = _nonblank(result["person_section_context"]).upper()
            require(SAFE_CONTEXT.fullmatch(parent_context) is not None, "person_section_context is invalid.")
            result["person_section_context"] = parent_context

    overrides = result.get("property_overrides", [])
    require(isinstance(overrides, list), "property_overrides must be an array.")
    seen_overrides: set[tuple[str, str]] = set()
    for override in overrides:
        require(isinstance(override, dict), "Each property override must be an object.")
        allowed_override = {"field_name", "column_name", "display", "required", "custom_label", "default_value"}
        require(not set(override) - allowed_override, "Unsupported property override field.")
        field_name = _nonblank(override.get("field_name")).upper()
        require(field_name, "Each property override requires field_name.")
        column_name = _nonblank(override.get("column_name")).upper()
        key = (field_name, column_name)
        require(key not in seen_overrides, f"Duplicate property override for {field_name}/{column_name or '*'}.")
        seen_overrides.add(key)
        override["field_name"] = field_name
        if column_name:
            override["column_name"] = column_name
        if "display" in override:
            require(_display_code(override["display"]), f"Unsupported display value for {field_name}.")
        if "required" in override:
            override["required"] = _boolean(override["required"], f"{field_name}.required")
        if "custom_label" in override:
            require(len(_nonblank(override["custom_label"])) <= 240, f"Custom label for {field_name} exceeds 240 characters.")

    subscribers = result.get("subscribers", [])
    require(isinstance(subscribers, list), "subscribers must be an array.")
    require(all(isinstance(value, str) and value.strip() for value in subscribers), "Each subscriber must be a nonempty name or code.")
    require(len(subscribers) == len(set(subscribers)), "Duplicate subscriber request.")

    translations = result.get("translations", [])
    require(isinstance(translations, list), "translations must be an array.")
    for translation in translations:
        require(isinstance(translation, dict), "Each translation must be an object.")
        require(set(translation) <= {"language", "source_language", "name", "description"}, "Unsupported translation field.")
        language = _nonblank(translation.get("language")).upper()
        require(language, "Each translation requires language.")
        translation["language"] = language
        if "source_language" in translation:
            translation["source_language"] = _nonblank(translation["source_language"]).upper()
    result["source_language"] = _nonblank(result.get("source_language") or "US").upper()
    return result


def _display_code(value: Any) -> str:
    return DISPLAY_CODES.get(_nonblank(value).upper(), "")


def _input_type_code(row: dict[str, Any]) -> str:
    saw_value = False
    for field in ("InputType", "InputFieldTypeCode", "InputFieldTypeMeaning"):
        value = _nonblank(row.get(field)).upper()
        saw_value = saw_value or bool(value)
        if value in INPUT_TYPE_CODES:
            return INPUT_TYPE_CODES[value]
    if not saw_value:
        return ""
    raise PreparationError(
        f"Property {_nonblank(row.get('FieldName')) or '<unknown>'} has no supported input field type.",
        "catalog_or_metadata_mismatch",
    )


def select_template(rows: list[dict[str, Any]], request: dict[str, Any]) -> dict[str, Any]:
    matches = [row for row in rows if row.get("Name") == request["template_name"]]
    if request.get("content_type_id") is not None:
        matches = [row for row in matches if str(row.get("ContentTypeId")) == str(request["content_type_id"])]
    matches = [
        row
        for row in matches
        if row.get("TemplateFlag") is None or _boolean(row.get("TemplateFlag"), "TemplateFlag")
    ]
    require(len(matches) == 1, f"Template match must be exact and unique; found {len(matches)}.", "catalog_or_metadata_mismatch")
    template = matches[0]
    _positive_int(template.get("SectionId"), "Template SectionId")
    _positive_int(template.get("ContentTypeId"), "Template ContentTypeId")
    if template.get("ProfileTypeId") is not None:
        require(int(template["ProfileTypeId"]) == TEMPLATE_PROFILE_TYPE_ID, "Template row is not owned by profile type 5.", "catalog_or_metadata_mismatch")
    return template


def _content_context(request: dict[str, Any], template: dict[str, Any], properties: list[dict[str, Any]]) -> str:
    candidates = [
        request.get("content_type_context_name"),
        template.get("ContentTypeContextName"),
        template.get("ContextName"),
    ]
    candidates.extend(row.get("ContextName") for row in properties)
    values = {_nonblank(value).upper() for value in candidates if _nonblank(value)}
    require(len(values) == 1, "Content type context is missing or ambiguous; provide content_type_context_name.", "catalog_or_metadata_mismatch")
    context = values.pop()
    require(SAFE_CONTEXT.fullmatch(context) is not None, "Resolved content type context is invalid.", "catalog_or_metadata_mismatch")
    return context


def select_person_section(
    rows: list[dict[str, Any]], request: dict[str, Any], template: dict[str, Any]
) -> dict[str, Any]:
    matches = rows
    if request.get("person_section_id") is not None:
        matches = [row for row in matches if str(row.get("SectionId")) == str(request["person_section_id"])]
    if request.get("person_section_context"):
        matches = [row for row in matches if row.get("SectionContext") == request["person_section_context"]]
    matches = [row for row in matches if str(row.get("ContentTypeId")) == str(template["ContentTypeId"])]
    require(len(matches) == 1, f"Active Person source match must be exact and unique; found {len(matches)}.", "catalog_or_metadata_mismatch")
    parent = matches[0]
    if parent.get("ProfileTypeId") is not None:
        require(
            int(parent["ProfileTypeId"]) == PERSON_PROFILE_TYPE_ID,
            "The selected parent row is not owned by the Person profile type.",
            "catalog_or_metadata_mismatch",
        )
    require(_boolean(parent.get("ActiveFlag"), "Person ActiveFlag"), "The selected Person content section is inactive.", "catalog_or_metadata_mismatch")
    if parent.get("TemplateBasedSectionFlag") is not None:
        require(_boolean(parent["TemplateBasedSectionFlag"], "Person TemplateBasedSectionFlag"), "The selected Person section is not template-based.", "catalog_or_metadata_mismatch")
    _positive_int(parent.get("SectionId"), "Person SectionId")
    require(_nonblank(parent.get("SectionContext")), "The Person source lacks SectionContext.", "catalog_or_metadata_mismatch")
    return parent


def validate_no_duplicate(
    rows: list[dict[str, Any]],
    request: dict[str, Any],
    template: dict[str, Any],
    parent: dict[str, Any] | None,
) -> None:
    for row in rows:
        if row.get("ProfileTypeId") is not None:
            require(
                int(row["ProfileTypeId"]) == request["target_profile_type_id"],
                "Target sections response contains a different profile type.",
                "catalog_or_metadata_mismatch",
            )
        if row.get("SectionContext") == request["section_context"]:
            raise PreparationError("The target profile type already contains the requested SectionContext.", "catalog_or_metadata_mismatch")
        if row.get("SectionName", row.get("Name")) == request["section_name"] and str(row.get("ContentTypeId")) == str(template["ContentTypeId"]):
            raise PreparationError("The target profile type already contains the requested name/template combination.", "catalog_or_metadata_mismatch")
        if parent is not None:
            same_parent_id = str(row.get("ParentSectionId")) == str(parent["SectionId"])
            same_parent_context = _nonblank(row.get("ParentSectionSectionContext")) == _nonblank(parent.get("SectionContext"))
            if same_parent_id or same_parent_context:
                raise PreparationError(
                    "This Person content section is already represented in the target profile type.",
                    "catalog_or_metadata_mismatch",
                )


def select_properties(
    rows: list[dict[str, Any]], request: dict[str, Any]
) -> list[dict[str, Any]]:
    allowed_sources = {"P", "B"} if request["target_profile_type_id"] == PERSON_PROFILE_TYPE_ID else {"M", "B"}
    selected: list[dict[str, Any]] = []
    keys: set[tuple[str, str, str, str]] = set()
    for row in rows:
        source = _nonblank(row.get("SourceProfileTypeCode")).upper()
        if source not in allowed_sources:
            continue
        field_name = _nonblank(row.get("FieldName")).upper()
        column_name = _nonblank(row.get("ColumnName")).upper()
        if column_name in {"COUNTRY_ID", "STATE_PROVINCE_ID"} or field_name == "NEXT_MOVE_LOCATION2":
            continue
        require(field_name and column_name, "Every eligible property requires FieldName and ColumnName.", "catalog_or_metadata_mismatch")
        key = (field_name, column_name, source, _nonblank(row.get("SourceCode")))
        require(key not in keys, f"Duplicate eligible property metadata for {field_name}/{column_name}.", "catalog_or_metadata_mismatch")
        keys.add(key)
        normalized = dict(row)
        normalized["FieldName"] = field_name
        normalized["ColumnName"] = column_name
        normalized["SourceProfileTypeCode"] = source
        normalized["InputFieldTypeCode"] = _input_type_code(row)
        display = _display_code(row.get("DisplayModeCode") or row.get("DisplayModeMeaning"))
        require(display, f"Property {field_name} has no supported display mode.", "catalog_or_metadata_mismatch")
        normalized["DisplayFlag"] = display
        selected.append(normalized)
    require(selected, "No eligible properties remain for the requested profile type.", "catalog_or_metadata_mismatch")

    # Catalog-backed templates can expose both mutually exclusive leading
    # attributes. Fusion identifies catalog-based entry with
    # CONTENT_ITEM_ID/VALUESET and can leave the template-specific free-form
    # name alternative (for example NAME or DEGREE_NAME) without an input
    # type. Preserve that blank alternative only when the exact catalog
    # property is present with the same display placement and label key.
    blank_input_rows = [row for row in selected if not row["InputFieldTypeCode"]]
    for row in blank_input_rows:
        expected_pair = (
            ("CONTENT_ITEM_ID", "VALUESET")
            if row["FieldName"] == "NAME" or row["FieldName"].endswith("_NAME")
            else None
        )
        require(
            expected_pair is not None,
            f"Property {row['FieldName']} has no supported input field type.",
            "catalog_or_metadata_mismatch",
        )
        pair_name, pair_type = expected_pair
        pair_matches = [
            candidate
            for candidate in selected
            if candidate["FieldName"] == pair_name
            and candidate["SourceProfileTypeCode"] == row["SourceProfileTypeCode"]
            and candidate["DisplayFlag"] == row["DisplayFlag"]
            and _nonblank(candidate.get("DisplayOrder")) == _nonblank(row.get("DisplayOrder"))
            and _nonblank(candidate.get("AttributeLabelKey"))
            == _nonblank(row.get("AttributeLabelKey"))
        ]
        require(
            len(pair_matches) == 1 and pair_matches[0]["InputFieldTypeCode"] == pair_type,
            f"Property {row['FieldName']} has a blank input type without one exact selected leading-attribute alternative.",
            "catalog_or_metadata_mismatch",
        )

    overrides = list(request.get("property_overrides", []))
    matched_overrides: set[int] = set()
    for row in selected:
        candidates = [
            (index, override)
            for index, override in enumerate(overrides)
            if override["field_name"] == row["FieldName"]
            and (not override.get("column_name") or override["column_name"] == row["ColumnName"])
        ]
        require(len(candidates) <= 1, f"Property override is ambiguous for {row['FieldName']}.")
        if candidates:
            index, override = candidates[0]
            matched_overrides.add(index)
            if "display" in override:
                row["DisplayFlag"] = _display_code(override["display"])
            if "required" in override:
                row["RequiredFlag"] = override["required"]
            if "custom_label" in override:
                row["CustomLabel"] = _nonblank(override["custom_label"])
            if "default_value" in override:
                row["DefaultValue"] = override["default_value"]
    unmatched = [overrides[index]["field_name"] for index in range(len(overrides)) if index not in matched_overrides]
    require(not unmatched, "Property overrides did not match eligible metadata: " + ", ".join(unmatched), "catalog_or_metadata_mismatch")
    def order_key(row: dict[str, Any]) -> tuple[int, str, str]:
        value = row.get("DisplayOrder")
        if value in (None, ""):
            order = 999999
        else:
            order = _positive_int(value, f"{row['FieldName']}.DisplayOrder")
        return order, row["FieldName"], row["ColumnName"]

    return sorted(selected, key=order_key)


def select_model_properties(
    template_rows: list[dict[str, Any]],
    person_section_rows: list[dict[str, Any]],
    request: dict[str, Any],
) -> list[dict[str, Any]]:
    """Merge model-only template rows with base rows from the selected Person section."""
    require(
        request["target_profile_type_id"] != PERSON_PROFILE_TYPE_ID,
        "Two-source model property resolution applies only to non-Person targets.",
    )

    invalid_template = [
        _nonblank(row.get("SourceProfileTypeCode")).upper()
        for row in template_rows
        if _nonblank(row.get("SourceProfileTypeCode")).upper() != "M"
    ]
    require(
        not invalid_template,
        "Model template properties response must contain only SourceProfileTypeCode M rows.",
        "catalog_or_metadata_mismatch",
    )

    invalid_person = [
        row
        for row in person_section_rows
        if _nonblank(row.get("SourceProfileTypeCode")).upper() != "B"
        or _nonblank(row.get("SourceCode"))
    ]
    require(
        not invalid_person,
        "Selected Person section properties response must contain only SourceProfileTypeCode B rows with null SourceCode.",
        "catalog_or_metadata_mismatch",
    )

    return select_properties([*person_section_rows, *template_rows], request)


def _safe_zip(source: Path) -> zipfile.ZipFile:
    require(source.is_file(), f"Source template ZIP does not exist: {source}")
    require(zipfile.is_zipfile(source), "Source template is not a valid ZIP.")
    archive = zipfile.ZipFile(source)
    names = archive.namelist()
    require(len(names) == len(set(names)), "Source template ZIP contains duplicate member names.")
    for name in names:
        path = Path(name)
        require(not path.is_absolute() and ".." not in path.parts, f"Unsafe ZIP member: {name}")
    require(archive.testzip() is None, "Source template ZIP failed its CRC check.")
    required = {METADATA_MEMBER, *BASE_MEMBERS}
    missing = sorted(required - set(names))
    require(not missing, "Source template ZIP is missing: " + ", ".join(missing), "catalog_or_metadata_mismatch")
    metadata = archive.read(METADATA_MEMBER)
    require(b"HRT_MANAGE_PROFILE_TYPES" in metadata, "Metadata marker is not for HRT_MANAGE_PROFILE_TYPES.", "catalog_or_metadata_mismatch")
    return archive


def _read_csv(archive: zipfile.ZipFile, member: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        text = archive.read(member).decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise PreparationError(f"{member} is not UTF-8 CSV.", "catalog_or_metadata_mismatch") from exc
    reader = csv.DictReader(io.StringIO(text))
    header = reader.fieldnames
    require(header is not None and len(header) == len(set(header)), f"{member} has an invalid header.", "catalog_or_metadata_mismatch")
    return list(header), list(reader)


def _validate_empty_native_template(archive: zipfile.ZipFile) -> None:
    csv_members = [name for name in archive.namelist() if name.lower().endswith(".csv")]
    require(csv_members, "Source template ZIP contains no CSV members.", "catalog_or_metadata_mismatch")
    nonempty = []
    for member in csv_members:
        _header, rows = _read_csv(archive, member)
        if rows:
            nonempty.append(member)
    require(
        not nonempty,
        "Source template ZIP must be a native template/spec export with header-only CSVs; "
        "data rows were found in: " + ", ".join(sorted(nonempty)),
        "catalog_or_metadata_mismatch",
    )


def _blank_row(header: list[str]) -> dict[str, Any]:
    return {field: "" for field in header}


def _set(row: dict[str, Any], values: dict[str, Any], member: str) -> dict[str, Any]:
    missing = sorted(set(values) - set(row))
    require(not missing, f"{member} source header is missing required columns: " + ", ".join(missing), "catalog_or_metadata_mismatch")
    for key, value in values.items():
        row[key] = "" if value is None else value
    return row


def _parent_section_keys(code: str, context: str, section_context: str) -> dict[str, str]:
    return {
        PROFILE_KEY: code,
        SECTION_PARENT_PREFIX + "ContentTypeContextName": context,
        SECTION_PARENT_PREFIX + "ProfileTypeCode": code,
        SECTION_PARENT_PREFIX + "SectionContext": section_context,
    }


def _base_section_keys(code: str, context: str, section_context: str) -> dict[str, str]:
    return {
        PROFILE_KEY: code,
        "ContentTypeContextName": context,
        "ProfileTypeCode": code,
        "SectionContext": section_context,
    }


def _property_keys(code: str, context: str, section_context: str, property_row: dict[str, Any]) -> dict[str, str]:
    return {
        **_parent_section_keys(code, context, section_context),
        "ProfileTypeCode": code,
        "ContextName": context,
        "ColumnName": property_row["ColumnName"],
        "SectionContext": section_context,
        "FieldName": property_row["FieldName"],
    }


def _display_order(request: dict[str, Any], target_rows: list[dict[str, Any]]) -> int:
    if request.get("display_order") is not None:
        return int(request["display_order"])
    values = []
    for row in target_rows:
        value = row.get("DisplayOrder")
        if not isinstance(value, bool) and re.fullmatch(r"[0-9]+", _nonblank(value)):
            values.append(int(value))
    return max(values, default=0) + 1


def _profile_date(value: Any, label: str) -> str:
    text = _nonblank(value)
    require(re.fullmatch(r"[0-9]{4}[-/][0-9]{2}[-/][0-9]{2}", text) is not None, f"{label} must be YYYY-MM-DD or YYYY/MM/DD.", "catalog_or_metadata_mismatch")
    normalized = text.replace("-", "/")
    try:
        date.fromisoformat(normalized.replace("/", "-"))
    except ValueError as exc:
        raise PreparationError(f"{label} must be a valid calendar date.", "catalog_or_metadata_mismatch") from exc
    return normalized


def _profile_usage_code(code: str, profile_type_id: int, metadata: dict[str, Any]) -> str:
    require(
        PROFILE_TYPES.get(profile_type_id) == code,
        "Cannot resolve ProfileUsageCode for an invalid profile type ID/code pair.",
        "catalog_or_metadata_mismatch",
    )
    expected = "P" if profile_type_id == PERSON_PROFILE_TYPE_ID else "M"
    for field in ("ProfileUsageCode", "UsageCode"):
        supplied = _nonblank(metadata.get(field))
        require(
            not supplied or supplied == expected,
            f"{field} for {code} must be {expected}; supplied value conflicts with the profile classification.",
            "catalog_or_metadata_mismatch",
        )
    return expected


def _profile_row(
    header: list[str],
    rows: list[dict[str, str]],
    code: str,
    profile_type_id: int,
    profile_metadata: list[dict[str, Any]],
) -> dict[str, Any]:
    matches = [row for row in rows if row.get("ProfileTypeCode") == code]
    require(len(matches) <= 1, f"Source template ZIP contains multiple {code} profile type rows.", "catalog_or_metadata_mismatch")
    if matches:
        result = {field: matches[0].get(field, "") for field in header}
        _set(result, {"ProfileUsageCode": _profile_usage_code(code, profile_type_id, matches[0])}, PROFILE_MEMBER)
    else:
        metadata_matches = [
            row
            for row in profile_metadata
            if str(row.get("ProfileTypeId")) == str(profile_type_id)
            and _nonblank(row.get("ProfileTypeCode")).upper() == code
        ]
        require(
            len(metadata_matches) == 1,
            f"The source ZIP lacks {code}; source-backed owner metadata must resolve it exactly once.",
            "catalog_or_metadata_mismatch",
        )
        metadata = metadata_matches[0]
        usage_code = _profile_usage_code(code, profile_type_id, metadata)
        aliases = {
            "ProfileStatusCode": ("ProfileStatusCode", "StatusCode", "Status"),
            "ProfileUsageCode": ("ProfileUsageCode", "UsageCode"),
            "PidApprovalFlag": ("PidApprovalFlag", "ApprovalRequiredFlag"),
            "AutoCreateFlag": ("AutoCreateFlag", "AutoCreatePersonProfileFlag"),
        }
        result = _blank_row(header)
        for field in header:
            if field == "AutoCreateFlag" and usage_code == "M":
                # Model profiles never inherit Person auto-create settings.
                continue
            value = None
            for source_field in aliases.get(field, (field,)):
                if source_field in metadata:
                    value = metadata[source_field]
                    break
            if value is None:
                continue
            if field in {"DateFrom", "DateTo"}:
                value = _profile_date(value, field)
            elif field.endswith("Flag"):
                value = _flag(value, field)
            result[field] = value
        _set(result, {"ProfileUsageCode": usage_code}, PROFILE_MEMBER)
        # The owning Profile Type row is import data, not a proven key-only
        # reference. Missing REST fields do not establish safe blank semantics.
        required_metadata = {
            "Description", "Summary", "ProfileStatusCode", "ProfileUsageCode",
            "DateFrom", "DateTo", "PidApprovalFlag", "ModuleId", "AutoCreateFlag",
        }
        if usage_code == "M":
            required_metadata.discard("AutoCreateFlag")
        missing = sorted(field for field in required_metadata if field in header and not _nonblank(result.get(field)))
        require(
            not missing,
            "Owning Profile Type metadata is incomplete: " + ", ".join(missing)
            + ". Supply complete REST metadata or an approved unchanged FSM current-data export reference; do not import the reference archive.",
            "catalog_or_metadata_mismatch",
        )
        if result.get("DateFrom") and result.get("DateTo"):
            require(
                result["DateFrom"] <= result["DateTo"],
                "Owning Profile Type DateFrom must not be after DateTo.",
                "catalog_or_metadata_mismatch",
            )
        _set(
            result,
            {
                "ProfileTypeCode": code,
                "ViewInstanceName": "ProfileType",
                "GroupingKey": code,
            },
            PROFILE_MEMBER,
        )
    if profile_type_id != PERSON_PROFILE_TYPE_ID and "AutoCreateFlag" in result:
        result["AutoCreateFlag"] = ""
    if "ProfileTypeId" in result:
        result["ProfileTypeId"] = ""
    if "GroupingKey" in result:
        result["GroupingKey"] = code
    return result


def _section_row(
    header: list[str],
    request: dict[str, Any],
    context: str,
    parent: dict[str, Any] | None,
    order: int,
) -> dict[str, Any]:
    code = request["target_profile_type_code"]
    section_context = request["section_context"]
    values: dict[str, Any] = {
        **_base_section_keys(code, context, section_context),
        "ViewInstanceName": "ProfileTypeSection",
        "GroupingKey": f"{code},{context},{section_context}",
        "ContentTypeRelationId": "",
        "SectionItemReqdFlag": _flag(request["section_item_required"], "section_item_required"),
        "ApprovalRequiredFlag": _flag(request["approval_required"], "approval_required"),
        "ModuleId": "",
        "ParentSectionProfileTypeCode": "PERSON" if parent else "",
        "ParentSectionContextName": context if parent else "",
        "DisplayOrder": order,
        "SectionLayout": request["section_layout"],
        "ActiveFlag": _flag(request["active"], "active"),
        "AnalyticPriority": "",
        "AnalyticPrioritySourceCode": "LATEST",
        "DffContextName": section_context,
        "Name": request["section_name"],
        "TemplateFlag": "",
        "Description": request["description"],
        "DefaultFlag": _flag(request["default_section"], "default_section"),
        "SecurityContext": section_context,
        "TemplateBasedSectionFlag": "Y",
        "LinkedinEnabledFlag": _flag(request["linkedin_enabled"], "linkedin_enabled"),
        "SkillRecommendEnabledFlag": _flag(request["skill_recommend_enabled"], "skill_recommend_enabled"),
        "ParentSectionSectionContext": parent.get("SectionContext", "") if parent else "",
        "SectionId": "",
        "ProfileTypeId": "",
        # Leave the generated surrogate relationship unset.  A literal
        # ``#null`` prevents the FSM importer from propagating the newly
        # resolved section identity to ProfileTypeSectionProperty children.
        "ContentTypeId": "",
        "ParentSectionId": "",
        "QualifierSetId1": "#null",
        "QualifierSetId2": "#null",
        "ParentSectionContentTypeId": "",
    }
    return _set(_blank_row(header), values, SECTION_MEMBER)


def _property_row(
    header: list[str], request: dict[str, Any], context: str, metadata: dict[str, Any]
) -> dict[str, Any]:
    code = request["target_profile_type_code"]
    section_context = request["section_context"]
    label = _nonblank(metadata.get("AttributeDisplayLabel") or metadata.get("Label"))
    require(label, f"Property {metadata['FieldName']} has no display label.", "catalog_or_metadata_mismatch")
    default_value = metadata.get("DefaultValue")
    if default_value is None:
        default_value = metadata.get("DefaultListValue")
    required = metadata.get("RequiredFlag")
    required_flag = _flag(required, f"{metadata['FieldName']}.RequiredFlag", False)
    custom_label = _nonblank(metadata.get("CustomLabel"))
    values: dict[str, Any] = {
        **_property_keys(code, context, section_context, metadata),
        "ViewInstanceName": "ProfileTypeSectionProperty",
        "GroupingKey": f"{code},{context},{section_context},{metadata['FieldName']}",
        "ValueSetName": metadata.get("ValueSetName") or "",
        "PropertySource": metadata["SourceProfileTypeCode"],
        "RequiredFlag": required_flag,
        "DisplayFlag": metadata["DisplayFlag"],
        "DefaultValue": default_value,
        "ModuleId": "",
        "AttributeLabel": label,
        "SearchFlag": _flag(metadata.get("SearchFlag"), f"{metadata['FieldName']}.SearchFlag", False),
        "ViewAttrbName": metadata.get("ViewAttrbName") or metadata.get("ViewAttributeName") or "",
        "SGUID": "",
        "AttributeLabelKey": metadata.get("AttributeLabelKey") or "",
        "SourceCode": metadata.get("SourceCode") or "",
        "InputFieldTypeCode": metadata["InputFieldTypeCode"],
        "DisplayOrder": metadata.get("DisplayOrder") or "",
        "ContentValueSetCode": metadata.get("ContentValueSetCode") or "",
        "CustomLabel": custom_label,
        "SectionPropId": "",
        "SectionId": "",
        "ProfileTypeId": "",
        "ContentTypeId": "",
    }
    return _set(_blank_row(header), values, PROPERTY_MEMBER)


def _translations(request: dict[str, Any]) -> list[dict[str, str]]:
    translations = request.get("translations") or [
        {
            "language": request["source_language"],
            "source_language": request["source_language"],
            "name": request["section_name"],
            "description": request["description"],
        }
    ]
    result = []
    for row in translations:
        result.append(
            {
                "language": row["language"],
                "source_language": row.get("source_language") or request["source_language"],
                "name": row.get("name") or request["section_name"],
                "description": row.get("description") or request["description"],
            }
        )
    require(len({row["language"] for row in result}) == len(result), "Duplicate translation language.")
    require(request["source_language"] in {row["language"] for row in result}, "translations must include source_language.")
    return result


def _section_translation_rows(
    header: list[str], request: dict[str, Any], context: str
) -> list[dict[str, Any]]:
    code = request["target_profile_type_code"]
    section_context = request["section_context"]
    result = []
    for translation in _translations(request):
        values = {
            **_parent_section_keys(code, context, section_context),
            "ViewInstanceName": "ProfileTypeSectionTranslation",
            "GroupingKey": section_context,
            "Description": translation["description"],
            "Language": translation["language"],
            "Name": translation["name"],
            "SourceLang": translation["source_language"],
            "SectionContext": section_context,
            "SectionId": "",
        }
        result.append(_set(_blank_row(header), values, SECTION_TRANSLATION_MEMBER))
    return result


def _property_translation_rows(
    header: list[str],
    request: dict[str, Any],
    context: str,
    properties: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    code = request["target_profile_type_code"]
    section_context = request["section_context"]
    result = []
    for metadata in properties:
        label = _nonblank(metadata.get("CustomLabel") or metadata.get("AttributeDisplayLabel") or metadata.get("Label"))
        base_keys = {
            **_parent_section_keys(code, context, section_context),
            PROPERTY_PARENT_PREFIX + "ProfileTypeCode": code,
            PROPERTY_PARENT_PREFIX + "ContextName": context,
            PROPERTY_PARENT_PREFIX + "ColumnName": metadata["ColumnName"],
            PROPERTY_PARENT_PREFIX + "SectionContext": section_context,
            PROPERTY_PARENT_PREFIX + "FieldName": metadata["FieldName"],
        }
        for translation in _translations(request):
            values = {
                **base_keys,
                "ViewInstanceName": "ProfileTypeSectionPropertyTranslation",
                "GroupingKey": f"{code},{context},{section_context},{metadata['FieldName']}",
                "Language": translation["language"],
                "SourceLang": translation["source_language"],
                "AttributeLabel": label,
                "FieldName": metadata["FieldName"],
                "ProfileTypeCode": code,
                "ContextName": context,
                "SectionContext": section_context,
                "SourceCode": metadata.get("SourceCode") or "",
                "SectionPropId": "",
                "SectionId": "",
                "ProfileTypeId": "",
                "ContentTypeId": "",
            }
            result.append(_set(_blank_row(header), values, PROPERTY_TRANSLATION_MEMBER))
    return result


def _subscriber_matches(row: dict[str, Any], requested: str) -> bool:
    return requested in {
        _nonblank(row.get("SourceCode")),
        _nonblank(row.get("SubscriberCode")),
        _nonblank(row.get("Name")),
        _nonblank(row.get("SourceName")),
        _nonblank(row.get("Meaning")),
        _nonblank(row.get("DisplayName")),
        _nonblank(row.get("SourceDescription")),
    }


def _content_source_rows(
    header: list[str],
    request: dict[str, Any],
    context: str,
    subscriber_catalog: list[dict[str, Any]],
    content_type_id: int,
) -> list[dict[str, Any]]:
    code = request["target_profile_type_code"]
    section_context = request["section_context"]
    result = []
    for requested in request.get("subscribers", []):
        matches = [row for row in subscriber_catalog if _subscriber_matches(row, requested)]
        require(len(matches) == 1, f"Subscriber {requested!r} must resolve exactly once; found {len(matches)}.", "catalog_or_metadata_mismatch")
        source = matches[0]
        source_code = _nonblank(source.get("SourceCode") or source.get("SubscriberCode"))
        source_id = _positive_int(source.get("SourceId"), f"Subscriber {requested} SourceId")
        if source.get("ContentTypeId") is not None:
            require(
                _positive_int(source.get("ContentTypeId"), f"Subscriber {requested} ContentTypeId")
                == content_type_id,
                f"Subscriber {requested!r} is scoped to a different content type.",
                "catalog_or_metadata_mismatch",
            )
        values = {
            **_parent_section_keys(code, context, section_context),
            "SourceCode": source_code,
            "SectionContext": section_context,
            "ViewInstanceName": "ContentSourceRelationship1",
            "GroupingKey": f"{source_id},{content_type_id},{section_context}",
            "SourceId": source_id,
            "ContentTypeId": content_type_id,
            "ModuleId": "",
            "SyncSectionPropFlag": "",
            "ContentSourceRlatId": "",
        }
        result.append(_set(_blank_row(header), values, CONTENT_SOURCE_MEMBER))
    return result


def _csv_bytes(header: list[str], rows: list[dict[str, Any]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=header, extrasaction="raise", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o600 << 16
    return info


def prepare(
    request: dict[str, Any],
    templates_payload: Any,
    properties_payload: Any,
    target_sections_payload: Any,
    source_template_zip: Path,
    output: Path,
    *,
    profile_types_payload: Any | None = None,
    person_sections_payload: Any | None = None,
    person_properties_payload: Any | None = None,
    subscriber_payload: Any | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    request = validate_request(request)
    templates = _collection_items(templates_payload, "template response")
    profile_types = _profile_items(profile_types_payload)
    property_metadata = _complete_property_items(properties_payload, "property response")
    target_sections = _collection_items(target_sections_payload, "target sections response")
    template = select_template(templates, request)
    if request.get("content_type_id") is None:
        request["content_type_id"] = int(template["ContentTypeId"])
    parent = None
    if request["target_profile_type_id"] == PERSON_PROFILE_TYPE_ID:
        properties = select_properties(property_metadata, request)
        person_base_property_count = None
        model_property_count = None
    else:
        require(person_sections_payload is not None, "A non-Person section requires a complete Person sections response.")
        parent = select_person_section(_collection_items(person_sections_payload, "Person sections response"), request, template)
        require(
            person_properties_payload is not None,
            "A non-Person section requires the complete selected Person section properties response.",
        )
        person_property_metadata = _complete_property_items(
            person_properties_payload, "selected Person section properties response"
        )
        properties = select_model_properties(property_metadata, person_property_metadata, request)
        person_base_property_count = len(person_property_metadata)
        model_property_count = len(property_metadata)
    context = _content_context(request, template, properties)
    validate_no_duplicate(target_sections, request, template, parent)

    requested_subscribers = request.get("subscribers", [])
    if requested_subscribers:
        require(subscriber_payload is not None, "Subscriber assignments require a subscriber catalog response.")
        subscriber_catalog = _collection_items(subscriber_payload, "subscriber catalog response")
    else:
        subscriber_catalog = []

    require(not output.exists(), f"Output already exists: {output}", "approval_blocker")
    with _safe_zip(source_template_zip) as source:
        _validate_empty_native_template(source)
        source_names = source.namelist()
        source_member_bytes = {member: source.read(member) for member in source_names}
        metadata = source_member_bytes[METADATA_MEMBER]
        headers: dict[str, list[str]] = {}
        rows: dict[str, list[dict[str, Any]]] = {}
        for member in BASE_MEMBERS:
            headers[member], source_rows = _read_csv(source, member)
            rows[member] = source_rows
        if requested_subscribers:
            require(CONTENT_SOURCE_MEMBER in source.namelist(), f"Source template ZIP lacks {CONTENT_SOURCE_MEMBER}.", "catalog_or_metadata_mismatch")
            headers[CONTENT_SOURCE_MEMBER], _source_rows = _read_csv(source, CONTENT_SOURCE_MEMBER)

        code = request["target_profile_type_code"]
        profile = _profile_row(
            headers[PROFILE_MEMBER],
            rows[PROFILE_MEMBER],
            code,
            request["target_profile_type_id"],
            profile_types,
        )
        order = _display_order(request, target_sections)
        section = _section_row(headers[SECTION_MEMBER], request, context, parent, order)
        property_rows = [_property_row(headers[PROPERTY_MEMBER], request, context, item) for item in properties]
        section_translations = _section_translation_rows(headers[SECTION_TRANSLATION_MEMBER], request, context)
        property_translations = _property_translation_rows(headers[PROPERTY_TRANSLATION_MEMBER], request, context, properties)
        content_sources = (
            _content_source_rows(
                headers[CONTENT_SOURCE_MEMBER],
                request,
                context,
                subscriber_catalog,
                int(template["ContentTypeId"]),
            )
            if requested_subscribers
            else []
        )

        member_bytes = {
            PROFILE_MEMBER: _csv_bytes(headers[PROFILE_MEMBER], [profile]),
            SECTION_MEMBER: _csv_bytes(headers[SECTION_MEMBER], [section]),
            PROPERTY_MEMBER: _csv_bytes(headers[PROPERTY_MEMBER], property_rows),
            SECTION_TRANSLATION_MEMBER: _csv_bytes(headers[SECTION_TRANSLATION_MEMBER], section_translations),
            PROPERTY_TRANSLATION_MEMBER: _csv_bytes(headers[PROPERTY_TRANSLATION_MEMBER], property_translations),
        }
        if content_sources:
            member_bytes[CONTENT_SOURCE_MEMBER] = _csv_bytes(headers[CONTENT_SOURCE_MEMBER], content_sources)

    result: dict[str, Any] = {
        "status": "planned" if dry_run else "prepared",
        "read_only_fusion_discovery": True,
        "fusion_writes_performed": False,
        "target_profile_type_id": request["target_profile_type_id"],
        "target_profile_type_code": request["target_profile_type_code"],
        "template_name": request["template_name"],
        "template_section_id": int(template["SectionId"]),
        "content_type_id": int(template["ContentTypeId"]),
        "content_type_context_name": context,
        "section_context": request["section_context"],
        "person_parent_section_id": int(parent["SectionId"]) if parent else None,
        "person_parent_section_context": parent.get("SectionContext") if parent else None,
        "property_count": len(property_rows),
        "person_base_property_count": person_base_property_count,
        "model_property_count": model_property_count,
        "subscriber_count": len(content_sources),
        "translation_count": len(section_translations),
        "source_template_zip": str(source_template_zip),
        "source_template_sha256": hashlib.sha256(source_template_zip.read_bytes()).hexdigest(),
        "output": str(output),
        "checks": [
            "complete REST collections",
            "exact template match",
            "profile-type property applicability",
            "two-source model property resolution when required",
            "active Person parent when required",
            "one Person section per target profile type",
            "native FSM template/spec archive with header-only CSVs",
            "native FSM header and member contract",
            "owning profile row populated from complete supplied metadata; import semantics require review",
            "metadata marker preserved byte-for-byte",
        ],
    }
    if dry_run:
        return result

    output.parent.mkdir(parents=True, exist_ok=True)
    source_member_bytes.update(member_bytes)
    with zipfile.ZipFile(output, "w") as candidate:
        for member in source_names:
            candidate.writestr(_zip_info(member), source_member_bytes[member])
    require(zipfile.is_zipfile(output), "Generated candidate is not a valid ZIP.", "artifact_persistence")
    with zipfile.ZipFile(output) as candidate:
        require(candidate.testzip() is None, "Generated candidate failed its CRC check.", "artifact_persistence")
        require(candidate.read(METADATA_MEMBER) == metadata, "Generated candidate changed the metadata marker.", "artifact_persistence")
    result["sha256"] = hashlib.sha256(output.read_bytes()).hexdigest()
    result["members"] = list(BASE_MEMBERS) + [METADATA_MEMBER] + ([CONTENT_SOURCE_MEMBER] if content_sources else [])
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a review-only Profile Types FSM ZIP from complete, sanitized REST GET responses."
    )
    parser.add_argument("--request", required=True, type=Path, help="Normalized configuration request JSON.")
    parser.add_argument("--templates-response", required=True, type=Path, help="Complete findTemplateSections response JSON.")
    parser.add_argument(
        "--properties-response",
        required=True,
        type=Path,
        help="Complete P/B template properties response for Person, or complete M template properties response for a non-Person target.",
    )
    parser.add_argument("--target-sections-response", required=True, type=Path, help="Complete target profile contentSections response JSON.")
    parser.add_argument("--profile-types-response", type=Path, help="Complete source-backed owning Profile Type metadata, including a locally extracted immutable FSM current-data export reference; not a Person parent section.")
    parser.add_argument("--person-sections-response", type=Path, help="Complete Person parent-section response JSON for non-Person targets.")
    parser.add_argument(
        "--person-properties-response",
        type=Path,
        help="Complete SourceProfileTypeCode B and null SourceCode properties response for the selected Person section; required for non-Person targets.",
    )
    parser.add_argument("--subscriber-response", type=Path, help="Complete subscriber catalog response JSON when subscribers are requested.")
    parser.add_argument("--source-template-zip", required=True, type=Path, help="Native HRT_MANAGE_PROFILE_TYPES FSM ZIP used only for headers and metadata.")
    parser.add_argument("--output", required=True, type=Path, help="New candidate ZIP path; existing files are never overwritten.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print the plan without writing the candidate ZIP.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        request = _load_json(args.request, "request")
        templates = _load_json(args.templates_response, "template response")
        properties = _load_json(args.properties_response, "property response")
        target_sections = _load_json(args.target_sections_response, "target sections response")
        profile_types = _load_json(args.profile_types_response, "profile types response") if args.profile_types_response else None
        person_sections = _load_json(args.person_sections_response, "Person sections response") if args.person_sections_response else None
        person_properties = (
            _load_json(args.person_properties_response, "selected Person section properties response")
            if args.person_properties_response
            else None
        )
        subscribers = _load_json(args.subscriber_response, "subscriber catalog response") if args.subscriber_response else None
        result = prepare(
            request,
            templates,
            properties,
            target_sections,
            args.source_template_zip,
            args.output,
            profile_types_payload=profile_types,
            person_sections_payload=person_sections,
            person_properties_payload=person_properties,
            subscriber_payload=subscribers,
            dry_run=args.dry_run,
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except PreparationError as exc:
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "failure_class": exc.failure_class,
                    "message": str(exc),
                    "recommended_action": "Correct the input or refresh the complete REST metadata, then run a new dry-run.",
                },
                indent=2,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2 if exc.failure_class == "catalog_or_metadata_mismatch" else 1


if __name__ == "__main__":
    raise SystemExit(main())
