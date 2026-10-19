#!/usr/bin/env python3
"""Retrieve Oracle Fusion setup tasks over REST."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from fusion_skill_paths import DEFAULT_PROPERTIES_PATH, add_auth_scripts_to_path

add_auth_scripts_to_path()

from fusion_auth import (
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    FusionHttpError,
    fusion_rest_json,
    get_access_token,
    read_properties,
    require_props,
)


SETUP_TASKS_RESOURCE = "/fscmRestApi/resources/latest/setupTasks"


def get_setup_tasks(props: dict[str, str], access_token: str, task_code: str, limit: int) -> dict[str, Any]:
    return fusion_rest_json(
        props,
        SETUP_TASKS_RESOURCE,
        access_token=access_token,
        query_params={
            "onlyData": "true",
            "totalResults": "true",
            "q": f"TaskCode='{task_code}'",
            "limit": str(limit),
        },
    )


def value(item: dict[str, Any], *keys: str) -> str:
    for key in keys:
        item_value = item.get(key)
        if item_value is not None:
            return str(item_value)
    return ""


def markdown_table(props: dict[str, str], response: dict[str, Any], task_code: str, limit: int) -> str:
    items = response.get("items")
    if not isinstance(items, list):
        raise RuntimeError(f"Fusion response did not include an items array: {response}")

    total_results = response.get("totalResults", len(items))
    rest_url = (
        f"{props['restBaseUrl'].rstrip('/')}{SETUP_TASKS_RESOURCE}"
        f"?onlyData=true&totalResults=true&q=TaskCode='{task_code}'&limit={limit}"
    )

    lines = [
        "# Fusion Setup Tasks",
        "",
        f"Environment: `{props['environment']}`",
        "",
        f"Task Code: `{task_code}`",
        "",
        "REST API:",
        f"`{rest_url}`",
        "",
        f"Total Results: `{total_results}`",
        "",
        "| # | Task Code | Task Name | Offering | Functional Area | Task Type |",
        "|---:|---|---|---|---|---|",
    ]

    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            continue
        lines.append(
            "| {index} | {task_code} | {task_name} | {offering} | {functional_area} | {task_type} |".format(
                index=index,
                task_code=value(item, "TaskCode"),
                task_name=value(item, "TaskName", "Name"),
                offering=value(item, "OfferingCode", "OfferingName"),
                functional_area=value(item, "FunctionalAreaCode", "FunctionalAreaName"),
                task_type=value(item, "TaskType", "SetupTaskType"),
            )
        )

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retrieve Oracle Fusion setup tasks and write a Markdown table.")
    parser.add_argument(
        "--properties",
        default=str(DEFAULT_PROPERTIES_PATH),
        help="Path to the Fusion environment properties file.",
    )
    parser.add_argument(
        "--task-code",
        required=True,
        help="Setup task code to retrieve, for example PO_MANAGE_INVENTORY_ORG_LOCATIONS.",
    )
    parser.add_argument(
        "--auth-code",
        help="OAuth2 authorization code. Used only when login is required.",
    )
    parser.add_argument(
        "--redirect-url",
        help="OAuth2 redirect URI to use when login is required.",
    )
    parser.add_argument(
        "--callback-timeout",
        type=int,
        default=DEFAULT_CALLBACK_TIMEOUT_SECONDS,
        help="Seconds to wait for a localhost OAuth callback.",
    )
    parser.add_argument(
        "--token-cache",
        help=(
            "Path to a file token cache. By default macOS Keychain is used when available, "
            "with fallback to a per-environment token cache."
        ),
    )
    parser.add_argument(
        "--force-login",
        action="store_true",
        help="Ignore any cached token and run the authorization-code login flow.",
    )
    parser.add_argument(
        "--access-token",
        help="Existing OAuth2 bearer token. Skips cached-token lookup and authorization-code exchange.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of setup tasks to request from Fusion.",
    )
    parser.add_argument(
        "--output",
        help="Markdown output path. Defaults to discovery/<environment>_setup_task_<task-code>.md.",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print the Markdown table to stdout as well as writing the output file.",
    )
    parser.add_argument(
        "--open-browser",
        action="store_true",
        default=True,
        help="Open the OAuth2 authorization URL in the default browser when login is required.",
    )
    parser.add_argument(
        "--no-open-browser",
        action="store_false",
        dest="open_browser",
        help="Print the authorization URL without opening a browser.",
    )
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
        response = get_setup_tasks(props, access_token, args.task_code, args.limit)
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
        response = get_setup_tasks(props, access_token, args.task_code, args.limit)

    markdown = markdown_table(props, response, args.task_code, args.limit)
    output_path = Path(
        args.output or f"discovery/{props['environment']}_setup_task_{args.task_code.lower()}.md"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    if args.print:
        print(markdown, end="")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
