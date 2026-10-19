#!/usr/bin/env python3
"""Find, start, poll, and download a Fusion setup task CSV export."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from fusion_skill_paths import (
    DEFAULT_PROPERTIES_PATH,
    add_auth_scripts_to_path,
    add_fsm_csv_export_scripts_to_path,
    add_project_mgmt_scripts_to_path,
    project_exports_root,
)

add_auth_scripts_to_path()
add_fsm_csv_export_scripts_to_path()
add_project_mgmt_scripts_to_path()

from setup_task_csv_support import (
    csv_export_import_flag,
    find_reference_path,
    find_task_matches,
    load_setup_tasks,
)
from find_setup_task_code import SETUP_TASKS_RESOURCE, filter_tasks, find_setup_tasks, get_value, quote_query_value
from fusion_auth import (
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    fusion_rest_json,
    get_access_token,
    read_properties,
    require_props,
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
from pillar_skill_metadata import (
    parent_skill_chain,
    kebab_case,
    repo_relative,
    resolve_task_skill_metadata,
)
from token_usage_logger import append_token_usage_log


SKILL_ID = "shared.setup-export.task-level-export"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export Fusion setup task data or its CSV template/spec package.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--task-code")
    group.add_argument("--task-name")
    parser.add_argument("--offering-name")
    parser.add_argument("--offering-code")
    parser.add_argument("--functional-area-name")
    parser.add_argument("--functional-area-code")
    parser.add_argument("--search-limit", type=int, default=100)
    parser.add_argument("--wait-seconds", type=int, default=300)
    parser.add_argument("--poll-interval", type=int, default=10)
    criteria_group = parser.add_mutually_exclusive_group()
    criteria_group.add_argument(
        "--export-criteria",
        help="JSON array to send as SetupTaskCSVExportCriteria.",
    )
    criteria_group.add_argument(
        "--export-criteria-file",
        help="Path to a JSON file containing the SetupTaskCSVExportCriteria array.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--template-only",
        "--template",
        "--spec",
        action="store_true",
        dest="template_only",
        default=True,
        help="Export only the setup task CSV template/spec package (the default).",
    )
    mode.add_argument(
        "--data",
        action="store_false",
        dest="template_only",
        help="Export populated setup CSV values; use only for an explicit setup-data request.",
    )
    parser.add_argument("--project-id", help="Project workspace ID under project/{project_id}. Defaults to FDOS_PROJECT_ID or the only initialized project.")
    parser.add_argument(
        "--output-dir",
        help=(
            "Output directory. Defaults to "
            "project/{project_id}/exports/<offering-kebab>/<functional-area-kebab>/<setup-task-name-kebab>."
        ),
    )
    parser.add_argument("--auth-code")
    parser.add_argument("--redirect-url")
    parser.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    parser.add_argument("--token-cache")
    parser.add_argument("--force-login", action="store_true")
    parser.add_argument("--access-token")
    parser.add_argument("--open-browser", action="store_true", default=True)
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    return parser.parse_args()


def load_export_criteria(args: argparse.Namespace, task_code: str) -> list[dict[str, object]]:
    raw_criteria = args.export_criteria
    if args.export_criteria_file:
        raw_criteria = Path(args.export_criteria_file).read_text(encoding="utf-8")
    if raw_criteria is None:
        return []
    try:
        criteria = json.loads(raw_criteria)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Export criteria must be valid JSON: {exc}") from exc
    return normalize_task_export_criteria(criteria, task_code)


def resolve_task(
    props: dict[str, str],
    access_token: str,
    args: argparse.Namespace,
) -> tuple[str, str, str | None, str | None, str]:
    if args.task_code:
        task = find_setup_task_by_code(props, access_token, args.task_code) or find_reference_task_by_code(args.task_code)
        task_name = get_value(task, "TaskName") if task else args.task_code
        csv_flag = csv_export_import_flag(task) if task else ""
        if task:
            print(
                f"TaskCode: {get_value(task, 'TaskCode') or args.task_code} "
                f"({task_name}); CSVExportImportSupportedFlag: {csv_flag or '(unknown)'}"
            )
        return (
            args.task_code,
            task_name,
            get_value(task, "OfferingName", "OfferingCode") if task else (args.offering_name or args.offering_code),
            get_value(task, "FunctionalAreaName", "FunctionalAreaCode")
            if task
            else (args.functional_area_name or args.functional_area_code),
            csv_flag,
        )
    items = find_setup_tasks(props, access_token, args.task_name, args.search_limit)
    items = filter_tasks(
        items,
        offering_name=args.offering_name,
        offering_code=args.offering_code,
        functional_area_name=args.functional_area_name,
        functional_area_code=args.functional_area_code,
    )
    if not items:
        raise RuntimeError("No setup task matched the supplied task name and filters.")
    exact = [item for item in items if get_value(item, "TaskName").casefold() == args.task_name.casefold()]
    selected = exact[0] if exact else items[0]
    if len(items) > 1 and not exact:
        print("Multiple setup tasks matched; using the first result:")
    csv_flag = csv_export_import_flag(selected)
    print(
        f"TaskCode: {get_value(selected, 'TaskCode')} ({get_value(selected, 'TaskName')}); "
        f"CSVExportImportSupportedFlag: {csv_flag or '(unknown)'}"
    )
    return (
        get_value(selected, "TaskCode"),
        get_value(selected, "TaskName") or args.task_name,
        get_value(selected, "OfferingName", "OfferingCode") or args.offering_name or args.offering_code,
        get_value(selected, "FunctionalAreaName", "FunctionalAreaCode")
        or args.functional_area_name
        or args.functional_area_code,
        csv_flag,
    )


def default_output_dir(
    task_name: str,
    offering: str | None,
    functional_area: str | None,
    project_id: str | None,
) -> Path:
    offering_part = kebab_case(offering or "offering")
    functional_area_part = kebab_case(functional_area or "functional area")
    task_part = kebab_case(task_name)
    return project_exports_root(project_id) / offering_part / functional_area_part / task_part


def print_pillar_skill_context(
    *,
    task_code: str,
    task_name: str,
    offering: str | None,
    functional_area: str | None,
    functional_area_code: str | None,
) -> tuple[str, str | None, str | None]:
    task_metadata = resolve_task_skill_metadata(
        task_code=task_code,
        task_name=task_name,
        offering=offering,
        functional_area=functional_area,
        functional_area_code=functional_area_code,
    )
    if task_metadata is None:
        print("No matching pillar setup-task metadata found; using supplied or Fusion task context for export path.")
        return task_name, offering, functional_area

    chain = parent_skill_chain(task_metadata)
    print("Resolved pillar skill metadata:")
    for label in ("offering", "functional_area", "task"):
        metadata = chain[label]
        if metadata:
            print(f"  {label}: {repo_relative(metadata.path)}")

    return (
        task_metadata.task_name or task_name,
        task_metadata.offering or offering,
        task_metadata.functional_area or functional_area,
    )


def find_setup_task_by_code(props: dict[str, str], access_token: str, task_code: str) -> dict[str, str] | None:
    response = fusion_rest_json(
        props,
        SETUP_TASKS_RESOURCE,
        access_token=access_token,
        query_params={
            "onlyData": "true",
            "totalResults": "true",
            "q": f"TaskCode='{quote_query_value(task_code)}'",
            "limit": "25",
        },
    )
    items = response.get("items")
    if not isinstance(items, list):
        return None
    for item in items:
        if isinstance(item, dict) and get_value(item, "TaskCode").casefold() == task_code.casefold():
            return item
    return None


def find_reference_task_by_code(task_code: str) -> dict[str, str] | None:
    reference_path = find_reference_path()
    if reference_path is None:
        return None
    matches = find_task_matches(load_setup_tasks(reference_path), task_code=task_code, allow_contains=False)
    return matches[0] if matches else None


def csv_export_not_supported_message(task_code: str, task_name: str, csv_flag: str) -> str:
    return (
        f"CSVExportImportSupportedFlag is {csv_flag or '(unknown)'} for "
        f"{task_code} ({task_name}). The setup task CSV export may not work, "
        "so no setup task CSV export was created."
    )


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
    activity_start_time = utc_now()
    args = parse_args()
    props = read_properties(Path(args.properties))
    require_props(props, ["environment", "restBaseUrl"])
    access_token = args.access_token or get_access_token(
        props,
        redirect_url=args.redirect_url,
        auth_code=args.auth_code,
        open_browser=args.open_browser,
        callback_timeout=args.callback_timeout,
        token_cache=args.token_cache,
        force_login=args.force_login,
    )

    task_code, task_name, offering, functional_area, csv_flag = resolve_task(props, access_token, args)
    task_name, offering, functional_area = print_pillar_skill_context(
        task_code=task_code,
        task_name=task_name,
        offering=offering or args.offering_name or args.offering_code,
        functional_area=functional_area or args.functional_area_name,
        functional_area_code=args.functional_area_code,
    )
    if csv_flag != "Y":
        print(csv_export_not_supported_message(task_code, task_name, csv_flag))
        return 2
    criteria = load_export_criteria(args, task_code)
    if criteria and args.template_only:
        raise ValueError("--export-criteria is not supported with --template-only.")

    scope = ExportScope(kind="task", primary_code=task_code, template_only=args.template_only)
    response = create_export_process(props, access_token, scope, task_export_criteria=criteria)
    process_id = extract_process_id(response, scope.process_child)
    if not process_id:
        raise RuntimeError(f"Fusion did not return a ProcessId: {response}")
    print(f"Started setup task {scope.export_label} process: {process_id}")

    process_status, result_items = wait_for_result(
        props,
        access_token,
        scope,
        str(process_id),
        args.wait_seconds,
        args.poll_interval,
    )
    current_status = status_code(result_items)
    if not process_completed(process_status.get("ProcessCompletedFlag")) and not current_status:
        print("Export process is not complete yet.")
        return 3

    should_download_log = current_status in ERROR_STATUS_CODES
    content, enclosure_name = download_result(
        props,
        access_token,
        scope,
        str(process_id),
        download_log=should_download_log,
    )
    output_dir = Path(args.output_dir) if args.output_dir else default_output_dir(
        task_name,
        offering,
        functional_area,
        args.project_id,
    )
    output_path = write_export_artifact(
        props,
        scope,
        str(process_id),
        content,
        output_dir=output_dir,
        is_log=enclosure_name == "ProcessLog",
    )
    project_id = infer_project_id(args.project_id, output_path)
    if project_id:
        token_log_path = append_token_usage_log(
            project_id=project_id,
            skill_id=SKILL_ID,
            task=f"Export setup task {scope.export_label}: {task_name}",
            trigger="setup task csv template export" if scope.template_only else "setup task export",
            activity_start_time=activity_start_time,
            artifact_paths=[output_path],
            files_read=0,
            estimated_input_tokens=0,
            notes=(
                f"TaskCode={task_code}; CriteriaCount={len(criteria)}; TemplateOnly={scope.template_only}; ProcessId={process_id}; Retrieved={enclosure_name}. "
                "Sensitive properties and token cache contents are excluded from estimates."
            ),
        )
        print(f"TokenUsageLog: {token_log_path}")
    print(f"StatusCode: {current_status or '(unknown)'}")
    print(f"Retrieved: {enclosure_name}")
    print(f"Wrote {output_path} ({len(content)} bytes)")
    return 4 if should_download_log else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
