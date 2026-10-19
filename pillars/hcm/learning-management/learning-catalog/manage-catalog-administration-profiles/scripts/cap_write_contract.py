"""CAP write-contract assessment and root readback checks; no I/O or authorization."""
from __future__ import annotations

import cap_read

ROOT = "learningCatalogProfiles"
FIELDS = ("learningCatalogProfileNumber", "name", "description", "visibility", "status",
          "isSystemDefault", "processingStatus")
TRANSPORT_LIMITATION = "User accepted existing shared loader transport; upload/initiation configured-host redirect protection is not established"
REQUIREMENTS = {
    "create": ["Deployed generated-number, omitted status/date and contributor-free semantics",
               "Duplicate-name semantics, complete accessible duplicate baseline and current live template/field parity",
               "Attributed CAP/UCM/loader privilege assessment and shared preflight; feature readiness; active project Run Book",
               "Executable CAP rules and exact ZIP/target/operation/input/evidence approval binding"],
    "update": ["Canonical item key and verified loader PATCH mapping", "Explicit field diff/null/concurrency contract and operation grants"],
    "contributors": ["Person resolution and criterion/attachment/parent keys", "Verified individual/file add/change/remove mappings and effective membership readback"],
    "activate": ["Verified status transition, canonical key/PATCH mapping and grants"],
    "deactivate": ["Canonical key/PATCH, current usage/provider eligibility and grants"],
    "content-defaults": ["Seeded per-type row keys, allowed fields and registration", "Observer replacement/null/reset/inheritance semantics"],
    "certificates": ["Existing CAP certificate key and permitted template resolver", "Enable/disable/null clearing, registration, grants and rendering/inheritance acceptance"],
    "delete": ["Logical deletion and eligible replacement/migration route", "System-default/provider protection, usage, grants and complete migration readback"],
    "reconcile": ["Documented action arguments, grants, shared execution route and terminal correlation"],
}


def describe_facts(payload):
    """Retain schema facts, not identifiers, links or default expressions."""
    root = cap_read.resource_description(payload, ROOT)
    for section in ("collection", "item"):
        container = root.get(section, {})
        if not isinstance(container, dict) or not isinstance(container.get("actions", []), list):
            raise ValueError("CAP describe action containers must be objects with action lists")
    cap_read.validate_listing_metadata(root, ("learningCatalogProfileNumber",), ("name",))
    attributes = root["attributes"]
    facts = {}
    for name in FIELDS:
        selected = [a for a in attributes if isinstance(a, dict) and a.get("name") == name]
        if len(selected) != 1:
            facts[name] = {"present": False}
            continue
        attribute = selected[0]
        facts[name] = {"present": True}
        for key in ("type", "updatable", "allowChanges", "mandatory", "inputRequired", "maxLength"):
            value = attribute.get(key)
            if type(value) in (str, int, bool) and (not isinstance(value, str) or len(value) <= 80):
                facts[name][key] = value
    methods = {}
    for section in ("collection", "item"):
        actions = root.get(section, {}).get("actions", [])
        methods[section] = sorted({a["method"] for a in actions if isinstance(a, dict)
                                  and a.get("method") in {"GET", "POST", "PATCH", "DELETE"}})
    return {"attributes": facts, "advertised_methods": methods}


def registration_facts(detail):
    if not isinstance(detail, dict) or detail.get("BusObjTopDiscriminator") != ROOT:
        raise ValueError("CAP registration identity mismatch")
    facts = {"matched": True}
    for field in ("BusObjTopDiscriminator", "ObjectType", "ProductAreaCode", "ServiceVersion",
                  "ValidOperations", "EffectiveDated", "TemplateFileName"):
        value = detail.get(field)
        if type(value) in (str, bool) and (not isinstance(value, str) or len(value) <= 120):
            facts[field] = value
    facts["template_reference_present"] = bool(isinstance(detail.get("UcmContentId"), str)
                                                and detail["UcmContentId"].strip())
    facts["template_content_verified"] = False
    return facts


def assess(root_payload, registration):
    """Successful metadata inspection never certifies create or execution rights."""
    root = describe_facts(root_payload)
    requirements = {key: list(value) for key, value in REQUIREMENTS.items()}
    if "POST" not in root["advertised_methods"]["collection"]:
        requirements["create"].insert(0, "Collection POST is not advertised by current describe")
    for field in ("learningCatalogProfileNumber", "status"):
        attribute = root["attributes"][field]
        if attribute.get("inputRequired") is True or attribute.get("mandatory") is True:
            requirements["create"].append(field + ": required-input marker needs reconciliation before omission; not a request to invent a value")
    return {"status": "assessed_writes_blocked", "write_eligible": False,
            "validation_purpose": "write_contract_inspection_only", "root": root,
            "registration": registration_facts(registration), "privileges_verified": False,
            "transport_limitation": TRANSPORT_LIMITATION,
            "operations": {key: {"status": "blocked", "blockers": value}
                           for key, value in requirements.items()},
            "next_step": "Resolve operation-specific evidence and executable validation; no load is approval-ready"}


def verify_root_readback(expected, read_result):
    """Compare a unique full root read. This is not a loader/job success evaluator."""
    if (not isinstance(expected, dict) or not expected or set(expected) - set(FIELDS)
            or any(not isinstance(v, str) or not v for v in expected.values())
            or "learningCatalogProfileNumber" not in expected or "name" not in expected):
        raise ValueError("Exact returned profile number/name and approved text fields are required")
    if (not isinstance(read_result, dict) or read_result.get("status") != "matched"
            or read_result.get("pagination_completed") is not True
            or read_result.get("match_count") != 1 or type(read_result.get("match_count")) is not int
            or not isinstance(read_result.get("matches"), list) or len(read_result["matches"]) != 1
            or not isinstance(read_result["matches"][0], dict)):
        raise ValueError("Complete unique exact readback is required")
    row = read_result["matches"][0]
    differences = sorted(key for key, value in expected.items() if row.get(key) != value)
    status = row.get("processingStatus")
    return {"status": "mismatch" if differences else "root_fields_match",
            "different_fields": differences,
            "processing": "pending" if status == "ORA_NEEDS_PROCESSING" else "unverified",
            "loader_completion_verified": False, "processing_completion_verified": False,
            "write_eligible": False,
            "next_step": "Verify loader terminal counts/errors and supported CAP processing evidence separately"}
