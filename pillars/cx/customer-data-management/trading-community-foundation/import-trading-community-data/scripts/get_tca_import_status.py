#!/usr/bin/env python3
"""Return a compact Trading Community Import Management status report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[6]
REST_CLIENT = REPOSITORY_ROOT / "core" / "fusion-api" / "rest-api-client" / "scripts" / "fusion_rest_client.py"
DEFAULT_PROPERTIES = REPOSITORY_ROOT / "core" / "auth" / "fusionEnv.properties"
IMPORT_ENDPOINT = "/crmRestApi/resources/11.13.18.05/importActivities"
COUNT_FIELDS = ("ReadFromFile", "LoadedSuccessfully", "ErrorsReported", "Warnings", "Unprocessed")
REPORT_FIELDS = ("ErrorReportContentId", "ExceptionReportContentId", "SuccessReportContentId")


class StatusError(RuntimeError):
    """A safe Trading Community status error."""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--import-activity-id", required=True)
    parser.add_argument("--expected-object-code", required=True)
    parser.add_argument("--expected-import-mode", required=True)
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES))
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--json", action="store_true", help="Return compact JSON instead of Markdown.")
    return parser.parse_args(argv)


def positive_activity_id(value: str) -> str:
    normalized = value.strip()
    if not normalized.isdigit() or int(normalized) < 1:
        raise StatusError("Import activity ID must be a positive integer.")
    return normalized


def run_rest(endpoint: str, args: argparse.Namespace) -> dict[str, Any]:
    command = [
        sys.executable,
        str(REST_CLIENT),
        endpoint,
        "--properties",
        args.properties,
        "--token-cache",
        args.token_cache,
        "--no-open-browser",
    ]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "The Fusion REST request failed."
        raise StatusError(detail)
    try:
        value = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise StatusError("The Fusion REST client returned an invalid status response.") from error
    if not isinstance(value, dict):
        raise StatusError("The Fusion REST client status response must be an object.")
    return value


def integer_count(value: Any) -> int:
    if value is None or value == "":
        return 0
    try:
        return int(str(value).strip())
    except ValueError:
        raise StatusError(f"Fusion returned a nonnumeric import count: {value!r}.")


def compact_status(
    activity: dict[str, Any],
    data_files_response: dict[str, Any],
    *,
    expected_object_code: str,
    expected_import_mode: str,
) -> dict[str, Any]:
    object_code = str(activity.get("ObjectCode") or "").strip()
    import_mode = str(activity.get("ImportMode") or "").strip()
    if object_code != expected_object_code:
        raise StatusError(
            f"Import activity ObjectCode mismatch: expected {expected_object_code!r}, received {object_code!r}."
        )
    if import_mode != expected_import_mode:
        raise StatusError(
            f"Import activity ImportMode mismatch: expected {expected_import_mode!r}, received {import_mode!r}."
        )

    raw_items = data_files_response.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        raise StatusError("Fusion returned no DataFiles status rows for the import activity.")
    items = [item for item in raw_items if isinstance(item, dict)]
    if len(items) != len(raw_items):
        raise StatusError("Fusion returned an invalid DataFiles status row.")
    statuses = [str(item.get("Status") or "").strip() for item in items]
    nonblank_statuses = [status for status in statuses if status]
    status = nonblank_statuses[0] if len(set(nonblank_statuses)) == 1 else "MULTIPLE"

    files = []
    for item in items:
        files.append(
            {
                "file_name": item.get("FileName"),
                "ucm_content_id": item.get("InputFileContentId"),
                "status": item.get("Status"),
                "read": integer_count(item.get("ReadFromFile")),
                "loaded": integer_count(item.get("LoadedSuccessfully")),
                "errors": integer_count(item.get("ErrorsReported")),
                "warnings": integer_count(item.get("Warnings")),
                "unprocessed": integer_count(item.get("Unprocessed")),
                "start_time": item.get("StartTime"),
                "end_time": item.get("EndTime"),
                "reports": {
                    field: item.get(field)
                    for field in REPORT_FIELDS
                    if item.get(field)
                },
            }
        )

    counts = {
        "read": sum(item["read"] for item in files),
        "loaded": sum(item["loaded"] for item in files),
        "errors": sum(item["errors"] for item in files),
        "warnings": sum(item["warnings"] for item in files),
        "unprocessed": sum(item["unprocessed"] for item in files),
    }
    return {
        "import_activity_id": activity.get("ImportActivityId"),
        "activity_name": activity.get("Name"),
        "object_code": object_code,
        "import_mode": import_mode,
        "activated": activity.get("Activate"),
        "schedule": activity.get("Schedule"),
        "status": status or None,
        "counts": counts,
        "files": files,
        "record_level_verification": "not_performed",
    }


def render_markdown(result: dict[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Trading Community import status",
        "",
        "| Item | Value |",
        "|---|---|",
        f"| Activity | {result['activity_name']} |",
        f"| Activity ID | {result['import_activity_id']} |",
        f"| Object | {result['object_code']} |",
        f"| Import mode | {result['import_mode']} |",
        f"| Status | {result['status'] or 'NOT_REPORTED'} |",
        f"| Activated | {result['activated']} |",
        f"| Schedule | {result['schedule']} |",
        "",
        "## Processing counts",
        "",
        "| Read | Loaded | Errors | Warnings | Unprocessed |",
        "|---:|---:|---:|---:|---:|",
        f"| {counts['read']} | {counts['loaded']} | {counts['errors']} | {counts['warnings']} | {counts['unprocessed']} |",
        "",
        "## Data files",
        "",
        "| File | UCM document | Status | Start | End |",
        "|---|---|---|---|---|",
    ]
    for item in result["files"]:
        lines.append(
            f"| {item['file_name']} | {item['ucm_content_id']} | {item['status']} | "
            f"{item['start_time'] or ''} | {item['end_time'] or ''} |"
        )
    reports = [
        (item["file_name"], name, value)
        for item in result["files"]
        for name, value in item["reports"].items()
    ]
    if reports:
        lines.extend(["", "## Fusion reports", "", "| File | Report | Content ID |", "|---|---|---|"])
        lines.extend(f"| {file_name} | {name} | {value} |" for file_name, name, value in reports)
    lines.extend(["", "Record-level verification was not performed."])
    if counts["errors"]:
        lines.extend([
            "",
            "The import completed with row errors. Retrieve the Fusion error report before correcting or resubmitting the source.",
        ])
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        activity_id = positive_activity_id(args.import_activity_id)
        activity = run_rest(f"{IMPORT_ENDPOINT}/{activity_id}", args)
        data_files = run_rest(f"{IMPORT_ENDPOINT}/{activity_id}/child/DataFiles", args)
        result = compact_status(
            activity,
            data_files,
            expected_object_code=args.expected_object_code,
            expected_import_mode=args.expected_import_mode,
        )
    except StatusError as error:
        print(f"Status check failed: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(render_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
