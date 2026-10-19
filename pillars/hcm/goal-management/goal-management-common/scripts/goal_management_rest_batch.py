"""Offline Goal Management batch preview/audit adapter. Never sends requests.

Consumes validated object-skill operations, not raw business input. Core owns
authentication and transport; this module owns Goal Management batch boundaries.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import re
from urllib.parse import urlsplit, unquote

from goal_management_route_selector import select_route
from resolve_goal_management_batch_contract import resolve_batch_contracts

CONTENT_TYPE = "application/vnd.oracle.adf.batch+json"
RESOURCES = {"goalPlans", "reviewPeriods", "libraryGoals", "performanceGoalsV2"}


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def _root(value):
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
            or parsed.query or parsed.fragment
            or not re.fullmatch(r"/hcmRestApi/resources/(?:latest|\d+(?:\.\d+)*)/?", parsed.path)):
        raise ValueError("A verified HTTPS HCM resource root is required; no /$batch suffix")
    return value.rstrip("/")


def _path(value):
    if not isinstance(value, str):
        raise ValueError("Relative resource path required")
    # Opaque item keys may be encoded, but routing delimiters must not be encoded.
    decoded = unquote(value)
    segments = decoded.split("/")
    if (not value.startswith("/") or value.startswith("//") or "\\" in decoded
            or any(c in decoded for c in "?#{}\r\n%") or "/action/" in decoded
            or any(s in {".", ".."} for s in segments)
            or len(segments) < 2 or segments[1] not in RESOURCES
            or decoded.count("/") != value.count("/")):
        raise ValueError("Unsupported or unsafe Goal Management relative path")
    return value


def _pattern(op):
    """Local eligible shapes, not a declaration of tenant capability."""
    path, method = op.get("path", ""), op.get("operation")
    if re.fullmatch(r"/(goalPlans|reviewPeriods|libraryGoals)/?", path) and method == "create":
        return "independent_setup"
    if re.fullmatch(r"/(goalPlans|reviewPeriods|libraryGoals)/[^/]+", path) and method in {"update", "delete"}:
        return "independent_setup"
    if (re.fullmatch(r"/performanceGoalsV2/?", path) and method == "create"
            or re.fullmatch(r"/performanceGoalsV2/[^/]+", path) and method == "update"):
        return "template_goal"
    if (re.fullmatch(r"/goalPlans/[^/]+/child/associatedPerfDocumentTypes", path) and method == "create"
            or re.fullmatch(r"/goalPlans/[^/]+/child/associatedPerfDocumentTypes/[^/]+", path) and method == "delete"):
        return "document_association"
    raise ValueError("Unsupported batch pattern; retain the owning skill's separate route")


def _combination(operations, root, contract):
    if not all(isinstance(op, dict) for op in operations):
        raise ValueError("Every batch operation must be an object")
    ids = [op.get("id") for op in operations]
    if not all(isinstance(i, str) for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("Unique part IDs required before dependency validation")
    if not isinstance(contract, dict) or not contract.get("evidence"):
        raise ValueError("Explicit combination contract evidence required")
    context = contract.get("transaction_context")
    if not isinstance(context, str) or not context.strip() or contract.get("batch_root") != root:
        raise ValueError("Combination must bind one root and transaction context")
    signatures = [{k: op.get(k) for k in ("id", "path", "operation")} for op in operations]
    if contract.get("parts") != signatures:
        raise ValueError("Combination evidence must cover the exact ordered parts")
    patterns = []
    for op in operations:
        _path(op.get("path"))
        patterns.append(_pattern(op))
        if op.get("contract", {}).get("transaction_context") != context:
            raise ValueError("Incompatible transaction contexts")
        dependencies = op.get("dependencies")
        if not isinstance(dependencies, list):
            raise ValueError("Explicit dependencies list required, even when empty")
        for dep in dependencies:
            if not isinstance(dep, dict) or not isinstance(dep.get("part_id"), str):
                raise ValueError("Dependency identity required")
            if dep["part_id"] in ids:
                raise ValueError("Same-batch dependency requires a later verified stage")
            if dep.get("verified") is not True or not dep.get("evidence"):
                raise ValueError("Prior-stage dependency needs verification evidence")
        serialized = json.dumps(op.get("payload"))
        if any(marker in serialized for marker in ('"$ref"', '${', '{{')):
            raise ValueError("Unresolved cross-part references are not supported")
    # Specialized operations cannot be mixed with unrelated setup transactions.
    mode = contract.get("pattern")
    if mode == "independent_setup" and set(patterns) == {mode}:
        if any(op.get("required_group") for op in operations):
            raise ValueError("Required groups must use their specialized pattern")
    elif mode == "template_goal" and set(patterns) == {mode}:
        if any(op.get("required_group") for op in operations):
            raise ValueError("Unknown template-goal group")
    elif mode == "document_association":
        groups = {}
        for op, pattern in zip(operations, patterns):
            group = op.get("required_group")
            if not isinstance(group, dict) or not isinstance(group.get("id"), str) or not group["id"]:
                raise ValueError("Document association requires a complete parent/child group")
            groups.setdefault(group["id"], []).append((op, pattern))
        for members in groups.values():
            member_ids = [op["id"] for op, _ in members]
            if any(op["required_group"].get("parts") != member_ids for op, _ in members):
                raise ValueError("Missing or reordered required group parts")
            parents = [op for op, p in members if p == "independent_setup"
                       and op["operation"] == "update" and re.fullmatch(r"/goalPlans/[^/]+", op["path"])]
            children = [op for op, p in members if p == "document_association"]
            if len(parents) != 1 or not children or len(children) + 1 != len(members):
                raise ValueError("Group needs exactly one plan update and its association children")
            if any(not child["path"].startswith(parents[0]["path"] + "/child/") for child in children):
                raise ValueError("Child association belongs to a different plan")
    else:
        raise ValueError("Unknown or incompatible batch combination")


def build_preview(*, intent, batch_root, operations, max_parts, combination_contract=None):
    """Build ONE ready dependency stage; never silently chunk or execute it.

    Each operation carries id, operation(create/update/delete), path, payload,
    identity, before, validated, dependencies_verified, and contract. Contract:
    batch_root, batch_enabled, evidence, path, operation, optional ifMatch.
    Domain builders/skills remain responsible for business and writable-field
    validation, duplicate checks, fresh IDs, and lifecycle prerequisites.
    """
    route = select_route([], intent)
    if route.get("transportIntent") != "adf_batch":
        raise ValueError("Explicit unambiguous REST batch intent required")
    root = _root(batch_root)
    if type(max_parts) is not int or max_parts < 1:
        raise ValueError("A positive reviewed max_parts limit is required")
    if not isinstance(operations, list) or not operations or len(operations) > max_parts:
        raise ValueError("Empty or oversized batch; explicitly plan separate approval stages")
    _combination(operations, root, combination_contract)
    parts, audit, ids, targets = [], [], set(), set()
    for op in deepcopy(operations):
        part_id = op.get("id")
        if not isinstance(part_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", part_id) or part_id in ids:
            raise ValueError("Every part needs a unique stable ID")
        ids.add(part_id)
        path = _path(op.get("path"))
        operation = op.get("operation")
        if operation not in {"create", "update", "delete"}:
            raise ValueError("Custom actions/ESS are not ordinary batch CRUD")
        if op.get("validated") is not True or op.get("dependencies_verified") is not True:
            raise ValueError("Complete object validation and earlier dependency verification first")
        contract = op.get("contract", {})
        if (contract.get("batch_enabled") is not True or not contract.get("evidence")
                or _root(contract.get("batch_root", "")) != root
                or contract.get("path") != path or contract.get("operation") != operation):
            raise ValueError("Current operation-specific batch contract does not match")
        if not isinstance(op.get("identity"), dict) or not op["identity"]:
            raise ValueError("Resolved business identity required for audit")
        target = (path, fingerprint(op["identity"]) if operation == "create" else "")
        if target in targets:
            raise ValueError("Duplicate target; use a later verified stage for dependent changes")
        targets.add(target)
        payload = op.get("payload")
        if operation != "delete" and (not isinstance(payload, dict) or not payload or "parts" in payload):
            raise ValueError("Reuse a nonempty validated entity payload, not a nested batch")
        if operation == "delete" and payload is not None:
            raise ValueError("Delete payload must be null")
        before = op.get("before")
        if operation != "create" and (not isinstance(before, dict) or not before):
            raise ValueError("Fresh pre-write values required")
        if operation == "update" and not set(payload).issubset(before):
            raise ValueError("Audit must include old values for every changed field")
        part = {"id": part_id, "operation": operation, "path": path, "payload": payload}
        if "ifMatch" in contract:
            if not isinstance(contract["ifMatch"], str) or not contract["ifMatch"] or contract["ifMatch"] == "*":
                raise ValueError("Use the exact current concurrency token, never a wildcard")
            part["ifMatch"] = [contract["ifMatch"]]
        parts.append(part)
        audit.append({"id": part_id, "identity": op["identity"], "path": path,
                      "operation": operation, "before": before, "requested": payload,
                      "contractEvidence": contract["evidence"],
                      "dependencies": deepcopy(op["dependencies"]),
                      "required_group": deepcopy(op.get("required_group"))})
    envelope = {"request": {"method": "POST", "url": root + "/",
                            "headers": {"Content-Type": CONTENT_TYPE}, "body": {"parts": parts}},
                "audit": audit, "max_parts": max_parts,
                "combination_contract": deepcopy(combination_contract),
                "approval_required": True, "automatic_retry": False}
    return {**envelope, "sha256": fingerprint(envelope)}


def resolve_and_build_preview(
    *, intent, batch_root, operations, runtime_metadata, max_parts
):
    """Resolve maintained parent CRUD capability, then build one immutable preview.

    This entry point is callable only for explicit REST batch intent.  The
    resolver itself returns ``selected=False`` without modifying operations for
    standard REST, HDL, FSM, or intake routes; this builder then refuses to
    create a batch preview for those routes.
    """
    resolved = resolve_batch_contracts(
        intent=intent,
        batch_root=batch_root,
        operations=operations,
        runtime_metadata=runtime_metadata,
    )
    if resolved.get("selected") is not True:
        raise ValueError("Explicit unambiguous REST batch intent required")
    return build_preview(
        intent=intent,
        batch_root=resolved["batch_root"],
        operations=resolved["operations"],
        max_parts=max_parts,
        combination_contract=resolved["combination_contract"],
    )


def assert_approved(preview, approved_sha256):
    envelope = {k: v for k, v in preview.items() if k != "sha256"}
    if approved_sha256 != preview.get("sha256") or fingerprint(envelope) != approved_sha256:
        raise ValueError("Batch changed or approval missing; generate a new preview")


def reconcile(preview, *, http_status, response, verified_after=None):
    """Conservative per-part audit. HTTP 2xx alone never proves persistence.

    verified_after maps part ID to an object-skill verification record containing
    matches=True and the freshly read after value. Missing/error responses remain
    unknown, not successful; no replay is selected here.
    """
    assert_approved(preview, preview.get("sha256"))
    expected = {part["id"] for part in preview["request"]["body"]["parts"]}
    parts = response.get("parts", []) if isinstance(response, dict) else []
    if not isinstance(parts, list):
        parts = []
    returned = [p.get("id") for p in parts if isinstance(p, dict)]
    complete = (len(parts) == len(expected) and len(returned) == len(expected)
                and all(isinstance(value, str) for value in returned)
                and set(returned) == expected)
    error = not 200 <= http_status < 300 or any(
        isinstance(p, dict) and (p.get("errors") or p.get("error")
                                or str(p.get("status", "")).startswith(("4", "5"))
                                or str(p.get("statusCode", "")).startswith(("4", "5")))
        for p in parts)
    rows = []
    for source in preview["audit"]:
        verification = (verified_after or {}).get(source["id"], {})
        status = "failed_or_rolled_back" if error else "unknown"
        if not error and complete and verification.get("matches") is True and "after" in verification:
            status = "verified"
        rows.append({**deepcopy(source), "status": status,
                     "after": deepcopy(verification.get("after"))})
    return {"sha256": preview["sha256"], "http_status": http_status,
            "status": "verified" if all(r["status"] == "verified" for r in rows) else "stop_for_review",
            "automatic_retry": False, "records": rows}
