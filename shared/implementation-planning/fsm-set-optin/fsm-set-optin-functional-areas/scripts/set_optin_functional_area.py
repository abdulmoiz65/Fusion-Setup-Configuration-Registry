#!/usr/bin/env python3
"""Set Oracle Fusion FSM Redwood opt-in status for a functional area."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "shared" / "implementation-planning" / "fsm-set-optin" / "fsm-set-optin").exists():
            return candidate
    raise RuntimeError("Could not locate repository root with the required layout")


REPO_ROOT = find_repo_root(Path(__file__).resolve())
FUSION_SKILLS_ROOT = REPO_ROOT
SET_OPTIN_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "shared" / "implementation-planning" / "fsm-set-optin" / "fsm-set-optin" / "scripts"
sys.path.insert(0, str(SET_OPTIN_SCRIPTS_PATH))

from fsm_set_optin import (  # noqa: E402
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    DEFAULT_PAGE_SIZE,
    DEFAULT_PROPERTIES_PATH,
    read_properties,
    require_props,
    resolve_project_id,
    run_set_optin as run_set_optin_engine,
)


SKILL_ID = "shared.implementation-planning.fsm-set-optin.fsm-set-optin-functional-areas"
TARGET_TYPE = "functional-area"
TRIGGER = "fsm set optin functional areas"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set FSM Redwood opt-in status for a functional area.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--base-url")
    parser.add_argument("--api-version", default="latest")
    parser.add_argument("--functional-area-name")
    parser.add_argument("--functional-area-code")
    parser.add_argument("--offering-name")
    parser.add_argument("--offering-code")
    parser.add_argument("--offering-id")
    parser.add_argument("--action", required=True, help="opt-in/enable, opt-out/disable, or set-choices.")
    parser.add_argument("--feature-choices")
    parser.add_argument("--output-dir")
    parser.add_argument("--project-id", help="Project workspace ID under project/{project_id}. Defaults to FDOS_PROJECT_ID or environment.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE)
    parser.add_argument("--auth-code")
    parser.add_argument("--redirect-url")
    parser.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--boss-token-cache", default="auto")
    parser.add_argument("--fusion-common-token-cache", default="auto")
    parser.add_argument("--force-login", action="store_true")
    parser.add_argument("--access-token")
    parser.add_argument("--boss-access-token")
    parser.add_argument("--fusion-common-access-token")
    parser.add_argument("--open-browser", action="store_true", default=True)
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    return parser.parse_args()


def resolve_scope_feature_code(args: argparse.Namespace) -> tuple[str, str | None]:
    target = args.functional_area_code or args.functional_area_name
    if not target:
        raise ValueError("Functional-area set opt-in requires --functional-area-code or --functional-area-name.")
    offering = args.offering_code or args.offering_name
    return target, offering


def prepare_set_optin_args(args: argparse.Namespace, props: dict[str, str]) -> argparse.Namespace:
    args.activity_start_time = utc_now()
    resolve_project_id(args.project_id, props.get("environment"))
    args.target_type = TARGET_TYPE
    args.target, args.offering = resolve_scope_feature_code(args)
    return args


def run_set_optin(args: argparse.Namespace) -> int:
    props = read_properties(Path(args.properties))
    require_props(props, ["environment", "restBaseUrl"])
    args = prepare_set_optin_args(args, props)
    return run_set_optin_engine(props, args, skill_id=SKILL_ID, trigger=TRIGGER)


def main() -> int:
    args = parse_args()
    try:
        return run_set_optin(args)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
