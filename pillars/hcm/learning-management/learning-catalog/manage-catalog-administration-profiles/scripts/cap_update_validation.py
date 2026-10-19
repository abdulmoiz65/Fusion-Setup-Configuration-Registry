"""Pure single-profile sparse PATCH policy; never authenticates or submits.

Python 3.11+. Evidence truth and referenced-file integrity belong to the routed
handoff. These checks bind its attributed conclusions to the exact final bytes;
a caller-supplied verified flag alone is not target readiness or write approval.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
import hashlib
import io
import json
import re
from urllib.parse import urlsplit
import zipfile

from cap_create_validation import validate_privilege_assessment
import cap_visibility

CONTRACT = {
    "businessObject": "learningCatalogProfiles",
    "datFile": "learningCatalogProfiles.dat",
    "restContext": "ORA_HCM_REST",
    "identityField": "learningCatalogProfileNumber",
    "allowedFields": ["description", "name", "visibility"],
    "restAction": "PATCH", "maxRows": 1,
}
LIMITS = {"description": 4000, "name": 250, "visibility": 30}
BASELINE_FIELDS = frozenset({
    "learningCatalogProfileNumber", "learningCatalogProfileId", "name",
    "description", "visibility", "status", "isSystemDefault", "providerNamesList",
    "reconcilePriority", "processingStatus",
})
COMPARE_FIELDS = BASELINE_FIELDS - {"processingStatus"}
REQUIRED_BASELINE_FIELDS = frozenset({
    "learningCatalogProfileNumber", "name", "description", "status", "visibility", "isSystemDefault",
})
CONFLICT_MODEL = "sparse_last_writer_wins"
# The registered URL helper is processing-only, never a business attribute or
# another framework control. Its actual name comes from target evidence.
RESERVED_DATE_HELPERS = BASELINE_FIELDS | frozenset({
    "RestAction", "effectiveOf", "sourceSystemId", "sourceSystemOwner",
    "creationDate", "lastModifiedDate", "createdByPersonId", "createdByDisplayName",
    "lastModifiedByPersonId", "lastModifiedByDisplayName", "statusMeaning",
    "visibilityMeaning", "processingStatusMeaning", "destinationProfileId",
    "reconcileStartDate", "reconcileEndDate", "reconcileLastRunProcessId",
    "reconcileLastRunProcessDate", "contributors", "contributorCriteria",
    "contributorPersonList", "contentDefaults", "certificates",
})
COMPOSITE_MAPPING_FIELDS = frozenset({
    "dateField", "dateValue", "patchUrl", "canonicalKey", "resolvedItemPath",
    "dateFieldIsStagingOnly", "dateFieldExcludedFromPayload", "dateFieldMappingVerified",
    "dateFieldDataType", "dateFieldFormat",
})


def _require(condition, message):
    if not condition:
        raise ValueError("Update validation: " + message)


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def _text(value, label, maximum):
    _require(isinstance(value, str) and bool(value.strip()),
             label + " must be nonempty text; explicit clearing is unavailable")
    _require(len(value) <= maximum, label + " exceeds supported maximum length")
    _require("|" not in value and all(ord(c) >= 32 and ord(c) != 127 for c in value)
             and not any(c in value for c in ("\u0085", "\u2028", "\u2029")),
             label + " contains an unsupported DAT delimiter or control character")
    # DAT null markers are not ordinary strings on this route.
    _require(value not in {"#NULL", "#NULL#"}, label + " cannot use an unverified null marker")


def _baseline(baseline, *, require_complete=False):
    _require(isinstance(baseline, dict) and set(baseline) <= BASELINE_FIELDS,
             "baseline must contain only declared observable root fields")
    _text(baseline.get(CONTRACT["identityField"]), "profile number", 2000)
    _require(all(v is None or isinstance(v, str) for v in baseline.values()),
             "baseline values must be strings or observed nulls")
    if require_complete:
        missing = sorted(REQUIRED_BASELINE_FIELDS - set(baseline))
        _require(not missing, "baseline lacks required observable settings: " + ", ".join(missing))


def validate_changes(baseline, changes, fields, *, duplicate_check=None):
    """Return an exact sparse diff; omission does not mean null, reset or default.

    Metadata only needs to establish fields actually requested. Rename search
    must be complete and list matching stable numbers, including self if found.
    """
    _baseline(baseline)
    _require(isinstance(changes, dict) and set(changes) <= set(CONTRACT["allowedFields"]),
             "only description, name and visibility can be changed")
    _require(isinstance(fields, dict), "typed update metadata is required")
    intended, diff = {}, []
    for name, value in changes.items():
        if name == "visibility":
            value = cap_visibility.normalize(value)
        field = fields.get(name)
        _require(isinstance(field, dict) and field.get("type") == "string"
                 and field.get("updatable") is True and field.get("allowChanges") == "always"
                 and type(field.get("maxLength")) is int and field["maxLength"] > 0,
                 "missing or contradictory writable metadata for " + name)
        _text(value, name, min(LIMITS[name], field["maxLength"]))
        _require(name in baseline, "baseline lacks old value for " + name)
        if name == "visibility":
            enum = field.get("enum")
            _require(isinstance(enum, list) and enum and all(isinstance(v, str) for v in enum)
                     and len(enum) == len(set(enum))
                     and value in enum and value in cap_visibility.CODES,
                     "visibility must be in the verified supported target lookup")
        if value == baseline[name]:
            continue
        if name == "visibility":
            _require(baseline.get("isSystemDefault") == "N",
                     "visibility changes require a verified non-system-default profile")
        if name == "name":
            check = duplicate_check or {}
            matches = check.get("matchingProfileNumbers")
            _require(check.get("status") == "verified" and check.get("complete") is True
                     and isinstance(check.get("source"), str) and bool(check["source"].strip())
                     and check.get("name") == value and isinstance(matches, list)
                     and all(isinstance(v, str) and v.strip() for v in matches),
                     "rename requires a complete attributed exact-name duplicate check")
            _require(not (set(matches) - {baseline[CONTRACT["identityField"]]}),
                     "rename collides with another accessible profile")
        intended[name] = value
        diff.append({"field": name, "before": baseline[name], "after": value})
    return {"status": "changes_ready" if intended else "no_op",
            "profileNumber": baseline[CONTRACT["identityField"]],
            "intendedFields": intended, "diff": sorted(diff, key=lambda item: item["field"])}


def _verified(checks, name):
    value = checks.get(name, {})
    _require(isinstance(value, dict) and value.get("status") == "verified"
             and isinstance(value.get("source"), str) and bool(value["source"].strip()),
             name + " requires independently verified attributed evidence")
    return value


def _mapping_contract(evidence):
    """Validate retained mapping semantics without time, disk or network checks."""
    checks = evidence.get("checks", {})
    _require(isinstance(checks, dict), "checks are required")
    identity = _verified(checks, "identity")
    _baseline(evidence.get("baseline"))
    number = evidence["baseline"][CONTRACT["identityField"]]
    strategy = identity.get("mapping")
    _require(isinstance(strategy, str) and strategy in {"number_only", "registered_composite"},
             "verified number-only or registered-composite loader mapping required")
    _require(identity.get("numberField") == CONTRACT["identityField"]
             and identity.get("profileNumber") == number
             and identity.get("itemRouteVerified") is True
             and identity.get("loaderMappingVerified") is True
             and identity.get("unchangedIdentityPayload") in {"excluded", "accepted"},
             "verified existing-item loader identity mapping required")
    effective = _verified(checks, "effectiveContext")
    policy = "server_current" if strategy == "number_only" else "fixed_key_date"
    _require(effective.get("executionDatePolicy") == policy,
             "effective-date policy does not match the verified loader mapping")
    try:
        date.fromisoformat(effective["observedDate"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Update validation: observed effective date is required, not an execution-time guarantee") from exc
    template = evidence.get("templateFields")
    _require(isinstance(template, list) and all(isinstance(v, str) and v for v in template)
             and len(set(template)) == len(template)
             and {"RestAction", CONTRACT["identityField"]} <= set(template),
             "exact live template fields are required")
    if "effectiveOf" in effective:
        _require(effective["effectiveOf"] == "RangeMode=UPDATE" and effective.get("mappingVerified") is True
                 and "effectiveOf" in template, "unverified effectiveOf helper mapping")
    if strategy == "number_only":
        _require(not (set(identity) & COMPOSITE_MAPPING_FIELDS),
                 "number-only mapping cannot carry composite-key helpers")
        return {}

    # This is a deliberately bounded use of getConfiguredRestUrl's registered
    # placeholders. Canonical GET alone cannot establish this loader mapping.
    registration = _verified(checks, "registration")
    field = identity.get("dateField")
    _require(isinstance(evidence.get("fields"), dict), "typed update metadata is required")
    _require(isinstance(field, str) and re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", field)
             and field.casefold() not in {name.casefold() for name in RESERVED_DATE_HELPERS}
             and field not in evidence.get("fields", {}) and field in template,
             "composite date helper must be a verified nonbusiness live-template field")
    _require(identity.get("dateFieldIsStagingOnly") is True
             and identity.get("dateFieldExcludedFromPayload") is True
             and identity.get("dateFieldMappingVerified") is True
             and identity.get("dateFieldDataType") in ("Date", "String"),
             "composite date helper needs verified staging, payload-exclusion and type evidence")
    # Shared loader Date input is slash-formatted; the registered backend DATE
    # formatter converts that staged value to ISO for the URL. String helpers
    # are not converted. dateValue always denotes the canonical ISO key date.
    dat_format = "yyyy/MM/dd" if identity["dateFieldDataType"] == "Date" else "yyyy-MM-dd"
    _require(identity.get("dateFieldFormat") == dat_format,
             "composite helper DAT format must match its verified Date or String mapping")
    value = identity.get("dateValue")
    try:
        valid_date = isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except ValueError:
        valid_date = False
    _require(valid_date and value == effective.get("observedDate"),
             "composite key date must be the exact observed canonical ISO date")
    # No URL encoding or date-overloading of the business number is introduced.
    # This branch interpolates only a safe, unchanged single path component.
    _require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", number) is not None,
             "composite mapping requires a safe unchanged profile number, not a date or URI")
    patch_url = "/learningCatalogProfiles/<" + field + ">,<" + CONTRACT["identityField"] + ">"
    key = value + "," + number
    excluded = registration.get("excludeInPayload")
    _require(identity.get("patchUrl") == registration.get("patchUrl") == patch_url
             and isinstance(excluded, list) and all(isinstance(item, str) for item in excluded)
             and len(excluded) == len(set(excluded)) and field in excluded
             and identity.get("canonicalKey") == key
             and identity.get("resolvedItemPath") == "/learningCatalogProfiles/" + key,
             "registered composite URL, exclusions and observed canonical identity must agree")
    _require(isinstance(evidence.get("intendedFields"), dict)
             and not (set(evidence["intendedFields"]) & set(excluded)),
             "registered payload exclusions cannot remove the approved changed business fields")
    return {field: value.replace("-", "/") if identity["dateFieldDataType"] == "Date" else value}


def validate_evidence(evidence, fingerprint, *, now=None):
    """Validate preparation evidence, without inferring facts from GET success."""
    _require(isinstance(evidence, dict), "current updateEvidence is required")
    _require(isinstance(fingerprint, str) and bool(re.fullmatch(r"[0-9a-f]{64}", fingerprint))
             and evidence.get("sourceFingerprint") == fingerprint, "source fingerprint mismatch")
    _require(evidence.get("operation") == "update", "explicit update operation is required")
    for key in ("businessObject", "restContext"):
        _require(evidence.get(key) == CONTRACT[key], key + " mismatch")
    env = evidence.get("environment", {})
    _require(isinstance(env, dict) and isinstance(env.get("host"), str)
             and isinstance(env.get("name"), str) and bool(env["name"].strip()),
             "confirmed environment is required")
    parsed = urlsplit(env["host"])
    _require(parsed.scheme == "https" and parsed.hostname and not parsed.username
             and not parsed.password and not parsed.path and not parsed.query and not parsed.fragment,
             "confirmed HTTPS origin is required")
    runbook = evidence.get("runbook", {})
    _require(isinstance(runbook, dict) and runbook.get("status") == "active"
             and all(isinstance(runbook.get(k), str) and runbook[k].strip()
                     for k in ("runID", "projectStateRef")), "active project-bound Run Book is required")
    try:
        checked = datetime.fromisoformat(evidence["verifiedAt"].replace("Z", "+00:00"))
        expires = datetime.fromisoformat(evidence["expiresAt"].replace("Z", "+00:00"))
        clock = now or datetime.now(timezone.utc)
        _require(checked.tzinfo is not None and expires.tzinfo is not None
                 and clock.tzinfo is not None and checked <= clock < expires,
                 "evidence is expired or future-dated")
    except (KeyError, AttributeError, TypeError, ValueError) as exc:
        raise ValueError("Update validation: valid current evidence timestamps with timezone are required") from exc
    checks = evidence.get("checks", {})
    _require(isinstance(checks, dict), "checks are required")
    facts = {name: _verified(checks, name) for name in (
        "registration", "fieldMapping", "identity", "omission", "effectiveContext",
        "baseline", "processingAcceptance", "concurrency")}
    try:
        validate_privilege_assessment(checks.get("privileges"))
    except ValueError as exc:
        raise ValueError("Update validation: " + str(exc)) from exc
    _require(checks["privileges"].get("operation") == "update",
             "privilege assessment must be operation-specific; GET/create is not PATCH access")
    _require(facts["fieldMapping"].get("restAction") == "PATCH",
             "explicit registered loader PATCH mapping is required")
    _require(facts["omission"].get("absentFieldsPreserved") is True,
             "absent-field preservation must be verified")
    _require(type(facts["baseline"].get("matchCount")) is int
             and facts["baseline"]["matchCount"] == 1 and facts["baseline"].get("complete") is True,
             "one unique complete accessible baseline is required")
    _baseline(evidence.get("baseline"), require_complete=True)
    _mapping_contract(evidence)
    concurrency = facts["concurrency"]
    _require(concurrency.get("mode") == CONFLICT_MODEL
             and concurrency.get("sameFieldOverwritePossible") is True
             and concurrency.get("unrelatedFieldsOmitted") is True,
             "disclosed sparse last-writer-wins conflict model is required; no conditional-version claim")
    _require(isinstance(evidence.get("intendedFields"), dict), "intendedFields must be the sparse change object")
    _require(set(evidence["intendedFields"]) <= set(evidence["templateFields"]),
             "changed field absent from live template")
    result = validate_changes(evidence["baseline"], evidence.get("intendedFields"), evidence.get("fields"),
                              duplicate_check=checks.get("duplicateCheck"))
    _require(result["intendedFields"] == evidence["intendedFields"],
             "intendedFields must be the sparse change set, not unchanged values")
    return evidence


def expected_row(evidence):
    """Exact supported columns, including only approved staging helpers."""
    row = {"RestAction": "PATCH", CONTRACT["identityField"]: evidence["baseline"][CONTRACT["identityField"]],
           **evidence["intendedFields"]}
    effective = evidence["checks"]["effectiveContext"]
    if "effectiveOf" in effective:
        row["effectiveOf"] = effective["effectiveOf"]
    if evidence["checks"]["identity"].get("mapping") == "registered_composite":
        row.update(_mapping_contract(evidence))
    return row


def validate_archive(content, evidence):
    """Final-byte verification; safe at frozen submission without fresh reads."""
    _require(isinstance(evidence, dict) and evidence.get("operation") == "update"
             and evidence.get("businessObject") == CONTRACT["businessObject"]
             and evidence.get("restContext") == CONTRACT["restContext"],
             "frozen archive requires the update contract, not read/create evidence")
    _baseline(evidence.get("baseline"), require_complete=True)
    _mapping_contract(evidence)
    _require(isinstance(content, bytes) and 0 < len(content) <= 4 * 1024 * 1024,
             "archive exceeds single-row bounds")
    try:
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            members = archive.infolist()
            _require(len(members) == 1, "exactly one DAT member is required")
            member = members[0]
            _require(member.filename == CONTRACT["datFile"] and not member.is_dir()
                     and not (member.flag_bits & 1) and member.file_size <= 1024 * 1024
                     and (member.external_attr >> 16) & 0o170000 != 0o120000,
                     "invalid, encrypted, oversized or unsafe DAT member")
            text = archive.read(member).decode("utf-8-sig")
    except (zipfile.BadZipFile, UnicodeError, RuntimeError, OSError) as exc:
        raise ValueError("Update validation: invalid ZIP or UTF-8 DAT") from exc
    lines = text.splitlines()
    _require(len(lines) == 2 and all(line for line in lines),
             "exactly one METADATA and one MERGE row are required")
    header, values = (line.split("|") for line in lines)
    obj = CONTRACT["businessObject"]
    _require(header[:2] == ["METADATA", obj] and values[:2] == ["MERGE", obj],
             "only the root MERGE row is supported")
    columns = header[2:]
    _require(len(header) == len(values) and len(columns) == len(set(columns))
             and all(re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", item) for item in columns),
             "invalid columns or row width")
    _require(set(columns) <= set(evidence["templateFields"]), "column absent from live template")
    change = validate_changes(evidence["baseline"], evidence["intendedFields"], evidence["fields"],
                              duplicate_check=evidence["checks"].get("duplicateCheck"))
    _require(change["status"] == "changes_ready" and change["intendedFields"] == evidence["intendedFields"],
             "no-op or unchanged-field rows must not become loads")
    row = dict(zip(columns, values[2:]))
    _require(row.get("RestAction") == "PATCH", "RestAction must be explicit PATCH; no POST fallback")
    _require(row == expected_row(evidence),
             "archive must match exact changed fields, immutable identity and verified helpers; no extra columns")
    return {"archiveSha256": hashlib.sha256(content).hexdigest(), "rowCount": 1,
            "businessObject": obj, "restAction": "PATCH",
            "profileNumber": evidence["baseline"][CONTRACT["identityField"]]}


def verify_environment(evidence, config, run_id):
    env = evidence["environment"]
    _require(config.get("host") == env["host"]
             and (config.get("environment") or config.get("host")) == env["name"]
             and run_id == evidence["runbook"]["runID"], "environment or Run Book binding changed")


def preparation_binding(content, evidence, fingerprint, config, run_id, *, now=None):
    validate_evidence(evidence, fingerprint, now=now)
    verify_environment(evidence, config, run_id)
    summary = validate_archive(content, evidence)
    binding = {"operation": "update", "archiveSha256": summary["archiveSha256"],
               "environment": evidence["environment"], "runbook": evidence["runbook"],
               "profileNumber": summary["profileNumber"], "inputs": evidence["intendedFields"],
               "baseline": evidence["baseline"], "sourceFingerprint": fingerprint,
               "evidenceSha256": _digest(evidence), "conflictModel": CONFLICT_MODEL}
    return {"validation_purpose": "update_preparation_only", "write_eligible": False,
            "binding": binding, "bindingSha256": _digest(binding)}


def verify_readback(evidence, profiles, *, complete):
    """Compare observed root state; never turn loader or processing pending green."""
    _baseline(evidence.get("baseline"))
    _require(isinstance(profiles, list) and all(isinstance(item, dict) for item in profiles),
             "readback profiles must be a list of observed objects")
    number = evidence["baseline"][CONTRACT["identityField"]]
    matches = [row for row in profiles if row.get(CONTRACT["identityField"]) == number]
    if complete is not True or len(matches) != 1:
        return {"status": "unverified", "profileNumber": number,
                "reason": "complete unique accessible number readback required", "matchCount": len(matches),
                "unchangedSettingsCoverage": "unverified", "allSettingsPreserved": False,
                "processingComplete": False, "loaderCompletionVerified": False}
    row = matches[0]
    expected = {k: v for k, v in evidence["baseline"].items() if k in COMPARE_FIELDS}
    expected.update(evidence["intendedFields"])
    # Missing optional baseline observations do not prohibit a basic update,
    # but they do prevent claiming complete unchanged-root-settings coverage.
    baseline_missing = sorted(COMPARE_FIELDS - set(evidence["baseline"]))
    missing = sorted(set(expected) - set(row))
    mismatches = [{"field": key, "expected": value, "observed": row[key]}
                  for key, value in sorted(expected.items()) if key in row and row[key] != value]
    processing = row.get("processingStatus")
    incomplete = bool(missing or baseline_missing)
    return {"status": "mismatch" if mismatches else "partial" if incomplete else "verified_observed_fields",
            "profileNumber": number, "matchCount": len(matches),
            "baselineMissingFields": baseline_missing, "missingFields": missing, "mismatches": mismatches,
            "unchangedSettingsCoverage": "mismatch" if mismatches else "partial" if incomplete else "declared_root_fields_only",
            "allSettingsPreserved": False,
            "comparedFields": sorted(set(expected) & set(row)),
            "processingStatus": processing,
            "processingState": "pending" if processing == "ORA_NEEDS_PROCESSING" else "unverified",
            "processingComplete": False, "loaderCompletionVerified": False,
            "limitations": ["Accessible root observations only, not contributor/default/certificate state.",
                            "No snapshot isolation or same-field lost-update prevention.",
                            "Loader completion and CAP processing require independent evidence."]}
