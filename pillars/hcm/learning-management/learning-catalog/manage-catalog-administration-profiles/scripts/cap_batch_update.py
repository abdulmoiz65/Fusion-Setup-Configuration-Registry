"""One approved CAP basic-attribute update through the unchanged shared REST CLI.

Python 3.11+. No HTTP/auth client or Data Loader fallback. inspect/prepare use
shared GET only. submit requires later exact-payload consent; verify is read-only.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.parse import unquote, urlsplit

import cap_read
import cap_workflow as workflow
import cap_create_handoff as common
from cap_profile_inspection import parent_key
from cap_update_inspection import typed_field_metadata
import cap_update_validation as policy
import cap_visibility

ROUTE = "cap-shared-rest-basic-batch-v2"
LEGACY_ROUTE = "cap-shared-rest-description-batch-v1"
ALLOWED_FIELDS = {"name", "description", "visibility"}
BATCH_ROOT = workflow.ROOT_PATH.rsplit("/", 1)[0] + "/"
MEDIA_TYPE = "application/vnd.oracle.adf.batch+json"
NODES = ("CAP-SELECT", "CAP-BATCH-INPUT", "CAP-BATCH-OBSERVE", "CAP-BATCH-DESIGN", "CAP-BATCH-READY")
VISIBILITY_LOOKUP_PATH = "/fscmRestApi/resources/11.13.18.05/commonLookupsLOV"
VISIBILITY_FINDER = "LookupTypeFinder;LookupType=ORA_WLF_CAP_ADMIN_VISIBILITY"


class BatchError(ValueError):
    """Sanitized local invariant failure, safe to report without HTTP content."""

    def __init__(self, message, failure_class="input_validation"):
        super().__init__(message)
        self.failure_class = failure_class


def require(condition, message):
    if not condition:
        raise BatchError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def now_utc():
    return datetime.now(timezone.utc)


def timestamp(value):
    require(isinstance(value, str), "Missing observation/approval time")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Timezone is required")
    return parsed


def item_path(path, host, key):
    """Validate trusted response identity without retaining private runtime URLs."""
    require(isinstance(path, str), "Missing canonical item link")
    parsed = urlsplit(path)
    target = urlsplit(host)
    if parsed.netloc:
        require(parsed.scheme == "https" and parsed.hostname == target.hostname
                and parsed.port in (None, 443) and not parsed.username and not parsed.password,
                "Canonical item belongs to another host")
    else:
        require(not parsed.scheme, "Unexpected item URI scheme")
    require(not parsed.query and not parsed.fragment, "Unexpected item URI suffix")
    decoded = unquote(parsed.path)
    suffix = "/learningCatalogProfiles/" + key
    prefixes = ("", workflow.ROOT_PATH.rsplit("/", 1)[0],
                workflow.ROOT_PATH.rsplit("/", 1)[0] + ":9")
    if decoded in {prefix + suffix for prefix in prefixes}:
        return
    require(re.fullmatch(r"/hcmRestApi/rest/rv:[A-Za-z0-9-]+/[A-Za-z0-9-]+/11\.13\.18\.05:9"
                         + re.escape(suffix), decoded), "Unexpected canonical resource/version/key")


def read_request(request):
    require(isinstance(request, dict), "A batch-update request is required")
    require(set(request) <= {"mode", "number", "expected_id", "expected_name", "host",
                            "confirmed_host", "environment", "headers", "changes"},
            "Unsupported request field, URL, operation or approval")
    read = {k: v for k, v in request.items() if k not in {"changes", "expected_name"}}
    workflow.validate_read_request(read)
    if isinstance(request.get("changes"), dict) and "status" in request["changes"]:
        raise BatchError("Status writes are unavailable: activation/deactivation require a verified lifecycle eligibility contract; deactivation needs current CAN_DEACTIVATE action hints and provider-use restrictions. Deletion is not a basic status edit.")
    require(read.get("mode") == "exact" and "number" in read,
            "Batch update requires an exact stable profile number")
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,1999}", read["number"]),
            "Unsafe profile number")
    require(isinstance(request.get("changes"), dict) and bool(request["changes"])
            and set(request["changes"]) <= ALLOWED_FIELDS,
            "Only explicit name, description and visibility replacements are supported")
    for field, value in request["changes"].items():
        if field == "visibility":
            value = cap_visibility.normalize(value)
        policy._text(value, field, policy.LIMITS[field])
    if "expected_name" in request:
        policy._text(request["expected_name"], "expected name", 250)
    return read


def ready(request):
    read = read_request(request)
    plan = workflow.shared_plan()
    nodes = {n["id"]: n for n in plan["task"]["nodes"]}
    current = nodes["CAP-SELECT"]["transitions"].get("batch_update")
    for expected in NODES[1:]:
        require(current == expected and expected in nodes, "Declared batch graph is missing/stale")
        if expected != NODES[-1]:
            current = nodes[expected]["transitions"].get("passed")
    require(nodes[NODES[-1]]["action_type"] == "terminal", "Preparation must stop for approval")
    workflow.configured_context(read)
    return read


def visibility_metadata(attribute, fetch):
    """Resolve the source-declared LOV through shared GET, never a fabricated enum.

    A single bounded complete page suffices for this two-choice lookup. Unexpected
    expansion/partial results require investigation rather than approval.
    """
    if "enum" in attribute:
        return attribute
    lov = attribute.get("lov", {})
    require(isinstance(lov, dict)
            and lov.get("childRef") == "LearnCatalogProfilesVisibilityLOVVA"
            and lov.get("attributeMap") == [{"source": "LookupCode", "target": "visibility"}],
            "Visibility lookup metadata does not advertise the supported LOV association")
    page = fetch(VISIBILITY_LOOKUP_PATH, {"finder": VISIBILITY_FINDER,
                 "onlyData": "true", "limit": "100", "offset": "0"})
    require(isinstance(page, dict) and page.get("hasMore") is False
            and page.get("offset", 0) == 0, "Visibility lookup must be complete")
    rows = page.get("items")
    require(isinstance(rows, list) and 0 < len(rows) <= 100
            and page.get("count", len(rows)) == len(rows), "Malformed visibility lookup")
    codes = []
    for row in rows:
        require(isinstance(row, dict) and isinstance(row.get("LookupCode"), str)
                and row["LookupCode"] in cap_visibility.CODES
                and row.get("EnabledFlag", "Y") == "Y"
                and row.get("LookupType", "ORA_WLF_CAP_ADMIN_VISIBILITY") == "ORA_WLF_CAP_ADMIN_VISIBILITY",
                "Unexpected or disabled visibility lookup entry")
        codes.append(row["LookupCode"])
    require(len(codes) == len(set(codes)), "Duplicate visibility lookup codes")
    return {**attribute, "enum": codes, "enumSource": {
        "path": VISIBILITY_LOOKUP_PATH, "finder": VISIBILITY_FINDER,
        "complete": True, "observedAt": now_utc().isoformat(), "codes": codes}}


def observation(request, *, get=None, clock=time.monotonic):
    """Metadata, unique baseline and canonical item reads; never number-only probing."""
    read = ready(request)
    get = get or workflow.shared_get
    started = clock()
    def fetch(path, query):
        remaining = 120 - (clock() - started)
        require(remaining >= 1, "Batch inspection timed out; identity is unverified")
        try:
            value = get(read, path, query, remaining)
        except Exception:
            raise BatchError("Shared GET failed; identity/metadata remains unverified. Resolve shared authentication, access or transport diagnostics before retrying reads.",
                             "transport/environment") from None
        require(clock() - started < 120, "Batch inspection exceeded its deadline")
        return value
    root = cap_read.resource_description(fetch(workflow.ROOT_PATH + "/describe", {}), "learningCatalogProfiles")
    rows = root.get("attributes")
    require(isinstance(rows, list) and all(isinstance(a, dict) and isinstance(a.get("name"), str) for a in rows)
            and len({a["name"] for a in rows}) == len(rows), "Malformed or duplicate root metadata")
    cap_read.validate_metadata(root, "learningCatalogProfileNumber", ["learningCatalogProfileNumber", "name"])
    actions = root.get("item", {}).get("actions", [])
    require(isinstance(actions, list) and any(isinstance(a, dict) and a.get("method") == "PATCH"
            for a in actions), "Current metadata does not advertise root update")
    attrs = {a["name"]: a for a in rows}
    fields = sorted(f for f in policy.BASELINE_FIELDS if attrs.get(f, {}).get("type") == "string")
    result = cap_read.collect_exact(lambda q: fetch(workflow.ROOT_PATH, q),
        {"onlyData": "false", "fields": ",".join(fields),
         "q": cap_read.exact_query("learningCatalogProfileNumber", read["number"])},
        selector_field="learningCatalogProfileNumber", value=read["number"],
        identity_fields=("learningCatalogProfileNumber",))
    require(result["status"] == "matched" and result["match_count"] == 1,
            "Complete unique accessible profile lookup is required")
    row = result["matches"][0]
    baseline = {f: row[f] for f in fields if f in row}
    policy._baseline(baseline, require_complete=True)
    if "expected_name" in request:
        require(baseline.get("name") == request["expected_name"], "Profile name and stable number disagree")
    if "expected_id" in read:
        require(baseline.get("learningCatalogProfileId") == read["expected_id"], "Stable profile ID disagrees")
    encoded, date = parent_key(row, read["number"])
    links = row.get("@context", {}).get("links", [])
    canonical = [link for link in links if isinstance(link, dict) and link.get("rel") in {"self", "canonical"}]
    require(canonical, "Fresh canonical/self link is required")
    for link in canonical:
        item_path(link.get("href"), read["host"], unquote(encoded))
    item = fetch(workflow.ROOT_PATH + "/" + encoded, {"onlyData": "true", "fields": ",".join(fields)})
    require(isinstance(item, dict) and all(f in item and item[f] == v for f, v in baseline.items()),
            "Canonical item does not match the observed baseline")
    metadata = typed_field_metadata({field: attrs.get(field, {}) for field in request["changes"]})
    if "visibility" in metadata:
        metadata["visibility"] = visibility_metadata(metadata["visibility"], fetch)
    duplicates = None
    if "name" in request["changes"] and request["changes"]["name"] != baseline["name"]:
        cap_read.validate_metadata(root, "name", ["learningCatalogProfileNumber", "name"])
        proposed_name = request["changes"]["name"]
        matches = cap_read.collect_exact(lambda q: fetch(workflow.ROOT_PATH, q),
            {"onlyData": "true", "fields": "learningCatalogProfileNumber,name",
             "q": cap_read.exact_query("name", proposed_name)},
            selector_field="name", value=proposed_name,
            identity_fields=("learningCatalogProfileNumber",))
        # collect_exact returns only after the final page; incomplete/looping
        # collections raise and cannot create duplicate-clearance evidence.
        duplicates = {"status": "verified", "complete": True, "name": proposed_name,
                      "source": "Current shared GET exact-name lookup, account-visible only",
                      "matchingProfileNumbers": [v["learningCatalogProfileNumber"] for v in matches["matches"]]}
    diff = policy.validate_changes(baseline, request["changes"], metadata, duplicate_check=duplicates)
    return {"route": ROUTE, "status": diff["status"], "observedAt": now_utc().isoformat(),
            "environment": {"name": read["environment"], "host": read["host"]},
            "baseline": baseline, "fieldMetadata": metadata, "changes": diff["intendedFields"],
            "duplicateCheck": duplicates,
            "visibilityReview": ({**cap_visibility.review(request["changes"]["visibility"]),
                "before": baseline["visibility"],
                "beforeLabel": cap_visibility.LABELS.get(baseline["visibility"], "Unknown")}
                if "visibility" in request["changes"] else None),
            "effectiveDate": date, "canonicalKey": unquote(encoded), "batchRoot": BATCH_ROOT,
            "validationPurpose": "batch_update_observation_only", "writeEligible": False,
            "limitations": ["Account-visible and nontransactional; GET does not prove update privileges",
                "Target acceptance is operation-specific; prior name/description success does not verify visibility access effects",
                cap_visibility.ACCESS_NOTE,
                "Fixed key date and sparse last-writer-wins; CAP processing completion is separate"]}


def batch_body(observed):
    require(observed.get("route") in {ROUTE, LEGACY_ROUTE} and observed.get("batchRoot") == BATCH_ROOT,
            "Not a declared batch observation")
    baseline = observed.get("baseline")
    policy._baseline(baseline, require_complete=True)
    number = baseline["learningCatalogProfileNumber"]
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,1999}", number), "Unsafe part identity")
    key = observed.get("canonicalKey")
    encoded, date = parent_key({"@context": {"key": key}}, number)
    require(unquote(encoded) == key and observed.get("effectiveDate") == date, "Canonical key/date mismatch")
    changes = observed.get("changes")
    allowed = {"description"} if observed.get("route") == LEGACY_ROUTE else ALLOWED_FIELDS
    require(isinstance(changes, dict) and bool(changes) and set(changes) <= allowed,
            "Unsupported or empty attribute change")
    diff = policy.validate_changes(baseline, changes, observed.get("fieldMetadata"),
                                   duplicate_check=observed.get("duplicateCheck"))
    require(diff["status"] == "changes_ready", "No-op must not become a write")
    return {"parts": [{"id": "details", "path": "/learningCatalogProfiles/" + key,
                      "operation": "update", "effectiveOf": "RangeMode=UPDATE", "payload": diff["intendedFields"]}]}


def safe_path(path, root):
    raw = Path(path).absolute()
    require(not any(p.is_symlink() for p in [raw, *raw.parents]), "Symlink paths are not supported")
    require(common._inside(raw, root), "Artifact must stay inside the selected project")
    return raw


def save_new(path, value):
    data = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    require(json.loads(Path(path).read_text()) == value, "Artifact write could not be verified")


def project_context(project, read):
    project = safe_path(project, workflow.REPO / "project").resolve(strict=True)
    state_path = safe_path(project / "state/project-state.json", project)
    state = common._json(state_path)
    control = state.get("runbook_control", {})
    if control.get("mode") == "required":
        require(control.get("status") == "active", "Required initial project Run Book is not active")
    workflow.configured_context(read)
    return project, common._file_digest(state_path)


def operation_for(changes):
    return "update_description" if set(changes) == {"description"} else "update_basics"


def privilege_check(value, environment, operation="update_description"):
    require(isinstance(value, dict) and value.get("environment") == environment
            and value.get("operation") == operation
            and value.get("enforcement") == "core.fusion-api.rest-api-client"
            and value.get("status") in {"assessed", "verified"}
            and value.get("knownDenial") is False
            and type(value.get("grantsVerified")) is bool
            and isinstance(value.get("source"), str) and value["source"].strip(),
            "An attributed current update-privilege assessment with no known denial is required")
    require(value["status"] != "verified" or value["grantsVerified"] is True,
            "Verified privileges require grant evidence; GET is insufficient")


def prepare(request, *, project_root, output_dir, privilege_path, get=None):
    read = ready(request)
    project, state_hash = project_context(project_root, read)
    output = safe_path(output_dir, project)
    require(not output.exists(), "Use a new preparation directory")
    privilege_path = safe_path(privilege_path, project)
    privileges = common._json(privilege_path)
    environment = {"name": read["environment"], "host": read["host"]}
    operation = operation_for(request["changes"])
    privilege_check(privileges, environment, operation)
    observed = observation(request, get=get)
    if observed["status"] == "no_op":
        return {"status": "no_op", "writeEligible": False, "profileNumber": read["number"]}
    body = batch_body(observed)
    created = now_utc()
    preview = {"route": ROUTE, "operation": operation, "method": "POST",
               "environment": environment, "batchRoot": BATCH_ROOT,
               "headers": {"Content-Type": MEDIA_TYPE, "REST-Framework-Version": "9",
                           **read.get("headers", {})},
               "request": request, "observation": observed, "payload": body,
               "payloadSha256": digest(body), "privileges": privileges,
               "privilegeSourceSha256": common._file_digest(privilege_path),
               "projectStateSha256": state_hash, "sourceFingerprint": common.source_fingerprint(),
               "createdAt": created.isoformat(), "expiresAt": (created + timedelta(minutes=30)).isoformat(),
               "approval": None, "writeEligible": False,
               "warnings": observed["limitations"] + (["Effective write grants unverified; Fusion enforces the approved genuine update"]
                   if not privileges["grantsVerified"] else [])}
    output.mkdir(parents=True, mode=0o700)
    save_new(output / "payload.json", body)
    save_new(output / "preview.json", {"preview": preview, "previewSha256": digest(preview)})
    return {"status": "awaiting_exact_payload_approval", "previewPath": str(output / "preview.json"),
            "payloadPath": str(output / "payload.json"), "previewSha256": digest(preview),
            "payloadSha256": digest(body), "preview": preview, "writeEligible": False}


def frozen(preview_path, project_root, approved_digest, *, now=None):
    project = safe_path(project_root, workflow.REPO / "project").resolve(strict=True)
    path = safe_path(preview_path, project).resolve(strict=True)
    retained = common._json(path)
    p = retained.get("preview")
    require(isinstance(p, dict) and re.fullmatch(r"[0-9a-f]{64}", approved_digest or "")
            and digest(p) == retained.get("previewSha256") == approved_digest,
            "Exact approval digest does not match the retained preview")
    require(p.get("route") == ROUTE and p.get("operation") == operation_for(p.get("request", {}).get("changes", {}))
            and p.get("method") == "POST" and p.get("batchRoot") == BATCH_ROOT
            and p.get("approval") is None and p.get("writeEligible") is False,
            "Wrong route/operation; read or Data Loader approval cannot authorize batch update")
    read = ready(p["request"])
    _, state_hash = project_context(project, read)
    require(p.get("environment") == {"name": read["environment"], "host": read["host"]}
            == p["observation"].get("environment"), "Frozen target disagrees")
    intended = policy.validate_changes(p["observation"]["baseline"], p["request"]["changes"],
                                      p["observation"]["fieldMetadata"],
                                      duplicate_check=p["observation"].get("duplicateCheck"))["intendedFields"]
    require(p["observation"]["baseline"]["learningCatalogProfileNumber"] == read["number"]
            and p["observation"]["changes"] == intended, "Frozen identity or inputs disagree")
    require(p.get("headers") == {"Content-Type": MEDIA_TYPE, "REST-Framework-Version": "9", **read.get("headers", {})},
            "Frozen headers changed")
    require(p.get("sourceFingerprint") == common.source_fingerprint()
            and p.get("projectStateSha256") == state_hash, "Implementation or project binding changed; reprepare")
    created, expires, observed = timestamp(p["createdAt"]), timestamp(p["expiresAt"]), timestamp(p["observation"]["observedAt"])
    require(observed <= created < expires and timedelta(0) < expires-created <= timedelta(minutes=30)
            and observed >= created-timedelta(minutes=3) and created <= (now or now_utc()) < expires,
            "Observation or exact preview expired; new preparation and approval required")
    privilege_check(p["privileges"], p["environment"], p["operation"])
    payload_path = safe_path(path.parent / "payload.json", project)
    body = common._json(payload_path)
    require(body == p.get("payload") == batch_body(p["observation"])
            and digest(body) == p.get("payloadSha256"), "Payload changed or is not the approved single sparse part")
    return project, path, p, payload_path


def shared_post(preview, payload_path):
    """Only the declared shared CLI sends HTTP/auth; no transport fallback."""
    read = read_request(preview["request"])
    workflow.configured_context(read)
    command = [sys.executable, str(workflow.REPO / "core/fusion-api/rest-api-client/scripts/fusion_rest_client.py"),
               preview["environment"]["host"] + BATCH_ROOT, "--method", "POST", "--raw",
               "--body", json.dumps(preview["payload"], separators=(",", ":")),
               "--timeout", "45", "--callback-timeout", "60"]
    for key, value in preview["headers"].items():
        command.extend(["--header", key + "=" + value])
    try:
        run = subprocess.run(command, cwd=workflow.REPO, capture_output=True, text=True, timeout=90, check=False)
        require(run.returncode == 0, "Shared batch request failed or is uncertain; do not retry")
        return json.loads(run.stdout)
    except (subprocess.TimeoutExpired, ValueError):
        raise BatchError("Shared batch response failed, timed out or is uncertain; reconcile before retry",
                         "transport/environment") from None


def response_summary(response, preview):
    require(isinstance(response, dict) and set(response) == {"parts"}
            and isinstance(response["parts"], list) and len(response["parts"]) == 1,
            "Unexpected batch envelope; outcome is uncertain")
    part = response["parts"][0]
    expected = preview["payload"]["parts"][0]
    require(isinstance(part, dict) and part.get("id") == expected["id"]
            and part.get("operation") == "update" and not any(k in part for k in ("error", "errors", "o:errorDetails")),
            "Batch part failed or mismatched; outer HTTP success is insufficient")
    if "status" in part:
        require(type(part["status"]) is int and 200 <= part["status"] < 300, "Batch part status is not successful")
    path = part.get("path")
    require(isinstance(path, str), "Missing batch response identity")
    item_path(path, preview["environment"]["host"], preview["observation"]["canonicalKey"])
    payload = part.get("payload")
    require(isinstance(payload, dict) and payload.get("learningCatalogProfileNumber") == preview["request"]["number"]
            and all(field in payload and payload[field] == value for field, value in expected["payload"].items()),
            "Response does not confirm requested identity and changed attributes; readback required")
    return {"status": "response_verified_readback_pending", "profileNumber": preview["request"]["number"],
            "readbackVerified": False, "processingComplete": False, "retryAllowed": False}


def submit(*, preview_path, project_root, approved_preview_sha256, approve=False, post=None):
    require(approve is True, "Later explicit approval of this exact target and payload is required")
    project, path, p, payload_path = frozen(preview_path, project_root, approved_preview_sha256)
    # Reissuing a preview cannot automatically replay the same approved request.
    key = digest({"environment": p["environment"], "route": ROUTE, "payload": p["payload"]})
    run_dir = safe_path(project / "state/runs/cap-batch-updates", project)
    run_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    attempt, receipt = run_dir / (key + ".attempt.json"), run_dir / (key + ".result.json")
    save_new(attempt, {"status": "attempt_started", "previewSha256": approved_preview_sha256,
                      "payloadSha256": p["payloadSha256"], "retryAllowed": False, "recordedAt": now_utc().isoformat()})
    try:
        summary = response_summary((post or shared_post)(p, payload_path), p)
    except BaseException:
        try:
            save_new(receipt, {"status": "failed_or_uncertain", "retryAllowed": False, "readbackVerified": False})
        except (OSError, ValueError):
            pass
        raise BatchError("Batch attempt failed or is uncertain; marker retained, reconcile with reads before any retry",
                         "Fusion API") from None
    try:
        save_new(receipt, summary)
    except (OSError, ValueError):
        summary["warning"] = "Response confirmed update but receipt persistence failed; do not resubmit"
    return {**summary, "attemptPath": str(attempt), "receiptPath": str(receipt)}


def verify(*, preview_path, project_root, get=None):
    project = safe_path(project_root, workflow.REPO / "project").resolve(strict=True)
    retained = common._json(safe_path(preview_path, project))
    p = retained["preview"]
    require(digest(p) == retained.get("previewSha256") and batch_body(p["observation"]) == p["payload"],
            "Verification preview integrity failed")
    require(p.get("route") in {ROUTE, LEGACY_ROUTE}, "Wrong verification route")
    # Verification deliberately permits an expired preview: no mutation occurs.
    request = dict(p["request"])
    if "name" in request["changes"]:
        request["expected_name"] = request["changes"]["name"]
    observed = observation(request, get=get)
    result = policy.verify_readback({"baseline": p["observation"]["baseline"],
                                    "intendedFields": p["payload"]["parts"][0]["payload"]}, [observed["baseline"]], complete=True)
    result["route"] = ROUTE
    result["loaderCompletionApplicable"] = False
    result["executionAttribution"] = "Current state comparison only; consult the retained submission receipt for execution evidence"
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("inspect", "prepare", "submit", "verify"))
    parser.add_argument("--request-stdin", action="store_true")
    parser.add_argument("--execute-read", action="store_true")
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--privilege-assessment", type=Path)
    parser.add_argument("--preview", type=Path)
    parser.add_argument("--approved-preview-sha256")
    parser.add_argument("--approve", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.operation in {"inspect", "prepare", "verify"}:
            require(args.execute_read, "Explicit routed read authorization is required")
        if args.operation in {"inspect", "prepare"}:
            require(args.request_stdin, "Request stdin is required")
            request = json.load(sys.stdin)
        if args.operation == "inspect":
            result = observation(request)
        elif args.operation == "prepare":
            result = prepare(request, project_root=args.project_root, output_dir=args.output_dir,
                             privilege_path=args.privilege_assessment)
        elif args.operation == "submit":
            result = submit(preview_path=args.preview, project_root=args.project_root,
                            approved_preview_sha256=args.approved_preview_sha256, approve=args.approve)
        else:
            result = verify(preview_path=args.preview, project_root=args.project_root)
    except (ValueError, OSError, TypeError, KeyError) as exc:
        # Never persist/print raw shared auth/HTTP output or exception payloads.
        result = {"status": "blocked_or_uncertain" if args.operation == "submit" else "blocked",
                  "message": str(exc) if isinstance(exc, BatchError) else "Batch workflow did not complete; inspect local input/readiness and retained attempt state. No automatic retry.",
                  "failure_class": exc.failure_class if isinstance(exc, BatchError) else "artifact_persistence" if isinstance(exc, OSError) else "input_validation",
                  "writeEligible": False}
        print(json.dumps(result, indent=2))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
