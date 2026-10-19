#!/usr/bin/env python3
"""Validate a Project Templates operation payload before approval (no live calls)."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
import uuid
from datetime import date
from pathlib import Path
from typing import Any


ROOT_REQUIRED = ("ProjectTemplateName", "ProjectTemplateNumber")
ROOT_REQUIRED_ALTERNATIVES = (
    ("BusinessUnitName", "BusinessUnitId"),
    ("ProjectUnitName", "ProjectUnitId"),
    ("OwningOrganizationName", "OwningOrganizationId"),
    ("ProjectTypeName", "ProjectTypeId"),
    ("LegalEntityName", "LegalEntityId"),
)
ROOT_CREATE_FIELDS = {
    "AllowCapitalizedInterestFlag",
    "AllowCrossChargeFlag",
    "AssetAllocationMethodCode",
    "AutoAssetCreateFlag",
    "AutoAssetLineAllocateMode",
    "BurdenScheduleFixedDate",
    "BurdenScheduleId",
    "BurdenScheduleName",
    "BusinessUnitId",
    "BusinessUnitName",
    "CapitalEventProcessingMethodCode",
    "CapitalizedInterestRateScheduleId",
    "CapitalizedInterestRateScheduleName",
    "CapitalizedInterestStopDate",
    "CrossChargeLaborFlag",
    "CrossChargeNonLaborFlag",
    "CurrencyConvDate",
    "CurrencyConvDateTypeCode",
    "CurrencyConvRateType",
    "EnableBudgetaryControlFlag",
    "IncludeNotesInKPINotificationsFlag",
    "InitialProjectStatus",
    "InitialProjectStatusCode",
    "KPINotificationEnabledFlag",
    "LaborTpFixedDate",
    "LaborTpSchedule",
    "LaborTpScheduleId",
    "LegalEntityId",
    "LegalEntityName",
    "NlTransferPriceFixedDate",
    "NlTransferPriceSchedule",
    "NlTransferPriceScheduleId",
    "OwningOrganizationId",
    "OwningOrganizationName",
    "PlanningProjectFlag",
    "ProjectCurrencyCode",
    "ProjectEndDate",
    "ProjectManagerEmail",
    "ProjectPlanType",
    "ProjectPlanTypeId",
    "ProjectPriorityCode",
    "ProjectStartDate",
    "ProjectTemplateDescription",
    "ProjectTemplateEndDate",
    "ProjectTemplateName",
    "ProjectTemplateNumber",
    "ProjectTemplateStartDate",
    "ProjectTypeId",
    "ProjectTypeName",
    "ProjectUnitId",
    "ProjectUnitName",
    "ServiceType",
    "ServiceTypeCode",
    "SourceApplicationCode",
    "SourceReference",
    "TransactionControlFlag",
    "WorkType",
    "WorkTypeId",
}
ROOT_CREATE_CHILDREN = {
    "ProjectClassifications",
    "ProjectCustomers",
    "ProjectTeamMembers",
    "ProjectTransactionControls",
    "ProviderBusinessUnits",
    "QuickEntries",
    "SetupOptions",
    "Tasks",
}
CHILD_METHODS = {
    "ProjectClassifications": {"POST", "PATCH", "DELETE"},
    "ProjectCustomers": {"POST"},
    "ProjectTeamMembers": {"POST", "PATCH", "DELETE"},
    "ProjectTransactionControls": {"POST"},
    "ProviderBusinessUnits": {"POST", "DELETE"},
    "QuickEntries": {"POST"},
    "SetupOptions": {"POST", "PATCH"},
    "Tasks": {"POST", "PATCH", "DELETE"},
    "TaskTransactionControls": {"POST"},
}
TASK_RUNTIME_REQUIRED = (
    "TaskName",
    "CrossChargeLaborFlag",
    "CrossChargeNonLaborFlag",
)
BOOLEAN_DEFAULTS = ("CrossChargeLaborFlag", "CrossChargeNonLaborFlag", "AllowCrossChargeFlag", "AutoAssetCreateFlag")
ASSET_ALLOCATION_CODES = {"AU", "CC", "EC", "SC", "SE", "CE", "N"}
PROJECT_TYPE_DERIVED_FIELDS = {"AllowCapitalizedInterestFlag", "AssetAllocationMethodCode"}
AUDIT_FIELDS = {"CreatedBy", "CreationDate", "LastUpdatedBy", "LastUpdateDate", "LastUpdateLogin", "links", "@context"}
PRIORITY_ENDPOINT = "/fscmRestApi/resources/11.13.18.05/standardLookups/PJF_PROJECT_PRIORITY_CODE/child/lookupCodes"
PUBLISHED_CONTRACT = json.loads((Path(__file__).resolve().parents[1] /
    "references/project-template-operation-contracts.json").read_text(encoding="utf-8"))
LOOKUP_DISPLAY_FIELDS = {
    "projectTemplates": (("AssetAllocationMethod", "AssetAllocationMethodCode", "PJC_ASSET_ALLOCATION_METHOD"),
                         ("CurrencyConvDateType", "CurrencyConvDateTypeCode", "PJF_DEF_RATE_DATE_CODE")),
    "Tasks": (("PercentCompleteCalculationMethod", "PercentCompleteCalculationMethodCode", "PJF_PERCENT_COMP_METHOD"),
              ("ProgressETCMethod", "ProgressETCMethodCode", "PJF_ETC_METHOD")),
}


def priority_lookup_request(meaning: str) -> dict[str, Any]:
    """Describe the workflow-selected GET; never perform a network call here."""
    if not isinstance(meaning, str) or not meaning.strip():
        raise ValueError("project priority display name must be nonblank")
    return {"method": "GET", "path": PRIORITY_ENDPOINT,
            "query": {"q": "Meaning='" + meaning.replace("'", "''") + "'"}}


def _create_metadata(describe: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    contract = describe.get("operationMetadata")
    if contract is not None:
        if not isinstance(contract, dict) or contract.get("method") != "POST" or contract.get("surface") != "projectTemplates":
            raise ValueError("root create operationMetadata must identify POST projectTemplates")
        resource = contract.get("resource")
        if not isinstance(resource, dict) or not isinstance(resource.get("attributes"), list):
            raise ValueError("create operationMetadata.resource must contain operation-specific attributes")
        return resource, True
    return _resource_metadata(describe), False


def prepare_payload(payload: Any, describe: dict[str, Any], operation: str = "create",
                    child_family: str | None = None, *, priority_lookup: Any = None,
                    effective_date: str | None = None, lookup_evidence: Any = None) -> dict[str, Any]:
    """Apply documented create defaults and resolve supplied lookup evidence offline."""
    prepared = copy.deepcopy(payload)
    issues: list[str] = []
    defaults: list[dict[str, Any]] = []
    resolutions: list[dict[str, Any]] = []
    if not isinstance(prepared, dict):
        return dict(payload=prepared, issues=issues, defaults=defaults, resolutions=resolutions)

    def default(obj: dict[str, Any], field: str, value: Any, path: str, source: str) -> None:
        if field not in obj:
            obj[field] = value
            defaults.append(dict(path=path + "." + field, value=value, source=source))

    root_create = operation == "create" and child_family is None
    task_create = operation == "create_child" and child_family == "Tasks"
    if root_create:
        contract = describe.get("operationMetadata", {})
        target_defaults = {}
        if isinstance(contract, dict) and contract.get("method") == "POST" and contract.get("surface") == "projectTemplates":
            resource = contract.get("resource", {})
            attributes = resource.get("attributes", []) if isinstance(resource, dict) else []
            if isinstance(attributes, list):
                target_defaults = {attr["name"]: attr["default"] for attr in attributes if isinstance(attr, dict)
                    and isinstance(attr.get("name"), str) and attr.get("default") is not None}
        for field in BOOLEAN_DEFAULTS:
            default(prepared, field, target_defaults.get(field, False), "root",
                    "operation-specific target create default" if field in target_defaults else "documented create default")
        field = "AutoAssetLineAllocateMode"
        default(prepared, field, target_defaults.get(field, "ALL_COSTS"), "root",
                "operation-specific target create default" if field in target_defaults else "documented create default")
    tasks = prepared.get("Tasks", []) if root_create else ([prepared] if task_create else [])
    owner = prepared if root_create else describe.get("parentContext", {})
    if isinstance(tasks, list):
        if root_create:
            # Allocate once during preparation; approval/revalidation consumes
            # the persisted body and never replaces supplied identifiers.
            reserved = {row["ExternalTaskId"] for row in tasks if isinstance(row, dict)
                        and isinstance(row.get("ExternalTaskId"), str)}
            namespace = None
            for index, task in enumerate(tasks):
                if not isinstance(task, dict) or "ExternalTaskId" in task:
                    continue
                number = task.get("TaskNumber")
                if isinstance(number, str) and number.strip():
                    candidate = number
                    source = "FSCR generated external ID from supplied TaskNumber"
                else:
                    if namespace is None:
                        namespace = "FSCR-" + uuid.uuid4().hex
                    candidate = namespace + "-" + str(index + 1).zfill(3)
                    source = "FSCR generated request-unique task sequence"
                if candidate in reserved:
                    issues.append(f"root.Tasks[{index}] generated ExternalTaskId conflicts with another task; supply unique identifiers")
                    continue
                reserved.add(candidate)
                default(task, "ExternalTaskId", candidate, f"root.Tasks[{index}]", source)
        by_id = {row["ExternalTaskId"]: row for row in tasks if isinstance(row, dict)
                 and isinstance(row.get("ExternalTaskId"), str) and row["ExternalTaskId"].strip()}
        def inherited(task: dict[str, Any], field: str, seen: set[int]) -> tuple[Any, str] | None:
            if id(task) in seen:
                return None
            if field in task:
                return task[field], "parent task." + field
            seen = seen | {id(task)}
            parent_id = task.get("ExternalParentTaskId")
            if parent_id is not None:
                if not isinstance(parent_id, str):
                    return None
                parent = by_id.get(parent_id) if root_create else describe.get("parentTaskContext")
                if not isinstance(parent, dict) or parent.get("ExternalTaskId") != parent_id:
                    return None
                return inherited(parent, field, seen)
            if isinstance(owner, dict) and isinstance(owner.get(field), bool):
                return owner[field], "project." + field
            return None
        for index, task in enumerate(tasks):
            if not isinstance(task, dict):
                continue
            path = f"root.Tasks[{index}]" if root_create else "child"
            if task_create and "TaskOrganizationName" not in task and "TaskOrganizationId" not in task:
                # FSCR input policy requested by the developer: reuse the
                # template organization, without claiming a Fusion default.
                owner_fields = [field for field in ("OwningOrganizationName", "OwningOrganizationId")
                                if isinstance(owner, dict) and field in owner]
                if len(owner_fields) > 1:
                    issues.append(path + " cannot reuse conflicting owning organization representations")
                elif len(owner_fields) == 1 and _nonblank(owner[owner_fields[0]]):
                    source_field = owner_fields[0]
                    task_field = source_field.replace("Owning", "Task")
                    default(task, task_field, owner[source_field], path,
                            "FSCR input policy: template." + source_field)
            if task_create and "TaskOrganizationName" not in task and "TaskOrganizationId" not in task:
                contract = describe.get("operationMetadata", {})
                if isinstance(contract, dict) and contract.get("method") == "POST" and contract.get("surface") == ("projectTemplates" if root_create else "Tasks"):
                    resource = contract.get("resource", {})
                    if root_create and isinstance(resource, dict):
                        children = resource.get("children", {})
                        resource = children.get("Tasks", {}) if isinstance(children, dict) else {}
                    attributes = resource.get("attributes", []) if isinstance(resource, dict) else []
                    attributes = attributes if isinstance(attributes, list) else []
                    candidates = [(attr["name"], attr["default"]) for attr in attributes if isinstance(attr, dict)
                        and attr.get("name") in ("TaskOrganizationName", "TaskOrganizationId")
                        and "default" in attr and _nonblank(attr["default"])]
                    if len(candidates) == 1:
                        field, value = candidates[0]
                        default(task, field, value, path, "operation-specific target create default")
                    elif len(candidates) > 1:
                        issues.append(path + " has ambiguous operation-specific task organization defaults")
            for field in BOOLEAN_DEFAULTS[:2]:
                if field not in task:
                    value = inherited(task, field, set())
                    if value is None:
                        issues.append(path + "." + field + " needs evidenced project/parent-task inheritance or an explicit boolean")
                    else:
                        default(task, field, value[0], path, value[1])
    quick_entries = prepared.get("QuickEntries", []) if root_create else ([prepared] if operation == "create_child" and child_family == "QuickEntries" else [])
    if isinstance(quick_entries, list):
        for index, entry in enumerate(quick_entries):
            if isinstance(entry, dict):
                default(entry, "MandatoryFlag", False, f"root.QuickEntries[{index}]" if root_create else "child", "documented quick-entry create default")

    aliases = [field for field in ("ProjectPriority", "ProjectPriorityName") if field in prepared]
    if aliases and not (root_create or operation == "update"):
        issues.append("project priority display-name resolution applies only to root create/update")
    elif aliases:
        if len(aliases) != 1 or "ProjectPriorityCode" in prepared:
            issues.append("supply exactly one priority display name or ProjectPriorityCode")
        else:
            meaning = prepared[aliases[0]]
            try:
                request = priority_lookup_request(meaning)
            except ValueError as exc:
                issues.append(str(exc))
                request = None
            as_of = _parse_date(effective_date, "priority effective_date", issues)
            if (not isinstance(priority_lookup, dict) or priority_lookup.get("lookupType") != "PJF_PROJECT_PRIORITY_CODE"
                    or not isinstance(priority_lookup.get("items"), list) or priority_lookup.get("hasMore") is not False):
                issues.append("priority resolution requires complete paginated lookup evidence with hasMore=false")
            elif request is not None and as_of is not None:
                matches = []
                for row in priority_lookup["items"]:
                    if not isinstance(row, dict) or not isinstance(row.get("Meaning"), str):
                        issues.append("priority lookup evidence contains a malformed member")
                        continue
                    if row["Meaning"] != meaning:
                        continue
                    if row.get("EnabledFlag") not in ("Y", "N"):
                        issues.append("priority lookup evidence has an invalid EnabledFlag")
                    if row.get("EnabledFlag") != "Y":
                        continue
                    if any(field not in row for field in ("LookupCode", "StartDateActive", "EndDateActive")):
                        issues.append("priority lookup evidence is missing code or effective-date fields")
                    dates = []
                    for field in ("StartDateActive", "EndDateActive"):
                        value = row.get(field)
                        dates.append(_parse_date(value, "priority." + field, issues) if value is not None else None)
                    start, end = dates
                    if ((start is None or start <= as_of) and (end is None or as_of <= end)):
                        matches.append(row)
                        if not isinstance(row.get("LookupCode"), str) or not row["LookupCode"].strip():
                            issues.append("priority lookup evidence has an eligible row without a nonblank LookupCode")
                if len(matches) != 1:
                    issues.append(f"blocking priority lookup ambiguity: expected one enabled effective match, found {len(matches)}")
                elif not issues:
                    row = matches[0]
                    prepared.pop(aliases[0])
                    prepared["ProjectPriorityCode"] = row["LookupCode"]
                    resolutions.append(dict(field="ProjectPriorityCode", request=request, Meaning=meaning,
                        LookupCode=row["LookupCode"], EnabledFlag=row["EnabledFlag"],
                        StartDateActive=row.get("StartDateActive"), EndDateActive=row.get("EndDateActive"),
                        effective_date=effective_date, match_count=1))
    objects = [(prepared, "root", "projectTemplates")] if child_family is None else [(prepared, "child", child_family)]
    if child_family is None and isinstance(prepared.get("Tasks"), list):
        objects += [(row, f"root.Tasks[{index}]", "Tasks") for index, row in enumerate(prepared["Tasks"]) if isinstance(row, dict)]
    for obj, path, surface in objects:
        for alias, code, lookup_type in LOOKUP_DISPLAY_FIELDS.get(surface, ()):
            if alias not in obj:
                continue
            evidence_key = path + "." + code
            if code in obj:
                issues.append(evidence_key + " must use one display name or code, not both")
                continue
            evidence = lookup_evidence.get(evidence_key) if isinstance(lookup_evidence, dict) else None
            # The same exact/enabled/effective/cardinality contract is shared by
            # documented standard lookup types, with no HTTP from this script.
            synthetic = {"ProjectPriority": obj[alias]}
            proxy = {**evidence, "lookupType": "PJF_PROJECT_PRIORITY_CODE"} if isinstance(evidence, dict) and evidence.get("lookupType") == lookup_type else None
            resolved = prepare_payload(synthetic, describe, "update", priority_lookup=proxy, effective_date=effective_date)
            if resolved["issues"]:
                issues += [evidence_key + ": " + issue for issue in resolved["issues"]]
                continue
            obj.pop(alias)
            obj[code] = resolved["payload"]["ProjectPriorityCode"]
            record = resolved["resolutions"][0]
            record["field"] = evidence_key
            record["lookupType"] = lookup_type
            record["request"]["path"] = PRIORITY_ENDPOINT.replace("PJF_PROJECT_PRIORITY_CODE", lookup_type)
            resolutions.append(record)
    return dict(payload=prepared, issues=issues, defaults=defaults, resolutions=resolutions)
TASK_REQUIRED_ALTERNATIVES = (
    ("TaskOrganizationName", "TaskOrganizationId"),
)
EXCLUSIVE_ROOT_PAIRS = (
    ("BusinessUnitName", "BusinessUnitId"),
    ("ProjectUnitName", "ProjectUnitId"),
    ("OwningOrganizationName", "OwningOrganizationId"),
    ("ProjectTypeName", "ProjectTypeId"),
    ("ProjectPlanType", "ProjectPlanTypeId"),
    ("LegalEntityName", "LegalEntityId"),
    ("InitialProjectStatus", "InitialProjectStatusCode"),
    ("BurdenScheduleName", "BurdenScheduleId"),
    ("CapitalizedInterestRateScheduleName", "CapitalizedInterestRateScheduleId"),
    ("LaborTpSchedule", "LaborTpScheduleId"),
    ("NlTransferPriceSchedule", "NlTransferPriceScheduleId"),
    ("ServiceType", "ServiceTypeCode"),
    ("WorkType", "WorkTypeId"),
)
EXCLUSIVE_TASK_PAIRS = (
    ("TaskOrganizationName", "TaskOrganizationId"),
    ("ServiceType", "ServiceTypeCode"),
    ("WorkType", "WorkTypeId"),
    ("BurdenSchedule", "BurdenScheduleId"),
    ("LaborTpSchedule", "LaborTpScheduleId"),
    ("NlTransferPriceSchedule", "NlTransferPriceScheduleId"),
)
AT_MOST_ONE_TASK_GROUPS = (
    ("TaskManagerEmail", "TaskManagerName", "TaskManagerPersonId"),
)
TASK_CREATE_FORBIDDEN = {"TaskId", "ParentTaskId", "LowestLevelTask", "links"}
CHILD_REFERENCE_PAIRS = {
    "ProjectClassifications": (("ClassCategory", "ClassCategoryId"), ("ClassCode", "ClassCodeId")),
    "ProviderBusinessUnits": (("BusinessUnitName", "BusinessUnitId"),),
    "SetupOptions": (("OptionName", "OptionCode"),),
    "ProjectTransactionControls": (("Billable", "BillableHint"), ("Capitalizable", "CapitalizableHint"),
        ("Chargeable", "ChargeableHint"), ("PersonType", "PersonTypeHint"),
        ("ExpenditureCategoryId", "ExpenditureCategoryName"), ("ExpenditureTypeId", "ExpenditureTypeName"),
        ("Job", "JobId"), ("Organization", "OrganizationId"), ("NonLaborResourceId", "NonLaborResourceName")),
}
CHILD_REFERENCE_PAIRS["TaskTransactionControls"] = CHILD_REFERENCE_PAIRS["ProjectTransactionControls"]
CHILD_REFERENCE_GROUPS = {
    "ProjectCustomers": (("PartyId", "PartyName", "PartyNumber"),),
    "ProjectTransactionControls": (("PersonName", "PersonId", "PersonNumber", "EmailAddress"),),
    "TaskTransactionControls": (("PersonName", "PersonId", "PersonNumber", "EmailAddress"),),
}
DATE_FIELDS = {
    "ProjectTemplateStartDate",
    "ProjectTemplateEndDate",
    "ProjectStartDate",
    "ProjectEndDate",
    "TaskStartDate",
    "TaskFinishDate",
    "TransactionStartDate",
    "TransactionCompletionDate",
}


def _nonblank(value: Any) -> bool:
    return value is not None and (not isinstance(value, str) or bool(value.strip()))


def _parse_date(value: Any, path: str, issues: list[str]) -> date | None:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        issues.append(f"{path} must be an ISO YYYY-MM-DD string")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        issues.append(f"{path} must be an ISO YYYY-MM-DD date")
        return None


def _validate_type(value: Any, metadata: dict[str, Any], path: str, issues: list[str]) -> None:
    if value is None and metadata.get("nullable") is True:
        return
    kind = metadata.get("type")
    if metadata.get("name") in {*BOOLEAN_DEFAULTS, "AllowCapitalizedInterestFlag"}:
        kind = "boolean"
    if kind == "boolean" and not isinstance(value, bool):
        issues.append(f"{path} must be a JSON boolean, not a string boolean")
    elif kind == "integer" and (isinstance(value, bool) or not isinstance(value, int)):
        issues.append(f"{path} must be an integer")
    elif kind == "number" and (isinstance(value, bool) or not isinstance(value, (int, float))):
        issues.append(f"{path} must be numeric")
    elif kind in {"string", "date"} and not isinstance(value, str):
        issues.append(f"{path} must be a string")
    elif kind == "array" and not isinstance(value, list):
        issues.append(f"{path} must be an array")
    elif kind == "object" and not isinstance(value, dict):
        issues.append(f"{path} must be an object")

    max_length = metadata.get("maxLength")
    if max_length is None and kind == "string":
        max_length = metadata.get("precision")
    if max_length is not None and isinstance(value, str) and len(value) > int(max_length):
        issues.append(f"{path} exceeds maximum length {max_length}")

    if metadata.get("type") == "date" or metadata.get("format") == "date" or metadata.get("name") in DATE_FIELDS:
        _parse_date(value, path, issues)


def _check_exclusive_pairs(
    value: dict[str, Any], pairs: tuple[tuple[str, str], ...], path: str, issues: list[str]
) -> None:
    for left, right in pairs:
        if left in value and right in value:
            issues.append(f"{path} must not contain both {left} and {right}")


def _check_at_most_one_groups(
    value: dict[str, Any], groups: tuple[tuple[str, ...], ...], path: str, issues: list[str]
) -> None:
    for group in groups:
        present = [field for field in group if field in value]
        if len(present) > 1:
            issues.append(f"{path} must contain at most one of {', '.join(group)}")


def _check_required_alternatives(
    value: dict[str, Any], groups: tuple[tuple[str, ...], ...], path: str, issues: list[str]
) -> None:
    for group in groups:
        if not any(_nonblank(value.get(field)) for field in group):
            issues.append(f"{path} requires one of {', '.join(group)}")


def _resource_metadata(describe: dict[str, Any]) -> dict[str, Any]:
    try:
        return describe["Resources"]["projectTemplates"]
    except (KeyError, TypeError) as exc:
        raise ValueError("metadata must contain Resources.projectTemplates") from exc


def _metadata_required_fields(resource: dict[str, Any]) -> set[str]:
    """Return operation-required fields without treating nullable=false as required."""
    required = {
        field for field in resource.get("required", []) if isinstance(field, str)
    }
    for attribute in resource.get("attributes", []):
        if not isinstance(attribute, dict) or not isinstance(attribute.get("name"), str):
            continue
        if attribute.get("required") is True or attribute.get("mandatory") is True:
            required.add(attribute["name"])
    return required


def _published_schema(surface: str, method: str) -> dict[str, Any]:
    schema = PUBLISHED_CONTRACT["operations"][surface + ":" + method]["schema"]
    if "$ref" in schema:
        return PUBLISHED_CONTRACT["schemas"][schema["$ref"].rsplit("/", 1)[-1]]
    return schema


def _supported_alternatives(surface: str, attributes: Any) -> tuple[tuple[str, ...], ...]:
    groups = (EXCLUSIVE_ROOT_PAIRS if surface == "projectTemplates" else
              EXCLUSIVE_TASK_PAIRS + AT_MOST_ONE_TASK_GROUPS if surface == "Tasks" else
              CHILD_REFERENCE_PAIRS.get(surface, ()) + CHILD_REFERENCE_GROUPS.get(surface, ()))
    return tuple(group for group in groups if set(group) <= set(attributes))


def _known_task_bounds(task: dict[str, Any], context: Any, path: str) -> list[str]:
    if not isinstance(context, dict):
        return []
    issues = []
    for field in ("TaskStartDate", "TaskFinishDate"):
        if task.get(field) is None:
            continue
        value = _parse_date(task[field], path + "." + field, issues)
        for bound, lower in (("ProjectStartDate", True), ("ProjectEndDate", False)):
            if context.get(bound) is None:
                continue
            limit = _parse_date(context[bound], "project context." + bound, issues)
            if value and limit and ((lower and value < limit) or (not lower and value > limit)):
                issues.append(path + "." + field + " must fall within known project schedule bounds")
    return issues


def _metadata_shape_issues(describe: Any) -> list[str]:
    if not isinstance(describe, dict):
        return ["metadata must be a JSON object"]
    if "operationMetadata" in describe:
        contract = describe["operationMetadata"]
        if not isinstance(contract, dict):
            return ["operationMetadata must be a JSON object"]
        resource = contract.get("resource")
    else:
        try:
            resource = _resource_metadata(describe)
        except ValueError as exc:
            return [str(exc)]
    def check(item: Any, path: str) -> list[str]:
        if not isinstance(item, dict) or not isinstance(item.get("attributes"), list):
            return [path + " must contain an attributes array"]
        issues = []
        for attr in item["attributes"]:
            if not isinstance(attr, dict) or not isinstance(attr.get("name"), str):
                issues.append(path + " has an invalid attribute definition")
                continue
            for field in ("precision", "maxLength"):
                if field in attr:
                    try:
                        if int(attr[field]) < 0:
                            raise ValueError()
                    except (TypeError, ValueError):
                        issues.append(path + " has invalid " + field + " metadata")
        if "required" in item and (not isinstance(item["required"], list) or any(not isinstance(field, str) for field in item["required"])):
            issues.append(path + " required must be an array of field names")
        children = item.get("children", {})
        if not isinstance(children, dict):
            issues.append(path + " children must be an object")
        else:
            for name, child in children.items():
                issues += check(child, path + "." + name)
        return issues
    return check(resource, "metadata resource")


def _published_checks(payload: Any, schema: dict[str, Any], path: str,
                      surface: str, method: str) -> list[str]:
    """Validate the published request, never a response or describe field list."""
    if "$ref" in schema:
        schema = PUBLISHED_CONTRACT["schemas"][schema["$ref"].rsplit("/", 1)[-1]]
    issues: list[str] = []
    properties = schema.get("properties", {})
    if not isinstance(payload, dict):
        return [path + " must be a JSON object"]
    if not payload:
        issues.append(path + " must contain at least one requested field")
    for field, value in payload.items():
        if field not in properties or properties[field].get("readOnly") is True or (surface == "Tasks" and method == "POST" and field in TASK_CREATE_FORBIDDEN):
            issues.append(path + " contains unsupported or nonwritable attribute " + field)
            continue
        spec = properties[field]
        if spec.get("type") == "array":
            if not isinstance(value, list):
                issues.append(path + "." + field + " must be an array")
            else:
                for index, row in enumerate(value):
                    issues += _published_checks(row, spec["items"], f"{path}.{field}[{index}]", field, method)
            continue
        _validate_type(value, {**spec, "name": field}, path + "." + field, issues)
        if value is None and spec.get("nullable") is False:
            issues.append(path + "." + field + " must not be null")
    groups = TASK_REQUIRED_ALTERNATIVES if surface == "Tasks" else ROOT_REQUIRED_ALTERNATIVES if surface == "projectTemplates" else ()
    if method == "POST":
        required = set(schema.get("required", []))
        if surface == "Tasks" and path.startswith("root.Tasks["):
            # Nested template create can derive the task organization in Fusion.
            # Preserve the published schema; fresh operation-specific target
            # requirements are still checked separately below.
            required -= {"TaskOrganizationName", "TaskOrganizationId"}
        _check_metadata_required(payload, required, groups, path, issues)
    pairs = CHILD_REFERENCE_PAIRS
    _check_exclusive_pairs(payload, pairs.get(surface, ()), path, issues)
    if surface == "ProjectCustomers":
        party = ("PartyId", "PartyName", "PartyNumber")
        _check_at_most_one_groups(payload, (party,), path, issues)
        if method == "POST":
            _check_required_alternatives(payload, (party,), path, issues)
    if surface == "ProjectClassifications" and method == "POST":
        _check_required_alternatives(payload, pairs[surface], path, issues)
    if surface == "ProviderBusinessUnits" and method == "POST":
        _check_required_alternatives(payload, pairs[surface], path, issues)
    if surface == "SetupOptions" and method == "POST":
        _check_required_alternatives(payload, pairs[surface], path, issues)
    enums = {}
    if surface == "projectTemplates":
        enums = {"AssetAllocationMethodCode": ASSET_ALLOCATION_CODES,
            "AutoAssetLineAllocateMode": {"ALL_COSTS", "DIRECT_COSTS"},
            "CapitalEventProcessingMethodCode": {"M", "P", "N"},
            "CurrencyConvDateTypeCode": {"A", "P", "T", "F"}}
        if isinstance(payload.get("Tasks"), list):
            for index, task in enumerate(payload["Tasks"]):
                if isinstance(task, dict):
                    issues += _known_task_bounds(task, payload, f"{path}.Tasks[{index}]")
    elif surface == "Tasks":
        enums = {"PercentCompleteCalculationMethodCode": {"COST", "EFFORT", "MANUAL"},
            "ProgressETCMethodCode": {"REMAINING_PLAN", "MANUAL"}}
        _check_exclusive_pairs(payload, EXCLUSIVE_TASK_PAIRS, path, issues)
        _check_at_most_one_groups(payload, AT_MOST_ONE_TASK_GROUPS, path, issues)
        for field in ("TaskNumber", "ExternalTaskId", "ExternalParentTaskId"):
            if field in payload and (not isinstance(payload[field], str) or not payload[field].strip()):
                issues.append(path + "." + field + " must be a nonblank string")
    elif surface == "QuickEntries":
        enums = {"FieldCode": {"TEAM_MEMBER", "CLASSIFICATION", "LEGAL_ENTITY_ID", "CARRYING_OUT_ORGANIZATION_ID",
            "PARTNER_ORG", "PRIORITY_CODE", "CUSTOMER_NAME", "DESCRIPTION", "PROJECT_STATUS_CODE", "SUPPLIER_ORG"}}
        field = payload.get("FieldCode")
        if field in ("TEAM_MEMBER", "CLASSIFICATION") and not _nonblank(payload.get("Specification")):
            issues.append(path + ".Specification is required for " + field)
        elif field is not None and field not in ("TEAM_MEMBER", "CLASSIFICATION") and "Specification" in payload and payload["Specification"] is not None:
            issues.append(path + ".Specification applies only to TEAM_MEMBER or CLASSIFICATION")
    elif surface in ("ProjectTransactionControls", "TaskTransactionControls"):
        enums = {"Billable": {"N", "T"}, "Capitalizable": {"N", "T"}, "Chargeable": {"Y", "N"},
            "BillableHint": {"No", "Task"}, "CapitalizableHint": {"No", "Task"}, "ChargeableHint": {"Yes", "No"},
            "PersonType": {"EMP", "CWK"}, "PersonTypeHint": {"Employee", "Contingent Worker"}}
        people = ("PersonName", "PersonId", "PersonNumber", "EmailAddress")
        _check_at_most_one_groups(payload, (people,), path, issues)
        if any(_nonblank(payload.get(field)) for field in ("Job", "JobId")):
            _check_required_alternatives(payload, (people,), path, issues)
        if any(_nonblank(payload.get(field)) for field in ("Organization", "OrganizationId")):
            _check_required_alternatives(payload, (people, ("Job", "JobId")), path, issues)
    for field, allowed in enums.items():
        if field in payload and payload[field] is not None and (not isinstance(payload[field], str) or payload[field] not in allowed):
            issues.append(path + "." + field + " must be one of " + ", ".join(sorted(allowed)))
    for field in ("CodePercentage", "BillablePercent"):
        value = payload.get(field)
        if isinstance(value, (int, float)) and not isinstance(value, bool) and not 0 <= value <= 100:
            issues.append(path + "." + field + " must be between 0 and 100")
    for start, end in (("ProjectStartDate", "ProjectEndDate"), ("ProjectTemplateStartDate", "ProjectTemplateEndDate"),
                       ("TaskStartDate", "TaskFinishDate"), ("TransactionStartDate", "TransactionCompletionDate"),
                       ("StartDate", "FinishDate"), ("StartDateActive", "EndDateActive")):
        if payload.get(start) is not None and payload.get(end) is not None:
            first = _parse_date(payload[start], path + "." + start, issues)
            last = _parse_date(payload[end], path + "." + end, issues)
            if first and last and first > last:
                issues.append(path + "." + start + " must not be after " + end)
    return list(dict.fromkeys(issues))


def _check_metadata_required(
    value: dict[str, Any],
    required_fields: set[str],
    alternative_groups: tuple[tuple[str, ...], ...],
    path: str,
    issues: list[str],
) -> None:
    grouped_fields = {field for group in alternative_groups for field in group}
    for group in alternative_groups:
        if required_fields.intersection(group) and not any(
            _nonblank(value.get(field)) for field in group
        ):
            message = f"{path} requires one of {', '.join(group)}"
            if message not in issues:
                issues.append(message)
    for field in sorted(required_fields - grouped_fields):
        if not _nonblank(value.get(field)):
            message = f"{path} requires nonblank {field}"
            if message not in issues:
                issues.append(message)


def _validate_root_create(payload: Any, describe: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if not isinstance(payload, dict):
        return ["payload root must be a JSON object"]

    try:
        root, operation_specific = _create_metadata(describe)
    except ValueError as exc:
        return [str(exc)]
    root_attributes = {
        item["name"]: item
        for item in root.get("attributes", [])
        if item.get("updatable") is True and item.get("readOnly") is not True and item.get("name") not in AUDIT_FIELDS
    }
    for name, spec in _published_schema("projectTemplates", "POST")["properties"].items():
        if name in root_attributes:
            root_attributes[name] = {**spec, **root_attributes[name]}
    if not operation_specific:
        # These create defaults are documented independently of generic response metadata.
        for field in BOOLEAN_DEFAULTS:
            root_attributes.setdefault(field, {"name": field, "type": "boolean", "updatable": True})
        root_attributes.setdefault("AutoAssetLineAllocateMode", {"name": "AutoAssetLineAllocateMode", "type": "string", "updatable": True})
    children = root.get("children", {})
    allowed_root = (set(root_attributes) & ROOT_CREATE_FIELDS) | (
        set(children) & ROOT_CREATE_CHILDREN
    )

    for field in sorted(set(payload) - allowed_root):
        issues.append(f"root contains unsupported or nonwritable attribute {field}")
    for field in ROOT_REQUIRED:
        if not _nonblank(payload.get(field)):
            issues.append(f"root requires nonblank {field}")
    _check_required_alternatives(payload, ROOT_REQUIRED_ALTERNATIVES, "root", issues)
    required = (_metadata_required_fields(root) & allowed_root) if operation_specific else set()
    conflicting_derived = (required & PROJECT_TYPE_DERIVED_FIELDS) - set(payload)
    for field in sorted(conflicting_derived):
        issues.append(
            f"root contract conflict: operation metadata requires {field}, but its documented "
            "omission derives from project type; reconcile the create contract before preview, "
            "do not request a value or silently override derivation"
        )
    _check_metadata_required(
        payload,
        required - conflicting_derived,
        _supported_alternatives("projectTemplates", root_attributes),
        "root",
        issues,
    )
    _check_exclusive_pairs(payload, EXCLUSIVE_ROOT_PAIRS, "root", issues)
    # Schedule fields can derive from the project type; a fixed date alone does
    # not prove that the caller must also supply a schedule representation.

    if "ProjectPlanTypeName" in payload:
        issues.append("root must use ProjectPlanType, never ProjectPlanTypeName")
    if "AssetAllocationMethodCode" in payload and (not isinstance(payload["AssetAllocationMethodCode"], str) or payload["AssetAllocationMethodCode"] not in ASSET_ALLOCATION_CODES):
        issues.append("root.AssetAllocationMethodCode must be one of AU, CC, EC, SC, SE, CE, N")

    for field, value in payload.items():
        if field in root_attributes:
            _validate_type(value, root_attributes[field], f"root.{field}", issues)

    template_start = (
        _parse_date(payload["ProjectTemplateStartDate"], "root.ProjectTemplateStartDate", issues)
        if payload.get("ProjectTemplateStartDate") is not None
        else None
    )
    template_end = (
        _parse_date(payload["ProjectTemplateEndDate"], "root.ProjectTemplateEndDate", issues)
        if payload.get("ProjectTemplateEndDate") is not None
        else None
    )
    if template_start and template_end and template_start > template_end:
        issues.append("root.ProjectTemplateStartDate must not be after ProjectTemplateEndDate")

    for child_name, rows in payload.items():
        if child_name not in children:
            continue
        if not isinstance(rows, list):
            issues.append(f"root.{child_name} must be an array")
            continue
        child_attributes = {
            item["name"]: item
            for item in children[child_name].get("attributes", [])
            if item.get("updatable") is True and item.get("readOnly") is not True and item.get("name") not in AUDIT_FIELDS
        }
        child_schema = PUBLISHED_CONTRACT["schemas"].get("projectTemplates-" + child_name + "-item-post-request", {})
        for name, spec in child_schema.get("properties", {}).items():
            if name in child_attributes:
                child_attributes[name] = {**spec, **child_attributes[name]}
        if child_name == "Tasks":
            child_attributes = {
                name: item for name, item in child_attributes.items() if name not in TASK_CREATE_FORBIDDEN
            }
        for index, row in enumerate(rows):
            row_path = f"root.{child_name}[{index}]"
            if not isinstance(row, dict):
                issues.append(f"{row_path} must be an object")
                continue
            for field in sorted(set(row) - set(child_attributes)):
                issues.append(f"{row_path} contains unsupported or nonwritable attribute {field}")
            for field, value in row.items():
                if field in child_attributes:
                    _validate_type(value, child_attributes[field], f"{row_path}.{field}", issues)
            _check_metadata_required(
                row,
                (_metadata_required_fields(children[child_name]) & set(child_attributes)) if operation_specific else set(),
                _supported_alternatives(child_name, child_attributes),
                row_path,
                issues,
            )
            if child_name == "Tasks":
                for field in TASK_RUNTIME_REQUIRED:
                    if not _nonblank(row.get(field)):
                        issues.append(f"{row_path} requires nonblank {field}")
                # Omitted nested task organization is resolved by Fusion and
                # verified from task readback, not copied from the root name.
                _check_exclusive_pairs(row, EXCLUSIVE_TASK_PAIRS, row_path, issues)
                _check_at_most_one_groups(row, AT_MOST_ONE_TASK_GROUPS, row_path, issues)
                task_start = (
                    _parse_date(row["TaskStartDate"], f"{row_path}.TaskStartDate", issues)
                    if row.get("TaskStartDate") is not None
                    else None
                )
                task_finish = (
                    _parse_date(row["TaskFinishDate"], f"{row_path}.TaskFinishDate", issues)
                    if row.get("TaskFinishDate") is not None
                    else None
                )
                if task_start and task_finish and task_start > task_finish:
                    issues.append(f"{row_path}.TaskStartDate must not be after TaskFinishDate")

    tasks = payload.get("Tasks", [])
    if isinstance(tasks, list):
        if tasks:
            dated_tasks = any(
                isinstance(row, dict)
                and ("TaskStartDate" in row or "TaskFinishDate" in row)
                for row in tasks
            )
            if dated_tasks:
                project_start = (
                    _parse_date(
                        payload["ProjectStartDate"],
                        "root.ProjectStartDate",
                        issues,
                    )
                    if payload.get("ProjectStartDate") is not None
                    else None
                )
                project_end = (
                    _parse_date(
                        payload["ProjectEndDate"],
                        "root.ProjectEndDate",
                        issues,
                    )
                    if payload.get("ProjectEndDate") is not None
                    else None
                )
                if project_start and project_end and project_start > project_end:
                    issues.append("root.ProjectStartDate must not be after ProjectEndDate")
                if project_start and project_end and project_start <= project_end:
                    for index, row in enumerate(tasks):
                        if not isinstance(row, dict):
                            continue
                        for field in ("TaskStartDate", "TaskFinishDate"):
                            if row.get(field) is None:
                                continue
                            task_date = _parse_date(
                                row[field], f"root.Tasks[{index}].{field}", issues
                            )
                            if task_date and not project_start <= task_date <= project_end:
                                issues.append(
                                    f"root.Tasks[{index}].{field} must fall within "
                                    "root.ProjectStartDate and root.ProjectEndDate"
                                )
        # Type validation may already have reported malformed values. Never pass
        # arbitrary JSON arrays/objects into sets, dictionary keys or graph walks.
        identifiers: list[dict[str, str]] = []
        for index, row in enumerate(tasks):
            valid: dict[str, str] = {}
            if isinstance(row, dict):
                for field in ("ExternalTaskId", "TaskNumber", "ExternalParentTaskId"):
                    if field not in row:
                        continue
                    value = row[field]
                    if not isinstance(value, str) or not value.strip():
                        issues.append(f"root.Tasks[{index}].{field} must be a nonblank string")
                    else:
                        valid[field] = value
            identifiers.append(valid)
        populated_external_ids = [row["ExternalTaskId"] for row in identifiers if "ExternalTaskId" in row]
        if len(populated_external_ids) != len(set(populated_external_ids)):
            issues.append("root.Tasks ExternalTaskId values must be unique within the payload")
        populated_task_numbers = [row["TaskNumber"] for row in identifiers if "TaskNumber" in row]
        if len(populated_task_numbers) != len(set(populated_task_numbers)):
            issues.append("root.Tasks TaskNumber values must be unique within the payload")
        known_external_ids = set(populated_external_ids)
        for index, row in enumerate(identifiers):
            parent = row.get("ExternalParentTaskId")
            if _nonblank(parent) and parent not in known_external_ids:
                issues.append(
                    f"root.Tasks[{index}].ExternalParentTaskId does not match an ExternalTaskId in the atomic payload"
                )
            if _nonblank(parent) and parent == row.get("ExternalTaskId"):
                issues.append(f"root.Tasks[{index}] cannot be its own external parent")

        parent_by_id = {
            row.get("ExternalTaskId"): row.get("ExternalParentTaskId")
            for row in identifiers
            if "ExternalTaskId" in row
        }
        for external_id in parent_by_id:
            seen: set[Any] = set()
            current = external_id
            while current in parent_by_id and _nonblank(parent_by_id[current]):
                if current in seen:
                    issues.append("root.Tasks ExternalParentTaskId relationships must be acyclic")
                    break
                seen.add(current)
                current = parent_by_id[current]
            if issues and issues[-1] == "root.Tasks ExternalParentTaskId relationships must be acyclic":
                break

    return issues


def _validate_operation_object(
    payload: Any, resource: dict[str, Any], path: str, *, create: bool,
    forbidden: set[str] | None = None,
    alternative_groups: tuple[tuple[str, ...], ...] = (),
) -> list[str]:
    if not isinstance(payload, dict):
        return [f"{path} must be a JSON object"]
    issues: list[str] = []
    attributes = {
        item["name"]: item for item in resource.get("attributes", [])
        if isinstance(item, dict) and item.get("updatable") is True
        and item.get("readOnly") is not True and item.get("name") not in AUDIT_FIELDS
        and item.get("name") not in (forbidden or set())
    }
    for field in sorted(set(payload) - set(attributes)):
        issues.append(f"{path} contains unsupported or nonwritable attribute {field}")
    for field, value in payload.items():
        if field in attributes:
            _validate_type(value, attributes[field], f"{path}.{field}", issues)
            if value is None and attributes[field].get("nullable") is False:
                issues.append(f"{path}.{field} must not be null")
    required = _metadata_required_fields(resource) & set(attributes)
    if create:
        # Collapse a published name/ID alternative only when both writable
        # representations exist in the selected operation. ID-only stays ID-only.
        supported_groups = tuple(group for group in alternative_groups if set(group) <= set(attributes))
        _check_metadata_required(payload, required, supported_groups, path, issues)
    else:
        # PATCH omits unchanged fields; required-on-create never means resend them.
        for field in required.intersection(payload):
            if not _nonblank(payload[field]):
                issues.append(f"{path}.{field} must not be blank")
    return issues


def validate_payload(
    payload: Any, describe: dict[str, Any], operation: str = "create",
    child_family: str | None = None,
    *, priority_lookup: Any = None, effective_date: str | None = None, lookup_evidence: Any = None,
) -> list[str]:
    """Validate exact method-specific metadata supplied by the selected workflow.

    Metadata is structural evidence, not permission or canonical-URI evidence.
    Root create retains its published field allowlist and nested-task overlay.
    Noncreate methods require operationMetadata identifying the selected surface,
    whose attributes must be narrowed to the exact published operation schema.
    """
    metadata_issues = _metadata_shape_issues(describe)
    if metadata_issues:
        return metadata_issues
    if operation == "create" and child_family is None:
        prepared = prepare_payload(payload, describe, operation, child_family,
                                   priority_lookup=priority_lookup, effective_date=effective_date, lookup_evidence=lookup_evidence)
        return list(dict.fromkeys(prepared["issues"] +
            _published_checks(prepared["payload"], _published_schema("projectTemplates", "POST"), "root", "projectTemplates", "POST") +
            _validate_root_create(prepared["payload"], describe)))
    methods = {"update": "PATCH", "end_date": "PATCH", "create_child": "POST",
               "update_child": "PATCH", "delete_child": "DELETE"}
    if operation not in methods:
        return [f"unsupported operation {operation}"]
    method = methods[operation]
    is_child = operation.endswith("_child")
    if is_child != (child_family is not None):
        return ["child_family is required only for a child operation"]
    if is_child and method not in CHILD_METHODS.get(child_family, set()):
        return [f"unsupported {method} operation for child family {child_family}"]
    contract = describe.get("operationMetadata")
    if not isinstance(contract, dict):
        return ["noncreate preflight requires exact operationMetadata"]
    expected_surface = child_family if is_child else "projectTemplates"
    if contract.get("method") != method or contract.get("surface") != expected_surface:
        return ["operationMetadata method/surface does not match the selected operation"]
    resource = contract.get("resource")
    if not isinstance(resource, dict) or not isinstance(resource.get("attributes"), list):
        return ["operationMetadata.resource must contain the exact operation attributes"]
    if operation == "delete_child":
        return [] if payload in (None, {}) else ["DELETE child operation must have no request body"]
    prepared = prepare_payload(payload, describe, operation, child_family,
                               priority_lookup=priority_lookup, effective_date=effective_date, lookup_evidence=lookup_evidence)
    payload = prepared["payload"]
    issues = _validate_operation_object(payload, resource, "child" if is_child else "root",
                                        create=operation == "create_child",
                                        forbidden=TASK_CREATE_FORBIDDEN if operation == "create_child" and child_family == "Tasks" else None,
                                        alternative_groups=_supported_alternatives(expected_surface,
                                            [attr['name'] for attr in resource['attributes'] if attr.get('updatable') is True and attr.get('readOnly') is not True]))
    issues = prepared["issues"] + issues
    issues += _published_checks(payload, _published_schema(expected_surface, method),
                                "child" if is_child else "root", expected_surface, method)
    if not isinstance(payload, dict):
        return issues
    if not payload:
        issues.append("write payload must contain at least one requested field")
    if operation == "end_date" and (set(payload) != {"ProjectTemplateEndDate"}
                                   or not _nonblank(payload.get("ProjectTemplateEndDate"))):
        issues.append("end_date requires only a nonblank ProjectTemplateEndDate")
    if not is_child:
        if set(payload).intersection(ROOT_CREATE_CHILDREN):
            issues.append("root nested PATCH row binding is not established by the 26C field schema; select a reviewed direct-child operation where published, or stop for operation-specific binding evidence")
        if "AssetAllocationMethodCode" in payload and (not isinstance(payload["AssetAllocationMethodCode"], str) or payload["AssetAllocationMethodCode"] not in ASSET_ALLOCATION_CODES):
            issues.append("root.AssetAllocationMethodCode must be one of AU, CC, EC, SC, SE, CE, N")
        _check_exclusive_pairs(payload, EXCLUSIVE_ROOT_PAIRS, "root", issues)
        if "ProjectPlanTypeName" in payload:
            issues.append("root must use ProjectPlanType, never ProjectPlanTypeName")
        for start, end in (("ProjectTemplateStartDate", "ProjectTemplateEndDate"),
                           ("ProjectStartDate", "ProjectEndDate")):
            if payload.get(start) is not None and payload.get(end) is not None:
                first = _parse_date(payload[start], f"root.{start}", issues)
                last = _parse_date(payload[end], f"root.{end}", issues)
                if first and last and first > last:
                    issues.append(f"root.{start} must not be after {end}")
    elif child_family == "Tasks":
        issues += _known_task_bounds(payload, describe.get("parentContext"), "child")
        if _nonblank(payload.get("ExternalParentTaskId")):
            parent = describe.get("parentTaskContext")
            if not isinstance(parent, dict) or parent.get("ExternalTaskId") != payload["ExternalParentTaskId"]:
                issues.append("child.ExternalParentTaskId needs uniquely identified parent-task evidence")
        _check_exclusive_pairs(payload, EXCLUSIVE_TASK_PAIRS, "child", issues)
        _check_at_most_one_groups(payload, AT_MOST_ONE_TASK_GROUPS, "child", issues)
    return list(dict.fromkeys(issues))


def _required_reference_paths(payload: dict[str, Any]) -> dict[str, Any]:
    required: dict[str, Any] = {}
    root_groups = ROOT_REQUIRED_ALTERNATIVES + (
        ("ProjectPlanType", "ProjectPlanTypeId"),
        ("InitialProjectStatus", "InitialProjectStatusCode"),
        ("ProjectCurrencyCode",),
        ("WorkType", "WorkTypeId"),
    )
    for group in root_groups:
        for field in group:
            if _nonblank(payload.get(field)):
                required[field] = payload[field]
                break
    for index, task in enumerate(payload.get("Tasks", [])):
        if not isinstance(task, dict):
            continue
        for field in ("TaskOrganizationName", "TaskOrganizationId"):
            if _nonblank(task.get(field)):
                required[f"Tasks[{index}].{field}"] = task[field]
                break
    return required


def validate_reference_ledger(payload: Any, ledger: Any) -> list[str]:
    """Keep legacy callers compatible; Fusion validates reference eligibility on POST."""
    del payload, ledger
    return []


def validate_evidence_artifacts(ledger: Any, ledger_directory: Path) -> list[str]:
    """Verify that every cited evidence artifact is local and checksum-bound."""
    issues: list[str] = []
    checked: set[tuple[str, str]] = set()
    records = []
    if isinstance(ledger, dict):
        records.extend(ledger.get("entries", []))
        records.extend(ledger.get("compatibilityChecks", []))
    for record in records:
        if not isinstance(record, dict):
            continue
        artifact = record.get("evidenceArtifact")
        digest = record.get("evidenceSha256")
        if not isinstance(artifact, str) or not isinstance(digest, str):
            continue
        key = (artifact, digest.lower())
        if key in checked:
            continue
        checked.add(key)
        relative = Path(artifact)
        if relative.is_absolute() or ".." in relative.parts:
            issues.append(f"reference evidence artifact must be task-local: {artifact}")
            continue
        path = ledger_directory / relative
        if not path.is_file():
            issues.append(f"reference evidence artifact does not exist: {artifact}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest.lower():
            issues.append(f"reference evidence artifact checksum mismatch: {artifact}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--payload", required=True, type=Path)
    parser.add_argument("--describe-json", required=True, type=Path)
    parser.add_argument("--operation", default="create",
                        choices=("create", "update", "end_date", "create_child", "update_child", "delete_child"))
    parser.add_argument("--child-family", choices=tuple(CHILD_METHODS))
    parser.add_argument(
        "--reference-ledger",
        type=Path,
        help="Optional discovery record; it is not a pre-submit eligibility gate.",
    )
    parser.add_argument(
        "--validation-output",
        type=Path,
        help="Write the authoritative validation record computed from the current input bytes.",
    )
    parser.add_argument(
        "--expected-payload-sha256",
        help="Optional task-local approved-artifact integrity check; not execution authorization.",
    )
    parser.add_argument("--priority-lookup-json", type=Path,
                        help="Complete priority lookup GET evidence obtained by the selected workflow; no network calls.")
    parser.add_argument("--lookup-evidence-json", type=Path,
                        help="Documented code-field lookup evidence keyed by prepared JSON path; no network calls.")
    parser.add_argument("--effective-date", help="Target business date YYYY-MM-DD for priority eligibility.")
    parser.add_argument("--prepared-payload-output", type=Path,
                        help="Create a new defaulted/resolved payload only when validation passes; existing destinations are refused.")
    args = parser.parse_args()

    inputs = [args.payload, args.describe_json, args.priority_lookup_json, args.lookup_evidence_json, args.reference_ledger]
    outputs = [args.validation_output, args.prepared_payload_output]
    input_paths = {path.resolve() for path in inputs if path is not None}
    output_paths = [path.resolve() for path in outputs if path is not None]
    existing = [path for path in input_paths | set(output_paths) if path.exists()]
    inode_collision = any(output.exists() and output != other and output.samefile(other)
                          for output in output_paths for other in existing)
    if input_paths.intersection(output_paths) or len(output_paths) != len(set(output_paths)) or inode_collision:
        print(json.dumps({"status": "failed", "issues": ["output paths must not overwrite inputs or each other"]}))
        return 2
    if args.prepared_payload_output and (args.prepared_payload_output.exists() or args.prepared_payload_output.is_symlink()):
        print(json.dumps({"status": "failed", "failure_class": "approval_blocker",
                          "issues": ["prepared payload output already exists; select a new versioned destination"]}))
        return 2

    try:
        payload_bytes = args.payload.read_bytes()
        payload = json.loads(payload_bytes)
        describe_bytes = args.describe_json.read_bytes()
        describe = json.loads(describe_bytes)
        priority_bytes = args.priority_lookup_json.read_bytes() if args.priority_lookup_json else None
        priority = json.loads(priority_bytes) if priority_bytes is not None else None
        lookup_bytes = args.lookup_evidence_json.read_bytes() if args.lookup_evidence_json else None
        lookup_evidence = json.loads(lookup_bytes) if lookup_bytes is not None else None
        ledger_bytes = args.reference_ledger.read_bytes() if args.reference_ledger else None
    except (OSError, ValueError):
        print(json.dumps({"status": "failed", "failure_class": "input_validation", "issues": ["cannot read or parse input artifacts"]}))
        return 2
    metadata_issues = _metadata_shape_issues(describe)
    if metadata_issues:
        print(json.dumps({"status": "failed", "failure_class": "catalog_mismatch", "issues": metadata_issues}))
        return 2
    prepared = prepare_payload(payload, describe, args.operation, args.child_family,
                               priority_lookup=priority, effective_date=args.effective_date, lookup_evidence=lookup_evidence)
    normalized = prepared["payload"]
    issues = list(dict.fromkeys(prepared["issues"] + validate_payload(normalized, describe, args.operation, args.child_family,
                              priority_lookup=priority, effective_date=args.effective_date, lookup_evidence=lookup_evidence)))
    payload_digest = hashlib.sha256(payload_bytes).hexdigest()
    if args.expected_payload_sha256 is not None:
        expected = args.expected_payload_sha256
        if not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
            issues.append("expected payload SHA-256 must contain exactly 64 hexadecimal characters")
        elif payload_digest != expected.lower():
            issues.append("payload differs from the approval-bound artifact; a new preview and approval are required")
        elif normalized != payload:
            issues.append("approval-bound payload needs defaults or lookup resolution; prepare a new artifact and obtain new approval")
    result = {
        "status": "passed" if not issues else "failed",
        "operation": args.operation,
        "child_family": args.child_family,
        "payload_sha256": payload_digest,
        "metadata_sha256": hashlib.sha256(describe_bytes).hexdigest(),
        "reference_ledger_sha256": (
            hashlib.sha256(ledger_bytes).hexdigest() if ledger_bytes is not None else None
        ),
        "issues": issues,
        "defaults": prepared["defaults"],
        "resolutions": prepared["resolutions"],
        "priority_evidence_sha256": hashlib.sha256(priority_bytes).hexdigest() if priority_bytes is not None else None,
        "lookup_evidence_sha256": hashlib.sha256(lookup_bytes).hexdigest() if lookup_bytes is not None else None,
        "metadata_scope": "operation_specific" if "operationMetadata" in describe else "generic_describe",
    }
    if not issues:
        normalized_bytes = (json.dumps(normalized, indent=2) + "\n").encode("utf-8")
        result["prepared_payload_sha256"] = hashlib.sha256(normalized_bytes).hexdigest()
        result["prepared_payload"] = normalized
        if args.prepared_payload_output:
            if args.prepared_payload_output.resolve() in {args.payload.resolve(), args.describe_json.resolve(),
                                                         args.validation_output.resolve() if args.validation_output else None}:
                raise ValueError("prepared payload output must not overwrite an input or validation artifact")
            try:
                # Exclusive creation also refuses a destination created after preflight.
                with args.prepared_payload_output.open("xb") as destination:
                    destination.write(normalized_bytes)
            except FileExistsError:
                print(json.dumps({"status": "failed", "failure_class": "approval_blocker",
                                  "issues": ["prepared payload output appeared during preparation; select a new destination"]}))
                return 2
            except OSError:
                print(json.dumps({"status": "failed", "failure_class": "artifact_persistence",
                                  "issues": ["cannot persist prepared payload; preserve any partial artifact and use a new destination"]}))
                return 2
    rendered = json.dumps(result, indent=2) + "\n"
    if args.validation_output:
        args.validation_output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if not issues else 2


if __name__ == "__main__":
    sys.exit(main())
