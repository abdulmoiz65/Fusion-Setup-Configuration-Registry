#!/usr/bin/env python3
"""CPQ approval binding and single-use handoff to the unchanged Core Data Loader."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import time
import uuid
import unicodedata
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cpq_execution as execution
import cpq_live_contract as live
import cpq_evidence_store as evidence_store
import cpq_reconciliation_discovery as reconciliation_discovery

ROOT = Path(__file__).resolve().parents[6]
TASK = "ORA_CPQ_SETUP_ASSISTANT"
TASK_NAME = "CPQ Setup Assistant"
STAGES = ("INITIALIZE", "IMPORT_COMPANY_AND_ADMINS", "SUBMIT")
MAX_TTL = 900
STATE_PATH = "state/cpq-setup-assistant/approvals.sqlite3"
SKILL_PATH = Path("pillars/cx/configure-price-quote/company-profile/cpq-setup-assistant")
COORDINATION_PATH = SKILL_PATH / ".runtime/submission-locks.sqlite3"
DISCOVERY_PATH = "/crmRestApi/resources/latest/setupAssistants/SA_SETUP_ASSISTANT"
DISCOVERY_QUERY = {"expand": "CPQRoleMappings,CPQUsers,CPQStarterDataImport,CompanyProfiles,SetupProgress", "onlyData": "true"}
TRANSPORT_FIELDS = {"RestAction", "REST-Framework-Version", "Content-Type"}


class GuardError(ValueError):
    """A local, safe-to-display blocker."""


def capabilities():
    """Only guarantees implemented by this declared route; no inferred server support."""
    return {"schemaVersion": "cpq-capabilities/1", "guarantees": {
        "checkout-target-locking": True, "authenticated-actor": False,
        "server-side-conditional-write": False, "cross-host-locking": False,
        "non-bypassable-execution": False, "safe-post-handoff-unlock": False},
        "approvalMode": "explicit-local", "liveApprovalAvailable": True,
        "blocker": None,
        "limitations": "Actor attribution is caller-supplied, not authenticated. ATEAM-1461 recommendation 3 remains unmet."}


def check_required_guarantees(proposal):
    required = proposal.get("requiredGuarantees", [])
    require(isinstance(required, list) and all(isinstance(item, str) for item in required),
            "requiredGuarantees must be a list of capability names.")
    available = capabilities()["guarantees"]
    require(all(available.get(item) is True for item in required),
            "A required guarantee is unsupported by the declared CPQ route; inspect capabilities and stop.")


def require(condition, message):
    if not condition:
        raise GuardError(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def core():
    sys.path.insert(0, str(ROOT / "core/data-loader/scripts"))
    import upload_and_initiate
    return upload_and_initiate


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalized_target(proposal):
    """HTTPS origin and case-sensitive environment identity; never include credentials."""
    host, environment = proposal.get("host"), proposal.get("environment")
    require(isinstance(host, str) and not any(c.isspace() for c in host), "Invalid target origin.")
    try:
        url = urlsplit(host)
        name = (url.hostname or "").encode("idna").decode("ascii").lower().removesuffix(".")
        port = url.port
    except (ValueError, UnicodeError):
        raise GuardError("Invalid target origin.") from None
    require(url.scheme.lower() == "https" and name and len(name) <= 253
            and all(re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label) for label in name.split("."))
            and (port is None or port > 0)
            and url.username is None and url.password is None and url.path in ("", "/")
            and not url.query and not url.fragment and "?" not in host and "#" not in host,
            "Target must be an HTTPS DNS origin without credentials, path, query, or fragment.")
    require(isinstance(environment, str) and environment.strip()
            and not any(ord(c) < 32 or ord(c) == 127 for c in environment), "Invalid environment identifier.")
    origin = "https://" + name + (f":{port}" if port not in (None, 443) else "")
    return {"host": origin, "environment": unicodedata.normalize("NFC", environment.strip())}


def execution_settings(preflight):
    """The supported non-secret CPQ prepared-DAT execution contract."""
    require({"taskRouted", "sourceType", "supportsRunBookTaskCode", "runID", "uploadFileName"} <= preflight.keys(),
            "Required execution settings are missing.")
    require(preflight.get("taskRouted") is True and preflight.get("sourceType") is None
            and type(preflight.get("supportsRunBookTaskCode")) is bool,
            "Unsupported execution routing settings.")
    run_id = preflight.get("runID")
    require(isinstance(run_id, str) and bool(run_id.strip()), "A configured Run Book is required.")
    name = preflight.get("uploadFileName")
    require(isinstance(name, str) and name and Path(name).name == name and name.endswith(".zip"),
            "Invalid upload filename setting.")
    require(not any(preflight.get(k) for k in (
        "cxImportHighVolumeLoad", "cxImportObjectCode", "cxUcmAccount", "cxFiles", "fbdiBusinessObject",
        "fbdiUcmAccount", "fbdiFiles", "fbdiLoadAdapterInterfaceId")), "Alternate loader settings are not supported for CPQ.")
    return {"executionRoute": "data-loader", "fileAction": "IMPORT_AND_LOAD", "sourceType": None,
            "taskRouted": True, "runID": run_id,
            "supportsRunBookTaskCode": preflight["supportsRunBookTaskCode"],
            "uploadFileName": name, "ucmAccount": "hcm$/dataloader$/import$",
            "wrapperAttempts": 1, "adapterPolicy": "core.data-loader",
            "initiationOptions": dict(execution.INITIATION_OPTIONS)}


def archive_rows(content, loader):
    """Inspect the already validated DAT archive; never rebuild the source."""
    rows = []
    for member_name, member_content in live.contract.archive_members(content):
        sections = loader.metadata.parse_source_sections(member_content, source_name="CPQ archive")
        headers = {section.discriminator: section.attributes for section in sections}
        require(len(headers) == len(sections) and all(len(set(h)) == len(h) for h in headers.values()),
                "Duplicate DAT sections or attributes.")
        for line in live.contract._lines(member_content):
            if not line:
                continue
            if line.startswith("METADATA|") or live.contract._COMMENT.fullmatch(line):
                continue
            fields = line.split("|")
            require(len(fields) >= 3 and fields[0] == "MERGE" and fields[1] in headers,
                    "Unsupported CPQ DAT directive or section.")
            require(len(fields[2:]) == len(headers[fields[1]]), "Malformed CPQ DAT row.")
            values = dict(zip(headers[fields[1]], fields[2:]))
            require("SAMPLE_VALUE" not in values.values(), "Unresolved transport placeholder.")
            rows.append({"section": fields[1], "values": values})
    require(bool(rows), "CPQ archive has no operations.")
    return rows


def validate_scope(stage, rows, target):
    """Fail closed on mixed stages and unsupported operations."""
    sections = [r["section"] for r in rows]
    require(stage in STAGES, "Unknown CPQ mutation type.")
    if stage == "INITIALIZE":
        require(target == {"scope": "environment", "businessObject": "cpqSetupAssistantInitialize"},
                "Initialization requires an explicit environment-scoped initialization target.")
        require(sections == ["cpqSetupAssistantInitialize"],
                "Initialization must contain exactly one initialization row.")
        require("Status" not in rows[0]["values"], "Initialization cannot submit status.")
        require(rows[0]["values"].get("RestAction", "POST").upper() == "POST",
                "Initialization must use POST.")
        return
    require(isinstance(target, dict) and isinstance(target.get("assistantName"), str)
            and bool(target["assistantName"].strip()), "Discovered assistant target is required.")
    require(sections.count("setupAssistants") == 1, "Exactly one assistant parent is required.")
    for row in rows:
        values = {k: v for k, v in row["values"].items() if v != ""}
        section = row["section"]
        require("IsDataExisting" not in values, "IsDataExisting is read-only.")
        if section == "setupAssistants":
            if "Name" in values:
                require(values["Name"] == target["assistantName"], "Assistant target mismatch.")
            allowed = {"Name", "RestAction", "REST-Framework-Version", "Content-Type"}
            if stage == "SUBMIT":
                allowed.add("Status")
                require(values.get("Status") == "SUBMITTED", "Submission must set Status=SUBMITTED.")
            require(set(values) <= allowed, "Unsupported parent field or mixed mutation stages.")
            require(values.get("RestAction", "PATCH").upper() == "PATCH",
                    "Assistant parent must use the registered PATCH operation.")
        elif section == "CompanyProfiles":
            require(stage == "IMPORT_COMPANY_AND_ADMINS" and "Status" not in values,
                    "Company Profile changes belong only to the child import.")
            require(bool(target.get("companyProfileId")), "Discovered Company Profile target is required.")
            require(values.get("CompanyProfileId") == str(target["companyProfileId"]),
                    "Company Profile target mismatch.")
            require(values.get("RestAction", "PATCH").upper() == "PATCH",
                    "Company Profile must use PATCH.")
        elif section == "CPQUsers":
            require(stage == "IMPORT_COMPANY_AND_ADMINS", "Administrators belong only to the child import.")
            require(all(values.get(k, "").strip() for k in ("FirstName", "LastName", "Email")),
                    "New administrators require first name, last name, and email.")
            require(not set(values) & {"CPQUserId", "Id", "PartyNumber", "UserName", "Status"},
                    "Generated identities and status are not allowed for new administrators.")
            require(values.get("RestAction", "POST").upper() == "POST", "Administrators must use POST.")
        else:
            raise GuardError("Unrecognized CPQ section.")
    if stage == "SUBMIT":
        require(sections == ["setupAssistants"], "Submission cannot contain child operations.")
    else:
        require(sections.count("CompanyProfiles") <= 1 and len(sections) > 1,
                "Child import needs children and at most one Company Profile update.")


def inspect(proposal_path, preflight_path, task_path, loader=None):
    loader = loader or core()
    proposal = read_json(proposal_path)
    preflight = loader.load_preflight_envelope(Path(preflight_path))
    artifact = loader._approved_artifact(preflight)
    task = read_json(task_path)
    preview = task.get("preview", {})
    require(preview.get("taskCode") == TASK and preview.get("taskName") == TASK_NAME
            and preview.get("executionRoute") == "data-loader",
            "A CPQ Data Loader Task Validator preview is required.")
    require(preflight.get("taskRouted") is True and preflight.get("sourceType") is None
            and preflight.get("mappingComplete") is True, "Incomplete or unsupported Core preflight.")
    final_data = preview.get("finalData")
    require(isinstance(final_data, dict) and final_data.get("archiveSha256") ==
            loader.archive_sha256(artifact.content), "Task preview does not match the exact archive.")
    require(normalized_target(proposal) == normalized_target(preflight),
            "Proposal and Core preflight targets differ.")
    execution_settings(preflight)
    rows = archive_rows(artifact.content, loader)
    validate_scope(proposal.get("stage"), rows, proposal.get("target"))
    # Include all preview/finalData and preflight fields, not merely taskCode/route.
    binding = {"proposal": proposal, "preflight": preflight, "preview": preview, "operations": rows}
    return binding, artifact, task


def build_manifest(binding, *, ttl=MAX_TTL, now=None, nonce=None):
    """Create the complete reviewable manifest BEFORE requesting approval."""
    require(type(ttl) in (int, float) and math.isfinite(ttl) and 0 < ttl <= MAX_TTL,
            "Manifest validity must be between 1 and 900 seconds.")
    now = time.time() if now is None else now
    base = {k: binding[k] for k in ("proposal", "preflight", "preview", "operations", "liveValidation")}
    p = base["proposal"]
    evidence = base["liveValidation"]
    require(isinstance(evidence, dict) and evidence.get("schemaVersion") == "cpq-live-validation/1"
            and {"intent", "state", "taskEvidence", "taskInputPath", "effectiveRoute"} <= evidence.keys(),
            "A live-validated preview is required; regenerate legacy manifests.")
    require(evidence["intent"].get("artifactSha256") == base["preview"]["finalData"]["archiveSha256"]
            and evidence["intent"].get("stage") == execution.STAGES[p["stage"]]
            and [{"section": op["section"], "values": dict(op["fields"])}
                 for op in evidence["intent"].get("operations", [])] == base["operations"]
            and evidence["effectiveRoute"] == execution.route(base["preflight"]),
            "Live evidence differs from the approved intent or route.")
    check_required_guarantees(p)
    require(base["preview"].get("taskCode") == TASK and base["preview"].get("taskName") == TASK_NAME,
            "Exact CPQ task code and name are required.")
    require(normalized_target(p) == normalized_target(base["preflight"]), "Target mismatch.")
    validate_scope(p.get("stage"), base["operations"], p.get("target"))
    admins = [row["values"] for row in base["operations"] if row["section"] == "CPQUsers"]
    profiles = sum(row["section"] == "CompanyProfiles" for row in base["operations"])
    # Generate the summary from scope/counts, never raw names, emails, or business values.
    summaries = {
        "INITIALIZE": "Initialize CPQ Setup Assistant in the selected environment.",
        "IMPORT_COMPANY_AND_ADMINS": f"Update {profiles} Company Profile record(s) and create {len(admins)} administrator(s).",
        "SUBMIT": "Submit the selected CPQ setup by setting Status to SUBMITTED.",
    }
    return dict(base, schemaVersion="cpq-approval-manifest/3", stage=p["stage"],
                taskCode=TASK, taskName=TASK_NAME,
                target=dict(normalized_target(p), target=p["target"]),
                executionSettings=execution_settings(base["preflight"]),
                archiveSha256=base["preview"]["finalData"]["archiveSha256"],
                administratorSet=admins, redactedBusinessSummary=summaries[p["stage"]],
                createdAt=now, expiresAt=now + ttl, nonce=nonce or str(uuid.uuid4()))


def validate_manifest(manifest, now):
    require(isinstance(manifest, dict), "A canonical CPQ manifest is required.")
    require({"proposal", "preflight", "preview", "operations", "schemaVersion", "stage", "target",
             "archiveSha256", "administratorSet", "redactedBusinessSummary", "createdAt", "expiresAt", "nonce",
             "taskCode", "taskName", "executionSettings", "liveValidation"}
            <= manifest.keys(), "Required canonical manifest fields are missing.")
    created, expires = manifest.get("createdAt"), manifest.get("expiresAt")
    require(all(type(v) in (int, float) and math.isfinite(v) for v in (created, expires)),
            "Manifest timestamps are missing or invalid.")
    require(created <= now < expires, "Manifest is expired or its time is invalid.")
    nonce = manifest.get("nonce")
    require(isinstance(nonce, str) and re.fullmatch(
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", nonce),
        "Manifest requires its preview-generated UUID nonce.")
    expected = build_manifest(manifest, ttl=expires - created, now=created, nonce=nonce)
    require(manifest == expected, "Manifest fields are missing or do not match the prepared proposal.")


def validate_historical_manifest(manifest, now):
    """Read/recovery only, after the caller matched a consumed ledger digest.

    Version 2 records cannot gain live-validation evidence retrospectively. Keep
    their status/pre-handoff recovery available, never approve or execute them.
    """
    if manifest.get("schemaVersion") != "cpq-approval-manifest/2":
        return validate_manifest(manifest, now)
    require({"proposal", "preflight", "preview", "operations", "stage", "target", "archiveSha256",
             "administratorSet", "redactedBusinessSummary", "createdAt", "expiresAt", "nonce",
             "taskCode", "taskName", "executionSettings"} <= manifest.keys(), "Incomplete historical manifest.")
    created, expires = manifest["createdAt"], manifest["expiresAt"]
    require(all(type(v) in (int, float) and math.isfinite(v) for v in (created, expires))
            and created <= now < expires and 0 < expires - created <= MAX_TTL,
            "Historical approval time is invalid.")
    require(manifest["taskCode"] == TASK and manifest["taskName"] == TASK_NAME
            and manifest["stage"] == manifest["proposal"].get("stage")
            and normalized_target(manifest["proposal"]) == normalized_target(manifest["preflight"]),
            "Historical task or target differs.")
    validate_scope(manifest["stage"], manifest["operations"], manifest["proposal"]["target"])


def manifest_path(path):
    path = Path(path).resolve()
    require(any(path.is_relative_to(root) for root in (Path(tempfile.gettempdir()).resolve(), Path('/tmp').resolve()))
            and not path.is_relative_to(ROOT.resolve()),
            "Keep the manifest in protected temporary storage outside the repository/project.")
    return path


def save_manifest(manifest, path):
    path = manifest_path(path)
    # No overwrite: a new preview must use a new file and a new nonce.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(canonical_bytes(manifest))
        stream.flush()
        os.fsync(stream.fileno())


def load_manifest(path, binding):
    manifest = read_json(manifest_path(path))
    validate_manifest(manifest, time.time())
    require(all(manifest.get(k) == v for k, v in binding.items()),
            "Prepared data changed since manifest creation; preview and approve again.")
    return manifest


def ledger(project):
    project = Path(project).resolve()
    require(project.parent == (ROOT / "project").resolve() and project.name != "_template"
            and (project / "state").is_dir(), "Select an existing project/<project_id> workspace.")
    path = project / STATE_PATH
    require(path.resolve().is_relative_to(project), "Unsafe approval ledger path.")
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    connection = sqlite3.connect(path, timeout=10)
    os.chmod(path, 0o600)
    connection.execute("PRAGMA synchronous=FULL")
    connection.execute("CREATE TABLE IF NOT EXISTS approvals (nonce TEXT PRIMARY KEY, binding TEXT, "
                       "target TEXT, stage TEXT, issued REAL, expires REAL, used REAL)")
    connection.execute("CREATE TABLE IF NOT EXISTS approval_records (nonce TEXT PRIMARY KEY, fingerprint TEXT NOT NULL)")
    connection.execute("CREATE TABLE IF NOT EXISTS reconciliations (id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL)")
    connection.execute("CREATE TABLE IF NOT EXISTS reconciliation_current (child_nonce TEXT PRIMARY KEY, id TEXT NOT NULL)")
    connection.execute("CREATE TABLE IF NOT EXISTS submission_jobs (nonce TEXT PRIMARY KEY, request_id TEXT, content_id TEXT)")
    connection.execute("CREATE TABLE IF NOT EXISTS submission_status_checks (nonce TEXT, observed REAL, report TEXT)")
    registry = ROOT / COORDINATION_PATH
    require(registry.resolve().is_relative_to((ROOT / SKILL_PATH).resolve()), "Unsafe shared lock registry path.")
    attach_coordination(connection, registry)
    migrate_legacy_locks(connection, project)
    return connection


def attach_coordination(connection, path):
    """Attach the checkout registry to the project transaction (SQLite super-journal)."""
    path = Path(path).resolve()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    require(connection.execute("PRAGMA journal_mode=DELETE").fetchone()[0] == "delete",
            "Project approval ledger must use rollback journaling for atomic shared locks.")
    connection.execute("ATTACH DATABASE ? AS coordination", (str(path),))
    os.chmod(path, 0o600)
    require(connection.execute("PRAGMA coordination.journal_mode=DELETE").fetchone()[0] == "delete",
            "Shared lock registry must use rollback journaling.")
    connection.execute("PRAGMA coordination.synchronous=FULL")
    connection.execute("CREATE TABLE IF NOT EXISTS coordination.stage_attempts "
                       "(nonce TEXT PRIMARY KEY, target TEXT NOT NULL, stage TEXT NOT NULL, completed INTEGER NOT NULL)")
    connection.execute("CREATE TABLE IF NOT EXISTS coordination.attempt_phases (nonce TEXT PRIMARY KEY, phase TEXT NOT NULL)")
    connection.execute("CREATE TABLE IF NOT EXISTS coordination.submission_locks "
                       "(target TEXT PRIMARY KEY, nonce TEXT NOT NULL, phase TEXT NOT NULL, updated REAL NOT NULL)")


def migrate_legacy_locks(connection, project):
    """Import retained project-local locks before any new-version execution.

    Other projects are read-only; their old local tables are retired when that
    project next opens through this guard. Never discard an uncertain lock.
    """
    legacy = []
    for path in (ROOT / "project").glob("*/" + STATE_PATH):
        if path.resolve() == (project / STATE_PATH).resolve():
            source = connection
        else:
            source = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
        try:
            if source.execute("SELECT 1 FROM main.sqlite_master WHERE type='table' AND name='submission_locks'").fetchone():
                legacy.extend(source.execute("SELECT target, nonce, phase, updated FROM main.submission_locks").fetchall())
        finally:
            if source is not connection:
                source.close()
    with connection:
        connection.execute("BEGIN IMMEDIATE")
        for row in legacy:
            existing = connection.execute("SELECT nonce FROM coordination.submission_locks WHERE target=?", (row[0],)).fetchone()
            require(existing is None or existing[0] == row[1], "Conflicting legacy submission locks; retain them and resolve the status blocker.")
            connection.execute("INSERT OR IGNORE INTO coordination.submission_locks VALUES (?, ?, ?, ?)", row)
        connection.execute("DROP TABLE IF EXISTS main.submission_locks")


def target_digest(binding):
    p = binding["proposal"]
    return digest(dict(normalized_target(p), target=p.get("target")))


def submission_target(binding):
    # The declared endpoint identifies one assistant per origin. Different environment
    # labels, profile IDs, or proposal metadata must not evade its submission lock.
    return digest({"origin": normalized_target(binding["proposal"])["host"], "resource": DISCOVERY_PATH})


def require_unlocked(db, binding):
    require(db.execute("SELECT 1 FROM coordination.submission_locks WHERE target=?", (submission_target(binding),)).fetchone() is None,
            "This setup has a retained submission lock; use the declared recovery/status workflow.")


def require_no_pending_stage(db, binding):
    pending = db.execute("SELECT nonce FROM coordination.stage_attempts WHERE target=? AND completed=0 "
                         "AND stage IN ('INITIALIZE', 'IMPORT_COMPANY_AND_ADMINS') AND nonce<>?",
                         (submission_target(binding), binding.get("nonce", ""))).fetchone()
    require(pending is None,
            "An earlier initialization or child import is unresolved; reconcile its exact job before another mutation.")


def check_submission_state(binding, response):
    profiles, users = compare_current_state(binding, response)
    evidence = binding["proposal"]["rediscovery"]
    require(profiles == evidence.get("companyProfileSha256") and users == evidence.get("cpqUsersSha256")
            and digest({k: response.get(k) for k in ("Id", "Name", "Status")}) == evidence.get("assistantSha256"),
            "Fusion state changed since approval; reconcile and obtain a new final approval.")


def recover_submission(db, binding, approval_record, properties):
    """Release only a lock whose owner provably has not entered Core handoff."""
    require(binding.get("stage") == "SUBMIT", "Recovery requires the locked final manifest.")
    key, nonce = submission_target(binding), binding.get("nonce")
    with db:
        db.execute("BEGIN IMMEDIATE")
        row = db.execute("SELECT binding, issued, used FROM approvals WHERE nonce=?", (nonce,)).fetchone()
        require(row is not None and row[0] == digest(binding) and row[2] is not None,
                "Recovery requires the consumed final approval.")
        validate_historical_manifest(binding, row[1])
        require(isinstance(approval_record, dict)
                and approval_record == approval_payload(binding, approval_record.get("actor"), row[1]),
                "Recovery approval record does not match.")
        fingerprint = db.execute("SELECT fingerprint FROM approval_records WHERE nonce=?", (nonce,)).fetchone()
        require(fingerprint is not None and fingerprint[0] == digest(approval_record), "Recovery approval integrity check failed.")
        lock = db.execute("SELECT nonce, phase FROM coordination.submission_locks WHERE target=?", (key,)).fetchone()
        require(lock is not None and lock[0] == nonce and lock[1] in {"checking", "precheck_failed"},
                "Submission may have reached Data Loader; retain the lock and inspect the identified load/status. No automatic release is safe.")
    response = read_current_state(binding, properties)
    compare_current_state(binding, response)  # Identity, eligible status, and complete current records.
    with db:
        db.execute("BEGIN IMMEDIATE")
        deleted = db.execute("DELETE FROM coordination.submission_locks WHERE target=? AND nonce=? AND phase IN ('checking','precheck_failed')",
                             (key, nonce)).rowcount
        require(deleted == 1, "Submission entered handoff during recovery; lock retained.")
        child_nonce = binding["proposal"]["rediscovery"].get("afterNonce", "existing:" + submission_target(binding))
        db.execute("UPDATE reconciliation_current SET id=? WHERE child_nonce=?", (str(uuid.uuid4()), child_nonce))
    return {"status": "released_before_handoff", "nonce": nonce,
            "nextAction": "Run reconciliation and build a new final manifest with separate approval; the old nonce remains consumed."}


def retain_job_ids(db, nonce, result):
    request_id, content_id = str(result.get("RequestId") or ""), str(result.get("ContentId") or "")
    request_id = request_id if re.fullmatch(r"[1-9][0-9]*", request_id) else None
    content_id = content_id if re.fullmatch(r"UCMFA[0-9]+", content_id) else None
    db.execute("INSERT OR REPLACE INTO submission_jobs VALUES (?, ?, ?)", (nonce, request_id, content_id))


def inspect_submission(db, binding, approval_record, properties):
    """Read only the recorded load; status alone never releases an uncertain lock."""
    require(binding.get("stage") == "SUBMIT", "Status inspection requires the attempted final manifest.")
    nonce = binding.get("nonce")
    row = db.execute("SELECT binding, issued, used FROM approvals WHERE nonce=?", (nonce,)).fetchone()
    require(row is not None and row[0] == digest(binding) and row[2] is not None, "No matching submission attempt.")
    validate_historical_manifest(binding, row[1])
    require(isinstance(approval_record, dict)
            and approval_record == approval_payload(binding, approval_record.get("actor"), row[1]), "Status approval does not match.")
    fingerprint = db.execute("SELECT fingerprint FROM approval_records WHERE nonce=?", (nonce,)).fetchone()
    require(fingerprint is not None and fingerprint[0] == digest(approval_record), "Status approval integrity check failed.")
    lock = db.execute("SELECT nonce FROM coordination.submission_locks WHERE target=?", (submission_target(binding),)).fetchone()
    require(lock is not None and lock[0] == nonce, "Submission lock ownership differs.")
    identifiers = db.execute("SELECT request_id, content_id FROM submission_jobs WHERE nonce=?", (nonce,)).fetchone()
    require(identifiers is not None and any(identifiers), "No authoritative request/content ID was captured; retain the lock and escalate the unknown outcome.")
    core()
    import get_data_load_info as status_client
    field, value, query = status_client._data_set_lookup(identifiers[0] or identifiers[1])
    response = read_declared_json(binding, properties, status_client.DATA_SETS_PATH,
                                 {"q": query, "onlyData": "true", "limit": "500"})
    require(isinstance(response, dict) and response.get("hasMore") is False
            and isinstance(response.get("items"), list) and len(response["items"]) == 1,
            "Load status is missing, incomplete, or ambiguous; retain the submission lock.")
    data_set = response["items"][0]
    match_field = "DataSetRequestId" if field == "RequestId" else "UcmContentId"
    require(isinstance(data_set, dict) and str(data_set.get(match_field)) == value, "Load status returned a different request.")
    assistant = read_submission_assistant(binding, properties)
    require(isinstance(assistant, dict) and assistant.get("Name") == binding["proposal"]["target"]["assistantName"],
            "Status lookup returned a different assistant.")
    load_status = data_set.get("DataSetStatus")
    report = {"nonce": nonce, field: value, "observedAt": time.time(), "lockRetained": True,
              "releasePermitted": False, "loadStatus": load_status if isinstance(load_status, str)
              and re.fullmatch(r"[A-Z0-9_ -]{1,80}", load_status) else "UNRECOGNIZED",
              "assistantStatus": assistant.get("Status") if assistant.get("Status") in
              {"SETUP_NOT_DONE", "SUBMITTED", "IN_PROGRESS", "ERROR", "COMPLETED"} else "UNRECOGNIZED",
              "statusSha256": digest(response), "assistantSha256": digest(assistant),
              "blocker": "The declared status contract does not prove that a pending submission cannot apply later."}
    with db:
        db.execute("INSERT INTO submission_status_checks VALUES (?, ?, ?)", (nonce, report["observedAt"], canonical_bytes(report).decode()))
    return report


def inspect_child_outcome(db, binding, approval_record, properties):
    """Assess observed effects without granting retry authority or clearing markers."""
    with execution_lock(binding):
        require_latest_child(db, binding, approval_record)
        completion_verified = False
        try:
            verify_child_completion(db, binding, properties)
            completion_verified = True
        except (GuardError, live.contract.ContractError):
            pass
        response = read_current_state(binding, properties)
        baseline = binding["liveValidation"]["state"]
        require({k: response.get(k) for k in ("Id", "Name", "Status")} == baseline["assistant"],
                "Assistant changed; outcome remains uncertain.")
        profiles = complete_collection(response, "CompanyProfiles")
        users = complete_collection(response, "CPQUsers")
        require(len(profiles) == 1 and all(profiles[0].get(k) == baseline["CompanyProfiles"][0].get(k)
                for k in ("Id", "CompanyProfileId", "IsDataExisting")), "Company identity changed; outcome remains uncertain.")
        rows = []
        for index, operation in enumerate(binding["operations"]):
            section, values = operation["section"], operation["values"]
            if section == "setupAssistants":
                continue
            candidates = profiles if section == "CompanyProfiles" else [u for u in users if str(u.get("Email", "")).strip().casefold() == values["Email"].strip().casefold()]
            fields = {k: v for k, v in values.items() if k not in TRANSPORT_FIELDS and k not in {"Name", "CompanyProfileId"} and not k.startswith("SourceRef")}
            classification = "uncertain"
            if not candidates:
                classification = "not_observed"
            elif len(candidates) == 1 and all(k in candidates[0] and scalar(candidates[0][k]) == v for k, v in fields.items()):
                classification = "matches_approved"
            rows.append({"operationIndex": index, "section": section, "observation": classification})
        complete = False
        try:
            compare_current_state(binding, response)
            complete = True
        except GuardError:
            pass
        report = {"nonce": binding["nonce"], "observedAt": time.time(), "operations": rows,
                  "completionVerified": completion_verified, "completeStateVerified": complete,
                  "stateSha256": digest(response), "retryPermitted": False, "pendingMarkerRetained": True,
                  "nextAction": "Use full reconciliation when completion and every state change are verified; otherwise resolve the original job without replay. Absence does not prove a write cannot apply later."}
        with db:
            db.execute("INSERT INTO submission_status_checks VALUES (?, ?, ?)", (binding["nonce"], report["observedAt"], canonical_bytes(report).decode()))
        return report


def consumed_approval(db, binding, record):
    row = db.execute("SELECT binding, issued, used FROM approvals WHERE nonce=?", (binding.get("nonce"),)).fetchone()
    require(row is not None and row[0] == digest(binding) and row[2] is not None,
            "Recovery requires the exact consumed approval.")
    validate_historical_manifest(binding, row[1])
    require(isinstance(record, dict) and record == approval_payload(binding, record.get("actor"), row[1]),
            "Recovery approval does not match.")
    saved = db.execute("SELECT fingerprint FROM approval_records WHERE nonce=?", (binding["nonce"],)).fetchone()
    require(saved == (digest(record),), "Recovery approval integrity check failed.")


def recover_prewrite(db, binding, approval_record, properties):
    """Release only a durably proven zero-write attempt; never restore its nonce."""
    nonce = binding.get("nonce")
    with execution_lock(binding):
        consumed_approval(db, binding, approval_record)
        def eligible():
            require(db.execute("SELECT phase FROM coordination.attempt_phases WHERE nonce=?", (nonce,)).fetchone() == ("checking",),
                    "Write boundary reached or unknown; retain the attempt and reconcile without replay.")
            ids = db.execute("SELECT request_id, content_id FROM submission_jobs WHERE nonce=?", (nonce,)).fetchone()
            require(ids is None or not any(ids), "Captured remote identifiers prohibit pre-write release.")
        eligible()
        response = read_current_state(binding, properties)
        baseline = binding["liveValidation"]["state"]["assistant"]
        require(isinstance(response, dict) and response.get("Id") == baseline.get("Id")
                and response.get("Name") == baseline.get("Name") and response.get("Status") == "SETUP_NOT_DONE",
                "Assistant identity or eligibility changed; retain the attempt.")
        with db:
            db.execute("BEGIN IMMEDIATE")
            consumed_approval(db, binding, approval_record)
            eligible()
            db.execute("UPDATE coordination.attempt_phases SET phase='released' WHERE nonce=?", (nonce,))
            db.execute("UPDATE coordination.stage_attempts SET completed=1 WHERE nonce=?", (nonce,))
            if binding["stage"] == "SUBMIT":
                removed = db.execute("DELETE FROM coordination.submission_locks WHERE target=? AND nonce=? AND phase IN ('checking','precheck_failed','handoff','uncertain')",
                                     (submission_target(binding), nonce)).rowcount
                require(removed == 1, "Submission lock cannot be safely released.")
            if binding["stage"] == "IMPORT_COMPANY_AND_ADMINS":
                db.execute("DELETE FROM reconciliation_current WHERE child_nonce IN (SELECT nonce FROM approvals WHERE target=? AND stage='IMPORT_COMPANY_AND_ADMINS')", (target_digest(binding),))
            receipt = binding["proposal"].get("rediscovery", {})
            receipt_key = receipt.get("afterNonce", "existing:" + submission_target(binding))
            db.execute("DELETE FROM reconciliation_current WHERE child_nonce=?", (receipt_key,))
    return {"status": "released_before_write", "nonce": nonce, "nonceConsumed": True,
            "nextAction": "Rebuild current-state evidence and obtain fresh stage-specific approval."}


def existing_source(binding):
    proposal = dict(binding["proposal"])
    proposal.pop("rediscovery", None)
    return digest({"proposal": proposal, **{k: binding[k] for k in ("preflight", "preview", "operations")}})


def require_no_child_history(db, binding):
    # Check checkout-wide history as well as legacy project records. A completed
    # child write must use full child reconciliation, never the existing-state route.
    known = db.execute("SELECT 1 FROM coordination.stage_attempts s LEFT JOIN coordination.attempt_phases p ON p.nonce=s.nonce "
                       "WHERE s.target=? AND s.stage='IMPORT_COMPANY_AND_ADMINS' AND COALESCE(p.phase,'unknown')<>'released'",
                       (submission_target(binding),)).fetchone()
    legacy = db.execute("SELECT 1 FROM approvals a LEFT JOIN coordination.attempt_phases p ON p.nonce=a.nonce "
                        "WHERE a.target=? AND a.stage='IMPORT_COMPANY_AND_ADMINS' AND a.used IS NOT NULL AND COALESCE(p.phase,'unknown')<>'released'",
                        (target_digest(binding),)).fetchone()
    require(known is None and legacy is None, "A child attempt exists; use its exact completion and full reconciliation.")
    require_no_pending_stage(db, binding)


def reconcile_existing(db, binding, artifact, properties, run_config, task_input):
    require(binding["proposal"]["stage"] == "SUBMIT", "Existing-state reconciliation requires a final-only submission artifact.")
    key = "existing:" + submission_target(binding)
    with execution_lock(binding):
        with db:
            db.execute("BEGIN IMMEDIATE")
            require_unlocked(db, binding)
            require_no_child_history(db, binding)
            db.execute("DELETE FROM reconciliation_current WHERE child_nonce=?", (key,))
        evidence = execution.collect(binding, artifact.content, properties, run_config, task_input)
        state = evidence["state"]
        response = read_current_state(binding, properties)
        require({k: response.get(k) for k in ("Id", "Name", "Status")} == state["assistant"], "Assistant changed during existing-state verification.")
        for name in ("CompanyProfiles", "CPQUsers"):
            clean = lambda rows: sorted(({k: v for k, v in row.items() if k != "links"} for row in rows), key=canonical_bytes)
            require(clean(complete_collection(response, name)) == clean(state[name]), "Existing records changed during verification.")
        profiles, users = compare_current_state(binding, response)
        receipt = {"schemaVersion": "cpq-existing-state/1", "reconciliationId": str(uuid.uuid4()),
                   "targetSha256": target_digest(binding), "sourceSha256": existing_source(binding),
                   "observedAt": time.time(), "companyProfileSha256": profiles, "cpqUsersSha256": users,
                   "assistantSha256": digest({k: response.get(k) for k in ("Id", "Name", "Status")})}
        with db:
            db.execute("BEGIN IMMEDIATE")
            require_unlocked(db, binding)
            require_no_child_history(db, binding)
            db.execute("INSERT INTO reconciliations VALUES (?, ?)", (receipt["reconciliationId"], digest(receipt)))
            db.execute("INSERT OR REPLACE INTO reconciliation_current VALUES (?, ?)", (key, receipt["reconciliationId"]))
        return receipt


def check_existing_receipt(db, binding, now):
    require_no_child_history(db, binding)
    receipt = binding["proposal"]["rediscovery"]
    require(db.execute("SELECT fingerprint FROM reconciliations WHERE id=?", (receipt.get("reconciliationId"),)).fetchone() == (digest(receipt),),
            "Existing-state receipt is missing or modified.")
    require(db.execute("SELECT id FROM reconciliation_current WHERE child_nonce=?", ("existing:" + submission_target(binding),)).fetchone() == (receipt.get("reconciliationId"),),
            "Existing-state receipt was superseded; rediscover before approval.")
    require(receipt.get("targetSha256") == target_digest(binding) and receipt.get("sourceSha256") == existing_source(binding),
            "Existing-state receipt does not cover this exact final artifact and route.")
    observed = receipt.get("observedAt")
    require(type(observed) in (int, float) and observed <= now < observed + MAX_TTL and binding.get("createdAt", now) >= observed,
            "Existing-state evidence is expired or postdates approval.")


def check_reconciliation(db, binding, now):
    p = binding["proposal"]
    if p["stage"] != "SUBMIT":
        return
    if p.get("rediscovery", {}).get("schemaVersion") == "cpq-existing-state/1":
        check_existing_receipt(db, binding, now)
        return
    previous = db.execute("SELECT nonce, binding, used FROM approvals WHERE target=? AND "
                          "stage='IMPORT_COMPANY_AND_ADMINS' AND used IS NOT NULL AND NOT EXISTS (SELECT 1 FROM coordination.attempt_phases ap WHERE ap.nonce=approvals.nonce AND ap.phase='released') ORDER BY used DESC LIMIT 1",
                          (target_digest(binding),)).fetchone()
    evidence = p.get("rediscovery", {})
    require(previous is not None, "Final submission requires a recorded child-import attempt.")
    require(isinstance(evidence, dict) and evidence.get("schemaVersion") == "cpq-reconciliation/1",
            "Run CPQ reconciliation; caller-declared verification is not accepted.")
    stored = db.execute("SELECT fingerprint FROM reconciliations WHERE id=?", (evidence.get("reconciliationId"),)).fetchone()
    require(stored is not None and stored[0] == digest(evidence), "Reconciliation receipt is missing or modified.")
    require(evidence.get("afterNonce") == previous[0] and evidence.get("verifiedBinding") == previous[1]
            and evidence.get("targetSha256") == target_digest(binding),
            "Rediscovery must reconcile the latest child import for this target.")
    current = db.execute("SELECT id FROM reconciliation_current WHERE child_nonce=?", (previous[0],)).fetchone()
    require(current is not None and current[0] == evidence["reconciliationId"],
            "A newer reconciliation attempt superseded this receipt; verify current state again.")
    observed = evidence.get("observedAt")
    require(type(observed) in (int, float) and previous[2] < observed <= now < observed + MAX_TTL,
            "Rediscovery must follow the child import and be no more than 900 seconds old.")
    require(evidence.get("allOperationsVerified") is True,
            "Every approved child operation must be verified before submission.")
    require(binding.get("createdAt", now) >= observed, "Final manifest predates verified rediscovery.")
    require(all(isinstance(evidence.get(k), str) and re.fullmatch(r"[0-9a-f]{64}", evidence[k])
                for k in ("companyProfileSha256", "cpqUsersSha256")),
            "Both Company Profile and CPQ-user rediscovery fingerprints are required.")


def read_submission_assistant(binding, properties):
    # A status diagnostic must remain available while children are incomplete or
    # the job is changing state. It never grants mutation or lock-release authority.
    return read_declared_json(binding, properties, DISCOVERY_PATH, {"onlyData": "true"})


def read_current_state(binding, properties):
    """Read complete child collections through fixed declared paths only."""
    try:
        return reconciliation_discovery.discover(
            lambda endpoint, query: read_declared_json(binding, properties, endpoint, query))
    except live.contract.ContractError as error:
        raise GuardError(str(error)) from error


def read_declared_json(binding, properties, endpoint, query):
    sys.path.insert(0, str(ROOT / "core/fusion-api/rest-api-client/scripts"))
    import rest_client_common as client
    props = client.read_properties(Path(properties))
    require(normalized_target({"host": props.get("restBaseUrl"), "environment": props.get("environment")})
            == normalized_target(binding["proposal"]), "Read configuration differs from the approved target.")
    url = client.build_url(props, endpoint, query)
    auth_props = client.props_with_scope_property(props, "scope")
    args = client.build_parser(description="CPQ read-only verification", default_token_cache="auto").parse_args([endpoint])
    token = client.get_token(auth_props, args)
    kwargs = {"method": "GET", "headers": {"REST-Framework-Version": "9", "Accept": "application/json"},
              "json_body": None, "timeout": 30}
    try:
        content, _, status = client.request_bytes(props, url, access_token=token, **kwargs)
    except client.FusionHttpError as exc:
        if exc.status_code not in {401, 403}:
            raise
        token = client.get_token(auth_props, args, force_login=True)
        content, _, status = client.request_bytes(props, url, access_token=token, **kwargs)
    require(status == 200, "Rediscovery did not return a successful record response.")
    return json.loads(content)


def complete_collection(response, name):
    collection = response.get(name)
    require(isinstance(collection, dict) and collection.get("hasMore") is False
            and isinstance(collection.get("items"), list)
            and all(isinstance(row, dict) for row in collection["items"]),
            "Rediscovery must provide complete, unambiguous Company Profile and CPQ-user collections.")
    rows = collection["items"]
    require("count" not in collection or type(collection["count"]) is int and collection["count"] == len(rows),
            "Rediscovery collection count is inconsistent.")
    return rows


def scalar(value):
    require(value is None or type(value) in (str, bool, int, float), "Unverifiable non-scalar discovered value.")
    if value is None:
        return ""
    if type(value) is bool:
        return "true" if value else "false"
    return str(value)


def compare_current_state(binding, response):
    require(isinstance(response, dict) and response.get("Name") == binding["proposal"]["target"]["assistantName"]
            and response.get("Status") == "SETUP_NOT_DONE", "Assistant identity or current status blocks submission.")
    profiles = complete_collection(response, "CompanyProfiles")
    users = complete_collection(response, "CPQUsers")
    target = binding["proposal"]["target"]
    require(bool(target.get("companyProfileId")) and len(profiles) == 1, "Company Profile target is missing or ambiguous.")
    profile = profiles[0]
    ids = [scalar(profile[k]) for k in ("Id", "CompanyProfileId") if k in profile]
    require(bool(ids) and all(value == str(target["companyProfileId"]) for value in ids),
            "Rediscovered Company Profile identity differs from the approved target.")
    # This contract defines every returned CPQUsers record as an administrator.
    require(bool(users), "At least one current CPQ administrator is required.")
    emails = [row.get("Email") for row in users]
    require(all(isinstance(email, str) and email.strip() for email in emails),
            "CPQ-user discovery lacks required email identity fields; verification is blocked.")
    email_keys = [email.strip().casefold() for email in emails]
    require(len(set(email_keys)) == len(email_keys), "Duplicate CPQ-user identities make verification ambiguous.")
    if binding["proposal"]["stage"] == "IMPORT_COMPANY_AND_ADMINS":
        baseline = binding.get("liveValidation", {}).get("state")
        require(isinstance(baseline, dict), "Approved pre-import state is required for complete reconciliation.")
        current = {"assistant": {k: response.get(k) for k in ("Id", "Name", "Status")},
                   "CompanyProfiles": profiles, "CPQUsers": users}
        try:
            live.verify_child_outcome(execution.parsed_binding(binding), baseline, current)
        except live.contract.ContractError as error:
            raise GuardError(str(error)) from error
    approved_emails = []
    for operation in binding["operations"]:
        section, values = operation["section"], operation["values"]
        if section == "setupAssistants":
            continue  # The parent is routing-only during child import; checked above.
        if section == "CompanyProfiles":
            actual = profile
        else:
            require(section == "CPQUsers", "Unsupported child operation during reconciliation.")
            key = values["Email"].strip().casefold()
            approved_emails.append(key)
            matches = [row for row, email in zip(users, email_keys) if email == key]
            require(len(matches) == 1, "An approved administrator is missing or ambiguous.")
            actual = matches[0]
        for field, expected in values.items():
            if field in TRANSPORT_FIELDS or field == "Name" or field.startswith("SourceRef") or section == "CompanyProfiles" and field == "CompanyProfileId":
                continue
            require(field in actual, "Discovery lacks a field required to verify an approved change.")
            require(scalar(actual[field]) == expected, "A current value differs from an approved child change.")
    require(len(set(approved_emails)) == len(approved_emails), "Approved administrator set contains duplicates.")
    # Discovery order and REST navigation links are not business state. Keep
    # operation order untouched; only normalize read-only record collections.
    normalize = lambda rows: sorted(({k: v for k, v in row.items() if k != "links"} for row in rows), key=canonical_bytes)
    return digest(normalize(profiles)), digest(normalize(users))


def require_latest_child(db, binding, record):
    """Verify a consumed approval historically; expiry must not prevent later reconciliation."""
    require(binding.get("stage") == "IMPORT_COMPANY_AND_ADMINS", "Reconciliation requires the child-import manifest.")
    latest = db.execute("SELECT nonce, binding, issued, used FROM approvals WHERE target=? AND "
                        "stage='IMPORT_COMPANY_AND_ADMINS' AND used IS NOT NULL AND NOT EXISTS (SELECT 1 FROM coordination.attempt_phases ap WHERE ap.nonce=approvals.nonce AND ap.phase='released') ORDER BY used DESC LIMIT 1",
                        (target_digest(binding),)).fetchone()
    require(latest is not None and latest[0] == binding.get("nonce") and latest[1] == digest(binding),
            "Reconciliation must use the latest attempted child import for this target.")
    validate_historical_manifest(binding, latest[2])
    require(isinstance(record, dict) and record == approval_payload(binding, record.get("actor"), latest[2]),
            "Child approval record is missing or does not match.")
    fingerprint = db.execute("SELECT fingerprint FROM approval_records WHERE nonce=?", (latest[0],)).fetchone()
    require(fingerprint is not None and fingerprint[0] == digest(record), "Child approval record integrity check failed.")
    return latest[3]


def verify_child_completion(db, binding, properties):
    identifiers = db.execute("SELECT request_id, content_id FROM submission_jobs WHERE nonce=?",
                             (binding["nonce"],)).fetchone()
    require(identifiers is not None and all(identifiers),
            "Child import lacks exact request/content IDs; reconcile the uncertain outcome without replay.")
    return execution.verify_completed_load(binding, {
        "RequestId": identifiers[0], "ContentId": identifiers[1],
        "dataSetName": binding["preflight"]["uploadFileName"],
    }, properties)


def reconcile(db, binding, approval_record, properties):
    reconciliation_id = str(uuid.uuid4())
    with db:
        db.execute("BEGIN IMMEDIATE")
        attempted_at = require_latest_child(db, binding, approval_record)
        # A new observation supersedes old success even if this read/comparison fails.
        db.execute("INSERT INTO reconciliation_current VALUES (?, ?) ON CONFLICT(child_nonce) DO UPDATE SET id=excluded.id",
                   (binding["nonce"], reconciliation_id))
    require(time.time() >= attempted_at, "Local clock predates the child-import attempt.")
    completion = verify_child_completion(db, binding, properties)
    response = read_current_state(binding, properties)
    profile_hash, users_hash = compare_current_state(binding, response)
    observed = time.time()
    require(observed > attempted_at, "Rediscovery must follow the child-import attempt.")
    receipt = {"schemaVersion": "cpq-reconciliation/1", "reconciliationId": reconciliation_id,
               "afterNonce": binding["nonce"], "verifiedBinding": digest(binding),
               "targetSha256": target_digest(binding), "observedAt": observed,
               "allOperationsVerified": True, "loadCompletionSha256": digest(completion), "companyProfileSha256": profile_hash, "cpqUsersSha256": users_hash,
               "assistantSha256": digest({k: response.get(k) for k in ("Id", "Name", "Status")})}
    with db:
        db.execute("BEGIN IMMEDIATE")
        require_latest_child(db, binding, approval_record)  # Reject a child attempt started during the read.
        require(db.execute("SELECT id FROM reconciliation_current WHERE child_nonce=?", (binding["nonce"],)).fetchone()[0]
                == reconciliation_id, "A newer reconciliation started during discovery.")
        db.execute("INSERT INTO reconciliations VALUES (?, ?)", (receipt["reconciliationId"], digest(receipt)))
        db.execute("UPDATE coordination.stage_attempts SET completed=1 WHERE nonce=?", (binding["nonce"],))
    return receipt


def reconcile_initialization(db, binding, approval_record, properties):
    require(binding.get("stage") == "INITIALIZE", "Initialization reconciliation requires its exact manifest.")
    row = db.execute("SELECT binding, issued, used FROM approvals WHERE nonce=?", (binding.get("nonce"),)).fetchone()
    require(row is not None and row[0] == digest(binding) and row[2] is not None,
            "Initialization reconciliation requires the consumed approval.")
    validate_historical_manifest(binding, row[1])
    require(isinstance(approval_record, dict)
            and approval_record == approval_payload(binding, approval_record.get("actor"), row[1]),
            "Initialization approval record does not match.")
    record = db.execute("SELECT fingerprint FROM approval_records WHERE nonce=?", (binding["nonce"],)).fetchone()
    require(record is not None and record[0] == digest(approval_record), "Initialization approval integrity check failed.")
    completion = verify_child_completion(db, binding, properties)
    current = read_current_state(binding, properties)
    require(current.get("Name") == live.ASSISTANT_NAME and current.get("Status") == "SETUP_NOT_DONE"
            and current.get("Id") == binding.get("liveValidation", {}).get("state", {}).get("assistant", {}).get("Id")
            and len(complete_collection(current, "CompanyProfiles")) == 1,
            "Completed initialization has not established one eligible Company Profile.")
    receipt = {"status": "verified", "stage": "INITIALIZE", "nonce": binding["nonce"],
               "observedAt": time.time(), "loadCompletionSha256": digest(completion),
               "stateSha256": digest(current)}
    with db:
        db.execute("BEGIN IMMEDIATE")
        db.execute("INSERT INTO submission_status_checks VALUES (?, ?, ?)",
                   (binding["nonce"], receipt["observedAt"], canonical_bytes(receipt).decode()))
        db.execute("UPDATE coordination.stage_attempts SET completed=1 WHERE nonce=?", (binding["nonce"],))
    return receipt


def approval_payload(binding, actor, approved_at):
    require(isinstance(actor, str) and re.fullmatch(r"[^\s\x00-\x1f\x7f]{1,256}", actor),
            "A nonempty caller-supplied actor label is required for approval audit attribution.")
    return {"schemaVersion": "cpq-approval/1", "manifestSha256": digest(binding),
            "taskCode": TASK, "taskName": TASK_NAME, "archiveSha256": binding["archiveSha256"],
            "finalData": binding["preview"]["finalData"], "target": binding["target"],
            "operations": binding["operations"], "executionSettings": binding["executionSettings"],
            "actor": actor, "approvedAt": approved_at, "expiresAt": binding["expiresAt"], "nonce": binding["nonce"]}


def approve(db, binding, *, confirmed, reviewed_binding, actor=None, now=None):
    require(confirmed is True, "Record approval only after explicit user authorization.")
    require(reviewed_binding == digest(binding), "Proposal changed since the approval preview.")
    now = time.time() if now is None else now
    validate_manifest(binding, now)
    # Explicit-local mode records attribution; it does not authenticate identity.
    payload = approval_payload(binding, actor, now)
    with db:
        db.execute("BEGIN IMMEDIATE")
        check_reconciliation(db, binding, now)
        nonce = binding["nonce"]
        require(db.execute("SELECT 1 FROM approvals WHERE nonce=?", (nonce,)).fetchone() is None,
                "Manifest nonce already approved; create a fresh preview for a new approval.")
        db.execute("INSERT INTO approvals VALUES (?, ?, ?, ?, ?, ?, NULL)",
                   (nonce, digest(binding), target_digest(binding), binding["stage"], now, binding["expiresAt"]))
        db.execute("INSERT INTO approval_records VALUES (?, ?)", (nonce, digest(payload)))
    return {"nonce": nonce, "bindingSha256": digest(binding), "expiresAt": binding["expiresAt"],
            "approvalSha256": digest(payload), "approvalRecord": payload}


def check_approval(db, binding, nonce, now, approval_record=None):
    validate_manifest(binding, now)
    require(nonce == binding["nonce"], "Execution nonce does not match the reviewed manifest.")
    record = db.execute("SELECT binding, issued, expires, used FROM approvals WHERE nonce=?", (nonce,)).fetchone()
    require(record is not None and record[0] == digest(binding), "Approval does not cover this exact proposal.")
    require(record[3] is None, "Approval already used; reconcile before requesting new approval.")
    require(record[1] <= now < record[2], "Approval is expired or its time is invalid.")
    require(record[2] == binding["expiresAt"], "Ledger expiry differs from the approved manifest.")
    require(isinstance(approval_record, dict), "A versioned approval record is required.")
    expected = approval_payload(binding, approval_record.get("actor"), record[1])
    require(approval_record == expected, "Approval record does not match the manifest or approval time.")
    fingerprint = db.execute("SELECT fingerprint FROM approval_records WHERE nonce=?", (nonce,)).fetchone()
    require(fingerprint is not None and fingerprint[0] == digest(approval_record),
            "Approval record integrity check failed.")
    check_reconciliation(db, binding, now)


def execution_lock(binding):
    from cpq_target_lock import TargetLock
    return TargetLock(normalized_target(binding["proposal"])["host"],
                      directory=ROOT / SKILL_PATH / ".runtime/operation-locks")


def execute(db, binding, artifact, task, nonce, properties, run_config, *, approval_record=None, dry_run=False, loader=None):
    require(isinstance(approval_record, dict), "A versioned approval record is required.")
    # Serialize initialization/children/submission through the same local target
    # lock; the durable submission lock remains authoritative after process exit.
    with execution_lock(binding):
        return _execute(db, binding, artifact, task, nonce, properties, run_config,
                        approval_record=approval_record, dry_run=dry_run, loader=loader)


def _execute(db, binding, artifact, task, nonce, properties, run_config, *, approval_record=None, dry_run=False, loader=None):
    loader = loader or core()
    require(isinstance(approval_record, dict), "A versioned approval record is required.")
    require(task.get("preview") == binding["preview"] and loader.archive_sha256(artifact.content) == binding["archiveSha256"],
            "Execution data differs from the manifest.")
    require(execution_settings(binding["preflight"]) == binding["executionSettings"]
            and loader.UCM_DOCUMENT_ACCOUNT == binding["executionSettings"]["ucmAccount"],
            "Execution settings differ from the manifest.")
    check_approval(db, binding, nonce, time.time(), approval_record)
    require_unlocked(db, binding)
    require_no_pending_stage(db, binding)
    # Validate current registration/readiness/state before any possible mutation.
    execution.verify_live(binding, artifact.content, properties, run_config)
    # Prepare private snapshots so execution cannot reopen changed caller files.
    with tempfile.TemporaryDirectory(prefix="cpq-approved-") as directory:
        directory = Path(directory)
        archive = directory / "approved.zip"
        archive.write_bytes(artifact.content)
        os.chmod(archive, 0o600)
        preflight = dict(binding["preflight"], approvedArtifactPath=str(archive))
        envelope = loader.persist_preflight_envelope(preflight, directory / "preflight.json")
        task = dict(task)
        # Same user approval, adapted to Core's existing envelope. Never a second prompt.
        task["approval"] = {"approved": True, "taskCode": TASK, "executionRoute": "data-loader"}
        task_path = directory / "task.json"
        task_path.write_text(json.dumps(task), encoding="utf-8")
        os.chmod(task_path, 0o600)
        loader._require_approved_task_validation(artifact, task_path)
        with db:
            db.execute("BEGIN IMMEDIATE")
            now = time.time()
            check_approval(db, binding, nonce, now, approval_record)
            require_unlocked(db, binding)
            require_no_pending_stage(db, binding)
            if not dry_run:
                # Persist recovery evidence before consuming approval or allowing
                # any upload. This private snapshot is not an approval authority.
                evidence_store.retain(binding, approval_record)
                db.execute("INSERT INTO coordination.stage_attempts VALUES (?, ?, ?, 0)",
                           (nonce, submission_target(binding), binding["stage"]))
                db.execute("INSERT INTO coordination.attempt_phases VALUES (?, 'checking')", (nonce,))
                if binding["stage"] == "SUBMIT":
                    db.execute("INSERT INTO coordination.submission_locks VALUES (?, ?, 'checking', ?)",
                               (submission_target(binding), nonce, now))
                db.execute("UPDATE approvals SET used=? WHERE nonce=?", (now, nonce))
        if dry_run:
            return {"status": "validated", "stage": binding["proposal"]["stage"], "bindingSha256": digest(binding)}
        # Consumption commits BEFORE handoff, including auth failure, crash, or uncertain response.
        # Never restore approval or retry this call.
        is_submission = binding["stage"] == "SUBMIT"
        key = submission_target(binding)
        if is_submission:
            try:
                check_submission_state(binding, read_current_state(binding, properties))
                with db:
                    db.execute("BEGIN IMMEDIATE")
                    validate_manifest(binding, time.time())
                    check_reconciliation(db, binding, time.time())
                    changed = db.execute("UPDATE coordination.submission_locks SET phase='handoff', updated=? "
                                         "WHERE target=? AND nonce=? AND phase='checking'",
                                         (time.time(), key, nonce)).rowcount
                    require(changed == 1, "Submission lock changed during the state check; stop before handoff.")
            except BaseException:
                with db:
                    db.execute("UPDATE coordination.submission_locks SET phase='precheck_failed', updated=? "
                               "WHERE target=? AND nonce=? AND phase='checking'", (time.time(), key, nonce))
                raise
        try:
            def before_upload():
                validate_manifest(binding, time.time())
                execution.verify_live(binding, artifact.content, properties, run_config)
                with db:
                    db.execute("BEGIN IMMEDIATE")
                    validate_manifest(binding, time.time())
                    record = db.execute("SELECT binding, used FROM approvals WHERE nonce=?", (nonce,)).fetchone()
                    require(record is not None and record[0] == digest(binding) and record[1] is not None,
                            "Consumed approval record changed before upload.")
                    check_reconciliation(db, binding, time.time())
                    require_no_pending_stage(db, binding)
                    if is_submission:
                        lock = db.execute("SELECT nonce, phase FROM coordination.submission_locks WHERE target=?", (key,)).fetchone()
                        require(lock == (nonce, "handoff"), "Submission lock changed before upload.")
                    else:
                        require_unlocked(db, binding)
                    changed = db.execute("UPDATE coordination.attempt_phases SET phase='write_started' WHERE nonce=? AND phase='checking'", (nonce,)).rowcount
                    require(changed == 1, "Attempt was released or already reached the write boundary; fresh approval is required.")
            result = execution.upload(binding, artifact, envelope, task_path, properties, run_config, before_upload)
        except BaseException as exc:
            with db:
                retain_job_ids(db, nonce, {"ContentId": getattr(exc, "content_id", None)})
            if is_submission:
                with db:
                    db.execute("UPDATE coordination.submission_locks SET phase='uncertain', updated=? WHERE target=? AND nonce=?",
                               (time.time(), key, nonce))
            raise
        with db:
            retain_job_ids(db, nonce, result)
        if is_submission:
            with db:
                db.execute("UPDATE coordination.submission_locks SET phase='accepted', updated=? WHERE target=? AND nonce=?",
                           (time.time(), key, nonce))
        return result


def recovery_evidence(db, args):
    """Read historical evidence only; recheck both original ledger fingerprints."""
    if args.attempt_id:
        require(args.manifest is None and args.approval_record is None,
                "Choose an attempt ID or original evidence files, not both.")
        binding, approval = evidence_store.load(args.attempt_id)
    else:
        require(args.manifest is not None and args.approval_record is not None,
                "Recovery requires an attempt ID or the original manifest and approval record.")
        binding = read_json(manifest_path(args.manifest))
        approval = read_json(manifest_path(args.approval_record))
    consumed_approval(db, binding, approval)
    return binding, approval


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("capabilities", "preview", "approve", "execute", "reconcile", "reconcile-initialization", "recover-submission", "inspect-submission", "recover-prewrite", "reconcile-existing", "inspect-child-outcome", "retain-evidence"))
    parser.add_argument("--proposal", type=Path)
    parser.add_argument("--preflight", type=Path)
    parser.add_argument("--task-envelope", type=Path)
    parser.add_argument("--task-input", type=Path, help="Task Hook preview input; required at the routed live-read preview step")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--manifest", type=Path,
                        help="Private temporary manifest file; created exclusively by preview and reused unchanged")
    parser.add_argument("--confirmed", action="store_true", help="Internal flag after explicit user approval")
    parser.add_argument("--actor", help="Caller-supplied approval audit label; not authenticated; approve only")
    parser.add_argument("--approval-record", type=Path, help="Private temporary approval record; required for approve/execute")
    parser.add_argument("--reconciliation", type=Path, help="Private receipt output for reconcile; required input for SUBMIT")
    parser.add_argument("--reviewed-binding", help="Exact bindingSha256 presented with the approved preview")
    parser.add_argument("--nonce")
    parser.add_argument("--attempt-id", help="Consumed approval nonce; read-only recovery evidence lookup only")
    parser.add_argument("--ttl", type=int, help="Preview-only validity in seconds (default: 900)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--properties", type=Path, default=ROOT / "core/auth/fusionEnv.properties")
    parser.add_argument("--run-config", type=Path, default=ROOT / "core/data-loader/config/env.properties")
    args = parser.parse_args(argv)
    try:
        if args.command == "capabilities":
            print(json.dumps(capabilities()))
            return 0
        require(args.project is not None, "A project workspace is required.")
        recovery_commands = {"recover-submission", "inspect-submission", "recover-prewrite", "inspect-child-outcome", "reconcile", "reconcile-initialization", "retain-evidence"}
        require(not args.attempt_id or args.command in recovery_commands,
                "Retained evidence is for recovery only; it cannot authorize execution.")
        require(args.manifest is not None or args.attempt_id is not None,
                "A protected manifest path or recovery attempt ID is required.")
        loader = core()
        require(args.command == "preview" or args.ttl is None, "Set expiry only during preview.")
        if args.command in recovery_commands:
            if args.command == "reconcile":
                require(args.reconciliation is not None, "Reconciliation requires a new receipt output path.")
                require(not manifest_path(args.reconciliation).exists(), "Reconciliation output already exists.")
            with ledger(args.project) as db:
                binding, approval = recovery_evidence(db, args)
                if args.command == "retain-evidence":
                    result = {"status": "retained", "attemptId": evidence_store.retain(binding, approval)}
                elif args.command == "reconcile":
                    receipt = reconcile(db, binding, approval, args.properties)
                    save_manifest(receipt, args.reconciliation)
                    result = {"status": "verified", "reconciliationId": receipt["reconciliationId"],
                              "reconciliationSha256": digest(receipt)}
                else:
                    action = {"recover-submission": recover_submission, "inspect-submission": inspect_submission,
                              "recover-prewrite": recover_prewrite, "inspect-child-outcome": inspect_child_outcome,
                              "reconcile-initialization": reconcile_initialization}[args.command]
                    result = action(db, binding, approval, args.properties)
            print(json.dumps(result))
            return 1 if args.command == "inspect-child-outcome" and not (result["completionVerified"] and result["completeStateVerified"]) else 0
        require(all((args.proposal, args.preflight, args.task_envelope)), "Prepared proposal, preflight, and task envelope are required.")
        binding, artifact, task = inspect(args.proposal, args.preflight, args.task_envelope, loader)
        if args.command == "reconcile-existing":
            require(args.task_input is not None and args.reconciliation is not None, "Existing-state reconciliation requires Task Hook input and a new receipt output.")
            require(not manifest_path(args.reconciliation).exists(), "Receipt output already exists.")
            with ledger(args.project) as db:
                receipt = reconcile_existing(db, binding, artifact, args.properties, args.run_config, args.task_input)
                save_manifest(receipt, args.reconciliation)
            print(json.dumps({"status": "verified", "reconciliationId": receipt["reconciliationId"]}))
            return 0
        if binding["proposal"]["stage"] == "SUBMIT":
            require(args.reconciliation is not None, "Final submission requires a generated reconciliation receipt.")
            receipt = read_json(manifest_path(args.reconciliation))
            supplied = binding["proposal"].get("rediscovery")
            require(supplied is None or supplied == receipt, "Proposal rediscovery differs from the generated receipt.")
            binding["proposal"]["rediscovery"] = receipt
        with ledger(args.project) as db:
            if args.command == "preview":
                require_no_pending_stage(db, binding)
                check_reconciliation(db, binding, time.time())
                require(args.task_input is not None, "Preview requires Task Hook input for live validation.")
                binding["liveValidation"] = execution.collect(binding, artifact.content, args.properties,
                                                              args.run_config, args.task_input)
                binding = build_manifest(binding, ttl=MAX_TTL if args.ttl is None else args.ttl)
                save_manifest(binding, args.manifest)
                result = {"stage": binding["proposal"]["stage"], "bindingSha256": digest(binding),
                          "archiveSha256": binding["archiveSha256"], "nonce": binding["nonce"],
                          "expiresAt": binding["expiresAt"], "redactedBusinessSummary": binding["redactedBusinessSummary"]}
            elif args.command == "approve":
                binding = load_manifest(args.manifest, binding)
                require(args.approval_record is not None, "An approval record output path is required.")
                require(not manifest_path(args.approval_record).exists(), "Approval record path already exists.")
                result = approve(db, binding, confirmed=args.confirmed,
                                 reviewed_binding=args.reviewed_binding, actor=args.actor)
                save_manifest(result.pop("approvalRecord"), args.approval_record)
            else:
                binding = load_manifest(args.manifest, binding)
                require(bool(args.nonce), "Execution requires the recorded approval nonce.")
                require(args.approval_record is not None, "The reviewed approval record is required.")
                result = execute(db, binding, artifact, task, args.nonce, args.properties,
                                 args.run_config, approval_record=read_json(manifest_path(args.approval_record)),
                                 dry_run=args.dry_run, loader=loader)
        if args.command == "execute" and not args.dry_run:
            loader.data_loader_report.emit_inline_or_markdown(
                result, "initiation", None, loader.data_loader_report.render_initiation_report, stream=sys.stdout)
        else:
            print(json.dumps(result))
        return 0
    except Exception as exc:
        # Core errors can contain source/customer values; never print their raw message here.
        failure = "approval_blocker" if isinstance(exc, GuardError) else "input_validation"
        if isinstance(exc, (OSError, sqlite3.Error, evidence_store.EvidenceError)):
            failure = "artifact_persistence"
        if hasattr(exc, "stage"):
            failure = "transport_or_environment" if exc.stage in {"auth", "config"} else "fusion_api_error"
        if isinstance(exc, TimeoutError):
            failure = "process_timeout"
        elif hasattr(exc, "status_code"):
            failure = {401: "auth_expired_or_invalid", 403: "authorization_or_privilege"}.get(exc.status_code, "fusion_api_error")
        elif args.command in {"reconcile", "execute", "recover-submission", "inspect-submission"} and isinstance(exc, RuntimeError):
            failure = "transport_or_environment"
        print(json.dumps({"status": "blocked", "stage": args.command, "failure_class": failure,
                          "message": str(exc) if isinstance(exc, (GuardError, live.contract.ContractError, evidence_store.EvidenceError)) else "CPQ handoff failed; inspect sanitized Core diagnostics.",
                          "recommended_action": "Stop; reconcile any attempted load before fresh validation and approval."}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
