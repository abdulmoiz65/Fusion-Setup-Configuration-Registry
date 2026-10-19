#!/usr/bin/env python3
"""Thin instructor read/handoff adapter over unchanged FSCR CLIs (Python 3.11+).

No private HTTP/auth client and no upload entry point. Shared Data Loader owns
preflight, approval, upload, initiation, and separately requested status checks.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import zipfile

from instructor_validation import (BUSINESS_OBJECT, InstructorError, candidate_set,
                                  ensure_no_existing, fail, fingerprint, identifier,
                                  normalize_request, resolve_exact, search_text,
                                  verify_proposal, verify_readback)

SKILL = Path(__file__).resolve().parents[1]
ROOT = SKILL.parents[4]
REST_CLIENT = ROOT / "core/fusion-api/rest-api-client/scripts/fusion_rest_client.py"
PLANNER = ROOT / "pillars/hcm/learning-management/learning-management-common/scripts/rule_plan.py"
BASE = "/hcmRestApi/resources/11.13.18.05/"
PATHS = {"people": BASE + "workersLov", "instructors": BASE + BUSINESS_OBJECT,
         "people_metadata": BASE + "workersLov/describe", "instructor_metadata": BASE + BUSINESS_OBJECT + "/describe"}
FIELDS = "PersonId,DisplayName,PersonNumber,DepartmentName,LocationName,JobName,BusinessUnitName,AssignmentStatusType"
FINDER = ("findByWord;AssignmentType=E C N,PrimaryAssignmentOnly=true,"
          "AssignmentStatusType=ACTIVE SUSPENDED,DataSecurityPrivilege=PublicPerson,"
          "FilterAttributes=DisplayName PersonNumber DepartmentName")


def readiness():
    result = subprocess.run([sys.executable, str(PLANNER), "--pillar-skill-path", str(SKILL.parent),
                             "--setup-task", "Manage Instructors"], cwd=ROOT,
                            capture_output=True, text=True, timeout=30)
    try:
        value = json.loads(result.stdout)
    except ValueError:
        fail("catalog_mismatch", "Shared rule planner did not return a usable plan.")
    if result.returncode or value.get("status") != "planned":
        fail("catalog_mismatch", "Instructor rule plan is incomplete. Resolve named ora-resource contracts; no readiness override.")
    return value


def read_readiness(reader, expected_environment, operation):
    """Discovery eligibility only; never a Task Hook/create validation result."""
    if operation not in {"lookup", "check-existing"}:
        fail("unsupported", "Read readiness permits only person lookup and duplicate inspection.")
    if not expected_environment or not reader.expected_origin:
        fail("target_mismatch", "Confirm environment and origin before requesting data.")
    props = reader._target()
    if props.get("environment") != expected_environment:
        fail("target_mismatch", "Configured environment differs from the selected read target.")
    if not REST_CLIENT.is_file():
        fail("catalog_mismatch", "The declared shared REST client is unavailable.")
    return {"status": "read_ready", "operation": operation,
            "environment": expected_environment, "origin": reader.expected_origin,
            "method": "GET", "createReady": False}


class SharedReads:
    """Invoke the documented shared GET CLI; do not accept caller-selected URLs."""
    def __init__(self, properties, expected_origin, *, run=subprocess.run):
        self.properties = Path(properties).resolve()
        self.expected_origin = expected_origin.rstrip("/")
        self.run = run

    def _target(self):
        # Shared parsing and URL policy; authentication still belongs to its CLI.
        path = str(ROOT / "core/fusion-api/rest-api-client/scripts")
        if path not in sys.path:
            sys.path.insert(0, path)
        import rest_client_common as shared
        props = shared.read_properties(self.properties)
        if props.get("restBaseUrl", "").rstrip("/") != self.expected_origin:
            fail("target_mismatch", "Configured Fusion target differs from the selected environment.")
        shared.build_url(props, PATHS["people"], {})
        return props

    def get(self, resource, query, timeout=60):
        if resource not in PATHS:
            fail("unsupported", "Unknown instructor read route.")
        self._target()
        command = [sys.executable, str(REST_CLIENT), PATHS[resource], "--method", "GET",
                   "--properties", str(self.properties), "--header", "REST-Framework-Version=9",
                   "--timeout", str(max(1, int(timeout)))]
        for key, value in query.items():
            command.extend(["--query", key + "=" + str(value)])
        try:
            # Separate response bytes from shared authentication/status messages.
            with tempfile.TemporaryDirectory(prefix="fscr-instructor-read-") as directory:
                output = Path(directory) / "response.json"
                result = self.run([*command, "--output", str(output)], cwd=ROOT,
                                  capture_output=True, text=True, timeout=max(1, timeout))
                content = output.read_text(encoding="utf-8") if result.returncode == 0 and output.is_file() else ""
        except subprocess.TimeoutExpired:
            fail("process_timeout", "Shared GET exceeded its time bound; no complete result.")
        if result.returncode:
            # Shared stderr may contain personal query values or authentication URLs.
            text = result.stderr or ""
            code = "auth_authz" if any(s in text for s in ("401", "403")) else "transport_environment"
            if "CERTIFICATE_VERIFY_FAILED" in text:
                fail("transport_tls", "Shared GET failed certificate verification; TLS verification remains enabled.")
            fail(code, "Shared GET failed. Inspect diagnostics privately; no fallback or empty-result substitution.")
        try:
            value = json.loads(content)
        except ValueError:
            fail("fusion_api", "Shared GET did not return JSON; keep auth diagnostics private.")
        if not isinstance(value, dict):
            fail("fusion_api", "Expected a Fusion object response.")
        return value


def assess_flexfield_metadata(body):
    """Evaluate exposed DFF attributes, independently of Set functionality.

    A describe response is not evidence of child-omission/default semantics.
    Never turn this result into a Task Hook or create-ready attestation.
    """
    result = {"status": "blocked", "requiredCustomFields": [],
              "optionalCustomFields": [], "unknownFields": [],
              "createReady": False, "omissionVerified": False}
    try:
        attributes = body["Resources"][BUSINESS_OBJECT]["children"]["resourcesDFF"]["attributes"]
    except (KeyError, TypeError):
        return {**result, "reason": "dff_metadata_missing"}
    if not isinstance(attributes, list) or not attributes:
        return {**result, "reason": "dff_metadata_missing"}
    names = set()
    for attribute in attributes:
        if not isinstance(attribute, dict):
            return {**result, "reason": "dff_metadata_malformed"}
        name = attribute.get("name")
        if not isinstance(name, str) or not name or name in names:
            return {**result, "reason": "dff_metadata_malformed"}
        names.add(name)
        # These are technical identity/type/display fields, not custom inputs.
        if name in {"ResourceId", "ResourceType", "__FLEX_Context_DisplayValue"}:
            continue
        mandatory = attribute.get("mandatory")
        # Do not coerce strings, missing flags or conflicting declarations.
        if type(mandatory) is not bool or (
            "required" in attribute and attribute["required"] is not mandatory
        ) or ("nullable" in attribute and attribute["nullable"] is not (not mandatory)):
            result["unknownFields"].append(name)
        elif mandatory:
            result["requiredCustomFields"].append(name)
        else:
            result["optionalCustomFields"].append(name)
    if result["unknownFields"]:
        return {**result, "reason": "dff_requiredness_unknown"}
    if result["requiredCustomFields"]:
        return {**result, "reason": "required_dff_input_or_mapping_needed"}
    return {**result, "status": "exposed_fields_optional",
            "reason": "dff_context_defaults_and_child_omission_unverified"}


def inspect_prerequisites(reader, expected_environment):
    """Independent metadata-only readiness; never a create-validation verdict.

    User-selected inspection route authorizes this one fixed describe GET. No
    graph override, person records, arbitrary paths, response-link following,
    registration changes, or deployment jobs are available here.
    """
    if not expected_environment or not reader.expected_origin:
        fail("target_mismatch", "Metadata inspection requires the selected environment and origin.")
    props = reader._target()
    if props.get("environment") != expected_environment:
        fail("target_mismatch", "Configured environment name differs from the inspection target.")
    if not REST_CLIENT.is_file():
        fail("catalog_mismatch", "The declared shared REST client is unavailable.")
    body = reader.get("instructor_metadata", {})
    declarations = []

    def visit(value, path=(), in_dff=False):
        if isinstance(value, dict):
            is_dff = in_dff or value.get("name") == "resourcesDFF"
            if is_dff:
                flags = {k: value[k] for k in ("required", "mandatory", "nullable", "updatable", "insertable")
                         if type(value.get(k)) is bool or (k == "required" and isinstance(value.get(k), list))}
                if flags:
                    declarations.append({"metadataPath": "/".join(path),
                                         "name": value.get("name"), **flags})
            for key, child in value.items():
                visit(child, (*path, key), is_dff or key == "resourcesDFF")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, (*path, str(index)), in_dff)

    visit(body)
    return {"status": "metadata_inspected", "environment": expected_environment,
            "origin": reader.expected_origin, "method": "GET", "resource": PATHS["instructor_metadata"],
            "responseFingerprint": fingerprint(body), "topLevelKeys": sorted(body),
            "dffDeclarations": declarations, "dffRequiredness": "unverified",
            "flexfieldAssessment": assess_flexfield_metadata(body),
            "createReady": False,
            "limitation": "Observed describe flags only. Missing fields, child/context metadata or defaults do not establish optionality or safe omission. This result is not Data Loader validation."}


def validate_configuration(reader, expected_environment, scope):
    """Narrow root-only configuration preflight; no approval or write authority."""
    if not isinstance(scope, dict) or set(scope) != {"setFiltering", "decisionReference"}:
        fail("input_validation", "Supply only setFiltering and the recorded user decisionReference.")
    if scope["setFiltering"] != "deferred" or not isinstance(scope["decisionReference"], str) or not scope["decisionReference"].strip():
        fail("unsupported", "Set-enabled creation is not implemented; explicit project scope deferral is required.")
    if not expected_environment or not reader.expected_origin or reader._target().get("environment") != expected_environment:
        fail("target_mismatch", "Configuration check requires the selected environment and origin.")
    if not REST_CLIENT.is_file():
        fail("catalog_mismatch", "Shared REST client is unavailable.")
    body = reader.get("instructor_metadata", {})
    assessment = assess_flexfield_metadata(body)
    if assessment["status"] != "exposed_fields_optional":
        fail("configuration", assessment["reason"])
    dff = body["Resources"][BUSINESS_OBJECT]["children"]["resourcesDFF"]
    properties = dff.get("properties", {})
    if properties.get("FND_ACFF_ApplicationID") != "10503" or properties.get("FND_ACFF_Type") != "DFF":
        fail("configuration", "Unexpected resource flexfield contract.")
    custom = []
    context = None
    identity = None
    for attr in dff["attributes"]:
        name = attr["name"]
        if name == "ResourceId":
            identity = attr
        elif name == "__FLEX_Context":
            context = attr
        elif name not in {"ResourceType", "__FLEX_Context_DisplayValue"}:
            custom.append(attr)
    if identity is None or identity.get("hasDefaultValueExpression") is not True or context is None:
        fail("configuration", "Missing parent identity default or optional context declaration.")
    if str(len(custom)) != properties.get("FlexMetaShownGlobalNum"):
        fail("configuration", "Global segment count is incomplete or inconsistent.")
    for attr in [*custom, context]:
        if attr.get("hasDefaultValueExpression", False) is not False or any(
            key in attr for key in ("defaultValue", "default", "defaultValueExpression")
        ):
            fail("configuration", "Custom/context default requires an additional supported mapping.")
        if attr is not context and attr.get("properties", {}).get("FND_ACFF_IsGlobal") != "true":
            fail("configuration", "Non-global segment requires context-specific validation.")
    return {"status": "configuration_validated", "environment": expected_environment,
            "origin": reader.expected_origin, "operation": "root_only_create",
            "setFiltering": "deferred", "decisionReference": scope["decisionReference"],
            "dffInputRequired": False, "customFields": [a["name"] for a in custom],
            "responseFingerprint": fingerprint(body), "scopeFingerprint": fingerprint(scope),
            "createReady": False, "runtimeOmissionVerified": False,
            "limitation": "Source and live metadata support omitting optional DFF inputs. Loader validation, task checks, privileges, exact approval and post-load verification remain required."}


def collect_pages(get, resource, query, *, key, page_size=100, max_pages=20,
                  max_seconds=120, clock=time.monotonic):
    """Bounded collection; a limit/error never establishes absence or uniqueness."""
    if not 1 <= page_size <= 100 or not 1 <= max_pages <= 20 or not 0 < max_seconds <= 120:
        fail("input_validation", "Requested pagination bounds exceed instructor execution limits.")
    started, offset, items, pages, seen = clock(), 0, [], 0, set()
    reason = "page_limit"
    while pages < max_pages:
        remaining = max_seconds - (clock() - started)
        if remaining <= 0:
            reason = "time_limit"
            break
        try:
            body = get(resource, {**query, "limit": page_size, "offset": offset}, min(60, remaining))
        except InstructorError as error:
            reason = error.code
            break
        page = body.get("items")
        if not isinstance(page, list) or type(body.get("hasMore")) is not bool:
            reason = "invalid_pagination_response"
            break
        if any(not isinstance(row, dict) or row.get(key) is None for row in page):
            reason = "missing_identity"
            break
        digest = fingerprint(page)
        if page and digest in seen:
            reason = "pagination_loop"
            break
        seen.add(digest)
        if "offset" in body and body["offset"] != offset:
            reason = "unexpected_offset"
            break
        if len(page) > page_size:
            reason = "unexpected_page_size"
            break
        pages += 1
        items.extend(page)
        if body["hasMore"] is False:
            return {"items": items, "complete": True, "pages": pages, "reason": None}
        if not page:
            reason = "empty_nonterminal_page"
            break
        offset += len(page)
    return {"items": items, "complete": False, "pages": pages, "reason": reason}


def person_query(kind, value):
    query = {"finder": FINDER, "fields": FIELDS, "onlyData": "true"}
    if kind == "person_id":
        query["q"] = "PersonId=" + identifier(value)
    elif kind in {"person_number", "full_name", "partial_name"}:
        query["finder"] += ",SearchTerms=" + search_text(value)
    else:
        fail("unverified_contract", "No enabled email lookup contract.")
    return query


def lookup_person(reader, person, context):
    result = collect_pages(reader.get, "people", person_query(person["kind"], person["value"]), key="PersonId")
    if person["kind"] == "partial_name":
        return {"discovery": candidate_set(person["value"], result["items"], complete=result["complete"], context=context),
                "pagination": {k: result[k] for k in ("complete", "pages", "reason")}}
    return resolve_exact(person, result["items"], complete=result["complete"])


def instructor_rows(reader, person_id):
    return collect_pages(reader.get, "instructors",
                         {"q": "personId=" + identifier(person_id), "onlyData": "true"}, key="instructorId")


def inspect_archive(archive, proposal):
    """Business cross-check AFTER shared conversion/validation, not a DAT template.

    Deliberately only the minimal root/personId route. A newly required Set/DFF
    mapping needs verified authoring before this function can accept those fields.
    """
    body = verify_proposal(proposal)
    try:
        with zipfile.ZipFile(archive) as zipped:
            infos = zipped.infolist()
            if len(infos) != 1 or infos[0].filename != BUSINESS_OBJECT + ".dat" or infos[0].file_size > 1024 * 1024:
                fail("input_validation", "Expected one bounded instructor DAT member, no child or path entries.")
            lines = list(csv.reader(io.StringIO(zipped.read(infos[0]).decode("utf-8-sig")), delimiter="|", quoting=csv.QUOTE_NONE))
    except (OSError, zipfile.BadZipFile, UnicodeError):
        fail("artifact_persistence", "Could not read instructor archive.")
    if not lines or len(lines[0]) != 4 or lines[0][:2] != ["METADATA", BUSINESS_OBJECT] or set(lines[0][2:]) != {"personId", "RestAction"}:
        fail("unverified_contract", "Archive is not the minimal verified-schema handoff shape; do not discard additional fields.")
    fields, actual = lines[0][2:], []
    for row in lines[1:]:
        if len(row) != 4 or row[:2] != ["MERGE", BUSINESS_OBJECT]:
            fail("input_validation", "Archive contains a non-create or malformed row.")
        values = dict(zip(fields, row[2:]))
        if values.pop("RestAction") != "POST":
            fail("unsupported", "Only explicit create RestAction POST is allowed.")
        identifier(values["personId"])
        actual.append(values)
    expected = [r["inputs"] for r in body["rows"]]
    if actual != expected or not actual or len({r["personId"] for r in actual}) != len(actual):
        fail("stale_proposal", "Archive rows do not exactly match the current proposed people and order.")
    import hashlib
    return {"archiveSha256": hashlib.sha256(Path(archive).read_bytes()).hexdigest(),
            "proposalFingerprint": proposal["fingerprint"], "operation": "create",
            "environment": body["environment"], "rowCount": len(actual),
            "businessObject": BUSINESS_OBJECT}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["readiness", "inspect-prerequisites", "validate-configuration", "validate-request", "lookup", "check-existing", "readback", "check-archive"])
    parser.add_argument("--input", type=Path, help="Private input JSON; never put real people in project records.")
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--properties", type=Path, default=ROOT / "core/auth/fusionEnv.properties")
    parser.add_argument("--expected-origin")
    parser.add_argument("--expected-environment")
    args = parser.parse_args(argv)
    try:
        if args.command == "readiness":
            result = readiness()
        elif args.command == "inspect-prerequisites":
            if not args.expected_origin or not args.expected_environment:
                fail("target_mismatch", "Confirm environment and origin before metadata inspection.")
            result = inspect_prerequisites(SharedReads(args.properties, args.expected_origin), args.expected_environment)
        else:
            if not args.input:
                fail("input_validation", "This command requires --input.")
            value = json.loads(args.input.read_text())
            if args.command == "validate-configuration":
                if not args.expected_origin or not args.expected_environment:
                    fail("target_mismatch", "Confirm environment and origin before configuration validation.")
                readiness()
                result = validate_configuration(SharedReads(args.properties, args.expected_origin), args.expected_environment, value)
            elif args.command == "validate-request":
                result = {"status": "valid_intake_only", "rows": len(normalize_request(value)["rows"])}
            elif args.command == "check-archive":
                if not args.archive:
                    fail("input_validation", "Archive path is required.")
                result = inspect_archive(args.archive, value)
            else:
                if not args.expected_origin or not args.expected_environment:
                    fail("target_mismatch", "Confirm environment and origin before requesting data.")
                reader = SharedReads(args.properties, args.expected_origin)
                if args.command in {"lookup", "check-existing"}:
                    read_readiness(reader, args.expected_environment, args.command)
                else:
                    readiness()  # Post-create verification retains its existing graph gate.
                if args.command == "lookup":
                    row = normalize_request(value)["rows"]
                    if len(row) != 1:
                        fail("input_validation", "Resolve one row at a time.")
                    result = lookup_person(reader, row[0]["person"],
                                           {"origin": args.expected_origin, "environment": args.expected_environment})
                else:
                    rows = instructor_rows(reader, value["personId"])
                    if args.command == "check-existing":
                        ensure_no_existing(value["personId"], rows["items"], complete=rows["complete"])
                        result = {"status": "no_accessible_existing_instructor"}
                    else:
                        result = verify_readback(value["personId"], rows["items"], complete=rows["complete"])
        print(json.dumps(result, indent=2))
        if result.get("verified") is False or result.get("pagination", {}).get("complete") is False:
            return 2
        return 0
    except InstructorError as error:
        print(json.dumps({"status": "blocked", "failure_class": error.code, "message": str(error)}))
        return 2
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired):
        print(json.dumps({"status": "blocked", "failure_class": "input_or_artifact", "message": "Invalid input, artifact, or incomplete planner response; inspect privately."}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
