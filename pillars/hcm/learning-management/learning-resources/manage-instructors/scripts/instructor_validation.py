#!/usr/bin/env python3
"""Instructor business rules only. Python 3.11+. No authentication or I/O."""
from __future__ import annotations

import copy
import hashlib
import json
import re

TASK_CODE = "CUSTOM_MANAGE_INSTRUCTORS"
BUSINESS_OBJECT = "learningInstructors"
MAX_ROWS = 20  # Local execution bound, not a Fusion product limit.
PERSON_FIELDS = ("PersonId", "DisplayName", "PersonNumber", "DepartmentName",
                 "LocationName", "AssignmentStatusType")
KINDS = {"person_number", "person_id", "full_name", "partial_name", "email"}


class InstructorError(ValueError):
    """Safe diagnostic: never embed a person value, response body, or token."""
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def fail(code, message):
    raise InstructorError(code, message)


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(",", ":")).encode()).hexdigest()


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]+", value):
        fail("input_validation", "Person IDs must be digit strings; never coerce floating-point IDs.")
    return value


def search_text(value):
    if not isinstance(value, str) or not value.strip():
        fail("input_validation", "Supply a person identifier or a person search request.")
    value = value.strip()
    # Finder delimiters have no source-verified escaping contract. Do not guess one.
    if any(ord(c) < 32 for c in value) or any(c in value for c in ",;=|%\\") or "://" in value:
        fail("input_validation", "Unsupported finder delimiter; use an exact person ID instead.")
    return value


def normalize_request(value):
    if not isinstance(value, dict) or set(value) != {"operation", "rows"}:
        fail("input_validation", "Request requires only operation and rows.")
    if value["operation"] != "create":
        fail("unsupported", "Only standalone instructor creation is in scope.")
    rows = value["rows"]
    if not isinstance(rows, list) or not 1 <= len(rows) <= MAX_ROWS:
        fail("input_validation", "Supply between one and twenty instructor rows.")
    result, seen = [], set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"row_id", "person", "provenance"}:
            fail("unsupported", "Rows accept row_id, person, provenance only; supplier and child data require a separate scope.")
        label = row["row_id"]
        if not isinstance(label, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", label) or label in seen:
            fail("input_validation", "Each row needs a unique stable row_id.")
        seen.add(label)
        if row["provenance"] != "user_supplied":
            fail("input_validation", "Do not infer a person from department, job, or context.")
        person = row["person"]
        if not isinstance(person, dict) or set(person) != {"kind", "value"} or person["kind"] not in KINDS:
            fail("input_validation", "Person needs one supported kind and value.")
        kind = person["kind"]
        if kind == "email":
            fail("unverified_contract", "Email resolution is unverified; ask for name, person number, or person ID.")
        text = identifier(person["value"]) if kind == "person_id" else search_text(person["value"])
        result.append({"row_id": label, "provenance": "user_supplied", "person": {"kind": kind, "value": text}})
    return {"operation": "create", "rows": result}


def person_view(item):
    if not isinstance(item, dict):
        fail("fusion_api", "Person response is not an object.")
    key = item.get("PersonId")
    # Fusion JSON may encode IDs as integers. Preserve strings and leading zeros.
    if type(key) is int:
        key = str(key)
    identifier(key)
    result = {field: item.get(field) for field in PERSON_FIELDS}
    result["PersonId"] = key
    return result


def unique_people(items):
    by_id = {}
    for item in items:
        person = person_view(item)
        key = person["PersonId"]
        if key in by_id and by_id[key] != person:
            fail("ambiguous", "Conflicting person/assignment rows; narrow the lookup.")
        by_id[key] = person
    return list(by_id.values())


def candidate_set(search, items, *, complete, context):
    """Keep this result in private runtime memory/storage, never project records."""
    people = unique_people(items)
    body = {"search": search_text(search), "context": copy.deepcopy(context),
            "complete": complete is True, "people": people}
    return {**body, "version": fingerprint(body),
            "candidates": [{"label": "C" + str(i + 1), **p} for i, p in enumerate(people)],
            "status": ("partial" if complete is not True else
                       "selection_required" if people else "no_accessible_candidates")}


def select_candidate(candidates, version, label, context):
    body = {k: candidates[k] for k in ("search", "context", "complete", "people")}
    if candidates.get("version") != version or fingerprint(body) != version or body["context"] != context:
        fail("stale_selection", "Candidate set or environment changed; repeat discovery and selection.")
    displayed = [{"label": "C" + str(i + 1), **p} for i, p in enumerate(body["people"])]
    if candidates.get("candidates") != displayed:
        fail("stale_selection", "Displayed candidates changed; repeat discovery and selection.")
    if not body["complete"]:
        fail("partial", "Discovery was incomplete; narrow the search before selecting.")
    if not isinstance(label, str) or not re.fullmatch(r"C[1-9][0-9]*", label):
        fail("selection_required", "Select an explicit candidate label, even for a single candidate.")
    index = int(label[1:]) - 1
    if index >= len(body["people"]):
        fail("selection_required", "Candidate label is not in this result set.")
    return body["people"][index]["PersonId"]  # Must be freshly resolved before proposal.


def resolve_exact(person_input, items, *, complete):
    if complete is not True:
        fail("partial", "Incomplete lookup cannot establish person uniqueness.")
    fields = {"person_id": "PersonId", "person_number": "PersonNumber", "full_name": "DisplayName"}
    field = fields.get(person_input["kind"])
    if field is None:
        fail("selection_required", "Partial names require explicit selection then a fresh ID lookup.")
    # Literal equality: no undocumented case folding or fuzzy identity decisions.
    matches = [p for p in unique_people(items) if p[field] == person_input["value"]]
    if len(matches) != 1:
        fail("no_match" if not matches else "ambiguous", "Exact lookup must resolve one accessible person.")
    if matches[0]["AssignmentStatusType"] != "ACTIVE":
        fail("unverified_contract", "Only verified ACTIVE assignments qualify; suspended/inactive semantics remain unresolved.")
    return matches[0]


def ensure_no_existing(person_id, items, *, complete):
    identifier(person_id)
    if complete is not True:
        fail("partial", "Incomplete instructor lookup cannot establish absence.")
    for item in items:
        if not isinstance(item, dict) or str(item.get("personId", "")) != person_id:
            fail("fusion_api", "Instructor lookup returned an unexpected person identity.")
    if items:
        fail("duplicate", "An accessible instructor already exists for this person; no create is allowed.")


def build_proposal(request, resolved_rows, *, environment, version):
    request = normalize_request(request)
    if type(version) is not int or version < 1 or not isinstance(environment, dict) or not environment:
        fail("input_validation", "Require a positive proposal version and verified target context.")
    if len(resolved_rows) != len(request["rows"]):
        fail("input_validation", "Every requested row must have a resolution; do not silently omit rows.")
    people, rows = set(), []
    for original, resolved in zip(request["rows"], resolved_rows):
        if resolved.get("row_id") != original["row_id"]:
            fail("input_validation", "Resolved row order/identity does not match the request.")
        person = person_view(resolved["person"])
        supplied = original["person"]
        if supplied["kind"] == "partial_name":
            selection = resolved.get("selection", {})
            if not {"candidates", "version", "label", "context"} <= set(selection):
                fail("selection_required", "A partial-name row needs its explicit version-bound selection.")
            chosen = select_candidate(selection["candidates"], selection["version"], selection["label"], selection["context"])
            if chosen != person["PersonId"] or selection["candidates"]["search"] != supplied["value"] or selection["context"] != environment:
                fail("stale_selection", "Selected person/search/target does not match the proposal.")
        else:
            resolve_exact(supplied, [person], complete=True)
        if person["AssignmentStatusType"] != "ACTIVE":
            fail("unverified_contract", "Non-active assignment creation is not enabled.")
        if person["PersonId"] in people:
            fail("duplicate", "Multiple input rows resolve to the same person.")
        people.add(person["PersonId"])
        rows.append({"row_id": original["row_id"], "person": person, "action": "create",
                     "inputs": {"personId": person["PersonId"]}, "trainingSupplier": None})
    body = {"taskCode": TASK_CODE, "businessObject": BUSINESS_OBJECT, "operation": "create",
            "version": version, "environment": copy.deepcopy(environment),
            "requestFingerprint": fingerprint(request), "rows": rows,
            "readiness": "draft_not_load_approval"}
    return {**body, "fingerprint": fingerprint(body)}


def verify_proposal(proposal):
    body = {k: v for k, v in proposal.items() if k != "fingerprint"}
    if proposal.get("fingerprint") != fingerprint(body):
        fail("stale_proposal", "Proposal changed; prepare a new version and preview.")
    if body.get("taskCode") != TASK_CODE or body.get("businessObject") != BUSINESS_OBJECT or body.get("operation") != "create":
        fail("unsupported", "This handoff is only for instructor creation.")
    return body


def verify_readback(person_id, items, *, complete):
    identifier(person_id)
    if complete is not True:
        return {"status": "partial", "verified": False, "count": len(items)}
    if len(items) != 1:
        return {"status": "no_accessible_match" if not items else "ambiguous", "verified": False, "count": len(items)}
    item = items[0]
    if str(item.get("personId", "")) != person_id:
        fail("fusion_api", "Readback person identity does not match the attempted row.")
    missing = [k for k in ("instructorId", "instructorNumber", "trainingSupplierId", "instructorStatus") if k not in item or (item[k] is None and k != "trainingSupplierId")]
    supplier_absent = "trainingSupplierId" in item and item["trainingSupplierId"] is None
    return {"status": "verified_root" if not missing and supplier_absent and item.get("instructorNumber") and item.get("instructorId") else "verification_pending",
            "verified": not missing and supplier_absent and bool(item.get("instructorNumber")) and bool(item.get("instructorId")),
            "count": 1, "missingFields": missing, "supplierAbsent": supplier_absent,
            "profile": {k: item.get(k) for k in ("instructorId", "instructorNumber", "instructorStatus")},
            "schedulingAvailability": "not_verified"}
