#!/usr/bin/env python3
"""Offline PTO/PEO planning, generation and archive validation. No Fusion writes."""
from __future__ import annotations
import argparse
import json
import re
import sys
import uuid
import zipfile
from datetime import date
from pathlib import Path

MEMBER = "Organization.dat"
CODES = {"PTO": "PA_PROJECT_ORG", "PEO": "PA_EXPENDITURE_ORG"}
CONTEXT = "Project Type Class Information"
PERMISSIONS = {
    "indirect": "allowIndirectProjects",
    "capitalization": "allowProjectsEnabledForCapital",
    "billing": "allowProjectsEnabledForBilling",
}
SEGMENTS = [v + "(PER_ORGANIZATION_INFORMATION_EFF=" + CONTEXT + ")" for v in PERMISSIONS.values()]
ROOT = ["SourceSystemOwner", "SourceSystemId", "EffectiveStartDate", "EffectiveEndDate", "Name", "ClassificationCode"]
KEYS = ["SourceSystemOwner", "SourceSystemId", "EffectiveStartDate", "EffectiveEndDate"]
SOURCE_REF = "OrganizationId(SourceSystemId)"
TASK_CODE = "PJF_MANAGE_PROJECT_ORGANIZATION_CLASSIFICATIONS"


def text(value, field, limit=240):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"{field}: enter a nonblank string of at most {limit} characters.")
    if "|" in value or any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise ValueError(f"{field}: unsupported HDL character.")
    return value


def as_date(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}[-/]\d{2}[-/]\d{2}", value):
        raise ValueError("Use a valid YYYY-MM-DD or YYYY/MM/DD date.")
    return date.fromisoformat(value.replace("/", "-"))


def dates(row):
    start, end = as_date(row["EffectiveStartDate"]), as_date(row["EffectiveEndDate"])
    if start > end:
        raise ValueError("Effective end date precedes start date.")
    return start, end


def hdl_date(value):
    return as_date(value).isoformat().replace("-", "/")


def identity(value):
    if isinstance(value, bool) or not str(value).isdigit() or int(value) <= 0:
        raise ValueError("A resolved positive OrganizationId is required.")
    return str(value)


def normalize_request(request):
    allowed = {"organization_name", "requested_target_classification", "pto_permissions",
               "source_system_owner", "source_system_ids"}
    if not isinstance(request, dict) or set(request) - allowed or any(v is None for v in request.values()):
        raise ValueError("Unsupported or null single-organization input; bulk requests use the organizations envelope.")
    name = text(request.get("organization_name"), "organization_name")
    target = request.get("requested_target_classification", [])
    target = ["PTO", "PEO"] if target == "BOTH" else [target] if isinstance(target, str) else target
    if (not isinstance(target, list) or (not target and "requested_target_classification" in request)
            or any(t not in CODES for t in target) or len(set(target)) != len(target)):
        raise ValueError("Select PTO, PEO or both.")
    supplied = request.get("pto_permissions", {})
    if not isinstance(supplied, dict) or set(supplied) - set(PERMISSIONS):
        raise ValueError("Unknown PTO permission.")
    perms = {}
    for key, v in supplied.items():
        if type(v) is bool:
            perms[key] = "Y" if v else "N"
        elif isinstance(v, str) and v.strip().upper() in {"Y", "N", "ENABLE", "ENABLED", "DISABLE", "DISABLED"}:
            perms[key] = "Y" if v.strip().upper() in {"Y", "ENABLE", "ENABLED"} else "N"
        else:
            raise ValueError("PTO permissions must be Boolean or Y/N.")
    owner = request.get("source_system_owner", "")
    if not isinstance(owner, str):
        raise ValueError("Invalid source owner.")
    owner = text(owner if owner.strip() else "HRC_SQLLOADER", "source_system_owner")
    return name, [t for t in CODES if t in target], perms, owner


def resolve_classification_state(request, evidence):
    """Resolve existence from complete governed REST evidence, never from export."""
    name, targets, perms, owner = normalize_request(request)
    if not isinstance(evidence, dict):
        raise ValueError("Complete trusted REST evidence required.")
    for flag in ("Fresh", "OrganizationSearchComplete", "ClassificationsComplete"):
        if evidence.get(flag) is not True:
            raise ValueError(f"Complete trusted evidence required: {flag}.")
    text(evidence.get("TargetEnvironment"), "TargetEnvironment", 2048)
    text(evidence.get("EvidenceRef"), "EvidenceRef", 2048)
    when = as_date(evidence.get("AsOfDate"))
    matches = evidence.get("OrganizationMatches")
    if not isinstance(matches, list) or any(not isinstance(row, dict) for row in matches):
        raise ValueError("Complete organization matches required.")
    found = {}
    for row in matches:
        if row.get("Name") != name:
            raise ValueError("Search evidence does not match the exact name.")
        key = identity(row.get("OrganizationId"))
        state = (row["Name"], dates(row))
        if key in found and found[key] != state:
            raise ValueError("Conflicting effective records require reconciliation.")
        found[key] = state
    if not found:
        raise ValueError(f'Organization "{name}" was not found. Select an existing organization.')
    selected = evidence.get("SelectedOrganization", {})
    if not isinstance(selected, dict):
        raise ValueError("Selected organization identity is incomplete.")
    oid = identity(selected.get("OrganizationId"))
    if len(found) > 1 and evidence.get("SelectionConfirmed") is not True:
        raise ValueError(f'More than one organization is named "{name}". Select the organization to classify.')
    if oid not in found or (selected.get("Name"), dates(selected)) != found[oid]:
        raise ValueError("Selected identity differs from search evidence.")
    start, end = dates(selected)
    if not start <= when <= end:
        raise ValueError("The selected organization is not effective on the requested date.")
    classes = evidence.get("Classifications")
    if not isinstance(classes, list) or any(not isinstance(row, dict) for row in classes):
        raise ValueError("Complete classification list required.")
    for row in classes:
        if identity(row.get("OrganizationId")) != oid:
            raise ValueError("Child evidence belongs to a different organization.")
        dates(row)
    for row in classes:
        text(row.get("ClassificationCode"), "ClassificationCode")
        if row.get("Status") not in {"A", "I"}:
            raise ValueError("Classification status is unresolved.")
    if not any(row["Status"] == "A" and dates(row)[0] <= when <= dates(row)[1] for row in classes):
        raise ValueError("Verify an active existing prior classification for the effective organization.")
    existing_targets = {}
    for target, code in CODES.items():
        rows = [row for row in classes if row["ClassificationCode"] == code]
        if rows and (len(rows) != 1 or rows[0]["Status"] != "A"
                     or dates(rows[0]) != (start, end)):
            raise ValueError(f'The existing {target} setup for "{name}" needs review before we can continue.')
        existing_targets[target] = rows
    return {"name": name, "targets": targets, "supplied_permissions": perms, "owner": owner,
            "organization_id": oid, "start": start, "end": end, "when": when,
            "selected": selected, "classifications": classes, "existing_targets": existing_targets}


def requires_existing_pto_update_identity(request, evidence):
    """Only explicit existing PTO updates need original HDL identity; no export call."""
    state = resolve_classification_state(request, evidence)
    return bool(state["existing_targets"]["PTO"] and state["supplied_permissions"])


def resolve_existing_pto_update_identity(request, evidence):
    """Resolve already registered original keys, without export calls or flag reads."""
    state = resolve_classification_state(request, evidence)
    if not state["existing_targets"]["PTO"] or not state["supplied_permissions"]:
        return None
    exported = classification_export(evidence, verify_permissions=False)
    rows = [row for row in exported["Rows"] if row.get("Name") == state["name"]
            and row.get("ClassificationCode") == CODES["PTO"]]
    if len(rows) > 1:
        raise ValueError("Classification export contains more than one matching PTO record; reconcile the ambiguous baseline.")
    if not rows:
        raise ValueError("REST proves an existing PTO but its update identity receipt has no exact PTO record; stop without creating a duplicate classification.")
    if identity(rows[0].get("OrganizationId")) != state["organization_id"]:
        raise ValueError("Classification export PTO identity differs from the selected organization.")
    info = existing_pto_information(evidence, rows[0], state["organization_id"], state["start"], state["end"])
    require_existing_source_key(info)
    return {"identity": info, "EvidenceRef": exported["EvidenceRef"]}


def plan_request(request, evidence):
    if isinstance(request, dict) and "organizations" in request:
        from bulk_project_organization_classifications import plan_bulk_request
        return plan_bulk_request(request, evidence)
    state = resolve_classification_state(request, evidence)
    name, targets, perms, owner = (state[key] for key in
                                  ("name", "targets", "supplied_permissions", "owner"))
    oid, start, end, when, selected, classes = (state[key] for key in
        ("organization_id", "start", "end", "when", "selected", "classifications"))
    missing, already = [], []
    # Explicit permission intent selects PTO, but REST alone decides whether it exists.
    checked_targets = targets + (["PTO"] if perms and "PTO" not in targets else [])
    for target in checked_targets:
        existing = state["existing_targets"][target]
        if not existing:
            missing.append(target)
            continue
        already.append(target)
    changes, existing_info, update_identity = {}, None, None
    if "PTO" in missing:
        # New PTO values are request-owned; omission defaults N, never export values.
        perms = {key: perms.get(key, "N") for key in PERMISSIONS}
    elif perms:
        # Consume already available authoritative keys only. No existing permission
        # values are read or compared, and the planner never initiates an export.
        update_identity = resolve_existing_pto_update_identity(request, evidence)
        existing_info = update_identity["identity"]
        changes = dict(perms)
        require_existing_source_key(existing_info)
        if request.get("source_system_owner", "").strip() and owner != existing_info["SourceSystemOwner"]:
            raise ValueError("A PTO update must preserve the existing information row's source owner.")
        owner = existing_info["SourceSystemOwner"]
    # resolve_classification_state already requires an active, effective prior
    # classification. An existing PTO or PEO satisfies that requirement; adding
    # the other role must not require an unrelated third classification.
    ids = request.get("source_system_ids", {})
    components = missing + (["PTO_INFO"] if "PTO" in missing else [])
    if not isinstance(ids, dict) or set(ids) - set(components):
        raise ValueError("Source IDs may identify only new components.")
    for value in ids.values():
        text(value, "source_system_ids")
    return {"status": "ADD_MISSING" if missing else "UPDATE_PERMISSIONS" if changes else "ALREADY_CONFIGURED", "name": name,
            "organization_id": oid, "missing": missing, "already": already, "components": components,
            "permissions": perms, "permission_changes": changes,
            "existing_pto_information": existing_info,
            "classification_export_ref": update_identity["EvidenceRef"] if update_identity else None,
            "classification_baseline_ref": evidence["EvidenceRef"],
            "validation_run_id": evidence.get("ValidationRunId"),
            "baseline_collected_at": evidence.get("CollectedAt"),
            "baseline_as_of_date": evidence["AsOfDate"],
            "export_required": False,
            "update_identity_required": bool(state["existing_targets"]["PTO"] and state["supplied_permissions"]),
            "permission_scope": "explicit_changes_only" if changes else "new_pto_only" if "PTO" in missing else "preserve_existing",
            "existing_pto_permissions_verified": False,
            "owner": owner, "target": evidence["TargetEnvironment"],
            "start": hdl_date(selected["EffectiveStartDate"]), "end": hdl_date(selected["EffectiveEndDate"])}


def classification_export(evidence, verify_permissions=True):
    """Accept only the governed, complete task-data export projection for this run."""
    receipt = evidence.get("ClassificationsExport")
    if (not isinstance(receipt, dict) or receipt.get("Status") != "SUCCESS"
            or receipt.get("Complete") is not True or receipt.get("Fresh") is not True
            or receipt.get("Mode") != "data" or receipt.get("Scope") != "task"
            or receipt.get("TaskCode") != TASK_CODE or not receipt.get("ProcessId")
            or receipt.get("TargetEnvironment") != evidence.get("TargetEnvironment")
            or receipt.get("AsOfDate") != evidence.get("AsOfDate")
            or not evidence.get("ExportRunId") or receipt.get("RunId") != evidence["ExportRunId"]
            or not receipt.get("EvidenceRef") or not receipt.get("MetadataEvidenceRef")
            or not isinstance(receipt.get("ArtifactSha256"), str)
            or not re.fullmatch(r"[0-9a-f]{64}", receipt["ArtifactSha256"])
            or not isinstance(receipt.get("Rows"), list)
            or any(not isinstance(row, dict) for row in receipt["Rows"])):
        raise ValueError("Fresh complete readable task-data classification export is required; do not infer new PTO setup.")
    for row in receipt["Rows"]:
        try:
            text(row.get("Name"), "Export organization name")
            identity(row.get("OrganizationId"))
            text(row.get("ClassificationCode"), "Export classification")
            dates(row)
            if row.get("Status") not in {"A", "I"}:
                raise ValueError("Unresolved status")
            if verify_permissions and row["ClassificationCode"] == CODES["PTO"]:
                values = row.get("Permissions")
                if (not isinstance(values, dict) or set(values) != set(PERMISSIONS)
                        or any(v not in {"Y", "N"} for v in values.values())):
                    raise ValueError("Unresolved PTO permissions")
        except (KeyError, ValueError, TypeError) as exc:
            raise ValueError("Classification export contains incomplete or invalid classification data; stop before artifacts.") from exc
    return receipt


def existing_pto_information(evidence, exported, oid, start, end):
    """Read only original information-row identity from already registered export."""
    if dates(exported) != (start, end) or exported.get("Status") != "A":
        raise ValueError("The existing PTO export record needs review before we can continue.")
    identity_fields = {"OrganizationId", "Name", "ClassificationCode", "Status",
                       "EffectiveStartDate", "EffectiveEndDate", "SourceKeyBinding"}
    row = {key: value for key, value in exported.items() if key in identity_fields}
    row.update({"Fresh": True, "TargetEnvironment": evidence["TargetEnvironment"],
                "EvidenceRef": evidence["ClassificationsExport"]["EvidenceRef"]})
    binding = exported.get("SourceKeyBinding", {})
    verified = (isinstance(binding, dict) and binding.get("Component") == "OrgInformation"
                and binding.get("OrgInformationContext") == CONTEXT
                and type(binding.get("SequenceNumber")) is int and binding["SequenceNumber"] == 1)
    row["SourceKeyVerified"] = verified
    if verified:
        row.update({key: binding.get(key) for key in ("SourceSystemOwner", "SourceSystemId",
                                                    "OrgInformationContext", "SequenceNumber")})
    return row


def require_existing_source_key(row):
    if row.get("SourceKeyVerified") is not True or not all(
            isinstance(row.get(key), str) and row[key].strip()
            for key in ("SourceSystemOwner", "SourceSystemId")):
        raise ValueError("REST proves existing PTO state but the registered identity evidence lacks the original OrgInformation source-key binding required for the supported HCM Data Loader update. No key or update artifact was fabricated.")
    for key in ("SourceSystemOwner", "SourceSystemId"):
        text(row[key], key)


def headers(reference):
    return {
        "Organization": ROOT,
        "OrgUnitClassification": KEYS + [reference, "ClassificationCode", "CategoryCode", "Status"],
        "OrgInformation": KEYS + [reference, "ClassificationCode", "SequenceNumber",
            "FLEX:PER_ORGANIZATION_INFORMATION_EFF", "EFF_CATEGORY_CODE", "OrgInformationContext"] + SEGMENTS,
    }


def build_schema_evidence(schema, reference):
    sys.path.insert(0, str(Path(__file__).resolve().parents[6] / "core/data-loader/scripts"))
    from data_loader_metadata import is_supported_source_attribute
    if schema.discriminator != "Organization" or reference not in {SOURCE_REF, "OrganizationId"}:
        raise ValueError("Organization schema and supported reference required.")
    result = headers(reference)
    limits = {key: [] for key in ("SourceSystemOwner", "SourceSystemId")}
    for component, attrs in result.items():
        if not all(is_supported_source_attribute(component, attr, schema) for attr in attrs):
            raise ValueError(f"{component}: unsupported target headers.")
        if component == "Organization":
            continue
        metadata = {a["AttributeName"]: a for a in schema.attributes.get(component, [])}
        for key in limits:
            n = metadata.get(key, {}).get("DataLength")
            if isinstance(n, bool) or not str(n).isdigit() or int(n) <= 0:
                raise ValueError(f"{component}.{key}: missing target key length.")
            limits[key].append(int(n))
    return {"Validated": True, "Headers": result, "KeyLengths": {k: min(v) for k, v in limits.items()}}


def allocate_source_ids(components):
    if not set(components).issubset({"PTO", "PEO", "PTO_INFO"}):
        raise ValueError("Unsupported component.")
    return {c: uuid.uuid4().hex + "_" + c for c in components}


def mapping_binding(plan):
    return {k: plan[k] for k in ("target", "organization_id", "name", "owner", "missing", "permissions", "permission_changes", "classification_baseline_ref", "classification_export_ref", "validation_run_id", "baseline_collected_at", "baseline_as_of_date", "start", "end")}


def generate_dat(request, evidence):
    if isinstance(request, dict) and "organizations" in request:
        raise ValueError("Use generate_bulk_dats for a bulk request's separate PEO/PTO payloads.")
    plan = plan_request(request, evidence)
    if not plan["missing"] and not plan["permission_changes"]:
        return ""
    owner = evidence.get("SourceOwner", {})
    if (owner.get("LookupType") != "HRC_SOURCE_SYSTEM_OWNER" or owner.get("LookupCode") != plan["owner"]
            or owner.get("Status") != "found" or owner.get("EnabledFlag") != "Y"):
        raise ValueError("Source owner must be found, enabled and verified before generation.")
    when = as_date(evidence.get("LookupAsOfDate"))
    if ((owner.get("StartDateActive") and as_date(owner["StartDateActive"]) > when)
            or (owner.get("EndDateActive") and as_date(owner["EndDateActive"]) < when)):
        raise ValueError("Source owner is not effective.")
    reference = evidence.get("ParentReference", {})
    mode, parent = reference.get("Attribute"), reference.get("Value")
    if reference.get("Verified") is not True or identity(reference.get("OrganizationId")) != plan["organization_id"]:
        raise ValueError("Verified parent reference required.")
    if mode != "OrganizationId" or identity(parent) != plan["organization_id"]:
        raise ValueError("Use the resolved existing OrganizationId as the parent reference.")
    schema = evidence.get("HdlSchema", {})
    expected = headers(mode)
    if schema.get("Validated") is not True or schema.get("Headers") != expected:
        raise ValueError("Core-derived target schema evidence required.")
    mapping = evidence.get("SourceKeyMapping", {}) if plan["missing"] else {}
    ids = mapping.get("SourceSystemIds", {})
    if plan["missing"] and (mapping.get("Persisted") is not True or not mapping.get("MappingRef")
            or mapping.get("Binding") != mapping_binding(plan) or set(ids) != set(plan["components"])):
        raise ValueError("Persist matching component source keys before generation.")
    for key, value in request.get("source_system_ids", {}).items():
        if ids.get(key) != value:
            raise ValueError("Legacy source ID differs from persisted mapping.")
    for key in ("SourceSystemOwner", "SourceSystemId"):
        n = schema.get("KeyLengths", {}).get(key)
        if type(n) is not int or n <= 0:
            raise ValueError("Target key lengths required.")
        for value in ([plan["owner"]] if key == "SourceSystemOwner" else list(ids.values())):
            text(value, key, n)
    if len(set(ids.values())) != len(ids) or (mode == SOURCE_REF and parent in ids.values()):
        raise ValueError("Created component keys must be distinct from each other and the parent.")
    ledger = evidence.get("PersistedMappings") if plan["missing"] else None
    if plan["missing"] and (evidence.get("PersistedMappingsComplete") is not True or not isinstance(ledger, list) or mapping not in ledger):
        raise ValueError("Complete persisted mapping ledger required.")
    for record in ledger or []:
        if not isinstance(record, dict) or not isinstance(record.get("Binding"), dict) or not isinstance(record.get("SourceSystemIds"), dict):
            raise ValueError("Invalid mapping ledger record.")
        binding = record["Binding"]
        ledger_target = binding.get("target", binding.get("TargetEnvironment"))
        ledger_owner = binding.get("owner", binding.get("SourceSystemOwner"))
        if not ledger_target or not ledger_owner:
            raise ValueError("Mapping ledger record lacks target/owner scope.")
        if ledger_target == plan["target"] and ledger_owner == plan["owner"]:
            for component, value in ids.items():
                if value in record["SourceSystemIds"].values() and (
                        binding != mapping["Binding"] or record["SourceSystemIds"].get(component) != value):
                    raise ValueError("Source key conflicts with a persisted component binding.")
    lines = ["|".join(["METADATA", "Organization"] + ROOT)]
    if plan["missing"]:
        lines.append("|".join(["METADATA", "OrgUnitClassification"] + expected["OrgUnitClassification"]))
    common = [plan["owner"], None, plan["start"], plan["end"], str(parent)]
    for target in plan["missing"]:
        row = [*common]
        row[1] = ids[target]
        lines.append("|".join(["MERGE", "OrgUnitClassification"] + row + [
            CODES[target], "PA_PROJECT_ORG" if target == "PTO" else "NO_EFF_CATEGORY", "A"]))
    if "PTO" in plan["missing"]:
        lines.append("|".join(["METADATA", "OrgInformation"] + expected["OrgInformation"]))
        row = [*common]
        row[1] = ids["PTO_INFO"]
        lines.append("|".join(["MERGE", "OrgInformation"] + row + [
            "PA_PROJECT_ORG", "1", CONTEXT, "PA_PROJECT_ORG", CONTEXT] + list(plan["permissions"].values())))
    elif plan["permission_changes"]:
        current = plan["existing_pto_information"]
        update_headers = expected["OrgInformation"][:-len(SEGMENTS)] + [
            segment for key, segment in zip(PERMISSIONS, SEGMENTS) if key in plan["permission_changes"]]
        limits = schema["KeyLengths"]
        text(current["SourceSystemId"], "existing PTO source key", limits["SourceSystemId"])
        if current["SourceSystemId"] in ids.values():
            raise ValueError("A new component key cannot replace the existing PTO information key.")
        lines.append("|".join(["METADATA", "OrgInformation"] + update_headers))
        lines.append("|".join(["MERGE", "OrgInformation", current["SourceSystemOwner"],
            current["SourceSystemId"], plan["start"], plan["end"], str(parent),
            "PA_PROJECT_ORG", "1", CONTEXT, "PA_PROJECT_ORG", CONTEXT] + [
                plan["permission_changes"][key] for key in PERMISSIONS if key in plan["permission_changes"]]))
    return "\n".join(lines) + "\n"


def validate_text(content, bulk_role=None):
    if bulk_role:
        from bulk_project_organization_classifications import validate_bulk_text
        return validate_bulk_text(content, bulk_role)
    metadata, rows, errors = {}, {}, []
    for number, line in enumerate(content.splitlines(), 1):
        if not line.strip():
            continue
        fields = line.split("|")
        if len(fields) < 2 or fields[0] not in {"METADATA", "MERGE"} or fields[1] not in headers(SOURCE_REF):
            errors.append(f"Line {number}: unexpected instruction/component.")
            continue
        op, component, values = fields[0], fields[1], fields[2:]
        if op == "METADATA":
            if component in metadata:
                errors.append(f"Duplicate {component} metadata.")
            metadata[component] = values
        elif component not in metadata or len(values) != len(metadata[component]):
            errors.append(f"Line {number}: row/header mismatch.")
        else:
            rows.setdefault(component, []).append(dict(zip(metadata[component], values)))
    if errors:
        return errors
    classes, infos = rows.get("OrgUnitClassification", []), rows.get("OrgInformation", [])
    if rows.get("Organization"):
        errors.append("Existing organization must have no parent MERGE.")
    reference = SOURCE_REF if SOURCE_REF in metadata.get("OrgUnitClassification", []) else "OrganizationId"
    expected = headers(reference)
    codes = [r.get("ClassificationCode") for r in classes]
    update = bool(infos) and "PA_PROJECT_ORG" not in codes
    wanted = {"Organization"} | ({"OrgUnitClassification"} if classes else set()) | ({"OrgInformation"} if infos else set())
    if set(metadata) != wanted or any(metadata.get(c) != expected[c] for c in wanted if not (update and c == "OrgInformation")):
        errors.append("Headers must match the selected classification contract.")
        return errors
    if update:
        header = metadata["OrgInformation"]
        prefix = expected["OrgInformation"][:-len(SEGMENTS)]
        selected_segments = [s for s in SEGMENTS if s in header]
        if not selected_segments or header != prefix + selected_segments:
            return ["Existing PTO updates require exact identity fields and only supplied permission segments."]
    if (not codes and not update) or len(codes) != len(set(codes)) or not set(codes).issubset(CODES.values()):
        errors.append("Single-request validation requires one row per missing classification; use --bulk-role for a bulk archive.")
    if len(infos) != (1 if "PA_PROJECT_ORG" in codes or update else 0):
        errors.append("PTO requires exactly one information row in the same file.")
    identities, keys = set(), set()
    for row in classes + infos:
        try:
            for k, v in row.items():
                text(v, k, 2048)
            dates(row)
            if reference == "OrganizationId":
                identity(row[reference])
            identities.add((row["SourceSystemOwner"], row[reference], row["EffectiveStartDate"], row["EffectiveEndDate"]))
            key = row["SourceSystemId"]
            if key in keys or (reference == SOURCE_REF and key == row[reference]):
                errors.append("Duplicate source key or parent key reused.")
            keys.add(key)
        except (KeyError, ValueError) as exc:
            errors.append(str(exc))
    if len(identities) != 1:
        errors.append("All child rows must reference one parent, owner and date range.")
    for row in classes:
        category = "PA_PROJECT_ORG" if row["ClassificationCode"] == "PA_PROJECT_ORG" else "NO_EFF_CATEGORY"
        if row["CategoryCode"] != category or row["Status"] != "A":
            errors.append("Invalid classification category or status.")
    for row in infos:
        fixed = {"ClassificationCode": "PA_PROJECT_ORG", "SequenceNumber": "1",
                 "FLEX:PER_ORGANIZATION_INFORMATION_EFF": CONTEXT,
                 "EFF_CATEGORY_CODE": "PA_PROJECT_ORG", "OrgInformationContext": CONTEXT}
        if any(row.get(k) != v for k, v in fixed.items()):
            errors.append("Invalid PTO flexfield constants.")
        values = [row[k] for k in SEGMENTS if k in row]
        if any(v not in {"Y", "N"} for v in values):
            errors.append("PTO permissions need Y/N.")
    return errors


def validate(archive, bulk_role=None):
    with zipfile.ZipFile(archive) as package:
        if package.namelist() != [MEMBER]:
            return ["Archive must contain only Organization.dat at ZIP root."]
        return validate_text(package.read(MEMBER).decode("utf-8-sig"), bulk_role=bulk_role)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", nargs="?", type=Path)
    parser.add_argument("--request", type=Path)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--output-dir", type=Path, help="Bulk ZIP destination under selected project artifacts.")
    parser.add_argument("--project-root", type=Path, help="Existing selected project root for bulk output.")
    parser.add_argument("--bulk-role", choices=("PEO", "PTO"), help="Validate a multi-parent role ZIP.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        if args.archive:
            if args.request or args.evidence or args.output or args.output_dir or args.project_root or args.dry_run:
                raise ValueError("Choose archive validation or request generation.")
            errors = validate(args.archive, bulk_role=args.bulk_role)
            if errors:
                raise ValueError("\n".join(errors))
            print("Project Organization Classifications HDL structure validated.")
        else:
            if not args.request or not args.evidence or not (args.dry_run or args.output or args.output_dir):
                raise ValueError("Provide request, evidence and --dry-run or --output.")
            request, evidence = json.loads(args.request.read_text()), json.loads(args.evidence.read_text())
            if isinstance(request, dict) and "organizations" in request:
                from bulk_project_organization_classifications import generate_bulk_dats, write_bulk_archives
                if args.output or args.bulk_role or (not args.dry_run and (not args.output_dir or not args.project_root)):
                    raise ValueError("Bulk generation uses --output-dir and --project-root, or --dry-run.")
                plan, outputs = generate_bulk_dats(request, evidence)
                if not args.dry_run:
                    plan["archives"] = write_bulk_archives(outputs, plan, args.output_dir, args.project_root)
                else:
                    plan["archive_roles"] = list(outputs)
                print(json.dumps(plan, indent=2))
                return 0
            if args.output_dir or args.project_root or args.bulk_role:
                raise ValueError("Bulk output options require an organizations array.")
            plan = plan_request(request, evidence)
            content = generate_dat(request, evidence)
            if content:
                errors = validate_text(content)
                if errors:
                    raise ValueError("\n".join(errors))
                if not args.dry_run:
                    with args.output.open("x") as stream:
                        stream.write(content)
            print(json.dumps(plan, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError, UnicodeDecodeError, zipfile.BadZipFile) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
