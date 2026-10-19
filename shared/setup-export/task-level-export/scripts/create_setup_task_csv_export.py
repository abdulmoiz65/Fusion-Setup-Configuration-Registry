#!/usr/bin/env python3
"""Create an Oracle Fusion setup task CSV export process."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from fusion_skill_paths import DEFAULT_PROPERTIES_PATH, add_auth_scripts_to_path, add_fsm_csv_export_scripts_to_path

add_auth_scripts_to_path()
add_fsm_csv_export_scripts_to_path()

from setup_task_csv_support import (
    csv_export_import_flag,
    find_reference_path,
    find_task_matches,
    load_setup_tasks,
)
from fusion_auth import (
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    FusionHttpError,
    get_access_token,
    read_properties,
    require_props,
)
from fsm_csv_export_engine import ExportScope, create_task_export, extract_process_id as extract_engine_process_id
from fsm_csv_export_engine import normalize_task_export_criteria


def create_export(
    props: dict[str, str],
    access_token: str,
    task_code: str,
    *,
    criteria: list[dict[str, Any]] | None = None,
    template_only: bool = False,
) -> dict[str, Any]:
    return create_task_export(props, access_token, task_code, criteria=criteria, template_only=template_only)


def extract_process_id(response: dict[str, Any], *, template_only: bool = False) -> int | None:
    scope = ExportScope(kind="task", primary_code="", template_only=template_only)
    return extract_engine_process_id(response, scope.process_child)


def find_reference_task_by_code(task_code: str) -> dict[str, Any] | None:
    reference_path = find_reference_path()
    if reference_path is None:
        return None
    matches = find_task_matches(load_setup_tasks(reference_path), task_code=task_code, allow_contains=False)
    return matches[0] if matches else None


def check_csv_export_supported(task_code: str) -> bool:
    task = find_reference_task_by_code(task_code)
    if task is None:
        print(f"Could not find {task_code} in a local setup task reference; continuing with Fusion export request.")
        return True
    csv_flag = csv_export_import_flag(task)
    task_name = task.get("TaskName", task_code)
    print(f"CSVExportImportSupportedFlag: {csv_flag or '(unknown)'} for {task_code} ({task_name})")
    if csv_flag != "Y":
        print(
            "The setup task CSV export may not work for this task, "
            "so no setup task CSV export was created."
        )
        return False
    return True


def markdown_output(props: dict[str, str], task_code: str, response: dict[str, Any], *, template_only: bool) -> str:
    process_id = extract_process_id(response, template_only=template_only)
    title = "Setup Task CSV Template Export" if template_only else "Setup Task CSV Export"
    lines = [
        f"# {title}",
        "",
        f"Environment: `{props['environment']}`",
        "",
        f"Task Code: `{task_code}`",
        "",
        f"ProcessId: `{process_id or ''}`",
        "",
        "Response:",
        "",
        "```json",
        json.dumps(response, indent=2),
        "```",
        "",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create an Oracle Fusion setup task CSV export or template process.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--task-code", required=True)
    criteria_group = parser.add_mutually_exclusive_group()
    criteria_group.add_argument(
        "--export-criteria",
        help="JSON array to send as SetupTaskCSVExportCriteria.",
    )
    criteria_group.add_argument(
        "--export-criteria-file",
        help="Path to a JSON file containing the SetupTaskCSVExportCriteria array.",
    )
    parser.add_argument("--output")
    parser.add_argument("--print", action="store_true")
    parser.add_argument(
        "--template-only",
        "--template",
        "--spec",
        action="store_true",
        dest="template_only",
        help="Create a setup task CSV template/spec export process instead of a setup data export process.",
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


def load_export_criteria(args: argparse.Namespace) -> list[dict[str, Any]]:
    raw_criteria = args.export_criteria
    if args.export_criteria_file:
        raw_criteria = Path(args.export_criteria_file).read_text(encoding="utf-8")
    if raw_criteria is None:
        return []
    try:
        criteria = json.loads(raw_criteria)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Export criteria must be valid JSON: {exc}") from exc
    return normalize_task_export_criteria(criteria, args.task_code)


def main() -> int:
    args = parse_args()
    props = read_properties(Path(args.properties))
    require_props(props, ["environment", "restBaseUrl"])
    if not check_csv_export_supported(args.task_code):
        return 2
    criteria = load_export_criteria(args)
    if criteria and args.template_only:
        raise ValueError("--export-criteria is not supported with --template-only.")

    access_token = args.access_token or get_access_token(
        props,
        redirect_url=args.redirect_url,
        auth_code=args.auth_code,
        open_browser=args.open_browser,
        callback_timeout=args.callback_timeout,
        token_cache=args.token_cache,
        force_login=args.force_login,
    )

    try:
        response = create_export(props, access_token, args.task_code, criteria=criteria, template_only=args.template_only)
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403} or args.access_token:
            raise
        print("Cached access token was rejected by Fusion. Running login flow again.")
        access_token = get_access_token(
            props,
            redirect_url=args.redirect_url,
            auth_code=args.auth_code,
            open_browser=args.open_browser,
            callback_timeout=args.callback_timeout,
            token_cache=args.token_cache,
            force_login=True,
        )
        response = create_export(props, access_token, args.task_code, criteria=criteria, template_only=args.template_only)

    output = markdown_output(props, args.task_code, response, template_only=args.template_only)
    export_type = "csv_template_export" if args.template_only else "csv_export"
    output_path = Path(
        args.output or f"discovery/{props['environment']}_setup_task_{export_type}_{args.task_code.lower()}.md"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    if args.print:
        print(output, end="")
    print(f"Wrote {output_path}")
    process_id = extract_process_id(response, template_only=args.template_only)
    if process_id:
        print(f"ProcessId: {process_id}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
