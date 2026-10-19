#!/usr/bin/env python3
"""Compare two Oracle Fusion setup ZIP packages using FSCR OAuth."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_ID = "shared.baseline-assessment.setup-compare.fsm-setup-compare"


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "core" / "auth" / "fusion-oauth-authentication").exists():
            return candidate
    raise RuntimeError("Could not locate repository root with the required layout")


REPO_ROOT = find_repo_root(Path(__file__).resolve())
FUSION_SKILLS_ROOT = REPO_ROOT
AUTH_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "core" / "auth" / "fusion-oauth-authentication" / "scripts"
PROJECT_MGMT_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "core" / "project-mgmt" / "scripts"
DEFAULT_PROPERTIES_PATH = FUSION_SKILLS_ROOT / "core" / "auth" / "fusionEnv.properties"
PROJECTS_ROOT = FUSION_SKILLS_ROOT / "project"


def add_to_path(path: Path) -> None:
    path_string = str(path)
    if path_string not in sys.path:
        sys.path.insert(0, path_string)


def project_artifacts_root(project_id: str) -> Path:
    return PROJECTS_ROOT / project_id / "artifacts"


def resolve_project_id(explicit_project_id: str | None = None, default_project_id: str | None = None) -> str:
    if explicit_project_id:
        return explicit_project_id
    env_project_id = os.environ.get("FDOS_PROJECT_ID")
    if env_project_id:
        return env_project_id
    if default_project_id:
        return default_project_id

    candidates = [
        path.parent.parent.name
        for path in PROJECTS_ROOT.glob("*/state/project-state.json")
        if path.parent.parent.name != "_template"
    ]
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise RuntimeError("No project workspace found under project/{project_id}. Pass --project-id.")
    raise RuntimeError(
        "Multiple project workspaces found under project/{project_id}. Pass --project-id or set FDOS_PROJECT_ID."
    )


add_to_path(AUTH_SCRIPTS_PATH)
add_to_path(PROJECT_MGMT_SCRIPTS_PATH)

from fusion_auth import BoundAccessToken, request_context, DEFAULT_CALLBACK_TIMEOUT_SECONDS, get_access_token, read_properties, require_props
from fsm_setup_compare_engine import (
    DEFAULT_ARTIFACTS,
    CompareError,
    CompareHttpError,
    resource_root_from_props,
    run_compare as run_compare_engine,
    resource_root_from_props,
    slug,
)
from token_usage_logger import append_token_usage_log


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_output_dir(project_id: str, entity_type: str, object_name: str) -> Path:
    return (
        project_artifacts_root(project_id)
        / "shared"
        / "baseline-assessment"
        / "setup-compare"
        / slug(entity_type.replace("_", "-"))
        / slug(object_name)
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two Oracle Fusion FSM setup ZIP packages.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--base-url", help="Fusion host, UI URL, or /fscmRestApi/resources root. Defaults to restBaseUrl.")
    parser.add_argument("--api-version", default="latest")
    parser.add_argument("--zip1", required=True)
    parser.add_argument("--zip2", required=True)
    parser.add_argument("--object-name", required=True)
    parser.add_argument("--entity-type", choices=["TASK", "OFFERING", "FUNCTIONAL_AREA"], default="TASK")
    parser.add_argument("--task-name")
    parser.add_argument("--task-code")
    parser.add_argument("--offering-name")
    parser.add_argument("--offering-code")
    parser.add_argument("--functional-area-name")
    parser.add_argument("--functional-area-code")
    parser.add_argument("--no-lookup-code", action="store_true")
    parser.add_argument(
        "--source-cfg-created-by-flow",
        choices=["OFFERING_EXPORT_IMPORT", "OFFERING_EXPORT_IMPORT_CSV", "TASK", "TASK_CSV"],
    )
    parser.add_argument("--output-dir")
    parser.add_argument("--project-id", help="Project workspace ID under project/{project_id}. Defaults to FDOS_PROJECT_ID or environment.")
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
    if args.entity_type == "TASK" and not args.task_name and not args.task_code:
        raise ValueError("Task compare requires --task-code or --task-name.")
    if args.entity_type == "OFFERING" and not args.offering_name and not args.offering_code:
        raise ValueError("Offering compare requires --offering-code or --offering-name.")
    if args.entity_type == "FUNCTIONAL_AREA":
        missing = []
        if not args.offering_name and not args.offering_code:
            missing.append("--offering-code or --offering-name")
        if not args.functional_area_name and not args.functional_area_code:
            missing.append("--functional-area-code or --functional-area-name")
        if missing:
            raise ValueError("Functional-area compare requires " + " and ".join(missing) + ".")

    return {
        "task_name": args.task_name,
        "task_code": args.task_code,
        "offering_name": args.offering_name,
        "offering_code": args.offering_code,
        "functional_area_name": args.functional_area_name,
        "functional_area_code": args.functional_area_code,
    }


def artifact_paths_from_summary(summary: dict[str, object]) -> list[Path]:
    artifact_paths = [
        Path(str(path))
        for path in (summary.get("processOutputPath"), summary.get("standardReportPath"))
        if path
    ]
    artifacts = summary.get("artifacts", [])
    if isinstance(artifacts, list):
        artifact_paths.extend(
            Path(str(artifact["path"]))
            for artifact in artifacts
            if isinstance(artifact, dict) and artifact.get("path")
        )
    return artifact_paths


def run_compare(
    props: dict[str, str],
    access_token: str,
    args: argparse.Namespace,
    *,
    skill_id: str = SKILL_ID,
    trigger: str = "setup compare",
) -> int:
    root = resource_root_from_props(props, args.base_url, args.api_version)
    project_id = resolve_project_id(args.project_id, props.get("environment"))
    output_dir = (
        Path(args.output_dir)
        if args.output_dir
        else default_output_dir(project_id, args.entity_type, args.object_name)
    )
    scope_codes = resolve_scope_feature_code(args)

    summary = run_compare_engine(
        access_token=access_token,
        root=root,
        zip1=Path(args.zip1),
        zip2=Path(args.zip2),
        object_name=args.object_name,
        entity_type=args.entity_type,
        output_dir=output_dir,
        **scope_codes,
        no_lookup_code=args.no_lookup_code,
        source_cfg_created_by_flow=args.source_cfg_created_by_flow,
        poll_interval_seconds=args.poll_interval_seconds,
        timeout_minutes=args.timeout_minutes,
        no_poll=args.no_poll,
        skip_downloads=args.skip_downloads,
        include_diagnostics=args.include_diagnostics,
        artifact_names=args.artifact,
        dry_run=args.dry_run,
    )

    if args.dry_run:
        print(json.dumps({"ok": True, "dryRun": summary}, indent=2, ensure_ascii=False))
        return 0

    artifact_paths = artifact_paths_from_summary(summary)
    token_log_path = append_token_usage_log(
        project_id=project_id,
        skill_id=skill_id,
        task=f"Compare setup ZIPs: {args.object_name}",
        trigger=trigger,
        activity_start_time=args.activity_start_time,
        artifact_paths=artifact_paths,
        files_read=2,
        estimated_input_tokens=0,
        notes=(
            f"EntityType={args.entity_type}; CompareProcessId={summary.get('compareProcessId')}; "
            "Sensitive properties and token cache contents are excluded from estimates."
        ),
    )
    print(f"TokenUsageLog: {token_log_path}")

    print(json.dumps({"ok": True, "summary": summary}, indent=2, ensure_ascii=False))
    return 0


def main() -> int:
    args = parse_args()
    args.activity_start_time = utc_now()
    props = read_properties(Path(args.properties))
    require_props(props, ["environment", "restBaseUrl"])
    access_token = get_token(props, args)
    try:
        return run_compare(props, access_token, args)
    except CompareHttpError as exc:
        if exc.status_code not in {401, 403} or args.access_token or args.dry_run:
            raise
        print("Cached access token was rejected by Fusion. Running login flow again.", file=sys.stderr)
        access_token = get_token(props, args, force_login=True)
        return run_compare(props, access_token, args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CompareError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        raise SystemExit(1)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        raise SystemExit(1)
