#!/usr/bin/env python3
"""Create, poll, and download Oracle Fusion FSM CSV export packages."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from fusion_skill_paths import (
    DEFAULT_PROPERTIES_PATH,
    add_auth_scripts_to_path,
    add_project_mgmt_scripts_to_path,
    project_exports_root,
)
from fsm_csv_export_engine import (
    ERROR_STATUS_CODES,
    ExportScope,
    create_export_process,
    download_result,
    extract_process_id,
    process_completed,
    status_code,
    wait_for_result,
    write_export_artifact,
    normalize_task_export_criteria,
)

add_auth_scripts_to_path()
add_project_mgmt_scripts_to_path()

from fusion_auth import (  # noqa: E402
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    FusionHttpError,
    get_access_token,
    read_properties,
    require_props,
)
from token_usage_logger import append_token_usage_log  # noqa: E402


SKILL_ID = "shared.setup-export.fsm-csv-export"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export Fusion FSM setup data or CSV templates as ZIP packages.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--scope", choices=["task", "offering", "functional-area"], required=True)
    parser.add_argument("--task-code")
    parser.add_argument("--offering-code")
    parser.add_argument("--functional-area-code")
    parser.add_argument("--process-id", help="Poll/download an existing export process instead of creating one.")
    parser.add_argument("--wait-seconds", type=int, default=300)
    parser.add_argument("--poll-interval", type=int, default=10)
    criteria_group = parser.add_mutually_exclusive_group()
    criteria_group.add_argument("--export-criteria", help="JSON array to send as SetupTaskCSVExportCriteria for task scope.")
    criteria_group.add_argument("--export-criteria-file", help="JSON file containing SetupTaskCSVExportCriteria for task scope.")
    parser.add_argument("--project-id", help="Project workspace ID under project/{project_id}. Defaults to FDOS_PROJECT_ID or the only initialized project.")
    parser.add_argument("--output-dir")
    parser.add_argument("--download-log", action="store_true", help="Download ProcessLog instead of FileContent.")
    parser.add_argument(
        "--template-only",
        "--template",
        "--spec",
        action="store_true",
        dest="template_only",
        help="Export the CSV template/spec package instead of setup CSV values.",
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


def build_scope(args: argparse.Namespace) -> ExportScope:
    if args.scope == "task":
        if not args.task_code:
            raise ValueError("--task-code is required for task scope")
        return ExportScope(kind="task", primary_code=args.task_code, template_only=args.template_only)
    if not args.offering_code:
        raise ValueError("--offering-code is required for offering and functional-area scopes")
    if args.scope == "functional-area" and not args.functional_area_code:
        raise ValueError("--functional-area-code is required for functional-area scope")
    return ExportScope(
        kind=args.scope,
        primary_code=args.offering_code,
        functional_area_code=args.functional_area_code,
        template_only=args.template_only,
    )


def load_export_criteria(args: argparse.Namespace, scope: ExportScope) -> list[dict[str, object]]:
    raw_criteria = args.export_criteria
    if args.export_criteria_file:
        raw_criteria = Path(args.export_criteria_file).read_text(encoding="utf-8")
    if raw_criteria is None:
        return []
    if args.process_id:
        raise ValueError("--export-criteria cannot be used with --process-id because no create request is made.")
    if scope.kind != "task":
        raise ValueError("--export-criteria is supported only with --scope task.")
    if scope.template_only:
        raise ValueError("--export-criteria is not supported with --template-only.")
    try:
        criteria = json.loads(raw_criteria)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Export criteria must be valid JSON: {exc}") from exc
    return normalize_task_export_criteria(criteria, scope.primary_code)


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


def run_export(props: dict[str, str], access_token: str, scope: ExportScope, args: argparse.Namespace) -> int:
    process_id = args.process_id
    if not process_id:
        response = create_export_process(props, access_token, scope, task_export_criteria=args.export_criteria_items)
        extracted = extract_process_id(response, scope.process_child)
        if not extracted:
            raise RuntimeError(f"Fusion did not return a ProcessId: {response}")
        process_id = str(extracted)
        print(f"Started {scope.kind} {scope.export_label} process: {process_id}")

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
    output_path = write_export_artifact(
        props,
        scope,
        process_id,
        content,
        output_dir=Path(args.output_dir) if args.output_dir else project_exports_root(args.project_id) / "fsm-csv-export",
        is_log=enclosure_name == "ProcessLog",
    )
    project_id = infer_project_id(args.project_id, output_path)
    if project_id:
        token_log_path = append_token_usage_log(
            project_id=project_id,
            skill_id=SKILL_ID,
            task=f"Export FSM {scope.export_label}: {scope.kind}",
            trigger="fsm csv template export" if scope.template_only else "fsm csv export",
            activity_start_time=args.activity_start_time,
            artifact_paths=[output_path],
            files_read=0,
            estimated_input_tokens=0,
            notes=(
                f"Scope={scope.kind}; Code={scope.primary_code}; CriteriaCount={len(args.export_criteria_items)}; TemplateOnly={scope.template_only}; ProcessId={process_id}; "
                f"Retrieved={enclosure_name}. Sensitive properties and token cache contents are excluded from estimates."
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
    scope = build_scope(args)
    args.export_criteria_items = load_export_criteria(args, scope)
    access_token = get_token(props, args)
    try:
        return run_export(props, access_token, scope, args)
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403} or args.access_token:
            raise
        print("Cached access token was rejected by Fusion. Running login flow again.", file=sys.stderr)
        access_token = get_token(props, args, force_login=True)
        return run_export(props, access_token, scope, args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
