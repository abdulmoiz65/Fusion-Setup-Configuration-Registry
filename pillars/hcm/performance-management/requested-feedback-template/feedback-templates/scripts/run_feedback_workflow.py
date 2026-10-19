#!/usr/bin/env python3
"""Request Feedback task entry point: provider handoff, preview, one approved write.

Default/dry-run is offline. --live-read adds declared GETs. --execute requires a
saved preview, matching approval and an unused attempt file; no automatic retry.
Questionnaire loads remain exclusively owned by the Questionnaire/Data Loader
workflow. This wrapper never submits questionnaire CRUD or an HDL load.
"""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, unquote

from resolve_questionnaire_compatibility import (
    CONTRACT, CoreClient, WorkflowError, check_provenance, digest, literal, require, resolve, plan_requirements, channel_guidance, resolve_manager_selection,
)

PROVIDER = "hcm.hcm-tool.questionnaire.questionnaires"
CHECKS = ("inputs", "identity", "authenticated_access", "catalog", "manager_type",
          "route_capability", "artifact_paths", "lifecycle")


def component_scope(provider_spec):
    """Describe requested content only; this is not a target HDL schema."""
    components = {"Questionnaire"}
    types = set()
    for record in provider_spec["records"]:
        if record.get("attachments"):
            components.add("QuestionnaireAttachment")
        for section in record.get("sections", []):
            components.add("Section")
            for question in section.get("questions", []):
                components.add("Question")
                mode = question.get("mode")
                require(mode in ("direct", "direct-text", "reference"),
                        "PROVIDER_DESIGN_INCOMPLETE", "Question mode must identify direct content or a reference.")
                if mode in ("direct", "direct-text"):
                    kind = question.get("attributes", {}).get("QuestionType")
                    require(kind in ("TEXT", "1CHOICE", "MULTCHOICE", "NONE") and
                            (mode != "direct-text" or kind == "TEXT"),
                            "PROVIDER_DESIGN_INCOMPLETE", "Resolve the direct QuestionType before handoff.")
                    require(kind not in ("TEXT", "NONE") or not question.get("answers"),
                            "PROVIDER_DESIGN_INCOMPLETE", "TEXT and NONE questions cannot contain Answer rows.")
                    types.add(kind)
                if question.get("answers"):
                    components.add("Answer")
    return {"components": [name for name in ("Questionnaire", "QuestionnaireAttachment", "Section", "Question", "Answer")
                           if name in components],
            "direct_question_types": sorted(types),
            "attachments_requested": "QuestionnaireAttachment" in components,
            "answers_requested": "Answer" in components,
            "translations_requested": bool(provider_spec.get("translations"))}


def payload_digest(payload):
    """RFC 8785 for this contract's flat ASCII-key, string/boolean-only body.

    Reject numbers, containers, non-ASCII keys and invalid Unicode rather than
    pretending Python's generic JSON serializer implements all of JCS.
    """
    require(isinstance(payload, dict) and bool(payload), "INVALID_PAYLOAD", "Payload must be a nonempty object.")
    require(all(isinstance(k, str) and k.isascii() and isinstance(v, (str, bool))
                for k, v in payload.items()), "INVALID_PAYLOAD", "Only flat contract strings/booleans are supported.")
    try:
        raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    except UnicodeError as exc:
        raise WorkflowError("INVALID_PAYLOAD", "Invalid Unicode in payload.") from exc
    return hashlib.sha256(raw).hexdigest()


def canonical_path(row, base_url, collection):
    links = row.get("@context", {}).get("links", row.get("links", []))
    urls = [x.get("href") for x in links if x.get("rel") == "canonical"]
    require(len(urls) == 1 and isinstance(urls[0], str), "CANONICAL_PATH_MISSING", "Expected one fresh canonical item link.")
    url = urlsplit(urls[0])
    base = urlsplit(base_url)
    path = url.path
    require((not url.netloc or (url.scheme == "https" and url.hostname == base.hostname and
            (url.port or 443) == (base.port or 443) and not url.username and not url.password)) and
            not url.query and not url.fragment and path.startswith(collection + "/") and
            "/" not in unquote(path[len(collection) + 1:]) and
            unquote(path[len(collection) + 1:]) not in ("", ".", ".."),
            "CANONICAL_PATH_INVALID", "Canonical item link must belong to the approved collection and host.")
    return path


def strong_etag_header(value):
    """ADF context may expose the opaque token without HTTP entity-tag quotes."""
    require(isinstance(value, str) and bool(value) and not value.startswith("W/"),
            "INVALID_ETAG", "If-Match requires a nonempty strong ETag.")
    opaque = value[1:-1] if value.startswith('"') and value.endswith('"') else value
    require(bool(opaque) and all(0x21 <= ord(c) <= 0x7e and c != '"' for c in opaque),
            "INVALID_ETAG", "ETag contains an unsupported character or malformed quotation.")
    return '"' + opaque + '"'


def plan(spec, client=None, now=None, manager_snapshot=None):
    """Recompute association compatibility or bind an ordinary update to current state."""
    spec = copy.deepcopy(spec)
    action = spec.get("action")
    rejected = channel_guidance(spec)
    if rejected is not None:
        return rejected
    if action == "plan_requirements":
        require(client is None, "INVALID_OPTIONS", "Requirement planning is offline; no live client is permitted.")
        return plan_requirements(spec)
    require(action in ("questionnaire_handoff", "associate", "update_template"),
            "INVALID_ACTION", "Select provider handoff, association or ordinary template update.")
    ordinary_update = action == "update_template"
    expected_stage = ("before_template_update" if ordinary_update else
                      "before_questionnaire_creation" if action == "questionnaire_handoff" else "before_association")
    require(spec.get("stage") == expected_stage, "STAGE_MISMATCH", "Compatibility stage must match the requested operation.")
    outcome = spec.get("provider_outcome")
    if action == "associate" and (spec.get("questionnaire_intent") == "create" or outcome is not None):
        check_provenance(outcome, spec.get("context"), now)
        require(outcome.get("provider") == PROVIDER and
                outcome.get("candidate_code") == spec.get("candidate", {}).get("code"),
                "PROVIDER_IDENTITY_MISMATCH", "Provider outcome must identify the requested questionnaire.")
        if outcome.get("status") != "verified":
            return {"status": "blocked", "action": action, "resolution_outcome": "SKILL_LIMITATION",
                    "provider_outcome": outcome,
                    "errors": [{"code": "QUESTIONNAIRE_PROVIDER_NOT_VERIFIED",
                                "message": "Resolve the provider result before association; tenant repair is not established."}],
                    "milestones": {"questionnaire_creation": "not_verified", "content_verification": "not_verified",
                                   "association": "not_started", "association_readback": "not_verified"}}
    if ordinary_update:
        context = spec.get("context")
        require(isinstance(context, dict) and all(isinstance(context.get(k), str) and context[k]
                for k in ("base_url", "resource_version", "run_id")), "INVALID_CONTEXT", "Target/version/run are required.")
        preflight = spec.get("preflight")
        check_provenance(preflight, context, now)
        current = preflight.get("current_template", {})
        require(isinstance(current, dict) and current.get("TemplateType") in ("ORA_GENERAL", "ORA_PERF_GOAL") and
                current.get("TemplateType") == spec.get("template_type"),
                "REQUEST_BINDING_MISMATCH", "Ordinary updates must preserve the current template type.")
        require(spec.get("operation") == "patch_feedback_template", "UNSUPPORTED_OPERATION", "Ordinary update requires PATCH.")
        payload = spec.get("payload")
        require(isinstance(payload, dict) and not ({"QuestionnaireId", "TemplateType"} & set(payload)),
                "ASSOCIATION_ACTION_REQUIRED", "Questionnaire/type changes require the associate action and its compatibility gate.")
        candidate = {"id": current.get("QuestionnaireId")}
        resolution = None
    else:
        resolution = resolve(spec, client, now)
    result = {"status": "blocked", "action": action, "resolution": resolution,
              "milestones": {"questionnaire_creation": "not_started", "content_verification": "not_verified",
                             "association": "not_started", "association_readback": "not_verified"}}
    if not ordinary_update and not resolution["compatibility"]["gate_passed"]:
        return result
    if ordinary_update:
        # No compatibility pass is claimed for an unchanged questionnaire.
        result.pop("resolution")
        result["milestones"].update(questionnaire_creation="not_changed", content_verification="not_required",
                                    association="not_changed", association_readback="not_required",
                                    template_update="not_started", template_update_readback="not_verified")
    if not ordinary_update:
        candidate = resolution["evidence"]["candidate"]
        if spec.get("questionnaire_intent") == "existing":
            result["milestones"]["content_verification"] = "not_required"
    context = spec["context"]
    if action == "questionnaire_handoff":
        provider_spec = spec.get("provider_specification")
        require(isinstance(provider_spec, dict) and provider_spec.get("intent") == "create" and
                provider_spec.get("task") == "questionnaires" and provider_spec.get("operation") == "MERGE",
                "PROVIDER_INTENT_MISMATCH", "The existing provider supports a create-only Questionnaire handoff.")
        records = provider_spec.get("records", [])
        require(isinstance(records, list) and len(records) == 1, "PROVIDER_IDENTITY_MISMATCH", "One candidate per handoff is required.")
        header = records[0].get("attributes", {})
        require(header.get("QuestionnaireCode") == candidate.get("code") and
                header.get("QuestionnaireName") == candidate.get("name") and
                isinstance(candidate.get("subscriber_name"), str) and
                header.get("SubscriberName") == candidate["subscriber_name"] and
                str(header.get("QstnrVersionNum")) == str(candidate.get("version")) and
                header.get("Status") == "A" and
                header.get("TemplateQstnrCode") == candidate.get("template_code"),
                "PROVIDER_IDENTITY_MISMATCH", "Provider identity/template/status differ from the validated design.")
        require(candidate.get("provider_specification_sha256") == digest(provider_spec),
                "PROVIDER_DESIGN_CHANGED", "Provider design differs from the reviewed specification.")
        task_context = spec.get("questionnaire_task_context")
        check_provenance(task_context, context, now)
        tasks = task_context.get("task_codes", [])
        require(task_context.get("questionnaire_intent") == "create" and
                isinstance(tasks, list) and tasks.count("HRT_MANAGE_QUESTIONNAIRES") == 1 and
                tasks.count("ORA_HRA_FEEDBACK_TEMPLATES") == 1 and
                tasks.index("HRT_MANAGE_QUESTIONNAIRES") < tasks.index("ORA_HRA_FEEDBACK_TEMPLATES"),
                "QUESTIONNAIRE_TASK_MAPPING_REQUIRED", "Refresh the create scope and map Questionnaires before Feedback Templates.")
        scope = component_scope(provider_spec)
        require(spec.get("requested_component_scope") == scope, "PROVIDER_COMPONENT_SCOPE_MISMATCH",
                "Requested component scope must match the preserved provider design.")
        result.update(status="handoff_ready", handoff={
            "provider": PROVIDER, "context": context, "template_type": spec["template_type"],
            "provider_specification": provider_spec, "specification_sha256": digest(provider_spec),
            "requested_component_scope": scope, "questionnaire_task_context": task_context,
            "readiness": {"consumer_compatibility": "passed", "provider_validation": "pending",
                          "import_validation": "pending", "creation": "not_started"},
            "compatibility_input_sha256": resolution["compatibility"]["input_sha256"],
            "approval_scope": "Provider validation only; Data Loader preview and approval remain required."})
        return result

    contract = json.loads(CONTRACT.read_text())
    preflight = spec.get("preflight")
    check_provenance(preflight, context, now)
    if "manager_selection" in spec:
        manager_client = client
        if client is None and manager_snapshot is not None:
            # Offline approval binding replays only the already reviewed matches.
            # execute() repeats the complete live lookup before any write.
            class ApprovedManagerSnapshot:
                def request(self, method, path, query):
                    require(method == "GET" and isinstance(manager_snapshot.get("matches"), list),
                            "LOOKUP_INCOMPLETE", "Approved manager snapshot is incomplete.")
                    return {"items": manager_snapshot["matches"], "hasMore": False}
            manager_client = ApprovedManagerSnapshot()
        managers = resolve_manager_selection(spec["manager_selection"], manager_client)
        require(spec.get("payload", {}).get("ShareWithManagers") == managers["value"],
                "MANAGER_PAYLOAD_MISMATCH", "Payload must match the resolved manager selection.")
        preflight.setdefault("checks", {})["manager_type"] = True
        result["manager_resolution"] = managers
    require(all(preflight.get("checks", {}).get(k) is True for k in CHECKS),
            "PREFLIGHT_INCOMPLETE", "Complete task validation, authenticated target read, and route-capability checks first.")
    operation = spec.get("operation")
    require(operation in ("create_general_feedback_template", "create_performance_goal_feedback_template", "patch_feedback_template"),
            "UNSUPPORTED_OPERATION", "Only declared POST/PATCH association operations are supported.")
    operation_contract = contract["operations"][operation]
    require(operation_contract.get("enabled") is True, "UNSUPPORTED_OPERATION", "Operation is disabled.")
    payload = spec.get("payload")
    body_hash = payload_digest(payload)
    fields = operation_contract["payload_fields"]
    require(not (set(payload) - set(fields)), "INVALID_PAYLOAD", "Payload contains undeclared fields.")
    for name, field in fields.items():
        value = payload.get(name)
        require(not field.get("required") or name in payload, "INVALID_PAYLOAD", "Missing required payload field: " + name)
        if name in payload:
            require(isinstance(value, str) if field["type"] == "string" else isinstance(value, bool),
                    "INVALID_PAYLOAD", "Incorrect field type: " + name)
            require("enum" not in field or value in field["enum"], "INVALID_PAYLOAD", "Invalid field value: " + name)
            require(name == "Comments" or bool(value.strip()) if isinstance(value, str) else True,
                    "INVALID_PAYLOAD", "Blank field: " + name)
    collection = contract["operations"]["list_templates"]["path"]
    require(preflight.get("collection_path") == collection, "ROUTE_MISMATCH", "Preflight must cover the declared route.")
    current = preflight.get("current_template", {})
    method = operation_contract["method"]
    headers = {}
    if method == "PATCH":
        require(isinstance(current, dict) and isinstance(current.get("InUseFlag"), bool) and
                (ordinary_update or current.get("InUseFlag") is False) and
                current.get("StatusCode") in ("A", "I") and
                all(current.get(k) is not None for k in contract["operations"]["get_template_by_exact_name"]["response_requirements"]["required_fields"]),
                "LIFECYCLE_BLOCKED", "Resolve complete current template state; association changes require a confirmed unused template.")
        if ordinary_update:
            require(not current["InUseFlag"] or set(payload) <= {"Name", "Comments"},
                    "LIFECYCLE_BLOCKED", "Only name or description may change while the template is in use.")
            require(spec["template_type"] == "ORA_PERF_GOAL" or "GoalAttributeList" not in payload,
                    "INVALID_PAYLOAD", "Goal attributes apply only to Performance Goal Feedback.")
        require(ordinary_update or "QuestionnaireId" in payload or "TemplateType" in payload,
                "UNSUPPORTED_OPERATION", "This wrapper handles association changes; use the existing route for unrelated edits.")
        path = canonical_path(current, context["base_url"], collection)
        etag = current.get("@context", {}).get("headers", {}).get("ETag")
        if etag:
            headers["If-Match"] = strong_etag_header(etag)
        require(any(current.get(k) != v for k, v in payload.items()), "NO_CHANGE", "The requested values already match.")
    else:
        require(preflight.get("name_available") is True, "IDENTITY_CONFLICT", "Create name has not been proved available.")
        path = collection
    require(isinstance(spec.get("attempt_file"), str) and Path(spec["attempt_file"]).is_absolute(),
            "ATTEMPT_PATH_REQUIRED", "Bind an absolute project attempt-file path into the preview.")
    effective_type = payload.get("TemplateType", current.get("TemplateType"))
    effective_id = payload.get("QuestionnaireId", current.get("QuestionnaireId"))
    require(effective_type == spec["template_type"] and str(effective_id) == str(candidate.get("id")),
            "REQUEST_BINDING_MISMATCH", "Actual outgoing questionnaire/type differ from compatibility evidence.")
    if effective_type == "ORA_PERF_GOAL":
        attrs = payload.get("GoalAttributeList", current.get("GoalAttributeList"))
        require(isinstance(attrs, str) and bool(attrs.strip()),
                "GOAL_ATTRIBUTES_UNKNOWN", "Resolve source-mapped goal attributes before approval.")
    if effective_type == "ORA_PERF_GOAL" and payload.get("StatusCode") == "A":
        require(preflight.get("goal_activation_impact_reviewed") is True,
                "ACTIVATION_IMPACT_UNKNOWN", "Goal activation requires the existing impact review.")
    request = {"target_environment_alias": preflight.get("target_environment_alias"),
               "resolved_base_url": context["base_url"], "method": method,
               "relative_path": path, "query": {}, "conditional_headers": headers,
               "payload": payload, "canonical_payload_sha256": body_hash}
    require(isinstance(request["target_environment_alias"], str) and request["target_environment_alias"],
            "INVALID_CONTEXT", "Target environment alias is required.")
    result.update(status="approval_required", request=request,
                  preview_sha256=digest({"specification": spec, "request": request}))
    if not ordinary_update:
        result["milestones"]["questionnaire_creation"] = "existing_identity_verified"
    content = spec.get("content_verification") if not ordinary_update else None
    if content:
        check_provenance(content, context, now)
        require(content.get("candidate_id") == candidate.get("id") and
                content.get("candidate_code") == candidate.get("code") and
                content.get("matches_requested_content") is True and
                isinstance(content.get("expected_content_sha256"), str) and
                re.fullmatch(r"[0-9a-f]{64}", content["expected_content_sha256"]) is not None and
                content["expected_content_sha256"] == content.get("observed_content_sha256"),
                "CONTENT_MISMATCH", "Question content readback does not verify the requested candidate/design.")
        result["milestones"]["content_verification"] = "verified"
    return result


def exact_template(client, spec):
    contract = json.loads(CONTRACT.read_text())
    definition = contract["operations"]["get_template_by_exact_name"]
    name = spec["preflight"].get("current_template", {}).get("Name") or spec["payload"]["Name"]
    query = {"q": "Name=" + literal(name), "fields": definition["query"]["fields"], "limit": "2"}
    data = client.request("GET", definition["path"], query)
    require(isinstance(data.get("items"), list) and data.get("hasMore") is False,
            "IDENTITY_AMBIGUOUS", "Exact template read is incomplete.")
    return data["items"]


def execute(spec, preview, approval, client, attempt_file, now=None):
    # Verify approval binding offline before any connection, then refresh reads.
    offline_client = None
    if spec.get("action") == "associate" and "lookup_evidence" not in spec:
        # A live preview retains normalized, reviewed selection evidence. Replay
        # those facts for offline binding, then independently repeat live reads.
        resolution = preview.get("resolution", {})
        evidence = resolution.get("evidence", {})
        candidate = evidence.get("candidate", {})
        check_provenance(candidate, spec.get("context"), now)
        require(candidate.get("id") == spec.get("candidate", {}).get("id") and
                candidate.get("code") == spec.get("candidate", {}).get("code") and
                candidate.get("active") is True and candidate.get("latest") is True,
                "PREVIEW_CHANGED", "Approved selection evidence differs from the candidate.")
        class ApprovedSelectionSnapshot:
            def request(self, method, path, query):
                if path.endswith("/commonLookupsLOV"):
                    return {"items": preview.get("manager_resolution", {}).get("matches", []), "hasMore": False}
                require(method == "GET" and path.endswith("/questionnairesLOV") and
                        query.get("q") == resolution.get("selection_query") and query.get("offset") == "0",
                        "PREVIEW_CHANGED", "Offline selection does not match the approved lookup.")
                return {"items": [{"QuestionnaireId": candidate["id"], "QuestionnaireCode": candidate["code"],
                                   "SubscriberCode": candidate["subscriber_code"], "Status": "A", "LatestVersion": "Y"}],
                        "hasMore": False}
        offline_client = ApprovedSelectionSnapshot()
    expected = plan(spec, offline_client, now=now, manager_snapshot=preview.get("manager_resolution"))
    require(expected.get("status") == "approval_required" and preview == expected,
            "PREVIEW_CHANGED", "Saved preview must match the current specification and evidence.")
    check_provenance(approval, spec["context"], now)
    require(approval.get("approved") is True and approval.get("preview_sha256") == expected["preview_sha256"],
            "APPROVAL_MISMATCH", "Approval must cover this exact preview.")
    require(str(Path(attempt_file).resolve()) == str(Path(spec["attempt_file"]).resolve()),
            "ATTEMPT_PATH_CHANGED", "Attempt-file path differs from the approved specification.")
    require(not Path(attempt_file).exists(), "ATTEMPT_ALREADY_EXISTS", "Reconcile the previous attempt before fresh approval.")
    fresh = plan(spec, client, now)
    require(fresh == expected, "EVIDENCE_CHANGED", "Current target questionnaire selection differs from the preview.")
    rows = exact_template(client, spec)
    request = fresh["request"]
    if request["method"] == "POST":
        require(not rows, "IDENTITY_CONFLICT", "Template name now exists.")
    else:
        current = spec["preflight"]["current_template"]
        require(len(rows) == 1, "IDENTITY_CHANGED", "Update target no longer resolves exactly once.")
        require(all(rows[0].get(k) == v for k, v in current.items() if k not in ("links", "@context")) and
                canonical_path(rows[0], spec["context"]["base_url"], spec["preflight"]["collection_path"]) == request["relative_path"] and
                rows[0].get("@context", {}).get("headers", {}).get("ETag") == current.get("@context", {}).get("headers", {}).get("ETag"),
                "IDENTITY_CHANGED", "Template fields or concurrency token changed after preview.")
    # Exclusive marker is written before dispatch, including for uncertain outcomes.
    try:
        with Path(attempt_file).open("x", encoding="utf-8") as stream:
            json.dump({"preview_sha256": fresh["preview_sha256"], "state": "dispatch_started"}, stream)
    except FileExistsError as exc:
        raise WorkflowError("ATTEMPT_ALREADY_EXISTS", "Reconcile the previous attempt; automatic write retry is disabled.") from exc
    result = {"status": "partial", "milestones": copy.deepcopy(fresh["milestones"]),
              "preview_sha256": fresh["preview_sha256"]}
    ordinary_update = spec.get("action") == "update_template"
    write_milestone = "template_update" if ordinary_update else "association"
    readback_milestone = "template_update_readback" if ordinary_update else "association_readback"
    try:
        client.request(request["method"], request["relative_path"], request["query"],
                       request["payload"], request["conditional_headers"])
        result["milestones"][write_milestone] = "accepted"
        verification_spec = copy.deepcopy(spec)
        if request["method"] == "PATCH" and "Name" in request["payload"]:
            verification_spec["preflight"]["current_template"]["Name"] = request["payload"]["Name"]
        verified = exact_template(client, verification_spec)
        require(len(verified) == 1 and all(verified[0].get(k) == v for k, v in request["payload"].items()),
                "READBACK_MISMATCH", "Template readback differs from the approved fields.")
        if request["method"] == "PATCH":
            excluded = {"links", "@context"}
            if not ordinary_update:
                excluded.update(("QuestionnaireName", "GoalAttributeListCount"))
            elif "GoalAttributeList" in request["payload"]:
                excluded.add("GoalAttributeListCount")
            require(all(verified[0].get(k) == v for k, v in spec["preflight"]["current_template"].items()
                        if k not in request["payload"] and k not in excluded),
                    "READBACK_MISMATCH", "Unchanged template fields were not preserved.")
        if spec["template_type"] == "ORA_PERF_GOAL":
            attrs = request["payload"].get("GoalAttributeList", spec["preflight"].get("current_template", {}).get("GoalAttributeList"))
            require(isinstance(attrs, str) and verified[0].get("GoalAttributeList") == attrs and
                    int(verified[0].get("GoalAttributeListCount", -1)) == len([a for a in attrs.split(",") if a]),
                    "READBACK_MISMATCH", "Goal attributes/count were not verified.")
        result["milestones"][readback_milestone] = "verified"
        result["status"] = ("completed" if ordinary_update or
                            result["milestones"]["content_verification"] in ("verified", "not_required")
                            else "association_verified_content_pending")
    except Exception as exc:
        result["errors"] = [{"code": getattr(exc, "code", "WRITE_OR_READBACK_UNCERTAIN"),
                             "message": str(exc) if isinstance(exc, WorkflowError) else "Inspect sanitized core diagnostics; reconcile before any retry."}]
        authorization_failed = getattr(exc, "code", None) in ("AUTHENTICATION_FAILED", "AUTHORIZATION_DENIED")
        if authorization_failed:
            result["failure_class"] = "auth/authz"
        if result["milestones"][write_milestone] == "not_started":
            if authorization_failed:
                result["status"] = "blocked"
                result["milestones"][write_milestone] = "rejected"
            else:
                result["milestones"][write_milestone] = "uncertain_or_failed"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true", help="Offline preview; no external calls (default).")
    parser.add_argument("--live-read", action="store_true", help="Refresh declared GET evidence when preparing a preview.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--preview", type=Path)
    parser.add_argument("--approval", type=Path)
    parser.add_argument("--attempt-file", type=Path)
    args = parser.parse_args()
    try:
        require(not (args.dry_run and (args.execute or args.live_read)), "INVALID_OPTIONS", "Dry run cannot access Fusion.")
        spec = json.loads(args.input.read_text())
        require(not (spec.get("action") == "plan_requirements" and (args.execute or args.live_read)),
                "INVALID_OPTIONS", "Requirement planning is offline only.")
        rejected = channel_guidance(spec)
        if rejected is not None:
            result = rejected
        elif args.execute:
            require(args.preview and args.approval and args.attempt_file and not args.live_read,
                    "APPROVAL_MISSING", "Execution requires saved preview, approval and a new attempt file.")
            result = execute(spec, json.loads(args.preview.read_text()), json.loads(args.approval.read_text()),
                             CoreClient(spec["context"]["base_url"]), args.attempt_file)
        else:
            result = plan(spec, CoreClient(spec["context"]["base_url"]) if args.live_read else None)
    except Exception as exc:
        result = {"status": "blocked", "errors": [{"code": getattr(exc, "code", "WORKFLOW_FAILED"),
                  "message": str(exc) if isinstance(exc, WorkflowError) else "Workflow failed; inspect sanitized local/core diagnostics."}]}
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in ("requirements_ready", "handoff_ready", "approval_required", "completed", "association_verified_content_pending") else 2


if __name__ == "__main__":
    raise SystemExit(main())
