#!/usr/bin/env python3
"""Run Oracle Fusion OAuth login and persist a reusable access token cache."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from fusion_auth import (
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    OAUTH_SERVICE_CONFIG,
    get_access_token,
    oauth_service_properties,
    read_properties,
)


DEFAULT_PROPERTIES_PATH = Path(__file__).resolve().parents[2] / "fusionEnv.properties"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Login to Oracle Fusion and save an access token cache.")
    parser.add_argument(
        "--service", choices=tuple(OAUTH_SERVICE_CONFIG), default="standard",
        help="Select the configured OAuth scope and its separate token cache.",
    )
    parser.add_argument(
        "--properties",
        default=str(DEFAULT_PROPERTIES_PATH),
        help="Path to the Fusion environment properties file.",
    )
    parser.add_argument(
        "--auth-code",
        help="OAuth2 authorization code. If omitted, the browser login flow is started.",
    )
    parser.add_argument(
        "--code-verifier",
        help="PKCE code verifier for a supplied --auth-code. This value is not stored.",
    )
    parser.add_argument(
        "--redirect-url",
        help=(
            "OAuth2 redirect URI to use. Defaults to redirectUrl from the Fusion environment properties file. "
            "Use a registered localhost URL such as http://127.0.0.1:8765/oauth/callback "
            "to let the script capture the code automatically."
        ),
    )
    parser.add_argument(
        "--callback-timeout",
        type=int,
        default=DEFAULT_CALLBACK_TIMEOUT_SECONDS,
        help="Seconds to wait for a localhost OAuth callback.",
    )
    parser.add_argument(
        "--token-cache",
        help=(
            "External private cache override; defaults to ~/.fusionaim/<profile-fingerprint>_token.json."
        ),
    )
    parser.add_argument(
        "--open-browser",
        action="store_true",
        default=True,
        help="Open the OAuth2 authorization URL in the default browser. This is enabled by default.",
    )
    parser.add_argument(
        "--no-open-browser",
        action="store_false",
        dest="open_browser",
        help="Print the authorization URL without opening a browser.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    props = oauth_service_properties(read_properties(Path(args.properties)), args.service)
    token_cache = args.token_cache
    if token_cache is None and args.service != "standard":
        token_cache = OAUTH_SERVICE_CONFIG[args.service][2]
    get_access_token(
        props,
        redirect_url=args.redirect_url,
        auth_code=args.auth_code,
        code_verifier=args.code_verifier,
        open_browser=args.open_browser,
        callback_timeout=args.callback_timeout,
        token_cache=token_cache,
        force_login=True,
    )
    print(f"Login complete for {args.service}.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
