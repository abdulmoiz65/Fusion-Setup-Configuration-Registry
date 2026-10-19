#!/usr/bin/env python3
"""Poll and download an Oracle Fusion setup task CSV import process log."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Any

from fusion_skill_paths import DEFAULT_PROPERTIES_PATH, add_auth_scripts_to_path

add_auth_scripts_to_path()

from fusion_auth import (
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    FusionHttpError,
    fusion_rest_get_bytes,
    fusion_rest_json,
    get_access_token,
    read_properties,
    require_props,
)


SETUP_TASK_CSV_IMPORTS_RESOURCE = "/fscmRestApi/resources/11.13.18.05/setupTaskCSVImports"
SUCCESS_STATUS_CODES = {"COMPLETED", "COMPLETED_WARNINGS"}
ERROR_STATUS_CODES = {"COMPLETED_ERRORS"}
COMPLETE_STATUS_CODES = SUCCESS_STATUS_CODES | ERROR_STATUS_CODES


def process_resource(task_code: str, process_id: str) -> str:
    return f"{SETUP_TASK_CSV_IMPORTS_RESOURCE}/{task_code}/child/SetupTaskCSVImportProcess/{process_id}"


def result_collection_resource(task_code: str, process_id: str) -> str:
    return f"{process_resource(task_code, process_id)}/child/SetupTaskCSVImportProcessResult"


def result_resource(task_code: str, process_id: str) -> str:
    return f"{result_collection_resource(task_code, process_id)}/{process_id}"


def enclosure_resource(task_code: str, process_id: str, enclosure_name: str) -> str:
    return f"{result_resource(task_code, process_id)}/enclosure/{enclosure_name}"


def get_process_status(props: dict[str, str], access_token: str, task_code: str, process_id: str) -> dict[str, Any]:
    return fusion_rest_json(
        props,
        process_resource(task_code, process_id),
        access_token=access_token,
        query_params={"onlyData": "true"},
    )


def get_result_items(props: dict[str, str], access_token: str, task_code: str, process_id: str) -> list[dict[str, Any]]:
    response = fusion_rest_json(
        props,
        result_collection_resource(task_code, process_id),
        access_token=access_token,
        query_params={"onlyData": "true", "limit": "25"},
    )
    items = response.get("items")
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, dict)]


def status_code(items: list[dict[str, Any]]) -> str:
    for item in items:
        value = item.get("StatusCode")
        if value:
            return str(value)
    return ""


def wait_for_result(
    props: dict[str, str],
    access_token: str,
    task_code: str,
    process_id: str,
    wait_seconds: int,
    poll_interval: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    deadline = time.time() + wait_seconds
    while True:
        process_status = get_process_status(props, access_token, task_code, process_id)
        result_items = get_result_items(props, access_token, task_code, process_id)
        completed = process_status.get("ProcessCompletedFlag")
        current_status = status_code(result_items)
        print(
            f"ProcessCompletedFlag: {completed}; "
            f"StatusCode: {current_status or '(no result yet)'}; ResultCount: {len(result_items)}"
        )
        if completed or current_status in COMPLETE_STATUS_CODES:
            return process_status, result_items
        if wait_seconds <= 0 or time.time() >= deadline:
            return process_status, result_items
        time.sleep(poll_interval)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Poll and download an Oracle Fusion setup task CSV import log.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--task-code", required=True)
    parser.add_argument("--process-id", required=True)
    parser.add_argument("--wait-seconds", type=int, default=180)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--output")
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
        process_status, result_items = wait_for_result(
            props,
            access_token,
            args.task_code,
            args.process_id,
            args.wait_seconds,
            args.poll_interval,
        )
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
        process_status, result_items = wait_for_result(
            props,
            access_token,
            args.task_code,
            args.process_id,
            args.wait_seconds,
            args.poll_interval,
        )

    current_status = status_code(result_items)
    if not process_status.get("ProcessCompletedFlag") and current_status not in COMPLETE_STATUS_CODES:
        print("Import process is not complete yet.")
        print(f"TaskCode: {args.task_code}")
        print(f"ProcessId: {args.process_id}")
        print(f"StatusCode: {current_status or '(no result yet)'}")
        print("Polling stopped. Ask to retry this ProcessId before retrieving import process artifacts.")
        return 3

    raw_content = fusion_rest_get_bytes(
        props,
        enclosure_resource(args.task_code, args.process_id, "ProcessLog"),
        access_token=access_token,
    )
    output_path = Path(
        args.output
        or f"project/_adhoc/artifacts/shared/setup-import/task-level-import/{args.task_code.lower()}/{props['environment']}_setup_task_csv_import_{args.task_code.lower()}_{args.process_id}_process_log.txt"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(raw_content)

    print(f"ProcessId: {args.process_id}")
    print(f"StatusCode: {current_status or '(unknown)'}")
    print(f"Wrote {output_path} ({len(raw_content)} bytes)")
    return 4 if current_status in ERROR_STATUS_CODES else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
