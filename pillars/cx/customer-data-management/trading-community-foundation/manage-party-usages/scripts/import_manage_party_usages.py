#!/usr/bin/env python3
"""Import the fixed Manage Party Usages FSM package after Task Hook approval."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as element_tree
import zipfile


def find_repository_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "core" / "data-loader").is_dir() and (
            candidate / "shared" / "setup-import" / "fsm-csv-import"
        ).is_dir():
            return candidate
    raise RuntimeError("Could not locate the FSCR repository root.")


REPOSITORY_ROOT = find_repository_root()
FSM_SCRIPTS = REPOSITORY_ROOT / "shared" / "setup-import" / "fsm-csv-import" / "scripts"
AUTH_SCRIPTS = (
    REPOSITORY_ROOT
    / "core"
    / "auth"
    / "fusion-oauth-authentication"
    / "scripts"
)
VALIDATOR_SCRIPTS = REPOSITORY_ROOT / "core" / "data-loader" / "task-validator" / "scripts"
for scripts_path in (FSM_SCRIPTS, AUTH_SCRIPTS, VALIDATOR_SCRIPTS):
    if str(scripts_path) not in sys.path:
        sys.path.insert(0, str(scripts_path))

import fsm_csv_import_engine as engine  # noqa: E402
from fusion_auth import (  # noqa: E402
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    get_access_token,
    http_bytes,
    http_json,
    read_properties,
    require_props,
)
from task_rule_execution import approved_loader_payload  # noqa: E402


TASK_CODE = "HZ_MANAGE_PARTY_USAGES"
TASK_NAME = "Manage Party Usages"
EXECUTION_ADAPTER = (
    "cx.customer-data-management.trading-community-foundation."
    "manage-party-usages.native-fsm-import"
)
SOURCE_TARGET_DIFF_OK_FLAG = "Y"
DEFAULT_PROPERTIES = REPOSITORY_ROOT / "core" / "auth" / "fusionEnv.properties"
REST_FRAMEWORK_VERSION = "9"
IMPORT_PROCESS_CREATE_RESOURCE = (
    f"{engine.SETUP_TASK_CSV_IMPORTS_RESOURCE}/{TASK_CODE}/child/"
    "SetupTaskCSVImportProcess"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_fsm_archive(path: Path) -> None:
    if not zipfile.is_zipfile(path):
        raise ValueError("The supplied package is not a valid ZIP archive.")
    with zipfile.ZipFile(path) as archive:
        members = [
            member
            for member in archive.infolist()
            if not member.is_dir()
            and member.filename.rsplit("/", 1)[-1] == "ASM_SETUP_CSV_METADATA.xml"
        ]
        if len(members) != 1:
            raise ValueError("FSM ZIP must contain exactly one ASM_SETUP_CSV_METADATA.xml member.")
        try:
            root = element_tree.fromstring(archive.read(members[0]))
        except element_tree.ParseError as error:
            raise ValueError("ASM_SETUP_CSV_METADATA.xml is not valid XML.") from error
    object_short_names = [
        (element.text or "").strip()
        for element in root.iter()
        if element.tag.rsplit("}", 1)[-1] == "ObjectShortName"
        and (element.text or "").strip()
    ]
    if object_short_names != [TASK_CODE]:
        raise ValueError(
            "FSM metadata must contain exactly one ObjectShortName equal to " + TASK_CODE + "."
        )


def request_headers(access_token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {access_token}",
        "REST-Framework-Version": REST_FRAMEWORK_VERSION,
    }


def load_approved_final_data(
    envelope_path: Path,
    zip_file: Path,
) -> dict[str, Any]:
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    payload = approved_loader_payload(envelope.get("preview"), envelope.get("approval"))
    if payload.get("taskCode") != TASK_CODE or payload.get("taskName") != TASK_NAME:
        raise ValueError("Task Hook approval does not match Manage Party Usages.")
    final_data = payload.get("finalData")
    if not isinstance(final_data, dict):
        raise ValueError("Task Hook approval does not contain finalData.")
    if final_data.get("executionRoute") != "data-loader":
        raise ValueError("Approved executionRoute must be data-loader.")
    if final_data.get("executionAdapter") != EXECUTION_ADAPTER:
        raise ValueError("Approved executionAdapter does not match the task-local native FSM adapter.")
    if final_data.get("packageType") != "FSM" or final_data.get("wholeTask") is not True:
        raise ValueError("Approval must cover one whole-task FSM package.")
    if final_data.get("taskCode") != TASK_CODE or final_data.get("taskName") != TASK_NAME:
        raise ValueError("Approved finalData task identity does not match Manage Party Usages.")

    approved_path = Path(str(final_data.get("absoluteZipPath") or "")).expanduser().resolve()
    if approved_path != zip_file.expanduser().resolve():
        raise ValueError("Approved ZIP path does not match the supplied ZIP path.")
    approved_sha = str(final_data.get("archiveSha256") or "").lower()
    actual_sha = sha256_file(zip_file)
    if approved_sha != actual_sha:
        raise ValueError("Approved archive SHA-256 does not match the supplied ZIP bytes.")

    return final_data


def create_import(
    props: dict[str, str],
    access_token: str,
    file_content_base64: str,
) -> dict[str, Any]:
    payload = {
        "TaskCode": TASK_CODE,
        "FileContent": file_content_base64,
        "SourceTargetDiffOkFlag": SOURCE_TARGET_DIFF_OK_FLAG,
    }
    return http_json(
        props["restBaseUrl"].rstrip("/") + IMPORT_PROCESS_CREATE_RESOURCE,
        method="POST",
        json_body=payload,
        access_token=access_token, headers=request_headers(access_token),
    )


def extract_process_id(response: dict[str, Any]) -> int | None:
    """Read the documented child-create response, with legacy compatibility."""
    direct = response.get("ProcessId")
    if direct is not None:
        try:
            return int(direct)
        except (TypeError, ValueError):
            pass
    return engine.extract_process_id(response, "SetupTaskCSVImportProcess")


def redact_create_response(value: Any) -> Any:
    """Remove archive bytes from a response while preserving diagnostic shape."""
    if isinstance(value, dict):
        return {
            key: "<redacted>" if key == "FileContent" else redact_create_response(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_create_response(item) for item in value]
    return value


def get_process_status(
    props: dict[str, str], access_token: str, scope: engine.ImportScope, process_id: str
) -> dict[str, Any]:
    query = urllib.parse.urlencode({"onlyData": "true"})
    return http_json(
        props["restBaseUrl"].rstrip("/")
        + engine.process_resource(scope, process_id)
        + "?"
        + query,
        access_token=access_token, headers=request_headers(access_token),
    )


def get_result_items(
    props: dict[str, str], access_token: str, scope: engine.ImportScope, process_id: str
) -> list[dict[str, Any]]:
    query = urllib.parse.urlencode({"onlyData": "true", "limit": "25"})
    response = http_json(
        props["restBaseUrl"].rstrip("/")
        + engine.result_collection_resource(scope, process_id)
        + "?"
        + query,
        access_token=access_token, headers=request_headers(access_token),
    )
    items = response.get("items")
    return [item for item in items if isinstance(item, dict)] if isinstance(items, list) else []


def wait_for_result(
    props: dict[str, str],
    access_token: str,
    scope: engine.ImportScope,
    process_id: str,
    wait_seconds: int,
    poll_interval: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    deadline = time.time() + wait_seconds
    while True:
        process_status = get_process_status(props, access_token, scope, process_id)
        result_items = get_result_items(props, access_token, scope, process_id)
        completed_flag = process_status.get("ProcessCompletedFlag")
        current_status = engine.status_code(result_items)
        print(
            f"ProcessCompletedFlag: {completed_flag}; "
            f"StatusCode: {current_status or '(no result yet)'}; ResultCount: {len(result_items)}"
        )
        if engine.process_completed(completed_flag) or current_status in engine.TERMINAL_STATUS_CODES:
            return process_status, result_items
        if wait_seconds <= 0 or time.time() >= deadline:
            return process_status, result_items
        time.sleep(poll_interval)


def download_process_log(
    props: dict[str, str], access_token: str, scope: engine.ImportScope, process_id: str
) -> bytes:
    return http_bytes(
        props["restBaseUrl"].rstrip("/")
        + engine.enclosure_resource(scope, process_id, "ProcessLog"),
        access_token=access_token, headers=request_headers(access_token),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip-file", required=True, type=Path)
    parser.add_argument("--task-validation-envelope", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--properties", type=Path, default=DEFAULT_PROPERTIES)
    parser.add_argument("--token-cache")
    parser.add_argument("--wait-seconds", type=int, default=180)
    parser.add_argument("--poll-interval", type=int, default=15)
    parser.add_argument("--auth-code")
    parser.add_argument("--redirect-url")
    parser.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    parser.add_argument("--force-login", action="store_true")
    parser.add_argument("--no-open-browser", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.wait_seconds < 0 or args.poll_interval < 1:
        raise ValueError("wait-seconds must be nonnegative and poll-interval must be positive.")
    if not args.zip_file.is_file():
        raise FileNotFoundError(f"ZIP file does not exist: {args.zip_file}")
    validate_fsm_archive(args.zip_file)

    final_data = load_approved_final_data(
        args.task_validation_envelope,
        args.zip_file,
    )
    file_content_base64 = engine.read_zip_as_base64(args.zip_file)

    props = read_properties(args.properties)
    require_props(props, ["environment", "restBaseUrl"])
    if props["restBaseUrl"].rstrip("/") != str(final_data.get("targetEnvironment") or "").rstrip("/"):
        raise ValueError("Configured target environment does not match the approved targetEnvironment.")
    access_token = get_access_token(
        props,
        redirect_url=args.redirect_url,
        auth_code=args.auth_code,
        open_browser=not args.no_open_browser,
        callback_timeout=args.callback_timeout,
        token_cache=args.token_cache,
        force_login=args.force_login,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    response = create_import(
        props,
        access_token,
        file_content_base64,
    )
    create_response_path = args.output_dir / "manage-party-usages-import-create-response.json"
    create_response_path.write_text(
        json.dumps(redact_create_response(response), indent=2) + "\n",
        encoding="utf-8",
    )
    process_id = extract_process_id(response)
    if process_id is None:
        raise RuntimeError(
            "Fusion accepted the child-process create request without a usable ProcessId; "
            f"preserved the redacted response at {create_response_path}."
        )
    print(f"Started setup task CSV import process: {process_id}")

    metadata_path = args.output_dir / f"manage-party-usages-import-{process_id}.json"
    metadata_path.write_text(
        json.dumps(
            {
                "environment": props["environment"],
                "taskCode": TASK_CODE,
                "taskName": TASK_NAME,
                "zipFile": str(args.zip_file.resolve()),
                "archiveSha256": sha256_file(args.zip_file),
                "crossEnvironmentMigration": True,
                "processId": str(process_id),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    scope = engine.ImportScope("task", TASK_CODE)
    process_status, result_items = wait_for_result(
        props,
        access_token,
        scope,
        str(process_id),
        args.wait_seconds,
        args.poll_interval,
    )
    current_status = engine.status_code(result_items)
    completed = engine.process_completed(process_status.get("ProcessCompletedFlag"))
    if not completed and current_status not in engine.TERMINAL_STATUS_CODES:
        print("Import process is not complete yet.")
        print(f"TaskCode: {TASK_CODE}")
        print(f"ProcessId: {process_id}")
        print(f"StatusCode: {current_status or '(no result yet)'}")
        print(f"Wrote {metadata_path}")
        return 3

    process_log = download_process_log(
        props,
        access_token,
        scope,
        str(process_id),
    )
    log_path = args.output_dir / f"manage-party-usages-import-{process_id}-process.log"
    log_path.write_bytes(process_log)
    print(f"StatusCode: {current_status or '(unknown)'}")
    print(f"Wrote {metadata_path}")
    print(f"Wrote {log_path} ({len(process_log)} bytes)")
    return 4 if current_status in engine.ERROR_STATUS_CODES else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
