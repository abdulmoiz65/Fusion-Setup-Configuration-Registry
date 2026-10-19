#!/usr/bin/env python3
"""Poll and download an Oracle Fusion setup task CSV export result."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from fusion_skill_paths import DEFAULT_PROPERTIES_PATH, add_auth_scripts_to_path, add_fsm_csv_export_scripts_to_path

add_auth_scripts_to_path()
add_fsm_csv_export_scripts_to_path()

from fusion_auth import (
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    FusionHttpError,
    fusion_rest_get_bytes,
    get_access_token,
    read_properties,
    require_props,
)
from fsm_csv_export_engine import (
    ERROR_STATUS_CODES,
    SUCCESS_STATUS_CODES,
    ExportScope,
    decode_file_content,
    enclosure_resource as engine_enclosure_resource,
    get_process_status as engine_get_process_status,
    get_result_items as engine_get_result_items,
    process_completed,
    process_resource as engine_process_resource,
    result_collection_resource as engine_result_collection_resource,
    result_resource as engine_result_resource,
    status_code,
    wait_for_result as engine_wait_for_result,
)


def task_scope(task_code: str, *, template_only: bool = False) -> ExportScope:
    return ExportScope(kind="task", primary_code=task_code, template_only=template_only)


def process_resource(task_code: str, process_id: str) -> str:
    return engine_process_resource(task_scope(task_code), process_id)


def result_collection_resource(task_code: str, process_id: str) -> str:
    return engine_result_collection_resource(task_scope(task_code), process_id)


def result_resource(task_code: str, process_id: str) -> str:
    return engine_result_resource(task_scope(task_code), process_id)


def enclosure_resource(task_code: str, process_id: str, enclosure_name: str) -> str:
    return engine_enclosure_resource(task_scope(task_code), process_id, enclosure_name)


def get_process_status(props: dict[str, str], access_token: str, task_code: str, process_id: str) -> dict[str, Any]:
    return engine_get_process_status(props, access_token, task_scope(task_code), process_id)


def get_result_items(props: dict[str, str], access_token: str, task_code: str, process_id: str) -> list[dict[str, Any]]:
    return engine_get_result_items(props, access_token, task_scope(task_code), process_id)


def wait_for_result(
    props: dict[str, str],
    access_token: str,
    task_code: str,
    process_id: str,
    wait_seconds: int,
    poll_interval: int,
    *,
    template_only: bool = False,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    return engine_wait_for_result(
        props,
        access_token,
        task_scope(task_code, template_only=template_only),
        process_id,
        wait_seconds,
        poll_interval,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Poll and download an Oracle Fusion setup task CSV export or template result.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--task-code", required=True)
    parser.add_argument("--process-id", required=True)
    parser.add_argument("--wait-seconds", type=int, default=0)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--output")
    parser.add_argument("--log-output")
    parser.add_argument("--download-log", action="store_true", help="Download ProcessLog instead of FileContent.")
    parser.add_argument(
        "--template-only",
        "--template",
        "--spec",
        action="store_true",
        dest="template_only",
        help="Poll/download a setup task CSV template/spec export process instead of a setup data export process.",
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
            template_only=args.template_only,
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
            template_only=args.template_only,
        )

    current_status = status_code(result_items)
    if not process_completed(process_status.get("ProcessCompletedFlag")) and current_status not in SUCCESS_STATUS_CODES | ERROR_STATUS_CODES:
        print("Export process is not complete yet.")
        return 3

    should_download_log = args.download_log or current_status in ERROR_STATUS_CODES
    enclosure_name = "ProcessLog" if should_download_log else "FileContent"
    raw_content = fusion_rest_get_bytes(
        props,
        engine_enclosure_resource(
            task_scope(args.task_code, template_only=args.template_only),
            args.process_id,
            enclosure_name,
        ),
        access_token=access_token,
    )
    content = raw_content if should_download_log else decode_file_content(raw_content)

    if should_download_log:
        output_path = Path(
            args.log_output
            or (
                f"discovery/{props['environment']}_setup_task_"
                f"{'csv_template_export' if args.template_only else 'csv_export'}_"
                f"{args.task_code.lower()}_{args.process_id}_process_log.txt"
            )
        )
    else:
        output_path = Path(
            args.output
            or (
                f"discovery/{props['environment']}_setup_task_"
                f"{'csv_template_export' if args.template_only else 'csv_export'}_"
                f"{args.task_code.lower()}_{args.process_id}.zip"
            )
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(content)

    print(f"ProcessId: {args.process_id}")
    print(f"StatusCode: {current_status or '(unknown)'}")
    print(f"Wrote {output_path} ({len(content)} bytes)")
    if should_download_log:
        return 4 if current_status in ERROR_STATUS_CODES else 0
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
