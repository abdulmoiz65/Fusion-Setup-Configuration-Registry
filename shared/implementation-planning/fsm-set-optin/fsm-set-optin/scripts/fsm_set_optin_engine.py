"""Shared Oracle Fusion FSM Redwood opt-in engine.

This module owns the low-level lookup, choice selection, Fusion Common PATCH,
and ADF refresh mechanics for FSM set opt-in workflows. Callers supply OAuth
access tokens produced by the FSCR Fusion OAuth authentication skill.
"""

from __future__ import annotations

import importlib.util
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

_transport_path = (
    Path(__file__).resolve().parents[5]
    / "core/fusion-api/rest-api-client/scripts/trusted_http.py"
)
# Load the new security boundary from this code installation only. Do not
# fall back to a same-named module in cwd/PYTHONPATH or sys.modules.
if _transport_path.resolve() != _transport_path or not _transport_path.is_file():
    raise ImportError("Trusted core HTTP transport is missing or redirected; restore the FSCR installation.")
_transport_spec = importlib.util.spec_from_file_location("_fsm_optin_trusted_http", _transport_path)
if _transport_spec is None or _transport_spec.loader is None:
    raise ImportError("Trusted core HTTP transport could not be loaded.")
trusted_http = importlib.util.module_from_spec(_transport_spec)
_transport_spec.loader.exec_module(trusted_http)
DestinationError = trusted_http.DestinationError
normalize_service_origin = trusted_http.normalize_service_origin
open_authenticated = trusted_http.open_authenticated
validate_destination = trusted_http.validate_destination


ACTION_CONTENT_TYPE = "application/vnd.oracle.adf.action+json"
DEFAULT_PAGE_SIZE = 500

TARGETS = {
    "offering": {
        "aliases": {"offering", "offerings"},
        "path": "/api/boss/extraction/queries/ora/commonSetup/features/v1/$en/searchOfferings",
    },
    "functional-area": {
        "aliases": {"functional-area", "functional-areas", "functional_area", "functional_areas", "fa", "fas"},
        "path": "/api/boss/extraction/queries/ora/commonSetup/features/v1/$en/searchFunctionalAreas",
    },
    "feature": {
        "aliases": {"feature", "features"},
        "path": "/api/boss/extraction/queries/ora/commonSetup/features/v1/$en/searchFeatures",
    },
}

LOOKUP_FEATURE_TYPES = {
    "offering": "OFFERING",
    "functional-area": "FUNCTIONAL_AREA",
    "feature": "FEATURE",
}


class OptinError(RuntimeError):
    """Raised for expected FSM set opt-in workflow failures."""


class OptinHttpError(OptinError):
    """Raised when Fusion returns an HTTP error."""

    def __init__(self, status_code: int, method: str, url: str, body: bytes) -> None:
        self.status_code = status_code
        self.method = method
        self.url = url
        self.body = body
        super().__init__(f"HTTP {status_code} for {method} {redacted_url(url)}: {body_preview(body)}")


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def redact(value: str) -> str:
    value = re.sub(r"Authorization:\s*Bearer\s+[A-Za-z0-9._~+/=-]+", "Authorization: Bearer <redacted>", value, flags=re.I)
    value = re.sub(r"Bearer\s+[A-Za-z0-9._~+/=-]+", "Bearer <redacted>", value, flags=re.I)
    value = re.sub(r"Authorization:\s*Basic\s+[A-Za-z0-9+/=]+", "Authorization: Basic <redacted>", value, flags=re.I)
    return value


def redacted_url(url: str) -> str:
    return redact(url)


def body_preview(body: bytes, limit: int = 1200) -> str:
    text = body.decode("utf-8", errors="replace")
    if len(text) > limit:
        text = text[:limit] + "...<truncated>"
    return redact(text)


def decode_body(body: bytes) -> Any:
    text = body.decode("utf-8", errors="replace") if body else ""
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def normalize_base_url(raw: str) -> str:
    try:
        return normalize_service_origin(raw)
    except DestinationError as exc:
        raise OptinError(str(exc)) from exc


def validate_base_url(raw: str, approved_origin: str) -> str:
    base_url = normalize_base_url(raw)
    try:
        return validate_destination(base_url, normalize_base_url(approved_origin))
    except DestinationError as exc:
        raise OptinError(str(exc)) from exc


def normalize_resource_root(raw: str, api_version: str = "latest") -> str:
    base = normalize_base_url(raw)
    value = raw.strip().rstrip("/")
    if not re.match(r"^[a-z][a-z0-9+.-]*://", value, flags=re.I):
        value = "https://" + value
    parsed = urllib.parse.urlsplit(value)
    marker = "/fscmRestApi/resources/"
    if marker in parsed.path:
        before, after = parsed.path.split(marker, 1)
        version = after.split("/", 1)[0] or api_version
        return f"{base}{before}{marker}{version}".rstrip("/")
    return f"{base}/fscmRestApi/resources/{api_version}".rstrip("/")


def build_url(base_url: str, path: str, params: dict[str, Any] | None = None) -> str:
    url = urllib.parse.urljoin(normalize_base_url(base_url) + "/", path)
    parsed = urllib.parse.urlparse(url)
    pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    if params:
        pairs.extend((key, str(value)) for key, value in params.items() if value is not None)
    return urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(pairs)))


def request_json(
    access_token: str,
    method: str,
    url: str,
    *,
    approved_origin: str,
    body: Any | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 120,
    include_response_url: bool = False,
) -> dict[str, Any]:
    try:
        validate_destination(url, approved_origin)
    except DestinationError as exc:
        raise OptinError(str(exc)) from exc
    request_headers = dict(headers or {})
    request_headers["Authorization"] = f"Bearer {access_token}"
    request_headers.setdefault("Accept", "application/json, */*")
    payload = None
    if body is not None:
        payload = json.dumps(body).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=payload, headers=request_headers, method=method)
    try:
        with open_authenticated(req, approved_origin=approved_origin, timeout=timeout) as resp:
            result = {"status": resp.status, "body": decode_body(resp.read())}
            # Pagination needs the final URL after redirects. Keep existing
            # PATCH/refresh result and report shapes unchanged for other calls.
            if include_response_url:
                result["url"] = resp.geturl()
            return result
    except DestinationError as exc:
        raise OptinError(str(exc)) from exc
    except urllib.error.HTTPError as exc:
        raise OptinHttpError(exc.code, method, url, exc.read()) from exc
    except urllib.error.URLError as exc:
        raise OptinError(f"Network error for {method} {redacted_url(url)}: {redact(str(exc))}") from exc


def response_items(body: Any) -> list[dict[str, Any]]:
    if isinstance(body, list):
        return [item for item in body if isinstance(item, dict)]
    if not isinstance(body, dict):
        return []
    for key in ("items", "Items", "results", "Results", "value", "Value", "rows", "Rows", "data", "Data"):
        value = body.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    for key in ("result", "Result"):
        value = body.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            nested = response_items(value)
            if nested:
                return nested
    return []


def get_ci(row: Any, *keys: str) -> Any:
    if not isinstance(row, dict):
        return None
    lowered = {str(key).lower(): value for key, value in row.items()}
    for key in keys:
        value = lowered.get(key.lower())
        if value is not None:
            return value
    return None


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"true", "t", "yes", "y", "1"}
    return False


def page_has_more(body: Any) -> bool:
    if not isinstance(body, dict):
        return False
    for key in ("hasMore", "hasMoreRecords", "hasMoreResults", "hasNext", "more"):
        if truthy(get_ci(body, key)):
            return True
    links = body.get("links") or body.get("Links")
    if isinstance(links, list):
        return any(str(link.get("rel") or "").lower() == "next" for link in links if isinstance(link, dict))
    return False


def next_link(body: Any) -> str | None:
    if not isinstance(body, dict):
        return None
    links = body.get("links") or body.get("Links")
    if not isinstance(links, list):
        return None
    for link in links:
        if isinstance(link, dict) and str(link.get("rel") or "").lower() == "next":
            href = link.get("href") or link.get("Href")
            return str(href) if href else None
    return None


def page_count(body: Any, items: list[dict[str, Any]]) -> int:
    value = get_ci(body, "count", "itemCount")
    try:
        return int(value)
    except (TypeError, ValueError):
        return len(items)


def odata_literal(value: str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def urlencode(params: dict[str, Any]) -> str:
    return urllib.parse.urlencode([(key, value) for key, value in params.items() if value is not None])


class BossClient:
    def __init__(self, base_url: str, access_token: str, page_size: int = DEFAULT_PAGE_SIZE, timeout: int = 120,
                 *, approved_origin: str) -> None:
        self.approved_origin = normalize_base_url(approved_origin)
        self.base_url = validate_base_url(base_url, self.approved_origin)
        self.access_token = access_token
        self.page_size = page_size
        self.timeout = timeout

    def _request(self, method: str, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = build_url(self.base_url, path, params)
        return request_json(
            self.access_token,
            method,
            url,
            approved_origin=self.approved_origin,
            timeout=self.timeout,
            include_response_url=True,
        )

    def request_json(self, method: str, path: str, params: dict[str, Any] | None = None) -> Any:
        return self._request(method, path, params)["body"]

    def get_all(self, path: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        query = dict(params or {})
        offset = 0
        response = self._request("GET", path, query)
        while True:
            body = response["body"]
            items = response_items(body)
            records.extend(items)
            if not page_has_more(body):
                break
            link = next_link(body)
            if link:
                response = self._request("GET", urllib.parse.urljoin(response["url"], link))
                continue
            count = page_count(body, items)
            if count == 0:
                break
            offset += count
            query["$limit"] = self.page_size
            query["$offset"] = offset
            response = self._request("GET", path, query)
        return records


def normalize_target_type(value: str) -> str:
    normalized = value.strip().lower().replace("_", "-")
    for canonical, config in TARGETS.items():
        if normalized in config["aliases"]:
            return canonical
    raise OptinError("Target type must be offering, functional-area/fa, or feature.")


def normalize_action(value: str) -> str:
    normalized = value.strip().lower().replace("_", "-")
    aliases = {
        "enable": "opt-in",
        "opt-in": "opt-in",
        "optin": "opt-in",
        "on": "opt-in",
        "disable": "opt-out",
        "opt-out": "opt-out",
        "optout": "opt-out",
        "off": "opt-out",
        "set": "set-choices",
        "set-choice": "set-choices",
        "set-choices": "set-choices",
        "choices": "set-choices",
    }
    if normalized not in aliases:
        raise OptinError("Action must be opt-in, opt-out, enable, disable, or set-choices.")
    return aliases[normalized]


def feature_short_name(row: dict[str, Any]) -> str | None:
    value = get_ci(row, "featureShortName", "FeatureShortName", "shortName", "ShortName", "code", "Code")
    return str(value) if value not in (None, "") else None


def feature_name(row: dict[str, Any]) -> str | None:
    value = get_ci(row, "featureName", "FeatureName", "name", "Name", "displayName", "DisplayName")
    return str(value) if value not in (None, "") else None


def feature_id(row: dict[str, Any]) -> str | None:
    value = get_ci(row, "featureId", "FeatureId", "id", "Id")
    return str(value) if value not in (None, "") else None


def feature_classification(row: dict[str, Any]) -> str | None:
    value = get_ci(row, "classification", "Classification", "featureClassification", "FeatureClassification")
    return str(value) if value not in (None, "") else None


def unique_rows(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    unique: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = feature_short_name(row) or compact_json(row)
        unique[key] = row
    return unique


def candidate_preview(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "name": feature_name(row),
            "shortName": feature_short_name(row),
            "id": feature_id(row),
            "classification": feature_classification(row),
        }
        for row in rows[:20]
    ]


def lookup_code_api(access_token: str, rest_root: str, kind: str, query: str,
                    *, approved_origin: str) -> list[dict[str, Any]]:
    feature_type = LOOKUP_FEATURE_TYPES.get(kind)
    if not feature_type:
        return []
    params = urlencode(
        {
            "fields": "FeatureName,FeatureCode,FeatureType",
            "q": f"FeatureType={odata_literal(feature_type)};FeatureName={odata_literal(query)}",
        }
    )
    url = f"{rest_root}/features?{params}"
    body = request_json(access_token, "GET", url, approved_origin=approved_origin)["body"]
    return [
        {
            "featureName": get_ci(row, "FeatureName", "featureName"),
            "featureShortName": get_ci(row, "FeatureCode", "featureCode"),
            "classification": get_ci(row, "FeatureType", "featureType"),
            "raw": row,
        }
        for row in response_items(body)
    ]


def search_target(client: BossClient, kind: str, query: str, include_like: bool = True) -> list[dict[str, Any]]:
    path = TARGETS[kind]["path"]
    exact_short = f"featureShortName={odata_literal(query)}"
    exact_name = f"featureName={odata_literal(query)}"
    like_name = f"featureName ~Like {odata_literal('%' + query + '%')}"
    filters = [exact_short, exact_name]
    if include_like:
        filters.append(like_name)
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for filter_value in filters:
        for row in client.get_all(path, {"$filter": filter_value, "$limit": client.page_size}):
            key = feature_short_name(row) or compact_json(row)
            if key not in seen:
                seen.add(key)
                rows.append(row)
    return rows


def hydrate_lookup_code_row(client: BossClient, kind: str, row: dict[str, Any]) -> dict[str, Any]:
    short_name = feature_short_name(row)
    if not short_name:
        return row
    rows = search_target(client, kind, short_name, include_like=False)
    unique = unique_rows(rows)
    if len(unique) == 1:
        return next(iter(unique.values()))
    return row


def resolve_one(
    *,
    adf_access_token: str,
    rest_root: str,
    boss_client: BossClient,
    kind: str,
    query: str,
    label: str,
) -> dict[str, Any]:
    lookup_rows = lookup_code_api(
        adf_access_token, rest_root, kind, query, approved_origin=boss_client.approved_origin
    )
    if lookup_rows:
        unique = unique_rows(lookup_rows)
        if len(unique) == 1:
            return hydrate_lookup_code_row(boss_client, kind, next(iter(unique.values())))
        raise OptinError(f"Ambiguous {label} {query!r}. Candidates: {compact_json(candidate_preview(list(unique.values())))}")

    rows = search_target(boss_client, kind, query)
    if not rows:
        raise OptinError(f"No {label} matched {query!r}.")
    query_lower = query.strip().lower()
    exact = [
        row
        for row in rows
        if query_lower in {str(feature_short_name(row) or "").lower(), str(feature_name(row) or "").lower()}
    ]
    candidates = exact or rows
    unique = unique_rows(candidates)
    if len(unique) == 1:
        return next(iter(unique.values()))
    raise OptinError(f"Ambiguous {label} {query!r}. Candidates: {compact_json(candidate_preview(list(unique.values())))}")


def get_choices(client: BossClient, short_name: str) -> list[dict[str, Any]]:
    path = "/api/boss/extraction/queries/ora/commonSetup/features/v1/featureSelectedChoices"
    rows = client.get_all(path, {"featureShortName": short_name, "$limit": client.page_size})
    normalized = []
    for row in rows:
        normalized.append(
            {
                "choiceShortName": get_ci(row, "choiceShortName", "featureChoiceCode", "choiceCode"),
                "choiceName": get_ci(row, "choiceName", "featureChoiceName", "name"),
                "choiceEnabledFlag": truthy(get_ci(row, "choiceEnabledFlag")),
                "checkedFlag": truthy(get_ci(row, "checkedFlag")),
                "noneChoiceFlag": truthy(get_ci(row, "noneChoiceFlag", "noneChoice")),
                "raw": row,
            }
        )
    return normalized


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def choice_matches(choice: dict[str, Any], needle: str) -> bool:
    needle_lower = needle.strip().lower()
    values = [
        choice.get("choiceShortName"),
        choice.get("choiceName"),
        get_ci(choice.get("raw"), "featureChoiceCode"),
        get_ci(choice.get("raw"), "featureChoiceName"),
    ]
    return any(str(value).strip().lower() == needle_lower for value in values if value is not None)


def select_choices(choices: list[dict[str, Any]], action: str, requested_choices: list[str]) -> list[dict[str, Any]]:
    if not choices:
        raise OptinError("No feature choices were returned for the target.")
    if requested_choices:
        selected = []
        for requested in requested_choices:
            matches = [choice for choice in choices if choice_matches(choice, requested)]
            if len(matches) != 1:
                preview = [{"choiceShortName": c["choiceShortName"], "choiceName": c["choiceName"]} for c in choices]
                raise OptinError(f"Choice {requested!r} matched {len(matches)} rows. Available choices: {compact_json(preview)}")
            selected.append(matches[0])
        return selected

    desired = action == "opt-in"
    matches = [choice for choice in choices if choice["checkedFlag"] is desired]
    if len(matches) == 1:
        return matches
    if not desired:
        none = [
            choice
            for choice in choices
            if choice["noneChoiceFlag"] or str(choice.get("choiceShortName") or "").upper().startswith("ORA_NONE")
        ]
        if len(none) == 1:
            return none
    if desired:
        enabled_non_none = [choice for choice in choices if choice["choiceEnabledFlag"] and not choice["noneChoiceFlag"]]
        if len(enabled_non_none) == 1:
            return enabled_non_none
    preview = [
        {
            "choiceShortName": choice["choiceShortName"],
            "choiceName": choice["choiceName"],
            "checkedFlag": choice["checkedFlag"],
        }
        for choice in choices
    ]
    raise OptinError(f"Unable to infer choice for {action}. Provide --feature-choices. Available choices: {compact_json(preview)}")


def resolve_offering_context(
    *,
    adf_access_token: str,
    rest_root: str,
    boss_client: BossClient,
    target_kind: str,
    target_row: dict[str, Any],
    offering: str | None,
    offering_id: str | None,
) -> dict[str, Any]:
    if offering_id:
        return {
            "offeringId": offering_id,
            "offeringShortName": offering,
            "offeringName": None,
            "source": "--offering-id",
        }
    if target_kind == "offering":
        return {
            "offeringId": feature_id(target_row),
            "offeringShortName": feature_short_name(target_row),
            "offeringName": feature_name(target_row),
            "source": "target",
        }
    if offering:
        offering_row = resolve_one(
            adf_access_token=adf_access_token,
            rest_root=rest_root,
            boss_client=boss_client,
            kind="offering",
            query=offering,
            label="offering",
        )
        return {
            "offeringId": feature_id(offering_row),
            "offeringShortName": feature_short_name(offering_row),
            "offeringName": feature_name(offering_row),
            "source": "--offering",
        }

    short_name = feature_short_name(target_row)
    if not short_name:
        raise OptinError("Resolved target is missing featureShortName.")
    path = "/api/boss/extraction/queries/ora/commonSetup/features/v1/$en/sharedHierarchy"
    rows = boss_client.get_all(path, {"sharedHierarchyFor": short_name, "$limit": boss_client.page_size})
    if not rows:
        raise OptinError(f"Could not resolve parent offering for {short_name}. Provide --offering or --offering-id.")
    enabled = [row for row in rows if truthy(get_ci(row, "parentEnabledStatusFlag", "parentEnabledStatus"))]
    selected = (enabled or rows)[0]
    return {
        "offeringId": get_ci(selected, "parentId"),
        "offeringShortName": get_ci(selected, "parentShortName"),
        "offeringName": get_ci(selected, "parentName"),
        "source": "sharedHierarchy",
    }


def pre_disable_checks(
    client: BossClient,
    target_kind: str,
    target_row: dict[str, Any],
    offering_context: dict[str, Any],
    *,
    force: bool = False,
) -> list[str]:
    warnings: list[str] = []
    short_name = feature_short_name(target_row)
    if not short_name:
        raise OptinError("Resolved target is missing featureShortName.")

    locked_path = "/api/boss/extraction/queries/ora/commonSetup/features/v1/$en/lockedChildren"
    locked = client.get_all(locked_path, {"featureShortName": short_name, "$limit": client.page_size})
    if locked:
        names = [feature_name(row) or feature_short_name(row) for row in locked[:20]]
        message = "Disable blocked: locked children found: " + ", ".join(str(name) for name in names if name)
        if not force:
            raise OptinError(message)
        warnings.append(message)

    if target_kind != "offering" and offering_context.get("offeringShortName"):
        shared_path = "/api/boss/extraction/queries/ora/commonSetup/features/v1/$en/sharedHierarchy"
        shared = client.get_all(
            shared_path,
            {
                "sharedHierarchyFor": short_name,
                "excludeParentOffering": offering_context["offeringShortName"],
                "$limit": client.page_size,
            },
        )
        enabled = [row for row in shared if truthy(get_ci(row, "parentEnabledStatusFlag", "parentEnabledStatus"))]
        auto_enabled = [row for row in enabled if truthy(get_ci(row, "autoEnabledFlag"))]
        if auto_enabled:
            names = [get_ci(row, "parentName") for row in auto_enabled[:20]]
            message = "Disable blocked: target is auto-enabled by shared offering(s): " + ", ".join(str(name) for name in names if name)
            if not force:
                raise OptinError(message)
            warnings.append(message)
        elif enabled:
            names = [get_ci(row, "parentName") for row in enabled[:20]]
            message = "Target is also enabled in shared offering(s): " + ", ".join(str(name) for name in names if name)
            if not force:
                raise OptinError(message + ". Re-run with --force only after confirming the disable is intended.")
            warnings.append(message)
    return warnings


def patch_feature(base_url: str, short_name: str, body: dict[str, Any], access_token: str,
                  *, approved_origin: str) -> tuple[dict[str, Any], str]:
    url = f"{normalize_base_url(base_url)}/api/fusion-common/features/v1/features/{urllib.parse.quote(str(short_name), safe='')}"
    return request_json(access_token, "PATCH", url, body=body, approved_origin=approved_origin), url


def refresh_feature_selections(
    rest_root: str,
    offering_ids: list[str],
    access_token: str,
    *,
    approved_origin: str,
) -> tuple[dict[str, Any], str, dict[str, Any]]:
    url = f"{rest_root}/setupProcesses/action/refreshFeatureSelections"
    payload = {"additionalProperties": {str(index): str(value) for index, value in enumerate(offering_ids)}}
    headers = {"Content-Type": ACTION_CONTENT_TYPE, "Accept": "application/json, */*"}
    return request_json(access_token, "POST", url, body=payload, headers=headers,
                        approved_origin=approved_origin), url, payload


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "fsm-set-optin"


def write_standard_report(summary: dict[str, Any], path: Path) -> None:
    choices = ", ".join(str(choice.get("choiceShortName")) for choice in summary.get("selectedChoices", [])) or "-"
    warnings = summary.get("warnings") or ["None reported."]
    patch_result = summary.get("patchResult") if isinstance(summary.get("patchResult"), dict) else {}
    refresh_result = summary.get("refreshResult") if isinstance(summary.get("refreshResult"), dict) else {}
    lines = [
        "## Summary",
        f"- Environment: {summary.get('environment')}",
        f"- Target type: {summary.get('target', {}).get('type')}",
        f"- Target name: {summary.get('target', {}).get('name')}",
        f"- Target short name: {summary.get('target', {}).get('shortName')}",
        f"- Action: {summary.get('action')}",
        f"- Selected choices: {choices}",
        f"- Dry run: {summary.get('dryRun')}",
        "",
        "## Execution",
        f"- PATCH status: {patch_result.get('status', '-')}",
        f"- Refresh status: {refresh_result.get('status', '-')}",
        f"- Refresh offering IDs: {', '.join(summary.get('refreshOfferingIds') or []) or '-'}",
        "",
        "## Warnings",
        *[f"- {warning}" for warning in warnings],
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def run_set_optin(
    *,
    standard_access_token: str,
    boss_access_token: str,
    fusion_common_access_token: str | None,
    base_url: str,
    approved_origin: str,
    api_version: str,
    target_type: str,
    target: str,
    action: str,
    output_dir: Path,
    offering: str | None = None,
    offering_id: str | None = None,
    feature_choices: str | None = None,
    force: bool = False,
    dry_run: bool = False,
    page_size: int = DEFAULT_PAGE_SIZE,
) -> dict[str, Any]:
    base_url = validate_base_url(base_url, approved_origin)
    rest_root = normalize_resource_root(base_url, api_version)
    target_type = normalize_target_type(target_type)
    action = normalize_action(action)
    boss_client = BossClient(base_url, boss_access_token, page_size=page_size, approved_origin=approved_origin)

    row = resolve_one(
        adf_access_token=standard_access_token,
        rest_root=rest_root,
        boss_client=boss_client,
        kind=target_type,
        query=target,
        label=target_type,
    )
    short_name = feature_short_name(row)
    if not short_name:
        raise OptinError("Resolved target is missing featureShortName.")

    choices = get_choices(boss_client, short_name)
    selected_choices = select_choices(choices, action, split_csv(feature_choices))
    selected_codes = [str(choice.get("choiceShortName")) for choice in selected_choices if choice.get("choiceShortName")]
    if len(selected_codes) != len(selected_choices):
        raise OptinError("One or more selected choices are missing choiceShortName.")

    offering_context = resolve_offering_context(
        adf_access_token=standard_access_token,
        rest_root=rest_root,
        boss_client=boss_client,
        target_kind=target_type,
        target_row=row,
        offering=offering,
        offering_id=offering_id,
    )

    warnings: list[str] = []
    if action == "opt-out":
        warnings.extend(pre_disable_checks(boss_client, target_type, row, offering_context, force=force))

    classification = str(feature_classification(row) or "").upper()
    category = "ROOT_NODE" if target_type == "offering" or classification == "ROOT_NODE" else None
    patch_body: dict[str, Any] = {
        "selectedChoices": selected_codes,
        "caller": "REDWOOD",
    }
    if category is not None or target_type != "feature":
        patch_body["category"] = category

    offering_ids = []
    if offering_context.get("offeringId"):
        offering_ids.append(str(offering_context["offeringId"]))

    summary: dict[str, Any] = {
        "environment": base_url,
        "environmentResourceRoot": rest_root,
        "target": {
            "type": target_type,
            "name": feature_name(row),
            "shortName": short_name,
            "id": feature_id(row),
            "classification": feature_classification(row),
        },
        "action": action,
        "selectedChoices": [
            {
                "choiceShortName": choice.get("choiceShortName"),
                "choiceName": choice.get("choiceName"),
                "checkedFlag": choice.get("checkedFlag"),
            }
            for choice in selected_choices
        ],
        "offeringContext": offering_context,
        "refreshOfferingIds": offering_ids,
        "patchBody": patch_body,
        "warnings": warnings,
        "dryRun": dry_run,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    if dry_run:
        summary["patchSkipped"] = True
        summary["refreshSkipped"] = True
    else:
        if not fusion_common_access_token:
            raise OptinError("Fusion Common access token is required for write execution.")
        patch_result, patch_url = patch_feature(
            base_url, short_name, patch_body, fusion_common_access_token, approved_origin=approved_origin
        )
        summary["patchUrl"] = patch_url
        summary["patchResult"] = patch_result
        if offering_ids:
            refresh_result, refresh_url, refresh_payload = refresh_feature_selections(
                rest_root, offering_ids, standard_access_token, approved_origin=approved_origin
            )
            summary["refreshUrl"] = refresh_url
            summary["refreshPayload"] = refresh_payload
            summary["refreshResult"] = refresh_result
        summary["finalChoices"] = [
            {
                "choiceShortName": choice.get("choiceShortName"),
                "choiceName": choice.get("choiceName"),
                "checkedFlag": choice.get("checkedFlag"),
            }
            for choice in get_choices(boss_client, short_name)
        ]

    process_output = output_dir / f"fsm_set_optin_{slug(target_type)}_{slug(short_name)}_process_output.json"
    standard_report = output_dir / f"fsm_set_optin_{slug(target_type)}_{slug(short_name)}_standard_report.md"
    summary["processOutputPath"] = str(process_output.resolve())
    summary["standardReportPath"] = str(standard_report.resolve())
    process_output.write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    write_standard_report(summary, standard_report)
    return summary
