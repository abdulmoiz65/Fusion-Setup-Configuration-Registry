#!/usr/bin/env python3
"""Find, start, poll, and download a Fusion setup task CSV import log."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from fusion_skill_paths import DEFAULT_PROPERTIES_PATH, add_auth_scripts_to_path

add_auth_scripts_to_path()

from create_setup_task_csv_import import create_import, extract_process_id, read_zip_as_base64
from find_setup_task_code import filter_tasks, find_setup_tasks, get_value
from get_setup_task_csv_import_result import (
    COMPLETE_STATUS_CODES,
    ERROR_STATUS_CODES,
    enclosure_resource,
    status_code,
    wait_for_result,
)
from setup_task_csv_support import (
    csv_export_import_flag,
    find_reference_path,
    find_task_matches,
    load_setup_tasks,
)
from fusion_auth import (
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    FusionHttpError,
    fusion_rest_get_bytes,
    get_access_token,
    read_properties,
    require_props,
)


DEFAULT_ARTIFACT_ROOT = (
    Path("project")
    / "_adhoc"
    / "artifacts"
    / "shared"
    / "setup-import"
    / "task-level-import"
)


def slug(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import Fusion setup task data from a CSV ZIP package.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--task-code")
    parser.add_argument("--task-name")
    parser.add_argument("--offering-name")
    parser.add_argument("--offering-code")
    parser.add_argument("--functional-area-name")
    parser.add_argument("--functional-area-code")
    parser.add_argument("--search-limit", type=int, default=100)
    parser.add_argument("--zip-file", required=True, help="Path to the setup data ZIP file to import.")
    parser.add_argument("--wait-seconds", type=int, default=180)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument(
        "--output-dir",
        help=(
            "Output directory for import metadata and process log. Defaults to "
            "project/_adhoc/artifacts/shared/setup-import/task-level-import/<task_name>."
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


def resolve_task(
    props: dict[str, str],
    access_token: str,
    args: argparse.Namespace,
) -> tuple[str, str, str]:
    if args.task_code:
        reference_task = find_reference_task_by_code(args.task_code)
        task_name = args.task_name or get_value(reference_task or {}, "TaskName") or args.task_code
        csv_flag = csv_export_import_flag(reference_task)
        if reference_task:
            print(
                f"TaskCode: {args.task_code} ({task_name}); "
                f"CSVExportImportSupportedFlag: {csv_flag or '(unknown)'}"
            )
        return args.task_code, task_name, csv_flag
    if not args.task_name:
        raise RuntimeError("Provide either --task-code or --task-name.")

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
    task_code = get_value(selected, "TaskCode")
    task_name = get_value(selected, "TaskName") or args.task_name
    csv_flag = csv_export_import_flag(selected)
    print(f"TaskCode: {task_code} ({task_name}); CSVExportImportSupportedFlag: {csv_flag or '(unknown)'}")
    return task_code, task_name, csv_flag


def default_output_dir(task_name: str) -> Path:
    return DEFAULT_ARTIFACT_ROOT / slug(task_name)


def find_reference_task_by_code(task_code: str) -> dict[str, str] | None:
    reference_path = find_reference_path()
    if reference_path is None:
        return None
    matches = find_task_matches(load_setup_tasks(reference_path), task_code=task_code, allow_contains=False)
    return matches[0] if matches else None


def csv_import_not_supported_message(task_code: str, task_name: str, csv_flag: str) -> str:
    return (
        f"CSVExportImportSupportedFlag is {csv_flag or '(unknown)'} for "
        f"{task_code} ({task_name}). The setup task CSV import may not work, "
        "so no setup task CSV import was created."
    )


def main() -> int:
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

    task_code, task_name, csv_flag = resolve_task(props, access_token, args)
    if csv_flag and csv_flag != "Y":
        print(csv_import_not_supported_message(task_code, task_name, csv_flag))
        return 2

    zip_file = Path(args.zip_file)
    file_content_base64 = read_zip_as_base64(zip_file)

    try:
        response = create_import(props, access_token, task_code, file_content_base64)
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
        response = create_import(props, access_token, task_code, file_content_base64)

    process_id = extract_process_id(response)
    if not process_id:
        raise RuntimeError(f"Fusion did not return a ProcessId: {response}")
    print(f"Started setup task CSV import process: {process_id}")

    output_dir = Path(args.output_dir) if args.output_dir else default_output_dir(task_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = output_dir / f"{props['environment']}_setup_task_csv_import_{slug(task_code)}_{process_id}.json"
    metadata_path.write_text(
        json.dumps(
            {
                "environment": props["environment"],
                "taskCode": task_code,
                "taskName": task_name,
                "zipFile": str(zip_file),
                "processId": str(process_id),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    process_status, result_items = wait_for_result(
        props,
        access_token,
        task_code,
        str(process_id),
        args.wait_seconds,
        args.poll_interval,
    )
    current_status = status_code(result_items)
    if not process_status.get("ProcessCompletedFlag") and current_status not in COMPLETE_STATUS_CODES:
        print("Import process is not complete yet.")
        print(f"TaskCode: {task_code}")
        print(f"ProcessId: {process_id}")
        print(f"StatusCode: {current_status or '(no result yet)'}")
        print("Polling stopped. Ask to retry this ProcessId before retrieving import process artifacts.")
        print(f"Wrote {metadata_path}")
        return 3

    raw_content = fusion_rest_get_bytes(
        props,
        enclosure_resource(task_code, str(process_id), "ProcessLog"),
        access_token=access_token,
    )
    log_path = output_dir / f"{props['environment']}_setup_task_csv_import_{slug(task_code)}_{process_id}_process_log.txt"
    log_path.write_bytes(raw_content)

    print(f"StatusCode: {current_status or '(unknown)'}")
    print(f"Wrote {metadata_path}")
    print(f"Wrote {log_path} ({len(raw_content)} bytes)")
    return 4 if current_status in ERROR_STATUS_CODES else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
