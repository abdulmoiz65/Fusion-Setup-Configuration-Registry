#!/usr/bin/env python3
"""Offline, fail-closed evaluation of provider evidence. No Fusion/network writes."""

import argparse
import hashlib
import json
from pathlib import Path


TYPES = {"ORA_GENERAL", "ORA_PERF_GOAL"}
STAGES = {"before_questionnaire_creation", "before_association"}
SOURCES = {"target_contract", "owner_confirmation", "verified_association", "type_specific_lov"}


def goal_policy():
    contract = Path(__file__).resolve().parents[1] / "ora-resource/ora_rest_execution.json"
    return json.loads(contract.read_text())["questionnaire_selection"]["ORA_PERF_GOAL"]


def seeded_only_error(kind, stage, candidate):
    """Reject unsupported intent before collecting tenant evidence or creating data."""
    if kind != "ORA_PERF_GOAL":
        return None
    policy = goal_policy()
    code = candidate.get("code") if isinstance(candidate, dict) else None
    if stage == "before_questionnaire_creation" or (isinstance(code, str) and code.strip() and
                                                   code != policy["questionnaire_code"]):
        return {"code": "GOAL_FEEDBACK_SEEDED_QUESTIONNAIRE_REQUIRED",
                "message": policy["unsupported_message"], "status": "ineligible"}
    return None


def evaluate(data):
    """Evidence is normalized by the routed agent; this does not authenticate it."""
    errors = []

    def fail(code, message, status="unresolved"):
        errors.append({"code": code, "message": message, "status": status})

    def present(value):
        return isinstance(value, str) and bool(value.strip())

    def strings(value):
        return isinstance(value, list) and bool(value) and all(present(x) for x in value)

    if not isinstance(data, dict):
        data = {}
    kind = data.get("template_type")
    stage = data.get("stage")
    context = data.get("context")
    candidate = data.get("candidate")
    rule = data.get("association_rule")
    restriction = seeded_only_error(kind, stage, candidate)
    if restriction:
        errors.append(restriction)
    if not isinstance(kind, str) or kind not in TYPES or not isinstance(stage, str) or stage not in STAGES:
        fail("INVALID_INPUT", "Supply a supported template_type and stage.")
    if not isinstance(context, dict) or not all(
        present(context.get(k)) for k in ("base_url", "resource_version", "run_id")
    ):
        fail("INVALID_CONTEXT", "Exact target, resource version and current run are required.")
    if not isinstance(candidate, dict):
        candidate = {}
        fail("INVALID_CANDIDATE", "Supply one provider-resolved candidate or proposed design.")
    if not present(candidate.get("code")) or not present(candidate.get("subscriber_code")):
        fail("INVALID_CANDIDATE", "Portable questionnaire code and subscriber are required.")
    if not isinstance(rule, dict):
        rule = {}
        fail("ASSOCIATION_RULE_UNKNOWN", "Resolve type-specific association requirements first.")

    # Evidence provenance and freshness are mandatory even for successful history.
    for label, item in (("candidate", candidate), ("association_rule", rule)):
        if item.get("context") != context or not isinstance(context, dict):
            fail("EVIDENCE_CONTEXT_MISMATCH", label + " does not match this target/version/run.")
        if not present(item.get("source_ref")) or item.get("verified") is not True:
            fail("EVIDENCE_UNVERIFIED", label + " requires reviewed source evidence.")
        if item.get("conflicting_evidence") is not False:
            fail("CONFLICTING_OR_UNKNOWN_EVIDENCE", label + " must resolve contrary evidence.")
    if rule.get("template_type") != kind:
        fail("RULE_TYPE_MISMATCH", "Association evidence is not for the selected template type.")
    if not isinstance(rule.get("source_kind"), str) or rule["source_kind"] not in SOURCES:
        fail("RULE_SOURCE_UNKNOWN", "Use an accepted type-specific evidence source.")

    for flag in ("active", "latest", "provider_ready"):
        value = candidate.get(flag)
        if value is not True:
            fail("QUESTIONNAIRE_NOT_READY", flag + " is false or unverified.",
                 "ineligible" if value is False else "unresolved")
    subscribers = rule.get("subscriber_codes")
    if not strings(subscribers):
        fail("SUBSCRIBER_RULE_UNKNOWN", "Resolve allowed subscribers for this template type.")
    elif candidate.get("subscriber_code") not in subscribers:
        fail("SUBSCRIBER_MISMATCH", "Candidate subscriber is not eligible.", "ineligible")

    mode = rule.get("mode")
    if not isinstance(mode, str) or mode not in {"exact_questionnaire", "derived_template", "eligible_subscriber"}:
        fail("ASSOCIATION_RULE_UNKNOWN", "Association mode is not established.")
    if kind == "ORA_PERF_GOAL":
        if isinstance(mode, str) and mode in ("eligible_subscriber", "derived_template"):
            fail("GOAL_FEEDBACK_SEEDED_QUESTIONNAIRE_REQUIRED", goal_policy()["unsupported_message"], "ineligible")
        if present(candidate.get("subscriber_code")) and candidate["subscriber_code"] != goal_policy()["subscriber_code"]:
            fail("SUBSCRIBER_MISMATCH", "Resolve the seeded questionnaire under its declared subscriber.", "ineligible")
    # One accepted existing ID never establishes a general derivation rule.
    if rule.get("source_kind") in ("verified_association", "type_specific_lov") and mode != "exact_questionnaire":
        fail("RULE_OVERGENERALIZED", "Existing-reference evidence proves only exact identities.")

    if mode == "exact_questionnaire":
        ids = rule.get("questionnaire_ids")
        if not strings(ids):
            fail("ASSOCIATION_RULE_UNKNOWN", "Resolve exact allowed target questionnaire IDs.")
        elif stage == "before_questionnaire_creation":
            fail("NEW_QUESTIONNAIRE_NOT_ELIGIBLE", "Existing-association evidence does not establish new-creation support.",
                 "ineligible" if rule.get("new_questionnaire_supported") is False and
                 rule.get("source_kind") in ("target_contract", "owner_confirmation") else "unresolved")
        elif candidate.get("id") not in ids:
            # Successful history is a sample, not an exhaustive prohibition.
            exhaustive = (rule.get("exhaustive") is True and
                          rule.get("source_kind") in ("target_contract", "owner_confirmation"))
            fail("QUESTIONNAIRE_ID_MISMATCH", "Candidate is outside the evidenced identity set.",
                 "ineligible" if exhaustive else "unresolved")

    required_code = rule.get("required_questionnaire_code")
    if present(required_code) and candidate.get("code") != required_code:
        fail("QUESTIONNAIRE_CODE_MISMATCH", "The applicable product contract requires a different questionnaire code.",
             "ineligible" if rule.get("source_kind") in ("target_contract", "owner_confirmation") else "unresolved")

    # Rejections must be bound to this candidate and target, separately from
    # positive history. Never infer rejection from absence in a positive list.
    for rejection in data.get("rejections", []) if isinstance(data.get("rejections", []), list) else [{}]:
        if not isinstance(rejection, dict):
            fail("REJECTION_EVIDENCE_INVALID", "Rejection evidence must be structured.")
            continue
        if (rejection.get("context") != context or rejection.get("verified") is not True or
                not present(rejection.get("source_ref"))):
            fail("REJECTION_EVIDENCE_INVALID", "Rejection evidence needs reviewed current-context provenance.")
        elif (rejection.get("template_type") == kind and
              rejection.get("candidate_id") == candidate.get("id") and
              rejection.get("candidate_code") == candidate.get("code")):
            fail("CONFIRMED_ASSOCIATION_REJECTION", "Fusion rejected this exact candidate/type; resolve before retry.", "ineligible")

    if mode == "derived_template":
        codes = rule.get("template_codes")
        if not strings(codes):
            fail("TEMPLATE_RULE_UNKNOWN", "Resolve eligible questionnaire-template portable codes.")
        elif not present(candidate.get("template_code")):
            fail("TEMPLATE_UNKNOWN", "Candidate questionnaire-template identity is missing.")
        elif candidate["template_code"] not in codes:
            fail("QUESTIONNAIRE_TEMPLATE_MISMATCH", "Candidate derives from an ineligible template.", "ineligible")

    if stage == "before_questionnaire_creation":
        if rule.get("new_questionnaire_supported") is not True:
            fail("NEW_QUESTIONNAIRE_SUPPORT_UNPROVEN", "Custom creation needs explicit type-specific support.",
                 "ineligible" if rule.get("new_questionnaire_supported") is False and
                 rule.get("source_kind") in ("target_contract", "owner_confirmation") else "unresolved")
        if (mode == "derived_template" or candidate.get("template_required") is True) and not present(candidate.get("template_code")):
            fail("TEMPLATE_UNKNOWN", "Select a provider-validated questionnaire template before creation.")
    elif stage == "before_association" and not present(candidate.get("id")):
        fail("IDENTITY_UNKNOWN", "Association requires the current target questionnaire ID.")

    status = "eligible" if not errors else (
        "ineligible" if any(e["status"] == "ineligible" for e in errors) else "unresolved"
    )
    return {
        "status": status,
        "gate_passed": status == "eligible",
        "stage": stage,
        "template_type": kind,
        "context": context,
        "candidate_code": candidate.get("code"),
        "candidate_id": candidate.get("id"),
        "errors": errors,
        "input_sha256": hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":"),
                                                   ensure_ascii=True).encode()).hexdigest(),
        "note": "Local evidence check only; not JCS approval, vendor certification or write authorization.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Normalized evidence JSON; never credentials")
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        result = evaluate(data)
    except (OSError, ValueError, TypeError):
        result = {"status": "unresolved", "gate_passed": False,
                  "errors": [{"code": "INVALID_INPUT", "message": "Cannot read valid evidence JSON."}]}
    print(json.dumps(result, indent=2))
    return 0 if result["gate_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
