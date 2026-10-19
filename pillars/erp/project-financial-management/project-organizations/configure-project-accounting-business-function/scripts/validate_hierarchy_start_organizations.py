"""Validate trusted, fully paginated PABF start-organization REST receipts.

No HTTP, authentication, file writes, ZIP generation, or Fusion mutations.
The active workflow supplies a core REST collection reader after its preflight.
"""

from datetime import date
from urllib.parse import urlencode, urlsplit


RESOURCE = "/fscmRestApi/resources/11.13.18.05/projectOrganizationsLOV"
ROLES = {
    "ProjStartOrgName": ("PROJECTS", "Project Organization",
                         "Project and Task Owning Organization Hierarchy"),
    "ExpStartOrgName": ("EXPENDITURES", "Expenditure Organization",
                        "Expenditure Organization Hierarchy"),
}


class StartOrganizationError(ValueError):
    def __init__(self, message, failure_class="input_validation"):
        super().__init__(message)
        self.failure_class = failure_class


def request_url(rest_base_url, organization_name):
    parsed = urlsplit(rest_base_url)
    if (parsed.scheme != "https" or not parsed.netloc or parsed.username
            or parsed.password or parsed.query or parsed.fragment):
        raise StartOrganizationError("A configured HTTPS restBaseUrl is required.")
    # Let the REST client consume the encoded query; never interpolate raw
    # organization names into a URL or widen the exact-name predicate.
    query = "OrganizationName='" + organization_name.replace("'", "''") + "'"
    return rest_base_url.rstrip("/") + RESOURCE + "?" + urlencode({"q": query})


def _date(value, field):
    try:
        result = date.fromisoformat(value)
        if result.isoformat() != value:
            raise ValueError("Noncanonical date")
        return result
    except (TypeError, ValueError):
        raise StartOrganizationError(field + " must be a valid YYYY-MM-DD date.") from None


def _collection(receipt, target, name, url, hierarchy):
    if (not isinstance(receipt, dict) or receipt.get("status") != "success"
            or receipt.get("complete") is not True):
        raise StartOrganizationError(
            name + ": REST lookup failed or pagination is incomplete for the " + hierarchy + ".",
            "fusion_api_error")
    if (receipt.get("restBaseUrl") != target or receipt.get("organization_name") != name
            or receipt.get("request_url") != url or not receipt.get("evidence_ref")):
        raise StartOrganizationError(name + ": missing or mismatched target lookup provenance for the "
                                     + hierarchy + ".")
    pages = receipt.get("pages")
    if not isinstance(pages, list) or not pages:
        raise StartOrganizationError(name + ": pagination is incomplete for the " + hierarchy + ".")
    rows, offset = [], 0
    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            raise StartOrganizationError(name + ": malformed collection page for the " + hierarchy + ".")
        items = page.get("items")
        if (not isinstance(items, list) or type(page.get("count")) is not int
                or type(page.get("offset")) is not int or page.get("count") != len(items)
                or page.get("offset") != offset
                or page.get("hasMore") is not (index < len(pages) - 1)
                or (not items and index < len(pages) - 1)):
            raise StartOrganizationError(name + ": pagination is incomplete for the " + hierarchy + ".")
        if any(not isinstance(row, dict) for row in items):
            raise StartOrganizationError(name + ": malformed organization row for the " + hierarchy + ".")
        rows.extend(items)
        offset += len(items)
    return rows


def resolve_start_organizations(names, rest_base_url, effective_date, fetch_collection,
                                collection_cache=None):
    """Return mapped names/receipts only when every supplied hierarchy role passes.

    names uses ProjStartOrgName and/or ExpStartOrgName; omitted roles preserve
    the task baseline. fetch_collection(url) must be the workflow's governed
    core reader returning successful, target-bound pages and evidence_ref.
    Identical names reuse one collection; the two graph nodes may share a
    task-run cache bound to the exact target, effective date and supplied name.
    """
    if not isinstance(names, dict) or set(names) - set(ROLES):
        raise StartOrganizationError("Use only ProjStartOrgName and ExpStartOrgName.")
    as_of = _date(effective_date, "Target validation effective date")
    cache = {} if collection_cache is None else collection_cache
    values, receipts = {}, {}
    for field, name in names.items():
        role, label, hierarchy = ROLES[field]
        if not isinstance(name, str) or not name.strip():
            raise StartOrganizationError(field + " requires a nonblank organization name.")
        url = request_url(rest_base_url, name)
        cache_key = (rest_base_url, effective_date, name)
        if cache_key not in cache:
            try:
                receipt = fetch_collection(url)
            except Exception:
                # Preserve only safe role context, never raw response bodies,
                # authentication headers, or transport exception payloads.
                raise StartOrganizationError(name + ": REST lookup failed for the " + hierarchy + ".",
                                             "transport_or_environment") from None
            _collection(receipt, rest_base_url, name, url, hierarchy)
            cache[cache_key] = receipt
        receipt = cache[cache_key]
        rows = _collection(receipt, rest_base_url, name, url, hierarchy)
        exact = [row for row in rows if row.get("OrganizationName") == name]
        active = {}
        for row in exact:
            identity = row.get("OrganizationId")
            if (type(identity) is not int or identity <= 0
                    or type(row.get("ActiveStatusFlag")) is not bool
                    or "ToDate" not in row or "ProjectOrganizationType" not in row):
                raise StartOrganizationError(name + ": incomplete organization fields for the " + hierarchy + ".")
            start = _date(row.get("FromDate"), "FromDate for " + name + " in the " + hierarchy)
            end = (_date(row["ToDate"], "ToDate for " + name + " in the " + hierarchy)
                   if row["ToDate"] is not None else date.max)
            if end < start:
                raise StartOrganizationError(name + ": invalid effective date range for the " + hierarchy + ".")
            if row["ActiveStatusFlag"] is True and start <= as_of <= end:
                active.setdefault(identity, []).append(row)
        if len(active) > 1:
            raise StartOrganizationError(name + " matches multiple active, effective OrganizationId values for the "
                                         + hierarchy + ". Select one organization.")
        eligible = ([row for row in next(iter(active.values()))
                     if row["ProjectOrganizationType"] == role] if active else [])
        if not eligible:
            raise StartOrganizationError(name + " is not an active " + label + " for the " + hierarchy + ".")
        # Different business-unit or duplicate rows for the same ID and role
        # are retained as evidence; they never create identity ambiguity.
        details = [{key: row[key] for key in ("OrganizationId", "OrganizationName", "FromDate",
                                             "ToDate", "ActiveStatusFlag", "ProjectOrganizationType")}
                   for row in eligible]
        values[field] = eligible[0]["OrganizationName"]
        receipts[field] = {
            "OrganizationId": eligible[0]["OrganizationId"],
            "OrganizationName": values[field], "ProjectOrganizationType": role,
            "EffectiveDate": effective_date, "RoleRows": details,
            "restBaseUrl": rest_base_url, "RequestPath": RESOURCE,
            "EvidenceRef": receipt["evidence_ref"], "PaginationComplete": True,
        }
    return {"values": values, "receipts": receipts}
