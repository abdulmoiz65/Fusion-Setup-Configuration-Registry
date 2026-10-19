#!/usr/bin/env python3
"""Validate a CRM describe probe and delegate it to the core REST client.

This task-local wrapper owns only the Service Mapping probe boundaries. OAuth,
HTTP execution, token refresh, and response handling remain in the core client.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from urllib.parse import ParseResult, urlparse

REPOSITORY_ROOT = Path(__file__).resolve().parents[6]
CORE_REST_CLIENT = REPOSITORY_ROOT / "core/fusion-api/rest-api-client/scripts/fusion_rest_client.py"
DEFAULT_PROPERTIES_PATH = REPOSITORY_ROOT / "core/auth/fusionEnv.properties"
DEFAULT_CALLBACK_TIMEOUT_SECONDS = 300


def configured_rest_base_url(properties_path: str) -> str:
    """Read the configured Fusion REST base URL with the core parser."""
    core_scripts_path = str(CORE_REST_CLIENT.parent)
    if core_scripts_path not in sys.path:
        sys.path.insert(0, core_scripts_path)
    from rest_client_common import read_properties, require_props

    properties = read_properties(Path(properties_path))
    require_props(properties, ["restBaseUrl"])
    return properties["restBaseUrl"]


def normalized_origin(parsed: ParseResult) -> tuple[str, str, int]:
    """Return a case-normalized URL origin with its effective port."""
    scheme = parsed.scheme.lower()
    if scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Absolute endpoint must use an HTTP(S) URL with a host")
    try:
        port = parsed.port
    except ValueError as exc:
        raise ValueError("Absolute endpoint contains an invalid port") from exc
    return scheme, parsed.hostname.lower(), port or (443 if scheme == "https" else 80)


def validate_absolute_endpoint_authority(endpoint: str, properties_path: str) -> None:
    """Require absolute endpoints to use the configured Fusion URL authority."""
    parsed_endpoint = urlparse(endpoint)
    if parsed_endpoint.username is not None or parsed_endpoint.password is not None:
        raise ValueError("Absolute endpoint must not contain user information")
    if parsed_endpoint.fragment:
        raise ValueError("Absolute endpoint must not contain a URL fragment")

    parsed_base = urlparse(configured_rest_base_url(properties_path))
    if normalized_origin(parsed_endpoint) != normalized_origin(parsed_base):
        raise ValueError("Absolute endpoint must match the configured Fusion REST scheme and authority")


def endpoint_path(endpoint: str) -> str:
    """Return the path component used for task-specific endpoint validation."""
    if endpoint.startswith(("http://", "https://")):
        return urlparse(endpoint).path
    return endpoint if endpoint.startswith("/") else f"/{endpoint}"


def build_core_command(args: argparse.Namespace) -> list[str]:
    """Build the core-client invocation after all local policy checks pass."""
    if args.endpoint.startswith(("http://", "https://")):
        validate_absolute_endpoint_authority(args.endpoint, args.properties)
    path = endpoint_path(args.endpoint)
    if not path.startswith("/crmRestApi/"):
        raise ValueError("This read-only probe supports only /crmRestApi endpoints")
    if not path.rstrip("/").endswith("/describe"):
        raise ValueError("This metadata probe supports only CRM REST /describe endpoints")

    output = Path(args.output)
    if output.resolve().is_relative_to(REPOSITORY_ROOT):
        raise ValueError("Write raw responses outside the repository workspace")

    command = [
        sys.executable,
        str(CORE_REST_CLIENT),
        args.endpoint,
        "--method",
        "GET",
        "--properties",
        args.properties,
        "--output",
        str(output),
        "--timeout",
        str(args.timeout),
        "--token-cache",
        args.token_cache,
        "--callback-timeout",
        str(args.callback_timeout),
    ]
    if args.force_login:
        command.append("--force-login")
    command.append("--open-browser" if args.open_browser else "--no-open-browser")
    return command


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a read-only Fusion REST describe probe through the core client.")
    parser.add_argument("endpoint", help="CRM REST endpoint path or absolute URL.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--output", required=True, help="Response output path outside the project workspace.")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--force-login", action="store_true")
    parser.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    parser.add_argument("--open-browser", action="store_true", default=True)
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    args = parser.parse_args()
    args.access_token = None
    args.redirect_url = None
    args.auth_code = None

    result = subprocess.run(build_core_command(args), check=False)
    return result.returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
