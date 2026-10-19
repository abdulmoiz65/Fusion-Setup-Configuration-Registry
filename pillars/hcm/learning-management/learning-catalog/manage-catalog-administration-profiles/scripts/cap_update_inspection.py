"""Bounded root-only update contract observation, using the shared GET client.

Item GET success is not proof of loader PATCH routing or effective write grants.
No user URL, HTTP implementation, write, upload or approval route exists here.
"""
from __future__ import annotations

import time
import re
from urllib.parse import quote
import cap_read
import cap_workflow as workflow
from cap_profile_inspection import parent_key
from cap_update_validation import BASELINE_FIELDS


def typed_field_metadata(raw):
    """Normalize only unambiguous positive lengths; never coerce permissions.

    Fusion describe can serialize maxLength as decimal text. Keep raw evidence
    separately and omit an unusable length from this typed projection so the
    update validator still fails closed for that field.
    """
    result = {}
    for name, field in raw.items():
        value = dict(field)
        length = value.pop("maxLength", None)
        if type(length) is int and length > 0:
            value["maxLength"] = length
        elif isinstance(length, str) and re.fullmatch(r"[0-9]{1,9}", length) and int(length) > 0:
            value["maxLength"] = int(length)
        result[name] = value
    return result


def inspect_update(request, *, get=None, clock=time.monotonic):
    ready = workflow.readiness("inspect-update-contract", request)
    if not ready["live_available"]:
        raise workflow.CapabilityUnavailable("Update inspection readiness failed")
    workflow.configured_context(request)
    get = get or workflow.shared_get
    start = clock()
    def remaining():
        seconds = 120 - (clock() - start)
        if seconds < 1:
            raise TimeoutError("Update inspection deadline reached")
        return seconds
    root = cap_read.resource_description(get(request, workflow.ROOT_PATH + "/describe", {}, remaining()),
                                         "learningCatalogProfiles")
    number = request["number"]
    attribute_rows = root.get("attributes")
    if (not isinstance(attribute_rows, list)
            or any(not isinstance(a, dict) or not isinstance(a.get("name"), str) or not a["name"]
                   for a in attribute_rows)
            or len({a["name"] for a in attribute_rows}) != len(attribute_rows)):
        raise ValueError("Malformed or duplicate root attribute metadata")
    cap_read.validate_metadata(root, "learningCatalogProfileNumber", ["learningCatalogProfileNumber", "name"])
    attrs = {a["name"]: a for a in root["attributes"]}
    fields = sorted(f for f in BASELINE_FIELDS if attrs.get(f, {}).get("type") == "string")
    query = {"onlyData": "false", "fields": ",".join(fields),
             "q": cap_read.exact_query("learningCatalogProfileNumber", number)}
    found = cap_read.collect_exact(lambda q: get(request, workflow.ROOT_PATH, q, remaining()), query,
        selector_field="learningCatalogProfileNumber", value=number,
        identity_fields=("learningCatalogProfileNumber",))
    result = {"status": found["status"], "match_count": found["match_count"],
              "environment": request["environment"], "host": request["host"],
              "validation_purpose": "update_contract_inspection_only", "write_eligible": False,
              "loader_mapping_verified": False, "write_grants_verified": False,
              "side_effects": [], "language": request.get("headers", {}).get("Accept-Language", "Server default"),
              "limitations": ["Account-visible, server-current, nontransactional observation",
                              "Item GET does not prove loader PATCH mapping, omitted-field behavior or write grants"]}
    result["field_metadata"] = {f: {k: attrs[f][k] for k in
        ("type", "updatable", "allowChanges", "maxLength", "mandatory", "required", "nullable") if k in attrs[f]}
        for f in ("description", "name", "visibility", "learningCatalogProfileNumber") if f in attrs}
    result["typed_field_metadata"] = typed_field_metadata(result["field_metadata"])
    result["metadata_normalization"] = "Positive decimal maxLength only; raw metadata retained; permissions unchanged"
    if found["status"] != "matched":
        return result
    row = found["matches"][0]
    baseline = {f: row[f] for f in fields if f in row}
    if any(v is not None and not isinstance(v, str) for v in baseline.values()):
        raise ValueError("Update baseline contains unexpected value types")
    if "expected_id" in request and baseline.get("learningCatalogProfileId") != request["expected_id"]:
        raise ValueError("Update inspection expected identity mismatch")
    result["baseline"] = baseline
    result["missing_baseline_fields"] = sorted(BASELINE_FIELDS - set(baseline))
    key, effective = parent_key(row, number)
    result["effective_date"] = effective
    result["item_routes"] = {}
    for label, encoded in (("canonical", key), ("number_only", quote(number, safe=""))):
        try:
            item = get(request, workflow.ROOT_PATH + "/" + encoded,
                       {"onlyData": "true", "fields": ",".join(fields)}, remaining())
        except workflow.SharedReadFailure:
            # Shared failure text is deliberately sanitized, not proof of HTTP 404.
            result["item_routes"][label] = {"status": "unverified", "reason": "Shared item GET failed; no status inferred"}
            result["status"] = "partial"
            break  # no retry or fallback after a failed request
        if not isinstance(item, dict) or item.get("learningCatalogProfileNumber") != number:
            raise ValueError("Item read returned a different or missing profile identity")
        if baseline.get("learningCatalogProfileId") is not None and (
                item.get("learningCatalogProfileId") != baseline["learningCatalogProfileId"]):
            raise ValueError("Item read returned a conflicting stable profile ID")
        matches = all(f in item and item[f] == v for f, v in baseline.items())
        result["item_routes"][label] = {"status": "matched" if matches else "baseline_changed",
                                        "matches_baseline": matches}
        if not matches:
            result["status"] = "partial"
            break
    return result
