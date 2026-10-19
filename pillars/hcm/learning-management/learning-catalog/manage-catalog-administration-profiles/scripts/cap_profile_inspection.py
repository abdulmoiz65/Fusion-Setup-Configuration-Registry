"""Read-only profile/child inspection using the declared shared GET route.

Python3.11+. Parent key is obtained from a unique current response, never a
locally chosen date. Raw keys/person rows remain transient. No write API.
"""
from __future__ import annotations

from datetime import date
import re
import time
from urllib.parse import quote

import cap_read
import cap_workflow as workflow

CHILDREN = ("contributorCriteria", "contributorPersonList", "contentDefaults", "certificates")
PROCESS_FIELD_TYPES = {"reconcilePriority": "string", "reconcileStartDate": "datetime",
                       "reconcileEndDate": "datetime", "reconcileLastRunProcessDate": "datetime"}
PROCESS_FIELDS = tuple(PROCESS_FIELD_TYPES)
# Version1: Redwood uses row.criteriaId in contributorCriteria item URLs.
# This is a resource-specific identity, not an inference from required/inCreate.
# ora_reference_lookups.md carries the source and execution contract.
CHILD_IDENTITY_CONTRACTS = {"contributorCriteria": {"version": 1, "fields": {"criteriaId": "string"}}}


def parent_key(row, number):
    context = row.get("@context")
    key = context.get("key") if isinstance(context, dict) else None
    if not isinstance(key, str) or not key.endswith("," + number):
        raise ValueError("Canonical CAP key absent or mismatched")
    effective = key[:-(len(number) + 1)]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", effective):
        raise ValueError("Canonical effective date is not documented ISO date")
    date.fromisoformat(effective)
    return quote(key, safe=""), effective


def child_names(description):
    children = description.get("children", {})
    if isinstance(children, dict):
        return set(children)
    if isinstance(children, list):
        return {x.get("name") for x in children if isinstance(x, dict)}
    return set()


def child_identity(description, resource):
    """Return supported identity metadata or fail before reading business rows."""
    if not isinstance(description, dict) or not isinstance(description.get("collection"), dict):
        raise ValueError("Malformed child metadata")
    actions = description["collection"].get("actions", [])
    if not isinstance(actions, list):
        raise ValueError("Malformed child action metadata")
    if not any(isinstance(a, dict) and a.get("method") == "GET" for a in actions):
        raise ValueError("Collection GET not advertised")
    attrs = description.get("attributes", [])
    if not isinstance(attrs, list):
        raise ValueError("Malformed child attributes")
    mapping = {}
    for attr in attrs:
        if (not isinstance(attr, dict) or not isinstance(attr.get("name"), str)
                or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", attr["name"])
                or ("key" in attr and type(attr["key"]) is not bool)):
            raise ValueError("Malformed child attribute metadata")
        if attr["name"] in mapping:
            raise ValueError("Duplicate child attribute metadata")
        mapping[attr["name"]] = attr
    advertised = {name: attr.get("type") for name, attr in mapping.items() if attr.get("key") is True}
    explicit = CHILD_IDENTITY_CONTRACTS.get(resource, {}).get("fields")
    if explicit:
        if any(name not in mapping or mapping[name].get("type") != kind
               or mapping[name].get("key") is False for name, kind in explicit.items()):
            raise ValueError("Verified child identity absent or incompatible")
        if advertised and advertised != explicit:
            raise ValueError("Advertised and verified child identities conflict")
        return explicit
    if not advertised or any(kind not in {"string", "integer", "number"} for kind in advertised.values()):
        raise ValueError("No supported declared child identity")
    return advertised


def count_child(request, path, description, remaining, *, get, clock, resource=None):
    """Count validated records only; never emit person IDs or arbitrary values."""
    try:
        identity = child_identity(description, resource)
    except ValueError as exc:
        # These are fixed local messages, never values from the remote response.
        return {"status": "unavailable", "reason": str(exc)}
    keys = list(identity)
    # Reuse tested pagination logic with lossless numeric identity normalization.
    def fetch(query, budget):
        page = get(request, path, query, min(budget, remaining()))
        if not isinstance(page, dict) or not isinstance(page.get("items"), list):
            return page
        result = {**page, "items": []}
        for row in page["items"]:
            if not isinstance(row, dict):
                raise ValueError("Invalid child record")
            projected = {}
            for key, kind in identity.items():
                value = row.get(key)
                if ((kind == "string" and (not isinstance(value, str) or not value.strip()))
                        or (kind in {"integer", "number"} and type(value) is not int)):
                    raise ValueError("Invalid child identity")
                projected[key] = str(value)
            result["items"].append(projected)
        return result
    result = cap_read.collect_listing(fetch, {"onlyData": "true", "fields": ",".join(keys)},
        identity_fields=tuple(keys), fields=keys, max_seconds=min(120, remaining()), clock=clock)
    return {k: result[k] for k in ("status", "retrieved_count", "pagination_completed", "total_count", "pages", "errors")}


def result_envelope(request, root_result):
    return {"children": {}, "write_eligible": False, "validation_purpose": "retrieval_only",
        "match_count": root_result["match_count"],
        "root_lookup": {"pagination_completed": True, "pages": root_result["pages"]},
        "processing_completion_verified": False, "side_effects": [],
        "terminal_node": "CAP-I-DONE", "environment": request["environment"], "host": request["host"],
        "language": request.get("headers", {}).get("Accept-Language", "Server default"),
        "taskCode": workflow.CODE, "taskName": workflow.TASK,
        "completed_path": ["CAP-SELECT", "CAP-I-VALIDATE", "CAP-I-PREREQ", "CAP-I-READ"],
        "outcomes": {"CAP-SELECT": "profile", "CAP-I-VALIDATE": "passed", "CAP-I-PREREQ": "passed", "CAP-I-READ": "observed"},
        "limitations": ["Account-visible only", "Server-current date and selected/default language",
                        "Paginated observations are not a transactional snapshot",
                        "Criterion row counts are not effective contributor counts",
                        "Counts do not prove effective access, content inheritance or certificate rendering",
                        "No job completion or mutation is inferred from root state"]}


def inspect_profile(request, *, get=None, clock=time.monotonic):
    """Called by CAP-I route; revalidate also for direct Python callers."""
    ready = workflow.readiness("inspect-profile", request)
    if not ready["live_available"]:
        raise workflow.CapabilityUnavailable("Profile inspection readiness failed")
    workflow.configured_context(request)
    get = get or workflow.shared_get
    started = clock()
    def remaining():
        budget = 180 - (clock() - started)
        if budget < 1:
            raise TimeoutError("Profile inspection deadline reached")
        return budget
    root = cap_read.resource_description(get(request, workflow.ROOT_PATH + "/describe", {}, remaining()),
                                         "learningCatalogProfiles")
    number = request["number"]
    cap_read.validate_metadata(root, "learningCatalogProfileNumber", ["learningCatalogProfileNumber", "name"])
    attrs = {a.get("name"): a for a in root["attributes"] if isinstance(a, dict)}
    fields = list(cap_read.validate_listing_metadata(root, ("learningCatalogProfileNumber",), workflow.DISPLAY_FIELDS))
    fields += [f for f, kind in PROCESS_FIELD_TYPES.items() if attrs.get(f, {}).get("type") == kind]
    if "expected_id" in request:
        if attrs.get("learningCatalogProfileId", {}).get("type") not in {"string", "integer", "number"}:
            raise ValueError("Expected ID metadata missing")
        fields.append("learningCatalogProfileId")
    result = cap_read.collect_exact(lambda q: get(request, workflow.ROOT_PATH, q, remaining()),
        {"onlyData": "false", "fields": ",".join(fields),
         "q": cap_read.exact_query("learningCatalogProfileNumber", number)},
        selector_field="learningCatalogProfileNumber", value=number,
        identity_fields=("learningCatalogProfileNumber",))
    remaining()
    if result["status"] != "matched":
        return {**result_envelope(request, result), "status": result["status"]}
    row = result["matches"][0]
    if "expected_id" in request and (type(row.get("learningCatalogProfileId")) not in (int, str)
            or str(row["learningCatalogProfileId"]) != request["expected_id"]):
        raise ValueError("Expected profile identity mismatch")
    public = {f: row[f] for f in fields if f != "learningCatalogProfileId" and f in row}
    if any(value is not None and not isinstance(value, str) for value in public.values()):
        raise ValueError("Profile field type mismatch")
    output = {**result_envelope(request, result), "status": "observed", "profile": public,
        "unavailable_fields": [f for f in (*workflow.DISPLAY_FIELDS, *PROCESS_FIELDS) if f not in public]}
    try:
        key, effective = parent_key(row, number)
    except (ValueError, TypeError):
        output.update(status="partial", child_blocker="Canonical parent key unavailable; no child requests")
        return output
    output["effective_date"] = effective
    for child in CHILDREN:
        if child not in child_names(root):
            output["children"][child] = {"status": "unavailable", "reason": "Child not advertised by root describe"}
            continue
        path = workflow.ROOT_PATH + "/" + key + "/child/" + child
        try:
            description = cap_read.resource_description(get(request, path + "/describe", {}, remaining()), child)
            output["children"][child] = count_child(request, path, description, remaining,
                                                    get=get, clock=clock, resource=child)
        except (ValueError, OSError, TimeoutError):
            output["children"][child] = {"status": "unavailable", "reason": "Shared child metadata/read failed or deadline reached"}
    if any(v.get("status") != "complete" for v in output["children"].values()):
        output["status"] = "partial"
    return output
