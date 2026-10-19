#!/usr/bin/env python3
"""Compare two setup ZIP packages for a Fusion setup task."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "shared" / "baseline-assessment" / "setup-compare" / "fsm-setup-compare").exists():
            return candidate
    raise RuntimeError("Could not locate repository root with the required layout")


REPO_ROOT = find_repo_root(Path(__file__).resolve())
FUSION_SKILLS_ROOT = REPO_ROOT
FSM_COMPARE_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "shared" / "baseline-assessment" / "setup-compare" / "fsm-setup-compare" / "scripts"
AUTH_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "core" / "auth" / "fusion-oauth-authentication" / "scripts"
sys.path.insert(0, str(FSM_COMPARE_SCRIPTS_PATH))
sys.path.insert(0, str(AUTH_SCRIPTS_PATH))

from fusion_auth import (  # noqa: E402
    BoundAccessToken,
    request_context,
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    get_access_token,
    read_properties,
    require_props,
)
from fsm_setup_compare import (  # noqa: E402
    DEFAULT_ARTIFACTS,
    DEFAULT_PROPERTIES_PATH,
    CompareHttpError,
    resolve_project_id,
    run_compare as run_compare_engine,
    resource_root_from_props,
)


SKILL_ID = "shared.baseline-assessment.setup-compare.task-level-compare"
ENTITY_TYPE = "TASK"
TRIGGER = "task-level compare"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two Oracle Fusion setup task ZIP packages.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--base-url")
    parser.add_argument("--api-version", default="latest")
    parser.add_argument("--zip1", required=True)
    parser.add_argument("--zip2", required=True)
    parser.add_argument("--object-name", required=True)
    parser.add_argument("--task-name")
    parser.add_argument("--task-code")
    parser.add_argument("--output-dir")
    parser.add_argument("--project-id", help="Project workspace ID under project/{project_id}. Defaults to FDOS_PROJECT_ID or environment.")
    parser.add_argument("--source-cfg-created-by-flow", choices=["TASK", "TASK_CSV"])
    parser.add_argument("--poll-interval-seconds", type=int, default=20)
    parser.add_argument("--timeout-minutes", type=int, default=60)
    parser.add_argument("--no-poll", action="store_true")
    parser.add_argument("--skip-downloads", action="store_true")
    parser.add_argument("--include-diagnostics", action="store_true")
    parser.add_argument("--artifact", action="append", default=list(DEFAULT_ARTIFACTS))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--auth-code")
    parser.add_argument("--redirect-url")
    parser.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--force-login", action="store_true")
    parser.add_argument("--access-token")
    parser.add_argument("--open-browser", action="store_true", default=True)
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    return parser.parse_args()


def get_token(props: dict[str, str], args: argparse.Namespace, *, force_login: bool = False) -> str:
    resource_root_from_props(props, args.base_url, args.api_version)
    if args.dry_run:
        return ""
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


def resolve_scope_feature_code(args: argparse.Namespace) -> dict[str, str | None]:
    if not args.task_name and not args.task_code:
        raise ValueError("Task compare requires --task-code or --task-name.")
    return {
        "task_name": args.task_name,
        "task_code": args.task_code,
        "offering_name": None,
        "offering_code": None,
        "functional_area_name": None,
        "functional_area_code": None,
    }


def prepare_compare_args(args: argparse.Namespace, props: dict[str, str]) -> argparse.Namespace:
    args.activity_start_time = utc_now()
    resolve_project_id(args.project_id, props.get("environment"))
    args.entity_type = ENTITY_TYPE
    scope = resolve_scope_feature_code(args)
    args.task_name = scope["task_name"]
    args.task_code = scope["task_code"]
    args.offering_name = scope["offering_name"]
    args.offering_code = scope["offering_code"]
    args.functional_area_name = scope["functional_area_name"]
    args.functional_area_code = scope["functional_area_code"]
    args.no_lookup_code = False
    return args


def run_compare(args: argparse.Namespace) -> int:
    props = read_properties(Path(args.properties))
    require_props(props, ["environment", "restBaseUrl"])
    args = prepare_compare_args(args, props)
    access_token = get_token(props, args)
    try:
        return run_compare_engine(props, access_token, args, skill_id=SKILL_ID, trigger=TRIGGER)
    except CompareHttpError as exc:
        if exc.status_code not in {401, 403} or args.access_token or args.dry_run:
            raise
        print("Cached access token was rejected by Fusion. Running login flow again.", file=sys.stderr)
        access_token = get_token(props, args, force_login=True)
        return run_compare_engine(props, access_token, args, skill_id=SKILL_ID, trigger=TRIGGER)


def main() -> int:
    args = parse_args()
    try:
        return run_compare(args)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
