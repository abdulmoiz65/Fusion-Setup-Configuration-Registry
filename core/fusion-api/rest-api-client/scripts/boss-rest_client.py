#!/usr/bin/env python3
"""Invoke Oracle Fusion BOSS REST APIs with the BOSS OAuth scope."""

from __future__ import annotations

import sys

from rest_client_common import run_client


def main() -> int:
    return run_client(
        description="Invoke Oracle Fusion BOSS REST APIs with boss_scope OAuth authentication.",
        default_token_cache="auto",
        scope_property="boss_scope",
        required_path_prefix="/api/boss",
    )


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
