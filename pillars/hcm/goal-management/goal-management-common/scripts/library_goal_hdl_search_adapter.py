"""HDL-only Library Goal search normalization; never treats missing rows as empty."""
from __future__ import annotations

import json
from hdl_dat_validator import HdlDatValidationError


def _integer(value, label):
    if isinstance(value, bool) or not str(value).isdigit():
        raise HdlDatValidationError(f"SEARCH_RESPONSE_INVALID: {label} must be an integer.")
    return int(value)


def normalize_page(response, *, expected_offset=0):
    if not isinstance(response, dict) or "result" not in response:
        raise HdlDatValidationError("SEARCH_RESPONSE_INVALID: missing action result.")
    result = response["result"]
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except ValueError as exc:
            raise HdlDatValidationError("SEARCH_RESPONSE_INVALID: invalid result JSON.") from exc
    if not isinstance(result, dict) or not isinstance(result.get("items"), list):
        raise HdlDatValidationError("SEARCH_RESPONSE_INVALID: result.items must be an array.")
    summary = result.get("summary")
    if not isinstance(summary, list) or len(summary) != 1 or not isinstance(summary[0], dict):
        raise HdlDatValidationError("SEARCH_RESPONSE_INVALID: one result.summary is required.")
    summary = summary[0]
    offset, count, limit = [_integer(summary.get(k), k) for k in ("offset", "count", "limit")]
    more = summary.get("hasMore")
    if more not in (True, False, "true", "false") or type(more) not in (bool, str):
        raise HdlDatValidationError("SEARCH_RESPONSE_INVALID: missing or invalid hasMore.")
    more = more is True or more == "true"
    rows = result["items"]
    if offset != expected_offset or count != len(rows) or limit < 1 or count > limit or (more and not count):
        raise HdlDatValidationError("SEARCH_RESPONSE_INVALID: inconsistent pagination.")
    if any(not isinstance(r, dict) or not isinstance(r.get("GoalName"), str) for r in rows):
        raise HdlDatValidationError("SEARCH_RESPONSE_INVALID: malformed goal row.")
    return {"items": rows, "hasMore": more, "nextOffset": offset + count}


def collect_pages(fetch_page, *, max_pages=1000):
    rows, offset = [], 0
    for _ in range(max_pages):
        page = normalize_page(fetch_page(offset), expected_offset=offset)
        rows.extend(page["items"])
        if not page["hasMore"]:
            return rows
        offset = page["nextOffset"]
    raise HdlDatValidationError("SEARCH_PAGINATION_LIMIT: duplicate check incomplete.")


def replay_pages(pages):
    if not isinstance(pages, list) or not pages:
        raise HdlDatValidationError("SEARCH_EVIDENCE_MISSING: supply complete captured pages.")
    rows, offset, more = [], 0, True
    for response in pages:
        if not more:
            raise HdlDatValidationError("SEARCH_RESPONSE_INVALID: pages follow a terminal page.")
        page = normalize_page(response, expected_offset=offset)
        rows.extend(page["items"])
        offset, more = page["nextOffset"], page["hasMore"]
    if more:
        raise HdlDatValidationError("SEARCH_PAGINATION_INCOMPLETE: more pages are required.")
    return rows
