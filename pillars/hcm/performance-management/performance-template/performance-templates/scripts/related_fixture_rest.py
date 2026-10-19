#!/usr/bin/env python3
"""Fetch declared metadata and resolve Performance Template related fixtures."""

from __future__ import annotations

import argparse
from datetime import date
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Callable, Sequence
from urllib.parse import urlparse


TASK_ROOT = Path(__file__).resolve().parents[1]
FSCR_ROOT = Path(__file__).resolve().parents[6]
CONTRACT_PATH = TASK_ROOT / "ora-resource" / "related_fixture_routes.json"
REST_SCRIPTS = FSCR_ROOT / "core" / "fusion-api" / "rest-api-client" / "scripts"
AUTH_SCRIPTS = FSCR_ROOT / "core" / "auth" / "fusion-oauth-authentication" / "scripts"
sys.path.insert(0, str(REST_SCRIPTS))
sys.path.insert(0, str(AUTH_SCRIPTS))

from fusion_auth import FusionHttpError, get_access_token, read_properties, require_props  # noqa: E402
from rest_client_common import build_url, request_bytes  # noqa: E402


class RouteError(ValueError):
    """The request is outside the declared related-fixture contract."""


def stable_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(stable_bytes(value)).hexdigest()


def read_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RouteError(f"{label} is unavailable or invalid JSON: {path}") from error
    if not isinstance(value, dict):
        raise RouteError(f"{label} must be a JSON object")
    return value


def required_string(value: dict[str, Any], key: str) -> str:
    result = value.get(key)
    if not isinstance(result, str) or not result.strip():
        raise RouteError(f"Request specification requires nonblank {key}")
    return result.strip()


def validate_environment(environment: str) -> str:
    parsed = urlparse(environment)
    if parsed.scheme != "https" or not parsed.netloc or parsed.path not in {"", "/"}:
        raise RouteError("environment must be an HTTPS Fusion origin without a resource path")
    return environment.rstrip("/")


def contract() -> dict[str, Any]:
    return read_object(CONTRACT_PATH, "related-fixture route contract")


def metadata_binding(spec: dict[str, Any]) -> dict[str, Any]:
    routes = contract()["metadata_routes"]
    route_name = required_string(spec, "route")
    route = routes.get(route_name)
    if not isinstance(route, dict):
        raise RouteError(f"Metadata route is not declared: {route_name}")
    binding = {
        "environment": validate_environment(required_string(spec, "environment")),
        "method": "GET",
        "relative_path": route["path"],
        "query": {},
        "headers": contract()["required_headers"],
        "classification": "read_only_metadata",
        "route": route_name,
        "resource": route["resource"],
        "source": route["source"],
    }
    binding["binding_sha256"] = digest(binding)
    return binding


def _render_finder(route: dict[str, Any], arguments: dict[str, Any]) -> str | None:
    required = route.get("required_finder_arguments", [])
    if not required:
        if arguments:
            raise RouteError("This lookup route does not accept finder arguments")
        return None
    if set(arguments) != set(required):
        raise RouteError("Finder arguments must be exactly: " + ", ".join(required))
    allowed = route.get("allowed_finder_values", {})
    finder = route["finder"]
    for key in required:
        value = arguments[key]
        if not isinstance(value, str) or not value.strip() or any(ch in value for ch in ";,{}"):
            raise RouteError(f"Invalid finder argument {key}")
        if key in allowed and value not in allowed[key]:
            raise RouteError(f"Finder argument {key} is outside its declared allowlist")
        finder = finder.replace("{" + key + "}", value)
    return finder


def lookup_binding(spec: dict[str, Any], *, offset: int = 0) -> tuple[dict[str, Any], dict[str, Any]]:
    config = contract()
    route_name = required_string(spec, "route")
    route = config["lookup_routes"].get(route_name)
    if not isinstance(route, dict):
        raise RouteError(f"Lookup route is not declared: {route_name}")
    match_field = required_string(spec, "match_field")
    if match_field not in route["match_fields"]:
        raise RouteError(f"Match field is not allowed for {route_name}: {match_field}")
    match_value = required_string(spec, "match_value")
    query = dict(route.get("fixed_query", {}))
    query.update({"onlyData": "true", "limit": "499", "offset": str(offset)})
    if route.get("omit_fields") is not True:
        query["fields"] = ",".join(route["fields"])
    filters = spec.get("filters", {})
    if not isinstance(filters, dict):
        raise RouteError("filters must be an object")
    required_filters = route.get("required_filters", [])
    if set(filters) != set(required_filters):
        if filters or required_filters:
            raise RouteError("Filters must be exactly: " + ", ".join(required_filters))
    rendered_filters = []
    for key in required_filters:
        value = filters[key]
        if not isinstance(value, str) or not value.isdigit():
            raise RouteError(f"Filter {key} must be a numeric identifier string")
        rendered_filters.append(route["filter_templates"][key].replace("{value}", value))
    if rendered_filters:
        query["q"] = " and ".join(filter(None, [query.get("q"), *rendered_filters]))
    finder_arguments = spec.get("finder_arguments", {})
    if not isinstance(finder_arguments, dict):
        raise RouteError("finder_arguments must be an object")
    finder = _render_finder(route, finder_arguments)
    if finder:
        query["finder"] = finder
    binding = {
        "environment": validate_environment(required_string(spec, "environment")),
        "method": "GET",
        "relative_path": route["path"],
        "query": query,
        "headers": config["required_headers"],
        "classification": "read_only_lov",
        "route": route_name,
        "source": route["source"],
    }
    binding["binding_sha256"] = digest(binding)
    request = {
        "match_field": match_field,
        "match_value": match_value,
        "as_of": spec.get("as_of"),
        "identity_field": route["identity_field"],
    }
    return binding, request


def _resource_from_metadata(metadata: dict[str, Any], name: str) -> dict[str, Any]:
    resources = metadata.get("Resources")
    resource = resources.get(name) if isinstance(resources, dict) else None
    if not isinstance(resource, dict):
        raise RouteError(f"Metadata does not contain Resources.{name}")
    return resource


def _declared_action(resource: dict[str, Any], operation: str, method: str) -> None:
    level = "collection" if operation == "create" else "item"
    container = resource.get(level)
    actions = container.get("actions") if isinstance(container, dict) else None
    action_name = {"create": "create", "update": "update", "delete": "delete"}[operation]
    matches = [action for action in actions or [] if action.get("name") == action_name and action.get("method") == method]
    if len(matches) != 1:
        raise RouteError(f"Fresh metadata does not declare exactly one {method} {operation} action")


def _declared_item_get(resource: dict[str, Any]) -> None:
    item = resource.get("item")
    actions = item.get("actions") if isinstance(item, dict) else None
    matches = [
        action for action in actions or []
        if action.get("name") == "get" and action.get("method") == "GET"
    ]
    if len(matches) != 1:
        raise RouteError("Fresh metadata does not declare exactly one GET item action")


def _declared_collection_get(resource: dict[str, Any]) -> None:
    collection = resource.get("collection")
    actions = collection.get("actions") if isinstance(collection, dict) else None
    matches = [
        action for action in actions or []
        if action.get("name") == "get" and action.get("method") == "GET"
    ]
    if len(matches) != 1:
        raise RouteError("Fresh metadata does not declare exactly one GET collection action")


def _validate_setup_payload(resource: dict[str, Any], operation: str, payload: dict[str, Any]) -> None:
    if operation == "delete":
        if payload:
            raise RouteError("Delete does not accept a payload")
        return
    if not payload:
        raise RouteError(f"{operation} requires a nonempty payload")
    attributes = {
        item.get("name"): item
        for item in resource.get("attributes", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    unknown = sorted(set(payload) - set(attributes))
    if unknown:
        raise RouteError("Setup payload contains fields absent from fresh metadata: " + ", ".join(unknown))
    blocked = sorted(
        name for name in payload
        if not attributes[name].get("updatable", False)
        or attributes[name].get("allowChanges") == "never"
        or operation == "update" and attributes[name].get("allowChanges") == "inCreate"
    )
    if blocked:
        raise RouteError("Setup payload contains fields not writable for this operation: " + ", ".join(blocked))
    invalid_types = []
    for name, value in payload.items():
        attribute = attributes[name]
        valid = True
        if value is None:
            valid = not attribute.get("mandatory", False)
        elif attribute.get("type") == "boolean":
            valid = isinstance(value, bool)
        elif attribute.get("type") == "date":
            valid = isinstance(value, str)
            if valid:
                try:
                    date.fromisoformat(value)
                except ValueError:
                    valid = False
        elif attribute.get("type") == "string":
            valid = isinstance(value, str)
            if valid and attribute.get("format") == "BigInt":
                valid = value.isdigit()
            elif valid and attribute.get("format") == "BigDecimal":
                try:
                    Decimal(value)
                except InvalidOperation:
                    valid = False
        if not valid:
            invalid_types.append(name)
    if invalid_types:
        raise RouteError("Setup payload values do not match fresh metadata types: " + ", ".join(sorted(invalid_types)))
    if payload.get("SectionType") == "OS":
        os_false_fields = {
            "EnableItemsFlag", "ContentProfileFlag", "FreeFormAllowedFlag",
            "AddItemsConfirmCritFlag", "RateItemFlag",
            "UseSectionRatingForPerformanceRatingFlag", "ShowSectionWeightFlag",
            "ShowSectionMinimumWeightFlag", "ShowMandatoryFlag", "ShowCriticalFlag",
            "ShowDescriptionFlag", "ShowMeasurementFlag", "ShowDueDateFlag",
            "ShowReminderDateFlag", "ShowOwnedByFlag", "ShowStatusFlag",
            "ShowPercentCompleteFlag", "UseProfileFlag", "UseSpecifiedProfileFlag",
            "UseWorkerGoalsFlag", "UseSpecifiedContentItemFlag",
            "ShowTargetPerformanceRatingFlag", "ShowTargetProficiencyLevelFlag",
        }
        exposed_os_false_fields = os_false_fields.intersection(attributes)
        missing = sorted(name for name in exposed_os_false_fields if payload.get(name) is not False)
        if missing:
            raise RouteError(
                "Overall Summary requires source-declared false flags: " + ", ".join(missing)
            )
        os_null_fields = {
            "ContentTypeId", "RatingType", "PerformanceRatingModelId",
            "ItemCalculationCode", "ProfileTypeId", "ProfileId",
        }
        populated = sorted(name for name in os_null_fields if payload.get(name) is not None)
        if populated:
            raise RouteError("Overall Summary requires null fields: " + ", ".join(populated))
    if operation == "create":
        missing = sorted(
            name for name, item in attributes.items()
            if item.get("mandatory")
            and not item.get("hasDefaultValueExpression")
            and item.get("allowChanges") != "never"
            and name not in payload
        )
        if missing:
            raise RouteError("Setup create is missing metadata-required fields: " + ", ".join(missing))


def setup_preview(spec: dict[str, Any]) -> dict[str, Any]:
    config = contract()
    route_name = required_string(spec, "route")
    route = config["setup_routes"].get(route_name)
    if not isinstance(route, dict):
        raise RouteError(f"Setup route is not declared: {route_name}")
    operation = required_string(spec, "operation")
    method = route["allowed_operations"].get(operation)
    if not method:
        raise RouteError(f"Setup operation is not declared: {operation}")
    metadata_path = Path(required_string(spec, "metadata_path"))
    metadata_record = read_object(metadata_path, "fresh metadata record")
    if metadata_record.get("classification") != "read_only_metadata" or metadata_record.get("route") != route["metadata_route"]:
        raise RouteError("Setup metadata record does not match the route's declared metadata provider")
    metadata = metadata_record.get("metadata")
    if not isinstance(metadata, dict) or metadata_record.get("response_sha256") != digest(metadata):
        raise RouteError("Setup metadata record is missing or its response digest changed")
    resource = _resource_from_metadata(metadata, route["resource"])
    _declared_action(resource, operation, method)
    payload = spec.get("payload", {})
    if not isinstance(payload, dict):
        raise RouteError("payload must be an object")
    _validate_setup_payload(resource, operation, payload)
    relative_path = route["path"]
    identity = spec.get("identity")
    headers = {
        "REST-Framework-Version": "9",
        "Content-Type": "application/vnd.oracle.adf.resourceitem+json",
    }
    if operation in {"update", "delete"}:
        if not isinstance(identity, str) or not identity.isdigit():
            raise RouteError("Update and delete require a numeric identity string")
        relative_path += "/" + identity
        if_match = spec.get("if_match")
        if not isinstance(if_match, str) or not if_match.strip():
            raise RouteError("Update and delete require a nonblank fresh if_match value")
        headers["If-Match"] = if_match.strip()
    elif identity is not None:
        raise RouteError("Create must not bind a preexisting identity")
    binding = {
        "environment": validate_environment(required_string(spec, "environment")),
        "method": method,
        "relative_path": relative_path,
        "query": {},
        "headers": headers,
        "body_sha256": digest(payload) if payload else None,
        "metadata_response_sha256": metadata_record["response_sha256"],
        "contract_sha256": hashlib.sha256(CONTRACT_PATH.read_bytes()).hexdigest(),
        "classification": "writable_setup",
        "route": route_name,
        "operation": operation,
        "provider_skill": route["provider_skill"],
        "provider_offering": route.get("provider_offering"),
        "provider_task_code": route.get("provider_task_code"),
        "identity_field": route["identity_field"],
    }
    preview = {"schema_version": "1.0", "binding": binding, "payload": payload or None, "mutation": True}
    preview["preview_sha256"] = digest(preview)
    return preview


def setup_read_binding(spec: dict[str, Any]) -> dict[str, Any]:
    config = contract()
    route_name = required_string(spec, "route")
    route = config["setup_routes"].get(route_name)
    if not isinstance(route, dict):
        raise RouteError(f"Setup route is not declared: {route_name}")
    identity = required_string(spec, "identity")
    if not identity.isdigit():
        raise RouteError("Setup item read requires a numeric identity string")
    metadata_record = read_object(
        Path(required_string(spec, "metadata_path")), "fresh metadata record"
    )
    if (
        metadata_record.get("classification") != "read_only_metadata"
        or metadata_record.get("route") != route["metadata_route"]
    ):
        raise RouteError("Setup metadata record does not match the route's declared metadata provider")
    metadata = metadata_record.get("metadata")
    if not isinstance(metadata, dict) or metadata_record.get("response_sha256") != digest(metadata):
        raise RouteError("Setup metadata record is missing or its response digest changed")
    resource = _resource_from_metadata(metadata, route["resource"])
    _declared_item_get(resource)
    binding = {
        "environment": validate_environment(required_string(spec, "environment")),
        "method": "GET",
        "relative_path": route["path"] + "/" + identity,
        "query": {},
        "headers": config["required_headers"],
        "classification": "read_only_setup_item",
        "route": route_name,
        "identity": identity,
        "identity_field": route["identity_field"],
        "provider_skill": route["provider_skill"],
        "metadata_response_sha256": metadata_record["response_sha256"],
        "contract_sha256": hashlib.sha256(CONTRACT_PATH.read_bytes()).hexdigest(),
    }
    binding["binding_sha256"] = digest(binding)
    return binding


def setup_probe_binding(spec: dict[str, Any], *, offset: int = 0) -> tuple[dict[str, Any], str, str]:
    config = contract()
    route_name = required_string(spec, "route")
    route = config["setup_routes"].get(route_name)
    if not isinstance(route, dict):
        raise RouteError(f"Setup route is not declared: {route_name}")
    guard = route.get("duplicate_guard")
    if not isinstance(guard, dict):
        raise RouteError("Setup route does not declare a duplicate guard")
    match_field = required_string(spec, "match_field")
    if match_field != guard.get("match_field"):
        raise RouteError("Setup duplicate guard match field is not declared")
    match_value = required_string(spec, "match_value")
    metadata_record = read_object(
        Path(required_string(spec, "metadata_path")), "fresh metadata record"
    )
    if (
        metadata_record.get("classification") != "read_only_metadata"
        or metadata_record.get("route") != route["metadata_route"]
    ):
        raise RouteError("Setup metadata record does not match the route's declared metadata provider")
    metadata = metadata_record.get("metadata")
    if not isinstance(metadata, dict) or metadata_record.get("response_sha256") != digest(metadata):
        raise RouteError("Setup metadata record is missing or its response digest changed")
    resource = _resource_from_metadata(metadata, route["resource"])
    _declared_collection_get(resource)
    attribute_names = {
        item.get("name") for item in resource.get("attributes", []) if isinstance(item, dict)
    }
    fields = guard.get("fields")
    if not isinstance(fields, list) or not fields or any(field not in attribute_names for field in fields):
        raise RouteError("Setup duplicate guard fields do not match fresh metadata")
    binding = {
        "environment": validate_environment(required_string(spec, "environment")),
        "method": "GET",
        "relative_path": route["path"],
        "query": {
            "fields": ",".join(fields),
            "onlyData": "true",
            "limit": "499",
            "offset": str(offset),
        },
        "headers": config["required_headers"],
        "classification": "read_only_setup_duplicate_guard",
        "route": route_name,
        "provider_skill": route["provider_skill"],
        "metadata_response_sha256": metadata_record["response_sha256"],
        "contract_sha256": hashlib.sha256(CONTRACT_PATH.read_bytes()).hexdigest(),
    }
    binding["binding_sha256"] = digest(binding)
    return binding, match_field, match_value


def probe_setup_duplicates(
    spec: dict[str, Any], fetch_page: Callable[[dict[str, Any]], dict[str, Any]]
) -> dict[str, Any]:
    offset = 0
    matches: list[dict[str, Any]] = []
    pages: list[dict[str, Any]] = []
    while True:
        binding, match_field, match_value = setup_probe_binding(spec, offset=offset)
        body = fetch_page(binding)
        items = body.get("items")
        if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
            raise RouteError("Setup duplicate guard response does not contain an items array")
        matches.extend(item for item in items if str(item.get(match_field, "")) == match_value)
        pages.append({
            "binding_sha256": binding["binding_sha256"],
            "offset": offset,
            "count": len(items),
            "response_sha256": digest(body),
        })
        if not body.get("hasMore"):
            break
        next_offset = body.get("offset", offset) + body.get("limit", len(items))
        if not isinstance(next_offset, int) or next_offset <= offset:
            raise RouteError("Setup duplicate guard pagination did not advance")
        offset = next_offset
    return {
        "status": "resolved",
        "classification": "read_only_setup_duplicate_guard",
        "route": spec["route"],
        "match_field": match_field,
        "match_value": match_value,
        "match_count": len(matches),
        "matches": matches,
        "pages": pages,
    }


def validate_setup_approval(preview: dict[str, Any], approval: dict[str, Any]) -> None:
    expected_preview = preview.get("preview_sha256")
    material = dict(preview)
    material.pop("preview_sha256", None)
    if expected_preview != digest(material):
        raise RouteError("Setup preview digest changed")
    required = {
        "preview_sha256": expected_preview,
        "environment": preview["binding"]["environment"],
        "method": preview["binding"]["method"],
        "relative_path": preview["binding"]["relative_path"],
    }
    if approval.get("approved") is not True or any(approval.get(key) != value for key, value in required.items()):
        raise RouteError("Setup approval does not match the exact preview")
    if not approval.get("approved_at") or not approval.get("authorization_source"):
        raise RouteError("Setup approval must record time and authorization source")


def sanitize_provider_error(body: str) -> dict[str, Any] | str:
    """Keep bounded Oracle diagnostics without persisting URLs or credentials."""
    allowed = {"title", "detail", "errorCode", "o:errorCode", "message", "severity"}
    try:
        parsed = json.loads(body)
    except (TypeError, json.JSONDecodeError):
        return body[:1000]
    if not isinstance(parsed, dict):
        return "Provider returned a non-object error response"
    result: dict[str, Any] = {}
    def collect(value: Any) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                if key in allowed and isinstance(nested, (str, int, float, bool)):
                    result.setdefault(key, nested[:1000] if isinstance(nested, str) else nested)
                elif isinstance(nested, (dict, list)):
                    collect(nested)
        elif isinstance(value, list):
            for nested in value[:20]:
                collect(nested)
    collect(parsed)
    return result or "Provider returned an error without a safe diagnostic field"


def _parse_date(value: Any, field: str) -> date | None:
    if value in {None, ""}:
        return None
    if not isinstance(value, str):
        raise RouteError(f"Returned {field} is not an ISO date string")
    try:
        return date.fromisoformat(value[:10])
    except ValueError as error:
        raise RouteError(f"Returned {field} is not an ISO date string") from error


def validate_candidate(route: dict[str, Any], item: dict[str, Any], as_of: str | None) -> None:
    status = route.get("status")
    if status and item.get(status["field"]) not in status["allowed"]:
        raise RouteError("Exact lookup match is not active")
    for key, value in route.get("required_values", {}).items():
        actual = item.get(key)
        if isinstance(value, str):
            actual = str(actual) if actual is not None else actual
        if actual != value:
            raise RouteError(f"Exact lookup match has ineligible {key}")
    effectivity = route.get("effectivity")
    if effectivity:
        if not as_of:
            raise RouteError("This route requires as_of for a fresh effectivity check")
        try:
            day = date.fromisoformat(as_of)
        except ValueError as error:
            raise RouteError("as_of must use YYYY-MM-DD") from error
        start = _parse_date(item.get(effectivity["start"]), effectivity["start"])
        end = _parse_date(item.get(effectivity["end"]), effectivity["end"])
        if start and start > day or end and end < day:
            raise RouteError("Exact lookup match is not effective on as_of")


def list_pages(spec: dict[str, Any], fetch: Callable[[dict[str, Any]], dict[str, Any]]) -> dict[str, Any]:
    route_name = required_string(spec, "route")
    route = contract()["lookup_routes"].get(route_name)
    if not isinstance(route, dict) or route.get("allow_declared_list") is not True:
        raise RouteError("Declared list is not allowed for this lookup route")
    probe = dict(spec)
    probe.setdefault("match_field", route["identity_field"])
    probe.setdefault("match_value", "LIST_ONLY")
    items: list[dict[str, Any]] = []
    pages: list[dict[str, Any]] = []
    excluded_ineligible_count = 0
    offset = 0
    while True:
        binding, _request = lookup_binding(probe, offset=offset)
        body = fetch(binding)
        page_items = body.get("items", [])
        if not isinstance(page_items, list):
            raise RouteError("Lookup response items must be an array")
        for item in page_items:
            if not isinstance(item, dict):
                raise RouteError("Lookup response item must be an object")
            try:
                validate_candidate(route, item, spec.get("as_of"))
            except RouteError:
                excluded_ineligible_count += 1
                continue
            items.append(item)
        pages.append({"offset": offset, "count": len(page_items), "response_sha256": digest(body)})
        if not body.get("hasMore"):
            break
        offset += int(body.get("limit") or len(page_items) or 499)
    return {
        "status": "listed",
        "classification": "read_only_lov",
        "route": route_name,
        "item_count": len(items),
        "identity_field": route["identity_field"],
        "items": items,
        "excluded_ineligible_count": excluded_ineligible_count,
        "pages": pages,
    }


def resolve_pages(
    spec: dict[str, Any], fetch_page: Callable[[dict[str, Any]], dict[str, Any]]
) -> dict[str, Any]:
    route = contract()["lookup_routes"][required_string(spec, "route")]
    offset = 0
    matches: list[dict[str, Any]] = []
    page_audits: list[dict[str, Any]] = []
    while True:
        binding, request = lookup_binding(spec, offset=offset)
        body = fetch_page(binding)
        items = body.get("items")
        if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
            raise RouteError("Lookup response does not contain an items array")
        matches.extend(item for item in items if str(item.get(request["match_field"], "")) == request["match_value"])
        page_audits.append({"binding_sha256": binding["binding_sha256"], "offset": offset, "count": len(items), "response_sha256": digest(body)})
        if not body.get("hasMore"):
            break
        next_offset = body.get("offset", offset) + body.get("limit", len(items))
        if not isinstance(next_offset, int) or next_offset <= offset:
            raise RouteError("Lookup pagination did not advance")
        offset = next_offset
    if len(matches) != 1:
        raise RouteError(f"Lookup returned {len(matches)} exact matches; exactly one is required")
    candidate = matches[0]
    validate_candidate(route, candidate, request["as_of"])
    identity = candidate.get(request["identity_field"])
    if identity in {None, ""}:
        raise RouteError("Exact lookup match is missing its declared identity")
    return {
        "status": "resolved",
        "classification": "read_only_lov",
        "route": spec["route"],
        "identity_field": request["identity_field"],
        "identity": str(identity),
        "match_field": request["match_field"],
        "match_value": request["match_value"],
        "as_of": request["as_of"],
        "record": candidate,
        "pages": page_audits,
    }


def execute_get_response(
    binding: dict[str, Any], properties: Path, token_cache: Path
) -> tuple[dict[str, Any], dict[str, str], int]:
    props = read_properties(properties)
    require_props(props, ["environment", "restBaseUrl", "scope"])
    if props["restBaseUrl"].rstrip("/") != binding["environment"]:
        raise RouteError("Configured restBaseUrl does not match the request environment")
    token = get_access_token(props, token_cache=str(token_cache), open_browser=False)
    url = build_url(props, binding["relative_path"], binding["query"])
    content, headers, status = request_bytes(
        props, url, method="GET", access_token=token, headers=binding["headers"], json_body=None, timeout=60
    )
    if status != 200:
        raise RouteError(f"Declared read returned HTTP {status}")
    try:
        body = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RouteError("Declared read did not return JSON") from error
    if not isinstance(body, dict):
        raise RouteError("Declared read did not return a JSON object")
    return body, headers, status


def execute_get(binding: dict[str, Any], properties: Path, token_cache: Path) -> dict[str, Any]:
    body, _headers, _status = execute_get_response(binding, properties, token_cache)
    return body


def _header(headers: dict[str, str], name: str) -> str | None:
    expected = name.lower()
    for key, value in headers.items():
        if key.lower() == expected:
            return value
    return None


def run(spec: dict[str, Any], properties: Path, token_cache: Path) -> dict[str, Any]:
    command = required_string(spec, "command")
    if command == "metadata":
        binding = metadata_binding(spec)
        body = execute_get(binding, properties, token_cache)
        resources = body.get("Resources")
        if not isinstance(resources, dict) or binding["resource"] not in resources:
            raise RouteError("Metadata response does not contain the declared resource identity")
        return {
            "status": "resolved",
            "classification": binding["classification"],
            "route": binding["route"],
            "binding": binding,
            "response_sha256": digest(body),
            "metadata": body,
        }
    if command == "resolve":
        return resolve_pages(spec, lambda binding: execute_get(binding, properties, token_cache))
    if command == "list":
        return list_pages(spec, lambda binding: execute_get(binding, properties, token_cache))
    if command == "setup_preview":
        return setup_preview(spec)
    if command == "setup_read":
        binding = setup_read_binding(spec)
        body, headers, status = execute_get_response(binding, properties, token_cache)
        actual_identity = body.get(binding["identity_field"])
        if str(actual_identity) != binding["identity"]:
            raise RouteError("Setup item read returned a different identity")
        return {
            "status": "resolved",
            "classification": binding["classification"],
            "route": binding["route"],
            "binding": binding,
            "http_status": status,
            "etag": _header(headers, "ETag"),
            "response_sha256": digest(body),
            "record": body,
        }
    if command == "setup_probe":
        return probe_setup_duplicates(
            spec, lambda binding: execute_get(binding, properties, token_cache)
        )
    if command == "setup_execute":
        preview = read_object(Path(required_string(spec, "preview_path")), "setup preview")
        approval = read_object(Path(required_string(spec, "approval_path")), "setup approval")
        validate_setup_approval(preview, approval)
        binding = preview["binding"]
        props = read_properties(properties)
        require_props(props, ["environment", "restBaseUrl", "scope"])
        if props["restBaseUrl"].rstrip("/") != binding["environment"]:
            raise RouteError("Configured restBaseUrl does not match the approved setup environment")
        token = get_access_token(props, token_cache=str(token_cache), open_browser=False)
        url = build_url(props, binding["relative_path"], binding["query"])
        content, headers, status = request_bytes(
            props, url, method=binding["method"], access_token=token,
            headers=binding["headers"], json_body=preview.get("payload"), timeout=60,
        )
        try:
            response = json.loads(content.decode("utf-8")) if content else None
        except (UnicodeDecodeError, json.JSONDecodeError):
            response = content.decode("utf-8", errors="replace")
        return {
            "status": "submitted",
            "preview_sha256": preview["preview_sha256"],
            "http_status": status,
            "response": response,
            "write_retried": False,
            "verification_required": True,
        }
    raise RouteError(f"Unsupported command: {command}")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--spec", required=True, type=Path)
    result.add_argument("--properties", required=True, type=Path)
    result.add_argument("--token-cache", required=True, type=Path)
    result.add_argument("--output", required=True, type=Path)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    result: dict[str, Any]
    exit_code = 0
    try:
        spec = read_object(args.spec, "request specification")
        result = run(spec, args.properties, args.token_cache)
    except FusionHttpError as error:
        result = {
            "status": "http_error",
            "http_status": error.status_code,
            "error": "Declared Fusion request failed",
            "provider_error": sanitize_provider_error(error.body),
            "write_retried": False,
        }
        exit_code = 2
    except (RouteError, OSError, RuntimeError, ValueError) as error:
        result = {"status": "validation_error", "error": str(error), "write_retried": False}
        exit_code = 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result.get("status", "preview_ready"), "output": str(args.output)}))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
