#!/usr/bin/env python3
"""Resolve an offering and export its FSM setup data as a CSV ZIP package."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "shared" / "setup-export" / "fsm-csv-export").exists():
            return candidate
    raise RuntimeError("Could not locate repository root with the required layout")


REPO_ROOT = find_repo_root(Path(__file__).resolve())
FUSION_SKILLS_ROOT = REPO_ROOT
FSM_EXPORT_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "shared" / "setup-export" / "fsm-csv-export" / "scripts"
AUTH_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "core" / "auth" / "fusion-oauth-authentication" / "scripts"
PROJECT_MGMT_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "core" / "project-mgmt" / "scripts"
DEFAULT_PROPERTIES_PATH = FUSION_SKILLS_ROOT / "core" / "auth" / "fusionEnv.properties"
sys.path.insert(0, str(FSM_EXPORT_SCRIPTS_PATH))
sys.path.insert(0, str(AUTH_SCRIPTS_PATH))
sys.path.insert(0, str(PROJECT_MGMT_SCRIPTS_PATH))

from fusion_auth import (  # noqa: E402
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    FusionHttpError,
    get_access_token,
    read_properties,
    require_props,
)
from fsm_csv_export_engine import (  # noqa: E402
    ERROR_STATUS_CODES,
    ExportScope,
    create_export_process,
    extract_process_id,
    download_result,
    process_completed,
    resolve_feature_code,
    slug,
    status_code,
    wait_for_result,
    write_export_artifact,
)
from fusion_skill_paths import project_exports_root  # noqa: E402
from token_usage_logger import append_token_usage_log  # noqa: E402


SKILL_ID = "shared.setup-export.offering-export"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export Fusion setup data or CSV templates for an offering.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--offering-code")
    group.add_argument("--offering-name")
    parser.add_argument("--search-limit", type=int, default=25)
    parser.add_argument("--process-id")
    parser.add_argument("--wait-seconds", type=int, default=300)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--project-id", help="Project workspace ID under project/{project_id}. Defaults to FDOS_PROJECT_ID or the only initialized project.")
    parser.add_argument("--output-dir")
    parser.add_argument("--download-log", action="store_true")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--template-only",
        "--template",
        "--spec",
        action="store_true",
        dest="template_only",
        default=True,
        help="Export the offering CSV template/spec package (the default).",
    )
    mode.add_argument(
        "--data",
        action="store_false",
        dest="template_only",
        help="Export populated setup CSV values; use only for an explicit setup-data request.",
    )
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
    if args.access_token:
        return str(args.access_token)
    return get_access_token(
        props,
        redirect_url=args.redirect_url,
        auth_code=args.auth_code,
        open_browser=args.open_browser,
        callback_timeout=args.callback_timeout,
        token_cache=args.token_cache,
        force_login=args.force_login or force_login,
    )


def resolve_offering_code(props: dict[str, str], access_token: str, args: argparse.Namespace) -> str:
    if args.offering_code:
        return str(args.offering_code)
    offering_code = resolve_feature_code(
        props,
        access_token,
        str(args.offering_name),
        feature_type="OFFERING",
        limit=args.search_limit,
    )
    print(f"OfferingCode: {offering_code} ({args.offering_name})")
    return offering_code


def run_export(props: dict[str, str], access_token: str, args: argparse.Namespace) -> int:
    offering_code = resolve_offering_code(props, access_token, args)
    scope = ExportScope(kind="offering", primary_code=offering_code, template_only=args.template_only)
    process_id = args.process_id
    if not process_id:
        response = create_export_process(props, access_token, scope)
        extracted = extract_process_id(response, scope.process_child)
        if not extracted:
            raise RuntimeError(f"Fusion did not return a ProcessId: {response}")
        process_id = str(extracted)
        print(f"Started offering {scope.export_label} process: {process_id}")

    process_status, result_items = wait_for_result(
        props,
        access_token,
        scope,
        process_id,
        args.wait_seconds,
        args.poll_interval,
    )
    current_status = status_code(result_items)
    if not process_completed(process_status.get("ProcessCompletedFlag")) and current_status not in ERROR_STATUS_CODES:
        print("Export process is not complete yet.")
        return 3

    should_download_log = args.download_log or current_status in ERROR_STATUS_CODES
    content, enclosure_name = download_result(
        props,
        access_token,
        scope,
        process_id,
        download_log=should_download_log,
    )
    output_dir = (
        Path(args.output_dir)
        if args.output_dir
        else project_exports_root(args.project_id) / "setup-export" / "offering-export" / slug(offering_code)
    )
    output_path = write_export_artifact(
        props,
        scope,
        process_id,
        content,
        output_dir=output_dir,
        is_log=enclosure_name == "ProcessLog",
    )
    project_id = infer_project_id(args.project_id, output_path)
    if project_id:
        token_log_path = append_token_usage_log(
            project_id=project_id,
            skill_id=SKILL_ID,
            task=f"Export offering {scope.export_label}: {offering_code}",
            trigger="offering csv template export" if scope.template_only else "offering export",
            activity_start_time=args.activity_start_time,
            artifact_paths=[output_path],
            files_read=0,
            estimated_input_tokens=0,
            notes=(
                f"OfferingCode={offering_code}; TemplateOnly={scope.template_only}; ProcessId={process_id}; Retrieved={enclosure_name}. "
                "Sensitive properties and token cache contents are excluded from estimates."
            ),
        )
        print(f"TokenUsageLog: {token_log_path}")
    print(f"ProcessId: {process_id}")
    print(f"StatusCode: {current_status or '(unknown)'}")
    print(f"Retrieved: {enclosure_name}")
    print(f"Wrote {output_path} ({len(content)} bytes)")
    return 4 if should_download_log and current_status in ERROR_STATUS_CODES else 0


def infer_project_id(explicit_project_id: str | None, output_path: Path) -> str | None:
    parts = output_path.parts
    if "project" in parts:
        project_index = parts.index("project")
        if len(parts) > project_index + 1:
            project_id = parts[project_index + 1]
            if explicit_project_id is None or explicit_project_id == project_id:
                return project_id
    return None


def main() -> int:
    args = parse_args()
    args.activity_start_time = utc_now()
    props = read_properties(Path(args.properties))
    require_props(props, ["environment", "restBaseUrl"])
    access_token = get_token(props, args)
    try:
        return run_export(props, access_token, args)
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403} or args.access_token:
            raise
        print("Cached access token was rejected by Fusion. Running login flow again.", file=sys.stderr)
        access_token = get_token(props, args, force_login=True)
        return run_export(props, access_token, args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
