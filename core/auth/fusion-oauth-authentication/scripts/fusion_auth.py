"""Shared Oracle Fusion REST authentication helpers.

This module centralizes the OAuth2 authorization-code flow and token caching so
Fusion REST scripts can ask for a valid access token without duplicating login
logic.
"""

from __future__ import annotations

import base64
import hashlib
import http.server
import json
import ipaddress
import re
import os
import platform
import secrets
import shutil
import stat
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path
from typing import Any, NamedTuple


DEFAULT_CALLBACK_TIMEOUT_SECONDS = 300
TOKEN_EXPIRY_SKEW_SECONDS = 60
KEYCHAIN_SERVICE = "FusionAIM OAuth Token"
CLIENT_SECRET_SERVICE = "FSCR OAuth Client Secret"
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
AUTH_HOME = Path.home().resolve() / ".fusionaim"
OAUTH_TRUST_POLICY = AUTH_HOME / "oauth-trust.json"
OAUTH_TRUST_WELCOME = (
    "FSCR needs to enroll the trusted Fusion Environment\n"
    "Please enter the Fusion URL and a name for the environment. Also provide the Oauth Client ID "
    "so that an approved environments trust file can be created"
)
OAUTH_AUTHORIZE_PATH = "/oauth2/v1/authorize"
OAUTH_TOKEN_PATH = "/oauth2/v1/token"


# Shared by the login CLI and REST clients; properties cannot add new routes.
OAUTH_SERVICE_CONFIG = {
    "standard": ("restBaseUrl", "scope", "auto"),
    "boss": ("restBaseUrl", "boss_scope", "auto"),
    "fusion-common": ("restBaseUrl", "fusion_common_scope", "auto"),
    "field-service": ("fs_restBaseUrl", "fs_scope", "auto"),
    "cdp": ("cdp_restBaseUrl", "cdp_scope", "auto"),
}


class FusionHttpError(RuntimeError):
    def __init__(self, status_code: int, url: str, body: str) -> None:
        super().__init__(f"HTTP {status_code} calling {url}: {body}")
        self.status_code = status_code
        self.url = url
        self.body = body


class UnauthorizedRestHostError(ValueError):
    """Raised before a credential can be sent to an unconfigured REST host."""


class UnauthorizedTokenEndpointError(ValueError):
    """Raised before a client secret can be sent to an untrusted OAuth endpoint."""


def _oauth_endpoint(url: str) -> tuple[tuple[str, str, int], str]:
    try:
        origin = _rest_authority(url)
        parsed = urllib.parse.urlsplit(url)
        if parsed.query or "?" in url or "%" in parsed.path or any(part in {".", ".."} for part in parsed.path.split("/")):
            raise ValueError("Non-canonical OAuth URL")
        return origin, parsed.path or "/"
    except ValueError as exc:
        raise UnauthorizedTokenEndpointError("OAuth endpoints require canonical HTTPS URLs without credentials, query, or fragment") from exc


def load_oauth_trust_policy() -> dict[str, Any]:
    """Trust comes only from the fixed, user-owned policy, never from properties."""
    try:
        value = read_private_json(OAUTH_TRUST_POLICY)
    except (OSError, ValueError) as exc:
        raise UnauthorizedTokenEndpointError("An independently enrolled ~/.fusionaim/oauth-trust.json policy is required") from exc
    if not isinstance(value, dict) or value.get("version") != 1 or not isinstance(value.get("environments"), dict):
        raise UnauthorizedTokenEndpointError("Invalid OAuth trust policy")
    return value


def authorized_token_authority(props: dict[str, str]) -> tuple[str, str, int]:
    return _token_authority_for_policy(props, load_oauth_trust_policy())


def _token_authority_for_policy(props: dict[str, str], policy: dict[str, Any]) -> tuple[str, str, int]:
    endpoints = _oauth_endpoints_for_policy(props, policy)
    return _oauth_endpoint(endpoints["tokenUrl"])[0]


def oauth_endpoints(props: dict[str, str]) -> dict[str, str]:
    """Resolve OAuth URLs exclusively from the independently enrolled policy."""
    return _oauth_endpoints_for_policy(props, load_oauth_trust_policy())


def _oauth_endpoints_for_policy(props: dict[str, str], policy: dict[str, Any]) -> dict[str, str]:
    require_props(props, ["environment", "clientId"])
    entry = policy["environments"].get(props["environment"])
    if not isinstance(entry, dict):
        raise UnauthorizedTokenEndpointError("Environment has no independently approved OAuth trust policy")
    try:
        issuer_origin, issuer_path = _oauth_endpoint(entry["issuer"])
        if issuer_path != "/":
            raise ValueError("Issuer must be the approved authority")
        endpoints = {}
        for prop, path_key in (("authorizeUrl", "authorize_path"), ("tokenUrl", "token_path")):
            path = entry[path_key]
            if not isinstance(path, str) or not path.startswith("/") or path.startswith("//"):
                raise UnauthorizedTokenEndpointError("Approved endpoint paths must start with one slash")
            endpoint = entry["issuer"].rstrip("/") + path
            origin, resolved_path = _oauth_endpoint(endpoint)
            if origin != issuer_origin or resolved_path != path:
                raise UnauthorizedTokenEndpointError("Invalid approved OAuth endpoint path")
            # Accept matching legacy settings, but never use them as destinations.
            if props.get(prop) and _oauth_endpoint(props[prop]) != (origin, resolved_path):
                raise UnauthorizedTokenEndpointError("OAuth endpoint differs from the independently approved authority or path")
            endpoints[prop] = endpoint
        if not isinstance(entry["client_ids"], list) or props["clientId"] not in entry["client_ids"]:
            raise UnauthorizedTokenEndpointError("OAuth client is not enrolled for this environment")
        if entry.get("fusion_origin") and _fusion_origin(props.get("_fusion_base_url", props.get("restBaseUrl", ""))) != entry["fusion_origin"]:
            raise UnauthorizedTokenEndpointError("Fusion URL differs from the enrolled environment")
    except (KeyError, TypeError) as exc:
        raise UnauthorizedTokenEndpointError("Incomplete OAuth trust policy") from exc
    return endpoints


def oauth_trust_entry(
    environment: str, issuer: str, client_id: str,
    authorize_path: str = OAUTH_AUTHORIZE_PATH, token_path: str = OAUTH_TOKEN_PATH,
) -> dict[str, Any]:
    """Validate independently supplied enrollment values, never configuration defaults."""
    if any(not value.strip() or any(ord(c) < 32 or ord(c) == 127 for c in value)
           for value in (environment, issuer, client_id)):
        raise UnauthorizedTokenEndpointError("Approved environment, issuer and client ID must be nonempty and contain no control characters")
    _, issuer_path = _oauth_endpoint(issuer)
    if issuer_path != "/":
        raise UnauthorizedTokenEndpointError("Approved issuer must be an HTTPS authority without a path")
    issuer = issuer.rstrip("/")
    for path in (authorize_path, token_path):
        if not path.startswith("/") or path.startswith("//"):
            raise UnauthorizedTokenEndpointError("Approved endpoint paths must start with one slash")
        _oauth_endpoint(issuer + path)
    return {"issuer": issuer, "authorize_path": authorize_path,
            "token_path": token_path, "client_ids": [client_id]}


def _fusion_origin(url: str) -> str:
    (scheme, host, port), _ = _oauth_endpoint(url)
    host = f"[{host}]" if ":" in host else host
    return f"{scheme}://{host}" + (f":{port}" if port != 443 else "")


def discover_oauth_issuer(fusion_url: str) -> str:
    """Resolve the user-supplied Fusion origin's login redirects without credentials.

    Request only the Fusion origin; an off-origin OAuth authorization redirect
    supplies the issuer but is never followed. Ignore response bodies and cookies.
    """
    origin = _fusion_origin(fusion_url)
    url = origin + "/"  # Do not pass caller-controlled deep links or queries into login.
    opener = urllib.request.build_opener(_NoRedirectHandler())
    deadline = time.monotonic() + 30
    seen: set[str] = set()
    for _ in range(8):
        if url in seen:
            raise UnauthorizedTokenEndpointError("Fusion login redirect loop; no trust policy was created")
        seen.add(url)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise UnauthorizedTokenEndpointError("Fusion issuer discovery timed out; no trust policy was created")
        request = urllib.request.Request(url, headers={"Accept": "text/html"}, method="GET")
        try:
            try:
                response = opener.open(request, timeout=min(10, remaining))
            except urllib.error.HTTPError as error:
                response = error
            with response:
                locations = response.headers.get_all("Location", [])
                if response.status not in {301, 302, 303, 307, 308} or len(locations) != 1:
                    raise UnauthorizedTokenEndpointError(
                        "Fusion did not return an unambiguous OAuth login redirect; use fusion_auth_setup.py trust --issuer for explicit enrollment"
                    )
                location = locations[0]
        except (urllib.error.URLError, OSError) as error:
            raise UnauthorizedTokenEndpointError("Cannot reach the Fusion login page over verified HTTPS; no trust policy was created") from error
        if (not location or len(location) > 16384 or "\\" in location
                or any(c.isspace() or ord(c) <= 32 or ord(c) == 127 for c in location)):
            raise UnauthorizedTokenEndpointError("Invalid Fusion login redirect")
        target = urllib.parse.urljoin(url, location)
        target_authority = _rest_authority(target)  # Reject HTTP, credentials and fragments before following.
        if target_authority != _rest_authority(origin):
            if urllib.parse.urlsplit(target).path != OAUTH_AUTHORIZE_PATH:
                raise UnauthorizedTokenEndpointError("Fusion redirected to an unsupported identity endpoint; use explicit issuer enrollment")
            parsed = urllib.parse.urlsplit(target)
            return _fusion_origin(urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "", "", "")))
        url = target
    raise UnauthorizedTokenEndpointError("Too many Fusion login redirects; no trust policy was created")


def fusion_oauth_trust_entry(environment: str, fusion_url: str, client_id: str) -> dict[str, Any]:
    """Use the supplied Fusion URL as the enrollment trust source, not OAuth properties."""
    origin = _fusion_origin(fusion_url)
    oauth_trust_entry(environment, origin, client_id)  # Validate all supplied values before network access.
    issuer = discover_oauth_issuer(fusion_url)
    return {**oauth_trust_entry(environment, issuer, client_id), "fusion_origin": origin}


def ensure_oauth_trust_policy(props: dict[str, str]) -> None:
    """Offer first-use enrollment only when the fixed policy file is absent."""
    try:
        authorized_token_authority(props)
        return
    except UnauthorizedTokenEndpointError:
        try:
            OAUTH_TRUST_POLICY.lstat()
        except FileNotFoundError:
            pass
        else:
            raise  # Existing invalid policies, including dangling symlinks, stay untouched.
    if not sys.stdin.isatty():
        raise UnauthorizedTokenEndpointError(
            OAUTH_TRUST_WELCOME + "\nRun fusion_login.py in an interactive terminal, or use "
            "fusion_auth_setup.py trust --fusion-url HTTPS_FUSION_URL --environment ENV --client-id CLIENT_ID."
        )
    print(OAUTH_TRUST_WELCOME)
    try:
        fusion_url = input("Fusion URL: ").strip()
        environment = input("Environment name: ").strip()
        client_id = input("Oauth Client ID: ").strip()
    except (EOFError, KeyboardInterrupt):
        raise UnauthorizedTokenEndpointError("OAuth trust enrollment cancelled; no policy was created") from None
    if environment != props.get("environment") or client_id != props.get("clientId"):
        raise UnauthorizedTokenEndpointError("Environment name and OAuth client ID must match the selected Fusion configuration")
    if _fusion_origin(fusion_url) != _fusion_origin(props.get("_fusion_base_url", props.get("restBaseUrl", ""))):
        raise UnauthorizedTokenEndpointError("Fusion URL must match the selected environment")
    entry = fusion_oauth_trust_entry(environment, fusion_url, client_id)
    policy = {"version": 1, "environments": {environment: entry}}
    _token_authority_for_policy(props, policy)  # Compare before writing or accessing credentials.
    write_private_json(OAUTH_TRUST_POLICY, policy, replace=False)
    authorized_token_authority(props)
    print(f"Created private OAuth trust policy in {OAUTH_TRUST_POLICY}. Continuing login.")


def require_authorized_token_url(props: dict[str, str], url: str) -> None:
    if _oauth_endpoint(url) != _oauth_endpoint(oauth_endpoints(props)["tokenUrl"]):
        raise UnauthorizedTokenEndpointError("Token redirects must remain on the exact approved endpoint")


def client_secret_account(props: dict[str, str]) -> str:
    origin = authorized_token_authority(props)
    return hashlib.sha256(json.dumps([props["environment"], origin, props["clientId"]]).encode()).hexdigest()


def load_client_secret(props: dict[str, str]) -> str:
    # Revalidate before querying the secret store; never read clientSecret from props.
    account = client_secret_account(props)
    if sys.platform == "win32":
        from windows_private_storage import load_client_secret_windows
        return load_client_secret_windows(CLIENT_SECRET_SERVICE, account)
    if sys.platform.startswith("linux"):
        from linux_private_storage import cloud_secret_configured, load_client_secret_linux, local_secret_path, validate_secret
        if cloud_secret_configured():
            return load_client_secret_linux(CLIENT_SECRET_SERVICE, account, REPOSITORY_ROOT)
        try:
            payload = read_private_json(local_secret_path(AUTH_HOME, account))
        except FileNotFoundError as exc:
            raise ValueError("No Linux confidential-client secret is enrolled; use store-client-secret or a cloud-managed mount") from exc
        if not isinstance(payload, dict) or payload.get("version") != 1 or payload.get("account") != account:
            raise ValueError("Invalid Linux confidential-client secret enrollment")
        return validate_secret(payload.get("secret"))
    if not keychain_available():
        raise ValueError("Confidential-client login requires the enrolled macOS Keychain secret; use PKCE otherwise")
    result = subprocess.run(["security", "find-generic-password", "-s", CLIENT_SECRET_SERVICE, "-a", account, "-w"], capture_output=True, text=True, check=False)
    if result.returncode or not result.stdout.strip():
        raise ValueError("No confidential-client secret is enrolled in macOS Keychain")
    return result.stdout.rstrip("\n")


def store_linux_client_secret(props: dict[str, str], secret: str) -> None:
    """Enroll an explicit local Linux secret outside the repository."""
    from linux_private_storage import cloud_secret_configured, local_secret_path, validate_secret
    if cloud_secret_configured():
        raise ValueError("Cloud secret mount is configured; use check-client-secret instead of local enrollment")
    account = client_secret_account(props)
    value = validate_secret(secret)
    path = local_secret_path(AUTH_HOME, account)
    write_private_json(path, {"version": 1, "account": account, "secret": value})
    if load_client_secret(props) != value:
        raise RuntimeError("Linux private secret storage verification failed")


def _rest_authority(url: str) -> tuple[str, str, int]:
    # urlsplit strips some controls; reject them before parsing.
    if (
        not isinstance(url, str)
        or any(c.isspace() or ord(c) <= 32 or ord(c) == 127 for c in url)
        or "\\" in url
        or "#" in url
    ):
        raise UnauthorizedRestHostError("Invalid REST URL characters")
    try:
        parsed = urllib.parse.urlsplit(url)
        port = parsed.port
        if parsed.netloc.startswith("["):
            suffix = parsed.netloc[parsed.netloc.index("]") + 1:]
            if suffix and not re.fullmatch(r":[0-9]+", suffix):
                raise ValueError("Invalid IPv6 authority")
        elif ":" in parsed.netloc and not re.fullmatch(r"[0-9]+", parsed.netloc.rsplit(":", 1)[1]):
            raise ValueError("Invalid port")
        if (parsed.scheme != "https" or not parsed.hostname
                or parsed.username is not None or parsed.password is not None
                or parsed.netloc.endswith(":") or port == 0):
            raise ValueError("Invalid HTTPS authority")
    except ValueError as exc:
        raise UnauthorizedRestHostError("REST URL must have a valid HTTPS authority without credentials") from exc
    host = parsed.hostname
    if "%" in host:
        raise UnauthorizedRestHostError("Encoded REST hostnames are not allowed")
    try:
        host = ipaddress.ip_address(host).compressed
    except ValueError:
        try:
            host = host.encode("idna").decode("ascii").lower()
        except UnicodeError as exc:
            raise UnauthorizedRestHostError("Invalid REST hostname") from exc
    return "https", host, port if port is not None else 443


class RequestContext(NamedTuple):
    origin: tuple[str, str, int]
    scope_fingerprint: str
    service: str
    path_policy: str = ""


class BoundAccessToken(str):
    """A string-compatible token carrying its acquisition context in memory."""
    def __new__(cls, value: str, context: RequestContext):
        instance = super().__new__(cls, value)
        object.__setattr__(instance, "context", context)
        return instance

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("Token context is immutable")


def request_context(
    props: dict[str, str] | RequestContext | None,
    access_token: str | None = None,
) -> RequestContext:
    """Snapshot the selected profile, or verify it against token acquisition."""
    bound = getattr(access_token, "context", None)
    if props is None:
        if bound is None:
            raise UnauthorizedRestHostError("Authenticated requests require a selected service context")
        return bound
    if isinstance(props, RequestContext):
        context = props
    else:
        base = props.get("restBaseUrl", "")
        origin = _rest_authority(base)
        if urllib.parse.urlsplit(base).query:
            raise UnauthorizedRestHostError("REST base URL must not contain a query")
        scope = " ".join(props.get("scope", "").split())
        context = RequestContext(
            origin,
            hashlib.sha256(scope.encode()).hexdigest(),
            props.get("_rest_service", "standard"),
            props.get("_rest_path_policy", ""),
        )
    if bound is not None and bound != context:
        raise UnauthorizedRestHostError("Token acquisition context does not match the selected service")
    return context


def authorized_rest_hosts(selected: dict[str, str] | RequestContext | str) -> set[tuple[str, str, int]]:
    """Return only the selected service origin; never union profile origins."""
    if isinstance(selected, str):
        selected = {"restBaseUrl": selected}
    return {request_context(selected).origin}


def require_authorized_rest_url(props: dict[str, str] | RequestContext, url: str) -> None:
    context = request_context(props)
    if _rest_authority(url) != context.origin:
        raise UnauthorizedRestHostError("Refusing credentials to a different REST origin")
    if context.path_policy == "scim":
        if context.service != "standard":
            raise UnauthorizedRestHostError("SCIM requires the standard Fusion service")
        validate_scim_endpoint(urllib.parse.urlsplit(url).path)


def validate_scim_endpoint(endpoint: str, *, collection: str | None = None) -> None:
    pattern = r"/hcmRestApi/scim/(Users|Roles)(?:/[A-Za-z0-9_-]+)?/?"
    if not isinstance(endpoint, str) or not re.fullmatch(pattern, endpoint):
        raise UnauthorizedRestHostError("SCIM requires a relative Users or Roles collection/resource path")
    if collection and endpoint.rstrip("/") != f"/hcmRestApi/scim/{collection}":
        raise UnauthorizedRestHostError("SCIM collection override does not match its declared resource")


def reject_password_fields(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if "password" in str(key).lower():
                raise ValueError("Passwords must be handled by the Fusion reset/enrollment flow")
            reject_password_fields(item)
    elif isinstance(value, list):
        for item in value:
            reject_password_fields(item)


def rest_url(props: dict[str, str] | RequestContext, endpoint: str) -> str:
    """Resolve an endpoint without silently repairing unsafe URL syntax."""
    if (
        not endpoint
        or endpoint.startswith("//")
        or any(c.isspace() or ord(c) <= 32 or ord(c) == 127 for c in endpoint)
        or "\\" in endpoint
        or "#" in endpoint
    ):
        raise UnauthorizedRestHostError("Invalid REST endpoint")
    try:
        parsed = urllib.parse.urlsplit(endpoint)
    except ValueError as exc:
        raise UnauthorizedRestHostError("Invalid REST endpoint") from exc
    if parsed.scheme or parsed.netloc:
        url = endpoint
    else:
        context = request_context(props)
        scheme, host, port = context.origin
        host = f"[{host}]" if ":" in host else host
        base = props["restBaseUrl"].rstrip("/") if isinstance(props, dict) else f"{scheme}://{host}:{port}"
        url = base + "/" + endpoint.lstrip("/")
    require_authorized_rest_url(props, url)
    return url


class _AuthorizedRestRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, props: dict[str, str] | RequestContext) -> None:
        super().__init__()
        self._context = request_context(props)

    def http_error_302(self, req: Any, fp: Any, code: int, msg: str, headers: Any) -> Any:
        # Inspect raw Location before urllib normalizes controls or joins // URLs.
        location = headers.get("location", headers.get("uri"))
        if location is not None:
            rest_url(self._context, location)
        return super().http_error_302(req, fp, code, msg, headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_308 = http_error_302

    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Any:
        require_authorized_rest_url(self._context, newurl)
        if req.get_method() not in {"GET", "HEAD"}:
            raise UnauthorizedRestHostError("Authenticated write redirects are not allowed")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Authenticated callers without configuration must not follow redirects."""

    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


class _AuthorizedTokenRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Follow token redirects only when the client-secret authority remains trusted."""

    def __init__(self, props: dict[str, str]) -> None:
        super().__init__()
        self._props = dict(props)

    def http_error_302(self, req: Any, fp: Any, code: int, msg: str, headers: Any) -> Any:
        location = headers.get("location", headers.get("uri"))
        if location is not None:
            require_authorized_token_url(self._props, urllib.parse.urljoin(req.full_url, location))
            if location.startswith("//") or any(c.isspace() or ord(c) < 32 for c in location) or "\\" in location:
                raise UnauthorizedTokenEndpointError("Invalid token redirect")
        return super().http_error_302(req, fp, code, msg, headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_308 = http_error_302

    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Any:
        require_authorized_token_url(self._props, newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def authorized_urlopen(
    props: dict[str, str] | RequestContext | None,
    request: urllib.request.Request,
    *,
    timeout: int,
    access_token: str | None = None,
    handlers: tuple = (),
) -> Any:
    """Keep initial requests, redirects and pagination on the acquisition origin."""
    context = request_context(props, access_token)
    require_authorized_rest_url(context, request.full_url)
    if any(key.lower() == "host" for key, _ in request.header_items()):
        raise UnauthorizedRestHostError("An explicit Host header cannot override the selected origin")
    opener = urllib.request.build_opener(_AuthorizedRestRedirectHandler(context), *handlers)
    return opener.open(request, timeout=timeout)


def authorized_token_urlopen(props: dict[str, str], request: urllib.request.Request, *, timeout: int) -> Any:
    """Open a token request without forwarding its client secret to an unsafe redirect."""
    require_authorized_token_url(props, request.full_url)
    opener = urllib.request.build_opener(_AuthorizedTokenRedirectHandler(props))
    return opener.open(request, timeout=timeout)


def read_properties(path: Path) -> dict[str, str]:
    props: dict[str, str] = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"Invalid properties syntax at line {line_number}")
        key, value = line.split("=", 1)
        props[key.strip()] = value.strip()
    return props


def require_props(props: dict[str, str], names: list[str]) -> None:
    missing = [name for name in names if not props.get(name)]
    if missing:
        raise ValueError(f"Missing required properties: {', '.join(missing)}")


def service_auth_properties(
    props: dict[str, str],
    *,
    base_url_property: str,
    scope_property: str,
) -> dict[str, str]:
    """Return properties configured for a service-specific REST base URL and scope.

    Shared OAuth helpers consume the canonical ``restBaseUrl`` and ``scope``
    keys. This adapter lets callers select values such as ``fs_restBaseUrl`` /
    ``fs_scope`` or ``cdp_restBaseUrl`` / ``cdp_scope`` without changing the
    standard authentication flow.
    """
    require_props(props, [base_url_property, scope_property])
    if not props[scope_property].strip():
        raise ValueError(f"Missing required OAuth scope property: {scope_property}")
    service_props = dict(props)
    service_props["_fusion_base_url"] = props.get("_fusion_base_url", props.get("restBaseUrl", ""))
    service_props["restBaseUrl"] = props[base_url_property]
    service_props["scope"] = props[scope_property]
    service_props["_rest_service"] = next(
        (name for name, (base, scope, _) in OAUTH_SERVICE_CONFIG.items()
         if (base, scope) == (base_url_property, scope_property)),
        props.get("_rest_service", "standard"),
    )
    request_context(service_props)
    return service_props


def oauth_service_properties(props: dict[str, str], service: str) -> dict[str, str]:
    """Select a supported service without falling back to another OAuth scope."""
    if service not in OAUTH_SERVICE_CONFIG:
        raise ValueError(f"Unsupported OAuth service: {service}")
    base, scope, _ = OAUTH_SERVICE_CONFIG[service]
    return service_auth_properties(props, base_url_property=base, scope_property=scope)


def http_json(
    url: str,
    *,
    method: str = "GET",
    data: dict[str, str] | None = None,
    json_body: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    rest_props: dict[str, str] | None = None,
    token_props: dict[str, str] | None = None,
    access_token: str | None = None,
) -> dict[str, Any]:
    if rest_props is not None or access_token is not None:
        require_authorized_rest_url(request_context(rest_props, access_token), url)
    body = None
    request_headers = dict(headers or {})
    if any(k.lower() == "authorization" for k in request_headers) and rest_props is None and token_props is None and access_token is None:
        raise UnauthorizedRestHostError("Authenticated requests require a selected service context")

    if data is not None and json_body is not None:
        raise ValueError("Provide either form data or json_body, not both")
    if rest_props is not None and token_props is not None:
        raise ValueError("Provide either rest_props or token_props, not both")

    if json_body is not None:
        body = json.dumps(json_body).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
    elif data is not None:
        body = urllib.parse.urlencode(data).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/x-www-form-urlencoded")

    request_headers.setdefault("Accept", "application/json")
    request = urllib.request.Request(url, data=body, headers=request_headers, method=method)

    try:
        if rest_props is not None or access_token is not None:
            opener = authorized_urlopen(rest_props, request, timeout=60, access_token=access_token)
        elif token_props is not None:
            opener = authorized_token_urlopen(token_props, request, timeout=60)
        else:
            opener = urllib.request.build_opener(_NoRedirectHandler()).open(request, timeout=60)
        with opener as response:
            response_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise FusionHttpError(exc.code, url, error_body) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed calling {url}: {exc.reason}") from exc

    try:
        parsed = json.loads(response_body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Expected JSON from {url}, got: {response_body[:500]}") from exc

    if not isinstance(parsed, dict):
        raise RuntimeError(f"Expected a JSON object from {url}")
    return parsed


def http_bytes(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    rest_props: dict[str, str] | None = None,
    access_token: str | None = None,
) -> bytes:
    if rest_props is not None or access_token is not None:
        require_authorized_rest_url(request_context(rest_props, access_token), url)
    if any(k.lower() == "authorization" for k in (headers or {})) and rest_props is None and access_token is None:
        raise UnauthorizedRestHostError("Authenticated requests require a selected service context")
    request = urllib.request.Request(url, headers=dict(headers or {}), method=method)

    try:
        opener = (
            authorized_urlopen(rest_props, request, timeout=60, access_token=access_token)
            if rest_props is not None or access_token is not None
            else urllib.request.build_opener(_NoRedirectHandler()).open(request, timeout=60)
        )
        with opener as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise FusionHttpError(exc.code, url, error_body) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed calling {url}: {exc.reason}") from exc


def is_loopback_redirect(redirect_url: str) -> bool:
    parsed = urllib.parse.urlparse(redirect_url)
    return parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1"}


def pkce_enabled(props: dict[str, str]) -> bool:
    """Return whether the configured OAuth client uses PKCE."""
    value = props.get("pkce", "true").strip().lower()
    if value not in {"true", "false"}:
        raise ValueError("Property 'pkce' must be either true or false")
    return value == "true"


def create_pkce_verifier() -> str:
    """Create an RFC 7636-compatible, per-login PKCE code verifier."""
    return secrets.token_urlsafe(64)


def pkce_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def build_authorize_url(
    props: dict[str, str],
    redirect_url: str,
    state: str,
    *,
    code_challenge: str | None = None,
) -> str:
    endpoints = oauth_endpoints(props)
    params = {
        "client_id": props["clientId"],
        "response_type": "code",
        "redirect_uri": redirect_url,
        "scope": props["scope"],
        "state": state,
    }
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    return endpoints["authorizeUrl"] + "?" + urllib.parse.urlencode(params)


def wait_for_authorization_code(
    redirect_url: str, expected_state: str, timeout_seconds: int,
    *, authorize_url: str | None = None,
) -> str:
    parsed_redirect = urllib.parse.urlparse(redirect_url)
    host = parsed_redirect.hostname
    port = parsed_redirect.port
    if not host or not port:
        raise ValueError("Local callback redirect URL must include host and port")

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            self.server.callback_received = True  # type: ignore[attr-defined]
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            self.server.authorization_code = query.get("code", [""])[0]  # type: ignore[attr-defined]
            self.server.authorization_error = query.get("error", [""])[0]  # type: ignore[attr-defined]
            self.server.callback_state = query.get("state", [""])[0]  # type: ignore[attr-defined]

            oauth_error = self.server.authorization_error  # type: ignore[attr-defined]
            if oauth_error:
                safe_error = oauth_error if re.fullmatch(r"[a-zA-Z0-9_.-]{1,80}", oauth_error) else "provider_error"
                body = f"Oracle OAuth authorization failed: {safe_error}. No access token was saved. Return to the script for next steps."
                status = 400
            elif self.server.authorization_code:  # type: ignore[attr-defined]
                body = "Authorization complete. You can close this browser tab and return to the script."
                status = 200
            else:
                body = "The callback arrived without an authorization code or OAuth error. No access token was saved. Return to the script for next steps."
                status = 400

            self.send_response(status)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))

        def log_message(self, format: str, *args: object) -> None:
            return

    server = http.server.HTTPServer((host, port), CallbackHandler)
    server.timeout = timeout_seconds
    server.authorization_code = ""  # type: ignore[attr-defined]
    server.authorization_error = ""  # type: ignore[attr-defined]
    server.callback_state = ""  # type: ignore[attr-defined]
    server.callback_received = False  # type: ignore[attr-defined]

    print(f"Waiting up to {timeout_seconds} seconds for OAuth callback at {redirect_url}")
    try:
        # An existing SSO session can redirect immediately; bind before opening.
        if authorize_url is not None:
            webbrowser.open(authorize_url)
        server.handle_request()
    finally:
        server.server_close()

    authorization_error = server.authorization_error  # type: ignore[attr-defined]
    if authorization_error:
        raise RuntimeError(f"Authorization failed: {authorization_error}")

    authorization_code = server.authorization_code  # type: ignore[attr-defined]
    if not authorization_code:
        if server.callback_received:  # type: ignore[attr-defined]
            raise RuntimeError("OAuth callback arrived without an authorization code or error")
        raise TimeoutError("Timed out waiting for authorization callback")

    callback_state = server.callback_state  # type: ignore[attr-defined]
    if callback_state != expected_state:
        raise RuntimeError("Authorization callback state did not match the expected value")

    return str(authorization_code)


def exchange_authorization_code(
    props: dict[str, str],
    authorization_code: str,
    redirect_url: str,
    *,
    code_verifier: str | None = None,
) -> dict[str, Any]:
    props = dict(props)
    token_url = oauth_endpoints(props)["tokenUrl"]
    request_data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_url,
    }
    headers: dict[str, str] | None = None
    if pkce_enabled(props):
        if not code_verifier:
            raise ValueError("A PKCE code verifier is required to exchange the authorization code")
        request_data["client_id"] = props["clientId"]
        request_data["code_verifier"] = code_verifier
    else:
        credentials = f"{props['clientId']}:{load_client_secret(props)}".encode("utf-8")
        basic_auth = base64.b64encode(credentials).decode("ascii")
        headers = {"Authorization": f"Basic {basic_auth}"}
    token_response = http_json(
        token_url,
        method="POST",
        data=request_data,
        headers=headers,
        token_props=props,
    )
    access_token = token_response.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        safe_response = {key: value for key, value in token_response.items() if "token" not in key.lower()}
        raise RuntimeError(f"Token response did not include access_token: {safe_response}")
    return token_response


def token_cache_key(props: dict[str, str]) -> str:
    """Return a stable fingerprint for the complete OAuth token-use context."""
    require_props(props, ["clientId", "restBaseUrl", "scope"])
    endpoints = oauth_endpoints(props)
    oauth_scheme, oauth_host, oauth_port = _oauth_endpoint(endpoints["tokenUrl"])[0]
    request_context(props)
    rest_url = urllib.parse.urlsplit(props["restBaseUrl"])
    rest_port = rest_url.port or 443
    context = {
        "issuer": props.get("issuer", "").strip() or f"{oauth_scheme}://{oauth_host}:{oauth_port}",
        "authorize_endpoint": endpoints["authorizeUrl"],
        "token_endpoint": endpoints["tokenUrl"],
        "client_id": props["clientId"].strip(),
        "target_service": (
            f"{rest_url.scheme}://{(rest_url.hostname or '').lower()}:{rest_port}"
            f"{rest_url.path.rstrip('/') or '/'}"
        ),
        "scope": " ".join(props["scope"].split()),
    }
    serialized_context = json.dumps(context, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized_context.encode("utf-8")).hexdigest()


def token_cache_account(props: dict[str, str]) -> str:
    environment = props.get("environment", "fusion")
    return f"{environment}:{token_cache_key(props)}"


def validate_cache_path(path: Path) -> Path:
    path = Path(os.path.abspath(path.expanduser()))
    if path.is_relative_to(REPOSITORY_ROOT) or path.resolve().is_relative_to(REPOSITORY_ROOT):
        raise ValueError("Token caches must be outside the repository; omit --token-cache for the managed cache")
    # The descriptor traversal below rejects symlinks; resolve is only an escape check.
    return path


def token_cache_path(props: dict[str, str], override_path: str | None = None) -> Path:
    if override_path is not None and str(override_path) not in {"", "auto"}:
        return validate_cache_path(Path(override_path))
    return validate_cache_path(AUTH_HOME / f"{token_cache_key(props)}_token.json")


def _private_parent(path: Path, *, create: bool) -> int:
    """Open each directory by descriptor; never traverse a symlink."""
    path = Path(os.path.abspath(path))
    fd = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parent.parts[1:]:
            if create:
                try:
                    os.mkdir(part, mode=0o700, dir_fd=fd)
                except FileExistsError:
                    pass
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        info = os.fstat(fd)
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
            raise ValueError("Private storage directory must be owned by the current user with mode 0700")
        return fd
    except BaseException:
        os.close(fd)
        raise


def read_private_json(path: Path) -> Any:
    if sys.platform == "win32":
        from windows_private_storage import read_private_json_windows
        return read_private_json_windows(path, AUTH_HOME)
    fd = _private_parent(path, create=False)
    try:
        source = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        with os.fdopen(source, "r", encoding="utf-8") as handle:
            info = os.fstat(handle.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
                raise ValueError("Private file must be a single-link, user-owned mode-0600 regular file")
            return json.load(handle)
    finally:
        os.close(fd)


def write_private_json(path: Path, value: Any, *, replace: bool = True) -> None:
    if sys.platform == "win32":
        from windows_private_storage import write_private_json_windows
        write_private_json_windows(path, value, AUTH_HOME, replace=replace)
        return
    fd = _private_parent(path, create=True)
    temporary = ".fscr-" + secrets.token_hex(16)
    try:
        try:
            info = os.stat(path.name, dir_fd=fd, follow_symlinks=False)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.getuid():
                raise ValueError("Refusing an unsafe private-file destination")
        except FileNotFoundError:
            pass
        target = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=fd)
        with os.fdopen(target, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        if replace:
            os.replace(temporary, path.name, src_dir_fd=fd, dst_dir_fd=fd)
        else:
            # Publish complete JSON atomically without overwriting a concurrent enrollment.
            os.link(temporary, path.name, src_dir_fd=fd, dst_dir_fd=fd, follow_symlinks=False)
            os.unlink(temporary, dir_fd=fd)
        os.fsync(fd)
    finally:
        try:
            os.unlink(temporary, dir_fd=fd)
        except FileNotFoundError:
            pass
        os.close(fd)


def token_cache_payload(props: dict[str, str], token_response: dict[str, Any]) -> dict[str, Any]:
    now = int(time.time())
    expires_in = token_response.get("expires_in")
    if not isinstance(expires_in, int):
        expires_in = int(expires_in) if str(expires_in).isdigit() else 3600

    cache_data = {
        "cache_format_version": 2,
        "cache_profile": token_cache_key(props),
        "access_token": token_response["access_token"],
        "token_type": token_response.get("token_type", "Bearer"),
        "expires_at": now + expires_in,
        "saved_at": now,
    }
    if token_response.get("scope"):
        cache_data["scope"] = token_response["scope"]
    return cache_data


def save_file_token_cache(path: Path, props: dict[str, str], token_response: dict[str, Any]) -> None:
    path = validate_cache_path(path)
    write_private_json(path, token_cache_payload(props, token_response))


def cached_access_token(cache_data: Any, props: dict[str, str]) -> str | None:
    """Return a valid token only when its stored profile matches the caller."""
    if not isinstance(cache_data, dict):
        return None
    if cache_data.get("cache_format_version") != 2:
        return None
    if not secrets.compare_digest(str(cache_data.get("cache_profile", "")), token_cache_key(props)):
        return None

    access_token = cache_data.get("access_token")
    expires_at = cache_data.get("expires_at", 0)
    if not isinstance(access_token, str) or not access_token:
        return None
    try:
        expired = int(expires_at) <= int(time.time()) + TOKEN_EXPIRY_SKEW_SECONDS
    except (TypeError, ValueError):
        return None
    return None if expired else access_token


def load_file_cached_access_token(path: Path, props: dict[str, str]) -> str | None:
    path = validate_cache_path(path)
    try:
        cache_data = read_private_json(path)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None
    return cached_access_token(cache_data, props)


def keychain_available() -> bool:
    return platform.system() == "Darwin" and shutil.which("security") is not None


def save_keychain_token_cache(props: dict[str, str], token_response: dict[str, Any]) -> bool:
    if not keychain_available():
        return False

    payload = json.dumps(token_cache_payload(props, token_response))
    result = subprocess.run(
        [
            "security",
            "add-generic-password",
            "-U",
            "-s",
            KEYCHAIN_SERVICE,
            "-a",
            token_cache_account(props),
            "-w",
            payload,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def load_keychain_access_token(props: dict[str, str]) -> str | None:
    if not keychain_available():
        return None

    result = subprocess.run(
        [
            "security",
            "find-generic-password",
            "-s",
            KEYCHAIN_SERVICE,
            "-a",
            token_cache_account(props),
            "-w",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None

    try:
        cache_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None

    return cached_access_token(cache_data, props)


def load_cached_access_token(props: dict[str, str], file_cache_path: Path | None = None) -> str | None:
    if file_cache_path is not None:
        return load_file_cached_access_token(file_cache_path, props)
    return load_keychain_access_token(props) or load_file_cached_access_token(token_cache_path(props), props)


def save_token_cache(props: dict[str, str], token_response: dict[str, Any], file_cache_path: Path | None = None) -> str:
    if file_cache_path is not None:
        save_file_token_cache(file_cache_path, props, token_response)
        return str(file_cache_path)

    if save_keychain_token_cache(props, token_response):
        return "macOS Keychain"

    fallback_path = token_cache_path(props)
    save_file_token_cache(fallback_path, props, token_response)
    return str(fallback_path)


def login_for_access_token(
    props: dict[str, str],
    *,
    redirect_url: str,
    auth_code: str | None = None,
    code_verifier: str | None = None,
    open_browser: bool = True,
    callback_timeout: int = DEFAULT_CALLBACK_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    ensure_oauth_trust_policy(props)
    authorization_code = auth_code
    selected_code_verifier = code_verifier
    if not authorization_code:
        state = secrets.token_urlsafe(24)
        if pkce_enabled(props):
            selected_code_verifier = create_pkce_verifier()
        authorize_url = build_authorize_url(
            props,
            redirect_url,
            state,
            code_challenge=pkce_code_challenge(selected_code_verifier) if selected_code_verifier else None,
        )
        print("Opening Oracle Identity Cloud login in your browser.")
        print(authorize_url)
        print()
        if is_loopback_redirect(redirect_url):
            authorization_code = wait_for_authorization_code(
                redirect_url, state, callback_timeout,
                authorize_url=authorize_url if open_browser else None,
            )
        else:
            if open_browser:
                webbrowser.open(authorize_url)
            print(
                "The configured redirect URL is not localhost, so the script cannot capture the code "
                "automatically. After redirect, paste the value of the 'code' query parameter."
            )
            authorization_code = input("Authorization code: ").strip()
    return exchange_authorization_code(
        props,
        authorization_code,
        redirect_url,
        code_verifier=selected_code_verifier,
    )


def get_access_token(
    props: dict[str, str],
    *,
    redirect_url: str | None = None,
    auth_code: str | None = None,
    code_verifier: str | None = None,
    open_browser: bool = True,
    callback_timeout: int = DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    token_cache: str | None = None,
    force_login: bool = False,
) -> str:
    props = dict(props)
    ensure_oauth_trust_policy(props)
    context = request_context(props)
    require_props(props, ["restBaseUrl"])
    required_properties = [
        "environment",
        "restBaseUrl",
        "clientId",
        "scope",
        "redirectUrl",
    ]
    require_props(props, required_properties)
    if pkce_enabled(props) and auth_code and not code_verifier:
        raise ValueError("PKCE login with --auth-code also requires --code-verifier")
    file_cache_path = token_cache_path(props, token_cache)

    if not force_login:
        cached_access_token = load_cached_access_token(props, file_cache_path)
        if cached_access_token:
            return BoundAccessToken(cached_access_token, context)

    selected_redirect_url = redirect_url or props["redirectUrl"]
    token_response = login_for_access_token(
        props,
        redirect_url=selected_redirect_url,
        auth_code=auth_code,
        code_verifier=code_verifier,
        open_browser=open_browser,
        callback_timeout=callback_timeout,
    )
    cache_location = save_token_cache(props, token_response, file_cache_path)
    print(f"Saved access token cache in {cache_location}")
    return BoundAccessToken(str(token_response["access_token"]), context)


def fusion_rest_json(
    props: dict[str, str],
    resource_path: str,
    *,
    access_token: str,
    query_params: dict[str, str],
) -> dict[str, Any]:
    base_url = props["restBaseUrl"].rstrip("/")
    query_string = urllib.parse.urlencode(query_params)
    url = f"{base_url}{resource_path}?{query_string}"
    return http_json(url, headers={"Authorization": f"Bearer {access_token}"}, rest_props=props, access_token=access_token)


def fusion_rest_post_json(
    props: dict[str, str],
    resource_path: str,
    *,
    access_token: str,
    json_body: dict[str, Any],
) -> dict[str, Any]:
    base_url = props["restBaseUrl"].rstrip("/")
    url = f"{base_url}{resource_path}"
    return http_json(
        url,
        method="POST",
        json_body=json_body,
        headers={"Authorization": f"Bearer {access_token}"},
        rest_props=props,
        access_token=access_token,
    )


def fusion_rest_get_bytes(
    props: dict[str, str],
    resource_path: str,
    *,
    access_token: str,
) -> bytes:
    base_url = props["restBaseUrl"].rstrip("/")
    url = f"{base_url}{resource_path}"
    return http_bytes(url, headers={"Authorization": f"Bearer {access_token}"}, rest_props=props, access_token=access_token)
