"""Opt-in Alert batch-create contract; no network access or file writes."""
from __future__ import annotations

import base64
import copy
import hashlib
import json
import re
import uuid
from pathlib import Path
from urllib.parse import quote, urlsplit
import alert_validation

VERSION = alert_validation.VERSION
ENDPOINT = "/hcmRestApi/resources/latest"
HEADERS = {
    "Content-Type": "application/vnd.oracle.adf.batch+json",
    "REST-Framework-Version": "4",
}
POLICY = {
    "request_attempts": 1,
    "automatic_write_retry": False,
    "automatic_rollback": False,
    "server_atomicity": "unverified",
    "server_stop_on_first_part_error": "unverified",
    "verification": "correlate_all_parts_then_independent_read_back",
    "body_verification": "deferred",
}
FIELDS = {
    "alert": {"AlertCode", "Name", "Description", "AlertType", "AlertAccessLevel", "EnabledFlag", "TestModeFlag"},
    "template": {"TemplateCode", "Name", "MimeType", "Subject", "DefaultLanguage", "EnabledFlag", "Body"},
    "recipient": {"RecipientCode", "ChannelType", "ValueExpression"},
}
REQUIRED = {
    "alert": FIELDS["alert"] - {"Description"},
    "template": FIELDS["template"] - {"Body"},
    "recipient": FIELDS["recipient"],
}


class BatchApprovalError(ValueError):
    """Missing or stale approval/source/provider gate binding."""


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest().upper()


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def project_id(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value):
        raise ValueError("Batch project_id must be one safe path segment")
    return value


def receipt_reference(project, attempt):
    """Return the sole project-owned canonical receipt reference for an attempt."""
    return f"project/{project_id(project)}/state/runs/alert-receipts/{attempt}.json"


def origin(value):
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Batch target must be an HTTPS origin without credentials")
    if parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
        raise ValueError("Batch target must contain only the Fusion origin")
    return parsed.hostname.lower(), parsed.port or 443


def _unique_codes(items, field):
    codes = [item[field] for item in items]
    if len(codes) != len(set(codes)):
        raise ValueError(f"Duplicate {field} in the same parent scope")


def _validate_entity(payload, entity):
    child = {"alert": "templates", "template": "recipients"}.get(entity)
    if not isinstance(payload, dict) or set(payload) - FIELDS[entity] - ({child} if child else set()):
        raise ValueError(f"Unsupported fields in batch {entity} payload")
    for field in REQUIRED[entity]:
        if field not in payload or payload[field] is None or payload[field] == "":
            raise ValueError(f"Batch {entity} requires {field}")
    for field, value in payload.items():
        if field == child:
            continue
        if field in {"EnabledFlag", "TestModeFlag"}:
            if type(value) is not bool:
                raise ValueError(f"{field} must be a JSON boolean")
        elif value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"{field} must be a nonblank string when supplied")
        if field in {"TemplateCode", "RecipientCode"} and len(value) > 32:
            raise ValueError(f"{field} exceeds 32 characters")
    code = payload[{"alert": "AlertCode", "template": "TemplateCode", "recipient": "RecipientCode"}[entity]]
    if code in {".", ".."} or any(c in code for c in "/\\?#%"):
        raise ValueError("Batch codes must be safe canonical path segments")
    if "Body" in payload:
        try:
            decoded = base64.b64decode(payload["Body"], validate=True)
            decoded.decode("utf-8")
            if base64.b64encode(decoded).decode("ascii") != payload["Body"]:
                raise ValueError("noncanonical encoding")
        except (ValueError, UnicodeError) as exc:
            raise ValueError("Batch Body must be canonical Base64 of UTF-8 text") from exc
    if child and child in payload:
        items = payload[child]
        if not isinstance(items, list) or not items:
            raise ValueError(f"{child} must be a nonempty array when supplied")
        child_entity = "template" if entity == "alert" else "recipient"
        for item in items:
            _validate_entity(item, child_entity)
        _unique_codes(items, "TemplateCode" if entity == "alert" else "RecipientCode")


def validate_envelope(envelope):
    if not isinstance(envelope, dict) or set(envelope) != {"parts"}:
        raise ValueError("Batch envelope must contain only parts")
    parts = envelope["parts"]
    if not isinstance(parts, list) or not parts:
        raise ValueError("Batch requires at least one part")
    ids = []
    for part in parts:
        if not isinstance(part, dict) or set(part) != {"id", "path", "operation", "payload"}:
            raise ValueError("Invalid batch part shape")
        if not isinstance(part["id"], str) or not re.fullmatch(r"createAlert[1-9][0-9]*", part["id"]):
            raise ValueError("Invalid batch part id")
        if part["path"] != "/eventAlerts" or part["operation"] != "create":
            raise ValueError("Batch supports only create parts at /eventAlerts")
        _validate_entity(part["payload"], "alert")
        ids.append(part["id"])
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate batch part id")
    _unique_codes([p["payload"] for p in parts], "AlertCode")


def build_work_unit(operations, *, source_sha256, target_environment, validation_mode="simple", attempt_id=None, recovery_context="initial", project_id_value="test-project"):
    """Fold existing normalized CREATE operations into nested batch parts."""
    alerts, templates, bodies = {}, {}, set()
    consumed = 0
    for op in operations:
        if op["operation"] != "CREATE" or op.get("body_attachment_plan") is not None:
            raise ValueError("batch-create supports CREATE hierarchies with inline Body only")
        key = op["client_alert_key"]
        entity = op["entity"]
        payload = copy.deepcopy(op["payload"])
        if entity == "alert" and op["method"] == "POST":
            if key in alerts:
                raise ValueError("Duplicate Alert client key")
            alerts[key] = payload
        elif entity == "template" and op["method"] == "POST":
            tkey = (key, op["template_key"])
            if key not in alerts or tkey in templates:
                raise ValueError("Missing parent or duplicate Template client key")
            templates[tkey] = payload
            alerts[key].setdefault("templates", []).append(payload)
        elif entity in {"template_body", "template_recipient"}:
            tkey = (key, op["template_key"])
            if tkey not in templates:
                raise ValueError("Missing included parent Template")
            if entity == "template_body":
                if op["method"] != "PATCH" or set(payload) != {"Body"} or tkey in bodies or not isinstance(payload["Body"], str):
                    raise ValueError("Invalid or duplicate inline Body operation")
                templates[tkey]["Body"] = base64.b64encode(payload["Body"].encode("utf-8")).decode("ascii")
                bodies.add(tkey)
            else:
                if op["method"] != "POST":
                    raise ValueError("Recipients must use CREATE")
                templates[tkey].setdefault("recipients", []).append(payload)
        else:
            raise ValueError("Unsupported batch entity or method")
        consumed += 1
    if consumed != len(operations):
        raise ValueError("Not all included operations were consumed")
    envelope = {"parts": [{"id": f"createAlert{i}", "path": "/eventAlerts", "operation": "create", "payload": payload} for i, payload in enumerate(alerts.values(), 1)]}
    validate_envelope(envelope)
    if target_environment:
        origin(target_environment)
    attempt_id = attempt_id or str(uuid.uuid4())
    if not isinstance(attempt_id, str) or not re.fullmatch(r"[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}", attempt_id):
        raise ValueError("Batch attempt_id must be a UUID")
    if not isinstance(recovery_context, str) or not recovery_context.strip() or len(recovery_context) > 200:
        raise ValueError("Batch recovery_context must be a nonblank bounded string")
    approved_project = project_id(project_id_value)
    approved_receipt = receipt_reference(approved_project, attempt_id)
    document = {
        "contract_version": VERSION,
        "execution_mode": "batch-create",
        "validation_mode": validation_mode,
        "validation_policy": alert_validation.policy(validation_mode),
        "approval_scope": "entire_batch_create",
        "target_environment": target_environment,
        "source_artifact_sha256": source_sha256,
        # Both values are deliberately inside the hashed document.  A recovery
        # is a new attempt, never a replay authorized by an earlier phrase.
        "attempt_id": attempt_id,
        "recovery_context": recovery_context,
        "project_id": approved_project,
        "execution_receipt_reference": approved_receipt,
        "execution_policy": copy.deepcopy(POLICY),
        "request": {
            "method": "POST", "uri": f"{target_environment.rstrip('/') if target_environment else ''}{ENDPOINT}",
            "headers": dict(HEADERS), "payload": envelope, "payload_sha256": digest(envelope),
        },
    }
    fingerprint = digest(document) if target_environment else None
    return {
        "approval_binding_complete": bool(target_environment),
        "approval_document": document,
        "work_unit_sha256": fingerprint,
        "approval_phrase": f"Confirm Alert Batch {fingerprint}" if fingerprint else None,
        "approval_blocker": ("Deep provider preflight gates must pass before approval" if validation_mode == "deep" else None) if fingerprint else "Target environment is required",
    }


def validate_submission(unit, *, approval_phrase, source_workbook, gate_evidence, configured_origin):
    """Fail before authentication on stale approval, source, route or gate evidence."""
    if not isinstance(unit, dict) or not isinstance(unit.get("approval_document"), dict):
        raise ValueError("Batch operation file must contain one work-unit wrapper")
    doc = unit["approval_document"]
    fingerprint = digest(doc)
    if unit.get("work_unit_sha256") != fingerprint or approval_phrase != f"Confirm Alert Batch {fingerprint}":
        raise BatchApprovalError("Missing or mismatched exact Alert Batch approval")
    if doc.get("contract_version") != VERSION or doc.get("execution_mode") != "batch-create" or doc.get("approval_scope") != "entire_batch_create" or doc.get("execution_policy") != POLICY:
        raise ValueError("Unsupported batch contract or execution policy")
    if (not isinstance(doc.get("attempt_id"), str)
            or not re.fullmatch(r"[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}", doc["attempt_id"])
            or not isinstance(doc.get("recovery_context"), str)
            or not doc["recovery_context"].strip()):
        raise BatchApprovalError("Batch approval is missing its attempt or recovery binding")
    try:
        if receipt_reference(doc.get("project_id"), doc["attempt_id"]) != doc.get("execution_receipt_reference"):
            raise BatchApprovalError("Batch receipt reference does not match project and attempt")
    except (KeyError, ValueError) as exc:
        raise BatchApprovalError("Batch approval has an unsafe project or receipt reference") from exc
    mode = doc.get("validation_mode")
    if doc.get("validation_policy") != alert_validation.policy(mode):
        raise BatchApprovalError("Validation policy differs from the supported mode")
    target = doc.get("target_environment")
    if not isinstance(target, str) or origin(target) != origin(configured_origin):
        raise ValueError("Approved batch environment differs from configured Fusion origin")
    request = doc.get("request", {})
    if not isinstance(request, dict):
        raise ValueError("Batch request must be an object")
    if request.get("method") != "POST" or request.get("uri") != target.rstrip("/") + ENDPOINT or request.get("headers") != HEADERS:
        raise ValueError("Batch method, endpoint or headers differ from the supported route")
    validate_envelope(request.get("payload"))
    if digest(request["payload"]) != request.get("payload_sha256"):
        raise ValueError("Batch payload digest mismatch")
    if not source_workbook or file_digest(source_workbook) != doc.get("source_artifact_sha256"):
        raise BatchApprovalError("Source workbook changed; regenerate and reapprove the batch")
    if mode == "simple":
        # All simple-mode gates above are deterministic and local. No live
        # preflight artifact (or assertion that a live check passed) is needed.
        if gate_evidence is not None and not isinstance(gate_evidence, dict):
            raise BatchApprovalError("Provider preflight evidence must be an object")
        if gate_evidence and gate_evidence.get("validation_mode") != "simple":
            raise BatchApprovalError("Supplied gate evidence belongs to a different validation mode")
        return request
    evidence = gate_evidence or {}
    if not isinstance(evidence, dict):
        raise BatchApprovalError("Provider preflight evidence must be an object")
    if evidence.get("validation_mode") != "deep" or evidence.get("work_unit_sha256") != fingerprint or evidence.get("target_environment") != target or evidence.get("status") != "ready_for_approval":
        raise BatchApprovalError("Missing or stale provider preflight evidence")
    gates = evidence.get("gates", {})
    if not isinstance(gates, dict):
        raise BatchApprovalError("Provider gates must be an object")
    for gate in ("ALERT.VALIDATE", "ALERT.LOOKUP", "ALERT.DEPENDENCY", "ALERT.DESIGN"):
        record = gates.get(gate, {})
        if not isinstance(record, dict) or record.get("status") != "passed" or not record.get("artifact") or not record.get("sha256"):
            raise BatchApprovalError(f"Required provider gate has not passed: {gate}")
        if file_digest(record["artifact"]) != record["sha256"]:
            raise BatchApprovalError(f"Provider gate evidence changed: {gate}")
    return request


def inspect_response(envelope, response, target):
    """Correlate by part id and canonical codes; never infer Body storage."""
    errors, reports = [], []
    parts = response.get("parts") if isinstance(response, dict) else None
    expected = {p["id"]: p for p in envelope["parts"]}
    if not isinstance(parts, list):
        return {"parts": [], "errors": [{"message": "Fusion did not return a batch parts array."}]}
    received = {}
    for part in parts:
        pid = part.get("id") if isinstance(part, dict) else None
        if not isinstance(pid, str) or pid not in expected or pid in received:
            errors.append({"message": "Fusion returned an unknown, missing, or duplicate part identifier."})
            continue
        received[pid] = part

    def compare(wanted, actual, entity, parent_path, identities):
        if not isinstance(actual, dict):
            raise ValueError(f"Missing {entity} response payload")
        for error_key in ("errors", "error", "errorDetails"):
            if actual.get(error_key):
                raise ValueError(f"Fusion reported a {entity} business error; reconcile before retry")
        code_field, id_field = {"alert": ("AlertCode", "AlertId"), "template": ("TemplateCode", "TemplateId"), "recipient": ("RecipientCode", "RecipientId")}[entity]
        item_path = parent_path + "/" + quote(wanted[code_field], safe="")
        for field, value in wanted.items():
            if field not in {"templates", "recipients", "Body"} and (actual.get(field) != value or type(actual.get(field)) is not type(value)):
                raise ValueError(f"Returned {entity} {field} differs from the approved value")
        external_id = actual.get(id_field)
        if isinstance(external_id, bool) or not str(external_id).isdigit():
            raise ValueError(f"Missing valid {id_field}")
        links = actual.get("links", [])
        canonical = [l.get("href") for l in links if isinstance(l, dict) and l.get("rel") == "canonical"] if isinstance(links, list) else []
        if len(canonical) != 1 or not isinstance(canonical[0], str):
            raise ValueError(f"Missing unambiguous {entity} canonical link")
        parsed = urlsplit(canonical[0])
        if origin(f"{parsed.scheme}://{parsed.netloc}") != origin(target) or parsed.path != item_path or parsed.query or parsed.fragment:
            raise ValueError(f"Returned {entity} canonical link differs from the approved key/environment")
        identities.append({"entity": entity, "code": wanted[code_field], "id": external_id, "canonical_uri": canonical[0]})
        child = {"alert": "templates", "template": "recipients"}.get(entity)
        if child:
            collection = actual.get(child, {"items": []})
            items = collection.get("items") if isinstance(collection, dict) else collection
            wanted_items = wanted.get(child, [])
            if not isinstance(items, list) or len(items) != len(wanted_items) or (isinstance(collection, dict) and collection.get("hasMore")):
                raise ValueError(f"Returned {child} count differs or is incomplete")
            child_entity = "template" if child == "templates" else "recipient"
            child_code = "TemplateCode" if child == "templates" else "RecipientCode"
            mapped = {item.get(child_code): item for item in items if isinstance(item, dict) and isinstance(item.get(child_code), str)}
            if len(mapped) != len(items):
                raise ValueError(f"Duplicate or missing {child_code} in response")
            for wanted_item in wanted_items:
                compare(wanted_item, mapped.get(wanted_item[child_code]), child_entity, item_path + "/child/" + child, identities)

    for pid, part in expected.items():
        actual = received.get(pid)
        identities = []
        try:
            if not actual:
                raise ValueError("Fusion omitted this batch part")
            status = actual.get("status", actual.get("statusCode"))
            if status is not None and (not str(status).isdigit() or not 200 <= int(status) < 300):
                raise ValueError("Fusion rejected this batch part; review business errors before recovery")
            if any(actual.get(k) for k in ("errors", "error", "errorDetails")):
                raise ValueError("Fusion reported a business error for this batch part")
            if actual.get("operation") != "create":
                raise ValueError("Fusion returned an unexpected part operation")
            compare(part["payload"], actual.get("payload"), "alert", "/hcmRestApi/resources/11.13.18.05/eventAlerts", identities)
        except (ValueError, TypeError) as exc:
            errors.append({"part_id": pid, "message": str(exc)})
            reports.append({"part_id": pid, "status": "reconciliation_required", "reported_identities": identities})
        else:
            reports.append({"part_id": pid, "status": "response_matched_pending_read_back", "reported_identities": identities})
    return {"parts": reports, "errors": errors, "body_verification": "deferred", "independent_read_back": "required"}
