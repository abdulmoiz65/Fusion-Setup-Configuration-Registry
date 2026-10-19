#!/usr/bin/env python3
"""Import the fixed Manage Additional Identifier Types FSM package after approval."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET
import zipfile


def repository_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "core" / "data-loader").is_dir() and (candidate / "shared" / "setup-import" / "fsm-csv-import").is_dir():
            return candidate
    raise RuntimeError("Could not locate the FDOS repository root.")


ROOT = repository_root()
for directory in (
    ROOT / "shared" / "setup-import" / "fsm-csv-import" / "scripts",
    ROOT / "core" / "auth" / "fusion-oauth-authentication" / "scripts",
    ROOT / "core" / "data-loader" / "task-validator" / "scripts",
):
    sys.path.insert(0, str(directory))

import fsm_csv_import_engine as engine  # noqa: E402
from fusion_auth import DEFAULT_CALLBACK_TIMEOUT_SECONDS, get_access_token, http_bytes, http_json, read_properties, require_props  # noqa: E402
from task_rule_execution import approved_loader_payload  # noqa: E402


TASK_CODE = "HZ_MANAGE_ADDITIONAL_IDENTIFIER_TYPES"
TASK_NAME = "Manage Additional Identifier Types"
EXECUTION_ADAPTER = "cx.customer-data-management.trading-community-foundation.manage-additional-identifier-types.native-fsm-import"
DEFAULT_PROPERTIES = ROOT / "core" / "auth" / "fusionEnv.properties"
CREATE_RESOURCE = f"{engine.SETUP_TASK_CSV_IMPORTS_RESOURCE}/{TASK_CODE}/child/SetupTaskCSVImportProcess"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_fsm_archive(path: Path) -> None:
    if not zipfile.is_zipfile(path):
        raise ValueError("The supplied package is not a valid ZIP archive.")
    with zipfile.ZipFile(path) as archive:
        members = [member for member in archive.infolist() if not member.is_dir() and member.filename.rsplit("/", 1)[-1] == "ASM_SETUP_CSV_METADATA.xml"]
        if len(members) != 1:
            raise ValueError("FSM ZIP must contain exactly one ASM_SETUP_CSV_METADATA.xml member.")
        try:
            metadata = ET.fromstring(archive.read(members[0]))
        except ET.ParseError as error:
            raise ValueError("ASM_SETUP_CSV_METADATA.xml is not valid XML.") from error
    codes = [(element.text or "").strip() for element in metadata.iter() if element.tag.rsplit("}", 1)[-1] == "ObjectShortName" and (element.text or "").strip()]
    if codes != [TASK_CODE]:
        raise ValueError(f"FSM metadata must contain exactly one ObjectShortName equal to {TASK_CODE}.")


def load_approved_final_data(envelope_path: Path, zip_file: Path) -> dict[str, Any]:
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    payload = approved_loader_payload(envelope.get("preview"), envelope.get("approval"))
    if payload.get("taskCode") != TASK_CODE or payload.get("taskName") != TASK_NAME:
        raise ValueError("Task Hook approval does not match Manage Additional Identifier Types.")
    final_data = payload.get("finalData")
    if not isinstance(final_data, dict):
        raise ValueError("Task Hook approval does not contain finalData.")
    required = {
        "executionRoute": "data-loader",
        "executionAdapter": EXECUTION_ADAPTER,
        "packageType": "FSM",
        "taskCode": TASK_CODE,
        "taskName": TASK_NAME,
    }
    for field, expected in required.items():
        if final_data.get(field) != expected:
            raise ValueError(f"Approved {field} does not match this native FSM adapter.")
    approved_path = Path(str(final_data.get("absoluteZipPath") or "")).expanduser().resolve()
    if approved_path != zip_file.expanduser().resolve():
        raise ValueError("Approved ZIP path does not match the supplied ZIP path.")
    if str(final_data.get("archiveSha256") or "").lower() != sha256_file(zip_file):
        raise ValueError("Approved archive SHA-256 does not match the supplied ZIP bytes.")
    return final_data


def headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}", "REST-Framework-Version": "9"}


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: "<redacted>" if key == "FileContent" else redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


def create_process(props: dict[str, str], token: str, file_content: str) -> dict[str, Any]:
    return http_json(
        props["restBaseUrl"].rstrip("/") + CREATE_RESOURCE,
        method="POST",
        json_body={"TaskCode": TASK_CODE, "FileContent": file_content, "SourceTargetDiffOkFlag": "Y"},
        access_token=token, headers=headers(token),
    )


def wait_for_result(props: dict[str, str], token: str, scope: engine.ImportScope, identifier: str, wait_seconds: int, poll_interval: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    deadline = time.time() + wait_seconds
    while True:
        status = http_json(
            props["restBaseUrl"].rstrip("/") + engine.process_resource(scope, identifier) + "?" + urllib.parse.urlencode({"onlyData": "true"}),
            access_token=token, headers=headers(token),
        )
        result = http_json(
            props["restBaseUrl"].rstrip("/") + engine.result_collection_resource(scope, identifier) + "?" + urllib.parse.urlencode({"onlyData": "true", "limit": "25"}),
            access_token=token, headers=headers(token),
        )
        items = [item for item in result.get("items", []) if isinstance(item, dict)]
        if engine.process_completed(status.get("ProcessCompletedFlag")) or engine.status_code(items) in engine.TERMINAL_STATUS_CODES:
            return status, items
        if wait_seconds <= 0 or time.time() >= deadline:
            return status, items
        time.sleep(poll_interval)


def process_id(response: dict[str, Any]) -> int | None:
    try:
        return int(response["ProcessId"])
    except (KeyError, TypeError, ValueError):
        return engine.extract_process_id(response, "SetupTaskCSVImportProcess")


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
    final_data = load_approved_final_data(args.task_validation_envelope, args.zip_file)
    props = read_properties(args.properties)
    require_props(props, ["environment", "restBaseUrl"])
    if props["restBaseUrl"].rstrip("/") != str(final_data.get("targetEnvironment") or "").rstrip("/"):
        raise ValueError("Configured target environment does not match the approved targetEnvironment.")
    token = get_access_token(props, redirect_url=args.redirect_url, auth_code=args.auth_code, open_browser=not args.no_open_browser, callback_timeout=args.callback_timeout, token_cache=args.token_cache, force_login=args.force_login)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    response = create_process(props, token, engine.read_zip_as_base64(args.zip_file))
    response_path = args.output_dir / "manage-additional-identifier-types-import-create-response.json"
    response_path.write_text(json.dumps(redact(response), indent=2) + "\n", encoding="utf-8")
    identifier = process_id(response)
    if identifier is None:
        raise RuntimeError(f"Fusion accepted the import without a usable ProcessId; preserved the redacted response at {response_path}.")
    scope = engine.ImportScope("task", TASK_CODE)
    status, results = wait_for_result(props, token, scope, str(identifier), args.wait_seconds, args.poll_interval)
    metadata_path = args.output_dir / f"manage-additional-identifier-types-import-{identifier}.json"
    metadata_path.write_text(json.dumps({"environment": props["environment"], "taskCode": TASK_CODE, "taskName": TASK_NAME, "zipFile": str(args.zip_file.resolve()), "archiveSha256": sha256_file(args.zip_file), "processId": str(identifier)}, indent=2) + "\n", encoding="utf-8")
    if not engine.process_completed(status.get("ProcessCompletedFlag")) and engine.status_code(results) not in engine.TERMINAL_STATUS_CODES:
        print(f"Import process is not complete yet. TaskCode: {TASK_CODE}; ProcessId: {identifier}; Wrote {metadata_path}")
        return 3
    log = http_bytes(props["restBaseUrl"].rstrip("/") + engine.enclosure_resource(scope, str(identifier), "ProcessLog"), access_token=token, headers=headers(token))
    log_path = args.output_dir / f"manage-additional-identifier-types-import-{identifier}-process.log"
    log_path.write_bytes(log)
    print(f"Started setup task CSV import process: {identifier}")
    print(f"Wrote {metadata_path}")
    print(f"Wrote {log_path} ({len(log)} bytes)")
    return 4 if engine.status_code(results) in engine.ERROR_STATUS_CODES else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
