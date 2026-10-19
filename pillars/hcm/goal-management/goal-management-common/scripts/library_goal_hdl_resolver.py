#!/usr/bin/env python3
"""Resolve Library Goal HDL context from canonical requirements and Core read evidence.

No upload, initiation, REST mutation, Run Book update, or implicit live call.
The owning task supplies its allowed control before requesting live reads.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

from hdl_dat_validator import HdlDatValidationError, require_reference, validate_source_owner
from library_goal_hdl_search_adapter import replay_pages, normalize_page
from library_goal_hdl_fields import load_crosswalk, resolve_rows
from library_goal_search_contract import build_search_payload
from duplicate_identity import assess_duplicates, validate_incoming

ROOT = Path(__file__).resolve().parents[5]
CATALOG_DIR = Path(__file__).resolve().parents[1] / "hdl-mappings"
HDL_ROUTES = {"hdl_generate", "hdl_dat_preflight"}
PROFILES = {"performance_library_goal": "PERFORMANCE", "development_library_goal": "DEVELOPMENT"}


def _fresh_item_path(candidate, host):
    """Return only a same-host item link supplied by the search result."""
    if not isinstance(candidate, dict) or not isinstance(candidate.get("links"), list):
        raise HdlDatValidationError("SEARCH_HYDRATION_INVALID: matching candidate has no fresh item link.")
    expected = urlparse(host)
    for link in candidate["links"]:
        if not isinstance(link, dict) or link.get("rel") not in {"self", "canonical"} or not isinstance(link.get("href"), str):
            continue
        parsed = urlparse(link["href"])
        if (parsed.scheme, parsed.netloc) != (expected.scheme, expected.netloc) or not parsed.path.startswith("/hcmRestApi/"):
            continue
        query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        query["fields"] = "*"
        return urlunparse(("", "", parsed.path, "", urlencode(query), ""))
    raise HdlDatValidationError("SEARCH_HYDRATION_INVALID: matching candidate has no valid same-host item link.")


def _schema_check(value, schema, path="catalog"):
    """Validate the schema subset used by this dependency-free, local catalog."""
    types = {"object": dict, "array": list, "string": str, "boolean": bool}
    if "type" in schema and type(value) is not types[schema["type"]]:
        raise HdlDatValidationError(f"CATALOG_INVALID: {path} has the wrong type.")
    if "const" in schema and value != schema["const"]:
        raise HdlDatValidationError(f"CATALOG_INVALID: {path} violates its fixed contract.")
    if "enum" in schema and value not in schema["enum"]:
        raise HdlDatValidationError(f"CATALOG_INVALID: {path} has an unsupported value.")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or ("pattern" in schema and not re.search(schema["pattern"], value)):
            raise HdlDatValidationError(f"CATALOG_INVALID: {path} is invalid.")
    if isinstance(value, dict):
        if set(schema.get("required", [])) - set(value) or len(value) < schema.get("minProperties", 0):
            raise HdlDatValidationError(f"CATALOG_INVALID: {path} is incomplete.")
        for key, item in value.items():
            rule = schema.get("properties", {}).get(key, schema.get("additionalProperties", {}))
            if rule is False:
                raise HdlDatValidationError(f"CATALOG_INVALID: unknown property {path}.{key}.")
            if isinstance(rule, dict):
                _schema_check(item, rule, f"{path}.{key}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0) or (schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value)):
            raise HdlDatValidationError(f"CATALOG_INVALID: invalid list {path}.")
        for item in value:
            _schema_check(item, schema.get("items", {}), path + "[]")


def load_catalog():
    catalog = json.loads((CATALOG_DIR / "library-goal.json").read_text())
    validate_catalog(catalog)
    return catalog


def validate_catalog(catalog):
    _schema_check(catalog, json.loads((CATALOG_DIR / "library-goal.schema.json").read_text()))
    fields = catalog["fields"]
    if len({v["field"] for v in fields.values()}) != len(fields):
        raise HdlDatValidationError("CATALOG_INVALID: duplicate HDL attribute mappings.")
    for spec in fields.values():
        if spec["source"] not in catalog["sources"] or ("default" in spec and spec["default"] not in spec.get("codes", [spec["default"]])):
            raise HdlDatValidationError("CATALOG_INVALID: missing provenance or invalid default.")
    if any(fields[k].get("required") is not True for k in ("GoalName", "TypeCode", "StatusCode", "Visible")):
        raise HdlDatValidationError("CATALOG_INVALID: core semantic fields must remain required.")
    if fields["StatusCode"].get("default") != "I" or fields["Visible"].get("default") != "ALL":
        raise HdlDatValidationError("CATALOG_INVALID: unsupported create defaults.")


def guard_route(request):
    if request.get("route") not in HDL_ROUTES or request.get("profile") not in PROFILES:
        raise HdlDatValidationError("HDL_ROUTE_REQUIRED: this resolver is Library Goal HDL only.")
    if not isinstance(request.get("environment"), str) or not request["environment"].strip():
        raise HdlDatValidationError("ENVIRONMENT_REQUIRED: use the configured environment.")


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def resolve_context(request, evidence, *, catalog=None, policy=None):
    """Pure resolution from full metadata and actual read timestamps, never samples."""
    guard_route(request)
    catalog = load_catalog() if catalog is None else deepcopy(catalog)
    validate_catalog(catalog)
    policy = json.loads((CATALOG_DIR / "source-system-policy.json").read_text()) if policy is None else deepcopy(policy)
    if (policy.get("routes") != ["hdl_generate", "hdl_dat_preflight"] or
        policy.get("lookupType") != "HRC_SOURCE_SYSTEM_OWNER" or
        policy.get("selectFirstEnabledOwner") is not False or policy.get("createMissingOwner") is not False or
        policy.get("precedence") != ["suppliedSourceSystemOwner", "environmentOwner"] or
        not isinstance(policy.get("version"), str) or not isinstance(policy.get("environmentOwners"), dict)):
        raise HdlDatValidationError("OWNER_POLICY_INVALID: unsupported selection policy.")
    rows = request.get("rows")
    if not isinstance(rows, list) or not rows or any(not isinstance(r, dict) for r in rows):
        raise HdlDatValidationError("BUSINESS_ROWS_REQUIRED: provide canonical Library Goal rows.")
    if request.get("operation", "create") != "create":
        raise HdlDatValidationError("CREATE_RESOLVER_ONLY: updates retain the existing fresh-row preflight contract.")
    now = datetime.now(timezone.utc).isoformat()
    context = {"environment": request["environment"], "generatedAt": now,
               "verifiedAt": evidence.get("verifiedAt"), "evidenceSources": {"read": evidence}}
    require_reference(context, "read")
    if evidence.get("schemaSource") != "UCM_TEMPLATE" or not isinstance(evidence.get("templateAttributes"), list):
        raise HdlDatValidationError("FULL_TEMPLATE_REQUIRED: a reduced DAT sample is not metadata.")
    attrs = evidence.get("attributes")
    if not isinstance(attrs, list) or any(not isinstance(a, dict) or not a.get("AttributeName") for a in attrs):
        raise HdlDatValidationError("HDL_METADATA_INVALID: full component attributes are required.")
    if len({a["AttributeName"] for a in attrs}) != len(attrs):
        raise HdlDatValidationError("HDL_METADATA_INVALID: duplicate attribute definitions.")
    attrs = {a["AttributeName"]: a for a in attrs}
    template = set(evidence["templateAttributes"])
    rows, additional_fields = resolve_rows(rows, catalog, attrs, template)
    needed = {"Name", "ContextName", "DateFrom", "SourceSystemOwner", "SourceSystemId"}
    fields = deepcopy(catalog["fields"])
    fields.update(additional_fields)
    # The versioned catalog carries the LibraryGoalCommonPVO entity mapping.
    # Generic HDL labels do not erase that source evidence. Explicit live
    # semantics must agree whenever the catalog's physical field is present.
    catalog_priority = fields["PriorityCode"]["field"]
    priority = [a["AttributeName"] for a in attrs.values()
                if a["AttributeName"] in template and
                (a["AttributeName"] == "PriorityCode" or
                 str(a.get("AttributeLabel", "")).strip().casefold() in {"priority", "priority code"})]
    proof = evidence.get("priorityMapping")
    if proof is not None:
        require_reference({**context, "evidenceSources": {**context["evidenceSources"], "priority-mapping": proof}}, "priority-mapping")
        if proof.get("ContextName") != "GOAL" or proof.get("semantic") != "PriorityCode":
            raise HdlDatValidationError("PRIORITY_MAPPING_INVALID: require GOAL PriorityCode evidence.")
        if priority and set(priority) != {proof.get("field")}:
            raise HdlDatValidationError("PRIORITY_MAPPING_INVALID: context evidence conflicts with template labels.")
        priority = [proof.get("field")]
    if catalog_priority in template and catalog_priority in attrs:
        if priority and set(priority) != {catalog_priority}:
            raise HdlDatValidationError("PRIORITY_MAPPING_INVALID: target evidence conflicts with source-backed catalog.")
        priority = [catalog_priority]
    if len(priority) != 1 or priority[0] not in template or priority[0] not in attrs:
        raise HdlDatValidationError("PRIORITY_MAPPING_REQUIRED: resolve one GOAL priority attribute from the full target template/context.")
    fields["PriorityCode"]["field"] = priority[0]
    priority_lookup = evidence.get("priorityLookup")
    if not isinstance(priority_lookup, dict) or priority_lookup.get("LookupType") != "HRG_PRIORITY":
        raise HdlDatValidationError("PRIORITY_LOOKUP_REQUIRED: current HRG_PRIORITY lookup evidence is required.")
    today = date.today().isoformat()
    priority_codes = [r["LookupCode"] for r in priority_lookup.get("lookupCodes", [])
                      if isinstance(r, dict) and r.get("LookupCode") and r.get("EnabledFlag") in (True, "Y")
                      and (not r.get("StartDateActive") or r["StartDateActive"][:10] <= today)
                      and (not r.get("EndDateActive") or r["EndDateActive"][:10] >= today)]
    if priority_codes.count("MEDIUM") != 1 or len(priority_codes) != len(set(priority_codes)):
        raise HdlDatValidationError("PRIORITY_LOOKUP_INVALID: require one enabled effective MEDIUM code.")
    fields["PriorityCode"]["codes"] = priority_codes
    if len({v["field"] for v in fields.values()}) != len(fields):
        raise HdlDatValidationError("PRIORITY_MAPPING_INVALID: field overlaps another semantic mapping.")
    semantic_names = {k for row in rows for k in row} - {"SourceSystemOwner", "SourceSystemId", "DateFrom"}
    unknown = semantic_names - fields.keys()
    if unknown:
        raise HdlDatValidationError("MAPPING_UNSUPPORTED: " + ", ".join(sorted(unknown)))
    selected = [k for k, v in fields.items() if k in semantic_names or v.get("required")]
    needed.update(fields[k]["field"] for k in selected)
    if needed - template or needed - attrs.keys():
        raise HdlDatValidationError("CATALOG_METADATA_MISMATCH: missing " + ", ".join(sorted((needed - template) | (needed - attrs.keys()))))
    metadata = {}
    for field in needed:
        attr = attrs[field]
        if attr.get("readOnly") is True or attr.get("createable") is False or attr.get("serverGenerated") is True:
            raise HdlDatValidationError(f"CATALOG_METADATA_MISMATCH: {field} does not accept create input.")
        metadata[field] = {"operations": ["create"], "type": "date" if field == "DateFrom" else "string"}
        if attr.get("DataLength"):
            try:
                length = int(attr["DataLength"])
                if length < 1 or isinstance(attr["DataLength"], bool):
                    raise ValueError("invalid length")
            except (TypeError, ValueError) as exc:
                raise HdlDatValidationError(f"HDL_METADATA_INVALID: length for {field}.") from exc
            metadata[field]["maxLength"] = length
    mapping = {k: fields[k]["field"] for k in selected}
    for semantic, field in mapping.items():
        spec, attr = fields[semantic], attrs[field]
        metadata[field]["type"] = spec["type"]
        actual_type = str(attr.get("DataType", "")).lower()
        if actual_type and actual_type != {"integer": "number", "decimal": "number", "date": "date", "string": "string"}[spec["type"]]:
            raise HdlDatValidationError(f"CATALOG_METADATA_MISMATCH: datatype for {field}.")
        if spec.get("codes"):
            live_codes = attr.get("allowedValues")
            if live_codes is not None and (not isinstance(live_codes, list) or not set(spec["codes"]) <= set(live_codes)):
                raise HdlDatValidationError(f"CATALOG_METADATA_MISMATCH: codes for {field}.")
            metadata[field]["allowedValues"] = spec["codes"]
        elif attr.get("allowedValues") is not None:
            live_codes = attr["allowedValues"]
            if not isinstance(live_codes, list) or not all(isinstance(code, str) and code for code in live_codes):
                raise HdlDatValidationError(f"HDL_METADATA_INVALID: allowed values for {field}.")
            metadata[field]["allowedValues"] = live_codes
    lookup = evidence.get("sourceOwners")
    if not isinstance(lookup, dict) or lookup.get("LookupType") != "HRC_SOURCE_SYSTEM_OWNER" or not isinstance(lookup.get("lookupCodes"), list):
        raise HdlDatValidationError("OWNER_LOOKUP_INVALID: complete HRC_SOURCE_SYSTEM_OWNER evidence required.")
    base = {k: evidence[k] for k in ("environment", "verifiedAt", "source")}
    owners = {**base, "lookupType": "HRC_SOURCE_SYSTEM_OWNER", "items": lookup["lookupCodes"]}
    context["evidenceSources"]["HRC_SOURCE_SYSTEM_OWNER"] = owners
    enabled = []
    for item in owners["items"]:
        if not isinstance(item, dict) or not item.get("LookupCode"):
            raise HdlDatValidationError("OWNER_LOOKUP_INVALID: malformed code.")
        try:
            validate_source_owner(context, item["LookupCode"])
            enabled.append(item["LookupCode"])
        except ValueError:
            pass
    metadata["SourceSystemOwner"]["allowedValues"] = enabled
    configured = policy.get("environmentOwners", {}).get(request["environment"])
    crosswalk = load_crosswalk()
    context.update({"defaultOperation": "create", "allowedOperations": ["create"],
                    "mandatoryFields": {"ContentItem": ["Name", "ContextName", "DateFrom", "ItemText9", "ItemText1", "ItemText10"]},
                    "semanticFields": {"ContentItem": mapping}, "fieldMetadata": {"ContentItem": metadata},
                    "variantField": mapping["TypeCode"], "createRows": [], "derivedValues": {},
                    "resolvedSemanticValues": {}, "mappingEvidence": {"ContentItem": {}},
                    "resolutionContract": {"catalogVersion": catalog["version"], "catalogSha256": _digest(catalog),
                                           "voCrosswalkVersion": crosswalk["version"], "voCrosswalkSha256": _digest(crosswalk),
                                           "ownerPolicyVersion": policy["version"], "ownerPolicySha256": _digest(policy)}})
    context["evidenceSources"]["catalog-template"] = {**base, "source": "Versioned Goal Management HDL catalog and VO crosswalk checked against full UCM template",
        "mappings": {"ContentItem": mapping}, "catalogSources": catalog["sources"], "catalogVersion": catalog["version"],
        "voCrosswalkSource": crosswalk["source"], "voCrosswalkVersion": crosswalk["version"]}
    context["mappingEvidence"]["ContentItem"] = {k: {"field": v, "evidenceRef": "catalog-template"} for k, v in mapping.items()}
    context["evidenceSources"]["HRG_PRIORITY"] = {**base, "source": "Current HRG_PRIORITY lookup", "items": priority_lookup["lookupCodes"]}
    context["mandatoryFields"]["ContentItem"].append(mapping["PriorityCode"])
    try:
        validate_incoming(rows, PROFILES[request["profile"]])
    except ValueError as exc:
        raise HdlDatValidationError(str(exc)) from exc
    for index, supplied in enumerate(rows):
        row = deepcopy(supplied)
        name = row.get("GoalName")
        if not isinstance(name, str) or not name.strip():
            raise HdlDatValidationError("GOAL_NAME_INVALID: provide nonblank unique names.")
        candidates = replay_pages(evidence.get("searchPages", {}).get(name))
        assessment = assess_duplicates(row, candidates, kind=PROFILES[request["profile"]],
            pagination_complete=True, environment=evidence["environment"],
            expected_environment=request["environment"])
        if assessment["status"] != "clear":
            raise HdlDatValidationError("EXISTING_GOAL_REQUIRES_RECONCILIATION: " + assessment["status"] +
                "; hydrate candidate type before deciding or reusing.")
        if row.get("TypeCode", PROFILES[request["profile"]]) != PROFILES[request["profile"]]:
            raise HdlDatValidationError("VARIANT_MISMATCH: supplied goal type conflicts with selected task.")
        row["TypeCode"] = PROFILES[request["profile"]]
        row.setdefault("StatusCode", fields["StatusCode"]["default"])
        row.setdefault("Visible", fields["Visible"]["default"])
        row.setdefault("PriorityCode", fields["PriorityCode"]["default"])
        if row["StatusCode"] != "I":
            raise HdlDatValidationError("ACTIVE_CREATE_UNSUPPORTED: stage inactive, then use separate activation approval.")
        owner = row.pop("SourceSystemOwner", configured)
        if row.pop("ContextName", catalog["context"]) != catalog["context"]:
            raise HdlDatValidationError("INVALID_GOAL_CONTEXT: Library Goal ContentItem must use GOAL.")
        if not owner:
            raise HdlDatValidationError("OWNER_POLICY_NOT_CONFIGURED: configure an environment owner in source-system-policy.json.")
        try:
            validate_source_owner(context, owner)
        except ValueError as exc:
            raise HdlDatValidationError(f"OWNER_POLICY_INVALID: configured/supplied owner is not enabled and effective: {owner}.") from exc
        source_id = row.pop("SourceSystemId", None)
        location = f"ContentItem.dat|ContentItem|line:{index + 2}"
        context["createRows"].append(location)
        values = {"ContextName": catalog["context"], "SourceSystemOwner": owner,
                  "DateFrom": _date_value(row.pop("DateFrom", row.get("StartDate", now[:10])), "DateFrom")}
        if row.get("StartDate") and row.get("TargetCompletionDate"):
            if _date_value(row["StartDate"], "StartDate") > _date_value(row["TargetCompletionDate"], "TargetCompletionDate"):
                raise HdlDatValidationError("DATE_RANGE_INVALID: target completion precedes start date.")
        if row.get("DateTo") and _date_value(row.get("DateFrom", row.get("StartDate", now[:10])), "DateFrom") > _date_value(row["DateTo"], "DateTo"):
            raise HdlDatValidationError("DATE_RANGE_INVALID: effective end precedes DateFrom.")
        if source_id is not None:
            if not isinstance(source_id, str) or not source_id.strip():
                raise HdlDatValidationError("SOURCE_KEY_INVALID: supplied source ID is blank.")
            values["SourceSystemId"] = source_id
        scope = {}
        for semantic, value in row.items():
            spec = fields[semantic]
            if spec.get("requiresValueEvidence"):
                proof = evidence.get("resolvedReferences", {}).get(name, {}).get(semantic)
                if not isinstance(proof, dict):
                    raise HdlDatValidationError(f"REFERENCE_EVIDENCE_REQUIRED: owning lookup must resolve {semantic}.")
                ref = f"scope:{index}:{semantic}"
                context["evidenceSources"][ref] = proof
                require_reference(context, ref)
                scope[semantic] = {"value": value, "evidenceRef": ref}
            if spec["type"] == "date":
                value = _date_value(value, semantic)
            if spec["type"] == "integer" and (type(value) is not int or value <= 0):
                raise HdlDatValidationError(f"REFERENCE_INVALID: {semantic} requires a resolved positive integer.")
            if spec["type"] == "decimal":
                from decimal import Decimal, InvalidOperation
                try:
                    if isinstance(value, bool) or not Decimal(str(value)).is_finite():
                        raise InvalidOperation
                except (InvalidOperation, ValueError):
                    raise HdlDatValidationError(f"VALUE_INVALID: {semantic} requires a finite decimal.")
            if value is None or isinstance(value, (dict, list, bool)):
                raise HdlDatValidationError(f"VALUE_INVALID: {semantic} requires a scalar value.")
            value = str(value)
            field = spec["field"]
            if any(c in value for c in ("|", "\r", "\n", "\x00")) or len(value) > metadata[field].get("maxLength", float("inf")):
                raise HdlDatValidationError(f"VALUE_INVALID: {semantic} exceeds the HDL field contract.")
            if metadata[field].get("allowedValues") and value not in metadata[field]["allowedValues"]:
                raise HdlDatValidationError(f"VALUE_INVALID: unsupported {semantic} code.")
            values[field] = value
        context["derivedValues"][location] = values
        if scope:
            context["resolvedSemanticValues"][location] = scope
    return context


def _date_value(value, semantic):
    try:
        if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError("ISO date required")
        return date.fromisoformat(value).strftime("%Y/%m/%d")
    except ValueError as exc:
        raise HdlDatValidationError(f"DATE_INVALID: {semantic} requires a valid YYYY-MM-DD date.") from exc


def read_live_evidence(request, control):
    """Declared read adapter; call only after the owning workflow permits this HDL task."""
    guard_route(request)
    task = control.get("execution_control", {}).get("task", {})
    expected_area = "Performance Library Goals" if request["profile"] == "performance_library_goal" else "Development Library Goals"
    from plan_guided_next_actions import _control_fingerprint
    execution = control.get("execution_control", {})
    branch = "performance-library-goals" if request["profile"] == "performance_library_goal" else "development-library-goals"
    expected_skill = f"pillars/hcm/goal-management/{branch}/goal-library/SKILL.md"
    if (control.get("allowed") is not True or control.get("status") != "allowed" or
        task.get("functional_area") != expected_area or task.get("task_code") != "HRG_MANAGE_GOAL_LIBRARY" or
        task.get("offering") != "Goal Management" or task.get("skill_path") != expected_skill or
        type(task.get("sequence")) is not int or task["sequence"] < 1 or not execution.get("plan_fingerprint") or
        control.get("execution_control_fingerprint") != _control_fingerprint(execution)):
        raise HdlDatValidationError("EXECUTION_CONTROL_REQUIRED: obtain a fresh allowed owning-task control.")
    rows = request.get("rows")
    if request.get("operation", "create") != "create" or not isinstance(rows, list) or not rows:
        raise HdlDatValidationError("BUSINESS_ROWS_REQUIRED: root Library Goal create rows are required.")
    catalog = load_catalog()
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise HdlDatValidationError("BUSINESS_ROWS_REQUIRED: root Library Goal create rows are required.")
        names = [value for key, value in row.items()
                 if isinstance(key, str) and re.sub(r"[^a-z0-9]", "", key.casefold()) in {"goalname", "name"}]
        if not any(isinstance(value, str) and value.strip() for value in names):
            raise HdlDatValidationError("GOAL_NAME_INVALID: provide nonblank unique names.")
        for semantic, value in row.items():
            if value is None or isinstance(value, (dict, list, bool)) or any(c in str(value) for c in ("|", "\r", "\n", "\x00")):
                raise HdlDatValidationError(f"VALUE_INVALID: invalid {semantic} input.")
            if semantic in {"StartDate", "TargetCompletionDate", "DateFrom"}:
                _date_value(value, semantic)
    sys.path.insert(0, str(ROOT / "core/data-loader/scripts"))
    import data_loader_metadata as core
    config = core.read_config(open_browser=False)
    if config["environment"] != request["environment"]:
        raise HdlDatValidationError("ENVIRONMENT_MISMATCH: request differs from Core configuration.")
    started = datetime.now(timezone.utc).isoformat()
    schema = core.load_business_object_schema("ContentItem", config, allow_aliases=False)
    template = set(schema.sections_by_discriminator["ContentItem"].attribute_names)
    attributes = {a["AttributeName"]: a for a in schema.attributes["ContentItem"]}
    normalized_rows, _ = resolve_rows(rows, catalog, attributes, template)
    for row in normalized_rows:
        if not isinstance(row.get("GoalName"), str) or not row["GoalName"].strip():
            raise HdlDatValidationError("GOAL_NAME_INVALID: provide nonblank unique names.")
        seen.add(row["GoalName"])
    def get(path):
        return core.get_json(config["host"] + path, config["auth"], stage="library-goal-hdl-read")
    owner_root = "/fscmRestApi/resources/latest/commonLookups/HRC_SOURCE_SYSTEM_OWNER"
    owner = get(owner_root)
    codes, offset = [], 0
    for _ in range(1000):
        page = get(owner_root + "/child/lookupCodes?" + urlencode({"limit": 500, "offset": offset, "onlyData": "true"}))
        if not isinstance(page.get("items"), list) or type(page.get("hasMore")) is not bool:
            raise HdlDatValidationError("OWNER_LOOKUP_INVALID: malformed pagination.")
        codes.extend(page["items"])
        if not page["hasMore"]:
            break
        if not page["items"]:
            raise HdlDatValidationError("OWNER_LOOKUP_INVALID: empty nonterminal page.")
        offset += len(page["items"])
    else:
        raise HdlDatValidationError("OWNER_LOOKUP_INVALID: pagination limit.")
    searches = {}
    priority_codes, offset = [], 0
    for _ in range(1000):
        page = get("/fscmRestApi/resources/latest/commonLookups/HRG_PRIORITY/child/lookupCodes?" + urlencode({"limit": 500, "offset": offset, "onlyData": "true"}))
        if not isinstance(page.get("items"), list) or type(page.get("hasMore")) is not bool:
            raise HdlDatValidationError("PRIORITY_LOOKUP_INVALID: malformed pagination.")
        priority_codes.extend(page["items"])
        if not page["hasMore"]:
            break
        if not page["items"]:
            raise HdlDatValidationError("PRIORITY_LOOKUP_INVALID: empty nonterminal page.")
        offset += len(page["items"])
    else:
        raise HdlDatValidationError("PRIORITY_LOOKUP_INVALID: pagination limit.")
    for row in normalized_rows:
        pages, offset = [], 0
        for _ in range(1000):
            response = core.request_json(config["host"] + "/hcmRestApi/resources/latest/libraryGoals/action/findByAdvancedSearchQuery",
                config["auth"], stage="library-goal-hdl-read", method="POST",
                data=json.dumps(build_search_payload(query=row["GoalName"], offset=offset)).encode(),
                content_type="application/vnd.oracle.adf.action+json")
            pages.append(response)
            page = normalize_page(response, expected_offset=offset)
            if not page["hasMore"]:
                break
            offset = page["nextOffset"]
        else:
            raise HdlDatValidationError("SEARCH_PAGINATION_LIMIT: duplicate check incomplete.")
        # Search projections omit identity dates. Hydrate every exact-name candidate
        # from its fresh opaque item link; never synthesize a key or use a broad query.
        matches = [r for r in replay_pages(pages) if r["GoalName"].strip() == row["GoalName"].strip()]
        if matches:
            try:
                items = [get(_fresh_item_path(candidate, config["host"])) for candidate in matches]
            except HdlDatValidationError as exc:
                if "no fresh item link" not in str(exc):
                    raise
                # Some action contracts omit item links. Use only an exact-name,
                # fully-expanded and completely paged collection fallback.
                items, offset = [], 0
                for _ in range(1000):
                    detail = get("/hcmRestApi/resources/latest/libraryGoals?" + urlencode({
                        "q": "GoalName='" + row["GoalName"].strip().replace("'", "''") + "'",
                        "fields": "*", "limit": 500, "offset": offset, "onlyData": "true"}))
                    if not isinstance(detail.get("items"), list) or type(detail.get("hasMore")) is not bool:
                        raise HdlDatValidationError("SEARCH_HYDRATION_INVALID: invalid collection response.")
                    items.extend(detail["items"])
                    if not detail["hasMore"]:
                        break
                    if not detail["items"]:
                        raise HdlDatValidationError("SEARCH_HYDRATION_INVALID: empty nonterminal page.")
                    offset += len(detail["items"])
                else:
                    raise HdlDatValidationError("SEARCH_PAGINATION_LIMIT: hydration incomplete.")
            hydrated = [{"result": {"items": items, "summary": [{"offset": 0,
                "count": len(items), "limit": max(1, len(items)), "hasMore": False}]}}]
            if not replay_pages(hydrated):
                raise HdlDatValidationError("SEARCH_HYDRATION_INVALID: search candidate disappeared; refresh evidence.")
            pages = hydrated
        searches[row["GoalName"]] = pages
    return {"environment": config["environment"], "verifiedAt": started,
            "source": "Core Data Loader full UCM template, component attributes, owner lookup and goal search",
            "schemaSource": schema.schema_source,
            "templateAttributes": list(schema.sections_by_discriminator["ContentItem"].attribute_names),
            "attributes": list(schema.attributes["ContentItem"]),
            "sourceOwners": {"LookupType": owner.get("LookupType"), "lookupCodes": codes}, "searchPages": searches,
            "priorityLookup": {"LookupType": "HRG_PRIORITY", "lookupCodes": priority_codes}}
