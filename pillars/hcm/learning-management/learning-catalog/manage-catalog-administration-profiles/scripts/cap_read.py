"""Pure helpers for metadata-gated exact collection GETs; no I/O or auth.

Consuming rules select the resource, fields, finder, locale and page budget.
These helpers neither plan task rules nor authorize writes.
"""
from __future__ import annotations

import re
import math
import time


class LookupContractError(ValueError):
    pass


def exact_query(field: str, value: str) -> str:
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", field):
        raise LookupContractError("Invalid query attribute")
    if not isinstance(value, str) or not value.strip():
        raise LookupContractError("Selector must be nonempty text; never coerce numeric identifiers")
    # Query escaping varies by ADF release. Refuse unverified literals instead
    # of equating URL encoding with query-language escaping.
    if any(c in value for c in "'\"\\;\r\n\x00") or any(ord(c) < 32 for c in value):
        raise LookupContractError("Quoted, escaped or control-character selectors need a verified query-literal contract")
    return field + "='" + value + "'"


def resource_description(payload: dict, resource: str) -> dict:
    """Accept the named ADF describe resource only, not child attributes."""
    try:
        result = payload["Resources"][resource]
    except (KeyError, TypeError):
        raise LookupContractError("Describe response has no selected root resource")
    if not isinstance(result, dict):
        raise LookupContractError("Invalid root description")
    return result


def validate_metadata(description: dict, selector_field: str, required_fields: list[str], finder: str | None = None) -> None:
    collection = description.get("collection", {})
    # ADF describe advertises verbs under collection.actions. Some supplied
    # normalized descriptions use methods; never use item actions as proof.
    methods = collection.get("actions", collection.get("methods", []))
    if not any(isinstance(m, dict) and str(m.get("method", "")).upper() == "GET" for m in methods):
        raise LookupContractError("Collection GET not advertised")
    attrs = description.get("attributes")
    if not isinstance(attrs, list):
        raise LookupContractError("Root attributes missing")
    mapping = {a.get("name"): a for a in attrs if isinstance(a, dict)}
    if any(f not in mapping for f in required_fields):
        raise LookupContractError("Required response attributes missing")
    if any(mapping[f].get("type") != "string" for f in required_fields):
        raise LookupContractError("Required response fields must preserve string identity and text values")
    selected = mapping.get(selector_field, {})
    if selected.get("type") != "string" or selected.get("queryable") is not True:
        raise LookupContractError("Selector is not a queryable string")
    if finder:
        matches = [f for f in description.get("finders", description.get("collection", {}).get("finders", [])) if f.get("name") == finder]
        if len(matches) != 1 or not any(a.get("name") == selector_field for a in matches[0].get("attributes", [])):
            raise LookupContractError("Declared finder or its selector argument is missing")
        extra = [a for a in matches[0].get("attributes", []) if a.get("name") != selector_field and a.get("required") not in {"Optional", False, None}]
        if extra:
            raise LookupContractError("Finder requires additional verified arguments")


def collect_exact(fetch_page, query: dict[str, str], *, selector_field: str, value: str,
                  identity_fields: tuple[str, ...], max_pages: int = 20, page_size: int = 100) -> dict:
    """Exhaust offset paging with strict envelopes; never return partial success."""
    exact_query(selector_field, value)
    if not 1 <= max_pages <= 100 or not 1 <= page_size <= 500:
        raise LookupContractError("Invalid bounded pagination budget")
    matches = []
    seen = set()
    offset = 0
    for page_number in range(max_pages):
        page = fetch_page({**query, "limit": str(page_size), "offset": str(offset)})
        if not isinstance(page, dict) or not isinstance(page.get("items"), list):
            raise LookupContractError("Invalid collection response")
        items = page["items"]
        count, more = page.get("count"), page.get("hasMore")
        if (type(count) is not int or count != len(items) or type(more) is not bool
                or type(page.get("offset")) is not int or page["offset"] != offset
                or type(page.get("limit")) is not int or not 0 < page["limit"] <= page_size
                or count > page["limit"] or (more and not count)):
            raise LookupContractError("Incomplete or inconsistent pagination envelope")
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get(selector_field), str):
                raise LookupContractError("Selector field missing from result")
            identity = tuple(item.get(f) for f in identity_fields)
            if any(not isinstance(v, str) or not v for v in identity):
                raise LookupContractError("Identity missing or not text")
            if identity in seen:
                raise LookupContractError("Repeated identity across pages; collection changed or pagination ignored")
            seen.add(identity)
            if item[selector_field] == value:
                matches.append(item)
        if not more:
            return {"status": "matched" if len(matches) == 1 else "ambiguous" if matches else "no_accessible_match",
                    "match_count": len(matches), "matches": matches, "pages": page_number + 1,
                    "validation_purpose": "retrieval_only", "write_eligible": False}
        offset += count
    raise LookupContractError("Pagination budget exhausted; result is incomplete")


def finder_query(finder: str, argument: str, value: str) -> str:
    exact_query(argument, value)
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", finder) or any(c in value for c in ",=:"):
        raise LookupContractError("Finder identifier or value needs a verified parameter-escaping contract")
    return finder + ";" + argument + "=" + value


def validate_listing_metadata(description: dict, identity_fields: tuple[str, ...],
                              requested_fields: tuple[str, ...]) -> list[str]:
    """Listing needs a collection GET and stable text identity, not a finder."""
    collection = description.get("collection", {})
    actions = collection.get("actions", collection.get("methods", []))
    if not any(isinstance(a, dict) and a.get("method") == "GET" for a in actions):
        raise LookupContractError("Collection GET not advertised")
    attrs = description.get("attributes")
    if not isinstance(attrs, list) or not identity_fields:
        raise LookupContractError("Listing attributes or stable identity missing")
    names = [a.get("name") for a in attrs if isinstance(a, dict)]
    if len(names) != len(set(names)):
        raise LookupContractError("Duplicate metadata attributes")
    mapping = {a.get("name"): a for a in attrs if isinstance(a, dict)}
    fields = list(dict.fromkeys([*identity_fields, *requested_fields]))
    if any(f not in mapping for f in identity_fields):
        raise LookupContractError("Listing identity attribute missing")
    available = [f for f in fields if f in mapping]
    if any(mapping[f].get("type") != "string" for f in available):
        raise LookupContractError("Listing identity and selected fields must be text")
    return available


def collect_listing(fetch_page, query: dict[str, str], *, identity_fields: tuple[str, ...],
                    fields: list[str], max_pages: int = 20, page_size: int = 100,
                    max_rows: int = 2000, max_seconds: float = 120,
                    clock=time.monotonic) -> dict:
    """List only through a caller-selected GET; retain validated pages on failure.

    fetch_page(query, remaining_seconds) MUST enforce the supplied wall-clock
    timeout, including auth/retries. No I/O, auth or automatic retries live here.
    Returned rows are ephemeral. next_offset is diagnostic, not a safe resume token.
    """
    for value, ceiling in ((max_pages, 100), (page_size, 500), (max_rows, 50000)):
        if type(value) is not int or not 1 <= value <= ceiling:
            raise LookupContractError("Invalid listing page/row budget")
    if (type(max_seconds) not in (int, float) or not math.isfinite(max_seconds)
            or not 0 < max_seconds <= 600):
        raise LookupContractError("Invalid listing time budget")
    if (not identity_fields or not fields or len(fields) != len(set(fields))
            or not set(identity_fields).issubset(fields)
            or any(not isinstance(f, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", f) for f in fields)):
        raise LookupContractError("Listing requires declared fields and stable identity")
    if query != {"onlyData": "true", "fields": ",".join(fields)}:
        raise LookupContractError("Unfiltered listing accepts only declared fields and onlyData")
    started = clock()
    rows, seen = [], set()
    offset = pages = requests = 0

    def finish(code=None, failure_class=None):
        complete = code is None
        return {"status": "complete" if complete else "partial" if rows else "failed",
                "items": rows, "retrieved_count": len(rows),
                "pagination_completed": complete, "total_count": len(rows) if complete else None,
                "pages": pages, "requests": requests, "next_offset": None if complete else offset,
                "elapsed_seconds": max(0, clock() - started),
                "errors": [] if complete else [{"code": code, "failure_class": failure_class}],
                "validation_purpose": "retrieval_only", "write_eligible": False}

    while requests < max_pages:
        remaining = max_seconds - (clock() - started)
        if remaining <= 0:
            return finish("time_limit", "process_timeout")
        if len(rows) >= max_rows:
            return finish("row_limit", "process_timeout")
        limit = min(page_size, max_rows - len(rows))
        requests += 1
        try:
            page = fetch_page({**query, "limit": str(limit), "offset": str(offset)}, remaining)
        except Exception as exc:
            # Never reflect raw exception text: it can contain URLs or credentials.
            transport = isinstance(exc, (TimeoutError, OSError))
            return finish("fetch_timeout" if isinstance(exc, TimeoutError) else "fetch_error",
                          "transport_or_environment" if transport else "fusion_api_error")
        if not isinstance(page, dict) or not isinstance(page.get("items"), list):
            return finish("invalid_page", "catalog_or_metadata_mismatch")
        items, count, more = page["items"], page.get("count"), page.get("hasMore")
        if (type(count) is not int or count != len(items) or type(more) is not bool
                or type(page.get("offset")) is not int or page["offset"] != offset
                or type(page.get("limit")) is not int or not 0 < page["limit"] <= limit
                or count > page["limit"] or (more and not count)):
            return finish("inconsistent_pagination", "catalog_or_metadata_mismatch")
        pending, page_ids = [], set()
        for item in items:
            if not isinstance(item, dict):
                return finish("invalid_row", "catalog_or_metadata_mismatch")
            identity = tuple(item.get(f) for f in identity_fields)
            if any(not isinstance(v, str) or not v for v in identity):
                return finish("invalid_identity", "catalog_or_metadata_mismatch")
            if identity in seen or identity in page_ids:
                return finish("repeated_identity", "catalog_or_metadata_mismatch")
            if any(f in item and item[f] is not None and not isinstance(item[f], str) for f in fields):
                return finish("invalid_field_type", "catalog_or_metadata_mismatch")
            page_ids.add(identity)
            pending.append({f: item[f] for f in fields if f in item})
        rows.extend(pending)
        seen.update(page_ids)
        pages += 1
        offset += count
        if clock() - started >= max_seconds:
            return finish("time_limit", "process_timeout")
        if not more:
            return finish()
    return finish("page_limit", "process_timeout")
