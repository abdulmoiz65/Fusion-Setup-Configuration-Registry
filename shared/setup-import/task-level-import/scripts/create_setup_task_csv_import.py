#!/usr/bin/env python3
"""Create an Oracle Fusion setup task CSV import process."""

from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path
from typing import Any

from fusion_skill_paths import DEFAULT_PROPERTIES_PATH, add_auth_scripts_to_path

add_auth_scripts_to_path()

from setup_task_csv_support import (
    csv_export_import_flag,
    find_reference_path,
    find_task_matches,
    load_setup_tasks,
)
from fusion_auth import (
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    FusionHttpError,
    fusion_rest_post_json,
    get_access_token,
    read_properties,
    require_props,
)


SETUP_TASK_CSV_IMPORTS_RESOURCE = "/fscmRestApi/resources/11.13.18.05/setupTaskCSVImports"


def read_zip_as_base64(zip_file: Path) -> str:
    if not zip_file.exists():
        raise FileNotFoundError(f"ZIP file does not exist: {zip_file}")
    content = zip_file.read_bytes()
    if not content.startswith(b"PK\x03\x04"):
        raise ValueError(f"Expected a ZIP file starting with PK signature: {zip_file}")
    return base64.b64encode(content).decode("ascii")


def create_import(
    props: dict[str, str],
    access_token: str,
    task_code: str,
    file_content_base64: str,
) -> dict[str, Any]:
    payload = {
        "TaskCode": task_code,
        "SetupTaskCSVImportProcess": [
            {
                "TaskCode": task_code,
                "FileContent": file_content_base64,
            }
        ],
    }
    return fusion_rest_post_json(
        props,
        SETUP_TASK_CSV_IMPORTS_RESOURCE,
        access_token=access_token,
        json_body=payload,
    )


def extract_process_id(response: dict[str, Any]) -> int | None:
    process_items = response.get("SetupTaskCSVImportProcess")
    if not isinstance(process_items, list):
        return None
    for item in process_items:
        if isinstance(item, dict) and item.get("ProcessId") is not None:
            return int(item["ProcessId"])
    return None


def find_reference_task_by_code(task_code: str) -> dict[str, Any] | None:
    reference_path = find_reference_path()
    if reference_path is None:
        return None
    matches = find_task_matches(load_setup_tasks(reference_path), task_code=task_code, allow_contains=False)
    return matches[0] if matches else None


def check_csv_import_supported(task_code: str) -> bool:
    task = find_reference_task_by_code(task_code)
    if task is None:
        print(f"Could not find {task_code} in a local setup task reference; continuing with Fusion import request.")
        return True
    csv_flag = csv_export_import_flag(task)
    task_name = task.get("TaskName", task_code)
    print(f"CSVExportImportSupportedFlag: {csv_flag or '(unknown)'} for {task_code} ({task_name})")
    if csv_flag != "Y":
        print(
            "The setup task CSV import may not work for this task, "
            "so no setup task CSV import was created."
        )
        return False
    return True


def markdown_output(props: dict[str, str], task_code: str, zip_file: Path, response: dict[str, Any]) -> str:
    process_id = extract_process_id(response)
    lines = [
        "# Setup Task CSV Import",
        "",
        f"Environment: `{props['environment']}`",
        "",
        f"Task Code: `{task_code}`",
        "",
        f"ZIP File: `{zip_file}`",
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
    parser = argparse.ArgumentParser(description="Create an Oracle Fusion setup task CSV import process.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--task-code", required=True)
    parser.add_argument("--zip-file", required=True, help="Path to the setup data ZIP file to import.")
    parser.add_argument("--output")
    parser.add_argument("--print", action="store_true")
    parser.add_argument("--auth-code")
    parser.add_argument("--redirect-url")
    parser.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    parser.add_argument("--token-cache")
    parser.add_argument("--force-login", action="store_true")
    parser.add_argument("--access-token")
    parser.add_argument("--open-browser", action="store_true", default=True)
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    props = read_properties(Path(args.properties))
    require_props(props, ["environment", "restBaseUrl"])
    if not check_csv_import_supported(args.task_code):
        return 2

    access_token = args.access_token or get_access_token(
        props,
        redirect_url=args.redirect_url,
        auth_code=args.auth_code,
        open_browser=args.open_browser,
        callback_timeout=args.callback_timeout,
        token_cache=args.token_cache,
        force_login=args.force_login,
    )
    zip_file = Path(args.zip_file)
    file_content_base64 = read_zip_as_base64(zip_file)

    try:
        response = create_import(props, access_token, args.task_code, file_content_base64)
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
        response = create_import(props, access_token, args.task_code, file_content_base64)

    output = markdown_output(props, args.task_code, zip_file, response)
    output_path = Path(
        args.output or f"project/_adhoc/artifacts/shared/setup-import/task-level-import/{args.task_code.lower()}/setup_task_csv_import.md"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    if args.print:
        print(output, end="")
    print(f"Wrote {output_path}")
    process_id = extract_process_id(response)
    if process_id:
        print(f"ProcessId: {process_id}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
