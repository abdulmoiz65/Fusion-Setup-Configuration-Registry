#!/usr/bin/env python3
"""Build and verify deterministic GROW-8154 previews without Fusion access.

This helper reads local JSON and writes sanitized JSON to stdout. It has no
network, authentication, loader, polling, retry, or Fusion mutation code.
"""

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path


SCHEMA_VERSION = "1.0"
TASK_CODES = (
    "HRT_MANAGE_PROFILE_CONTENT_TYPES",
    "HRT_MANAGE_PROFILE_CONTENT_ITEMS",
    "ORA_MANAGE_PROFILE_ITEM_CATALOG",
    "HRT_MANAGE_INSTANCE_QUALIFIERS",
    "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS",
)
OBJECT_GROUPS = (
    "content_types",
    "content_type_properties",
    "content_type_relationships",
    "content_items",
    "content_item_rating_descriptions",
    "content_item_relationships",
    "item_catalogs",
    "item_catalog_content_items",
    "item_catalog_item_rating_descriptions",
    "instance_qualifiers",
    "instance_qualifier_sets",
    "educational_establishments",
    "behavior_item_catalogs",
    "competency_to_behavior_relationships",
)
GROUP_TASKS = {
    "content_types": "HRT_MANAGE_PROFILE_CONTENT_TYPES",
    "content_type_properties": "HRT_MANAGE_PROFILE_CONTENT_TYPES",
    "content_type_relationships": "HRT_MANAGE_PROFILE_CONTENT_TYPES",
    "content_items": "HRT_MANAGE_PROFILE_CONTENT_ITEMS",
    "content_item_rating_descriptions": "HRT_MANAGE_PROFILE_CONTENT_ITEMS",
    "content_item_relationships": "HRT_MANAGE_PROFILE_CONTENT_ITEMS",
    "item_catalogs": "ORA_MANAGE_PROFILE_ITEM_CATALOG",
    "item_catalog_content_items": "ORA_MANAGE_PROFILE_ITEM_CATALOG",
    "item_catalog_item_rating_descriptions": "ORA_MANAGE_PROFILE_ITEM_CATALOG",
    "instance_qualifiers": "HRT_MANAGE_INSTANCE_QUALIFIERS",
    "instance_qualifier_sets": "HRT_MANAGE_INSTANCE_QUALIFIERS",
    "educational_establishments": "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS",
    "behavior_item_catalogs": "ORA_MANAGE_PROFILE_ITEM_CATALOG",
    "competency_to_behavior_relationships": "HRT_MANAGE_PROFILE_CONTENT_ITEMS",
}
APPROVED_ROUTES = {
    "HRT_MANAGE_PROFILE_CONTENT_TYPES": "core.data-loader",
    "HRT_MANAGE_PROFILE_CONTENT_ITEMS": "core.data-loader",
    "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS": "core.data-loader",
}
BLOCKED_ROUTES = {
    "ORA_MANAGE_PROFILE_ITEM_CATALOG": (
        "catalog-only import requires the task-specific FSM package and "
        "core.data-loader Task Hook preview; combined-set submission is unsupported"
    ),
    "HRT_MANAGE_INSTANCE_QUALIFIERS": "exact provider member and field contract is not established",
}
BLOCKED_OBJECT_GROUPS = {
    "content_item_rating_descriptions": "item-specific proficiency-description persistence is unproven",
    "item_catalog_item_rating_descriptions": "catalog rating-description persistence is unproven",
    "competency_to_behavior_relationships": "competency-to-behavior persistence is unproven",
}
SAFE_ALIAS = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
SAFE_REQUEST_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
SHA256 = re.compile(r"^[a-f0-9]{64}$")
SENSITIVE_KEY = re.compile(
    r"(?:password|secret|token|private[_-]?key|authorization|credential|client[_-]?id)",
    re.IGNORECASE,
)
SENSITIVE_VALUE = re.compile(
    r"(?:bearer\s+\S+|-----BEGIN\s+[A-Z0-9 ]*PRIVATE\s+KEY-----|"
    r"(?:password|secret|token|private[_ -]?key)\s*[:=]\s*\S+)",
    re.IGNORECASE,
)
REDACTED = "[REDACTED-SENSITIVE-MATERIAL]"


class PreviewContractError(ValueError):
    """Raised when a request cannot safely reach the next local gate."""


def canonical_json_bytes(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def canonical_sha256(value):
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def sanitize(value, key=""):
    if SENSITIVE_KEY.search(str(key)):
        return REDACTED
    if isinstance(value, dict):
        return {
            str(item_key): sanitize(item_value, str(item_key))
            for item_key, item_value in value.items()
        }
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if isinstance(value, str) and SENSITIVE_VALUE.search(value):
        return REDACTED
    return value


def contains_sensitive(value, key=""):
    if SENSITIVE_KEY.search(str(key)):
        return True
    if isinstance(value, dict):
        return any(
            contains_sensitive(item_value, str(item_key))
            for item_key, item_value in value.items()
        )
    if isinstance(value, list):
        return any(contains_sensitive(item) for item in value)
    return isinstance(value, str) and bool(SENSITIVE_VALUE.search(value))


def require_mapping(value, label):
    if not isinstance(value, dict):
        raise PreviewContractError("%s must be an object" % label)
    return value


def require_list(value, label):
    if not isinstance(value, list):
        raise PreviewContractError("%s must be an array" % label)
    return value


def validate_contract(contract):
    root = require_mapping(contract, "contract")
    if root.get("schema_version") != SCHEMA_VERSION:
        raise PreviewContractError("contract.schema_version must be 1.0")
    complete_set_id = root.get("complete_set_id")
    if not isinstance(complete_set_id, str) or not complete_set_id.strip():
        raise PreviewContractError("contract.complete_set_id is required")

    scope = require_mapping(root.get("scope"), "contract.scope")
    task_codes = require_list(scope.get("task_codes"), "contract.scope.task_codes")
    if not task_codes or len(set(task_codes)) != len(task_codes):
        raise PreviewContractError("contract.scope.task_codes must contain unique task codes")
    unsupported = sorted(set(task_codes) - set(TASK_CODES))
    if unsupported:
        raise PreviewContractError(
            "contract.scope.task_codes contains unsupported values: %s"
            % ", ".join(unsupported)
        )
    if scope.get("complete_related_set") is not True:
        raise PreviewContractError("contract.scope.complete_related_set must be true")

    objects = require_mapping(root.get("objects"), "contract.objects")
    missing_groups = sorted(set(OBJECT_GROUPS) - set(objects))
    extra_groups = sorted(set(objects) - set(OBJECT_GROUPS))
    if missing_groups or extra_groups:
        raise PreviewContractError(
            "contract.objects must contain exactly the 14 governed object groups"
        )
    for group in OBJECT_GROUPS:
        rows = require_list(objects[group], "contract.objects.%s" % group)
        if rows and GROUP_TASKS[group] not in task_codes:
            raise PreviewContractError(
                "contract.objects.%s is outside the selected task scope" % group
            )
        for row in rows:
            record = require_mapping(row, "contract.objects.%s record" % group)
            if record.get("review_status") not in ("supplied", "confirmed"):
                raise PreviewContractError(
                    "every preview record must be supplied or confirmed"
                )
    represented_tasks = {
        GROUP_TASKS[group] for group in OBJECT_GROUPS if objects[group]
    }
    if represented_tasks != set(task_codes):
        raise PreviewContractError(
            "selected task scope must exactly match the tasks represented by object rows"
        )
    for label in (
        "objects",
        "mappings",
        "validation_results",
        "dependencies",
        "exact_match_results",
    ):
        if contains_sensitive(root.get(label), label):
            raise PreviewContractError(
                "sensitive material is not allowed in preview configuration values"
            )

    mappings = require_list(root.get("mappings"), "contract.mappings")
    unresolved = [
        item
        for item in mappings
        if isinstance(item, dict) and item.get("status") in ("uncertain", "blocked")
    ]
    if unresolved:
        raise PreviewContractError(
            "all uncertain or blocked mappings must be confirmed before preview"
        )

    validation_results = require_list(
        root.get("validation_results"), "contract.validation_results"
    )
    if any(
        isinstance(item, dict) and item.get("status") == "blocked"
        for item in validation_results
    ):
        raise PreviewContractError("blocked validation results prevent preview")

    dependencies = require_list(root.get("dependencies"), "contract.dependencies")
    if any(
        not isinstance(item, dict) or item.get("status") != "verified"
        for item in dependencies
    ):
        raise PreviewContractError(
            "every required dependency must have exact verified evidence"
        )

    exact_results = require_list(
        root.get("exact_match_results"), "contract.exact_match_results"
    )
    expected_reference_list = [
        row.get("local_key")
        for group in OBJECT_GROUPS
        for row in objects[group]
        if isinstance(row, dict)
    ]
    expected_references = set(expected_reference_list)
    if (
        any(not isinstance(value, str) or not value for value in expected_reference_list)
        or len(expected_references) != len(expected_reference_list)
    ):
        raise PreviewContractError("governed record local keys must be nonblank and unique")
    for group in OBJECT_GROUPS:
        for row in objects[group]:
            provider_key = require_mapping(
                row.get("provider_key"),
                "contract.objects.%s record.provider_key" % group,
            )
            provider_values = provider_key.get("values")
            if not isinstance(provider_key.get("type"), str) or not provider_key.get("type"):
                raise PreviewContractError("every provider key requires a nonblank type")
            if not isinstance(provider_values, list) or not provider_values or not all(
                isinstance(value, str) and value for value in provider_values
            ):
                raise PreviewContractError("every provider key requires exact nonblank values")

    allowed_classifications = {
        "exact",
        "not-found",
        "multiple-exact",
        "evidence-unavailable",
    }
    for item in exact_results:
        result = require_mapping(item, "contract.exact_match_results item")
        if "match_source" not in result:
            raise PreviewContractError("exact-match match_source is required")
        classification = result.get("classification")
        status = result.get("status")
        match_count = result.get("match_count")
        if classification not in allowed_classifications or status not in ("ready", "blocked"):
            raise PreviewContractError("exact-match classification or status is invalid")
        match_source = result.get("match_source")
        if match_source not in (None, "customer", "seeded"):
            raise PreviewContractError("exact-match match_source is invalid")
        if classification != "exact" and match_source is not None:
            raise PreviewContractError(
                "exact-match match_source is allowed only for exact classification"
            )
        if not isinstance(match_count, int) or isinstance(match_count, bool) or match_count < 0:
            raise PreviewContractError("exact-match match_count must be a nonnegative integer")
        expected_status = "ready" if classification == "not-found" else "blocked"
        if status != expected_status:
            raise PreviewContractError("exact-match status is inconsistent with classification")
        if classification == "exact" and match_count != 1:
            raise PreviewContractError("exact classification requires one match")
        if classification == "multiple-exact" and match_count < 2:
            raise PreviewContractError("multiple-exact classification requires at least two matches")
        if classification in ("not-found", "evidence-unavailable") and match_count != 0:
            raise PreviewContractError("classification match_count is inconsistent")
        require_mapping(result.get("provider_key"), "exact-match provider_key")
        require_list(result.get("differing_fields"), "exact-match differing_fields")
        require_list(result.get("warnings"), "exact-match warnings")
    actual_references = {
        item.get("object_reference")
        for item in exact_results
        if isinstance(item, dict)
    }
    if None in expected_references or actual_references != expected_references:
        raise PreviewContractError(
            "exact-match results must cover every governed record exactly once"
        )
    if len(actual_references) != len(exact_results):
        raise PreviewContractError("exact-match object references must be unique")
    validate_exact_check_bindings(root)
    if any(
        item.get("classification") == "not-found"
        and not item.get("evidence_reference")
        for item in exact_results
    ):
        raise PreviewContractError("exact-match evidence reference is required before preview")
    blocking_exact = [
        item
        for item in exact_results
        if not isinstance(item, dict)
        or item.get("status") == "blocked"
        or item.get("classification")
        in ("exact", "multiple-exact", "evidence-unavailable")
    ]
    if blocking_exact:
        raise PreviewContractError(
            "exact, multiple-exact, or evidence-unavailable results prevent creation"
        )

    lifecycle = require_mapping(root.get("lifecycle"), "contract.lifecycle")
    if lifecycle.get("status") not in ("duplicate_checked", "preview_ready"):
        raise PreviewContractError(
            "contract.lifecycle.status must be duplicate_checked before preview"
        )
    return root


def validate_provider_key(value, label):
    key = require_mapping(value, label)
    if set(key) != {"type", "values"}:
        raise PreviewContractError("%s requires only type and values" % label)
    if not isinstance(key["type"], str) or not key["type"].strip():
        raise PreviewContractError("%s.type must be a nonblank string" % label)
    values = key["values"]
    if not isinstance(values, list) or not values or not all(
        isinstance(item, str) and item.strip() for item in values
    ):
        raise PreviewContractError("%s.values must contain exact nonblank strings" % label)
    if contains_sensitive(key):
        raise PreviewContractError("sensitive material is not allowed in provider keys")
    return key


def validate_source_and_mapping_shapes(root):
    """Enforce the existing canonical source/mapping schema without resolving files."""
    if root.get("input_method") not in (
        "conversation", "blank_template", "spreadsheet", "csv", "host_extracted_document"
    ):
        raise PreviewContractError("contract.input_method is invalid")
    source = require_mapping(root.get("source"), "contract.source")
    required = {"safe_filename", "sha256", "retention"}
    if not required <= set(source) or set(source) - (required | {"external_reference"}):
        raise PreviewContractError("contract.source fields are invalid")
    if source["retention"] not in ("external-reference-only", "not-applicable"):
        raise PreviewContractError("contract.source.retention is invalid")
    for field in ("safe_filename", "external_reference"):
        if source.get(field) is not None and not isinstance(source[field], str):
            raise PreviewContractError("contract.source.%s must be a string or null" % field)
    fingerprint = source["sha256"]
    if fingerprint is not None and (
        not isinstance(fingerprint, str) or not SHA256.fullmatch(fingerprint)
    ):
        raise PreviewContractError("contract.source.sha256 must be a SHA-256 or null")
    for mapping in require_list(root.get("mappings"), "contract.mappings"):
        item = require_mapping(mapping, "mapping")
        if set(item) != {"source_reference", "target", "confidence", "status"}:
            raise PreviewContractError("mapping fields are invalid")
        if any(not isinstance(item[field], str) or not item[field].strip()
               for field in ("source_reference", "target")):
            raise PreviewContractError("mapping source reference and target must be nonblank")
        confidence = item["confidence"]
        if (isinstance(confidence, bool) or not isinstance(confidence, (int, float))
                or not 0 <= confidence <= 1):
            raise PreviewContractError("mapping confidence must be a number from zero to one")
        if item["status"] not in ("supplied", "confirmed", "uncertain", "blocked"):
            raise PreviewContractError("mapping status is invalid")


def validate_exact_check_bindings(root):
    """Bind every local check to its supplied record, without certifying live evidence."""
    validate_source_and_mapping_shapes(root)
    objects = require_mapping(root.get("objects"), "contract.objects")
    if set(objects) != set(OBJECT_GROUPS):
        raise PreviewContractError("contract.objects must contain exactly the 14 governed object groups")
    records = {}
    for group in OBJECT_GROUPS:
        for row in require_list(objects[group], "contract.objects.%s" % group):
            record = require_mapping(row, "governed record")
            values = require_mapping(record.get("values"), "record.values")
            if any(not isinstance(value, (str, int, float, bool, type(None)))
                   for value in values.values()):
                raise PreviewContractError("record.values must contain scalar values")
            source_refs = require_list(record.get("source_references"), "record.source_references")
            if not source_refs or any(not isinstance(value, str) or not value.strip()
                                      for value in source_refs):
                raise PreviewContractError("record.source_references must contain nonblank references")
            if record.get("review_status") not in (
                "supplied", "inferred-pending-review", "confirmed", "blocked", "not-applicable"
            ):
                raise PreviewContractError("record.review_status is invalid")
            reference = record.get("local_key")
            if not isinstance(reference, str) or not reference.strip() or reference in records:
                raise PreviewContractError("governed record local keys must be nonblank and unique")
            records[reference] = validate_provider_key(record.get("provider_key"), "record.provider_key")
    checks = require_list(root.get("exact_match_results"), "contract.exact_match_results")
    references = set()
    for check in checks:
        item = require_mapping(check, "exact-match result")
        reference = item.get("object_reference")
        if not isinstance(reference, str) or reference not in records or reference in references:
            raise PreviewContractError("exact-match results must cover every governed record exactly once")
        references.add(reference)
        key = validate_provider_key(item.get("provider_key"), "exact-match provider_key")
        if key != records[reference]:
            raise PreviewContractError("exact-match provider key differs from its governed record")
        identifiers = require_list(item.get("matched_identifiers", []), "matched_identifiers")
        if identifiers and len(identifiers) != item.get("match_count"):
            raise PreviewContractError("matched identifiers must cover every exact match")
        for identifier in identifiers:
            matched = validate_provider_key(identifier, "matched identifier")
            # This helper's keys are literal. Provider-specific comparison must
            # remain in its registered adapter, never inferred by this report.
            if matched != key:
                raise PreviewContractError("matched identifier differs from the checked literal provider key")
        evidence = item.get("evidence_reference")
        if evidence is not None and (not isinstance(evidence, str) or not evidence.strip()):
            raise PreviewContractError("evidence_reference must be a nonblank string or null")
        for field in ("differing_fields", "warnings"):
            if not all(isinstance(value, str) for value in require_list(item.get(field), field)):
                raise PreviewContractError("%s must contain strings" % field)
    if not records or references != set(records):
        raise PreviewContractError("exact-match results must cover every governed record exactly once")


def classify_exact_provider_key(proposed_key, candidates):
    """Compare literal keys without similarity search or reuse recommendations.

    The caller supplies keys from the task's supported exact-evidence route.
    This local comparison does not establish provider-specific case rules,
    evidence completeness, or live absence by itself.
    """

    proposed = validate_provider_key(proposed_key, "proposed_key")
    values = proposed["values"]
    key_type = proposed["type"]
    exact = []
    for candidate in require_list(candidates, "candidates"):
        item = require_mapping(candidate, "candidate")
        if contains_sensitive(item):
            raise PreviewContractError("sensitive material is not allowed in exact candidates")
        candidate_key = validate_provider_key(item.get("provider_key"), "candidate.provider_key")
        if candidate_key.get("type") != key_type:
            continue
        candidate_values = candidate_key["values"]
        if len(candidate_values) != len(values):
            raise PreviewContractError("candidate provider key component count differs from the proposed key")
        if candidate_values == values:
            exact.append(item)

    if len(exact) > 1:
        classification = "multiple-exact"
        status = "blocked"
    elif len(exact) == 1:
        classification = "exact"
        status = "blocked"
    else:
        classification = "not-found"
        status = "ready"
    return {
        "status": status,
        "classification": classification,
        "match_source": (
            exact[0].get("match_source")
            if len(exact) == 1
            and exact[0].get("match_source") in ("customer", "seeded")
            else None
        ),
        "match_count": len(exact),
        "matched_identifiers": [
            {"type": item["provider_key"]["type"],
             "values": list(item["provider_key"]["values"])}
            for item in exact
        ],
        "warnings": [],
    }


def build_exact_check_report(contract, target_environment_alias):
    """Expose duplicate identifiers without constructing an executable preview."""
    root = require_mapping(contract, "contract")
    if root.get("schema_version") != SCHEMA_VERSION:
        raise PreviewContractError("contract.schema_version must be 1.0")
    if not isinstance(target_environment_alias, str) or not SAFE_ALIAS.fullmatch(target_environment_alias):
        raise PreviewContractError("target_environment_alias must be a safe non-secret alias")
    complete_set_id = root.get("complete_set_id")
    if not isinstance(complete_set_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", complete_set_id):
        raise PreviewContractError("contract.complete_set_id is required")
    scope = require_mapping(root.get("scope"), "contract.scope")
    tasks = require_list(scope.get("task_codes"), "contract.scope.task_codes")
    if any(not isinstance(task, str) or task not in TASK_CODES for task in tasks):
        raise PreviewContractError("contract.scope.task_codes contains unsupported values")
    if not tasks or len(set(tasks)) != len(tasks) or scope.get("complete_related_set") is not True:
        raise PreviewContractError("exact report requires one complete related task set")
    validate_exact_check_bindings(root)
    represented = {GROUP_TASKS[group] for group in OBJECT_GROUPS if root["objects"][group]}
    if set(tasks) != represented:
        raise PreviewContractError("selected task scope must exactly match the tasks represented by object rows")
    source = require_mapping(root.get("source"), "contract.source")
    for field in ("mappings", "validation_results", "dependencies"):
        require_list(root.get(field), "contract.%s" % field)
    if contains_sensitive(root.get("objects")) or any(
        contains_sensitive(root.get(field)) for field in ("mappings", "validation_results", "dependencies")
    ):
        raise PreviewContractError("sensitive material is not allowed in report configuration values")
    checks = require_list(root.get("exact_match_results"), "exact_match_results")
    if not checks or contains_sensitive(checks) or contains_sensitive(complete_set_id):
        raise PreviewContractError("non-sensitive exact-match results are required")
    rows = []
    references = set()
    provider_blocked_references = {
        record["local_key"]
        for group in OBJECT_GROUPS
        if group in BLOCKED_OBJECT_GROUPS or GROUP_TASKS[group] in BLOCKED_ROUTES
        for record in root["objects"][group]
    }
    for check in checks:
        item = require_mapping(check, "exact-match result")
        reference = item.get("object_reference")
        if not isinstance(reference, str) or not reference.strip() or reference in references:
            raise PreviewContractError("exact-match object references must be nonblank and unique")
        references.add(reference)
        classification = item.get("classification")
        count = item.get("match_count")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise PreviewContractError("match_count must be a nonnegative integer")
        valid_count = {
            "exact": count == 1,
            "multiple-exact": count > 1,
            "not-found": count == 0,
            "evidence-unavailable": count == 0,
        }
        if not valid_count.get(classification, False):
            raise PreviewContractError("classification and match_count are inconsistent")
        expected_status = "ready" if classification == "not-found" else "blocked"
        if item.get("status") != expected_status:
            raise PreviewContractError("exact-match status is inconsistent with classification")
        if "match_source" not in item or item["match_source"] not in (None, "customer", "seeded"):
            raise PreviewContractError("exact-match match_source is required and must be valid")
        if classification != "exact" and item["match_source"] is not None:
            raise PreviewContractError("exact-match match_source is allowed only for exact classification")
        identifiers = require_list(item.get("matched_identifiers", []), "matched_identifiers")
        if identifiers and len(identifiers) != count:
            raise PreviewContractError("matched identifiers must cover every exact match")
        missing_identifiers = count > 0 and not identifiers
        gaps = []
        if missing_identifiers:
            gaps.append("Matching identifier evidence is missing.")
        if not item.get("evidence_reference"):
            gaps.append("Exact-check source evidence reference is missing.")
        rows.append({
            "object_reference": reference,
            "provider_key": copy.deepcopy(item["provider_key"]),
            "classification": classification,
            "match_source": item["match_source"],
            "match_count": count,
            "matched_identifiers": copy.deepcopy(identifiers),
            "evidence_reference": sanitize(item.get("evidence_reference")),
            "differing_fields": copy.deepcopy(require_list(item.get("differing_fields", []), "differing_fields")),
            "evidence_gaps": gaps,
            "create_blocked": classification != "not-found" or bool(gaps) or reference in provider_blocked_references,
        })
    provider_blockers = preview_scope_blockers(tasks, root["objects"])
    blocked = any(row["create_blocked"] for row in rows) or bool(provider_blockers)
    report = {
        "schema_version": SCHEMA_VERSION,
        "complete_set_id": complete_set_id,
        "target_environment_alias": target_environment_alias,
        "scope": copy.deepcopy(scope),
        "input_method": root.get("input_method"),
        "source": sanitize(copy.deepcopy(source)),
        "objects": copy.deepcopy(root["objects"]),
        "mappings": copy.deepcopy(root["mappings"]),
        "validation_results": copy.deepcopy(root["validation_results"]),
        "dependencies": copy.deepcopy(root["dependencies"]),
        "status": "blocked" if blocked else "review_only",
        "lifecycle_status": "review_only",
        "exact_match_results": rows,
        "provider_blockers": provider_blockers,
        "creation_authorized": False,
        "submission_attempted": False,
        "live_evidence_verified": False,
        "safe_next_action": (
            "Stop creation for blocked records; resolve exact evidence without reuse or updates."
            if blocked else
            "Complete the remaining task checks and immutable package review; this report is not execution approval."
        ),
    }
    report["report_fingerprint"] = canonical_sha256(report)
    return report


def preview_scope_blockers(task_codes, objects):
    blocked = [
        "%s: %s" % (task, BLOCKED_ROUTES[task])
        for task in task_codes
        if task in BLOCKED_ROUTES
    ]
    blocked.extend(
        "%s: %s" % (group, reason)
        for group, reason in BLOCKED_OBJECT_GROUPS.items()
        if objects.get(group)
    )
    return blocked


def require_supported_preview_scope(task_codes, objects):
    blocked = preview_scope_blockers(task_codes, objects)
    if blocked:
        raise PreviewContractError(
            "provider readiness prevents preview for persistence: %s" % "; ".join(blocked)
        )


def build_preview(contract, target_environment_alias, *, review_blocked=False):
    if not SAFE_ALIAS.fullmatch(str(target_environment_alias or "")):
        raise PreviewContractError(
            "target_environment_alias must be a safe non-secret alias"
        )
    root = validate_contract(contract)
    task_codes = root["scope"]["task_codes"]
    provider_blockers = preview_scope_blockers(task_codes, root["objects"])
    if not review_blocked:
        require_supported_preview_scope(task_codes, root["objects"])
    present = [group for group in OBJECT_GROUPS if root["objects"][group]]
    omitted = [group for group in OBJECT_GROUPS if not root["objects"][group]]
    body = {
        "schema_version": SCHEMA_VERSION,
        "complete_set_id": root["complete_set_id"],
        "input_method": root["input_method"],
        "source": sanitize(root["source"]),
        "target_environment_alias": target_environment_alias,
        "scope": copy.deepcopy(root["scope"]),
        "objects": sanitize(copy.deepcopy(root["objects"])),
        "confirmed_mappings": sanitize(copy.deepcopy(root["mappings"])),
        "validation_results": sanitize(copy.deepcopy(root["validation_results"])),
        "dependencies": sanitize(copy.deepcopy(root["dependencies"])),
        "exact_match_results": sanitize(copy.deepcopy(root["exact_match_results"])),
        "object_groups_present": present,
        "object_groups_omitted": omitted,
        "provider_routes": {
            task: APPROVED_ROUTES.get(task, "blocked-provider-unproven")
            for task in task_codes
        },
        "disclaimers": [
            "The skill did not design the content library or determine downstream suitability.",
            "Only the supported HCM Tool provider route may be used.",
            "V1 does not use HDL, HSDL, direct REST, update, merge, delete, migration, or downstream configuration.",
            "Proposal or package review is not persistence approval.",
        ],
        "requested_approval": "Authorize only local package preparation by supplying PREPARE PACKAGE <preview_fingerprint>; core.data-loader separately owns upload and initiation approval.",
        "lifecycle_status": "preview_ready",
    }
    preview = copy.deepcopy(body)
    if provider_blockers:
        # The entire validated request remains visible, but this artifact cannot
        # be approved or used as a submission receipt. Never approve a subset.
        body.update({
            "lifecycle_status": "preview_blocked",
            "provider_blockers": provider_blockers,
            "creation_authorized": False,
            "requested_approval": None,
            "safe_next_action": "Resolve the listed provider contracts for the complete set; no package or submission is authorized.",
        })
        preview = copy.deepcopy(body)
    preview["preview_fingerprint"] = canonical_sha256(body)
    return preview


def approve_preview(preview, approval_statement):
    root = require_mapping(preview, "preview")
    if root.get("lifecycle_status") != "preview_ready":
        raise PreviewContractError("only a preview_ready artifact can be approved")
    supplied = root.get("preview_fingerprint")
    body = dict(root)
    body.pop("preview_fingerprint", None)
    expected = canonical_sha256(body)
    if supplied != expected or not isinstance(supplied, str):
        raise PreviewContractError("preview fingerprint is missing or stale")
    require_supported_preview_scope(
        require_mapping(root.get("scope"), "preview.scope").get("task_codes", []),
        require_mapping(root.get("objects"), "preview.objects"),
    )
    exact_statement = "PREPARE PACKAGE %s" % supplied
    if approval_statement != exact_statement:
        raise PreviewContractError(
            "explicit approval must exactly bind the current preview fingerprint"
        )
    approved = copy.deepcopy(root)
    approved["approval"] = {
        "preview_fingerprint": supplied,
        "approval_statement": exact_statement,
    }
    approved["lifecycle_status"] = "approved"
    return approved


def record_submissions(approved_preview, receipts):
    root = require_mapping(approved_preview, "approved_preview")
    approval = require_mapping(root.get("approval"), "approved_preview.approval")
    fingerprint = root.get("preview_fingerprint")
    if approval.get("preview_fingerprint") != fingerprint:
        raise PreviewContractError("approval is not bound to the current preview")
    if approval.get("approval_statement") != "PREPARE PACKAGE %s" % fingerprint:
        raise PreviewContractError("approval statement is not exact")
    immutable_body = copy.deepcopy(root)
    immutable_body.pop("approval", None)
    immutable_body.pop("preview_fingerprint", None)
    immutable_body["lifecycle_status"] = "preview_ready"
    if canonical_sha256(immutable_body) != fingerprint:
        raise PreviewContractError("approved preview changed after approval")
    if root.get("lifecycle_status") != "approved":
        raise PreviewContractError("approved preview lifecycle status is invalid")
    require_supported_preview_scope(root["scope"]["task_codes"], root["objects"])
    receipt_list = require_list(receipts, "receipts")
    expected_tasks = set(root["scope"]["task_codes"])
    if not expected_tasks.issubset(set(APPROVED_ROUTES)):
        raise PreviewContractError("approved preview contains an unproven provider route")
    if root.get("provider_routes") != {
        task: APPROVED_ROUTES[task] for task in root["scope"]["task_codes"]
    }:
        raise PreviewContractError("approved preview provider routes are invalid")
    received_tasks = set()
    sanitized_receipts = []
    for receipt in receipt_list:
        item = require_mapping(receipt, "receipt")
        task_code = item.get("task_code")
        if task_code not in expected_tasks or task_code in received_tasks:
            raise PreviewContractError("submission receipts do not match unique preview tasks")
        if item.get("status") != "submitted":
            raise PreviewContractError("a submission receipt is not in submitted status")
        if not SHA256.fullmatch(str(item.get("package_sha256") or "")):
            raise PreviewContractError("receipt.package_sha256 must be SHA-256")
        request_id = item.get("request_id")
        if not SAFE_REQUEST_ID.fullmatch(str(request_id or "")):
            raise PreviewContractError("receipt.request_id must be a safe external identifier")
        received_tasks.add(task_code)
        sanitized_receipts.append(
            {
                "task_code": task_code,
                "package_sha256": item["package_sha256"],
                "request_id": request_id,
                "status": "submitted",
            }
        )
    if received_tasks != expected_tasks:
        raise PreviewContractError("every preview task requires one submission receipt")
    return {
        "schema_version": SCHEMA_VERSION,
        "complete_set_id": root["complete_set_id"],
        "preview_fingerprint": fingerprint,
        "lifecycle_status": "submitted_pending_verification",
        "submission_receipts": sorted(
            sanitized_receipts, key=lambda item: item["task_code"]
        ),
        "safe_next_action": "In a separate request, check each submitted process status; after success, obtain a fresh same-target readback.",
    }


def readback_comparison_rows(rows, label):
    """Exclude only source/review annotations, not values, keys or graph links.

    Local keys are retained canonical mapping identities. Unknown row fields are
    deliberately included so an unexpected persisted field cannot disappear.
    """
    return [
        {key: value for key, value in require_mapping(row, label + " record").items()
         if key not in ("source_references", "review_status")}
        for row in require_list(rows, label)
    ]


def verify_readback(approved_preview, submission, readback):
    approved = require_mapping(approved_preview, "approved_preview")
    submitted = require_mapping(submission, "submission")
    current = require_mapping(readback, "readback")
    if submitted.get("lifecycle_status") != "submitted_pending_verification":
        raise PreviewContractError("submission is not pending verification")
    if submitted.get("preview_fingerprint") != approved.get("preview_fingerprint"):
        raise PreviewContractError("submission does not belong to the approved preview")
    immutable_body = copy.deepcopy(approved)
    approval = require_mapping(immutable_body.pop("approval", None), "approved_preview.approval")
    fingerprint = immutable_body.pop("preview_fingerprint", None)
    immutable_body["lifecycle_status"] = "preview_ready"
    if approval.get("preview_fingerprint") != fingerprint or canonical_sha256(immutable_body) != fingerprint:
        raise PreviewContractError("approved preview is stale or changed")
    require_supported_preview_scope(approved["scope"]["task_codes"], approved["objects"])
    if submitted.get("complete_set_id") != approved.get("complete_set_id"):
        raise PreviewContractError("submission complete_set_id differs from the approved set")
    # Reuse the local approval and complete-receipt checks. This validates
    # retained evidence only; it does not upload or initiate a submission.
    record_submissions(approved, submitted.get("submission_receipts"))
    if current.get("target_environment_alias") != approved.get(
        "target_environment_alias"
    ):
        raise PreviewContractError("readback target differs from the approved target")
    if current.get("complete_set_id") != approved.get("complete_set_id"):
        raise PreviewContractError("readback complete_set_id differs from the approved set")
    if not SHA256.fullmatch(str(current.get("evidence_sha256") or "")):
        raise PreviewContractError("readback.evidence_sha256 must be SHA-256")
    process_statuses = require_mapping(
        current.get("process_statuses"), "readback.process_statuses"
    )
    if set(process_statuses) != set(approved["scope"]["task_codes"]):
        raise PreviewContractError("readback process statuses do not cover every task")
    if any(not isinstance(value, str) or value not in ("succeeded", "failed", "pending", "timeout")
           for value in process_statuses.values()):
        raise PreviewContractError("readback process statuses must be succeeded, failed, pending or timeout")
    if any(value != "succeeded" for value in process_statuses.values()):
        failed = "failed" in process_statuses.values()
        return {
            "schema_version": SCHEMA_VERSION,
            "complete_set_id": approved["complete_set_id"],
            "lifecycle_status": "process_failed" if failed else "readback_pending",
            "failure_class": "process_failed" if failed else (
                "process_timeout" if "timeout" in process_statuses.values() else None),
            "process_statuses": dict(process_statuses),
            "evidence_reference": sanitize(current.get("evidence_reference")),
            "evidence_sha256": current["evidence_sha256"],
            "differences": [],
            "autocorrection_attempted": False,
            "safe_next_action": (
                "Inspect the retained failed process status and ProcessLog without resubmitting automatically."
                if failed else "Recheck pending or timed-out process status without resubmitting automatically."
            ),
        }
    actual_objects = require_mapping(current.get("objects"), "readback.objects")
    if set(actual_objects) != set(OBJECT_GROUPS):
        raise PreviewContractError("readback.objects must contain exactly the 14 governed object groups")
    differences = []
    for group in OBJECT_GROUPS:
        expected_value = readback_comparison_rows(approved["objects"][group], "approved.objects." + group)
        actual_value = readback_comparison_rows(actual_objects[group], "readback.objects." + group)
        if canonical_json_bytes(expected_value) != canonical_json_bytes(actual_value):
            differences.append("objects.%s" % group)
    return {
        "schema_version": SCHEMA_VERSION,
        "complete_set_id": approved["complete_set_id"],
        "lifecycle_status": "verified" if not differences else "readback_mismatch",
        "evidence_reference": sanitize(current.get("evidence_reference")),
        "evidence_sha256": current["evidence_sha256"],
        "differences": differences,
        "autocorrection_attempted": False,
        "safe_next_action": (
            "No further action is required for this configuration set."
            if not differences
            else "Review discrepancies; V1 must not update or automatically correct them."
        ),
    }


def read_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build and verify local GROW-8154 preview and lifecycle records."
    )
    subparsers = parser.add_subparsers(dest="command")
    preview_parser = subparsers.add_parser("preview")
    preview_parser.add_argument("contract", type=Path)
    preview_parser.add_argument("--target-environment-alias", required=True)
    preview_parser.add_argument(
        "--review-blocked", action="store_true",
        help="Display all validated rows even when provider scope blocks approval; never enables execution",
    )
    report_parser = subparsers.add_parser("exact-report")
    report_parser.add_argument("contract", type=Path)
    report_parser.add_argument("--target-environment-alias", required=True)
    approve_parser = subparsers.add_parser("approve")
    approve_parser.add_argument("preview", type=Path)
    approve_parser.add_argument("--approval-statement", required=True)
    submitted_parser = subparsers.add_parser("submitted")
    submitted_parser.add_argument("approved_preview", type=Path)
    submitted_parser.add_argument("receipts", type=Path)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("approved_preview", type=Path)
    verify_parser.add_argument("submission", type=Path)
    verify_parser.add_argument("readback", type=Path)
    args = parser.parse_args(argv)
    if not args.command:
        parser.error("a command is required")
    try:
        if args.command == "exact-report":
            result = build_exact_check_report(read_json(args.contract), args.target_environment_alias)
        elif args.command == "preview":
            result = build_preview(
                read_json(args.contract), args.target_environment_alias,
                review_blocked=args.review_blocked,
            )
        elif args.command == "approve":
            result = approve_preview(
                read_json(args.preview), args.approval_statement
            )
        elif args.command == "submitted":
            result = record_submissions(
                read_json(args.approved_preview), read_json(args.receipts)
            )
        else:
            result = verify_readback(
                read_json(args.approved_preview),
                read_json(args.submission),
                read_json(args.readback),
            )
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        detail = sanitize(str(exc)) if isinstance(exc, PreviewContractError) else exc.__class__.__name__
        result = {
            "schema_version": SCHEMA_VERSION,
            "status": "blocked",
            "failure_class": "input_validation",
            "error_code": exc.__class__.__name__,
            "message": detail,
            "safe_next_action": "Correct the local input and rerun; no Fusion action was attempted.",
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    if result.get("lifecycle_status") in ("preview_blocked", "process_failed", "readback_pending", "readback_mismatch"):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
