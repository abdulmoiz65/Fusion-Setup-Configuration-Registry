"""Validate PABF tree versions from trusted core REST receipts; no I/O."""

from datetime import date
from urllib.parse import quote, urlencode, urlsplit


ROLES = {"project": "ProjTreeVersionName", "expenditure": "ExpTreeVersionName"}
RESOURCE = "/fscmRestApi/resources/11.13.18.05/fndTrees/"


class TreeVersionError(ValueError):
    def __init__(self, message, failure_class="input_validation"):
        super().__init__(message)
        self.failure_class = failure_class


def _date(value, field):
    try:
        result = date.fromisoformat(value)
        if result.isoformat() != value:
            raise ValueError("Noncanonical date")
        return result
    except (TypeError, ValueError):
        raise TreeVersionError(field + " is missing or is not a valid YYYY-MM-DD date.") from None


def request_url(rest_base_url, resolved_tree_code, version_name):
    base = urlsplit(rest_base_url)
    if (base.scheme != "https" or not base.netloc or base.username or base.password
            or base.query or base.fragment):
        raise TreeVersionError("A configured HTTPS restBaseUrl is required.")
    for value, label in ((resolved_tree_code, "REST-resolved TreeCode"), (version_name, "Tree Version Name")):
        if not isinstance(value, str) or not value.strip():
            raise TreeVersionError(label + " is required.")
    predicate = "TreeVersionName='" + version_name.replace("'", "''") + "'"
    return (rest_base_url.rstrip("/") + RESOURCE + quote(resolved_tree_code, safe="")
            + "/child/FndTreeVersionVO?" + urlencode({"q": predicate}))


def _rows(receipt, target, tree_code, version, url, context):
    if (not isinstance(receipt, dict) or receipt.get("status") != "success"
            or receipt.get("complete") is not True):
        raise TreeVersionError(context + ": REST lookup failed or pagination is incomplete."
                               " Stop before generating the PABF import ZIP.", "fusion_api_error")
    if (receipt.get("restBaseUrl") != target or receipt.get("tree_code") != tree_code
            or receipt.get("version_name") != version or receipt.get("request_url") != url
            or not receipt.get("evidence_ref")):
        raise TreeVersionError(context + ": missing or mismatched REST provenance.")
    pages = receipt.get("pages")
    if not isinstance(pages, list) or not pages:
        raise TreeVersionError(context + ": pagination is incomplete.")
    result, offset = [], 0
    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            raise TreeVersionError(context + ": malformed REST page.")
        items = page.get("items")
        if (not isinstance(items, list) or type(page.get("count")) is not int
                or type(page.get("offset")) is not int or page["count"] != len(items)
                or page["offset"] != offset or page.get("hasMore") is not (index < len(pages) - 1)
                or (not items and index < len(pages) - 1)
                or any(not isinstance(row, dict) for row in items)):
            raise TreeVersionError(context + ": pagination is incomplete or malformed.")
        result.extend(items)
        offset += len(items)
    return result


def validate_tree_versions(hierarchies, rest_base_url, configuration_date, fetch_collection,
                           response_cache=None):
    """Validate each supplied role, returning names/receipts only on success.

    Each hierarchy contains TreeName, REST-resolved TreeCode, TreeVersionName
    and TreeEvidenceRef from its successful fndTrees resolution. The active
    workflow supplies the current target configuration date and a governed
    core fetch_collection(url) that retains all pages with target provenance.
    A task-run cache can be shared by the two version nodes; only successful,
    active, effective results are stored. No code is obtained from a name or
    from the version record. Omitted hierarchy roles preserve the baseline.
    """
    if not isinstance(hierarchies, dict) or set(hierarchies) - set(ROLES):
        raise TreeVersionError("Use only project and expenditure hierarchy roles.")
    as_of = _date(configuration_date, "Current target configuration date")
    cache = {} if response_cache is None else response_cache
    values, receipts = {}, {}
    for role, hierarchy in hierarchies.items():
        if not isinstance(hierarchy, dict):
            raise TreeVersionError(role + " hierarchy resolution evidence is required.")
        for key in ("TreeName", "TreeCode", "TreeVersionName", "TreeEvidenceRef"):
            if not isinstance(hierarchy.get(key), str) or not hierarchy[key].strip():
                raise TreeVersionError(role + " hierarchy is missing " + key + ".")
        tree, tree_code, version = (hierarchy[key] for key in ("TreeName", "TreeCode", "TreeVersionName"))
        context = role.capitalize() + " Tree Version Name " + version + " under Tree " + tree
        url = request_url(rest_base_url, tree_code, version)
        key = (rest_base_url, configuration_date, tree_code, version)
        if key in cache:
            receipt = cache[key]
        else:
            try:
                receipt = fetch_collection(url)
            except Exception:
                raise TreeVersionError(context + ": REST lookup failed; stop before generating the PABF import ZIP.",
                                       "transport_or_environment") from None
        records = _rows(receipt, rest_base_url, tree_code, version, url, context)
        if any(not isinstance(row.get("TreeVersionName"), str) or not row["TreeVersionName"]
               for row in records):
            raise TreeVersionError(context + ": incomplete TreeVersionName fields in REST result.")
        exact = [row for row in records if row["TreeVersionName"] == version]
        if not exact:
            raise TreeVersionError(role.capitalize() + " Tree Version Name " + version
                                   + " does not exist under " + role.capitalize() + " Tree " + tree
                                   + ". Provide a valid tree version name.")
        if len(exact) != 1:
            raise TreeVersionError(context + " is ambiguous: multiple exact matching versions exist.")
        record = exact[0]
        status = record.get("Status")
        if status != "ACTIVE":
            shown = status if isinstance(status, str) and status.strip() else "blank or missing Status"
            raise TreeVersionError("Tree Version Name " + version + " exists under Tree " + tree
                                   + " but is " + shown + ". Select or activate an active tree version"
                                   " before generating the PABF import ZIP.")
        start = _date(record.get("EffectiveStartDate"), context + " EffectiveStartDate")
        end = _date(record.get("EffectiveEndDate"), context + " EffectiveEndDate")
        if not start <= as_of <= end:
            raise TreeVersionError("Tree Version Name " + version + " exists under Tree " + tree
                                   + " but is not effective on configuration date " + configuration_date
                                   + " (EffectiveStartDate=" + record["EffectiveStartDate"]
                                   + ", EffectiveEndDate=" + record["EffectiveEndDate"] + ")"
                                   + ". Select an active effective tree version before generating the PABF import ZIP.")
        cache[key] = receipt
        values[ROLES[role]] = record["TreeVersionName"]
        receipts[role] = {
            "TreeName": tree, "ResolvedTreeCode": tree_code, "TreeEvidenceRef": hierarchy["TreeEvidenceRef"],
            "TreeVersionName": record["TreeVersionName"], "Status": status,
            "EffectiveStartDate": record["EffectiveStartDate"], "EffectiveEndDate": record["EffectiveEndDate"],
            "ConfigurationDate": configuration_date, "restBaseUrl": rest_base_url,
            "VersionEvidenceRef": receipt["evidence_ref"], "PaginationComplete": True,
        }
    return {"values": values, "receipts": receipts}
