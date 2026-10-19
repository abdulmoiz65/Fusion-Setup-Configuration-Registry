#!/usr/bin/env python3
"""Local new-catalog set binding and comparison; no Fusion calls or approval writes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from build_profile_content_library_preview import OBJECT_GROUPS, contains_sensitive

TASK = "ORA_MANAGE_PROFILE_ITEM_CATALOG"
CAPABILITY = "item-catalog-new-set-v1"
REGISTRY = Path(__file__).resolve().parents[1] / "item-catalogs/references/catalog-new-set-fsm-provider.json"
PARENT = "ORA_TALENT_PROFILE_ITEM_CATALOG.csv"
CHILD = "ORA_TALENT_CATALOG_CONTENT_ITEM.csv"
RATING = "ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv"
CONFIRMATION_POLICY = "new-catalog-set-user-nonproduction-v1"
EXISTING_SKILL_CAPABILITY = "item-catalog-existing-skill-canary-v1"
EXISTING_SKILL_REGISTRY = REGISTRY.with_name("catalog-existing-skill-fsm-provider.json")


def validate_target_confirmation(proposal, contract):
    """Compare optional user classification bindings; Core still owns authentication."""
    if "target_classification_confirmation" not in contract:
        return
    confirmation = contract["target_classification_confirmation"]
    keys = {"policy_id", "confirmed_non_production", "target_environment",
            "proposal_fingerprint", "authenticated_target_evidence_reference",
            "confirmation_reference"}
    if not isinstance(confirmation, dict) or set(confirmation) != keys:
        raise ValueError("complete target classification confirmation is required")
    if (confirmation["policy_id"] != CONFIRMATION_POLICY
            or confirmation["confirmed_non_production"] is not True):
        raise ValueError("explicit non-production confirmation under the scoped policy is required")
    target = proposal.get("target_environment")
    if not isinstance(target, str) or not target.strip() or confirmation["target_environment"] != target:
        raise ValueError("target classification confirmation differs from the authenticated target")
    digest = proposal.get("proposal_fingerprint")
    if (not isinstance(digest, str) or len(digest) != 64
            or any(c not in "0123456789abcdef" for c in digest)
            or confirmation["proposal_fingerprint"] != digest):
        raise ValueError("target classification confirmation differs from the reviewed proposal")
    evidence = contract["target_evidence_reference"]
    if confirmation["authenticated_target_evidence_reference"] != evidence:
        raise ValueError("target classification confirmation differs from authenticated evidence")
    reference = confirmation["confirmation_reference"]
    if not isinstance(reference, str) or not reference.strip() or reference == evidence:
        raise ValueError("a separate sanitized user confirmation reference is required")


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


def registry(*, existing_skill=False):
    raw = (EXISTING_SKILL_REGISTRY if existing_skill else REGISTRY).read_bytes()
    data = json.loads(raw)
    if (data["schema_version"] != "1.0" or data["capability_id"] != (EXISTING_SKILL_CAPABILITY if existing_skill else CAPABILITY)
            or data["task_code"] != TASK or data["lifecycle"] != "certification-only"
            or data["parent_strategy"] != ("one-existing-custom-catalog" if existing_skill else "one-new-catalog")
            or data["child_strategy"] != ("one-portable-child" if existing_skill else "all-supplied-portable-children")
            or data["runtime_verification"] != "not-established"):
        raise ValueError("new-set registry is inconsistent; promotion requires a reviewed implementation")
    if existing_skill and (data["contexts"] != ["SKILL"] or data["allowed_supplier_codes"] != ["C"]):
        raise ValueError("existing SKILL canary scope cannot be broadened by registry edits")
    return data, hashlib.sha256(raw).hexdigest()


def validate_binding(proposal, *, existing_skill=False):
    """Validate already routed, sanitized evidence assertions, not their remote authority."""
    if not isinstance(proposal, dict) or contains_sensitive(proposal):
        raise ValueError("unsafe new-set proposal")
    if proposal.get("task_code") != TASK or proposal.get("operation") != "create":
        raise ValueError("new-set contract requires create-only Item Catalogs")
    contract = proposal.get("catalog_set_contract")
    keys = {"capability_id", "registry_sha256", "use", "target_classification",
            "target_evidence_reference", "source", "mappings", "group_counts"}
    if not isinstance(contract, dict) or set(contract) not in (keys, keys | {"target_classification_confirmation"}):
        raise ValueError("complete catalog_set_contract is required")
    if existing_skill and "target_classification_confirmation" in contract:
        raise ValueError("new-catalog user classification policy does not authorize existing-catalog certification; use routed target evidence")
    provider, digest = registry(existing_skill=existing_skill)
    if contract["capability_id"] != provider["capability_id"] or contract["registry_sha256"] != digest:
        raise ValueError("new-set capability registry binding differs")
    if contract["use"] != "controlled-certification" or contract["target_classification"] != "non-production":
        raise ValueError("new-set execution is controlled-certification in non-production only")
    if proposal["dependency_evidence"]["item_catalog_content_item_provider_use"] != "controlled-certification":
        raise ValueError("narrow provider verification cannot promote new-set use")
    if not isinstance(contract["target_evidence_reference"], str) or not contract["target_evidence_reference"].strip():
        raise ValueError("routed authenticated target evidence is required")
    validate_target_confirmation(proposal, contract)
    source = contract["source"]
    if not isinstance(source, dict) or set(source) != {"input_method", "reference", "sha256"}:
        raise ValueError("source input method, reference and fingerprint are required")
    if source["input_method"] not in {"direct", "template", "existing-file"}:
        raise ValueError("unsupported input method")
    if not isinstance(source["reference"], str) or not source["reference"].strip():
        raise ValueError("source reference is required")
    digest_value = source["sha256"]
    if not isinstance(digest_value, str) or len(digest_value) != 64 or any(c not in "0123456789abcdef" for c in digest_value):
        raise ValueError("source fingerprint is invalid")
    rows = proposal["rows"]
    if set(rows) != {PARENT, CHILD, RATING} or len(rows[PARENT]) != 1 or not rows[CHILD] or rows[RATING]:
        raise ValueError("new-set scope is one parent and all supplied children, with no rating rows")
    if existing_skill and len(rows[CHILD]) != 1:
        raise ValueError("existing SKILL certification requires exactly one explicitly selected canary child; never trim a batch")
    context = rows[PARENT][0]["ContextName"]
    if context not in provider["contexts"]:
        raise ValueError("unregistered new-set context")
    if rows[PARENT][0]["ContentValueSetCode"] in provider.get("excluded_catalog_codes", {}).get(context, []):
        raise ValueError("new-set creation cannot target a predefined or managed catalog")
    if any(row["ContentSupplierCode"] not in provider["allowed_supplier_codes"] for row in rows[CHILD]):
        raise ValueError("unsupported new-set supplier")
    counts = {name: 0 for name in OBJECT_GROUPS}
    counts.update(item_catalogs=1, item_catalog_content_items=len(rows[CHILD]))
    if contract["group_counts"] != counts or any(type(v) is not int for v in contract["group_counts"].values()):
        raise ValueError("complete 14-group counts must match the supplied portable set; do not omit unsupported groups")
    mappings = contract["mappings"]
    if not isinstance(mappings, list):
        raise ValueError("confirmed row mappings are required")
    expected = {(member, index) for member in (PARENT, CHILD) for index in range(len(rows[member]))}
    found = set()
    for mapping in mappings:
        if not isinstance(mapping, dict) or set(mapping) != {"member", "row_index", "source_reference", "status"}:
            raise ValueError("invalid row mapping")
        if (mapping["status"] != "confirmed" or type(mapping["row_index"]) is not int
                or not isinstance(mapping["source_reference"], str) or not mapping["source_reference"].strip()):
            raise ValueError("every supplied row requires a confirmed source mapping")
        key = (mapping["member"], mapping["row_index"])
        if key in found or key not in expected:
            raise ValueError("duplicate or foreign row mapping")
        found.add(key)
    if found != expected:
        raise ValueError("incomplete row mapping coverage")
    return fingerprint(proposal)


def preview(proposal, *, existing_skill=False):
    digest = validate_binding(proposal, existing_skill=existing_skill)
    return {"schema_version": "1.0", "status": "catalog_set_package_preview",
            "capability_id": EXISTING_SKILL_CAPABILITY if existing_skill else CAPABILITY, "catalog_set_fingerprint": digest,
            "proposal": json.loads(json.dumps(proposal)), "creation_authorized": False,
            "requested_approval": ("PREPARE EXISTING SKILL CANARY " if existing_skill else "PREPARE CATALOG SET ") + digest,
            "next_action": "Review every row and mapping; this approval permits local package preparation only."}


def require_approval(proposal, statement, *, existing_skill=False):
    digest = validate_binding(proposal, existing_skill=existing_skill)
    prefix = "PREPARE EXISTING SKILL CANARY " if existing_skill else "PREPARE CATALOG SET "
    if statement != prefix + digest:
        raise ValueError("exact complete-set package-preparation approval is missing or stale")
    return digest
