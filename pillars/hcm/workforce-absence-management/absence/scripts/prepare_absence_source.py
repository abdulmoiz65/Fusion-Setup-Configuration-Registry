#!/usr/bin/env python3
"""Offline absence-specific relationship assembly; never calls Fusion.

Consumes resolved business decisions, not natural-language prompts or REST
responses. Core continues to own DAT formatting, approvals and execution.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import secrets
import sys
import zipfile

SUPPORTED = {
    "absenceTypes", "absencePlans", "absenceReasons", "absenceCategories",
    "absenceLeaveAgreementTemplates", "absenceCertifications",
}
HIERARCHY = {
    "absenceTypeRegions": "AbsenceTypeRegionId",
    "absenceTypeRegionUsages": "AbsenceTypeRegionUsageId",
    "absenceUsageRules": "AbsenceUsageRuleId",
}
TYPE_PARENTS = {
    "absenceTypeRegions": "absenceTypes", "plans": "absenceTypes",
    "reasons": "absenceTypes", "absenceTypeRegionUsages": "absenceTypeRegions",
    "absenceUsageRules": "absenceTypeRegionUsages",
}
PERSONAS = ("Administrator", "Manager", "Employee")
TYPE_CREATE_OPTIONAL_RULE_FIELDS = frozenset({"EnableRuleEdit", "RuleReferenceDateLookupType"})
NATIVE_USER_KEYS = "native-user-keys"


def validate_native_user_key_candidate(schema, model):
    """Validate the metadata-backed, server-allocated create hierarchy.

    Multiple roots or repeated business keys cannot be disambiguated by the
    current nested user-key contract. Explicit rule creation has no LOCAL
    user-key alternative and requires a separately supported operation.
    """
    if model.get("hierarchyKeyStrategy") != NATIVE_USER_KEYS:
        return
    sections, operations = model["sections"], model["operations"]
    if schema.discriminator != "absenceTypes" or len(sections.get("absenceTypes", [])) != 1:
        raise ValueError("Native user-key validation requires exactly one new absence type")
    if any(op != "create" for values in operations.values() for op in values):
        raise ValueError("Native user-key validation is create-only; maintenance requires returned IDs")
    if sections.get("absenceUsageRules"):
        raise ValueError("Explicit rule creation is not covered by native user-key validation")
    expected = {
        "absenceTypeRegions": ("AbsenceTypeRegionId", "AbsenceRegionCode"),
        "absenceTypeRegionUsages": ("AbsenceTypeRegionUsageId", "AbsenceUsageCode"),
    }
    for section, (field, key) in expected.items():
        rows = sections.get(section, [])
        if not rows:
            continue
        attr = attributes(schema, section).get(field, {})
        if attr.get("AttributeMapKeyReferenceType") != "LOCAL" or user_keys(attr) != (key,):
            raise ValueError("Current metadata does not declare the native LOCAL user key: " + section)
        seen = set()
        for row in rows:
            if field in row:
                raise ValueError("Native user-key create must omit child LOCAL IDs")
            value = row.get(key, "")
            if not value.strip() or value in seen:
                raise ValueError("Native user keys must be populated and unique within the create: " + key)
            seen.add(value)
    for row in sections.get("absenceTypeRegionUsages", []):
        attr = attributes(schema, "absenceTypeRegionUsages").get("AbsenceTypeRegionId", {})
        if attr.get("AttributeMapKeyReferenceType") != "PARENT" or user_keys(attr) != ("AbsenceRegionCode",):
            raise ValueError("Current metadata does not declare the native region PARENT user key")
        if "AbsenceTypeRegionId" in row:
            raise ValueError("Native user-key create must omit child PARENT IDs")
    if model.get("generatedKeys") != []:
        raise ValueError("Native user-key create must not claim generated client IDs")
    if "complete post-load hierarchy reconciliation" not in model.get("requires", []):
        raise ValueError("Native user-key validation cannot omit its reconciliation gate")


def iso_date(value):
    if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value:
        raise ValueError("An explicit ISO YYYY-MM-DD operation date is required")
    return value


def type_controls(section, operation, start=None, end=None):
    if operation == "zap" and (start is not None or end is not None):
        raise ValueError("ZAP has no range date; retain lookup dates separately")
    if operation not in ("zap", "end-date") and end is not None:
        raise ValueError("End-date intent needs its own validated representation; it cannot be discarded")
    if operation == "create":
        # Pattern hierarchy inherits the root date; do not invent child controls.
        if section in HIERARCHY:
            return {"RestAction": "POST"}
        return {"RestAction": "POST", "effectiveOf": "RangeStartDate=" + iso_date(start)}
    if operation in ("update", "correction", "delete-changes"):
        return {"RestAction": "DELETE" if operation == "delete-changes" else "PATCH",
                "effectiveOf": "RangeMode=" + operation.upper().replace("-", "_")
                + ";RangeStartDate=" + iso_date(start)}
    if operation == "end-date":
        return {"RestAction": "PATCH", "effectiveOf": "RangeMode=END_DATE;RangeEndDate=" + iso_date(end)}
    if operation == "zap":
        return {"RestAction": "DELETE", "effectiveOf": "RangeMode=ZAP"}
    raise ValueError("Unsupported or ambiguous absence type operation")


def scalar(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if not isinstance(value, (str, int)):
        raise ValueError("Resolved values must be strings, integers or booleans; omit unset fields")
    result = str(value)
    if any(c in result for c in ("|", "\r", "\n", "\x00")):
        raise ValueError("DAT values must not contain pipes, newlines or NUL")
    return result


def attributes(schema, section):
    values = schema.attributes.get(section, ())
    result = {v["AttributeName"]: v for v in values}
    if len(result) != len(values):
        raise ValueError("Duplicate attribute metadata for " + section)
    return result


def registered_sections(schema):
    return {s.discriminator: {"component": schema.components.get(s.discriminator, {}),
                              "headers": list(s.attribute_names),
                              "attributes": list(schema.attributes.get(s.discriminator, ())),
                              "keyAlternatives": {a["AttributeName"]: list(user_keys(a))
                                  for a in schema.attributes.get(s.discriminator, ())
                                  if a.get("AttributeMapKeyReferenceType") in {"LOCAL", "PARENT"}}} for s in schema.sections}


def contract_fingerprint(schema):
    payload = {"businessObject": schema.discriminator,
               "sections": {s.discriminator: list(s.attribute_names) for s in schema.sections},
               "attributes": schema.attributes, "components": schema.components}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def leave_context_fingerprint(contexts):
    return hashlib.sha256(json.dumps(contexts, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def validate_leave_current_contexts(model):
    """Bind current Edit and existing-parent child POST controls to read-only context.

    This integrity check cannot prove that the supplied context came from Fusion;
    the task's fresh identity/read-context gate remains a live prerequisite.
    """
    contexts = model.get("leaveCurrentContexts", [])
    if not isinstance(contexts, list):
        raise ValueError("Leave Agreement current read context must be an array")
    if contexts or "leaveCurrentContextSha256" in model:
        if model.get("leaveCurrentContextSha256") != leave_context_fingerprint(contexts):
            raise ValueError("Leave Agreement current read context fingerprint differs; reread and prepare again")
    by_id = {}
    for context in contexts:
        if (not isinstance(context, dict) or set(context) != {"AbsenceAgreementId", "storedStartDate"}
                or not isinstance(context["AbsenceAgreementId"], str)
                or not re.fullmatch(r"[1-9][0-9]*", context["AbsenceAgreementId"])):
            raise ValueError("Leave Agreement current read context requires the exact returned agreement identity and stored Start Date")
        identity = context["AbsenceAgreementId"]
        if identity in by_id:
            raise ValueError("Duplicate Leave Agreement current read context identity")
        by_id[identity] = iso_date(context["storedStartDate"])
    for section, rows in model["sections"].items():
        for row, operation in zip(rows, model["operations"][section]):
            if operation != "edit" and (operation != "create" or section == "absenceLeaveAgreementTemplates"
                                        or not row.get("AbsenceAgreementId")):
                continue
            identity = row.get("AbsenceAgreementId")
            stored_start = by_id.get(identity)
            if stored_start is None:
                raise ValueError("Leave Agreement Edit or existing-parent child creation requires retained current read context")
            expected = ("RangeMode=CORRECTION;RangeStartDate=" if operation == "edit" else "RangeStartDate=")
            if row.get("effectiveOf") != expected + stored_start:
                raise ValueError("Leave Agreement current control differs from its bound parent's stored Start Date")


def user_keys(attr):
    # Reuse core's metadata normalization, loaded only after configuration preflight.
    from absence_source_io import core_modules
    metadata, _ = core_modules()
    return metadata.user_key_attribute_names(attr)


def require_equal(row, key, value):
    if key in row and row[key] != value:
        raise ValueError("Conflicting parent reference: " + key)
    row[key] = value


def parent_link(schema, section, row, parent_section, parent):
    component = schema.components.get(section, {})
    expected = component.get("ParentBusObjFileDiscriminator")
    if expected != parent_section:
        raise ValueError("Current metadata does not confirm parent section for " + section)
    refs = [a for a in attributes(schema, section).values()
            if a.get("AttributeMapKeyReferenceType") == "PARENT"]
    if not refs:
        raise ValueError("No current PARENT key metadata for " + section)
    for attr in refs:
        key = attr["AttributeName"]
        # Types deliberately use canonical business keys for direct children,
        # including plans and reasons, even if an existing root ID is known.
        use_business_keys = schema.discriminator == "absenceTypes" and parent_section == "absenceTypes"
        if use_business_keys and (key != "AbsenceTypeId" or set(user_keys(attr)) != {"Name", "LegislationCode"}):
            raise ValueError("Absence type parent-key contract changed; refresh task guidance")
        if parent.get(key) and not use_business_keys:
            require_equal(row, key, parent[key])
        else:
            if row.get(key):
                raise ValueError("Parent ID must be omitted when binding by user keys: " + key)
            row.pop(key, None)
            keys = user_keys(attr)
            if not keys or any(not parent.get(k) for k in keys):
                raise ValueError("Missing complete parent user keys for " + section)
            for field in keys:
                require_equal(row, field, parent[field])


def validate_graph(schema, sections):
    """Validate actual rows, not declared task-hook pass flags."""
    positions = {section: position for position, section in enumerate(sections)}
    for section, rows in sections.items():
        details = attributes(schema, section)
        for row in rows:
            for key, value in row.items():
                scalar(value)
                length = details.get(key, {}).get("DataLength")
                if length and len(value) > int(length):
                    raise ValueError("Value exceeds current metadata length: " + section + "." + key)
            if section == schema.discriminator:
                continue
            parent_section = schema.components.get(section, {}).get("ParentBusObjFileDiscriminator")
            if not parent_section or parent_section not in sections:
                raise ValueError("Missing registered parent section for " + section)
            if positions[parent_section] >= positions[section]:
                raise ValueError("Parent section must precede its child: " + section)
            candidates = sections.get(parent_section, [])
            # Metadata-only roots intentionally carry no row. Exact external
            # identity remains a workflow precondition, not an offline claim.
            parent_refs = [a for a in details.values() if a.get("AttributeMapKeyReferenceType") == "PARENT"]
            if not parent_refs:
                raise ValueError("Missing registered PARENT metadata in " + section)
            for attr in parent_refs:
                key = attr["AttributeName"]
                keys = (key,) if row.get(key) else user_keys(attr)
                if not keys or any(not row.get(k) for k in keys):
                    raise ValueError("Unresolved parent reference in " + section)
                if candidates:
                    matches = [p for p in candidates if all(p.get(k) == row[k] for k in keys)]
                    if len(matches) != 1:
                        raise ValueError("Parent reference must resolve exactly once in " + section)
                elif parent_section != schema.discriminator:
                    raise ValueError("Missing parent carrier in " + section)


def validate_type_rows(sections, operations, native_user_keys=False):
    roots = sections.get("absenceTypes", [])
    for section, rows in sections.items():
        for row, operation in zip(rows, operations[section]):
            if "EffectiveStartDate" in row:
                raise ValueError("Absence type source uses operation controls, not physical start dates")
            control_parts = {}
            for part in row.get("effectiveOf", "").split(";") if row.get("effectiveOf") else []:
                key, separator, value = part.partition("=")
                if not separator or key in control_parts:
                    raise ValueError("Malformed type date-effective control")
                control_parts[key] = value
            expected = type_controls(section, operation, control_parts.get("RangeStartDate"),
                                     control_parts.get("RangeEndDate"))
            if row.get("RestAction") != expected["RestAction"] or row.get("effectiveOf") != expected.get("effectiveOf"):
                raise ValueError("Absence type controls differ from the selected operation")
            if section in HIERARCHY and any(k.startswith("SourceRef") for k in row):
                raise ValueError("SourceRef is not absence type hierarchy identity")
            if section == "absenceTypes" and operation == "create":
                if "AbsenceTypeId" in row:
                    raise ValueError("Fusion must generate the absence type root ID")
                for field in ("Name", "LegislationCode", "LegDataGroupId", "AbsencePatternCode"):
                    if not row.get(field, "").strip():
                        raise ValueError("Missing resolved type field: " + field)
                if row["AbsencePatternCode"] not in ("GENERIC", "II", "MAP"):
                    raise ValueError("Unsupported absence pattern")
                # UCM marks these optional, but Fusion's create business
                # validation requires resolved values. Never silently insert
                # lookup codes here or mutate an approved source during verify.
                missing = [label for field, label in (
                    ("PartialDayCode", "Partial Day Rule"),
                    ("MaximumDuration", "Maximum Duration"),
                ) if not row.get(field, "").strip()]
                if missing:
                    raise ValueError(
                        "Missing resolved create values: " + ", ".join(missing) +
                        ". Apply absence-type create defaults and validate applicable "
                        "live lookups before preparing the source; preserve user values.")
            if section == "absenceTypes" and operation != "create":
                value = row.get("AbsenceTypeId", "")
                if (not value.isascii() or not value.isdecimal() or str(int(value)) != value or
                        not 0 < int(value) <= 9007199254740991):
                    raise ValueError("Non-create requires an exact returned AbsenceTypeId")
                # Maintenance targets the returned ID. Business-key context
                # belongs on metadata-only roots/child carriers, not a root
                # mutation. Without a baseline, even an echoed value cannot
                # be proved unchanged; never silently strip a requested edit.
                immutable = [label for field, label in (
                    ("LegislationCode", "Legislation"),
                    ("AbsencePatternCode", "Absence Pattern"),
                ) if field in row]
                if immutable:
                    raise ValueError("Absence type fields are immutable: " + ", ".join(immutable) +
                                     ". Omit them from root maintenance rows; retain the exact returned ID.")
            if section == "absenceTypeRegions" and operation == "create":
                for persona in PERSONAS:
                    if row.get(persona + "UsageCode") and not row.get(persona + "LookupType", "").strip():
                        raise ValueError("Region create needs its template-resolved persona lookup type: "
                                         + persona + "LookupType")
                if row.get("AbsenceRegionCode") == "SUPPLEMENTAL_DETAILS" and any(
                        row.get(persona + "UsageCode") != "ENABLE" for persona in PERSONAS):
                    raise ValueError("Create SUPPLEMENTAL_DETAILS must be enabled for all three personas")
            if section == "absenceTypeRegionUsages" and operation == "create" and "EnableFlag" in row:
                raise ValueError(
                    "Omit optional EnableFlag from absence-type usage create rows; pattern "
                    "EnableFlagCode is not a loader EnableFlag value. Preserve the three persona UsageCode settings.")
            if section == "plans":
                if "AbsenceTypePlanId" in row:
                    raise ValueError("Do not supply an AbsenceTypePlanId")
                for field in ("AbsencePlanId", "Priority", "PlanStatusCode"):
                    if not row.get(field):
                        raise ValueError("Missing resolved plan association field: " + field)
                if row["PlanStatusCode"] in ("C", "P"):
                    raise ValueError("Invalid type-plan association status")
            if section == "reasons" and operation == "create":
                if not row.get("AbsenceReasonId") or row.get("DefaultFlag") not in ("true", "false"):
                    raise ValueError("Reason association needs verified reason and explicit boolean DefaultFlag")
            if section in HIERARCHY and operation != "create":
                if roots:
                    raise ValueError("Existing Display Features require a metadata-only type root")
                if section == "absenceTypeRegions":
                    allowed = {"AbsenceTypeRegionId", "LegislationCode", "Name", "RestAction", "effectiveOf"}
                    if set(row) - allowed or operation != "correction":
                        raise ValueError("Existing region must be an identity-only CORRECTION carrier")
                if section == "absenceTypeRegionUsages" and operation in ("update", "correction"):
                    if any(not row.get(p + "UsageCode") for p in PERSONAS):
                        raise ValueError("Preserve all three persona usage values")
    if any(op in ("end-date", "delete-changes", "zap") for op in operations.get("absenceTypes", [])):
        if any(rows for section, rows in sections.items() if section != "absenceTypes"):
            raise ValueError("Parent lifecycle operations must not synthesize child lifecycle rows")
    generated = []
    for section, field in HIERARCHY.items():
        for row, operation in zip(sections.get(section, []), operations.get(section, [])):
            if native_user_keys and operation == "create" and section != "absenceUsageRules":
                continue
            value = row.get(field, "")
            if (not value.isascii() or not value.isdecimal() or
                    not 0 < int(value) <= 9007199254740991 or str(int(value)) != value):
                raise ValueError("Hierarchy IDs must be exact positive JavaScript-safe decimals")
            if operation == "create":
                generated.append(value)
    if len(set(generated)) != len(generated):
        raise ValueError("Duplicate create hierarchy LOCAL key")


def validate_model(schema, model):
    sections, operations = model["sections"], model["operations"]
    if model["businessObject"] != schema.discriminator:
        raise ValueError("Model and registered business object differ")
    if model.get("contractSha256") != contract_fingerprint(schema):
        raise ValueError("Registered contract differs from the prepared model; regenerate and revalidate")
    if model.get("hierarchyKeyStrategy") not in (None, NATIVE_USER_KEYS):
        raise ValueError("Unsupported hierarchy key strategy")
    if set(sections) != set(operations):
        raise ValueError("Missing section operation evidence")
    if not any(sections.values()):
        raise ValueError("The source must contain at least one mutation row")
    for section, rows in sections.items():
        header = set(schema.sections_by_discriminator[section].attribute_names)
        if len(rows) != len(operations[section]):
            raise ValueError("Missing row operation evidence")
        targets = set()
        local_ids = [a["AttributeName"] for a in attributes(schema, section).values()
                     if a.get("AttributeMapKeyReferenceType") == "LOCAL"]
        for row in rows:
            if set(row) - header:
                raise ValueError("Unsupported current template fields in " + section)
            if any(k in row for k in ("CreatedBy", "CreationDate", "LastUpdatedBy", "LastUpdateDate")):
                raise ValueError("Audit fields are not resolved mutation input")
            if local_ids and all(row.get(k) for k in local_ids):
                target = tuple(row[k] for k in local_ids) + (row.get("effectiveOf"),)
                if target in targets:
                    raise ValueError("Duplicate target identity/slice in " + section)
                targets.add(target)
    validate_graph(schema, sections)
    if schema.discriminator == "absenceTypes":
        validate_native_user_key_candidate(schema, model)
        validate_type_rows(sections, operations, model.get("hierarchyKeyStrategy") == NATIVE_USER_KEYS)
        validate_type_create_rule_metadata(schema, model)
    else:
        if model.get("hierarchyKeyStrategy"):
            raise ValueError("Hierarchy key strategy applies only to absence types")
        from absence_task_contracts import validate_task_rows
        validate_task_rows(schema.discriminator, sections, operations,
                           registered_sections=registered_sections(schema),
                           certification_contexts=model.get("certificationUiContexts"))
        if schema.discriminator == "absenceCertifications":
            contexts = model.get("certificationUiContexts", {})
            if model.get("certificationUiContextSha256") != leave_context_fingerprint(contexts):
                raise ValueError("Certification UI context fingerprint differs; reread and prepare again")
            if not isinstance(contexts, dict) or set(contexts) - set(sections):
                raise ValueError("Certification UI context has unknown sections")
        if schema.discriminator == "absenceLeaveAgreementTemplates":
            validate_leave_current_contexts(model)


def validate_type_create_rule_metadata(schema, model):
    """Return eligible new-US-type usages without modifying their rule cells.

    A populated rule field requires its companion whether row shapes differ
    or are already uniform. Share this invariant with exact-source validation;
    it must not depend on whether optional blank cells need to be filled.
    """
    if schema.discriminator != "absenceTypes":
        return []
    sections, operations = model["sections"], model["operations"]
    roots = sections.get("absenceTypes", [])
    usages = sections.get("absenceTypeRegionUsages", [])
    if not roots or not usages or any(
        op != "create" for section in ("absenceTypes", "absenceTypeRegions", "absenceTypeRegionUsages")
        for op in operations.get(section, [])
    ):
        return []
    if any(root.get("LegislationCode") != "US" or
           root.get("AbsencePatternCode") not in ("GENERIC", "II", "MAP") for root in roots):
        return []
    # Historical create evidence covers absent pairs on non-rule usages, not
    # filling a missing half of populated rule metadata or disabling a rule.
    if any(any(row.get(field) for field in TYPE_CREATE_OPTIONAL_RULE_FIELDS) and
           not all(row.get(field) for field in TYPE_CREATE_OPTIONAL_RULE_FIELDS) for row in usages):
        raise ValueError("Incomplete populated rule metadata; resolve both rule fields from the pattern")
    return usages


def resolve_type_create_rule_cells(schema, model):
    """Resolve the two inapplicable rule cells for a new US pattern hierarchy.

    Captured GENERIC/II/MAP create DATs and exact usage readbacks establish
    blank -> null for these optional fields only. This is an absence-specific
    create resolution, NOT a general equivalence of omission and blank. Keep
    the adapter's strict field-set check for all other fields and operations.
    """
    usages = validate_type_create_rule_metadata(schema, model)
    if not usages:
        return []
    # Only add a cell when that column is needed elsewhere in the same DAT
    # section. If every usage omits a field, keep the column omitted as before.
    selected = set().union(*(set(row) for row in usages))
    differing = selected - set.intersection(*(set(row) for row in usages))
    if not differing or differing - TYPE_CREATE_OPTIONAL_RULE_FIELDS:
        return []
    from absence_source_io import core_modules
    metadata, _ = core_modules()
    details = attributes(schema, "absenceTypeRegionUsages")
    for field in differing:
        attr = details.get(field, {})
        if (attr.get("MandatoryStatusCode") != "ORA_N" or
                attr.get("MandatoryStatus") not in (None, "", "No") or
                attr.get("DataType") != "String" or
                attr.get("AttributeMapKeyReferenceType") or metadata.is_key_attribute(attr)):
            raise ValueError("Current optional non-key String metadata is required to resolve " + field)
    resolutions = []
    for index, row in enumerate(usages):
        missing = sorted(differing - set(row))
        if missing:
            row.update({field: "" for field in missing})
            resolutions.append({"section": "absenceTypeRegionUsages", "rowIndex": index,
                                "fields": missing, "value": "",
                                "reason": "new-US-type-inapplicable-optional-rule-metadata"})
    return resolutions


def build_model(schema, intent):
    bo = intent.get("businessObject")
    if bo not in SUPPORTED or bo != schema.discriminator:
        raise ValueError("Unsupported or mismatched absence business object")
    if not isinstance(intent.get("records"), list) or not intent["records"]:
        raise ValueError("At least one explicitly resolved record is required")
    strategy = intent.get("hierarchyKeyStrategy")
    if strategy == "native-user-keys-validation":
        strategy = NATIVE_USER_KEYS
    if strategy not in (None, NATIVE_USER_KEYS) or (strategy and bo != "absenceTypes"):
        raise ValueError("Unsupported hierarchy key strategy")
    sections, operations, generated = {bo: []}, {bo: []}, set()
    leave_contexts = []
    certification_contexts = {}

    def visit(section, node, parent_section=None, parent=None, inherited=None):
        if not isinstance(node, dict) or set(node) - {
            "operation", "effectiveStartDate", "effectiveEndDate", "storedStartDate", "values", "children", "contextOnly", "uiContext"
        }:
            raise ValueError("Unknown or malformed resolved record input")
        if section not in schema.sections_by_discriminator:
            raise ValueError("Unknown current template section: " + section)
        op = node.get("operation", "create" if inherited and inherited[0] == "create" else None)
        # "Update" is user wording for the one current-version Redwood Edit.
        # Normalize before reading date input; a supplied date remains invalid.
        if bo == "absenceLeaveAgreementTemplates" and op == "update":
            op = "edit"
        start = node.get("effectiveStartDate", inherited[1] if inherited and op == "create" else None)
        end = node.get("effectiveEndDate")
        stored_start = None
        if "storedStartDate" in node:
            if (bo != "absenceLeaveAgreementTemplates" or section != bo
                    or (op != "edit" and not (op is None and node.get("contextOnly") is True))):
                raise ValueError("Stored Start Date is read-only context for an existing Leave Agreement")
            stored_start = iso_date(node["storedStartDate"])
        if bo == "absenceLeaveAgreementTemplates" and op == "delete" and node.get("children"):
            raise ValueError("Delete the current Leave Agreement as one parent action; do not synthesize child mutations or a cascade")
        if bo == "absenceCertifications" and op in {"end-date", "zap", "delete-changes"} and node.get("children"):
            raise ValueError("Certification End Date/Delete is one parent action; do not synthesize child mutations")
        if bo == "absenceLeaveAgreementTemplates" and parent is not None and op == "create" and inherited[0] != "create":
            if inherited[0] not in {"edit", None} or inherited[1] is None:
                raise ValueError("Adding a Leave Agreement child requires the exact current parent's stored Start Date")
            if start != inherited[1]:
                raise ValueError("A new Leave Agreement child must use the current parent's stored Start Date; "
                                 "a new date-effective intent is unavailable")
        if (bo == "absenceTypes" and section in HIERARCHY and op == "create" and inherited
                and start != inherited[1]):
            raise ValueError("New type hierarchy inherits the parent create date; a different child date is unsupported")
        row = {k: scalar(v) for k, v in node.get("values", {}).items()}
        if "uiContext" in node and bo != "absenceCertifications":
            raise ValueError("uiContext applies only to certification Redwood field validation")
        if stored_start is not None:
            identity = row.get("AbsenceAgreementId")
            if not identity or not re.fullmatch(r"[1-9][0-9]*", identity):
                raise ValueError("Stored Start Date context requires the exact returned Leave Agreement identity")
            leave_contexts.append({"AbsenceAgreementId": identity, "storedStartDate": stored_start})
        # Documented create defaults, applied before rendering/approval only.
        # Omission is not an explicit blank or a request to clear a value.
        # Lookup evidence remains required by the task before submission.
        if bo == "absenceTypes" and section == bo and op == "create":
            pattern = row.get("AbsencePatternCode")
            if pattern in ("GENERIC", "II", "MAP"):
                row.setdefault("PartialDayCode", "N" if pattern == "MAP" else "A")
                row.setdefault("MaximumDuration", "4160")
        if "RestAction" in row or "effectiveOf" in row:
            raise ValueError("Supply semantic operation/date, never caller-authored controls")
        details = attributes(schema, section)
        context_only = node.get("contextOnly", False)
        if not isinstance(context_only, bool):
            raise ValueError("contextOnly must be a boolean")
        if context_only:
            if section != bo or bo not in ("absenceTypes", "absencePlans", "absenceCategories", "absenceLeaveAgreementTemplates") or op is not None:
                raise ValueError("Only a type/plan/category/leave agreement root may be a metadata-only context without operation")
            identity = {a["AttributeName"] for a in details.values()
                        if a.get("AttributeMapKeyReferenceType") == "LOCAL"}
            for a in details.values():
                if a.get("AttributeMapKeyReferenceType") == "LOCAL":
                    identity.update(user_keys(a))
            if set(row) - identity:
                raise ValueError("Metadata-only root must contain identity context only")
        else:
            if op is None:
                raise ValueError("An explicit operation is required")
            if section == bo and not any(a.get("AttributeMapKeyReferenceType") == "LOCAL" for a in details.values()):
                raise ValueError("Current registered root LOCAL identity metadata is required")
            for field, attr in details.items():
                if attr.get("AttributeMapKeyReferenceType") != "LOCAL":
                    continue
                if bo == "absenceTypes" and section == "plans" and field == "AbsenceTypePlanId":
                    if field in row:
                        raise ValueError("Type-plan associations must not supply AbsenceTypePlanId")
                    continue
                if op == "create":
                    if field in row:
                        raise ValueError("Create IDs must not be copied or supplied: " + field)
                    if bo == "absenceTypes" and HIERARCHY.get(section) == field:
                        if strategy == NATIVE_USER_KEYS:
                            continue
                        if not attr.get("DataLength") or int(attr["DataLength"]) < 15:
                            raise ValueError("Current LOCAL key contract cannot carry safe 15-digit keys")
                        value = str(100000000000000 + secrets.randbelow(900000000000000))
                        while value in generated:
                            value = str(100000000000000 + secrets.randbelow(900000000000000))
                        generated.add(value)
                        row[field] = value
                elif not row.get(field):
                    raise ValueError("Non-create requires exact returned identity: " + field)
            if parent is not None:
                parent_link(schema, section, row, parent_section, parent)
            # These tasks retain a physical create date as well as effectiveOf.
            # This maps an already resolved business date; it is not a default.
            if op == "create" and section == bo:
                physical_start = bo == "absenceReasons"
                if bo == "absenceCategories":
                    from absence_source_io import core_modules
                    metadata, _ = core_modules()
                    physical_start = metadata.is_required_for_create(details.get("EffectiveStartDate", {}))
                if physical_start:
                    require_equal(row, "EffectiveStartDate", iso_date(start))
            if bo == "absenceTypes":
                controls = type_controls(section, op, start, end)
            else:
                from absence_task_contracts import derive_controls
                control_stored_start = stored_start if section == bo else inherited[1] if inherited else None
                controls = derive_controls(bo, section, op, start, end,
                                           stored_start=control_stored_start,
                                           registered_sections=registered_sections(schema))
            row.update(controls)
            sections.setdefault(section, []).append(row)
            operations.setdefault(section, []).append(op)
            if bo == "absenceCertifications":
                certification_contexts.setdefault(section, []).append(deepcopy(node.get("uiContext", {})))
        for child, nodes in node.get("children", {}).items():
            if not isinstance(nodes, list):
                raise ValueError("Children must be arrays of resolved records")
            for child_node in nodes:
                visit(child, child_node, section, row, (op, stored_start if stored_start is not None else start))

    for node in deepcopy(intent["records"]):
        visit(bo, node)
    # Use registered section order, which core validates as the DAT contract.
    sections = {s.discriminator: sections[s.discriminator] for s in schema.sections
                if s.discriminator in sections}
    model = {"businessObject": bo, "sections": sections, "operations": operations,
             "contractSha256": contract_fingerprint(schema),
             "generatedKeys": sorted(generated), "status": "offline_prepared_not_approved",
             "requires": ["current metadata and lookup evidence", "live child-key collision check" if generated else
                          "exact target identity verification", "core Data Loader validation, preview and approval"]}
    if strategy:
        model["hierarchyKeyStrategy"] = strategy
        model["requires"].append("complete post-load hierarchy reconciliation")
    if bo == "absenceCertifications":
        model["certificationUiContexts"] = certification_contexts
        model["certificationUiContextSha256"] = leave_context_fingerprint(certification_contexts)
        model["requires"].append("fresh target Redwood visibility, retained before-state and resolved-meaning provenance before preview")
    if leave_contexts:
        model["leaveCurrentContexts"] = leave_contexts
        model["leaveCurrentContextSha256"] = leave_context_fingerprint(leave_contexts)
        model["requires"].append("verify current parent stored Start Date before Edit or child creation")
    if bo == "absenceLeaveAgreementTemplates" and any(
            op in {"edit", "delete"} for rows in operations.values() for op in rows):
        model["requires"].append("verify native current-version adapter mapping for every included Edit or Delete section")
        if not leave_contexts and any(op == "create" for section, rows in operations.items() if section != bo for op in rows):
            model["requires"].append("verify current parent stored Start Date before child creation")
    if bo in ("absenceLeaveAgreementTemplates", "absenceCertifications"):
        for section, rows in sections.items():
            for index, row in enumerate(rows):
                if row.get("EffectiveStartDate"):
                    model["requires"].append(
                        f"current {bo}/{section}/{operations[section][index]} Fusion evidence for dual date population before preview")
    validate_model(schema, model)
    resolutions = resolve_type_create_rule_cells(schema, model)
    if resolutions:
        model["fieldResolutions"] = resolutions
        validate_model(schema, model)
    return model


def check_exact_source(schema, model, content):
    from absence_source_io import read_rows, validate_rows
    validate_model(schema, model)
    validate_rows(content, schema)
    actual = read_rows(content)
    # Omitted and explicitly empty are different business decisions. Never
    # erase that distinction when checking the bytes that will be uploaded.
    if actual != model["sections"]:
        raise ValueError("Exact DAT rows differ from the prepared model")
    validate_graph(schema, actual)
    return {"status": "offline_source_verified_not_approved", "sha256": hashlib.sha256(content).hexdigest(),
            "contractSha256": model["contractSha256"],
            "requires": model["requires"],
            "fieldResolutions": model.get("fieldResolutions", []),
            "rowCounts": {k: len(v) for k, v in actual.items()}}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--intent", type=Path, help="Resolved nested business rows; prepare mode")
    parser.add_argument("--output-dir", type=Path, help="New local directory; never overwritten")
    parser.add_argument("--model", type=Path, help="Prepared model for verify mode")
    parser.add_argument("--verify", type=Path, help="Exact DAT or single-DAT ZIP to check offline")
    args = parser.parse_args(argv)
    try:
        from absence_source_io import load_contract, render_rows
        schema = load_contract(args.contract)
        if args.verify:
            if not args.model or args.intent or args.output_dir:
                raise ValueError("Verify requires --model and excludes prepare arguments")
            model = json.loads(args.model.read_text(encoding="utf-8"))
            raw = args.verify.read_bytes()
            if args.verify.suffix.lower() == ".zip":
                with zipfile.ZipFile(args.verify) as archive:
                    entries = archive.infolist()
                    if len(entries) != 1 or not entries[0].filename.lower().endswith(".dat"):
                        raise ValueError("Expected exactly one DAT member and no other ZIP entries")
                    if entries[0].file_size > 50_000_000:
                        raise ValueError("DAT exceeds the 50 MB local verification limit")
                    content = archive.read(entries[0])
            else:
                content = raw
            receipt = check_exact_source(schema, model, content)
            receipt["archiveSha256"] = hashlib.sha256(raw).hexdigest()
        else:
            if not args.intent or not args.output_dir or args.model:
                raise ValueError("Prepare requires --intent and --output-dir")
            model = build_model(schema, json.loads(args.intent.read_text(encoding="utf-8")))
            content = render_rows(schema, model["sections"])
            receipt = check_exact_source(schema, model, content)
            args.output_dir.mkdir(parents=True, exist_ok=False)
            (args.output_dir / (schema.discriminator + ".dat")).write_bytes(content)
            (args.output_dir / "prepared-model.json").write_text(json.dumps(model, indent=2) + "\n", encoding="utf-8")
            (args.output_dir / "source-validation.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(receipt))
        return 0
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        print(json.dumps({"status": "failed", "stage": "offline_absence_source",
                          "failure_class": "input_validation", "message": str(exc),
                          "recommended_action": "Correct the resolved input/contract; do not upload or retry Fusion"}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
