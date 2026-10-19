#!/usr/bin/env python3
"""Prepare a consultant-supplied Goal Management HDL bundle without changing it."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from hdl_dat_validator import (
    HdlDatValidationError, PROFILES, _read_source, mapped_values,
    require_reference, validate_source_owner,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _nonblank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _row_key(filename: str, object_name: str, line: int) -> str:
    return f"{filename}|{object_name}|line:{line}"


def _uses_explicit_mass_request(row: dict[str, str], context: dict[str, Any]) -> bool:
    if not context.get("hasMassRequest"):
        return False
    external_id = row.get("GoalPlanExternalId")
    parents = context.get("massRequestParents", set())
    return not external_id or external_id in parents


def _generated_source_id(profile: str, object_name: str, row: dict[str, str]) -> str:
    fields = (
            "Name", "GoalPlanName", "GoalName", "Language", "ContextName",
            "GoalPlanExternalId", "WorkerAssignmentNumber", "OrganizationName",
            "ReviewPeriodName", "StartDate", "EndDate", "GoalPlanStartDate", "GoalPlanEndDate",
            "DocTypeName", "EligibilityProfileName", "ManagerAssignmentNumber",
    )
    if object_name == "ContentItem" and row.get("ItemDate1") and row.get("ItemDate2"):
        fields += ("ItemDate1", "ItemDate2", "ItemText9")
    # Preserve established plan keys. Extend only Goal identities that
    # previously omitted the worker and could collide across workers.
    if object_name in {"Goal", "GoalPlanGoal"}:
        fields += ("WorkerPersonNumber", "GoalWorkerPersonNumber", "GoalWorkerAssignmentNumber",
                   "GoalPersonNumber", "GoalAssignmentNumber", "GoalTypeCode", "GoalVersionTypeCode",
                   "TargetCompletionDate", "GoalStartDate", "GoalTargetCompletionDate")
    business = "|".join(row.get(name, "") for name in fields)
    digest = hashlib.sha256(f"{profile}|{object_name}|{business}".encode("utf-8")).hexdigest()[:16].upper()
    return f"FSCR_{object_name.upper()[:20]}_{digest}"


def _validated_source_owner(context: dict[str, Any], object_name: str) -> str:
    """Return a configured owner only when fresh runtime metadata allows it."""
    source_owner = context.get("sourceSystemOwner")
    if not _nonblank(source_owner):
        raise HdlDatValidationError(
            "sourceSystemOwner must be a nonblank code confirmed in HRC_SOURCE_SYSTEM_OWNER."
        )
    contract = context.get("fieldMetadata", {}).get(object_name, {}).get("SourceSystemOwner")
    allowed = contract.get("allowedValues") if isinstance(contract, dict) else None
    if not isinstance(allowed, list) or not allowed or not all(_nonblank(value) for value in allowed):
        raise HdlDatValidationError(
            f"Current HRC_SOURCE_SYSTEM_OWNER allowedValues are required for {object_name}."
        )
    value = source_owner.strip()
    validate_source_owner(context, value)
    if value not in allowed:
        raise HdlDatValidationError(
            f"sourceSystemOwner {value} is not enabled and effective in HRC_SOURCE_SYSTEM_OWNER."
        )
    return value


def _component_defaults(
    profile: str,
    object_name: str,
    context: dict[str, Any],
    row_count: int,
    row: dict[str, str],
) -> dict[str, tuple[str, str]]:
    values: dict[str, tuple[str, str]] = {}
    configured = context.get("defaultValues", {})
    if configured and not isinstance(configured, dict):
        raise HdlDatValidationError("defaultValues must be an object keyed by HDL component.")
    for key in ("*", object_name):
        component = configured.get(key, {}) if isinstance(configured, dict) else {}
        if not isinstance(component, dict):
            raise HdlDatValidationError(f"defaultValues.{key} must be an object.")
        for field, value in component.items():
            if not isinstance(field, str) or not isinstance(value, (str, int, float)) or isinstance(value, bool) or not _nonblank(str(value)):
                raise HdlDatValidationError(f"defaultValues.{key} must contain nonblank scalar values.")
            values[field] = (str(value), "target-metadata default")

    current_person = context.get("currentPerson", {})
    if current_person and not isinstance(current_person, dict):
        raise HdlDatValidationError("currentPerson must be an object supplied by the authenticated-worker route.")
    person_number = current_person.get("personNumber") if isinstance(current_person, dict) else None
    if _nonblank(person_number):
        if current_person.get("activePrimaryAssignment") is not True:
            raise HdlDatValidationError(
                "Authenticated requester must resolve to exactly one active primary assignment."
            )
        if object_name == "MassRequest" or (object_name == "GoalPlan" and not _uses_explicit_mass_request(row, context)):
            values.setdefault("ReqSubmittedByPersonNumber", (person_number.strip(), "authenticated Fusion person"))
        if object_name == "Goal":
            values.setdefault("AssignedByPersonNumber", (person_number.strip(), "authenticated Fusion person"))

    generated_at = context.get("generatedAt")
    if not _nonblank(generated_at):
        generated_at = _utc_now().isoformat().replace("+00:00", "Z")
    try:
        parsed_generated_at = datetime.fromisoformat(str(generated_at).replace("Z", "+00:00"))
    except ValueError as exc:
        raise HdlDatValidationError("generatedAt must be a timezone-aware ISO-8601 timestamp.") from exc
    if parsed_generated_at.tzinfo is None:
        raise HdlDatValidationError("generatedAt must include a timezone.")
    generated_date = parsed_generated_at.astimezone(timezone.utc).date().strftime("%Y/%m/%d")
    if object_name == "GoalPlan" and not _uses_explicit_mass_request(row, context):
        values.setdefault("RequestSubmissionDate", (generated_date, "current preparation date"))

    if object_name == "ContentItem":
        if row_count == 1:
            values.setdefault("ContextName", ("GOAL", "single Library Goal route"))
        if row.get("ContextName") == "GOAL" or row_count == 1:
            variant_field = context.get("semanticFields", {}).get("ContentItem", {}).get("TypeCode", context.get("variantField", "ItemText9"))
            if context.get("resolutionContract") and not context.get("semanticFields", {}).get("ContentItem", {}).get("TypeCode"):
                raise HdlDatValidationError("CATALOG_MAPPING_REQUIRED: resolved Library Goal context cannot guess TypeCode.")
            values.setdefault(variant_field, (PROFILES[profile]["variant"], "selected Library Goal variant"))
        values.setdefault("DateFrom", (generated_date, "current preparation date"))
        # Lifecycle/audience defaults use the live mapping, never guessed HDL slots.
        for semantic, desired in (("StatusCode", "I"), ("Visible", "ALL")):
            field = context.get("semanticFields", {}).get("ContentItem", {}).get(semantic)
            if field:
                metadata = context.get("fieldMetadata", {}).get("ContentItem", {}).get(field, {})
                candidates = [code for code in metadata.get("allowedValues", [])
                              if metadata.get("valueMap", {}).get(code, code) == desired]
                if len(candidates) != 1:
                    raise HdlDatValidationError(f"Resolve one current HDL code for {semantic}={desired} before defaulting.")
                values.setdefault(field, (candidates[0], "validated create-only lifecycle/audience default"))
    # Only goal-bearing create rows with a verified priority mapping participate.
    # Execution validation rejects a missing mapping; unrelated components and
    # update/delete rows retain their existing behavior.
    if object_name in {"Goal", "GoalPlanGoal"} or (object_name == "ContentItem" and
            (row.get("ContextName") == "GOAL" or row_count == 1 and profile.endswith("library_goal"))):
        field = context.get("semanticFields", {}).get(object_name, {}).get("PriorityCode")
        metadata = context.get("fieldMetadata", {}).get(object_name, {})
        if not field and object_name in {"Goal", "GoalPlanGoal"} and "PriorityCode" in metadata:
            field = "PriorityCode"
        if field and field not in row:
            contract = metadata.get(field, {})
            candidates = [c for c in contract.get("allowedValues", [])
                          if contract.get("valueMap", {}).get(c, c) == "MEDIUM"]
            if len(candidates) != 1:
                raise HdlDatValidationError("Resolve one current HDL Medium priority code before defaulting.")
            values.setdefault(field, (candidates[0], "validated create-only priority default"))
    return values


def _prepare_file(filename: str, content: bytes, profile: str, context: dict[str, Any]) -> tuple[bytes, list[dict[str, Any]]]:
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HdlDatValidationError(f"{filename} must be valid UTF-8 text.") from exc
    if "\x00" in text:
        raise HdlDatValidationError(f"{filename} contains binary NUL bytes.")
    lines = text.splitlines()
    parsed: list[dict[str, Any]] = []
    active: dict[str, list[str]] = {}
    object_counts: dict[str, int] = {}
    for number, raw in enumerate(lines, start=1):
        values = raw.split("|")
        if len(values) >= 2 and values[0] == "METADATA":
            active[values[1]] = values[2:]
        elif len(values) >= 2 and values[0] in {"MERGE", "DELETE"} and values[1] in active:
            object_counts[values[1]] = object_counts.get(values[1], 0) + 1
            parsed.append({"line": number, "values": values, "object": values[1], "fields": list(active[values[1]])})

    derived = context.get("derivedValues", {})
    if derived and not isinstance(derived, dict):
        raise HdlDatValidationError("derivedValues must be an object keyed by file, component, and input line.")
    source_owner = context.get("sourceSystemOwner")
    create_locations = set(context.get("createRows", []))
    substitutions: list[dict[str, Any]] = []
    row_values: dict[int, dict[str, str]] = {}

    for item in parsed:
        values = item["values"]
        fields = item["fields"]
        if len(values) != len(fields) + 2:
            raise HdlDatValidationError(f"{filename}:{item['line']} data row field count does not match METADATA.")
        row = {field: values[index + 2].strip() for index, field in enumerate(fields)}
        key = _row_key(filename, item["object"], item["line"])
        # Resolve operation before applying defaults. MERGE alone is not create intent.
        from hdl_dat_validator import _identity
        identity = _identity(item["object"], row, context)
        scoped = f"{filename}|{item['object']}|{identity}"
        operation = "delete" if values[0] == "DELETE" else context.get("rowOperations", {}).get(
            key, context.get("rowOperations", {}).get(scoped, context.get("defaultOperation")))
        if operation not in {"create", "update", "delete"}:
            raise HdlDatValidationError(f"{key} requires a resolved create/update/delete operation before preparation.")
        additions = (_component_defaults(profile, item["object"], context, object_counts[item["object"]], row)
                     if operation == "create" else {})
        row_specific = derived.get(key, {}) if isinstance(derived, dict) else {}
        if not isinstance(row_specific, dict):
            raise HdlDatValidationError(f"derivedValues.{key} must be an object.")
        for field, value in row_specific.items():
            additions[field] = (str(value), "resolved target/caller value")
        if operation != "delete":
            binding = context.get("rowBindings", {}).get(key, {})
            if binding and operation == "create":
                require_reference(context, binding.get("evidenceRef"))
                for field, value in binding.get("values", {}).items():
                    if row.get(field) and row[field] != str(value):
                        raise HdlDatValidationError(f"{key}: supplied {field} conflicts with resolved context.")
                    additions[field] = (str(value), "resolved row relationship")
            resolved = context.get("resolvedSemanticValues", {}).get(key, {})
            for field, value in mapped_values(context, item["object"], resolved).items():
                if row.get(field) and row[field] != value:
                    raise HdlDatValidationError(f"{key}: supplied {field} conflicts with requested semantic value.")
                additions[field] = (value, "verified semantic mapping")
        if operation == "create" and key in create_locations:
            resolved_owner = (additions.get("SourceSystemOwner", (None,))[0]
                              if context.get("resolutionContract") else None)
            source_owner = _validated_source_owner(
                {**context, "sourceSystemOwner": row.get("SourceSystemOwner") or resolved_owner or context.get("sourceSystemOwner")},
                item["object"],
            )
            additions.setdefault("SourceSystemOwner", (source_owner, "validated source-system owner"))
            identity_row = {**{field: value for field, (value, _) in additions.items()},
                            **{field: value for field, value in row.items() if value}}
            if item["object"] not in {"Goal", "GoalPlanGoal"} and not context.get("resolutionContract"):
                identity_row = row
            additions.setdefault("SourceSystemId", (_generated_source_id(profile, item["object"], identity_row), "deterministic create source key"))
        for field, (value, source) in additions.items():
            if any(character in value for character in ("|", "\r", "\n", "\x00")):
                raise HdlDatValidationError(f"Resolved {field} contains an unsupported DAT delimiter or newline.")
            existing = row.get(field, "")
            priority_field = context.get("semanticFields", {}).get(item["object"], {}).get("PriorityCode", "PriorityCode")
            if field == priority_field and field in row:
                # Unlike an absent column, explicit blank/#NULL is intentional.
                continue
            if existing:
                continue
            row[field] = value
            substitution = {
                "file": filename, "line": item["line"], "object": item["object"],
                "field": field, "value": value, "source": source,
            }
            if field in {
                "ReqSubmittedByPersonNumber", "AssignedByPersonNumber",
                "PersonId", "AssignmentId", "WorkerPersonNumber", "WorkerAssignmentNumber",
                "GoalWorkerPersonNumber", "GoalWorkerAssignmentNumber",
                "GoalPersonNumber", "GoalAssignmentNumber",
                "ObjectId",
            }:
                substitution["value"] = "<redacted>"
                substitution["valueSha256"] = hashlib.sha256(value.encode("utf-8")).hexdigest()
                substitution["sensitive"] = True
            substitutions.append(substitution)
            if field not in fields:
                fields.append(field)
        row_values[item["line"]] = row

    # Every repeated METADATA block for a component uses the union needed by its rows.
    object_unions: dict[str, list[str]] = {}
    for item in parsed:
        union = object_unions.setdefault(item["object"], list(item["fields"]))
        for field in row_values[item["line"]]:
            if field not in union:
                union.append(field)

    output: list[str] = []
    current_fields: dict[str, list[str]] = {}
    for number, raw in enumerate(lines, start=1):
        values = raw.split("|")
        if len(values) >= 2 and values[0] == "METADATA":
            object_name = values[1]
            fields = object_unions.get(object_name, values[2:])
            current_fields[object_name] = fields
            output.append("|".join(["METADATA", object_name, *fields]))
        elif number in row_values:
            object_name = values[1]
            row = row_values[number]
            output.append("|".join([values[0], object_name, *(row.get(field, "") for field in current_fields[object_name])]))
        else:
            output.append(raw)
    return ("\n".join(output) + "\n").encode("utf-8"), substitutions


def enrich_bundle(source: Path, profile: str, runtime_context: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    """Create a prepared directory while preserving the uploaded source bytes."""
    if profile not in PROFILES:
        raise HdlDatValidationError("profile must identify a supported Goal Management HDL bundle.")
    source_before = source.read_bytes() if source.is_file() else None
    source_resolved = source.resolve()
    output_resolved = output_dir.resolve()
    if output_resolved == source_resolved or (source.is_dir() and source_resolved in output_resolved.parents):
        raise HdlDatValidationError("prepared output must be outside the uploaded source path.")
    files, issues, source_type = _read_source(source)
    if issues:
        raise HdlDatValidationError(issues[0]["message"])
    local_context = dict(runtime_context)
    mass_request_parents: set[str] = set()
    has_mass_request = False
    for content in files.values():
        try:
            lines = content.decode("utf-8-sig").splitlines()
        except UnicodeDecodeError:
            continue
        metadata: dict[str, list[str]] = {}
        for raw in lines:
            values = raw.split("|")
            if len(values) >= 2 and values[0] == "METADATA":
                metadata[values[1]] = values[2:]
            elif len(values) >= 2 and values[0] in {"MERGE", "DELETE"} and values[1] == "MassRequest":
                has_mass_request = True
                fields = metadata.get("MassRequest", [])
                row = {field: values[index + 2].strip() for index, field in enumerate(fields) if index + 2 < len(values)}
                if row.get("GoalPlanExternalId"):
                    mass_request_parents.add(row["GoalPlanExternalId"])
    local_context["hasMassRequest"] = has_mass_request
    local_context["massRequestParents"] = mass_request_parents
    if output_dir.exists() and (not output_dir.is_dir() or any(output_dir.iterdir())):
        raise HdlDatValidationError("prepared output directory must be empty.")
    prepared_files: dict[str, bytes] = {}
    substitutions: list[dict[str, Any]] = []
    for filename, content in files.items():
        prepared, changes = _prepare_file(filename, content, profile, local_context)
        prepared_files[filename] = prepared
        substitutions.extend(changes)
    if source_before is not None and source.read_bytes() != source_before:
        raise HdlDatValidationError("source bundle changed during preparation.")
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, prepared in prepared_files.items():
        (output_dir / filename).write_bytes(prepared)
    return {
        "status": "prepared", "sourceType": source_type, "source": str(source),
        "preparedSource": str(output_dir), "substitutions": substitutions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a Goal Management HDL DAT/ZIP using internal resolved context.")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--profile", required=True, choices=tuple(PROFILES))
    parser.add_argument("--runtime-context", required=True, type=Path, help="Internal routed-workflow context; not consultant input.")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    context = json.loads(args.runtime_context.read_text(encoding="utf-8"))
    report = enrich_bundle(args.source, args.profile, context, args.output_dir)
    content = json.dumps(report, indent=2) + "\n"
    if args.report:
        args.report.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (HdlDatValidationError, json.JSONDecodeError, OSError) as exc:
        raise SystemExit(f"Error: {exc}")
