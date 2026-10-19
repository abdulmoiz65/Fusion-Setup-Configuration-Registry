#!/usr/bin/env python3
"""Normalize and validate the GROW-8154 proposal-intake CSV.

This local utility has no network client and no Fusion mutation route. It emits
sanitized JSON to stdout and never modifies the supplied CSV.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


CONTRACT_COLUMNS = (
    "complete_set_id",
    "task_code",
    "record_type",
    "local_key",
    "parent_local_key",
    "parent_exact_reference",
    "related_local_key",
    "related_exact_reference",
    "name",
    "code",
    "description",
    "value",
    "language",
    "effective_start_date",
    "effective_end_date",
    "sequence",
    "relationship_code",
    "location",
    "country_code",
    "country_geography_code",
    "state_country_code",
    "state_geography_code",
    "free_form_flag",
    "attribute_label",
    "column_name",
    "default_value",
    "required_flag",
    "display_code",
    "view_attribute_name",
    "rating_model_code",
    "rating_level_code",
    "mandatory_flag",
    "rating_interaction_type",
    "content_supplier_code",
    "additional_values_json",
    "source_reference",
    "review_status",
)

REVIEW_STATUSES = {
    "supplied",
    "inferred-pending-review",
    "confirmed",
    "blocked",
    "not-applicable",
}

TASK_CODES = {
    "content_types": "HRT_MANAGE_PROFILE_CONTENT_TYPES",
    "content_items": "HRT_MANAGE_PROFILE_CONTENT_ITEMS",
    "item_catalogs": "ORA_MANAGE_PROFILE_ITEM_CATALOG",
    "instance_qualifiers": "HRT_MANAGE_INSTANCE_QUALIFIERS",
    "educational_establishments": "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS",
}

RECORD_SPECS: dict[str, dict[str, Any]] = {
    "content_type": {
        "task": "content_types",
        "required": {"local_key", "name", "code"},
        "allowed": {
            "local_key",
            "name",
            "code",
            "description",
            "free_form_flag",
            "rating_model_code",
            "additional_values_json",
        },
        "readiness": "source-backed-proposal-intake",
    },
    "content_type_property": {
        "task": "content_types",
        "required": {"local_key", "name", "column_name"},
        "allowed": {
            "local_key",
            "parent_local_key",
            "parent_exact_reference",
            "name",
            "value",
            "attribute_label",
            "column_name",
            "default_value",
            "required_flag",
            "display_code",
            "view_attribute_name",
        },
        "parent_type": "content_type",
        "readiness": "source-backed-proposal-intake",
    },
    "content_type_relationship": {
        "task": "content_types",
        "required": {"local_key", "relationship_code", "effective_start_date"},
        "allowed": {
            "local_key",
            "parent_local_key",
            "parent_exact_reference",
            "related_local_key",
            "related_exact_reference",
            "relationship_code",
            "rating_interaction_type",
            "effective_start_date",
            "effective_end_date",
        },
        "parent_type": "content_type",
        "related_type": "content_type",
        "readiness": "source-backed-proposal-intake",
    },
    "content_item": {
        "task": "content_items",
        "required": {"local_key", "name", "code"},
        "allowed": {
            "local_key",
            "parent_local_key",
            "parent_exact_reference",
            "name",
            "code",
            "description",
            "rating_model_code",
            "content_supplier_code",
            "country_code",
            "additional_values_json",
            "effective_start_date",
            "effective_end_date",
        },
        "parent_type": "content_type",
        "readiness": "source-backed-proposal-intake",
    },
    "content_item_translation": {
        "task": "content_items",
        "required": {"local_key", "name", "language"},
        "allowed": {
            "local_key",
            "parent_local_key",
            "parent_exact_reference",
            "name",
            "description",
            "language",
        },
        "parent_type": "content_item",
        "readiness": "captured-provider-mapping-blocked",
        "blocker": "Content Item translation provider field and canonical readback mapping are unresolved.",
    },
    "content_item_proficiency_description": {
        "task": "content_items",
        "required": {"local_key", "description", "rating_level_code"},
        "allowed": {
            "local_key",
            "parent_local_key",
            "parent_exact_reference",
            "name",
            "description",
            "sequence",
            "rating_level_code",
        },
        "parent_type": "content_item",
        "readiness": "captured-provider-mapping-blocked",
        "blocker": "Item-specific proficiency mapping is blocked until the exact Rating Model and provider field contract are resolved.",
    },
    "content_item_relationship": {
        "task": "content_items",
        "required": {"local_key", "relationship_code"},
        "allowed": {
            "local_key",
            "parent_local_key",
            "parent_exact_reference",
            "related_local_key",
            "related_exact_reference",
            "relationship_code",
            "mandatory_flag",
            "effective_start_date",
            "effective_end_date",
        },
        "parent_type": "content_item",
        "related_type": "content_item",
        "readiness": "source-backed-proposal-intake",
    },
    "item_catalog": {
        "task": "item_catalogs",
        "required": {"local_key", "name"},
        "allowed": {"local_key", "name", "code", "description"},
        "readiness": "source-backed-proposal-intake",
        "blocker": "Item Catalog values are captured for review. Catalog-only or phase-one anchored-child FSM eligibility must be established separately from exact mapped provider rows, current evidence and the task-local contract; this intake is not package readiness.",
    },
    "item_catalog_membership": {
        "task": "item_catalogs",
        "required": {"local_key"},
        "allowed": {
            "local_key",
            "parent_local_key",
            "parent_exact_reference",
            "related_local_key",
            "related_exact_reference",
            "effective_start_date",
            "effective_end_date",
        },
        "readiness": "source-backed-proposal-intake",
        "blocker": "Item Catalog memberships are captured with their supplied references. Evaluate the guarded one-parent/one-child FSM contract separately; complete-set membership execution remains blocked pending the approved full-set provider design.",
        "parent_type": "item_catalog",
        "related_type": "content_item",
    },
    "item_catalog_rating_description": {
        "task": "item_catalogs",
        "required": {"local_key", "description"},
        "allowed": {
            "local_key",
            "parent_local_key",
            "parent_exact_reference",
            "name",
            "description",
            "sequence",
            "rating_level_code",
        },
        "readiness": "field-contract-unavailable",
        "blocker": "Item Catalog rating-description persistence is blocked until the workflow proves the provider field/readback contract and exact Rating Model reference.",
        "parent_type": "item_catalog",
    },
    "instance_qualifier_set": {
        "task": "instance_qualifiers",
        "required": {"local_key", "name"},
        "allowed": {"local_key", "name", "code", "description"},
        "readiness": "field-contract-unavailable",
        "blocker": "Instance Qualifier Set persistence is blocked until the exact provider member, field, dependency, and readback contract is proven.",
    },
    "instance_qualifier": {
        "task": "instance_qualifiers",
        "required": {"local_key", "name"},
        "allowed": {
            "local_key",
            "parent_local_key",
            "parent_exact_reference",
            "name",
            "code",
            "description",
            "value",
            "sequence",
            "additional_values_json",
        },
        "readiness": "field-contract-unavailable",
        "blocker": "Instance Qualifier persistence is blocked until the exact provider member, field, dependency, and readback contract is proven.",
        "parent_type": "instance_qualifier_set",
    },
    "educational_establishment": {
        "task": "educational_establishments",
        "required": {"local_key", "name", "code"},
        "allowed": {
            "local_key",
            "name",
            "code",
            "description",
            "location",
            "country_code",
            "country_geography_code",
            "state_country_code",
            "state_geography_code",
        },
        "readiness": "source-backed-proposal-intake",
    },
    "behavior_item_catalog": {
        "task": "item_catalogs",
        "required": {"local_key", "name"},
        "allowed": {"local_key", "name", "code", "description"},
        "readiness": "captured-provider-mapping-blocked",
        "blocker": "Behavior Item Catalog persistence is blocked until the approved interactive provider and exact catalog/readback contract are proven.",
    },
    "competency_behavior_relationship": {
        "task": "content_items",
        "required": {"local_key", "relationship_code"},
        "allowed": {
            "local_key",
            "parent_local_key",
            "parent_exact_reference",
            "related_local_key",
            "related_exact_reference",
            "relationship_code",
            "mandatory_flag",
            "effective_start_date",
            "effective_end_date",
        },
        "parent_type": "content_item",
        "related_type": "content_item",
        "readiness": "captured-provider-mapping-blocked",
        "blocker": "Competency-to-Behavior relationship persistence is blocked until the exact behavior relationship provider/readback contract is proven.",
    },
}

META_COLUMNS = {"complete_set_id", "task_code", "record_type", "source_reference", "review_status"}
REDACTED_SENSITIVE_VALUE = "[REDACTED-SENSITIVE-MATERIAL]"
SENSITIVE_MATERIAL = re.compile(
    r"""(?ix)
    (?:bearer\s+[a-z0-9._~+/=-]{8,})
    |(?:-----BEGIN\s+[A-Z0-9 ]*PRIVATE\s+KEY-----)
    |(?:(?:client[_ -]?(?:secret|id)|(?:access[_ -]?|refresh[_ -]?)?token|password|private[_ -]?key|authorization|credential|secret)
       [\"']?\s*[:=]\s*[\"']?\S+)
    """
)
SENSITIVE_FIELD = re.compile(
    r"password|secret|token|private[_ -]?key|authorization|credential|client[_ -]?id", re.IGNORECASE
)


def redact_json_fields(value: str) -> tuple[str, bool]:
    """Screen even invalid-for-provider nested JSON before any diagnostic output."""
    try:
        parsed = json.loads(value)
    except ValueError:
        return value, False
    except RecursionError:
        return REDACTED_SENSITIVE_VALUE, True
    redacted = False

    def scrub(item):
        nonlocal redacted
        if isinstance(item, dict):
            result = {}
            for key, child in item.items():
                if SENSITIVE_FIELD.search(key):
                    result[key] = REDACTED_SENSITIVE_VALUE
                    redacted = True
                else:
                    result[key] = scrub(child)
            return result
        if isinstance(item, list):
            return [scrub(child) for child in item]
        if isinstance(item, str) and SENSITIVE_MATERIAL.search(item):
            redacted = True
            return REDACTED_SENSITIVE_VALUE
        return item

    try:
        safe = scrub(parsed)
    except RecursionError:
        return REDACTED_SENSITIVE_VALUE, True
    return (json.dumps(safe, ensure_ascii=False), True) if redacted else (value, False)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def add_once(items: list[str], message: str) -> None:
    if message not in items:
        items.append(message)


def parse_iso_date(value: str) -> date:
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError("date must use exact YYYY-MM-DD form")
    return parsed


def validate_reference(
    record: dict[str, str],
    row_number: int,
    role: str,
    expected_type: str,
    identities: set[tuple[str, str]],
    errors: list[str],
) -> None:
    local_field = f"{role}_local_key"
    exact_field = f"{role}_exact_reference"
    local_value = record[local_field]
    exact_value = record[exact_field]
    if bool(local_value) == bool(exact_value):
        errors.append(
            f"row {row_number}: supply exactly one of {local_field} or {exact_field} for {role} reference"
        )
        return
    if local_value and (expected_type, local_value) not in identities:
        errors.append(
            f"row {row_number}: {local_field}={local_value!r} does not resolve to a {expected_type} row in this complete set"
        )


def normalize(path: Path, *, csv_text: str | None = None) -> tuple[dict[str, Any], int]:
    errors: list[str] = []
    blockers: list[str] = []
    records: list[dict[str, Any]] = []
    unmapped_records: list[dict[str, Any]] = []
    source_fingerprint = sha256_file(path) if csv_text is None else hashlib.sha256(csv_text.encode("utf-8")).hexdigest()

    with (path.open("r", encoding="utf-8-sig", newline="") if csv_text is None else io.StringIO(csv_text)) as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        if fieldnames != CONTRACT_COLUMNS:
            return (
                {
                    "schema_version": "1.0",
                    "status": "blocked",
                    "input_method": "file",
                    "source_file": path.name,
                    "source_fingerprint": source_fingerprint,
                    "complete_set_ids": [],
                    "task_scopes": [],
                    "records": [],
                    "unmapped_records": [],
                    "source_record_count": None,
                    "mapping_results": [],
                    "errors": ["CSV header does not exactly match the governed Stage 3 template."],
                    "blockers": [],
                },
                2,
            )

        for row_number, raw in enumerate(reader, start=2):
            if None in raw:
                errors.append(
                    f"row {row_number}: row contains fields beyond the governed template header"
                )
            row = {column: (raw.get(column) or "") for column in CONTRACT_COLUMNS}
            if not any(row.values()):
                continue
            for column, value in row.items():
                if value != value.strip():
                    errors.append(f"row {row_number}: {column} contains leading or trailing whitespace")
                if "\x00" in value:
                    errors.append(f"row {row_number}: {column} contains a NUL character")
                safe_value, redacted = redact_json_fields(value)
                if redacted or SENSITIVE_MATERIAL.search(value):
                    errors.append(
                        f"row {row_number}: {column} appears to contain sensitive authentication material"
                    )
                    row[column] = safe_value if redacted else REDACTED_SENSITIVE_VALUE

            record_type = row["record_type"]
            spec = RECORD_SPECS.get(record_type)
            if spec is None:
                errors.append(f"row {row_number}: unsupported record_type {record_type!r}")
                unmapped_records.append({
                    "csv_row": row_number,
                    "provided_record_type": record_type,
                    "provided_task_code": row["task_code"],
                    "mapping_readiness": "unmapped-requires-confirmation",
                    "values": row,
                    "source": {"file": path.name, "row": row_number,
                               "reference": row["source_reference"]},
                })
                continue

            expected_task = TASK_CODES[spec["task"]]
            if row["task_code"] != expected_task:
                errors.append(
                    f"row {row_number}: task_code must be {expected_task} for record_type {record_type}"
                )
            for required in sorted({"complete_set_id", "source_reference", "review_status"} | spec["required"]):
                if not row[required]:
                    errors.append(f"row {row_number}: {required} is required for {record_type}")
            if row["review_status"] not in REVIEW_STATUSES:
                errors.append(f"row {row_number}: invalid review_status {row['review_status']!r}")
            elif row["review_status"] in {"inferred-pending-review", "blocked", "not-applicable"}:
                add_once(
                    blockers,
                    f"At least one row has review_status={row['review_status']}; it cannot enter a configuration-ready proposal.",
                )
            nonblank_data = {column for column, value in row.items() if value and column not in META_COLUMNS}
            unexpected = sorted(nonblank_data - spec["allowed"])
            if unexpected:
                errors.append(
                    f"row {row_number}: fields not allowed for {record_type}: {', '.join(unexpected)}"
                )

            for field in ("effective_start_date", "effective_end_date"):
                if row[field]:
                    try:
                        parse_iso_date(row[field])
                    except ValueError as exc:
                        errors.append(f"row {row_number}: {field} {exc}")
            if row["effective_start_date"] and row["effective_end_date"]:
                try:
                    if parse_iso_date(row["effective_end_date"]) < parse_iso_date(row["effective_start_date"]):
                        errors.append(f"row {row_number}: effective_end_date precedes effective_start_date")
                except ValueError:
                    pass
            country_pair = bool(row["country_code"]), bool(row["country_geography_code"])
            state_pair = bool(row["state_country_code"]), bool(row["state_geography_code"])
            if country_pair[0] != country_pair[1]:
                errors.append(f"row {row_number}: country code and geography code must be supplied together")
            if state_pair[0] != state_pair[1]:
                errors.append(f"row {row_number}: state country and geography code must be supplied together")
            if any(state_pair) and not all(country_pair):
                errors.append(f"row {row_number}: state geography requires explicit country geography")
            if row["sequence"]:
                try:
                    if int(row["sequence"]) <= 0 or str(int(row["sequence"])) != row["sequence"]:
                        raise ValueError
                except ValueError:
                    errors.append(f"row {row_number}: sequence must be a positive base-10 integer")
            for field in ("free_form_flag", "required_flag", "mandatory_flag"):
                if row[field] not in {"", "Y", "N"}:
                    errors.append(f"row {row_number}: {field} must be blank, Y, or N")
            if row["additional_values_json"]:
                try:
                    additional_values = json.loads(row["additional_values_json"])
                except json.JSONDecodeError:
                    errors.append(f"row {row_number}: additional_values_json must be valid JSON")
                else:
                    if not isinstance(additional_values, dict) or any(
                        isinstance(value, (dict, list))
                        for value in additional_values.values()
                    ):
                        errors.append(
                            f"row {row_number}: additional_values_json must be an object containing scalar values"
                        )

            if spec.get("blocker"):
                add_once(blockers, spec["blocker"])

            records.append(
                {
                    "csv_row": row_number,
                    "task_code": row["task_code"],
                    "record_type": record_type,
                    "mapping_readiness": spec["readiness"],
                    "values": row,
                    "source": {
                        "file": path.name,
                        "row": row_number,
                        "reference": row["source_reference"],
                    },
                }
            )

    if not records and not errors:
        return (
            {
                "schema_version": "1.0",
                "status": "template_ready",
                "input_method": "blank_template",
                "source_file": path.name,
                "source_fingerprint": source_fingerprint,
                "complete_set_ids": [],
                "task_scopes": [],
                "records": [],
                "unmapped_records": [],
                "source_record_count": 0,
                "mapping_results": [],
                "errors": [],
                "blockers": [],
            },
            0,
        )

    set_ids = sorted({record["values"]["complete_set_id"] for record in records + unmapped_records if record["values"]["complete_set_id"]})
    if len(set_ids) != 1:
        errors.append("One input file must contain exactly one nonblank complete_set_id.")

    identities: set[tuple[str, str]] = set()
    for record in records:
        identity = (record["record_type"], record["values"]["local_key"])
        if identity[1] and identity in identities:
            errors.append(
                f"row {record['csv_row']}: duplicate local identity {identity[0]}/{identity[1]}"
            )
        identities.add(identity)

    seen_rows: set[str] = set()
    for record in records:
        row_identity = canonical_sha256(record["values"])
        if row_identity in seen_rows:
            errors.append(f"row {record['csv_row']}: exact duplicate input row")
        seen_rows.add(row_identity)

        spec = RECORD_SPECS[record["record_type"]]
        if spec.get("parent_type"):
            validate_reference(
                record["values"],
                record["csv_row"],
                "parent",
                spec["parent_type"],
                identities,
                errors,
            )
        if spec.get("related_type"):
            validate_reference(
                record["values"],
                record["csv_row"],
                "related",
                spec["related_type"],
                identities,
                errors,
            )

        if record["record_type"].endswith("relationship"):
            values = record["values"]
            same_local = values["parent_local_key"] and values["parent_local_key"] == values["related_local_key"]
            same_exact = values["parent_exact_reference"] and values["parent_exact_reference"] == values["related_exact_reference"]
            if same_local or same_exact:
                errors.append(f"row {record['csv_row']}: a relationship cannot link an object to itself")

    free_form_keys = {
        record["values"]["local_key"]
        for record in records
        if record["record_type"] == "content_type"
        and record["values"]["free_form_flag"] == "Y"
    }
    for record in records:
        if (
            record["record_type"]
            in {"content_type_property", "content_type_relationship", "content_item"}
            and record["values"]["parent_local_key"] in free_form_keys
        ):
            errors.append(
                f"row {record['csv_row']}: a free-form Content Type cannot own properties, relationships, or Content Items"
            )

    relationship_pairs: set[tuple[str, str]] = set()
    for record in records:
        if record["record_type"] != "content_type_relationship":
            continue
        values = record["values"]
        parent = values["parent_local_key"] or values["parent_exact_reference"]
        related = values["related_local_key"] or values["related_exact_reference"]
        pair = parent, related
        if all(pair) and pair in relationship_pairs:
            errors.append(
                f"row {record['csv_row']}: only one relationship type is allowed for the same Content Type pair"
            )
        relationship_pairs.add(pair)

    # A description belongs to an item's explicitly supplied model; never pick
    # a model from the level label or copy a shared model's standard description.
    items_by_key: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        if record["record_type"] == "content_item":
            items_by_key.setdefault(record["values"]["local_key"], []).append(record)
    description_keys: set[tuple[str, str, str]] = set()
    for record in records:
        if record["record_type"] != "content_item_proficiency_description":
            continue
        values = record["values"]
        parents = items_by_key.get(values["parent_local_key"], [])
        if values["parent_local_key"] and len(parents) == 1:
            if not parents[0]["values"]["rating_model_code"]:
                errors.append(
                    f"row {record['csv_row']}: parent content_item "
                    f"{values['parent_local_key']!r} requires an explicit rating_model_code "
                    "for supplied proficiency descriptions"
                )
        if values["parent_exact_reference"]:
            add_once(blockers, "Proficiency descriptions referencing an external item require exact item-to-model evidence; a model's existence alone is insufficient.")
        identity = (values["parent_local_key"], values["parent_exact_reference"], values["rating_level_code"])
        if identity in description_keys:
            errors.append(f"row {record['csv_row']}: duplicate proficiency description for the same parent and rating_level_code")
        description_keys.add(identity)

    task_scopes = sorted({record["task_code"] for record in records if record["task_code"]})
    mapping_results = sorted(
        {
            (record["record_type"], record["task_code"], record["mapping_readiness"])
            for record in records
        }
    )
    fingerprint_body = {
        "complete_set_ids": set_ids,
        "task_scopes": task_scopes,
        "records": [
            {
                "task_code": record["task_code"],
                "record_type": record["record_type"],
                "mapping_readiness": record["mapping_readiness"],
                "values": record["values"],
            }
            for record in records
        ],
    }
    status = "blocked" if errors or blockers else "normalized"
    if unmapped_records:
        # Corrections to unmapped values must invalidate the complete request,
        # even though no task or provider identity has been inferred for them.
        fingerprint_body["unmapped_records"] = unmapped_records
    result = {
        "schema_version": "1.0",
        "status": status,
        "input_method": "file",
        "source_file": path.name,
        "source_fingerprint": source_fingerprint,
        "normalized_input_fingerprint": canonical_sha256(fingerprint_body),
        "complete_set_ids": set_ids,
        "task_scopes": task_scopes,
        "records": records,
        "unmapped_records": unmapped_records,
        "source_record_count": len(records) + len(unmapped_records),
        "mapping_results": [
            {"record_type": item[0], "task_code": item[1], "readiness": item[2]}
            for item in mapping_results
        ],
        "errors": errors,
        "blockers": blockers,
    }
    return result, 2 if status == "blocked" else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize the local Stage 3 Profile Management Content Library Configuration proposal-intake CSV."
    )
    parser.add_argument("input_csv", type=Path, help="Path to a CSV using the governed intake header")
    args = parser.parse_args()

    path = args.input_csv.resolve()
    if not path.is_file():
        payload = {
            "schema_version": "1.0",
            "status": "blocked",
            "errors": ["Input CSV is missing or is not a regular file."],
            "blockers": [],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 2
    try:
        payload, exit_code = normalize(path)
    except (OSError, UnicodeError, csv.Error) as exc:
        payload = {
            "schema_version": "1.0",
            "status": "blocked",
            "source_file": path.name,
            "errors": [f"Input CSV could not be read safely: {exc.__class__.__name__}"],
            "blockers": [],
        }
        exit_code = 2
    print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
