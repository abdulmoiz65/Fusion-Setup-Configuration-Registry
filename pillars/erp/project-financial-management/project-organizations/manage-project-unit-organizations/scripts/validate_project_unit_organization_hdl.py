#!/usr/bin/env python3
"""Offline HDL checks and generation. Tenant evidence and load approval remain workflow gates."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from datetime import date
from pathlib import Path

MEMBER = "Organization.dat"
PROJECT_UNIT_CODE = "projectUnitCode(PER_ORGANIZATION_INFORMATION_EFF=PRJ_PU_ATTRIBUTES)"
CREATE = "CREATE_NEW"
EXISTING = "USE_EXISTING_ORGANIZATION"
CLASSIFICATION = "Project Unit Classification"
DATES = ["EffectiveStartDate", "EffectiveEndDate"]
INFO = DATES + ["OrganizationName", "ClassificationName", "SequenceNumber",
               "FLEX:PER_ORGANIZATION_INFORMATION_EFF", "EFF_CATEGORY_CODE",
               "OrgInformationContext", PROJECT_UNIT_CODE]
HEADERS = {
    CREATE: {
        "Organization": DATES + ["Name", "ClassificationCode", "ClassificationName"],
        "OrgInformation": INFO,
        "OrgUnitClassification": DATES + ["OrganizationName", "ClassificationName", "Status"],
    },
    EXISTING: {
        "Organization": DATES + ["Name", "ClassificationCode", "ClassificationName"],
        "OrgUnitClassification": DATES + ["OrganizationName", "ClassificationName", "ClassificationCode", "Status"],
        "OrgInformation": INFO,
    },
}


def parse_date(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}/[0-9]{2}/[0-9]{2}", value):
        raise ValueError("Date must use YYYY/MM/DD.")
    return date(*map(int, value.split("/")))


def normalize_rest_date(value, field):
    """Normalize REST evidence without relaxing the request's YYYY/MM/DD contract."""
    if isinstance(value, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        value = value.replace("-", "/")
    try:
        parse_date(value)
    except ValueError as error:
        raise ValueError(f"{field} must be a valid REST YYYY-MM-DD or normalized YYYY/MM/DD date.") from error
    return value


def text_field(value, field, limit):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"{field} must be a nonblank string of at most {limit} characters.")
    if any(c in value for c in "|\r\n\\") or any(ord(c) < 32 for c in value):
        raise ValueError(f"{field} contains unsupported HDL control/delimiter characters.")
    return value


def required_code(request):
    code = request.get("ProjectUnitCode")
    if code is None or (isinstance(code, str) and not code.strip()):
        suggestion = suggested_code(request)
        if suggestion:
            raise ValueError(
                f"ProjectUnitCode is required; ask the user to accept suggested code {suggestion} "
                "or enter a code.")
        raise ValueError("ProjectUnitCode is required; ask the user to enter a code.")
    return text_field(code, "ProjectUnitCode", 150)


def suggested_code(request):
    """Offer a name-derived code without ever placing it in an HDL request."""
    try:
        name = requested_organization_name(request)
    except ValueError:
        return None
    code = re.sub(r"_+", "_", re.sub(r"[^A-Z0-9_]+", "_", name.strip().upper()))[:150]
    return code if code.strip("_") else None


def requested_organization_name(request):
    """Return the one exact organization name supplied for route discovery."""
    supplied = [
        (field, request[field])
        for field in ("ProjectUnitName", "ExistingOrganizationName")
        if request.get(field) is not None
    ]
    if not supplied:
        raise ValueError("Supply ProjectUnitName or ExistingOrganizationName for organization routing.")
    names = [text_field(value, field, 240) for field, value in supplied]
    if len(set(names)) != 1:
        raise ValueError("ProjectUnitName and ExistingOrganizationName must match when both are supplied.")
    return names[0]


def derive_action(request, evidence):
    """Derive the HDL route from complete exact-name organization-search evidence."""
    if "Action" in request:
        raise ValueError("Action is derived from organization-search evidence and must be omitted from the request.")
    if evidence.get("OrganizationSearchComplete") is not True:
        raise ValueError("Complete organization-search evidence is required to derive the action.")
    matches = evidence.get("ActiveOrganizationMatches")
    if not isinstance(matches, list):
        raise ValueError("ActiveOrganizationMatches must be a complete list from the organization search.")
    name = requested_organization_name(request)
    for match in matches:
        if (not isinstance(match, dict) or not match.get("OrganizationId")
                or match.get("Name") != name or match.get("Active") is not True):
            raise ValueError("Every active organization match must contain the exact name, ID, and Active=true.")
    if not matches:
        return CREATE
    if len({match["OrganizationId"] for match in matches}) != len(matches):
        raise ValueError("ActiveOrganizationMatches must contain distinct OrganizationIds.")
    if len(matches) > 1 and evidence.get("SelectionConfirmed") is not True:
        raise ValueError("Multiple active organization matches require explicit selection; no HDL can be generated.")
    selected = evidence.get("SelectedOrganization")
    if (not isinstance(selected, dict) or not any(
            selected.get("OrganizationId") == match["OrganizationId"]
            and selected.get("Name") == match["Name"] for match in matches)):
        raise ValueError("SelectedOrganization must be bound to an exact active organization match.")
    if evidence.get("ClassificationsComplete") is not True or not isinstance(evidence.get("Classifications"), list):
        raise ValueError("Complete unfiltered classification evidence is required to derive the existing route.")
    start = request.get("EffectiveStartDate") or normalize_rest_date(
        selected.get("EffectiveStartDate"), "SelectedOrganization.EffectiveStartDate")
    start_date = parse_date(start)
    for row in evidence["Classifications"]:
        if not isinstance(row, dict) or row.get("OrganizationId") != selected["OrganizationId"]:
            raise ValueError("Classification evidence belongs to another OrganizationId.")
        if row.get("Status") not in {"A", "I"}:
            raise ValueError("Classification status is missing or unresolved.")
        if (row["Status"] == "A" and row.get("ClassificationCode") == "PRJ_PROJECT_UNIT"
                and parse_date(normalize_rest_date(row.get("EffectiveStartDate"), "Classifications.EffectiveStartDate"))
                <= start_date <= parse_date(normalize_rest_date(row.get("EffectiveEndDate"), "Classifications.EffectiveEndDate"))):
            raise ValueError("Organization is already an active PRJ_PROJECT_UNIT; no HDL can be generated.")
    return EXISTING


def derive_tree_placement_decision(request, evidence, selected, start_date):
    """Route declared tree placement without performing a tree write."""
    required = request.get("RequiredTreePlacement")
    if required is None:
        return "NOT_IN_SCOPE"
    if not isinstance(required, dict):
        raise ValueError("RequiredTreePlacement must be an object when supplied.")
    tree_code = text_field(required.get("TreeCode"), "RequiredTreePlacement.TreeCode", 240)
    parent_name = text_field(
        required.get("ParentOrganizationName"), "RequiredTreePlacement.ParentOrganizationName", 240)
    if selected is None:
        return "MANAGE_ORGANIZATION_TREES_REQUIRED_AFTER_POST_LOAD"
    placement = evidence.get("TreePlacementEvidence")
    if not isinstance(placement, dict) or placement.get("Fresh") is not True:
        raise ValueError("Fresh TreePlacementEvidence is required for an existing organization tree decision.")
    if (placement.get("TreeCode") != tree_code or not placement.get("TreeVersionId")
            or placement.get("ParentOrganizationName") != parent_name
            or not placement.get("ParentOrganizationId")
            or placement.get("ChildOrganizationId") != selected["OrganizationId"]
            or placement.get("ChildOrganizationName") != selected["Name"]):
        raise ValueError("Tree placement evidence must match the required tree, parent, and selected organization.")
    if placement.get("PlacementExists") is not True:
        return "MANAGE_ORGANIZATION_TREES_REQUIRED"
    lower = parse_date(normalize_rest_date(
        placement.get("EffectiveStartDate"), "TreePlacementEvidence.EffectiveStartDate"))
    upper = parse_date(normalize_rest_date(
        placement.get("EffectiveEndDate"), "TreePlacementEvidence.EffectiveEndDate"))
    if not lower <= start_date <= upper:
        raise ValueError("Existing tree placement is not effective on the Project Unit start date.")
    return "REUSE_EXISTING_TREE_PLACEMENT"


def prepare_request(request, evidence):
    """Consume fresh, target-bound resolver evidence; these flags are attestations."""
    if not isinstance(request, dict) or not isinstance(evidence, dict):
        raise ValueError("Request and evidence must be JSON objects.")
    if {"SourceSystemOwner", "SourceSystemId", "SetCode", "ReferenceDataSet"}.intersection(request):
        raise ValueError("Source-system and reference-data-set fields must be omitted.")
    code = required_code(request)
    if not request.get("TargetEnvironment") or request["TargetEnvironment"] != evidence.get("TargetEnvironment"):
        raise ValueError("Evidence must match the exact TargetEnvironment.")
    if not evidence.get("EvidenceRef") or evidence.get("Fresh") is not True:
        raise ValueError("Fresh workflow evidence and EvidenceRef are required.")
    action = derive_action(request, evidence)
    selected = None
    existing_start = None
    existing_classification_code = None
    if action == CREATE:
        name = requested_organization_name(request)
        classification = CLASSIFICATION
        start = request.get("EffectiveStartDate")
        if start is None or start == "":
            start = "0001/01/01"
    else:
        requested_name = requested_organization_name(request)
        selected = evidence.get("SelectedOrganization")
        if not isinstance(selected, dict) or not selected.get("OrganizationId"):
            raise ValueError("Select an exact OrganizationId from organization search results.")
        name = text_field(selected.get("Name"), "OrganizationName", 240)
        if requested_name != name:
            raise ValueError("ExistingOrganizationName must preserve the exact returned name.")
        existing_classification_code = text_field(
            selected.get("ClassificationCode"), "SelectedOrganization.ClassificationCode", 240)
        resolved_classification = evidence.get("ResolvedOrganizationClassification")
        if (not isinstance(resolved_classification, dict)
                or not resolved_classification.get("EvidenceRef")
                or resolved_classification.get("ClassificationCode") != existing_classification_code):
            raise ValueError(
                "Exact organizationClassificationsLOV evidence is required for the selected classification code.")
        classification = text_field(
            resolved_classification.get("ClassificationName"),
            "ResolvedOrganizationClassification.ClassificationName", 240)
        if classification == CLASSIFICATION:
            raise ValueError(
                "The existing Organization anchor cannot use Project Unit Classification.")
        if (selected.get("ClassificationName") is not None
                and selected["ClassificationName"] != classification):
            raise ValueError(
                "Selected organization classification name must match the exact LOV display label.")
        if request.get("ExistingClassification") is not None and request["ExistingClassification"] not in (
                existing_classification_code, classification):
            raise ValueError("ExistingClassification does not match the selected classification record.")
        if request.get("ExistingLocation") is not None:
            location = evidence.get("SelectedLocation", {})
            if (not isinstance(location, dict) or not location.get("LocationId") or location.get("LocationName") != request["ExistingLocation"]
                    or location["LocationId"] != selected.get("LocationId") or location.get("Active") is not True):
                raise ValueError("ExistingLocation requires an exact active selected LocationId.")
        existing_start = normalize_rest_date(
            selected.get("EffectiveStartDate"), "SelectedOrganization.EffectiveStartDate")
        start = request.get("EffectiveStartDate")
        if start is None or start == "":
            start = existing_start
    start_date = parse_date(start)
    end = request.get("EffectiveEndDate")
    if end is None:
        end = ""
    end_date = parse_date(end) if end != "" else None
    if end_date and end_date < start_date:
        raise ValueError("EffectiveEndDate precedes EffectiveStartDate.")
    if selected:
        selected_end = normalize_rest_date(
            selected.get("EffectiveEndDate"), "SelectedOrganization.EffectiveEndDate")
        lower, upper = parse_date(existing_start), parse_date(selected_end)
        if selected.get("Active") is not True or not lower <= start_date <= upper:
            raise ValueError("Selected organization must be active within its effective range.")
        if end_date and end_date > upper:
            raise ValueError("EffectiveEndDate exceeds the selected organization's effective range.")
        if evidence.get("ClassificationsComplete") is not True:
            raise ValueError("Complete unfiltered organization classifications are required.")
        rows = evidence.get("Classifications")
        if not isinstance(rows, list) or not rows:
            raise ValueError("Classification evidence is missing.")
        matched_parent = False
        for row in rows:
            if not isinstance(row, dict) or row.get("OrganizationId") != selected["OrganizationId"]:
                raise ValueError("Classification evidence belongs to another OrganizationId.")
            if row.get("Status") not in {"A", "I"}:
                raise ValueError("Classification status is missing or unresolved.")
            row_start = normalize_rest_date(
                row.get("EffectiveStartDate"), "Classifications.EffectiveStartDate")
            row_end = normalize_rest_date(
                row.get("EffectiveEndDate"), "Classifications.EffectiveEndDate")
            active = row["Status"] == "A" and parse_date(row_start) <= start_date <= parse_date(row_end)
            if active and row.get("ClassificationCode") == "PRJ_PROJECT_UNIT":
                raise ValueError("Organization already has an active PRJ_PROJECT_UNIT classification.")
            if (active and row.get("ClassificationCode") == existing_classification_code
                    and row.get("ClassificationName") == classification):
                matched_parent = True
        if not matched_parent:
            raise ValueError("Selected parent classification must be an exact active returned record.")
    value_set = evidence.get("CodeValueSetValidation", "unavailable")
    if value_set not in ("passed", "unavailable"):
        raise ValueError("Configured Project Unit Code value-set validation did not pass.")
    if value_set == "passed" and evidence.get("ValidatedProjectUnitCode") != code:
        raise ValueError("Value-set evidence must be bound to the exact ProjectUnitCode.")
    result = {"Action": action, "Name": name, "ClassificationName": classification,
              "ProjectUnitCode": code, "EffectiveStartDate": start, "EffectiveEndDate": end}
    result["TreePlacementDecision"] = derive_tree_placement_decision(
        request, evidence, selected, start_date)
    if selected:
        result.update(
            ExistingOrganizationEffectiveStartDate=existing_start,
            ExistingOrganizationClassificationCode=existing_classification_code,
        )
    return result


def generate_dat(request, evidence):
    row = prepare_request(request, evidence)
    return render_rows([row], row["Action"])


def render_rows(rows, action):
    """Write one metadata layout per component and one MERGE per organization."""
    if not rows or action not in HEADERS or any(row["Action"] != action for row in rows):
        raise ValueError("HDL rows must share one supported action.")
    sections = []
    for component, headers in HEADERS[action].items():
        lines = ["|".join(["METADATA", component] + headers)]
        for row in rows:
            values = {
                **row, "OrganizationName": row["Name"], "ClassificationCode": "PRJ_PROJECT_UNIT",
                "SequenceNumber": "1", "FLEX:PER_ORGANIZATION_INFORMATION_EFF": "PRJ_PU_ATTRIBUTES",
                "EFF_CATEGORY_CODE": "PRJ_PROJECT_UNIT", "OrgInformationContext": "PRJ_PU_ATTRIBUTES",
                PROJECT_UNIT_CODE: row["ProjectUnitCode"], "Status": "A",
            }
            if action == EXISTING and component == "Organization":
                values.update(
                    EffectiveStartDate=row["ExistingOrganizationEffectiveStartDate"],
                    EffectiveEndDate="",
                    ClassificationCode=row["ExistingOrganizationClassificationCode"],
                )
            lines.append("|".join(["MERGE", component] + [values[h] for h in headers]))
        sections.append("\n".join(lines))
    return "\n\n".join(sections) + "\n"


def validate_text(content, action=None):
    errors, metadata, records, events = [], {}, {}, []
    for number, line in enumerate(content.splitlines(), 1):
        if not line.strip():
            continue
        values = line.split("|")
        if len(values) < 2 or values[0] not in {"METADATA", "MERGE"}:
            errors.append(f"Line {number}: expected METADATA or MERGE.")
            continue
        kind, component = values[:2]
        events.append((kind, component))
        if component not in HEADERS[CREATE]:
            errors.append(f"Line {number}: unsupported component {component}.")
            continue
        if kind == "METADATA":
            if component in metadata or len(set(values[2:])) != len(values[2:]):
                errors.append(f"Line {number}: duplicate metadata or headers.")
            metadata[component] = values[2:]
        elif component not in metadata or len(values[2:]) != len(metadata[component]):
            errors.append(f"Line {number}: MERGE must follow metadata with the same field count.")
        else:
            records.setdefault(component, []).append(dict(zip(metadata[component], values[2:])))
    action = action or (
        EXISTING if "ClassificationCode" in metadata.get("OrgUnitClassification", []) else CREATE)
    if action not in HEADERS:
        return errors + ["Action must be CREATE_NEW or USE_EXISTING_ORGANIZATION."]
    expected = HEADERS[action]
    if events != [(kind, component) for component in expected for kind in ("METADATA", "MERGE")]:
        errors.append(f"{action}: require exactly one METADATA/MERGE pair per component in documented order.")
    for component, headers in expected.items():
        if metadata.get(component) != headers:
            errors.append(f"{component}: headers must exactly match the {action} contract (no source keys, SetCode or OrganizationId).")
        if len(records.get(component, [])) != 1:
            errors.append(f"{component}: expected exactly one MERGE row.")
    if errors:
        return errors
    rows = {component: records[component][0] for component in expected}
    first = next(iter(rows.values()))
    name, classification = first.get("Name", first.get("OrganizationName")), first["ClassificationName"]
    for component, row in rows.items():
        try:
            text_field(row.get("Name", row.get("OrganizationName")), f"{component}.Name", 240)
            text_field(row["ClassificationName"], f"{component}.ClassificationName", 240)
            start = parse_date(row["EffectiveStartDate"])
            end = parse_date(row["EffectiveEndDate"]) if row["EffectiveEndDate"] else None
            if end and end < start:
                errors.append(f"{component}: EffectiveEndDate precedes EffectiveStartDate.")
        except ValueError as error:
            errors.append(f"{component}: {error}")
        if row.get("Name", row.get("OrganizationName")) != name or row["ClassificationName"] != classification:
            errors.append(f"{component}: exact parent name and classification must match across components.")
        if action == CREATE and any(row[field] != first[field] for field in DATES):
            errors.append(f"{component}: effective dates must match across components.")
        if (action == EXISTING and component != "Organization"
                and any(row[field] != rows["OrgUnitClassification"][field] for field in DATES)):
            errors.append(f"{component}: child effective dates must match.")
        fixed = {"Status": "A", "SequenceNumber": "1",
                 "FLEX:PER_ORGANIZATION_INFORMATION_EFF": "PRJ_PU_ATTRIBUTES",
                 "EFF_CATEGORY_CODE": "PRJ_PROJECT_UNIT", "OrgInformationContext": "PRJ_PU_ATTRIBUTES"}
        if action == CREATE:
            fixed["ClassificationCode"] = "PRJ_PROJECT_UNIT"
            fixed["ClassificationName"] = CLASSIFICATION
        elif component == "OrgUnitClassification":
            fixed["ClassificationCode"] = "PRJ_PROJECT_UNIT"
        for field, value in fixed.items():
            if field in row and row[field] != value:
                errors.append(f"{component}.{field} must be {value!r}.")
    if action == EXISTING:
        anchor = rows["Organization"]
        try:
            text_field(anchor["ClassificationCode"], "Organization.ClassificationCode", 240)
        except ValueError as error:
            errors.append(str(error))
        if anchor["ClassificationCode"] == "PRJ_PROJECT_UNIT":
            errors.append("Organization.ClassificationCode must retain the existing parent classification code.")
        if anchor["ClassificationName"] == CLASSIFICATION:
            errors.append("Organization.ClassificationName must retain the existing LOV display label.")
        if anchor["EffectiveEndDate"]:
            errors.append("Organization.EffectiveEndDate must be blank for the existing-organization MERGE anchor.")
    try:
        text_field(rows["OrgInformation"][PROJECT_UNIT_CODE], "ProjectUnitCode", 150)
    except ValueError as error:
        errors.append(str(error))
    return errors


def validate(archive: Path, action=None):
    """Structural checks only: this does not prove tenant eligibility."""
    with zipfile.ZipFile(archive) as package:
        if package.namelist() != [MEMBER]:
            return [f"Archive must contain only {MEMBER} once at ZIP root."]
        return validate_text(package.read(MEMBER).decode("utf-8-sig"), action)


def validate_batch_text(content, action):
    """Validate a homogeneous multi-organization DAT using the single-row contract."""
    if action not in HEADERS:
        return ["Batch validation requires a supported --action."]
    sections = [section.splitlines() for section in content.rstrip("\n").split("\n\n")]
    expected = HEADERS[action]
    if len(sections) != len(expected):
        return [f"{action}: expected one section per component in documented order."]
    count = None
    for (component, headers), lines in zip(expected.items(), sections):
        if not lines or lines[0] != "|".join(["METADATA", component] + headers):
            return [f"{component}: expected the exact single metadata header in documented order."]
        if len(lines) < 2 or any(
                not line.startswith(f"MERGE|{component}|") or len(line.split("|")) != len(headers) + 2
                for line in lines[1:]):
            return [f"{component}: expected one or more complete MERGE rows after metadata."]
        if count is None:
            count = len(lines) - 1
        elif len(lines) - 1 != count:
            return [f"{component}: MERGE row count must match the other components."]
    errors = []
    names, codes = {}, {}
    for index in range(count):
        one = "\n\n".join("\n".join([section[0], section[index + 1]]) for section in sections) + "\n"
        errors.extend(f"Row {index + 1}: {error}" for error in validate_text(one, action))
        name = sections[0][index + 1].split("|")[4]
        code = sections[[*expected].index("OrgInformation")][index + 1].split("|")[-1]
        for label, value, seen in (("organization name", name, names), ("Project Unit code", code, codes)):
            if value in seen:
                errors.append(f"Rows {seen[value]} and {index + 1}: duplicate {label} in batch.")
            else:
                seen[value] = index + 1
    return errors


def validate_batch_archive(archive: Path, action):
    with zipfile.ZipFile(archive) as package:
        if package.namelist() != [MEMBER]:
            return [f"Archive must contain only {MEMBER} once at ZIP root."]
        return validate_batch_text(package.read(MEMBER).decode("utf-8-sig"), action)


def prepare_batch(request, evidence):
    """Collect every row issue; no row is eligible for export until all pass."""
    if not isinstance(request, dict) or not isinstance(evidence, dict):
        raise ValueError("Batch request and evidence must be JSON objects.")
    rows, proof = request.get("Rows"), evidence.get("Rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Batch request Rows must be a nonempty list.")
    if not isinstance(proof, list):
        raise ValueError("Batch evidence Rows must be a list aligned to request rows.")
    target = request.get("TargetEnvironment")
    if not isinstance(target, str) or not target or evidence.get("TargetEnvironment") != target:
        raise ValueError("Batch request and evidence must have the same TargetEnvironment.")
    report = {"TargetEnvironment": target, "Status": "blocked", "Rows": [], "Archives": []}
    grouped = {CREATE: [], EXISTING: []}
    names, codes = {}, {}
    for index, item in enumerate(rows, 1):
        result = {"RowNumber": index, "Status": "invalid", "Issues": []}
        report["Rows"].append(result)
        if not isinstance(item, dict):
            result["Issues"].append("Request row must be an object.")
            continue
        try:
            requested_organization_name(item)
        except ValueError as error:
            result["Issues"].append(str(error))
        try:
            required_code(item)
        except ValueError as error:
            result["Issues"].append(str(error))
            if item.get("ProjectUnitCode") is None or (
                    isinstance(item.get("ProjectUnitCode"), str)
                    and not item["ProjectUnitCode"].strip()):
                suggestion = suggested_code(item)
                if suggestion:
                    result["SuggestedProjectUnitCode"] = suggestion
        if result["Issues"]:
            continue
        if index > len(proof) or not isinstance(proof[index - 1], dict):
            result["Issues"].append("Matching resolver evidence row is required.")
            continue
        row_request, row_evidence = dict(item), dict(proof[index - 1])
        if (row_request.get("TargetEnvironment", target) != target
                or row_evidence.get("TargetEnvironment") != target):
            result["Issues"].append("Row request/evidence target must match batch TargetEnvironment.")
            continue
        row_request["TargetEnvironment"] = target
        try:
            prepared = prepare_request(row_request, row_evidence)
        except ValueError as error:
            result["Issues"].append(str(error))
            continue
        result.update(Action=prepared["Action"], Name=prepared["Name"],
                      ProjectUnitCode=prepared["ProjectUnitCode"],
                      TreePlacementDecision=prepared["TreePlacementDecision"],
                      EvidenceRef=row_evidence["EvidenceRef"])
        if prepared["Action"] == EXISTING:
            result["OrganizationId"] = row_evidence["SelectedOrganization"]["OrganizationId"]
        for label, value, seen in (("organization name", prepared["Name"], names),
                                   ("Project Unit code", prepared["ProjectUnitCode"], codes)):
            if value in seen:
                result["Issues"].append(f"Duplicate {label} with row {seen[value]}.")
                report["Rows"][seen[value] - 1]["Issues"].append(
                    f"Duplicate {label} with row {index}.")
            else:
                seen[value] = index
        grouped[prepared["Action"]].append(prepared)
    if len(proof) != len(rows):
        report["Issues"] = ["Evidence Rows count must equal request Rows count."]
    for row in report["Rows"]:
        row["Status"] = "invalid" if row["Issues"] else "valid"
    if all(row["Status"] == "valid" for row in report["Rows"]) and not report.get("Issues"):
        report["Status"] = "ready"
    return report, grouped


def batch_archives(grouped):
    """Return validated archive contents without writing partial output."""
    import io
    archives = {}
    for action, filename in ((CREATE, "ProjectUnitCreate.zip"), (EXISTING, "ProjectUnitExisting.zip")):
        rows = grouped[action]
        if not rows:
            continue
        content = render_rows(rows, action)
        errors = validate_batch_text(content, action)
        if errors:
            raise ValueError("; ".join(errors))
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as package:
            member = zipfile.ZipInfo(MEMBER, date_time=(1980, 1, 1, 0, 0, 0))
            member.compress_type = zipfile.ZIP_DEFLATED
            package.writestr(member, content)
        archives[filename] = {"Action": action, "RowCount": len(rows),
                              "Content": buffer.getvalue()}
    return archives


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", nargs="?", type=Path)
    parser.add_argument("--action", choices=list(HEADERS), help="Expected action for archive validation")
    parser.add_argument("--request", type=Path, help="JSON request for generation")
    parser.add_argument("--evidence", type=Path, help="JSON evidence from routed resolvers")
    parser.add_argument("--output", type=Path, help="New Organization.dat path; never overwrite")
    parser.add_argument("--dry-run", action="store_true", help="Validate generation without writing")
    parser.add_argument("--batch", action="store_true", help="Use Rows arrays for all-row validation and archives")
    parser.add_argument("--output-dir", type=Path, help="Existing directory for validated batch ZIPs")
    parser.add_argument("--report", type=Path, help="New JSON batch row report path; never overwrite")
    args = parser.parse_args()
    if args.batch:
        if args.archive:
            if (not args.action or args.request or args.evidence or args.output
                    or args.output_dir or args.report or args.dry_run):
                parser.error("Batch archive validation requires archive and --action only.")
        elif (not args.request or not args.evidence or args.output or args.action
              or (not args.dry_run and not args.output_dir)):
            parser.error("Batch generation requires --request, --evidence and --output-dir (or --dry-run).")
    elif args.request:
        if args.archive or args.action or not args.evidence or (not args.dry_run and not args.output):
            parser.error("Generation requires --evidence and --output (or --dry-run); omit archive/--action.")
        if args.output_dir or args.report:
            parser.error("--output-dir and --report require --batch.")
    elif not args.archive or args.evidence or args.output or args.dry_run or args.output_dir or args.report:
        parser.error("Supply an archive or --request with generation options.")
    try:
        if args.batch and args.archive:
            errors = validate_batch_archive(args.archive, args.action)
        elif args.batch:
            report, grouped = prepare_batch(
                json.loads(args.request.read_text()), json.loads(args.evidence.read_text()))
            archives = batch_archives(grouped) if report["Status"] == "ready" else {}
            if archives and not args.dry_run:
                if not args.output_dir.is_dir():
                    raise ValueError("Batch output directory must already exist.")
                paths = [args.output_dir / filename for filename in archives]
                if any(path.exists() for path in paths):
                    raise ValueError("Batch archive already exists; choose a new output directory.")
                if args.report and args.report.exists():
                    raise ValueError("Batch report already exists; choose a new report path.")
                for path, archive in zip(paths, archives.values()):
                    with path.open("xb") as output:
                        output.write(archive["Content"])
            for filename, archive in archives.items():
                report["Archives"].append({
                    "Filename": filename, "Action": archive["Action"],
                    "RowCount": archive["RowCount"],
                    "RowNumbers": [row["RowNumber"] for row in report["Rows"]
                                   if row["Action"] == archive["Action"]],
                    "SHA256": hashlib.sha256(archive["Content"]).hexdigest(),
                    "Written": not args.dry_run,
                })
            if args.report:
                with args.report.open("x", encoding="utf-8") as output:
                    json.dump(report, output, indent=2)
                    output.write("\n")
            print(json.dumps(report, indent=2))
            return 0 if report["Status"] == "ready" else 1
        elif args.request:
            content = generate_dat(json.loads(args.request.read_text()), json.loads(args.evidence.read_text()))
            errors = validate_text(content)
            if not errors and not args.dry_run:
                if args.output.name != MEMBER:
                    raise ValueError("Output filename must be Organization.dat.")
                with args.output.open("x", encoding="utf-8", newline="\n") as output:
                    output.write(content)
        else:
            errors = validate(args.archive, args.action)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
    except (ValueError, OSError, UnicodeError, zipfile.BadZipFile, RuntimeError) as error:
        print(f"Project Unit HDL input/artifact failure: {error}", file=sys.stderr)
        return 2
    print("Project Unit HDL checks passed; live lookup and Data Loader approval gates still apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
