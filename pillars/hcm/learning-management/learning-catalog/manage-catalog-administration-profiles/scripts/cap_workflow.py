"""CAP orchestration through unchanged shared interfaces. Python 3.11+.

Read-only HTTP/authentication belongs to fusion_rest_client.py. All mutations
remain executable refusals. Default CLI behavior is a local readiness check.
"""
from __future__ import annotations

import argparse
import functools
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.parse import parse_qsl, urlsplit

import cap_read
import cap_write_contract

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
from cap_paths import repository_root
REPO = repository_root(SKILL)
TASK = "Manage Catalog Administration Profiles"
CODE = "CUSTOM_MANAGE_CATALOG_ADMINISTRATION_PROFILES"
PINNED_UPSTREAM = "6d6bf4346f5e76ffff27888753b87febc862d8c6"
ROOT_PATH = "/hcmRestApi/resources/11.13.18.05/learningCatalogProfiles"
LOADER_PATH = "/hcmRestApi/resources/latest/dataLoaderBusinessObjects"
DISPLAY_FIELDS = ("name", "description", "status", "visibility", "isSystemDefault", "processingStatus")
WRITE_CONTRACTS = {
    "update": "Use cap_update_handoff.py for loader updates or cap_batch_update.py for basic-attribute shared REST updates, with route-specific evidence and exact approval; raw mutations remain unavailable",
    "activate": "Canonical status mapping, current transition/grants and restrictions",
    "deactivate": "Usage/provider/default restrictions and exact impact contract",
    "delete": "Logical-delete/replacement and association migration contract; never delete system default",
    "contributors": "People resolver, criteria/attachment keys and add/replace/remove membership contract",
    "content-defaults": "Seeded type-specific row/field/observer and inheritance contract",
    "certificates": "CAP row/template resolver, null clearing, privileges and inheritance contract",
    "reconcile": "Action arguments, privileges, shared route and terminal correlation contract",
    "prepare-create": "Use cap_create_handoff.py with verified evidence and selected project/task paths; no submission is exposed",
}


class CapabilityUnavailable(ValueError):
    """An explicitly unsupported shared capability; never a fallback trigger."""


def validate_read_request(request):
    """Validate CAP request shape before any credential or transport access."""
    if not isinstance(request, dict):
        raise ValueError("A read request object is required")
    allowed = {"mode", "name", "number", "expected_id", "host", "confirmed_host",
               "environment", "method", "path", "headers"}
    if set(request) - allowed:
        raise ValueError("Unsupported read input, changes, body or date")
    host = request.get("host")
    parsed = urlsplit(host) if isinstance(host, str) else None
    if (not parsed or parsed.scheme != "https" or not parsed.hostname
            or parsed.username or parsed.password or parsed.port not in (None, 443)
            or parsed.path or parsed.query or parsed.fragment
            or host != request.get("confirmed_host")):
        raise ValueError("The read target must be the confirmed HTTPS origin")
    if request.get("method", "GET") != "GET":
        raise ValueError("CAP reads require GET")
    if not isinstance(request.get("environment"), str) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", request["environment"]):
        raise ValueError("Confirmed environment identity is required")
    if request.get("path", ROOT_PATH) not in (ROOT_PATH, ROOT_PATH + "/describe"):
        raise ValueError("Only declared CAP root collection and metadata paths")
    headers = request.get("headers", {})
    if not isinstance(headers, dict):
        raise ValueError("Invalid headers")
    for key, value in headers.items():
        if key not in {"REST-Framework-Version", "Accept-Language"} or not isinstance(value, str):
            raise ValueError("Header is outside the CAP allowlist")
        if key == "REST-Framework-Version" and value != "9":
            raise ValueError("Unsupported REST framework version")
        if key == "Accept-Language" and not re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*", value):
            raise ValueError("Unsupported language")
    mode = request.get("mode")
    if mode == "list":
        if any(key in request for key in ("name", "number", "expected_id")):
            raise ValueError("Listing does not take a selector")
    elif mode == "exact":
        selectors = [key for key in ("name", "number") if key in request]
        if len(selectors) != 1:
            raise ValueError("Exact lookup requires one name or number")
        key = selectors[0]
        value = request[key]
        cap_read.exact_query("name" if key == "name" else "learningCatalogProfileNumber", value)
        # Number displaySize=30 is not a REST maximum. Bound local input by
        # the inherited source precision; enforce a smaller advertised max below.
        if len(value) > (250 if key == "name" else 2000):
            raise ValueError("Selector exceeds its supported length")
        if key == "number":
            cap_read.finder_query("findByLearningCatalogProfileNumber", "learningCatalogProfileNumber", value)
        if "expected_id" in request and (not isinstance(request["expected_id"], str) or not request["expected_id"]):
            raise ValueError("Expected identity must remain nonempty text")
    else:
        raise ValueError("Explicit exact or list mode is required")


def shared_plan():
    """Validate the selected CAP registry and its source rows locally."""
    path = REPO / "pillars/hcm/learning-management/learning-management-common/scripts/rule_plan.py"
    spec = importlib.util.spec_from_file_location("cap_upstream_planner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    plan = module.build_plan(SKILL.parent, TASK)
    if plan.get("validation", {}).get("status") != "ready" or plan["task"]["readiness"]["status"] != "ready":
        raise ValueError("CAP task graph is not ready")
    return plan


@functools.lru_cache(maxsize=1)
def shared_auth():
    path = REPO / "core/auth/fusion-oauth-authentication/scripts/fusion_auth.py"
    spec = importlib.util.spec_from_file_location("cap_shared_auth_configuration", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@functools.lru_cache(maxsize=1)
def shared_loader_metadata():
    """Import the public resolver only; its injected getter owns all I/O."""
    path = REPO / "core/data-loader/scripts/data_loader_metadata.py"
    spec = importlib.util.spec_from_file_location("cap_shared_loader_metadata", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if module.FDOS_ROOT.resolve() != REPO.resolve():
        raise ValueError("Shared loader resolved a different repository configuration")
    return module


def configured_context(request):
    """Read shared configuration without exposing credentials or allowing overrides."""
    module = shared_auth()
    props = module.read_properties(REPO / "core/auth/fusionEnv.properties")
    configured = urlsplit(props.get("restBaseUrl", ""))
    origin = configured.scheme + "://" + configured.netloc
    if (origin != request["host"] or props.get("environment") != request["environment"]):
        raise ValueError("Request does not match the configured environment and standard REST origin")
    module.require_authorized_rest_url(props, request["host"] + ROOT_PATH)
    return {"host": origin, "environment": props["environment"]}


def readiness(operation, request=None):
    """Read input readiness never becomes Task Hook/write readiness."""
    if operation not in {"retrieve", "list", "create", "inspect-write-contract", "inspect-profile", "inspect-update-contract"}:
        return {"status": "unsupported", "operation": operation, "write_eligible": False,
                "blockers": [WRITE_CONTRACTS.get(operation, "Unknown CAP operation"),
                             "No CAP write route is enabled"], "side_effects": []}
    if operation in {"retrieve", "list"}:
        validate_read_request(request)
        if request["mode"] != ("list" if operation == "list" else "exact"):
            raise ValueError("Operation and read mode disagree")
    if operation in {"inspect-profile", "inspect-update-contract"}:
        validate_read_request(request)
        if request["mode"] != "exact" or "number" not in request:
            raise ValueError("Profile inspection requires an exact number")
    if operation == "inspect-write-contract":
        if (not isinstance(request, dict) or request.get("mode") != "contract"
                or set(request) - {"mode", "environment", "host", "confirmed_host", "headers"}):
            raise ValueError("Contract inspection accepts only a confirmed target and read headers")
        validate_read_request({**request, "mode": "list"})
    blockers = []
    try:
        plan = shared_plan()
        if plan.get("validation", {}).get("status") != "ready":
            blockers.append("CAP-UPSTREAM-PLAN: shared plan is not ready")
    except (ValueError, OSError, ImportError):
        blockers.append("CAP-UPSTREAM-PLAN: shared task readiness is incomplete")
    if operation == "create":
        blockers.append("CAP-CREATE-EVIDENCE: current create contracts, grants and executable pillar validation are incomplete")
    return {"taskCode": CODE, "taskName": TASK, "operation": operation,
            "status": "unavailable" if blockers else "ready_for_read_preflight", "input_valid": operation != "create",
            "validation_purpose": "write_contract_inspection_only" if operation == "inspect-write-contract" else "retrieval_only" if operation != "create" else "create_readiness",
            "write_eligible": False, "live_available": not blockers, "blockers": blockers,
            "read_access_verified": False,
            "side_effects": [], "baseline": PINNED_UPSTREAM}


class SharedReadFailure(ValueError):
    """Sanitized shared-client failure; never reflect raw stdout/stderr."""


class ContractInspectionFailure(ValueError):
    """Preserve verified schema facts when registration uniqueness is unproven."""

    def __init__(self, facts):
        super().__init__("Registration lookup did not establish a unique complete result")
        self.facts = facts


def shared_get(request, path, query, timeout):
    """Invoke the documented core CLI, not a CAP HTTP/auth implementation.

    A process deadline covers login, one core-owned refresh and the request.
    Responses are memory-only. This function is private to the selected route;
    execute() validates input, plan and configuration before reaching it.
    """
    if timeout < 1:
        raise TimeoutError("CAP read deadline reached")
    # Recheck identity for each subprocess; no alternate properties or services.
    configured_context(request)
    command = [sys.executable, str(REPO / "core/fusion-api/rest-api-client/scripts/fusion_rest_client.py"),
               request["host"] + path, "--method", "GET", "--raw",
               "--timeout", str(max(1, int(min(45, timeout)))),
               "--callback-timeout", str(max(1, int(timeout)))]
    for key, value in query.items():
        command.extend(["--query", key + "=" + value])
    for key, value in {"REST-Framework-Version": "9", **request.get("headers", {})}.items():
        command.extend(["--header", key + "=" + value])
    try:
        completed = subprocess.run(command, cwd=REPO, capture_output=True,
                                   text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        raise TimeoutError("Shared GET/authentication exceeded its deadline") from None
    if completed.returncode != 0:
        raise SharedReadFailure("Shared GET failed; use the declared shared authentication/read-access diagnostics")
    try:
        return json.loads(completed.stdout)
    except (TypeError, ValueError):
        raise SharedReadFailure("Shared client did not return a complete JSON response") from None


def inspect_write_contract(request):
    """Reached only after source/target preflight; fixed shared GET metadata route."""
    root = shared_get(request, ROOT_PATH + "/describe", {}, 60)
    root_facts = cap_write_contract.describe_facts(root)
    description = cap_read.resource_description(
        shared_get(request, LOADER_PATH + "/describe", {}, 60), "dataLoaderBusinessObjects")
    collection = description.get("collection", {})
    if (not isinstance(collection, dict)
            or not isinstance(collection.get("actions", collection.get("methods", [])), list)):
        raise cap_read.LookupContractError("Malformed loader collection metadata")
    cap_read.validate_metadata(description, "BusObjTopDiscriminator", ["BusObjTopDiscriminator"])
    finders = description.get("finders", collection.get("finders", []))
    if not isinstance(finders, list):
        raise cap_read.LookupContractError("Malformed loader finder metadata")
    selected = [f for f in finders if isinstance(f, dict) and f.get("name") == "findDataLoaderBos"]
    if (len(selected) != 1 or not isinstance(selected[0].get("attributes", []), list)
            or any(not isinstance(a, dict) or a.get("required") not in ("Optional", False, None)
                   for a in selected[0].get("attributes", []))):
        raise cap_read.LookupContractError("Declared no-required-argument loader finder is not advertised")
    started = time.monotonic()
    page_facts = []
    next_offset = 0
    def fetch(url, auth, *, stage):
        nonlocal next_offset
        # The public resolver supplies selection and deduplication, while the
        # declared shared GET owns transport/auth. Never use its default HTTP.
        parsed = urlsplit(url)
        pairs = parse_qsl(parsed.query, keep_blank_values=True, strict_parsing=True)
        query = dict(pairs)
        if (parsed.scheme + "://" + parsed.netloc != request["host"]
                or parsed.path != LOADER_PATH or parsed.fragment
                or auth is not None or stage != "business-object-validation"
                or len(query) != len(pairs)
                or set(query) != {"finder", "onlyData", "offset", "q"}
                or query["finder"] != "findDataLoaderBos" or query["onlyData"] != "true"
                or query["offset"] != str(next_offset) or not query["q"]):
            raise cap_read.LookupContractError("Shared registration lookup contract changed")
        remaining = 120 - (time.monotonic() - started)
        if remaining < 1 or len(page_facts) >= 20 or next_offset >= 2000:
            raise cap_read.LookupContractError("Registration inspection bound reached")
        page = shared_get(request, LOADER_PATH, {**query, "limit": "100"}, remaining)
        if time.monotonic() - started >= 120:
            raise cap_read.LookupContractError("Registration inspection deadline exceeded")
        if (not isinstance(page, dict) or not isinstance(page.get("items"), list)
                or type(page.get("hasMore")) is not bool
                or any(type(page.get(key)) is not int for key in ("offset", "count", "limit"))
                or page["offset"] != next_offset or page["count"] != len(page["items"])
                or not 0 <= page["count"] <= page["limit"] <= 100 or page["limit"] < 1
                or (page["hasMore"] and not page["items"])):
            raise cap_read.LookupContractError("Malformed or nonadvancing registration page")
        for row in page["items"]:
            identifier = row.get("BusinessObjectId") if isinstance(row, dict) else None
            if type(identifier) not in (int, str) or not re.fullmatch(r"[1-9][0-9]{0,29}", str(identifier)):
                raise ValueError("Registration identifier must be an exact positive decimal")
        ids = [str(row["BusinessObjectId"]) for row in page["items"]]
        page_facts.append({"received_rows": len(ids), "distinct_ids": len(set(ids)),
                           "duplicate_id_rows": len(ids) - len(set(ids)),
                           "exact_discriminator_rows": sum(row.get("BusObjTopDiscriminator") == "learningCatalogProfiles" for row in page["items"])})
        next_offset += len(ids)
        return page
    loader = shared_loader_metadata()
    try:
        found = loader.resolve_business_object("learningCatalogProfiles",
                    {"host": request["host"], "auth": None}, allow_aliases=False, getter=fetch)
    except (cap_read.LookupContractError, loader.DataLoadError, SharedReadFailure, TimeoutError):
        # Never retain raw rows, IDs, links, response messages or credentials.
        raise ContractInspectionFailure({"root": root_facts, "registration_pages": page_facts,
            "registration_verified": False, "write_eligible": False}) from None
    identifier = found.get("BusinessObjectId")
    if type(identifier) not in (int, str) or not re.fullmatch(r"[1-9][0-9]{0,29}", str(identifier)):
        raise cap_read.LookupContractError("Registration identifier must be an exact positive decimal")
    detail = shared_get(request, LOADER_PATH + "/" + str(identifier), {"onlyData": "true"}, 60)
    if (not isinstance(detail, dict) or type(detail.get("BusinessObjectId")) not in (int, str)
            or str(detail["BusinessObjectId"]) != str(identifier)):
        raise cap_read.LookupContractError("Authoritative registration identity mismatch")
    result = cap_write_contract.assess(root, detail)
    result.update(taskCode=CODE, taskName=TASK, environment=request["environment"], host=request["host"],
                  registration_pages=page_facts, registration_verified=True,
                  terminal_node="CAP-CHECK-DONE", side_effects=[],
                  completed_path=["CAP-SELECT", "CAP-CHECK-VALIDATE", "CAP-CHECK-PREREQ", "CAP-CHECK-ROOT", "CAP-CHECK-LOADER"],
                  outcomes={"CAP-SELECT": "inspect", "CAP-CHECK-VALIDATE": "passed", "CAP-CHECK-PREREQ": "passed",
                            "CAP-CHECK-ROOT": "passed", "CAP-CHECK-LOADER": "observed"},
                  limitations=["Describe/registration advertisements are not write grants or proven defaults",
                               "Template reference is not downloaded/validated template content",
                               "No write operation becomes available from this assessment"])
    return result


def execute(operation, request=None):
    """Declared read-only route. Invocation requires routed read authorization."""
    result = readiness(operation, request)
    if not result.get("live_available"):
        raise CapabilityUnavailable("; ".join(result["blockers"]))
    configured_context(request)
    if operation == "inspect-update-contract":
        from cap_update_inspection import inspect_update
        return inspect_update(request)
    if operation == "inspect-write-contract":
        return inspect_write_contract(request)
    if operation == "inspect-profile":
        from cap_profile_inspection import inspect_profile
        return inspect_profile(request)
    description = cap_read.resource_description(shared_get(request, ROOT_PATH + "/describe", {}, 60),
                                                "learningCatalogProfiles")
    identity = ("learningCatalogProfileNumber",)
    fields = cap_read.validate_listing_metadata(description, identity, DISPLAY_FIELDS)
    unavailable_fields = [field for field in DISPLAY_FIELDS if field not in fields]
    if "name" not in fields:
        raise cap_read.LookupContractError("Name response metadata is required")
    if "expected_id" in request:
        attribute = next((a for a in description["attributes"] if a.get("name") == "learningCatalogProfileId"), {})
        if attribute.get("type") not in {"string", "integer", "number"}:
            raise cap_read.LookupContractError("Expected identity metadata is missing")
        fields.append("learningCatalogProfileId")
    query = {"onlyData": "true", "fields": ",".join(fields)}
    if operation == "list":
        result = cap_read.collect_listing(lambda q, remaining: shared_get(request, ROOT_PATH, q, remaining),
                    query, identity_fields=identity, fields=fields)
    else:
        field = "name" if "name" in request else identity[0]
        value = request["name"] if field == "name" else request["number"]
        finder = None if field == "name" else "findByLearningCatalogProfileNumber"
        cap_read.validate_metadata(description, field, [*identity, "name"], finder)
        attribute = next(a for a in description["attributes"] if a.get("name") == field)
        maximum = attribute.get("maxLength")
        if type(maximum) is int and maximum > 0 and len(value) > maximum:
            raise cap_read.LookupContractError("Selector exceeds current metadata maxLength")
        started = time.monotonic()
        def fetch(q):
            remaining = 120 - (time.monotonic() - started)
            if remaining < 1:
                raise TimeoutError("Exact lookup budget exhausted; uniqueness is not established")
            page = shared_get(request, ROOT_PATH, q, remaining)
            if time.monotonic() - started >= 120:
                raise TimeoutError("Exact lookup exceeded its total deadline")
            return page
        if finder:
            found = cap_read.collect_exact(fetch, {**query, "finder": cap_read.finder_query(finder, field, value)},
                    selector_field=field, value=value, identity_fields=identity)
        result = cap_read.collect_exact(fetch, {**query, "q": cap_read.exact_query(field, value)},
                    selector_field=field, value=value, identity_fields=identity)
        if finder and result["status"] != "ambiguous" and found["matches"] != result["matches"]:
            raise cap_read.LookupContractError("Finder and independent equality lookup disagree")
        if "expected_id" in request and result["status"] == "matched":
            actual = result["matches"][0].get("learningCatalogProfileId")
            if type(actual) not in (str, int) or str(actual) != request["expected_id"]:
                raise cap_read.LookupContractError("Expected profile identity does not match")
        for row in result["matches"]:
            if any(f in row and row[f] is not None and not isinstance(row[f], str)
                   for f in fields if f != "learningCatalogProfileId"):
                raise cap_read.LookupContractError("Exact read field violates its declared text metadata")
        # Do not pass response extras/self URLs through to output or project logs.
        result["matches"] = [{f: row[f] for f in fields if f in row and f != "learningCatalogProfileId"}
                             for row in result["matches"]]
        result["pagination_completed"] = True
    result.update(taskCode=CODE, taskName=TASK, environment=request["environment"], host=request["host"],
                  unavailable_fields=unavailable_fields,
                  terminal_node="CAP-R-PARTIAL" if result["status"] in {"partial", "failed"} else "CAP-R-DONE",
                  completed_path=["CAP-SELECT", "CAP-R-VALIDATE", "CAP-R-PREREQ", "CAP-R-METADATA", "CAP-R-GET"],
                  outcomes={"CAP-SELECT": "read", "CAP-R-VALIDATE": "passed", "CAP-R-PREREQ": "passed",
                            "CAP-R-METADATA": "passed", "CAP-R-GET": "partial" if result["status"] in {"partial", "failed"} else "complete"},
                  side_effects=[], validation_purpose="retrieval_only", write_eligible=False,
                  limitations={"account": "Only profiles accessible to the authenticated account; not tenant-global absence",
                               "effective_date": "Server-current; no historical/as-of override",
                               "language": request.get("headers", {}).get("Accept-Language", "Server default"),
                               "consistency": "Offset pages are not a transactional snapshot"},
                  next_step="Review accessible results; writes remain unavailable. Use shared auth diagnostics after a failed read.")
    result["reply_example"] = "Retrieve the selected profile by its exact number, or review the remaining write prerequisites."
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", help="retrieve, list, inspect-profile, inspect-write-contract; raw writes remain unavailable")
    parser.add_argument("--request-stdin", action="store_true")
    parser.add_argument("--execute-read", action="store_true", help="Run only an already-authorized routed read")
    args = parser.parse_args(argv)
    try:
        request = json.load(sys.stdin) if args.request_stdin else None
        result = execute(args.operation, request) if args.execute_read else readiness(args.operation, request)
    except ContractInspectionFailure as error:
        result = {"status": "blocked", "write_eligible": False,
                  "message": str(error), "partial_facts": error.facts}
    except (ValueError, OSError):
        result = {"status": "failed", "write_eligible": False,
                  "message": "CAP request or shared read failed; review input, source readiness, configured target and declared shared diagnostics. No write occurred."}
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"ready_for_read_preflight", "complete", "matched", "observed", "no_accessible_match", "ambiguous", "assessed_writes_blocked"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
