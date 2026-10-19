"""Shared command-line machinery for Oracle Fusion REST clients."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


CORE_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROPERTIES_PATH = CORE_ROOT / "auth" / "fusionEnv.properties"
AUTH_SCRIPTS_PATH = CORE_ROOT / "auth" / "fusion-oauth-authentication" / "scripts"
sys.path.insert(0, str(AUTH_SCRIPTS_PATH))

from fusion_auth import (  # noqa: E402
    BoundAccessToken,
    request_context,
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    OAUTH_SERVICE_CONFIG,
    FusionHttpError,
    authorized_urlopen,
    rest_url,
    get_access_token,
    read_properties,
    require_props,
    service_auth_properties,
    validate_scim_endpoint,
    reject_password_fields,
)


SUPPORTED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}


def parse_key_value(value: str, *, separator_hint: str) -> tuple[str, str]:
    if "=" in value:
        key, parsed_value = value.split("=", 1)
    elif ":" in value:
        key, parsed_value = value.split(":", 1)
    else:
        raise ValueError(f"Expected {separator_hint}: {value}")
    key = key.strip()
    if not key:
        raise ValueError(f"Missing key in {value}")
    return key, parsed_value.strip()


def parse_repeated_key_values(values: list[str] | None, *, separator_hint: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values or []:
        key, parsed_value = parse_key_value(value, separator_hint=separator_hint)
        parsed[key] = parsed_value
    return parsed


def load_json_body(args: argparse.Namespace) -> Any | None:
    if args.body and args.body_file:
        raise ValueError("Provide either --body or --body-file, not both")
    if args.body_file:
        return json.loads(Path(args.body_file).read_text(encoding="utf-8"))
    if args.body:
        return json.loads(args.body)
    return None


def endpoint_path(endpoint: str) -> str:
    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        return urllib.parse.urlparse(endpoint).path
    return endpoint if endpoint.startswith("/") else f"/{endpoint}"


def build_url(props: dict[str, str], endpoint: str, query_params: dict[str, str]) -> str:
    url = rest_url(props, endpoint)

    if not query_params:
        return _authorized_url(props, url)

    separator = "&" if urllib.parse.urlparse(url).query else "?"
    return _authorized_url(props, f"{url}{separator}{urllib.parse.urlencode(query_params)}")


def _authorized_url(props: dict[str, str], url: str) -> str:
    # Import locally to keep the URL policy next to all user-supplied endpoint handling.
    from fusion_auth import require_authorized_rest_url

    require_authorized_rest_url(props, url)
    return url


def service_configuration(service: str) -> tuple[str, str, str] | None:
    """Return service-specific base URL, OAuth scope, and default cache settings."""
    if service in {"fusion-common", "field-service", "cdp"}:
        return OAUTH_SERVICE_CONFIG[service]
    return None


def props_with_scope_property(props: dict[str, str], scope_property: str) -> dict[str, str]:
    if not props.get(scope_property, "").strip():
        raise ValueError(f"Missing required OAuth scope property: {scope_property}")
    if scope_property != "scope":
        return service_auth_properties(
            props, base_url_property="restBaseUrl", scope_property=scope_property,
        )
    scoped_props = dict(props)
    scoped_props["scope"] = props[scope_property]
    return scoped_props


def request_bytes(
    props: dict[str, str],
    url: str,
    *,
    method: str,
    access_token: str,
    headers: dict[str, str],
    json_body: Any | None,
    timeout: int,
) -> tuple[bytes, dict[str, str], int]:
    if props.get("_rest_path_policy") == "scim":
        _authorized_url(props, url)
        reject_password_fields(json_body)
    request_headers = dict(headers)
    request_headers["Authorization"] = f"Bearer {access_token}"
    request_headers.setdefault("Accept", "application/json")

    body = None
    if json_body is not None:
        body = json.dumps(json_body).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")

    request = urllib.request.Request(url, data=body, headers=request_headers, method=method)

    try:
        with authorized_urlopen(props, request, timeout=timeout, access_token=access_token) as response:
            return response.read(), dict(response.headers.items()), response.status
    except urllib.error.HTTPError as exc:
        error_body = "SCIM request failed; response suppressed" if props.get("_rest_path_policy") == "scim" else exc.read().decode("utf-8", errors="replace")
        raise FusionHttpError(exc.code, url, error_body) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed calling {url}: {exc.reason}") from exc


def render_response(content: bytes, headers: dict[str, str], *, pretty: bool) -> str:
    text = content.decode("utf-8", errors="replace")
    content_type = headers.get("Content-Type", headers.get("content-type", ""))
    if pretty and ("json" in content_type.lower() or text.lstrip().startswith(("{", "["))):
        try:
            return json.dumps(json.loads(text), indent=2) + "\n"
        except json.JSONDecodeError:
            return text
    return text


def write_or_print(content: bytes, headers: dict[str, str], args: argparse.Namespace) -> None:
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(content)
        print(f"Wrote {output_path} ({len(content)} bytes)")
        return

    rendered = render_response(content, headers, pretty=not args.raw)
    print(rendered, end="" if rendered.endswith("\n") else "\n")


def build_parser(*, description: str, default_token_cache: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("endpoint", help="Fusion REST resource path or absolute URL.")
    parser.add_argument("--scim-only", action="store_true", help="Restrict provisioning to standard Fusion SCIM Users/Roles paths.")
    parser.add_argument(
        "--service",
        choices=("standard", "fusion-common", "field-service", "cdp"),
        default="standard",
        help="Target service selected by the calling skill. Defaults to standard Fusion REST.",
    )
    parser.add_argument("--method", default="GET", choices=sorted(SUPPORTED_METHODS))
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument(
        "--query",
        action="append",
        help="Query parameter as key=value. May be supplied more than once.",
    )
    parser.add_argument(
        "--header",
        action="append",
        help="Additional header as Name=value or Name: value. May be supplied more than once.",
    )
    parser.add_argument("--body", help="JSON request body as a string.")
    parser.add_argument("--body-file", help="Path to a JSON request body file.")
    parser.add_argument("--output", help="Write response bytes to this file instead of printing.")
    parser.add_argument("--raw", action="store_true", help="Print response text without JSON pretty formatting.")
    parser.add_argument("--timeout", type=int, default=60, help="HTTP request timeout in seconds.")
    parser.add_argument("--auth-code", help="OAuth2 authorization code. Used only when login is required.")
    parser.add_argument("--redirect-url", help="OAuth2 redirect URI to use when login is required.")
    parser.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    parser.add_argument(
        "--token-cache",
        default=default_token_cache,
        help=f"Path to a file token cache. Defaults to {default_token_cache}.",
    )
    parser.add_argument("--force-login", action="store_true", help="Ignore cached token and run OAuth login.")
    parser.add_argument("--access-token", help="Existing OAuth2 bearer token. Skips token cache and login.")
    parser.add_argument("--open-browser", action="store_true", default=True)
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    return parser


def get_token(props: dict[str, str], args: argparse.Namespace, *, force_login: bool = False) -> str:
    if args.access_token:
        return BoundAccessToken(str(args.access_token), request_context(props))
    return get_access_token(
        props,
        redirect_url=args.redirect_url,
        auth_code=args.auth_code,
        open_browser=args.open_browser,
        callback_timeout=args.callback_timeout,
        token_cache=args.token_cache,
        force_login=args.force_login or force_login,
    )


def run_client(
    *,
    description: str,
    default_token_cache: str,
    scope_property: str,
    required_path_prefix: str | None = None,
    rejected_path_prefix: str | None = None,
    allow_service_routes: bool = False,
) -> int:
    parser = build_parser(description=description, default_token_cache=default_token_cache)
    args = parser.parse_args()
    props = read_properties(Path(args.properties))
    require_props(props, ["environment"])

    path = endpoint_path(args.endpoint)
    if args.scim_only:
        if args.service != "standard":
            raise ValueError("SCIM provisioning requires the standard Fusion service")
        validate_scim_endpoint(args.endpoint)
        props = {**props, "_rest_service": "standard", "_rest_path_policy": "scim"}
    common_path = path == "/api/fusion-common" or path.startswith("/api/fusion-common/")
    if common_path and args.service != "fusion-common":
        raise ValueError("Fusion Common endpoints require --service fusion-common and fusion_common_scope")
    if args.service == "fusion-common" and not common_path:
        raise ValueError("The fusion-common service only supports /api/fusion-common endpoints")
    if required_path_prefix and not path.startswith(required_path_prefix):
        raise ValueError(f"This client only supports endpoints under {required_path_prefix}")
    if rejected_path_prefix and path.startswith(rejected_path_prefix):
        raise ValueError(f"Use boss-rest_client.py for endpoints under {rejected_path_prefix}")
    if args.service != "standard" and not allow_service_routes:
        raise ValueError("This client only supports the standard Fusion REST service")

    query_params = parse_repeated_key_values(args.query, separator_hint="query key=value")
    headers = parse_repeated_key_values(args.header, separator_hint="header Name=value or Name: value")
    json_body = load_json_body(args)
    if args.scim_only:
        reject_password_fields(json_body)
    service = service_configuration(args.service)
    if service:
        base_url_property, service_scope_property, service_token_cache = service
        client_props = service_auth_properties(
            props,
            base_url_property=base_url_property,
            scope_property=service_scope_property,
        )
        if args.token_cache == default_token_cache:
            args.token_cache = service_token_cache
    else:
        require_props(props, ["restBaseUrl"])
        client_props = props
    url = build_url(client_props, args.endpoint, query_params)
    auth_props = props_with_scope_property(client_props, scope_property)
    access_token = get_token(auth_props, args)

    try:
        content, response_headers, status = request_bytes(
            auth_props,
            url,
            method=args.method,
            access_token=access_token,
            headers=headers,
            json_body=json_body,
            timeout=args.timeout,
        )
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403} or args.access_token or args.method not in {"GET", "HEAD"}:
            raise
        print("Cached access token was rejected by Fusion. Running login flow again.", file=sys.stderr)
        access_token = get_token(auth_props, args, force_login=True)
        content, response_headers, status = request_bytes(
            auth_props,
            url,
            method=args.method,
            access_token=access_token,
            headers=headers,
            json_body=json_body,
            timeout=args.timeout,
        )

    if args.output:
        print(f"HTTP {status}")
    if args.scim_only:
        reject_password_fields(json.loads(content))
    write_or_print(content, response_headers, args)
    return 0
