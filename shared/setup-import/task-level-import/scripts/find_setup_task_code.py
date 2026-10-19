#!/usr/bin/env python3
"""Find Oracle Fusion setup task codes by task name."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from fusion_skill_paths import DEFAULT_PROPERTIES_PATH, add_auth_scripts_to_path

add_auth_scripts_to_path()

from setup_task_csv_support import find_reference_path, find_task_matches, load_setup_tasks
from fusion_auth import (
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    FusionHttpError,
    fusion_rest_json,
    get_access_token,
    read_properties,
    require_props,
)


SETUP_TASKS_RESOURCE = "/fscmRestApi/resources/11.13.18.05/setupTasks"


def quote_query_value(value: str) -> str:
    return value.replace("'", "''")


def get_value(item: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = item.get(key)
        if value is not None:
            return str(value)
    return ""


def find_setup_tasks(
    props: dict[str, str],
    access_token: str,
    task_name: str,
    limit: int,
) -> list[dict[str, Any]]:
    response = fusion_rest_json(
        props,
        SETUP_TASKS_RESOURCE,
        access_token=access_token,
        query_params={
            "onlyData": "true",
            "totalResults": "true",
            "q": f"TaskName LIKE '%{quote_query_value(task_name)}%'",
            "limit": str(limit),
        },
    )
    items = response.get("items")
    if not isinstance(items, list):
        raise RuntimeError(f"Fusion response did not include an items array: {response}")
    return [item for item in items if isinstance(item, dict)]


def find_local_setup_tasks(task_name: str, limit: int) -> list[dict[str, Any]]:
    reference_path = find_reference_path()
    if reference_path is None:
        return []
    matches = find_task_matches(load_setup_tasks(reference_path), task_name=task_name, allow_contains=True)
    return matches[:limit]


def matches_optional(value: str, expected: str | None) -> bool:
    return expected is None or value.casefold() == expected.casefold()


def filter_tasks(
    items: list[dict[str, Any]],
    *,
    offering_name: str | None,
    offering_code: str | None,
    functional_area_name: str | None,
    functional_area_code: str | None,
) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []
    for item in items:
        if not matches_optional(get_value(item, "OfferingName"), offering_name):
            continue
        if not matches_optional(get_value(item, "OfferingCode"), offering_code):
            continue
        if not matches_optional(get_value(item, "FunctionalAreaName"), functional_area_name):
            continue
        if not matches_optional(get_value(item, "FunctionalAreaCode"), functional_area_code):
            continue
        filtered.append(item)
    return filtered


def markdown_table(props: dict[str, str], items: list[dict[str, Any]], task_name: str) -> str:
    lines = [
        "# Setup Task Code Search",
        "",
        f"Environment: `{props['environment']}`",
        "",
        f"Task Name Search: `{task_name}`",
        "",
        "| # | Task Code | Task Name | Offering | Functional Area | Available | CSV Import |",
        "|---:|---|---|---|---|---|---|",
    ]
    for index, item in enumerate(items, 1):
        offering = get_value(item, "OfferingName", "OfferingCode")
        functional_area = get_value(item, "FunctionalAreaName", "FunctionalAreaCode")
        lines.append(
            f"| {index} | {get_value(item, 'TaskCode')} | {get_value(item, 'TaskName')} | "
            f"{offering} | {functional_area} | {get_value(item, 'AvailableFlag')} | "
            f"{get_value(item, 'CSVExportImportSupportedFlag', 'ExportImportSupportedFlag')} |"
        )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find Oracle Fusion setup task codes by task name.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--task-name", required=True)
    parser.add_argument("--offering-name")
    parser.add_argument("--offering-code")
    parser.add_argument("--functional-area-name")
    parser.add_argument("--functional-area-code")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--output")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    parser.add_argument("--print", action="store_true", help="Print output as well as writing it.")
    parser.add_argument(
        "--local-reference-only",
        action="store_true",
        help="Search the effective FSCR setup-task catalog without calling Fusion.",
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
    if args.local_reference_only:
        reference_path = find_reference_path()
        props = {"environment": str(reference_path or "local setup task catalog")}
        items = find_local_setup_tasks(args.task_name, args.limit)
        items = filter_tasks(
            items,
            offering_name=args.offering_name,
            offering_code=args.offering_code,
            functional_area_name=args.functional_area_name,
            functional_area_code=args.functional_area_code,
        )
        output = json.dumps(items, indent=2) + "\n" if args.json else markdown_table(props, items, args.task_name)
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding="utf-8")
            print(f"Wrote {output_path}")
        if args.print or not args.output:
            print(output, end="")
        if not items:
            return 2
        return 0

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
        items = find_setup_tasks(props, access_token, args.task_name, args.limit)
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
        items = find_setup_tasks(props, access_token, args.task_name, args.limit)

    items = filter_tasks(
        items,
        offering_name=args.offering_name,
        offering_code=args.offering_code,
        functional_area_name=args.functional_area_name,
        functional_area_code=args.functional_area_code,
    )

    output = json.dumps(items, indent=2) + "\n" if args.json else markdown_table(props, items, args.task_name)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        print(f"Wrote {output_path}")
    if args.print or not args.output:
        print(output, end="")
    if not items:
        return 2
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
