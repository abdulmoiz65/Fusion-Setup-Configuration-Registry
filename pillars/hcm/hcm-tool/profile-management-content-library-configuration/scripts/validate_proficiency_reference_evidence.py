#!/usr/bin/env python3
"""Validate sanitized, routed proficiency reference evidence locally (no writes).

Reference success does not promote the unresolved description field/provider
mapping. This helper never fetches evidence or authorizes a package.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from build_profile_content_library_preview import contains_sensitive, canonical_sha256


def _timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("reference timestamps require an explicit timezone")
    return parsed


def validate(intake, evidence, target, as_of):
    """Compare exact supplied model/level and item binding, without inference."""
    if contains_sensitive(intake) or contains_sensitive(evidence):
        raise ValueError("sensitive material is not permitted in reference evidence")
    if not isinstance(target, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", target):
        raise ValueError("a safe target alias is required")
    required = {"schema_version", "target_environment_alias", "source_fingerprint", "intake_fingerprint",
                "captured_at", "valid_through", "complete", "evidence_references",
                "models", "item_model_bindings"}
    if not isinstance(evidence, dict) or set(evidence) != required:
        raise ValueError("reference evidence does not match the declared contract")
    if evidence["schema_version"] != "1.0" or evidence["complete"] is not True:
        raise ValueError("complete schema 1.0 reference evidence is required")
    fingerprint = evidence["source_fingerprint"]
    if not isinstance(fingerprint, str) or not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
        raise ValueError("a source fingerprint is required")
    if fingerprint != intake.get("source_fingerprint") or evidence["target_environment_alias"] != target:
        raise ValueError("reference evidence source/target binding differs from the request")
    if evidence["intake_fingerprint"] != canonical_sha256(intake):
        raise ValueError("normalized intake changed after reference evidence was bound")
    if not _timestamp(evidence["captured_at"]) <= _timestamp(as_of) <= _timestamp(evidence["valid_through"]):
        raise ValueError("reference evidence is stale or not yet valid")
    references = evidence["evidence_references"]
    if not isinstance(references, list) or not references or any(
        not isinstance(ref, str) or not ref.strip() for ref in references
    ):
        raise ValueError("routed source evidence references are required")
    models = evidence["models"]
    bindings = evidence["item_model_bindings"]
    if not isinstance(models, list) or not isinstance(bindings, list):
        raise ValueError("models and item_model_bindings must be arrays")
    for model in models:
        if not isinstance(model, dict) or set(model) != {"code", "level_codes"}:
            raise ValueError("each model requires code and level_codes")
        if not isinstance(model["code"], str) or not model["code"]:
            raise ValueError("model code must be nonblank")
        levels = model["level_codes"]
        if not isinstance(levels, list) or not levels or any(not isinstance(x, str) or not x for x in levels):
            raise ValueError("level codes must be nonblank strings")
        if len(levels) != len(set(levels)):
            raise ValueError("duplicate model level identities")
    for binding in bindings:
        if not isinstance(binding, dict) or set(binding) != {"item_reference", "model_code", "evidence_reference"}:
            raise ValueError("each item-model binding requires its exact identities and source reference")
        if any(not isinstance(value, str) or not value for value in binding.values()):
            raise ValueError("item-model binding values must be nonblank strings")
        if binding["evidence_reference"] not in references:
            raise ValueError("item-model applicability has no declared source reference")
    records = intake.get("records")
    if not isinstance(records, list) or intake.get("unmapped_records") or intake.get("errors"):
        raise ValueError("correct intake errors and mappings before reference validation")
    if intake.get("source_record_count") != len(records):
        raise ValueError("reference validation requires the complete intake row set")
    items = {}
    for record in records:
        if record["record_type"] == "content_item":
            items.setdefault(record["values"]["local_key"], []).append(record["values"])
    results = []
    for record in records:
        if record["record_type"] != "content_item_proficiency_description":
            continue
        values = record["values"]
        item_reference = values["parent_local_key"] or values["parent_exact_reference"]
        matches = [b for b in bindings if b["item_reference"] == item_reference]
        issues = []
        if len(matches) != 1:
            issues.append("An exact, unambiguous item-to-model applicability binding is required.")
        else:
            model_code = matches[0]["model_code"]
            if values["parent_local_key"]:
                parents = items.get(item_reference, [])
                if len(parents) != 1 or parents[0]["rating_model_code"] != model_code:
                    issues.append("The supplied parent model differs from the applicable model evidence.")
            model_matches = [model for model in models if model["code"] == model_code]
            if len(model_matches) != 1:
                issues.append("The exact existing rating model is missing or ambiguous.")
            elif values["rating_level_code"] not in model_matches[0]["level_codes"]:
                issues.append("The supplied rating_level_code does not exist in that exact model.")
        results.append({"object_reference": values["local_key"], "source": record["source"],
                        "status": "blocked" if issues else "references_verified", "issues": issues})
    body = {"schema_version": "1.0", "target_environment_alias": target,
            "source_fingerprint": fingerprint, "intake_fingerprint": evidence["intake_fingerprint"],
            "evidence_fingerprint": canonical_sha256(evidence),
            "status": "blocked" if any(row["issues"] for row in results) else "references_verified",
            "results": results, "creation_authorized": False,
            "field_mapping_status": "blocked_provider_mapping_unproven"}
    body["report_fingerprint"] = canonical_sha256(body)
    return body


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("intake", type=Path)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--target-environment-alias", required=True)
    parser.add_argument("--as-of", required=True)
    args = parser.parse_args(argv)
    try:
        result = validate(json.loads(args.intake.read_text()), json.loads(args.evidence.read_text()),
                          args.target_environment_alias, args.as_of)
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        # Do not echo caller-controlled exceptions or raw source values.
        result = {"status": "blocked", "failure_class": "input_validation",
                  "message": "Invalid, incomplete, sensitive or unbound reference input; correct the local evidence.",
                  "creation_authorized": False}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result["status"] == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
