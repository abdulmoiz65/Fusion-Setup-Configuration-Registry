#!/usr/bin/env python3
"""Fail-closed local validation for Goal Management HDL DAT bundles."""
from __future__ import annotations

import hashlib
import io
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
import stat
from typing import Any
import zipfile

from duplicate_identity import compare_goal_plan_review_period


PROFILES = {
    "goal_plan": {
        "required": ("GoalPlan.dat",),
        "optional": ("GoalPlanTranslation.dat", "Goal.dat"),
        "components": {
            "GoalPlan.dat": {
                "GoalPlan", "GoalPlanDocTypes", "MassRequest", "MassRequestAssignment",
                "EligibilityProfileObject", "MassRequestHierarchy", "MassRequestExemption",
                "GoalPlanAssignment", "GoalPlanGoal",
            },
            "GoalPlanTranslation.dat": {"GoalPlanTranslation"},
            "Goal.dat": {
                "Goal", "GoalPlanGoal", "GoalAction", "GoalMeasurement",
                "GoalTargetOutcome", "GoalTargetOutcomeProfileItem", "GoalAccess",
                "GoalAlignment",
            },
        },
    },
    "performance_library_goal": {
        "required": ("ContentItem.dat",),
        "optional": ("ContentItemTranslation.dat", "ContentItemRelationship.dat"),
        "components": {
            "ContentItem.dat": {"ContentItem"},
            "ContentItemTranslation.dat": {"ContentItemTranslation"},
            "ContentItemRelationship.dat": {"ContentItemRelationship"},
        },
        "variant": "PERFORMANCE",
    },
    "development_library_goal": {
        "required": ("ContentItem.dat",),
        "optional": ("ContentItemTranslation.dat", "ContentItemRelationship.dat"),
        "components": {
            "ContentItem.dat": {"ContentItem"},
            "ContentItemTranslation.dat": {"ContentItemTranslation"},
            "ContentItemRelationship.dat": {"ContentItemRelationship"},
        },
        "variant": "DEVELOPMENT",
    },
}
ALLOWED_OPERATIONS = {"create", "update", "delete"}
MAX_ZIP_MEMBERS = 20
MAX_ZIP_MEMBER_BYTES = 50 * 1024 * 1024
MAX_ZIP_TOTAL_BYTES = 100 * 1024 * 1024

USER_KEYS: dict[str, tuple[str, ...]] = {
    "GoalPlan": ("GoalPlanExternalId",),
    "GoalPlanTranslation": ("GoalPlanExternalId", "Language"),
    "GoalPlanDocTypes": ("GoalPlanExternalId", "DocTypeName"),
    "MassRequest": ("GoalPlanExternalId",),
    "MassRequestAssignment": ("GoalPlanExternalId", "OrganizationName"),
    "EligibilityProfileObject": ("GoalPlanExternalId", "EligibilityProfileName"),
    "MassRequestHierarchy": ("GoalPlanExternalId", "ManagerAssignmentNumber"),
    "MassRequestExemption": ("GoalPlanExternalId", "ManagerAssignmentNumber", "WorkerAssignmentNumber"),
    "GoalPlanAssignment": ("GoalPlanExternalId", "WorkerAssignmentNumber"),
    "GoalPlanGoal": ("GoalPlanExternalId", "GoalName"),
    "Goal": ("GoalName", "GoalTypeCode", "GoalVersionTypeCode", "StartDate",
             "TargetCompletionDate", "WorkerPersonNumber", "WorkerAssignmentNumber"),
    "ContentItem": ("Name", "ContextName"),
    "ContentItemTranslation": ("ContentItemName", "Language"),
    "ContentItemRelationship": (
        "ContextName", "ContentItemName", "RelatedContentTypeContextName", "RelatedContentItemName"
    ),
}
USER_KEY_ALTERNATIVES: dict[str, tuple[tuple[str, ...], ...]] = {
    "Goal": (
        USER_KEYS["Goal"],
        ("GoalName", "GoalTypeCode", "GoalVersionTypeCode", "StartDate",
         "TargetCompletionDate", "OrganizationName"),
    ),
    "GoalPlanGoal": (
        ("GoalPlanExternalId", "GoalName", "GoalStartDate", "GoalTargetCompletionDate",
         "GoalTypeCode", "GoalVersionTypeCode", "GoalWorkerPersonNumber", "GoalWorkerAssignmentNumber"),
        ("GoalPlanExternalId", "GoalName", "GoalStartDate", "GoalTargetCompletionDate",
         "GoalTypeCode", "GoalVersionTypeCode", "GoalPersonNumber", "GoalAssignmentNumber"),
        # Legacy structural fixtures remain readable; execution validates the
        # complete relationship independently of these audit identities.
        ("GoalPlanExternalId", "GoalName"),
        ("GoalPlanName", "GoalPlanStartDate", "GoalPlanEndDate", "GoalName"),
    ),
    "ContentItemTranslation": (
        ("ContentItemName", "Language"),
        ("Name", "Language"),
    ),
}
GOAL_PLAN_CHILDREN = {
    "GoalPlanTranslation", "GoalPlanDocTypes", "MassRequest", "MassRequestAssignment",
    "EligibilityProfileObject", "MassRequestHierarchy", "MassRequestExemption",
    "GoalPlanAssignment", "GoalPlanGoal",
}


class HdlDatValidationError(ValueError):
    """The manifest is incomplete or the DAT bundle is unsafe."""


def require_reference(context: dict[str, Any], reference: Any) -> dict[str, Any]:
    """Check provenance supplied by the routed read adapter, never renew it."""
    sources = context.get("targetEvidence", context.get("evidenceSources", {}))
    evidence = sources.get(reference) if isinstance(reference, str) else None
    if not isinstance(evidence, dict) or not evidence.get("source"):
        raise HdlDatValidationError("Resolved HDL values require structured read evidence.")
    if str(evidence.get("environment", "")).casefold() != str(context.get("environment", "")).casefold():
        raise HdlDatValidationError("Resolved HDL evidence belongs to another environment.")
    now = datetime.now(timezone.utc)
    verified = _timestamp(evidence.get("verifiedAt"), "evidence.verifiedAt")
    max_age = context.get("evidenceMaxAgeHours", 24)
    if isinstance(max_age, bool) or not isinstance(max_age, (int, float)) or not 0 < max_age <= 168:
        raise HdlDatValidationError("Invalid evidenceMaxAgeHours.")
    if verified > now + timedelta(minutes=5) or now - verified > timedelta(hours=max_age):
        raise HdlDatValidationError("Resolved HDL evidence is stale or future-dated.")
    return evidence


def validate_source_owner(context: dict[str, Any], value: str) -> None:
    evidence = require_reference(context, "HRC_SOURCE_SYSTEM_OWNER")
    if evidence.get("lookupType") != "HRC_SOURCE_SYSTEM_OWNER":
        raise HdlDatValidationError("Source owner evidence must identify HRC_SOURCE_SYSTEM_OWNER.")
    matches = [entry for entry in evidence.get("items", [])
               if isinstance(entry, dict) and entry.get("LookupCode") == value]
    if len(matches) != 1 or matches[0].get("EnabledFlag") != "Y":
        raise HdlDatValidationError("SourceSystemOwner must resolve to one enabled HRC_SOURCE_SYSTEM_OWNER code.")
    today = datetime.now(timezone.utc).date()
    for field, lower in (("StartDateActive", True), ("EndDateActive", False)):
        date = matches[0].get(field)
        if date:
            boundary = datetime.strptime(str(date)[:10], "%Y-%m-%d").date()
            if (lower and today < boundary) or (not lower and today > boundary):
                raise HdlDatValidationError("SourceSystemOwner is not effective on the validation date.")


def mapped_values(context: dict[str, Any], component: str, resolved: dict[str, Any]) -> dict[str, str]:
    """Translate every requested semantic value through an evidenced HDL mapping."""
    result: dict[str, str] = {}
    for semantic, binding in resolved.items():
        if not isinstance(binding, dict) or binding.get("value") in (None, ""):
            raise HdlDatValidationError("Every requested semantic value must be resolved before HDL preparation.")
        value_evidence = require_reference(context, binding.get("evidenceRef"))
        if str(value_evidence.get("values", {}).get(semantic, "")) != str(binding["value"]):
            raise HdlDatValidationError(f"Resolved {semantic} does not match target-read evidence.")
        mapping = context.get("semanticFields", {}).get(component, {})
        field = mapping.get(semantic)
        proof = context.get("mappingEvidence", {}).get(component, {}).get(semantic, {})
        mapping_evidence = require_reference(context, proof.get("evidenceRef"))
        metadata = context.get("fieldMetadata", {}).get(component, {}).get(field)
        if not field or proof.get("field") != field or not isinstance(metadata, dict):
            raise HdlDatValidationError(f"No verified HDL field mapping for {component}.{semantic}.")
        if mapping_evidence.get("mappings", {}).get(component, {}).get(semantic) != field:
            raise HdlDatValidationError(f"HDL mapping evidence does not establish {component}.{semantic}.")
        if metadata.get("serverGenerated") is True:
            raise HdlDatValidationError(f"Do not populate server-generated HDL field {field}.")
        if field in result:
            raise HdlDatValidationError("Different semantic inputs map to the same HDL field.")
        result[field] = str(binding["value"])
    return result


def validate_row_binding(row, component, operation, key, manifest):
    """Validate worker and relationship semantics separately from header validity."""
    binding = manifest.get("rowBindings", {}).get(key, {})
    if operation == "delete":
        return
    if component not in {"Goal", "GoalPlanGoal", "EligibilityProfileObject"}:
        return
    evidence = require_reference(manifest, binding.get("evidenceRef"))
    expected = binding.get("values", {})
    if not isinstance(expected, dict):
        raise HdlDatValidationError("Resolved row binding values must be an object.")
    if evidence.get("values") != expected:
        raise HdlDatValidationError("Row relationship must match the actual resolved evidence values.")
    if component == "Goal":
        if binding.get("kind") not in {"template", "worker", "organization"}:
            raise HdlDatValidationError("Goal requires an explicit template, worker or organization context.")
        fields = ("GoalName", "GoalTypeCode", "GoalVersionTypeCode", "StartDate", "TargetCompletionDate",
                  *(("OrganizationName",) if binding["kind"] == "organization" else
                    ("WorkerPersonNumber", "WorkerAssignmentNumber")))
        if any(row.get(field) for field in ("PersonId", "AssignmentId")):
            raise HdlDatValidationError("This Goal HDL route requires resolved worker user keys, not numeric worker IDs.")
    elif component == "GoalPlanGoal":
        worker_fields = (("GoalPersonNumber", "GoalAssignmentNumber") if key.startswith("GoalPlan.dat|")
                         else ("GoalWorkerPersonNumber", "GoalWorkerAssignmentNumber"))
        if binding.get("kind") == "organization":
            worker_fields = ("GoalOrganizationName",)
        fields = ("GoalPlanExternalId", "GoalName", "GoalTypeCode", "GoalVersionTypeCode",
                  "GoalStartDate", "GoalTargetCompletionDate", *worker_fields)
    else:
        fields = ("ObjectId", "GoalPlanExternalId", "EligibilityProfileName", "RequiredFlag")
        if (str(binding.get("massRequestId", "")) != row.get("ObjectId")
                or binding.get("goalPlanExternalId") != row.get("GoalPlanExternalId")
                or binding.get("talentObjectType") != "GOAL"):
            raise HdlDatValidationError("Eligibility ObjectId must resolve to the selected plan's MassRequest.")
        if any(evidence.get(field) != binding.get(field)
               for field in ("massRequestId", "goalPlanExternalId", "talentObjectType")):
            raise HdlDatValidationError("MassRequest relationship differs from target-read evidence.")
    for field in fields:
        if not row.get(field) or str(expected.get(field, "")) != row[field]:
            raise HdlDatValidationError(f"{component}.{field} does not match its resolved relationship.")
    for field, value in expected.items():
        if row.get(field) != str(value):
            raise HdlDatValidationError(f"{component}.{field} conflicts with resolved input.")
    for field in ("GoalId", "GoalPlanId", "EligyPrflId"):
        if row.get(field) and str(expected.get(field, "")) != row[field]:
            raise HdlDatValidationError(f"Additional {field} must match the same resolved relationship.")


def worker_goal_key(row, component, filename):
    if component == "Goal":
        fields = ("GoalName", "StartDate", "TargetCompletionDate", "GoalTypeCode",
                  "GoalVersionTypeCode", "WorkerPersonNumber", "WorkerAssignmentNumber", "OrganizationName")
    else:
        worker = (("GoalPersonNumber", "GoalAssignmentNumber") if filename == "GoalPlan.dat"
                  else ("GoalWorkerPersonNumber", "GoalWorkerAssignmentNumber"))
        fields = ("GoalName", "GoalStartDate", "GoalTargetCompletionDate", "GoalTypeCode",
                  "GoalVersionTypeCode", *worker, "GoalOrganizationName")
    return tuple(row.get(field, "") for field in fields)


def _digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _issue(code: str, message: str, *, file: str | None = None, line: int | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"code": code, "severity": "error", "message": message}
    if file is not None:
        result["file"] = file
    if line is not None:
        result["line"] = line
    return result


def _read_source(source: Path) -> tuple[dict[str, bytes], list[dict[str, Any]], str]:
    """Read a directory, single DAT, or flat ZIP without extracting members."""
    issues: list[dict[str, Any]] = []
    if source.is_dir():
        files = {
            path.name: path.read_bytes()
            for path in source.iterdir()
            if path.is_file() and path.suffix.lower() == ".dat"
        }
        return files, issues, "directory"
    if not source.is_file():
        raise HdlDatValidationError("HDL source must be an existing DAT file, ZIP file, or directory.")
    if source.suffix.lower() == ".dat":
        return {source.name: source.read_bytes()}, issues, "dat"
    if source.suffix.lower() != ".zip":
        raise HdlDatValidationError("HDL source must be a DAT file, ZIP file, or directory.")
    try:
        with zipfile.ZipFile(source) as archive:
            members = archive.infolist()
            if len(members) > MAX_ZIP_MEMBERS:
                raise HdlDatValidationError("HDL ZIP exceeds the permitted member count.")
            files: dict[str, bytes] = {}
            seen: set[str] = set()
            total = 0
            for member in members:
                member_path = PurePosixPath(member.filename)
                if member.is_dir():
                    raise HdlDatValidationError("HDL ZIP must not contain folders.")
                if member.flag_bits & 0x1:
                    raise HdlDatValidationError("Encrypted HDL ZIP members are not supported by local preflight.")
                if stat.S_ISLNK(member.external_attr >> 16):
                    raise HdlDatValidationError("HDL ZIP must not contain symbolic links.")
                if member_path.is_absolute() or len(member_path.parts) != 1 or ".." in member_path.parts:
                    raise HdlDatValidationError("HDL ZIP DAT files must be flat and must not contain unsafe paths.")
                normalized = member_path.name.casefold()
                if normalized in seen:
                    raise HdlDatValidationError("HDL ZIP contains duplicate member names.")
                seen.add(normalized)
                if member.file_size > MAX_ZIP_MEMBER_BYTES:
                    raise HdlDatValidationError("HDL ZIP member exceeds the permitted uncompressed size.")
                total += member.file_size
                if total > MAX_ZIP_TOTAL_BYTES:
                    raise HdlDatValidationError("HDL ZIP exceeds the permitted total uncompressed size.")
                if member_path.suffix.lower() != ".dat":
                    issues.append(_issue(
                        "UNSUPPORTED_ARCHIVE_MEMBER", "Goal Management HDL ZIP accepts DAT files only.",
                        file=member.filename,
                    ))
                    continue
                files[member_path.name] = archive.read(member)
            return files, issues, "zip"
    except (zipfile.BadZipFile, RuntimeError, OSError) as exc:
        raise HdlDatValidationError(f"HDL ZIP is corrupt or unreadable: {exc}") from exc


def _evidence_is_confirmed(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and value.get("confirmed") is True
        and isinstance(value.get("environment"), str)
        and bool(value["environment"].strip())
        and isinstance(value.get("verifiedAt"), str)
        and bool(value["verifiedAt"].strip())
        and isinstance(value.get("source"), str)
        and bool(value["source"].strip())
    )


def _timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise HdlDatValidationError(f"{label} must be a timezone-aware ISO-8601 timestamp.")
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise HdlDatValidationError(f"{label} must be a timezone-aware ISO-8601 timestamp.") from exc
    if parsed.tzinfo is None:
        raise HdlDatValidationError(f"{label} must include a timezone.")
    return parsed.astimezone(timezone.utc)


def _field_map(fields: list[str], values: list[str]) -> dict[str, str]:
    return {name: values[index].strip() for index, name in enumerate(fields) if index < len(values)}


def _identity(object_name: str, row: dict[str, str], manifest: dict[str, Any]) -> str | None:
    owner = row.get("SourceSystemOwner", "")
    source_id = row.get("SourceSystemId", "")
    if owner and source_id:
        identity = f"source:{owner}:{source_id}"
        if object_name == "ContentItemTranslation" and row.get("Language"):
            identity += f"|language:{row['Language']}"
        return identity
    configured = manifest.get("userKeyFields", {})
    if not isinstance(configured, dict):
        raise HdlDatValidationError("userKeyFields must be an object when supplied.")
    configured_keys = configured.get(object_name)
    if configured_keys is None:
        options = USER_KEY_ALTERNATIVES.get(object_name, (USER_KEYS.get(object_name, ()),))
    elif isinstance(configured_keys, (list, tuple)) and all(isinstance(key, str) for key in configured_keys):
        options = (tuple(configured_keys),)
    elif isinstance(configured_keys, (list, tuple)) and all(
        isinstance(option, (list, tuple)) and all(isinstance(key, str) for key in option)
        for option in configured_keys
    ):
        options = tuple(tuple(option) for option in configured_keys)
    else:
        raise HdlDatValidationError(
            f"userKeyFields.{object_name} must be a field list or a list of alternative field lists."
        )
    for keys in options:
        if keys and all(key and row.get(key) for key in keys):
            return "user:" + "|".join(f"{key}={row[key]}" for key in keys)
    return None


def _goal_plan_tokens(row: dict[str, str], *, parent: bool) -> set[str]:
    """Return supported parent identities from parent or child HDL attributes."""
    tokens: set[str] = set()
    # EligibilityProfileObject.ObjectId is the parent Mass Request ID, not the
    # Goal Plan ID. Only the explicit GoalPlanId attribute identifies a plan.
    goal_plan_id = row.get("GoalPlanId", "")
    if goal_plan_id:
        tokens.add(f"id:{goal_plan_id}")
    external_id = row.get("GoalPlanExternalId", "")
    if external_id:
        tokens.add(f"external:{external_id}")
    source_id = row.get("SourceSystemId" if parent else "GoalPlanId(SourceSystemId)", "")
    source_owner = row.get("SourceSystemOwner" if parent else "GoalPlanId(SourceSystemOwner)", "")
    if source_id and source_owner:
        tokens.add(f"source:{source_owner}:{source_id}")
    name = row.get("GoalPlanName", "")
    start = row.get("StartDate" if parent else "GoalPlanStartDate", "")
    end = row.get("EndDate" if parent else "GoalPlanEndDate", "")
    if name and start and end:
        tokens.add(f"business:{name}|{start}|{end}")
    return tokens


def _mandatory_fields(manifest: dict[str, Any], object_name: str, row: dict[str, str]) -> tuple[str, ...]:
    supplied = manifest.get("mandatoryFields", {})
    if not isinstance(supplied, dict) or not supplied:
        raise HdlDatValidationError("mandatoryFields must be an object keyed by HDL component.")
    contextual_name = f"{object_name}:{row.get('ContextName', '')}" if row.get("ContextName") else object_name
    if contextual_name in supplied:
        values = supplied[contextual_name]
    elif object_name in supplied:
        values = supplied[object_name]
    else:
        raise HdlDatValidationError(f"mandatoryFields must declare the current template fields for {contextual_name}.")
    if not isinstance(values, list) or not all(isinstance(value, str) and value for value in values):
        raise HdlDatValidationError(f"mandatoryFields.{object_name} must be a list of field names.")
    return tuple(values)


def _validate_execution_row(row, object_name, operation, key, manifest, profile):
    """Apply current operation metadata and shared business rules before handoff."""
    from goal_business_rules import validate_goal_plan_rules, validate_library_goal_rules
    metadata = manifest.get("fieldMetadata", {}).get(object_name)
    if not isinstance(metadata, dict) or not metadata:
        raise HdlDatValidationError(f"Current fieldMetadata is required for {object_name} execution.")
    for field, value in row.items():
        if field in {"METADATA", object_name}:
            continue
        if object_name in {"EligibilityProfileObject", "GoalPlanGoal"} and field.startswith("GoalPlanId("):
            raise HdlDatValidationError("Use template-supported GoalPlanExternalId, not GoalPlanId source hints.")
        contract = metadata.get(field)
        if not isinstance(contract, dict) or operation not in contract.get("operations", []):
            raise HdlDatValidationError(f"{field} is not supported for {operation} by current HDL metadata.")
        if value and operation == "create" and contract.get("serverGenerated") is True:
            raise HdlDatValidationError(f"Do not populate server-generated HDL field {field}.")
        if value and contract.get("allowedValues") and value not in contract["allowedValues"]:
            raise HdlDatValidationError(f"{field} is not in the current HDL value set.")
        if value and manifest.get("resolutionContract") and len(value) > contract.get("maxLength", float("inf")):
            raise HdlDatValidationError(f"{field} exceeds its current HDL maximum length.")
        if value and contract.get("type") == "date":
            datetime.strptime(value, "%Y/%m/%d")
    source_owner = row.get("SourceSystemOwner")
    if source_owner:
        validate_source_owner(manifest, source_owner)
        owner_contract = metadata.get("SourceSystemOwner")
        allowed_owners = owner_contract.get("allowedValues") if isinstance(owner_contract, dict) else None
        if not isinstance(allowed_owners, list) or not allowed_owners:
            raise HdlDatValidationError(
                "Current HRC_SOURCE_SYSTEM_OWNER allowedValues are required when SourceSystemOwner is populated."
            )
        if source_owner not in allowed_owners:
            raise HdlDatValidationError(
                f"SourceSystemOwner {source_owner} is not enabled and effective in HRC_SOURCE_SYSTEM_OWNER."
            )
    if operation == "delete":
        return
    effective = dict(row)
    if operation == "update":
        existing = manifest.get("existingRows", {}).get(key)
        if not isinstance(existing, dict) or not _evidence_is_confirmed(manifest["targetEvidence"].get(key)):
            raise HdlDatValidationError("Update requires the exact existing row and fresh identity-bound evidence.")
        effective = {**existing, **{k: v for k, v in row.items() if v != ""}}
    validate_row_binding(effective, object_name, operation, key, manifest)
    if operation == "create" and (object_name in {"Goal", "GoalPlanGoal"} or
            object_name == "ContentItem" and effective.get("ContextName") == "GOAL"):
        priority_field = manifest.get("semanticFields", {}).get(object_name, {}).get("PriorityCode")
        if not priority_field and object_name in {"Goal", "GoalPlanGoal"} and "PriorityCode" in metadata:
            priority_field = "PriorityCode"
        if not priority_field or priority_field not in metadata:
            raise HdlDatValidationError("Current semantic mapping and metadata are required for goal PriorityCode.")
        if priority_field not in effective:
            raise HdlDatValidationError("Goal create omits priority; prepare the Medium default before approval.")
        priority_codes = metadata[priority_field].get("allowedValues")
        if not priority_codes:
            raise HdlDatValidationError("Current allowedValues are required for PriorityCode.")
        if effective[priority_field] not in ("", "#NULL") and effective[priority_field] not in priority_codes:
            raise HdlDatValidationError("Goal priority is outside the current HDL value set.")
    resolved = manifest.get("resolvedSemanticValues", {}).get(key, {})
    mapped = mapped_values(manifest, object_name, resolved)
    for field, value in mapped.items():
        if effective.get(field) != value:
            raise HdlDatValidationError(f"{object_name}.{field} does not preserve the requested semantic value.")
    if object_name == "ContentItem" and effective.get("ContextName") == "GOAL":
        for field, value in row.items():
            if field.startswith("ItemNumber") and value and field not in mapped:
                raise HdlDatValidationError(f"Resolve the semantic mapping and target value for {field} before loading.")
    if object_name not in {"ContentItem", "GoalPlan"}:
        return
    if object_name == "ContentItem" and effective.get("ContextName") == "GOAL_MEASUREMENTS":
        return
    if object_name == "ContentItem" and effective.get("ContextName") != "GOAL":
        raise HdlDatValidationError("Exact existing or new ContentItem must belong to GOAL context.")
    mapping = manifest.get("semanticFields", {}).get(object_name)
    if not isinstance(mapping, dict):
        raise HdlDatValidationError(f"Live-metadata semanticFields mapping is required for {object_name}.")
    canonical = {}
    for semantic, field in mapping.items():
        if field not in metadata:
            raise HdlDatValidationError(f"Semantic field {semantic} is absent from current metadata.")
        if field not in effective:
            continue
        value = effective[field]
        # A blank HDL slot represents an omitted optional attribute.  Preserve
        # that omission instead of forcing it through boolean value mapping;
        # create rows can legitimately leave nullable switches unspecified.
        if value == "":
            continue
        contract = metadata[field]
        if value and contract.get("allowedValues") and value not in contract["allowedValues"]:
            raise HdlDatValidationError(f"Effective {field} is outside the current HDL value set.")
        value = contract.get("valueMap", {}).get(str(value), value)
        if contract.get("type") == "date" and value:
            value = datetime.strptime(value, "%Y/%m/%d").date().isoformat()
        if contract.get("type") == "integer" and value != "":
            value = int(value)
        if contract.get("type") == "boolean" and not isinstance(value, bool):
            raise HdlDatValidationError(f"{field} requires a current metadata boolean valueMap.")
        canonical[semantic] = value
    if object_name == "ContentItem":
        validate_library_goal_rules(canonical, PROFILES[profile]["variant"])
        for semantic in ("TypeCode", "StatusCode", "Visible"):
            if not metadata[mapping[semantic]].get("allowedValues"):
                raise HdlDatValidationError(f"Current allowedValues are required for {semantic}.")
    else:
        for field in ("GoalPlanName", "GoalPlanActiveCode", "PrimaryGoalPlanFlag", "StartDate", "EndDate"):
            if field not in canonical or canonical[field] is None or canonical[field] == "":
                raise HdlDatValidationError(f"Goal Plan {field} is required.")
        if canonical["GoalPlanActiveCode"] not in {"I", "A"}:
            raise HdlDatValidationError("Invalid Goal Plan status.")
        if not isinstance(canonical["PrimaryGoalPlanFlag"], bool):
            raise HdlDatValidationError("Resolve PrimaryGoalPlanFlag to a boolean through current metadata.")
        bounds = manifest.get("reviewPeriodBounds", {}).get(key)
        if canonical["PrimaryGoalPlanFlag"] is not True and not bounds:
            raise HdlDatValidationError("Regular Goal Plan requires resolved Review Period bounds.")
        validate_goal_plan_rules(canonical, review_period=bounds)


def validate_bundle(source: Path, manifest: dict[str, Any], *, execution_validation: bool = False) -> dict[str, Any]:
    profile = manifest.get("profile")
    if profile not in PROFILES:
        raise HdlDatValidationError("profile must identify a supported Goal Management HDL bundle.")
    contract = PROFILES[profile]
    allowed = set(manifest.get("allowedOperations", []))
    if not allowed or not allowed <= ALLOWED_OPERATIONS:
        raise HdlDatValidationError("allowedOperations must contain only create, update, or delete.")
    references = manifest.get("targetEvidence")
    if not isinstance(references, dict) or not references or not all(
        _evidence_is_confirmed(value) for value in references.values()
    ):
        raise HdlDatValidationError(
            "targetEvidence must contain structured, confirmed environment, verifiedAt, and source evidence."
        )
    validation_time = _timestamp(manifest.get("validationTime"), "validationTime")
    if execution_validation:
        validation_time = datetime.now(timezone.utc)
        if not manifest.get("environment"):
            raise HdlDatValidationError("Execution requires the exact target environment.")
    environments = {e["environment"].strip().casefold() for e in references.values()}
    if len(environments) != 1 or (manifest.get("environment") and manifest["environment"].strip().casefold() not in environments):
        raise HdlDatValidationError("All target evidence must belong to the execution environment.")
    max_age_hours = manifest.get("evidenceMaxAgeHours", 24)
    if isinstance(max_age_hours, bool) or not isinstance(max_age_hours, (int, float)) or not 0 < max_age_hours <= 168:
        raise HdlDatValidationError("evidenceMaxAgeHours must be greater than zero and no more than 168.")
    for name, evidence in references.items():
        verified_at = _timestamp(evidence["verifiedAt"], f"targetEvidence.{name}.verifiedAt")
        if verified_at > validation_time + timedelta(minutes=5):
            raise HdlDatValidationError(f"targetEvidence.{name} is later than validationTime.")
        if validation_time - verified_at > timedelta(hours=max_age_hours):
            raise HdlDatValidationError(f"targetEvidence.{name} is stale.")
    declared_rows = manifest.get("rowOperations")
    if not isinstance(declared_rows, dict):
        raise HdlDatValidationError("rowOperations must declare create, update, or delete for every scoped row key.")
    existing_parents = manifest.get("existingParents", {})
    if not isinstance(existing_parents, dict):
        raise HdlDatValidationError("existingParents must be an object when supplied.")
    existing_goal_plans: set[str] = set()
    for parent in existing_parents.get("GoalPlan", []):
        if not isinstance(parent, str) or not parent or not _evidence_is_confirmed(references.get(f"GoalPlan:{parent}")):
            raise HdlDatValidationError(
                "Every existingParents.GoalPlan value requires matching structured targetEvidence."
            )
        existing_goal_plans.update({parent, f"external:{parent}"})
    existing_content_items: set[str] = set()
    for parent in existing_parents.get("ContentItem", []):
        if not isinstance(parent, str) or not parent or not _evidence_is_confirmed(references.get(f"ContentItem:{parent}")):
            raise HdlDatValidationError(
                "Every existingParents.ContentItem value requires matching structured targetEvidence."
            )
        existing_content_items.add(parent)
    translation_parent_refs = manifest.get("translationParentReferences", {})
    if not isinstance(translation_parent_refs, dict):
        raise HdlDatValidationError("translationParentReferences must be an object when supplied.")

    files, issues, source_type = _read_source(source)
    required = contract["required"]
    optional = contract["optional"]
    permitted = set(required) | set(optional)
    for name in required:
        if name not in files:
            issues.append(_issue("MISSING_COMPONENT", "Required DAT file is missing.", file=name))
    for name in files:
        if name not in permitted:
            issues.append(_issue(
                "UNSUPPORTED_COMPONENT_FILE", "DAT file is not permitted for the selected profile.", file=name
            ))
    ordered_files = [name for name in (*required, *optional) if name in files]
    if manifest.get("files") != ordered_files:
        raise HdlDatValidationError("files must exactly match detected DAT files in permitted component order.")

    identities: set[str] = set()
    business_identities: set[tuple] = set()
    goal_plan_business_rows: list[dict[str, Any]] = []
    consumed_operations: set[str] = set()
    parsed_rows: list[dict[str, Any]] = []
    package_goal_plans: dict[str, tuple[str, int]] = {}
    goal_plan_parent_deletes: list[tuple[set[str], int]] = []
    goal_plan_child_deletes: list[tuple[set[str], str, int]] = []
    library_goals: set[str] = set()
    library_goal_tokens: set[str] = set()
    library_measurements: set[str] = set()
    library_relationships: set[tuple[str, str]] = set()
    library_translations: set[tuple[str, str]] = set()
    goal_keys: set[tuple[str, ...]] = set()
    association_keys: list[tuple[tuple[str, ...], str, str, int]] = []

    for filename in ordered_files:
        content = files[filename]
        if not content:
            issues.append(_issue("EMPTY_DAT", "DAT file is empty.", file=filename))
            continue
        if b"\x00" in content:
            issues.append(_issue("BINARY_DAT", "DAT file contains binary NUL bytes.", file=filename))
            continue
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError:
            issues.append(_issue("INVALID_ENCODING", "DAT file must be valid UTF-8 text.", file=filename))
            continue
        metadata: dict[str, list[str]] = {}
        for number, raw in enumerate(io.StringIO(text), start=1):
            raw = raw.rstrip("\r\n")
            if not raw or raw.startswith("COMMENT"):
                continue
            values = raw.split("|")
            verb, object_name = values[0], values[1] if len(values) > 1 else ""
            if verb == "METADATA" and object_name:
                if object_name not in contract["components"].get(filename, set()):
                    issues.append(_issue(
                        "UNSUPPORTED_COMPONENT", "HDL component is not permitted in this DAT file.",
                        file=filename, line=number,
                    ))
                metadata[object_name] = values
                continue
            if verb not in {"MERGE", "DELETE"}:
                issues.append(_issue(
                    "UNSUPPORTED_VERB", "Only METADATA, MERGE, DELETE, and COMMENT rows are accepted.",
                    file=filename, line=number,
                ))
                continue
            fields = metadata.get(object_name)
            if fields is None:
                issues.append(_issue(
                    "MISSING_METADATA", "Data row has no matching METADATA row.", file=filename, line=number
                ))
                continue
            if len(values) != len(fields):
                issues.append(_issue(
                    "FIELD_COUNT", "Data row field count does not match METADATA.", file=filename, line=number
                ))
                continue
            row = _field_map(fields, values)
            identity = _identity(object_name, row, manifest)
            if identity is None:
                issues.append(_issue(
                    "MISSING_KEY", "Row requires a complete source key or supported user key.",
                    file=filename, line=number,
                ))
                continue
            scoped_key = f"{filename}|{object_name}|{identity}"
            if scoped_key in identities:
                issues.append(_issue(
                    "DUPLICATE_ROW_KEY", "Scoped HDL row identity is duplicated.", file=filename, line=number
                ))
                continue
            identities.add(scoped_key)
            declared = declared_rows.get(scoped_key)
            actual = "delete" if verb == "DELETE" else declared
            conflict = (verb == "DELETE" and declared != "delete") or (verb == "MERGE" and declared == "delete")
            if declared not in ALLOWED_OPERATIONS or actual not in allowed or conflict:
                issues.append(_issue(
                    "UNAPPROVED_OPERATION",
                    "Row operation is missing, conflicts with its verb, or is outside approved scope.",
                    file=filename, line=number,
                ))
                continue
            consumed_operations.add(scoped_key)
            # Compare transport-independent business identities here. Dates are
            # validated separately and do not distinguish business duplicates.
            if actual == "create" and object_name in {"ContentItem", "GoalPlan"}:
                if object_name == "ContentItem":
                    business_key = (object_name, row.get("ItemText9"), row.get("Name"))
                    if all(business_key):
                        business_key = tuple(str(v).strip() for v in business_key)
                        if business_key in business_identities:
                            issues.append(_issue(
                                "DUPLICATE_BUSINESS_IDENTITY",
                                "Goal type and name match another create row.",
                                file=filename,
                                line=number,
                            ))
                        business_identities.add(business_key)
                elif row.get("GoalPlanName") and (
                    row.get("ReviewPeriodId") not in (None, "") or row.get("ReviewPeriodName")
                ):
                    canonical = {
                        "GoalPlanName": str(row["GoalPlanName"]).strip(),
                        "ReviewPeriodId": row.get("ReviewPeriodId"),
                        "ReviewPeriodName": row.get("ReviewPeriodName"),
                    }
                    for previous in goal_plan_business_rows:
                        if canonical["GoalPlanName"] != previous["GoalPlanName"]:
                            continue
                        comparison = compare_goal_plan_review_period(previous, canonical)
                        if comparison == "match":
                            issues.append(_issue(
                                "DUPLICATE_BUSINESS_IDENTITY",
                                "Goal Plan name and associated Review Period match another create row.",
                                file=filename,
                                line=number,
                            ))
                        elif comparison == "unresolved":
                            issues.append(_issue(
                                "UNRESOLVED_BUSINESS_IDENTITY",
                                "Goal Plan rows have no comparable associated Review Period.",
                                file=filename,
                                line=number,
                            ))
                    goal_plan_business_rows.append(canonical)
            if execution_validation:
                try:
                    _validate_execution_row(row, object_name, actual, scoped_key, manifest, profile)
                except (HdlDatValidationError, ValueError, TypeError, KeyError) as exc:
                    issues.append(_issue("BUSINESS_VALIDATION", str(exc), file=filename, line=number))
                effective = row
                if actual == "update":
                    effective = {**manifest.get("existingRows", {}).get(scoped_key, {}),
                                 **{field: value for field, value in row.items() if value != ""}}
                if verb != "DELETE" and object_name == "Goal":
                    goal_keys.add(worker_goal_key(effective, object_name, filename))
                elif verb != "DELETE" and object_name == "GoalPlanGoal":
                    association_keys.append((worker_goal_key(effective, object_name, filename), scoped_key, filename, number))
            if verb == "MERGE":
                required_fields = (_mandatory_fields(manifest, object_name, row) if actual == "create"
                                   else manifest.get("operationMandatoryFields", {}).get(object_name, {}).get("update", []))
                for field in required_fields:
                    if field not in row or not row[field]:
                        issues.append(_issue(
                            "MISSING_MANDATORY_DATA", f"Mandatory field {field} is absent or blank.",
                            file=filename, line=number,
                        ))

            if profile == "goal_plan":
                parent_tokens = _goal_plan_tokens(row, parent=object_name == "GoalPlan")
                if object_name == "GoalPlan" and parent_tokens:
                    for token in parent_tokens:
                        package_goal_plans[token] = (verb, number)
                    if verb == "DELETE":
                        goal_plan_parent_deletes.append((parent_tokens, number))
                elif object_name in GOAL_PLAN_CHILDREN:
                    matches = parent_tokens & (set(package_goal_plans) | existing_goal_plans)
                    if not parent_tokens:
                        issues.append(_issue(
                            "MISSING_PARENT_KEY",
                            "Goal Plan child requires a supported parent source or user key.",
                            file=filename, line=number,
                        ))
                    elif not matches:
                        issues.append(_issue(
                            "MISSING_PARENT",
                            "Goal Plan child refers to a parent not present in the package or confirmed in the target.",
                            file=filename, line=number,
                        ))
                    elif not parent_tokens <= (set(package_goal_plans) | existing_goal_plans) or len({package_goal_plans[token] for token in matches if token in package_goal_plans}) > 1:
                        issues.append(_issue("CONFLICTING_PARENT_KEYS", "All supplied parent keys must identify the same verified Goal Plan.", file=filename, line=number))
                    elif verb != "DELETE" and any(
                        token in package_goal_plans and package_goal_plans[token][1] > number
                        for token in matches
                    ):
                        issues.append(_issue(
                            "PARENT_ORDER", "Goal Plan parent must precede child MERGE rows.",
                            file=filename, line=number,
                        ))
                    if verb == "DELETE" and parent_tokens:
                        goal_plan_child_deletes.append((parent_tokens, object_name, number))
            else:
                context = row.get("ContextName", "")
                if object_name == "ContentItem":
                    if context not in {"GOAL", "GOAL_MEASUREMENTS"} and actual == "create":
                        issues.append(_issue(
                            "INVALID_GOAL_CONTEXT", "ContentItem ContextName must be GOAL or GOAL_MEASUREMENTS.",
                            file=filename, line=number,
                        ))
                    name = row.get("Name", "")
                    if context == "GOAL":
                        library_goals.add(name)
                        library_goal_tokens.add(f"name:{name}")
                        if row.get("SourceSystemOwner") and row.get("SourceSystemId"):
                            library_goal_tokens.add(f"source:{row['SourceSystemOwner']}:{row['SourceSystemId']}")
                        variant_field = manifest.get("variantField", "ItemText9")
                        if not isinstance(variant_field, str) or not variant_field:
                            raise HdlDatValidationError("variantField must be a nonblank field name.")
                        if (actual == "create" or row.get(variant_field)) and row.get(variant_field, "").upper() != contract["variant"]:
                            issues.append(_issue(
                                "VARIANT_MISMATCH",
                                f"Library Goal must use {contract['variant']} in {variant_field}.",
                                file=filename, line=number,
                            ))
                    elif context == "GOAL_MEASUREMENTS":
                        library_measurements.add(name)
                elif object_name == "ContentItemRelationship":
                    library_relationships.add((
                        row.get("ContentItemName", ""), row.get("RelatedContentItemName", "")
                    ))
                elif object_name == "ContentItemTranslation":
                    language = row.get("Language", "").upper()
                    enabled = manifest.get("enabledLanguages")
                    if not isinstance(enabled, list) or not enabled or not all(isinstance(item, str) and item for item in enabled):
                        raise HdlDatValidationError(
                            "enabledLanguages must contain the fresh target-enabled language codes when translations are supplied."
                        )
                    if language not in {item.upper() for item in enabled}:
                        issues.append(_issue(
                            "LANGUAGE_NOT_ENABLED", f"Translation language {language or '<blank>'} is not enabled in the target.",
                            file=filename, line=number,
                        ))
                    base_language = manifest.get("baseLanguage")
                    if isinstance(base_language, str) and language == base_language.upper():
                        issues.append(_issue(
                            "BASE_LANGUAGE_TRANSLATION",
                            "The base-language Library Goal row must be maintained through ContentItem, not ContentItemTranslation.",
                            file=filename, line=number,
                        ))
                    parent = translation_parent_refs.get(scoped_key)
                    if parent is None and row.get("SourceSystemOwner") and row.get("SourceSystemId"):
                        parent = f"source:{row['SourceSystemOwner']}:{row['SourceSystemId']}"
                    if parent is None and row.get("ContentItemName"):
                        parent = f"name:{row['ContentItemName']}"
                    if not isinstance(parent, str) or not parent:
                        issues.append(_issue(
                            "MISSING_TRANSLATION_PARENT_KEY",
                            "Library Goal translation requires an internally resolved parent reference.",
                            file=filename, line=number,
                        ))
                    elif parent not in library_goal_tokens and parent not in existing_content_items:
                        issues.append(_issue(
                            "MISSING_TRANSLATION_PARENT",
                            "Library Goal translation refers to no GOAL ContentItem in the package or confirmed target.",
                            file=filename, line=number,
                        ))
                    else:
                        translation_key = (parent, language)
                        if translation_key in library_translations:
                            issues.append(_issue(
                                "DUPLICATE_TRANSLATION_LANGUAGE",
                                "A Library Goal can contain only one translation row per language.",
                                file=filename, line=number,
                            ))
                        library_translations.add(translation_key)
            parsed_rows.append({
                "file": filename,
                "line": number,
                "object": object_name,
                "sourceIdentity": identity,
                "rowKey": scoped_key,
                "operation": actual,
            })

    for goal_key, key, filename, number in association_keys:
        binding = manifest.get("rowBindings", {}).get(key, {})
        evidence = references.get(binding.get("evidenceRef"), {})
        if goal_key not in goal_keys and evidence.get("existingGoal") is not True:
            issues.append(_issue("MISSING_GOAL_REFERENCE", "Association requires the full matching Goal key in the package or a verified existing Goal.", file=filename, line=number))
    for key in sorted(set(declared_rows) - consumed_operations):
        issues.append(_issue("EXTRA_OPERATION", f"Manifest operation has no matching validated row: {key}."))
    for parent_tokens, parent_line in goal_plan_parent_deletes:
        for child_tokens, component, child_line in goal_plan_child_deletes:
            if parent_tokens & child_tokens and component in {"GoalPlanGoal", "GoalPlanAssignment"} and child_line > parent_line:
                issues.append(_issue(
                    "DELETE_ORDER", f"{component} must be deleted before its Goal Plan parent.",
                    file="GoalPlan.dat", line=child_line,
                ))
    if library_measurements:
        related = {measurement for goal, measurement in library_relationships if goal in library_goals}
        for measurement in sorted(library_measurements - related):
            issues.append(_issue(
                "MISSING_MEASUREMENT_RELATIONSHIP",
                f"Library Goal measurement has no relationship to a GOAL content item: {measurement}.",
            ))

    return {
        "status": "passed" if not issues else "blocked",
        "validationScope": "execution" if execution_validation else "structural_only_not_upload_authorization",
        "profile": profile,
        "sourceType": source_type,
        "sourceSha256": _digest(source.read_bytes()) if source.is_file() else None,
        "files": [{"name": name, "sha256": _digest(files[name])} for name in ordered_files],
        "rows": parsed_rows,
        "issues": issues,
    }
