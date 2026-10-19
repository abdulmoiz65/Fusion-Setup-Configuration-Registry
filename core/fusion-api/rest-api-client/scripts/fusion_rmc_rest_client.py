#!/usr/bin/env python3
"""Invoke Oracle Risk and Security REST APIs with an isolated OAuth token cache."""

from __future__ import annotations

import sys

from rest_client_common import run_client


def main() -> int:
    return run_client(
        description="Invoke Oracle Risk and Security REST APIs with OAuth authentication.",
        default_token_cache="auto",
        scope_property="rmc_scope",
        rejected_path_prefix="/api/boss",
        allow_service_routes=True
    )


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
