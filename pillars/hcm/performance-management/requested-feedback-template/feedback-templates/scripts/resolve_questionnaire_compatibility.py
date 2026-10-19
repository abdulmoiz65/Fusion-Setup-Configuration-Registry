#!/usr/bin/env python3
"""Resolve type-specific questionnaire evidence using the declared core client.

Offline by default. --live-read permits only provider GETs. Policy applicability
is reviewed evidence; this module cannot authenticate an owner's assertion.
"""
import argparse
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from validate_questionnaire_compatibility import evaluate, seeded_only_error, goal_policy

TASK_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = TASK_ROOT.parents[4]
LOV = "/hcmRestApi/resources/11.13.18.05/questionnairesLOV"
CONTRACT = TASK_ROOT / "ora-resource/ora_rest_execution.json"
MANDATORY_PROFILE_PREREQUISITES = [
    {
        "code": "HRA_REQUEST_FEEDBACK_ENABLED",
        "level": "SITE",
        "required_value": "Y",
        "route": "core.fusion-api.apps-common.profile-options",
    },
    {
        "code": "ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED",
        "level": "SITE",
        "required_value": "Y",
        "route": "core.fusion-api.apps-common.profile-options",
    },
]
CONDITIONAL_PROFILE_RUNBOOK_TASK = {
    "name": "Manage Administrator Profile Values",
    "task_code": "FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES",
    "offering": "Performance Management",
    "functional_area": "Performance Management Common",
    "position": "first",
    "include_when": "any_profile_not_verified_y",
    "single_task_for_all_profiles": True,
}
SUPPORTED_ALTERNATIVES = [
    "Inspect Feedback Templates through declared REST GET operations.",
    "Plan creation through REST POST or supported updates through REST PATCH, with validation and separate approval.",
    "Use CSV/workbooks or a BRD as requirements for a separately requested REST plan, not as template import data.",
    "For General Feedback, delegate new questionnaires to the Questionnaire provider; Goal Feedback uses its seeded questionnaire.",
]


def channel_guidance(spec):
    """Consume the agent's explicit channel classification; never rewrite intent."""
    channel = spec.get("requested_channel", "REST")
    require(isinstance(channel, str) and bool(channel.strip()), "INVALID_INPUT", "Classify the requested channel.")
    if channel.strip().upper() == "REST":
        return None
    return with_profile_prerequisites({
        "status": "unsupported_request", "code": "UNSUPPORTED_EXECUTION_CHANNEL",
        "message": "Feedback Template setup supports declared REST GET, POST and PATCH operations. "
                   "CSV/FSM import/export, HDL/HSDL and Data Loader execution are unsupported for this object.",
        "requested_channel": channel, "executable_tasks": [],
        "supported_alternatives": copy.deepcopy(SUPPORTED_ALTERNATIVES),
        "follow_up_questions": ["Would you like a separately requested REST configuration plan or read-only inspection?"],
        "next_action": "await_revised_request", "write_authorized": False,
    })


def business_clarification(spec):
    """Collect domain decisions only; target IDs and reference codes are provider work."""
    kind = spec.get("template_type")
    values = spec.get("business_values")
    requested = spec.get("requested_questionnaire", {})
    questions = {}
    if kind is None or kind == "":
        questions["template_type"] = "Should this be General Feedback or Performance Goal Feedback?"
    if kind == "ORA_GENERAL" and not requested:
        questions["requested_questionnaire"] = "What is the existing or proposed questionnaire name or portable code?"
    if values is not None:
        require(isinstance(values, dict) and not (set(values) - {"name", "status", "manager_types", "goal_attributes"}),
                "INVALID_INPUT", "Use supported business_values fields: name, status, manager_types and goal_attributes.")
        fields = {
            "name": "What name should the feedback template have?",
            "status": "Should the template be Active or Inactive?",
            "manager_types": "Which specific manager types should this template use?",
        }
        if kind == "ORA_PERF_GOAL":
            fields["goal_attributes"] = "Which supported performance-goal attributes should the template include?"
        for field, question in fields.items():
            value = values.get(field)
            if value is None or value == "" or value == [] or (isinstance(value, str) and not value.strip()):
                questions[field] = question
            else:
                require(isinstance(value, str) or (field in ("manager_types", "goal_attributes") and
                        isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value)),
                        "INVALID_INPUT", "Business values must be text or nonempty lists of labels.")
        if values.get("status"):
            require(values["status"] in ("A", "I", "Active", "Inactive"),
                    "INVALID_INPUT", "Status must be Active or Inactive.")
        if kind == "ORA_GENERAL" and spec.get("questionnaire_intent", "unspecified") == "unspecified":
            questions["questionnaire_intent"] = "Should I use an existing questionnaire or propose a new General Feedback questionnaire?"
    if not questions:
        return None
    return with_profile_prerequisites({
        "status": "clarification_required", "code": "MISSING_BUSINESS_INPUT",
        "message": "Provide the missing business decisions; confirmed values will be retained.",
        "missing_business_fields": list(questions), "follow_up_questions": list(questions.values()),
        "confirmed_business_values": copy.deepcopy(values or {}),
        "requested_questionnaire": copy.deepcopy(requested), "template_type": kind,
        "questionnaire_intent": spec.get("questionnaire_intent", "unspecified"),
        "next_action": "ask_user", "executable_tasks": [], "write_authorized": False,
    })


class WorkflowError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def require(condition, code, message):
    if not condition:
        raise WorkflowError(code, message)


def digest(value):
    import hashlib
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True, allow_nan=False).encode()).hexdigest()


def check_provenance(value, context, now=None):
    require(isinstance(value, dict) and value.get("context") == context and
            value.get("verified") is True and value.get("conflicting_evidence") is False and
            isinstance(value.get("source_ref"), str) and bool(value["source_ref"].strip()),
            "EVIDENCE_UNVERIFIED", "Evidence must identify its source and match the target/version/run.")
    try:
        checked = datetime.fromisoformat(value["checked_at"].replace("Z", "+00:00"))
        expires = datetime.fromisoformat(value["expires_at"].replace("Z", "+00:00"))
        current = now or datetime.now(timezone.utc)
        require(checked.tzinfo is not None and expires.tzinfo is not None and
                checked <= current < expires, "EVIDENCE_EXPIRED", "Evidence is expired or has invalid timestamps.")
    except (KeyError, TypeError, AttributeError, ValueError) as exc:
        if isinstance(exc, WorkflowError):
            raise
        raise WorkflowError("EVIDENCE_EXPIRED", "Evidence needs checked_at and expires_at UTC timestamps.") from exc


def literal(value):
    require(isinstance(value, str) and bool(value.strip()) and not any(ord(c) < 32 for c in value),
            "INVALID_INPUT", "Query keys must be nonempty strings without control characters.")
    return "'" + value.replace("'", "''") + "'"


class CoreClient:
    """Thin adapter; reuse core OAuth, host validation and one-shot transport.

    No automatic mutation retry. A missing session requires the normal Chrome
    handoff outside this helper. Tests inject a fake client; no live calls needed.
    """
    def __init__(self, base_url):
        sys.path.insert(0, str(REPO_ROOT / "core/fusion-api/rest-api-client/scripts"))
        import rest_client_common as core
        self.core = core
        import fusion_auth
        self.auth = fusion_auth
        self.props = core.read_properties(core.DEFAULT_PROPERTIES_PATH)
        require(self.props.get("restBaseUrl", "").rstrip("/") == base_url.rstrip("/"),
                "TARGET_MISMATCH", "Configured Fusion host differs from the workflow target.")
        self.token = None

    def request(self, method, path, query=None, body=None, headers=None):
        url = self.core.build_url(self.props, path, query or {})
        if self.token is None:
            self.token = self.auth.load_cached_access_token(self.props)
            require(bool(self.token), "AUTH_HANDOFF_REQUIRED", "No valid cached session; use the routed Chrome sign-in handoff.")
        try:
            raw, _, status = self.core.request_bytes(
                self.props, url, method=method, access_token=self.token,
                headers={**(headers or {}), "REST-Framework-Version": "9"},
                json_body=body, timeout=60)
        except self.auth.FusionHttpError as exc:
            if exc.status_code in (401, 403):
                code = "AUTHENTICATION_FAILED" if exc.status_code == 401 else "AUTHORIZATION_DENIED"
                raise WorkflowError(code, f"Fusion returned HTTP {exc.status_code} for the declared {method} request.") from exc
            raise
        require(200 <= status < 300, "FUSION_API", "Fusion did not accept the request.")
        return json.loads(raw) if raw else {}


def lookup(client, query):
    rows = []
    for offset in range(0, 10000, 500):
        page = client.request("GET", LOV, {"q": query, "onlyData": "true", "limit": "500", "offset": str(offset)})
        require(isinstance(page, dict) and isinstance(page.get("items"), list) and
                isinstance(page.get("hasMore"), bool), "LOOKUP_INCOMPLETE", "Questionnaire lookup is incomplete.")
        rows.extend(page["items"])
        if not page["hasMore"]:
            return rows
        require(bool(page["items"]), "LOOKUP_INCOMPLETE", "Pagination made no progress.")
    raise WorkflowError("LOOKUP_INCOMPLETE", "Questionnaire lookup exceeded its bounded page limit.")


def with_profile_prerequisites(result):
    """Attach the PM baseline to every offline requirement-planning outcome."""
    planned = copy.deepcopy(result)
    planned["mandatory_profile_prerequisites"] = copy.deepcopy(MANDATORY_PROFILE_PREREQUISITES)
    planned["conditional_starting_runbook_task"] = copy.deepcopy(CONDITIONAL_PROFILE_RUNBOOK_TASK)
    return planned


def plan_requirements(spec):
    """Offline intake decision; no target identity, credentials or provider calls."""
    kind = spec.get("template_type")
    intent = spec.get("questionnaire_intent", "unspecified")
    requested = spec.get("requested_questionnaire", {})
    rejected = channel_guidance(spec)
    if rejected is not None:
        return rejected
    require(kind in (None, "", "ORA_GENERAL", "ORA_PERF_GOAL") and
            intent in ("unspecified", "existing", "create") and isinstance(requested, dict),
            "INVALID_INPUT", "Use General Feedback (ORA_GENERAL) or Performance Goal Feedback (ORA_PERF_GOAL), "
            "with questionnaire intent unspecified, existing or create.")
    require(all(isinstance(v, str) and bool(v.strip()) for v in requested.values()) and
            not (set(requested) - {"name", "code"}), "INVALID_INPUT", "Questionnaire name/code must be nonempty text.")
    if kind in (None, ""):
        return business_clarification(spec)
    policy = json.loads(CONTRACT.read_text())["questionnaire_selection"][kind]
    if kind == "ORA_PERF_GOAL":
        matches_seed = (requested.get("code") == policy["questionnaire_code"] if "code" in requested else
                        requested.get("name", policy["questionnaire_name"]) == policy["questionnaire_name"])
        if intent == "create" or not matches_seed:
            return with_profile_prerequisites({
                "status": "unsupported_request", "template_type": kind,
                "code": "GOAL_FEEDBACK_SEEDED_QUESTIONNAIRE_REQUIRED",
                "message": policy["unsupported_message"], "executable_tasks": [],
                "recommended_runbook_disposition": "not-applicable",
                "requested_questionnaire": requested,
                "supported_alternatives": [policy["unsupported_message"]],
                "follow_up_questions": ["Would you like to use the seeded Performance Goal Feedback questionnaire, or request a separate General Feedback plan?"],
                "next_action": "await_revised_request", "write_authorized": False,
            })
        clarification = business_clarification(spec)
        if clarification is not None:
            return clarification
        return with_profile_prerequisites({
            "status": "requirements_ready", "template_type": kind,
            "questionnaire_selection": {"name": policy["questionnaire_name"], "code": policy["questionnaire_code"]},
            "executable_tasks": ["resolve_seeded_questionnaire", "validate_feedback_template", "preview_template_write", "verify_template"],
            "questionnaire_creation_allowed": False,
        })
    clarification = business_clarification(spec)
    if clarification is not None:
        return clarification
    return with_profile_prerequisites({
        "status": "requirements_ready", "template_type": kind, "requested_questionnaire": requested,
        "questionnaire_creation_allowed": intent == "create",
        "executable_tasks": (["create_questionnaire_through_provider", "verify_questionnaire"] if intent == "create" else
                             ["resolve_existing_questionnaire"]) +
                            ["validate_feedback_template", "preview_template_write", "verify_template"],
    })


def resolve(spec, client=None, now=None):
    """Return validator input/output; failed resolution never creates data."""
    context = spec.get("context")
    require(isinstance(context, dict) and all(isinstance(context.get(k), str) and context[k]
            for k in ("base_url", "resource_version", "run_id")), "INVALID_CONTEXT", "Target/version/run are required.")
    kind, stage = spec.get("template_type"), spec.get("stage")
    require(kind in ("ORA_GENERAL", "ORA_PERF_GOAL") and
            stage in ("before_questionnaire_creation", "before_association"), "INVALID_INPUT", "Unknown type or stage.")
    restriction = seeded_only_error(kind, stage, spec.get("candidate"))
    if restriction:
        return {"evidence": {"context": context, "template_type": kind, "stage": stage,
                             "candidate": copy.deepcopy(spec.get("candidate", {}))},
                "compatibility": {"status": "ineligible", "gate_passed": False, "errors": [restriction],
                                  "input_sha256": digest(spec)},
                "selection_query": None, "policy_id": goal_policy()["policy_id"]}
    binding = spec.get("policy_evidence")
    if binding is None and kind == "ORA_GENERAL":
        binding = provider_policy_evidence(spec, now)
    check_provenance(binding, context, now)
    contract = json.loads(CONTRACT.read_text())
    policy = contract["questionnaire_selection"][kind]
    require(binding.get("policy_id") == policy["policy_id"], "POLICY_MISMATCH", "Review the applicable product policy for this target.")
    candidate = copy.deepcopy(spec.get("candidate", {}))
    check_provenance(candidate, context, now)
    require(candidate.get("subscriber_code") == policy["subscriber_code"],
            "SUBSCRIBER_MISMATCH", "Candidate subscriber differs from the selected product policy.")
    # CoreClient uses REST framework version 9: combine predicates with "and".
    # Semicolon filters use legacy syntax and return HTTP 400 under version 9.
    query = "SubscriberCode=" + literal(policy["subscriber_code"]) + " and Status='A' and LatestVersion='Y'"
    if policy["selection"] == "fixed_code":
        query += " and QuestionnaireCode=" + literal(policy["questionnaire_code"])
    elif stage == "before_association":
        query += " and QuestionnaireCode=" + literal(candidate.get("code"))
    else:
        # New general questionnaires need provider design checks, not a lookup
        # pretending the proposed identity already exists.
        query = None
    rows = []
    if query:
        if client is not None:
            rows = lookup(client, query)
        else:
            snapshot = spec.get("lookup_evidence")
            check_provenance(snapshot, context, now)
            require(snapshot.get("path") == LOV and snapshot.get("query") == query and
                    snapshot.get("complete") is True and isinstance(snapshot.get("items"), list),
                    "LOOKUP_INCOMPLETE", "Supply the exact complete provider query result or use --live-read.")
            rows = snapshot["items"]
        if kind == "ORA_PERF_GOAL" and not rows:
            raise WorkflowError("SEEDED_QUESTIONNAIRE_MISSING", "The required seeded questionnaire is unavailable. Resolve the prerequisite; do not create a replacement.")
        require(len(rows) == 1, "IDENTITY_AMBIGUOUS", "Expected one active/latest questionnaire under the type-specific selection.")
        row = rows[0]
        expected_code = policy.get("questionnaire_code", candidate.get("code"))
        require(isinstance(row, dict) and row.get("SubscriberCode") == policy["subscriber_code"] and
                row.get("Status") == "A" and row.get("LatestVersion") == "Y" and
                row.get("QuestionnaireCode") == expected_code and bool(row.get("QuestionnaireId")),
                "LOOKUP_CONFLICT", "Returned identity does not satisfy the declared selection.")
        if candidate.get("code") == row["QuestionnaireCode"] and stage == "before_association":
            require(str(candidate.get("id")) == str(row["QuestionnaireId"]),
                    "IDENTITY_CHANGED", "Candidate identity changed since provider verification.")
            candidate.update(active=True, latest=True)
    rule = {**binding, "template_type": kind, "source_kind": "target_contract",
            "subscriber_codes": [policy["subscriber_code"]],
            "new_questionnaire_supported": policy["new_questionnaire_supported"]}
    if policy["selection"] == "fixed_code":
        rule.update(mode="exact_questionnaire", exhaustive=True,
                    required_questionnaire_code=policy["questionnaire_code"],
                    questionnaire_ids=[str(rows[0]["QuestionnaireId"])])
    else:
        rule.update(mode="eligible_subscriber")
    data = {"context": context, "template_type": kind, "stage": stage,
            "candidate": candidate, "association_rule": rule, "rejections": spec.get("rejections", [])}
    return {"evidence": data, "compatibility": evaluate(data), "selection_query": query,
            "policy_id": policy["policy_id"]}


def provider_policy_evidence(spec, now=None):
    """Bind the declared General policy to actual current provider validation.

    A new identity has no association history. Its supported design and tenant
    references are checked by the provider; an existing identity additionally
    requires the association-stage LOV/readback. This is not write approval.
    """
    context = spec.get("context")
    receipt = spec.get("provider_validation")
    check_provenance(receipt, context, now)
    require(receipt.get("provider") == "hcm.hcm-tool.questionnaire.questionnaires" and
            receipt.get("subscriber_code") == "HRA" and
            receipt.get("candidate_code") == spec.get("candidate", {}).get("code"),
            "PROVIDER_IDENTITY_MISMATCH", "Provider validation must identify this HRA questionnaire.")
    required = ("subscriber", "schema", "references", "design", "lifecycle", "identity")
    require(all(receipt.get("checks", {}).get(k) is True for k in required),
            "PROVIDER_VALIDATION_INCOMPLETE", "Complete current provider checks before applying the General policy.")
    if spec.get("stage") == "before_questionnaire_creation":
        require(receipt.get("specification_sha256") == digest(spec.get("provider_specification")) and
                isinstance(spec.get("provider_specification"), dict),
                "PROVIDER_DESIGN_CHANGED", "Provider receipt must bind the proposed design.")
    require(receipt.get("restrictions_resolved") is True,
            "PROVIDER_RESTRICTIONS_UNRESOLVED", "Resolve current subscriber/template restrictions and contrary evidence.")
    policy = json.loads(CONTRACT.read_text())["questionnaire_selection"]["ORA_GENERAL"]
    return {**receipt, "policy_id": policy["policy_id"],
            "source_ref": str(CONTRACT) + "#questionnaire_selection/ORA_GENERAL; " + receipt["source_ref"]}


MANAGER_LOV = "/fscmRestApi/resources/11.13.18.05/commonLookupsLOV"


def resolve_manager_selection(selection, client):
    """All is a payload sentinel; specific types are current exact LOV matches."""
    values = [selection] if isinstance(selection, str) else selection
    require(isinstance(values, list) and bool(values) and
            all(isinstance(v, str) and v.strip() for v in values),
            "INVALID_MANAGER_SELECTION", "Supply All or specific manager names/codes.")
    if any(v.strip().upper() == "ALL" for v in values):
        require(len(values) == 1, "INVALID_MANAGER_SELECTION", "All cannot be mixed with specific types.")
        return {"value": "ALL", "basis": "declared_all_sentinel", "matches": []}
    rows = []
    for offset in range(0, 10000, 500):
        page = client.request("GET", MANAGER_LOV, {
            "fields": "LookupCode,Meaning", "finder": "LookupTypeFinder;LookupType=PER_SUPERVISOR_TYPE",
            "onlyData": "true", "limit": "500", "offset": str(offset)})
        require(isinstance(page, dict) and isinstance(page.get("items"), list) and
                isinstance(page.get("hasMore"), bool), "LOOKUP_INCOMPLETE", "Manager lookup is incomplete.")
        rows.extend(page["items"])
        if not page["hasMore"]:
            break
        require(bool(page["items"]), "LOOKUP_INCOMPLETE", "Manager pagination made no progress.")
    else:
        raise WorkflowError("LOOKUP_INCOMPLETE", "Manager lookup exceeded its bounded page limit.")
    matches = []
    for value in values:
        found = [r for r in rows if isinstance(r, dict) and
                 value.strip().casefold() in (str(r.get("LookupCode", "")).casefold(),
                                              str(r.get("Meaning", "")).casefold())]
        require(len(found) == 1 and bool(found[0].get("LookupCode")),
                "MANAGER_IDENTITY_UNRESOLVED", "Specific manager type must resolve exactly once: " + value)
        require(found[0]["LookupCode"] not in [r["LookupCode"] for r in matches],
                "INVALID_MANAGER_SELECTION", "Duplicate manager selection.")
        matches.append(found[0])
    return {"value": ",".join(r["LookupCode"] for r in matches), "basis": "current_exact_lov", "matches": matches}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--live-read", action="store_true", help="Use declared provider GETs through core; never writes.")
    args = parser.parse_args()
    try:
        spec = json.loads(args.input.read_text())
        result = resolve(spec, CoreClient(spec["context"]["base_url"]) if args.live_read else None)
    except Exception as exc:
        result = {"compatibility": {"status": "unresolved", "gate_passed": False},
                  "errors": [{"code": getattr(exc, "code", "RESOLUTION_FAILED"),
                              "message": str(exc) if isinstance(exc, WorkflowError) else "Resolution failed; inspect sanitized provider diagnostics."}]}
    print(json.dumps(result, indent=2))
    return 0 if result["compatibility"]["gate_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
