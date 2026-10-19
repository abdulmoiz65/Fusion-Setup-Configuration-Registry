"""Offline, opt-in single-root POST archive checks; never authenticates or submits."""
from __future__ import annotations
import cap_visibility

from datetime import datetime, timezone
import hashlib
import io
import re
import zipfile
import json
from urllib.parse import urlsplit

# CAP policy, not a declaration that any target's schema/grants have passed.
CONTRACT = {
    "businessObject": "learningCatalogProfiles", "datFile": "learningCatalogProfiles.dat",
    "restContext": "ORA_HCM_REST", "identityField": "learningCatalogProfileNumber",
    "allowedFields": ["learningCatalogProfileNumber", "name", "description", "visibility"],
    "requiredFields": ["name", "visibility"], "maxRows": 1, "restAction": "POST",
}


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def preparation_binding(content, evidence, fingerprint, config, run_id, *, now=None):
    """Offline binding only; supplied evidence must still be independently verified."""
    validate_evidence(evidence, CONTRACT, fingerprint, now=now)
    verify_environment(evidence, config, run_id)
    summary = validate_archive(content, CONTRACT, evidence)
    binding = {"operation": "create", "archiveSha256": summary["archiveSha256"],
               "environment": evidence["environment"], "runbook": evidence["runbook"],
               "inputs": evidence["intendedFields"], "sourceFingerprint": fingerprint,
               "evidenceSha256": _digest(evidence)}
    return {"validation_purpose": "create_preparation_only", "write_eligible": False,
            "binding": binding, "bindingSha256": _digest(binding)}


def verify_preparation_approval(content, evidence, fingerprint, config, run_id,
                                prepared, approval, *, now=None):
    """Reject altered inputs/target/operation/artifact; never authorize a core call."""
    actual = preparation_binding(content, evidence, fingerprint, config, run_id, now=now)
    _require(isinstance(prepared, dict) and prepared == actual, "prepared binding changed")
    _require(isinstance(approval, dict) and approval.get("approved") is True
             and approval.get("operation") == "create"
             and approval.get("bindingSha256") == actual["bindingSha256"],
             "explicit approval of the exact preparation binding is required")
    return actual


def _require(condition, message):
    if not condition:
        raise ValueError("Create validation: " + message)


def validate_privilege_assessment(item):
    """Keep grant evidence distinct from shared runtime authorization enforcement.

    The shared loader has no effective-role lookup or grant-certificate input.
    An assessed state permits read-only preparation, not a claim of write access.
    Known denials cannot be converted into that state. The handoff must still
    complete real shared preflight before producing an approval-ready preview.
    """
    _require(isinstance(item, dict) and isinstance(item.get("source"), str)
             and bool(item["source"].strip()), "privileges requires an attributed assessment")
    _require(item.get("knownDenial", False) is False, "privileges has a known authorization denial")
    if item.get("status") == "verified":
        return
    _require(item.get("status") == "assessed"
             and item.get("enforcement") == "core.data-loader"
             and item.get("grantsVerified") is False
             and item.get("knownDenial") is False,
             "privileges requires verified evidence or an explicit shared-loader assessment; unknown is not passed")


def validate_evidence(evidence, contract, fingerprint, *, now=None):
    """Check the shape/binding of evaluator evidence, not invent its truth.

    Callers must evaluate source-owned rules against authorized live metadata and
    privilege assessment. A supplied status or a passing offline fixture is not
    live proof of grants; assessed privileges remain explicitly unverified.
    """
    _require(isinstance(evidence, dict), "current createEvidence is required")
    _require(evidence.get("sourceFingerprint") == fingerprint, "source fingerprint mismatch")
    _require(evidence.get("businessObject") == contract["businessObject"], "business object mismatch")
    _require(evidence.get("restContext") == contract["restContext"], "REST context mismatch")
    _require(evidence.get("operation") == "create", "explicit create operation is required")
    env = evidence.get("environment", {})
    _require(isinstance(env, dict), "environment is required")
    host = env.get("host", "")
    _require(isinstance(host, str), "invalid host")
    parsed = urlsplit(host)
    _require(parsed.scheme == "https" and bool(parsed.hostname) and not parsed.username
             and not parsed.password and parsed.path == "" and not parsed.query and not parsed.fragment,
             "confirmed HTTPS origin is required")
    _require(isinstance(env.get("name"), str) and bool(env["name"].strip()), "environment name is required")
    runbook = evidence.get("runbook", {})
    _require(isinstance(runbook, dict) and runbook.get("status") == "active"
             and isinstance(runbook.get("runID"), str) and bool(runbook["runID"].strip())
             and isinstance(runbook.get("projectStateRef"), str) and bool(runbook["projectStateRef"].strip()),
             "active project-bound Run Book is required")
    clock = now or datetime.now(timezone.utc)
    try:
        checked = datetime.fromisoformat(evidence["verifiedAt"].replace("Z", "+00:00"))
        expires = datetime.fromisoformat(evidence["expiresAt"].replace("Z", "+00:00"))
        _require(checked.tzinfo is not None and expires.tzinfo is not None
                 and checked <= clock < expires, "evidence is expired or future-dated")
    except (KeyError, AttributeError, TypeError, ValueError) as exc:
        raise ValueError("Create validation: valid current evidence timestamps with timezone are required") from exc
    facts = evidence.get("checks", {})
    _require(isinstance(facts, dict), "checks are required")
    for key in ("registration", "fieldMapping", "identity", "defaultsAndDates",
                "duplicateCheck", "processingAcceptance"):
        item = facts.get(key, {})
        _require(isinstance(item, dict) and item.get("status") == "verified"
                 and isinstance(item.get("source"), str) and bool(item["source"].strip()),
                 key + " requires verified source evidence")
    validate_privilege_assessment(facts.get("privileges"))
    _require(facts["duplicateCheck"].get("matchCount") == 0
             and type(facts["duplicateCheck"].get("matchCount")) is int
             and facts["duplicateCheck"].get("complete") is True,
             "completed zero-match duplicate check is required; account absence alone is insufficient")
    _require(facts["identity"].get("numberMode") in {"supplied", "generated"}
             and facts["identity"].get("uniquenessEnforced") is True,
             "documented number handling and server uniqueness are required")
    fields = evidence.get("fields")
    _require(isinstance(fields, dict) and all(isinstance(v, dict) for v in fields.values()), "typed create fields are required")
    template = evidence.get("templateFields")
    _require(isinstance(template, list) and all(isinstance(v, str) and v for v in template)
             and len(template) == len(set(template)) and "RestAction" in template,
             "exact live template fields are required")
    for name in contract["allowedFields"]:
        field = fields.get(name, {})
        _require(isinstance(field, dict) and field.get("type") == "string"
                 and field.get("createAllowed") is True
                 and type(field.get("required")) is bool
                 and type(field.get("maxLength")) is int and field["maxLength"] > 0
                 and name in template, "missing or contradictory create metadata for " + name)
        if "enum" in field:
            _require(isinstance(field["enum"], list) and field["enum"]
                     and all(isinstance(v, str) and v for v in field["enum"]), "invalid enum metadata")
    _require(all(not v.get("required") or key in contract["allowedFields"]
                 for key, v in fields.items() if isinstance(v, dict)),
             "target requires fields outside the bounded create policy")
    return evidence


def validate_archive(content, contract, evidence):
    """Inspect the final immutable bytes before preview; no extraction to disk."""
    _require(isinstance(content, bytes) and 0 < len(content) <= 4 * 1024 * 1024, "archive exceeds single-row bounds")
    try:
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            members = archive.infolist()
            _require(len(members) == 1, "exactly one DAT member is required")
            member = members[0]
            _require(member.filename == contract["datFile"] and not member.is_dir()
                     and not (member.flag_bits & 1) and member.file_size <= 1024 * 1024
                     and (member.external_attr >> 16) & 0o170000 != 0o120000,
                     "invalid, encrypted, oversized or unsafe DAT member")
            text = archive.read(member).decode("utf-8-sig")
    except (zipfile.BadZipFile, UnicodeError, RuntimeError, OSError) as exc:
        raise ValueError("Create validation: invalid ZIP or UTF-8 DAT") from exc
    lines = [line for line in text.splitlines() if line.strip()]
    _require(len(lines) == 2, "one METADATA and one MERGE row are required")
    header, values = (line.split("|") for line in lines)
    obj = contract["businessObject"]
    _require(header[:2] == ["METADATA", obj] and values[:2] == ["MERGE", obj], "root MERGE only")
    columns = header[2:]
    _require(len(header) == len(values) and len(columns) == len(set(columns))
             and all(re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", v) for v in columns), "invalid columns or row width")
    _require(set(columns) <= set(evidence["templateFields"]), "column absent from live template")
    row = dict(zip(columns, values[2:]))
    _require(row.get("RestAction") == "POST", "RestAction must be explicit POST")
    allowed = set(contract["allowedFields"])
    _require(all(key in allowed or key == "RestAction" or value == "" for key, value in row.items()),
             "populated output-only/helper/unsupported field")
    required = set(contract["requiredFields"]) | {k for k, v in evidence["fields"].items() if v.get("required")}
    for name in required:
        _require(bool(row.get(name, "").strip()), "missing required field " + name)
    for name in allowed:
        value = row.get(name, "")
        if not value:
            continue
        if name == "visibility":
            _require(value in cap_visibility.CODES, "visibility must use an exact CAP code; normalize and review before packaging")
        field = evidence["fields"][name]
        _require(len(value) <= field["maxLength"] and all(ord(c) >= 32 for c in value), "invalid value for " + name)
        if "enum" in field:
            _require(value in field["enum"], "invalid enum value for " + name)
    identity = contract["identityField"]
    supplied = evidence["checks"]["identity"]["numberMode"] == "supplied"
    _require(bool(row.get(identity, "").strip()) == supplied, "number mode does not match submitted identity")
    intended = evidence.get("intendedFields")
    actual = {key: value for key, value in row.items() if key in allowed and value != ""}
    _require(isinstance(intended, dict) and actual == intended, "archive does not match reviewed intended fields")
    return {"archiveSha256": hashlib.sha256(content).hexdigest(), "rowCount": 1,
            "businessObject": obj, "restAction": "POST"}


def verify_environment(evidence, config, run_id):
    """Compare against core's selected context, not a caller-chosen alternate pod."""
    env = evidence["environment"]
    _require(config["host"] == env["host"]
             and (config.get("environment") or config["host"]) == env["name"]
             and run_id == evidence["runbook"]["runID"], "environment or Run Book binding changed")
