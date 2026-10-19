"""Pure CAP proposal/revision model. It is NOT a Fusion payload or load approval."""
from __future__ import annotations

from copy import deepcopy
import argparse
import hashlib
import json
import sys
import uuid
import cap_visibility

ROW_FIELDS = {"content_group", "name", "description", "visibility", "ownership",
              "contributors", "central_override", "intent", "broad_general", "source"}
INTENTS = {"create", "reuse", "update", "activate", "deactivate", "delete",
           "contributors", "content-defaults", "certificates", "reconcile"}
LIMITS = {"name": 250, "description": 4000}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def normalize_row(supplied, row_id=None):
    if not isinstance(supplied, dict) or set(supplied) - ROW_FIELDS:
        raise ValueError("Unknown proposal field; this is not a REST payload")
    if not isinstance(supplied.get("source"), str) or not supplied["source"].strip():
        raise ValueError("A chat/file/page/sheet/row provenance reference is required")
    if not isinstance(supplied.get("content_group"), str) or not supplied["content_group"].strip():
        raise ValueError("Ask for ownership/content boundaries before inventing groups")
    row = {key: deepcopy(supplied.get(key)) for key in ROW_FIELDS}
    for field in ("content_group", "name", "description", "ownership", "central_override"):
        value = row[field]
        if value is not None and (not isinstance(value, str) or not value.strip() or "\x00" in value):
            raise ValueError("Proposal text must be nonempty text or unknown")
        if value is not None and len(value) > LIMITS.get(field, 4000):
            raise ValueError("Proposal field exceeds its limit; do not truncate")
    if row["visibility"] is not None:
        row["visibility"] = cap_visibility.normalize(row["visibility"])
    if row["intent"] is None:
        row["intent"] = "create"
    if row["intent"] not in INTENTS:
        raise ValueError("Unknown proposed operation")
    if row["broad_general"] is None:
        row["broad_general"] = False
    if type(row["broad_general"]) is not bool:
        raise ValueError("Broad general ownership must be explicitly true or false")
    contributors = row["contributors"]
    if contributors is not None:
        allowed = {"method", "input_ref", "sha256", "requested_count"}
        if not isinstance(contributors, dict) or set(contributors) - allowed:
            raise ValueError("Use sanitized contributor reference/counts, not a roster or asserted grants")
        if contributors.get("method") not in {"individual", "personNumber", "email", "none"}:
            raise ValueError("Unknown contributor intake method")
        if contributors["method"] != "none" and (not isinstance(contributors.get("input_ref"), str) or not contributors["input_ref"].strip()):
            raise ValueError("A protected contributor-input reference is required")
        count = contributors.get("requested_count")
        if count is not None and (type(count) is not int or count < 0):
            raise ValueError("Requested count must be a nonnegative integer or unknown")
        if contributors["method"] == "none" and count not in (None, 0):
            raise ValueError("No contributors conflicts with a nonzero requested count")
        if "sha256" in contributors:
            value = contributors["sha256"]
            if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
                raise ValueError("Invalid protected input hash")
    provenance = {key: {"kind": "user-specified" if row[key] is not None else "unknown",
                        "source": supplied["source"]} for key in ROW_FIELDS - {"source"}}
    if row["visibility"] is not None:
        provenance["visibility"]["input"] = supplied["visibility"]
    if row["name"] is None:
        row["name"] = row["content_group"] + " Catalog"
        if len(row["name"]) > LIMITS["name"]:
            raise ValueError("Generated name exceeds250 characters; request a shorter name")
        provenance["name"]["kind"] = "assistant-proposed"
    if "intent" not in supplied or supplied["intent"] is None:
        provenance["intent"]["kind"] = "assistant-proposed"
    if "broad_general" not in supplied or supplied["broad_general"] is None:
        provenance["broad_general"]["kind"] = "assistant-proposed"
    if row["description"] is None:
        row["description"] = "Catalog administration for " + row["content_group"] + "."
        if len(row["description"]) > LIMITS["description"]:
            raise ValueError("Generated description needs a shorter reviewed content-group label")
        provenance["description"]["kind"] = "assistant-proposed"
    row.update(row_id=row_id or "cap-row-" + str(uuid.uuid4()), provenance=provenance)
    row["missing_fields"] = [key for key in ("visibility", "ownership", "contributors") if row[key] is None]
    row["resolved_contributor_count"] = None
    row["baseline_status"] = "not_checked"
    return row


def draft(rows, *, proposal_id=None):
    if not isinstance(rows, list) or not rows or len(rows) > 100:
        raise ValueError("Provide one to 100 known content groups; do not invent structure")
    normalized = [normalize_row(row) for row in rows]
    names = [row["name"] for row in normalized if row["name"] is not None]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate exact proposal names need explicit reconciliation")
    return {"schema_version": "1.0", "proposal_id": proposal_id or "cap-proposal-" + str(uuid.uuid4()),
            "revision": 1, "rows": normalized, "previous_sha256": None, "changes": [],
            "approval": None, "write_eligible": False, "status": "draft",
            "next_step": "Review proposed values and provide missing ownership, visibility and contributor details.",
            "reply_example": "For row 1, keep the name and use Everyone visibility; contributors are in my protected input file."}


def revise(proposal, changes):
    """Return a new version, preserving the old object and stable untouched rows."""
    if not isinstance(changes, list) or not changes:
        raise ValueError("A nonempty explicit proposal change set is required")
    result = deepcopy(proposal)
    result["revision"] += 1
    result["previous_sha256"] = digest(proposal)
    result["approval"] = None
    result["write_eligible"] = False
    result["status"] = "draft"
    result["changes"] = []
    for change in changes:
        if not isinstance(change, dict) or set(change) - {"action", "row_id", "values"}:
            raise ValueError("Invalid proposal revision")
        action, row_id = change.get("action"), change.get("row_id")
        if action == "add":
            if row_id is not None:
                raise ValueError("New row identities are generated locally")
            row = normalize_row(change.get("values"))
            result["rows"].append(row)
            result["changes"].append({"action": "add_proposal_row", "row_id": row["row_id"], "after": deepcopy(row)})
            continue
        matches = [row for row in result["rows"] if row["row_id"] == row_id]
        if len(matches) != 1 or action not in {"edit", "remove"}:
            raise ValueError("Select exactly one existing proposal row and an edit/remove action")
        old = matches[0]
        index = result["rows"].index(old)
        if action == "remove":
            if "values" in change:
                raise ValueError("Removal takes no values and never deletes a Fusion CAP")
            result["rows"].pop(index)
            result["changes"].append({"action": "remove_proposal_row", "row_id": row_id, "before": old})
        else:
            values = change.get("values")
            if not isinstance(values, dict) or not values or "source" not in values:
                raise ValueError("Edits require changed values and their provenance")
            new = normalize_row({**{key: old[key] for key in ROW_FIELDS}, **values}, row_id)
            for key in ROW_FIELDS - set(values) - {"source"}:
                new["provenance"][key] = deepcopy(old["provenance"][key])
            result["rows"][index] = new
            result["changes"].append({"action": "edit_proposal_row", "row_id": row_id,
                                      "before": old, "after": deepcopy(new)})
    names = [row["name"] for row in result["rows"] if row["name"] is not None]
    if len(names) != len(set(names)) or len(result["rows"]) > 100:
        raise ValueError("Revision duplicates a name or exceeds the local row budget")
    return result


def baseline_candidates(row, baseline):
    """Compare accessible root evidence only; no business-scope or membership guess."""
    if not isinstance(baseline, dict) or baseline.get("pagination_completed") is not True:
        return {"status": "baseline_not_verified", "candidates": [], "absence_proven": False}
    items = baseline.get("items")
    if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
        raise ValueError("Invalid baseline collection")
    candidates = []
    for item in items:
        if not ((row["name"] is not None and item.get("name") == row["name"]) or
                (row["broad_general"] and item.get("isSystemDefault") == "Y")):
            continue
        differences = [key for key in ("name", "description", "visibility")
                       if row[key] is not None and item.get(key) != row[key]]
        status = item.get("status")
        candidates.append({"profile_number": item.get("learningCatalogProfileNumber"),
                           "system_default": item.get("isSystemDefault"),
                           "root_differences": differences,
                           "recommendation": "review_reuse" if status == "ORA_ACTIVE" else
                                             "review_activation" if status == "ORA_INACTIVE" else "ineligible_or_unknown",
                           "verification_needed": ["ownership/content scope", "effective contributors and access"],
                           "delete_allowed": False, "write_eligible": False})
    return {"status": "selection_required" if len(candidates) > 1 else
                      "review_candidate" if candidates else "no_accessible_candidate",
            "candidates": candidates, "absence_proven": False,
            "limitation": "Accessible root snapshot only; current business/access suitability is not established."}


def presentation_rows(proposal):
    """Business-facing projection; counts explicitly say requested, not verified."""
    return [{"row_id": row["row_id"], "content_group": row["content_group"],
             "name": row["name"], "description": row["description"],
             "who_manages": row["ownership"] or "Needs input",
             "who_views": cap_visibility.LABELS.get(row["visibility"], "Needs input"),
             "visibility_code": row["visibility"],
             "visibility_input": row["provenance"]["visibility"].get("input", row["visibility"]),
             "access_note": cap_visibility.ACCESS_NOTE,
             "contributor_count": {"requested": (row["contributors"] or {}).get("requested_count"),
                                   "resolved": row["resolved_contributor_count"], "effective": None},
             "existing_new": "Not verified; baseline not checked",
             "proposed_action": row["intent"], "central_override": row["central_override"] or "Not specified",
             "missing_fields": row["missing_fields"]} for row in proposal["rows"]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("draft", "revise", "present"))
    args = parser.parse_args()
    try:
        payload = json.load(sys.stdin)
        if args.action == "draft":
            result = draft(payload["rows"])
        elif args.action == "revise":
            result = revise(payload["proposal"], payload["changes"])
        else:
            result = presentation_rows(payload["proposal"])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (KeyError, TypeError, ValueError):
        # Never echo contributor/source contents or untrusted exception text.
        print(json.dumps({"status": "invalid_input", "write_eligible": False,
                          "next_step": "Check the local proposal contract and supply missing content-group/provenance fields.",
                          "reply_example": "Our named content groups are Engineering and shared learning."}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
