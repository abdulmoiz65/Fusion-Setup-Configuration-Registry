"""Offline, pillar-owned invariants for normalized absence Data Loader rows.

This module does not fetch metadata, resolve business values, or grant readiness
or approval. The caller must separately validate the current registered template
and dated identities. Certification fields also need the Redwood visibility gate;
registration alone does not make a backend field a supported user input.
Rules come from each task's ora_defaulting_rules and ora_input_validation files.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re
import sys


SECTIONS = {
    "absencePlans": frozenset({"absencePlans", "absencePlanDDFs", "absencePlanDFFs",
                               "accrualBands", "eligibilityProfiles", "entitlementBands",
                               "entitlementBandDetails", "events"}),
    "absenceCategories": frozenset({"absenceCategories", "AbsenceCategoriesDDFFlex",
                                    "AbsenceCategoriesFlex", "absenceCategoryTypes"}),
    "absenceReasons": frozenset({"absenceReasons", "AbsenceReasonsDDFFlex", "AbsenceReasonsFlex"}),
    "absenceLeaveAgreementTemplates": frozenset({"absenceLeaveAgreementTemplates",
                                                 "absenceAgreementPlans", "absenceAgreementCertifications"}),
    # The certification DFF section's spelling/keys are deployment metadata,
    # not established by the task docs. Do not guess a section here.
    "absenceCertifications": frozenset({"absenceCertifications"}),
}
ROOT_IDS = {"absencePlans": "AbsencePlanId", "absenceCategories": "AbsenceCategoryId",
            "absenceReasons": "AbsenceReasonId", "absenceLeaveAgreementTemplates": "AbsenceAgreementId",
            "absenceCertifications": "AbsenceCertificationId"}
PLAN_IDS = {"accrualBands": "AccrualBandId", "eligibilityProfiles": "PlanEligibilityProfileId",
            "entitlementBands": "EntitlementBandId", "entitlementBandDetails": "EntitlementBandDetailId",
            "events": "PlanEventId"}
OPERATIONS = {"create": "POST", "update": "PATCH", "correction": "PATCH", "end-date": "PATCH",
              "delete-changes": "DELETE", "zap": "DELETE", "carrier-create": "PATCH"}
MODES = {"update": "UPDATE", "correction": "CORRECTION", "end-date": "END_DATE",
         "delete-changes": "DELETE_CHANGES", "zap": "ZAP"}
CERTIFICATION_UPDATE_IMMUTABLE = {
    "EffectiveStartDate": "stored Effective Start Date",
    "Name": "Name",
    "ClassificationCode": "Classification",
    "LegislationCode": "Legislation",
    "TriggerCode": "Trigger",
    "EffectiveEndDate": "stored Effective End Date",
    "ManagementTypeCode": "Management",
    "AbsenceRecordUpdateRuleCode": "Absence Record Update Rule",
}
CERTIFICATION_DETAILS = frozenset({
    "Name", "Description", "StatusCode", "LegislationCode", "ManagementTypeCode",
    "ClassificationCode", "TriggerCode", "AutoCompleteFlag", "AllowOnDemandFlag",
    "ConfirmOnDemandFlag", "EligibilityProfileId", "AbsenceRecordUpdateRuleCode",
})
CERTIFICATION_DATES = {
    "DueDate": ("DueDateRuleCode", "DueDateReferenceDateCode", "DueDateUnits", "DueDateUOMCode"),
    "Expiration": ("ExpirationRuleCode", "ExpirationReferenceDateRuleCode", "ExpirationDuration", "ExpirationUOMCode"),
}
CERTIFICATION_REASONS = {"ConfirmReasonRuleCode": "ConfirmReasonValues", "VoidReasonRuleCode": "VoidReasonValues"}
CERTIFICATION_EVENTS = {
    event: tuple(event + suffix for suffix in ("UpdateCode", "CalculationCode", "CalculationModeCode", "CalculationOverride"))
    for event in ("Create", "DueDate", "Complete", "Expiration")
}
CERTIFICATION_CONTROLS = frozenset({"AbsenceCertificationId", "RestAction", "effectiveOf", "EffectiveStartDate", "EffectiveEndDate"})
CERTIFICATION_FIELDS = (CERTIFICATION_DETAILS | CERTIFICATION_CONTROLS
    | frozenset(field for fields in CERTIFICATION_DATES.values() for field in fields)
    | frozenset(CERTIFICATION_REASONS) | frozenset(CERTIFICATION_REASONS.values())
    | frozenset(field for fields in CERTIFICATION_EVENTS.values() for field in fields))
CERTIFICATION_MAINTENANCE_FIELDS = frozenset({"Description", "StatusCode", "EligibilityProfileId",
    "CompleteUpdateCode", *CERTIFICATION_REASONS, *CERTIFICATION_REASONS.values()})
LEAVE_CURRENT_ACTIONS = {"create": "POST", "edit": "PATCH", "delete": "DELETE"}
LEAVE_EDIT_IMMUTABLE = {
    "EffectiveStartDate": "stored Start Date",
    "EffectiveEndDate": "stored End Date",
    "LegislationCode": "Legislation",
    "ManagementTypeCode": "Management Type",
    "AgreementPatternCode": "Agreement Type",
    "SourceAbsenceTypeId": "Source Absence Type",
}


def _iso(value: str | None, label: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{label} requires YYYY-MM-DD")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} is not a valid calendar date") from exc
    return value


def _registered_flex(business_object: str, section: str, registered_sections: dict | None) -> bool:
    """Recognize an extra flex section by native metadata, never its spelling.

    The caller builds this descriptor from the separately validated current
    template and component inventory. Registration is not evidence of live
    context/segment validity or of an existing effective-dated child item.
    """
    if business_object not in {"absenceLeaveAgreementTemplates", "absenceCertifications"}:
        return False
    entry = (registered_sections or {}).get(section)
    if not isinstance(entry, dict):
        return False
    component, headers = entry.get("component"), entry.get("headers")
    return (isinstance(component, dict) and isinstance(headers, (list, tuple))
            and all(isinstance(header, str) for header in headers)
            and component.get("BusObjFileDiscriminator") == section
            and component.get("ParentBusObjFileDiscriminator") == business_object
            and ({"RestAction"} if business_object == "absenceLeaveAgreementTemplates"
                 else {"RestAction", "effectiveOf"}).issubset(headers)
            and any(header.startswith("FLEX:") or header == "__FLEX_Context"
                    or header.startswith("__FLEX_Context(") for header in headers))


def _scope(business_object: str, section: str, operation: str,
           registered_sections: dict | None = None) -> None:
    if business_object not in SECTIONS or (section not in SECTIONS[business_object]
            and not _registered_flex(business_object, section, registered_sections)):
        raise ValueError(f"Unsupported task/section mapping: {business_object}/{section}")
    if business_object == "absenceLeaveAgreementTemplates":
        if operation not in LEAVE_CURRENT_ACTIONS:
            raise ValueError("Leave Agreements supports Create, Edit, or Delete of the current version; "
                             "dated Update, Correction, End Date, Delete Changes, and ZAP are unavailable")
        if operation == "edit" and section not in SECTIONS[business_object]:
            headers = (registered_sections or {}).get(section, {}).get("headers", ())
            if "effectiveOf" not in headers:
                raise ValueError("Leave Agreement Edit requires the registered effectiveOf control column")
        return
    if operation not in OPERATIONS:
        raise ValueError(f"Unsupported or ambiguous operation: {operation}; select an explicit date-effective operation")
    if business_object == "absenceCertifications" and operation == "delete-changes" and section != business_object:
        raise ValueError("Certification Delete Record is one parent action; do not synthesize child deletions")
    if business_object == "absencePlans" and section == "absencePlanDFFs" and operation == "delete-changes":
        raise ValueError("absencePlanDFFs DELETE_CHANGES is unsupported; do not substitute a parent operation")
    if operation == "carrier-create" and (business_object != "absenceReasons" or section != business_object):
        raise ValueError("carrier-create is supported only for an absenceReasons key-only parent")


def derive_controls(business_object: str, section: str, operation: str,
                    effective_start: str | None = None, effective_end: str | None = None,
                    *, stored_start: str | None = None,
                    registered_sections: dict[str, dict] | None = None) -> dict[str, str]:
    """Derive task-documented controls, never dates/defaults or a guessed delete.

An explicitly supplied create end date is retained as unresolved intent by
rejecting it here: a follow-on END_DATE needs separate verified identity and
approval. Physical date columns are caller-supplied values, not these controls.
"""
    _scope(business_object, section, operation, registered_sections)
    if business_object == "absenceLeaveAgreementTemplates" and operation in {"edit", "delete"}:
        if effective_start is not None or effective_end is not None:
            raise ValueError("Leave Agreement Edit and Delete do not accept a new effective date")
        if operation == "edit":
            return {"RestAction": "PATCH", "effectiveOf": "RangeMode=CORRECTION;RangeStartDate="
                    + _iso(stored_start, "Stored Start Date")}
        return {"RestAction": "DELETE", "effectiveOf": "RangeMode=ZAP"}
    if operation == "zap":
        if effective_start is not None or effective_end is not None:
            raise ValueError("ZAP has no range date; keep lookup identity dates separate")
        effective_of = "RangeMode=ZAP"
    elif operation == "end-date":
        effective_of = "RangeMode=END_DATE;RangeEndDate=" + _iso(effective_end, "End date")
    else:
        start = _iso(effective_start, "Effective start")
        if effective_end is not None:
            raise ValueError("Explicit end-date intent needs a separately validated representation; it cannot be discarded")
        prefix = "" if operation in {"create", "carrier-create"} else "RangeMode=" + MODES[operation] + ";"
        effective_of = prefix + "RangeStartDate=" + start
    return {"RestAction": OPERATIONS[operation], "effectiveOf": effective_of}


def _present(row: dict[str, str], field: str) -> bool:
    return field in row and isinstance(row[field], str) and bool(row[field].strip())


def _require(row: dict[str, str], *fields: str) -> None:
    for field in fields:
        if not _present(row, field):
            raise ValueError(f"Required field is missing or blank: {field}")


def _identifier(row: dict[str, str], field: str) -> None:
    _require(row, field)
    if not re.fullmatch(r"[1-9][0-9]*", row[field]):
        raise ValueError(f"{field} must be an exact positive-decimal identifier, not a name or composite key")


def _omit(row: dict[str, str], *fields: str) -> None:
    for field in fields:
        if field in row:
            raise ValueError(f"Field must be omitted for this operation: {field}")


def _controls(business_object: str, section: str, operation: str, row: dict[str, str],
              registered_sections: dict | None = None) -> str | None:
    _scope(business_object, section, operation, registered_sections)
    if business_object == "absenceLeaveAgreementTemplates" and operation in {"edit", "delete"}:
        _require(row, "RestAction")
        if row["RestAction"] != LEAVE_CURRENT_ACTIONS[operation]:
            raise ValueError("Leave Agreement current-version controls require the selected Edit or Delete action")
        if operation == "delete":
            if row.get("effectiveOf") != "RangeMode=ZAP":
                raise ValueError("Leave Agreement current Delete requires the date-free RangeMode=ZAP control")
            return None
        control = row.get("effectiveOf")
        prefix = "RangeMode=CORRECTION;RangeStartDate="
        if not isinstance(control, str) or not control.startswith(prefix):
            raise ValueError("Leave Agreement Edit requires the stored Start Date control")
        stored_start = _iso(control[len(prefix):], "Stored Start Date")
        if control != derive_controls(business_object, section, operation,
                                      stored_start=stored_start,
                                      registered_sections=registered_sections)["effectiveOf"]:
            raise ValueError("Leave Agreement Edit control differs from the stored Start Date")
        return stored_start
    _require(row, "RestAction", "effectiveOf")
    parts = row["effectiveOf"].split(";")
    parsed = {}
    for part in parts:
        key, separator, value = part.partition("=")
        if not separator or key in parsed:
            raise ValueError("Invalid or duplicated effectiveOf control")
        parsed[key] = value
    expected = derive_controls(business_object, section, operation,
                               parsed.get("RangeStartDate"), parsed.get("RangeEndDate"),
                               registered_sections=registered_sections)
    if any(row[key] != value for key, value in expected.items()):
        raise ValueError(f"{section} controls differ from operation {operation}")
    return parsed.get("RangeStartDate")


def _same_new_parent(sections: dict[str, list[dict[str, str]]], operations: dict[str, list[str]],
                     business_object: str, child: dict[str, str], name_field: str) -> dict[str, str] | None:
    matches = [parent for parent, op in zip(sections.get(business_object, []), operations.get(business_object, []))
               if op == "create" and _present(child, name_field) and _present(child, "LegislationCode")
               and parent.get(name_field) == child[name_field]
               and parent.get("LegislationCode") == child["LegislationCode"]]
    if len(matches) > 1:
        raise ValueError("Ambiguous same-archive parent business key")
    return matches[0] if matches else None


def _plans(section: str, row: dict[str, str], operation: str, sections, operations) -> None:
    _omit(row, "EffectiveStartDate", "EffectiveEndDate")
    if section == "absencePlans":
        if operation == "create":
            _require(row, "AbsencePlanName", "AbsencePlanTypeCode", "LegislationCode", "AbsencePlanStatusCode")
            _identifier(row, "LegislativeDataGroupId")
            _omit(row, "AbsencePlanId")
            if row.get("AbsencePlanTypeCode") in {"A", "N"} and row.get("AbsencePlanPeriodType") == "C":
                _require(row, "CalendarStartMonth", "CalendarStartDay")
        else:
            _identifier(row, "AbsencePlanId")
        return
    new_parent = _same_new_parent(sections, operations, "absencePlans", row, "AbsencePlanName")
    if operation == "create" and new_parent is not None:
        _omit(row, "AbsencePlanId")
        if section in {"accrualBands", "eligibilityProfiles"} and row["effectiveOf"] != new_parent["effectiveOf"]:
            raise ValueError("New accrual band/eligibility profile date must equal the new parent date")
    else:
        _identifier(row, "AbsencePlanId")
    if section in PLAN_IDS:
        if operation == "create":
            _omit(row, PLAN_IDS[section])
        else:
            _identifier(row, PLAN_IDS[section])
    if section == "entitlementBandDetails":
        _identifier(row, "EntitlementBandId")
    if operation == "create":
        if section in {"accrualBands", "eligibilityProfiles", "entitlementBands", "entitlementBandDetails"}:
            _require(row, "Sequence")
        if section == "eligibilityProfiles":
            _identifier(row, "BenefitsEligibilityProfileId")
        if section == "entitlementBandDetails":
            _require(row, "Name")
        if section == "events":
            _identifier(row, "EventId")
            _require(row, "ProcessTypeCode")


def _categories(section: str, row: dict[str, str], operation: str, sections, operations) -> None:
    if section == "absenceCategories":
        if operation == "create":
            _require(row, "Name", "Status")
            _omit(row, "AbsenceCategoryId", "AncAbsCategoryFAltcd", "BaseName")
        else:
            _identifier(row, "AbsenceCategoryId")
            if operation == "end-date":
                _require(row, "EffectiveStartDate", "EffectiveEndDate", "Name", "Status")
                if "LegislationCode" not in row:  # A resolved blank is valid.
                    raise ValueError("Parent category end-date must preserve LegislationCode, including a returned blank")
    elif section == "absenceCategoryTypes":
        if operation == "create":
            _omit(row, "AbsenceTypeCateId")
            _identifier(row, "AbsenceTypeId")
            _require(row, "Status", "EffectiveStartDate")
            new_parent = _same_new_parent(sections, operations, "absenceCategories", row, "Name")
            if new_parent is None:
                _identifier(row, "AbsenceCategoryId")
            else:
                _omit(row, "AbsenceCategoryId")
        else:
            _identifier(row, "AbsenceTypeCateId")
            _identifier(row, "AbsenceCategoryId")
    elif operation != "create":
        _identifier(row, "AbsenceCategoryId")
        if operation in {"update", "correction"}:
            _require(row, "EffectiveStartDate", "EffectiveEndDate")
        if operation == "update":
            parents = [p for p, op in zip(sections.get("absenceCategories", []), operations.get("absenceCategories", []))
                       if op == "update" and p.get("AbsenceCategoryId") == row["AbsenceCategoryId"]
                       and p.get("effectiveOf") == row["effectiveOf"]]
            if len(parents) != 1:
                raise ValueError("Category flex UPDATE requires its parent UPDATE to establish the dated slice")


def _reasons(section: str, row: dict[str, str], operation: str, sections) -> None:
    if section == "absenceReasons":
        if operation == "create":
            _require(row, "Name", "LegislationCode", "Status", "EffectiveStartDate")
            _omit(row, "AbsenceReasonId", "EffectiveEndDate")
        else:
            _identifier(row, "AbsenceReasonId")
            if operation == "carrier-create":
                if set(row) != {"AbsenceReasonId", "RestAction", "effectiveOf"}:
                    raise ValueError("Reason carrier-create must be a key-only parent PATCH")
                children = [child for flex in ("AbsenceReasonsDDFFlex", "AbsenceReasonsFlex")
                            for child in sections.get(flex, [])
                            if child.get("AbsenceReasonId") == row["AbsenceReasonId"]
                            and child.get("effectiveOf") == row["effectiveOf"]
                            and child.get("RestAction") == "POST"]
                if not children:
                    raise ValueError("Reason carrier-create requires a matching flex child POST")
    else:
        _identifier(row, "AbsenceReasonId")
        parents = [p for p in sections.get("absenceReasons", [])
                   if p.get("AbsenceReasonId") == row["AbsenceReasonId"] and p.get("effectiveOf") == row["effectiveOf"]]
        if len(parents) != 1:
            raise ValueError("Reason flex requires one parent MERGE with the same AbsenceReasonId and effectiveOf")
        if row["RestAction"] != "DELETE" and parents[0].get("RestAction") not in {"POST", "PATCH"}:
            raise ValueError("Reason flex MERGE requires a parent MERGE, not DELETE")


def _agreements(section: str, row: dict[str, str], operation: str, sections, operations,
                registered_sections: dict | None = None) -> None:
    if section == "absenceLeaveAgreementTemplates":
        if operation == "create":
            _require(row, "AbsenceAgreementName", "AgreementPatternCode", "LegislationCode")
            _omit(row, "AbsenceAgreementId")
            pattern = row["AgreementPatternCode"]
            # Generic metadata-backed graph validation owns the parent key
            # spelling. Use documented name keys when present; do not invent
            # a missing key from a captured environment.
            created_parents = [p for p, op in zip(sections.get(section, []), operations.get(section, [])) if op == "create"]
            children = [p for p, op in zip(sections.get("absenceAgreementPlans", []), operations.get("absenceAgreementPlans", []))
                        if op == "create" and
                        ((p.get("AbsenceAgreementName") == row["AbsenceAgreementName"]
                          and p.get("LegislationCode") == row["LegislationCode"])
                         or (len(created_parents) == 1 and "AbsenceAgreementName" not in p))]
            if not children:
                raise ValueError("Agreement create requires at least one unambiguously linked target plan")
            if pattern == "ORA_ANC_CHP_AGRMT":
                _omit(row, "SourceAbsenceTypeId")
                for child in children:
                    _omit(child, "SourcePlanId")
            elif pattern == "ORA_ANC_CHP_CONV":
                _identifier(row, "SourceAbsenceTypeId")
                for child in children:
                    _identifier(child, "SourcePlanId")
            else:
                raise ValueError("Unsupported agreement pattern")
        else:
            _identifier(row, "AbsenceAgreementId")
            if operation == "delete" and any(
                    (child.get("AbsenceAgreementId") == row["AbsenceAgreementId"]
                     or not re.fullmatch(r"[1-9][0-9]*", str(child.get("AbsenceAgreementId", ""))))
                    for child_section, children in sections.items() if child_section != section for child in children):
                raise ValueError("Delete the current Leave Agreement as one parent action; do not synthesize child mutations "
                                 "or a cascade without an explicit resolved identity proving a distinct parent")
    elif operation in {"edit", "delete"}:
        descriptor = (registered_sections or {}).get(section, {})
        attributes = descriptor.get("attributes")
        if not isinstance(attributes, (list, tuple)):
            raise ValueError("Current registered child key metadata is required for Leave Agreement Edit or Delete")
        references = [a for a in attributes if isinstance(a, dict)
                      and a.get("AttributeMapKeyReferenceType") in {"LOCAL", "PARENT"}]
        if not any(a.get("AttributeMapKeyReferenceType") == "PARENT" for a in references):
            raise ValueError("Current registered parent key metadata is required for Leave Agreement child Edit or Delete")
        if not any(a.get("AttributeMapKeyReferenceType") == "LOCAL" for a in references) and not _registered_flex(
                "absenceLeaveAgreementTemplates", section, registered_sections):
            raise ValueError("Current registered child identity metadata is required for Leave Agreement Edit or Delete")
        for attribute in references:
            key = attribute.get("AttributeName")
            if not isinstance(key, str) or not key:
                raise ValueError("Current registered child reference metadata has no attribute name")
            if _present(row, key):
                continue  # A returned native key need not be a positive decimal.
            alternatives = descriptor.get("keyAlternatives", {}).get(key)
            if not isinstance(alternatives, (list, tuple)) or not alternatives:
                _require(row, key)
            if any(not isinstance(name, str) or name not in descriptor.get("headers", ()) for name in alternatives):
                raise ValueError("Current registered child key alternatives are incomplete")
            _require(row, *alternatives)
    if section == "absenceAgreementPlans":
        if operation == "create" or "TargetPlanId" in row:
            _identifier(row, "TargetPlanId")
        if _present(row, "SourcePlanId"):
            _identifier(row, "SourcePlanId")
        if "OverideFlag" in row:
            _identifier(row, "PaymentPercentDisplayFormulaId")
            if row["OverideFlag"] not in {"true", "false"}:
                raise ValueError("OverideFlag requires a resolved Boolean, not Y/N")
    elif section == "absenceAgreementCertifications" and (operation == "create" or "AbsenceCertificationId" in row):
        _identifier(row, "AbsenceCertificationId")
    if _present(row, "EligibilityFormulaId") and _present(row, "EligibilityProfileId"):
        raise ValueError("Eligibility Formula and Eligibility Profile are mutually exclusive")


def _certifications(section, row, operation, context, registered_sections):
    """UI evidence supplements registration; this offline check grants no approval."""
    context = context or {}
    if not isinstance(context, dict):
        raise ValueError("Certification UI context must be an object")
    saved = context.get("beforeState", {})
    management = context.get("meanings", {}).get("ManagementTypeCode") if isinstance(context.get("meanings", {}), dict) else None
    if (operation != "create" and isinstance(saved, dict) and isinstance(management, dict)
            and management.get("code") == saved.get("ManagementTypeCode")
            and management.get("meaning") == "Pre-defined"):
        raise ValueError("The reviewed Redwood predefined certification exposes no enabled maintenance action")
    if section != "absenceCertifications":
        if operation not in {"create", "update", "correction"}:
            raise ValueError("Certification flex edits belong to the parent form, not separate Delete/End Date actions")
        descriptor = (registered_sections or {}).get(section, {})
        visible = context.get("visibleFields")
        if not isinstance(visible, list) or any(not isinstance(f, str) or f not in descriptor.get("headers", ()) for f in visible):
            raise ValueError("Certification flex input requires current Redwood-visible context/segment evidence")
        keys = {a.get("AttributeName") for a in descriptor.get("attributes", ()) if isinstance(a, dict)
                and a.get("AttributeMapKeyReferenceType") in {"LOCAL", "PARENT"}}
        keys.update(f for fs in descriptor.get("keyAlternatives", {}).values() for f in fs)
        if any(_present(row, f) and f not in set(visible) | keys | {"RestAction", "effectiveOf"} for f in row):
            raise ValueError("Certification flex field is not exposed in the current Redwood form")
        return
    for field in row:
        if _present(row, field) and field not in CERTIFICATION_FIELDS:
            raise ValueError(f"Certification field is not exposed in Redwood: {field}")
    if operation in {"end-date", "zap", "delete-changes"}:
        if any(_present(row, f) and f not in CERTIFICATION_CONTROLS for f in row):
            raise ValueError("Certification End Date/Delete does not accept configuration edits")
        if operation == "zap" and any(_present(row, f) for f in ("EffectiveStartDate", "EffectiveEndDate")):
            raise ValueError("Whole certification Delete accepts no mutation date")
        if operation == "end-date" and _present(row, "EffectiveEndDate") and row["effectiveOf"] != "RangeMode=END_DATE;RangeEndDate=" + row["EffectiveEndDate"]:
            raise ValueError("Certification physical end date must match the chosen End Date")
        if operation == "end-date" and saved:
            if (not isinstance(saved, dict)
                    or str(saved.get("AbsenceCertificationId", "")) != row.get("AbsenceCertificationId")):
                raise ValueError("Certification End Date requires the exact selected identity")
            start = _iso(saved.get("EffectiveStartDate"), "Selected Start Date")
            end = _iso(saved.get("EffectiveEndDate"), "Selected End Date")
            chosen = _iso(row["effectiveOf"].removeprefix("RangeMode=END_DATE;RangeEndDate="), "End Date")
            if not start <= chosen <= end:
                raise ValueError("Certification End Date must be within the selected row's stored date range")
        if operation == "delete-changes":
            evidence = context.get("deleteRecordEvidence", {})
            if (not isinstance(saved, dict) or not isinstance(evidence, dict)
                    or evidence.get("action") != "Delete Record"
                    or evidence.get("historyComplete") is not True
                    or evidence.get("adapterContract") != "DELETE_CHANGES_PHYSICAL_ROW"
                    or not isinstance(management, dict) or management.get("meaning") != "User-defined"
                    or management.get("code") != saved.get("ManagementTypeCode")
                    or not row.get("AbsenceCertificationId")):
                raise ValueError("Certification Delete Record requires exact selected row, "
                                 "complete History, User-defined protection and verified physical-row adapter evidence")
            for field in ("AbsenceCertificationId", "EffectiveStartDate", "EffectiveEndDate"):
                if not saved.get(field) or evidence.get(field) != saved[field]:
                    raise ValueError("Certification Delete Record evidence must match the exact selected row")
            if (saved["AbsenceCertificationId"] != row["AbsenceCertificationId"]
                    or row["effectiveOf"] != "RangeMode=DELETE_CHANGES;RangeStartDate="
                    + _iso(saved["EffectiveStartDate"], "Selected stored Start Date")
                    or any(_present(row, f) for f in ("EffectiveStartDate", "EffectiveEndDate"))):
                raise ValueError("Certification Delete Record uses only the selected row's stored start in effectiveOf")
            resolver_scripts = (
                Path(__file__).resolve().parents[2]
                / "absences-additional" / "absence-certifications" / "scripts"
            )
            if str(resolver_scripts) not in sys.path:
                sys.path.insert(0, str(resolver_scripts))
            from resolve_certification_delete_record import validate_evidence, validate_history
            validate_history(saved, evidence.get("history"))
            validate_evidence(evidence, saved, context.get("meanings", {}))
        return
    if operation in {"update", "correction"}:
        for field in row:
            if _present(row, field) and field not in CERTIFICATION_MAINTENANCE_FIELDS | CERTIFICATION_CONTROLS:
                raise ValueError(f"{field} is read-only or hidden in certification {operation.title()}")
        if _present(row, "EffectiveEndDate"):
            raise ValueError("Stored Effective End Date is read-only; use the separate End Date action")
    if operation == "create":
        _require(row, "Name", "ClassificationCode", "LegislationCode", "TriggerCode", "StatusCode")
        if row["ClassificationCode"] not in {"ORA_ANC_DOCUMENTATION", "ORA_ANC_PAYMENT_PERCENT"}:
            raise ValueError("Redwood Add offers only Documentation or Entitlement")
        if _present(row, "ManagementTypeCode") and row["ManagementTypeCode"] != "UD":
            raise ValueError("Management is read-only User-defined for certification Create")
        if _present(row, "EffectiveEndDate"):
            raise ValueError("Certification Create has no Effective End Date input")
    before, meanings = context.get("beforeState", {}), context.get("meanings", {})
    if (not isinstance(before, dict) or any(not isinstance(v, str) for v in before.values())
            or not isinstance(meanings, dict)):
        raise ValueError("Certification UI context requires beforeState and meanings objects")
    if operation == "create" and before:
        raise ValueError("New certification rules cannot borrow an existing beforeState")
    if operation == "correction" and "EffectiveStartDate" in before:
        if (before.get("AbsenceCertificationId") != row.get("AbsenceCertificationId")
                or row["effectiveOf"] != "RangeMode=CORRECTION;RangeStartDate=" + _iso(before["EffectiveStartDate"], "Selected stored Start Date")):
            raise ValueError("Certification Correct must use the exact selected row's stored Start Date")
    state = {**before, **{f: v for f, v in row.items() if _present(row, f)}}
    for field in CERTIFICATION_MAINTENANCE_FIELDS:
        if field in row:
            state[field] = row[field]  # Explicit mutable clears participate in completeness.

    def meaning(field):
        resolved = meanings.get(field)
        if (not isinstance(resolved, dict) or resolved.get("code") != state.get(field)
                or not isinstance(resolved.get("meaning"), str) or not resolved["meaning"]):
            raise ValueError(f"Current resolved Redwood meaning is required for {field}")
        return resolved["meaning"]

    if _present(row, "StatusCode") and meaning("StatusCode") not in {"Active", "Inactive"}:
        raise ValueError("Redwood certification Status offers only Active or Inactive")
    if _present(row, "AbsenceRecordUpdateRuleCode") and meaning("AbsenceRecordUpdateRuleCode") not in {
            "None", "Update authorization status", "Update late notice waiver status"}:
        raise ValueError("Absence Record Update Rule is not exposed in Redwood")
    conditional = CERTIFICATION_FIELDS - CERTIFICATION_CONTROLS - {
        "Name", "Description", "StatusCode", "ClassificationCode", "LegislationCode", "ManagementTypeCode"}
    if operation != "create" and not any(f in row for f in conditional - set(CERTIFICATION_UPDATE_IMMUTABLE)):
        return  # Do not recollect create inputs for a Description/status-only edit.
    if operation != "create" and before.get("AbsenceCertificationId") != row.get("AbsenceCertificationId"):
        raise ValueError("Certification conditional beforeState must match the exact selected identity")
    classification = state.get("ClassificationCode")
    if classification not in {"ORA_ANC_DOCUMENTATION", "ORA_ANC_PAYMENT_PERCENT"}:
        raise ValueError("Conditional edits require the saved Classification context")
    trigger, entitlement = meaning("TriggerCode"), classification == "ORA_ANC_PAYMENT_PERCENT"
    if trigger not in {"On demand", "On absence submit"} | ({"Managed by entitlement formula"} if entitlement else set()):
        raise ValueError("Trigger is not exposed for the selected Redwood Classification")
    managed = trigger == "Managed by entitlement formula"

    def hidden(fields, label):
        if any(_present(row, f) for f in fields):
            raise ValueError(f"{label} fields are hidden in this Redwood branch")

    def require_values(*fields):
        _require(state, *fields)
        if any(state[f].strip().lower() == "null" for f in fields):
            raise ValueError("Required Redwood values cannot be null")

    if trigger != "On absence submit":
        hidden(("EligibilityProfileId",), "Eligibility Profile")
    elif _present(row, "EligibilityProfileId") and row["EligibilityProfileId"].lower() != "null":
        _identifier(row, "EligibilityProfileId")
    if not managed:
        hidden(("AllowOnDemandFlag", "ConfirmOnDemandFlag"), "Formula-managed on-demand")
    if not entitlement:
        hidden(tuple(f for fs in CERTIFICATION_EVENTS.values() for f in fs[1:]), "Entitlement event")
    if managed:
        hidden(tuple(f for fs in CERTIFICATION_DATES.values() for f in fs)
               + CERTIFICATION_EVENTS["DueDate"] + CERTIFICATION_EVENTS["Expiration"]
               + CERTIFICATION_EVENTS["Create"][1:], "Formula-managed date/creation reevaluation")
    for field in ("AutoCompleteFlag", "AllowOnDemandFlag", "ConfirmOnDemandFlag"):
        if _present(row, field) and row[field] not in {"Y", "N"}:
            raise ValueError(f"{field} requires the resolved Y/N checkbox value")
    for rule, values in CERTIFICATION_REASONS.items():
        if rule not in row and values not in row:
            continue
        selected = meaning(rule)
        if selected == "Entry required":
            require_values(values)
            codes = [v.strip() for v in state[values].split(",")]
            if any(not v for v in codes) or len(codes) != len(set(codes)):
                raise ValueError("Required Reasons must be a complete, nonduplicate selection")
        elif selected == "Not applicable":
            hidden((values,), "Not applicable reason")
        else:
            raise ValueError("Reason Rule is not exposed in Redwood")
    visible = context.get("visibleFields", [])
    if not isinstance(visible, list) or any(not isinstance(f, str) or f not in CERTIFICATION_FIELDS for f in visible):
        raise ValueError("Invalid certification Redwood-visible field evidence")
    for event, fields in CERTIFICATION_EVENTS.items():
        if any(_present(row, f) and f not in visible for f in fields):
            raise ValueError(f"{event} event input has no visible Redwood control evidence")
        if _present(row, fields[0]) and meaning(fields[0]) not in {"None", "Set value to true", "Set value to false"}:
            raise ValueError("Absence Record Update choice is not exposed in Redwood")
    if operation != "create":
        return
    for event, fields in CERTIFICATION_DATES.items():
        rule, *dependents = fields
        if managed or not any(f in row for f in fields):
            continue
        selected = meaning(rule)
        if selected == "Calculate date":
            require_values(*dependents)
        elif selected in {"Capture date", "Not applicable"}:
            hidden(dependents, event + " calculation")
            if event == "DueDate" and selected == "Not applicable":
                hidden(CERTIFICATION_EVENTS[event], "Not applicable due-date event")
        else:
            raise ValueError("Date Rule is not exposed in Redwood")
    if entitlement:
        for event, fields in CERTIFICATION_EVENTS.items():
            _, calculation, mode, override = fields
            choices = {f: meaning(f) for f in (calculation, mode) if _present(row, f)}
            reevaluations = {f: m for f, m in choices.items() if m in {
                "Not applicable", "As of absence start date", "As of action date"}}
            updates = {f: m for f, m in choices.items() if m in {"None", "Override", "Recalculate", "Retract"}}
            if choices or _present(row, override):
                # The current LOV bindings determine the two roles, not guessed
                # CALC/CALC_MODE names or assumed reusable tenant codes.
                if len(reevaluations) != 1 or len(reevaluations) + len(updates) != len(choices):
                    raise ValueError("Entitlement update requires its own resolved reevaluation rule")
                selected = next(iter(reevaluations.values()))
                if selected == "Not applicable":
                    hidden(tuple(updates) + (override,), event + " entitlement update")
                elif len(updates) != 1:
                    raise ValueError("Applicable reevaluation requires Entitlement Update Rule")
                elif next(iter(updates.values())) == "Override":
                    require_values(override)
                    try:
                        if not Decimal(state[override]).is_finite():
                            raise ValueError("Revised Payment Percentage must be finite")
                    except InvalidOperation as exc:
                        raise ValueError("Revised Payment Percentage must be numeric") from exc
                else:
                    hidden((override,), event + " payment override")


def validate_task_rows(business_object: str, sections: dict[str, list[dict[str, str]]],
                       operations: dict[str, list[str]], *,
                       registered_sections: dict[str, dict] | None = None,
                       certification_contexts: dict | None = None) -> None:
    """Check local shape/task invariants; never claim live validation or approval."""
    if business_object not in SECTIONS:
        raise ValueError(f"Unsupported business object: {business_object}")
    if certification_contexts is not None and not isinstance(certification_contexts, dict):
        raise ValueError("Certification UI contexts must be a section-keyed object")
    if set(sections) != set(operations):
        raise ValueError("Section and operation inventories differ")
    for section, rows in sections.items():
        if section not in SECTIONS[business_object] and not _registered_flex(business_object, section, registered_sections):
            raise ValueError(f"Unsupported task section: {section}")
        if len(rows) != len(operations[section]):
            raise ValueError(f"Row/operation counts differ for {section}")
        contexts = (certification_contexts or {}).get(section, [{} for _ in rows])
        if business_object == "absenceCertifications" and (not isinstance(contexts, list) or len(contexts) != len(rows)):
            raise ValueError("Certification UI contexts must match section row counts")
        for index, (row, operation) in enumerate(zip(rows, operations[section])):
            if not isinstance(row, dict) or any(not isinstance(v, str) for v in row.values()):
                raise ValueError("Task validators require final serialized string values")
            start = _controls(business_object, section, operation, row, registered_sections)
            if business_object == section == "absenceCertifications" and operation == "update":
                for field, label in CERTIFICATION_UPDATE_IMMUTABLE.items():
                    if _present(row, field):
                        raise ValueError(f"{label} cannot be changed by Update; leave its data-record value blank")
            if business_object == "absenceCertifications":
                _certifications(section, row, operation, contexts[index], registered_sections)
            if business_object == "absenceLeaveAgreementTemplates" and operation in {"edit", "delete"}:
                guarded = LEAVE_EDIT_IMMUTABLE if section == business_object and operation == "edit" else {
                    "EffectiveStartDate": "stored Start Date", "EffectiveEndDate": "stored End Date"}
                for field, label in guarded.items():
                    if _present(row, field):
                        raise ValueError(f"{label} is read-only in Leave Agreement {operation.title()}; "
                                         "leave its data-record value blank")
            for field in ("EffectiveStartDate", "EffectiveEndDate"):
                if _present(row, field):
                    _iso(row[field], field)
            if _present(row, "EffectiveStartDate") and _present(row, "EffectiveEndDate") and row["EffectiveStartDate"] > row["EffectiveEndDate"]:
                raise ValueError("Physical effective date range is reversed")
            if business_object in {"absenceLeaveAgreementTemplates", "absenceCertifications"} and _present(row, "EffectiveStartDate"):
                if start is None or row["EffectiveStartDate"] != start:
                    raise ValueError("Physical EffectiveStartDate must match RangeStartDate")
                # Preserve a potentially supported dual-date input, but do not
                # certify it from header presence. The task's existing live
                # operation/section evidence gate remains mandatory before preview.
            if business_object in {"absenceReasons", "absenceCategories"} and operation == "create" and _present(row, "EffectiveStartDate") and row["EffectiveStartDate"] != start:
                raise ValueError("Create physical start and effectiveOf disagree")
            if business_object == "absenceCategories" and operation == "end-date" and _present(row, "EffectiveEndDate") and row["effectiveOf"] != "RangeMode=END_DATE;RangeEndDate=" + row["EffectiveEndDate"]:
                raise ValueError("Category physical end and END_DATE control disagree")
            if business_object == "absenceCategories" and section in {"AbsenceCategoriesDDFFlex", "AbsenceCategoriesFlex"} and operation == "update" and row.get("EffectiveStartDate") != start:
                raise ValueError("Category flex UPDATE physical start must identify the planned new slice")
            if business_object == "absencePlans":
                _plans(section, row, operation, sections, operations)
            elif business_object == "absenceCategories":
                _categories(section, row, operation, sections, operations)
            elif business_object == "absenceReasons":
                _reasons(section, row, operation, sections)
            elif business_object == "absenceLeaveAgreementTemplates":
                _agreements(section, row, operation, sections, operations, registered_sections)
            elif section == "absenceCertifications":
                if operation == "create":
                    _require(row, "Name", "ClassificationCode", "LegislationCode", "TriggerCode", "StatusCode")
                    _omit(row, "AbsenceCertificationId")
                else:
                    _identifier(row, "AbsenceCertificationId")
