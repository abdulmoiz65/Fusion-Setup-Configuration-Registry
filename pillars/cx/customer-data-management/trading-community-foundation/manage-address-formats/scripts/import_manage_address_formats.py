#!/usr/bin/env python3
"""Import the approved Manage Address Formats FSM archive with one safe revision fallback."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.parse
import xml.etree.ElementTree as element_tree
import zipfile
from pathlib import Path
from typing import Any


def repository_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "core" / "auth").is_dir() and (candidate / "shared" / "setup-import").is_dir():
            return candidate
    raise RuntimeError("Could not locate the FSCR repository root.")


ROOT = repository_root()
for folder in (
    ROOT / "core" / "auth" / "fusion-oauth-authentication" / "scripts",
    ROOT / "core" / "data-loader" / "task-validator" / "scripts",
    ROOT / "shared" / "setup-import" / "fsm-csv-import" / "scripts",
):
    sys.path.insert(0, str(folder))

from fusion_auth import (  # noqa: E402
    DEFAULT_CALLBACK_TIMEOUT_SECONDS, FusionHttpError, get_access_token, http_bytes,
    http_json, read_properties, require_props,
)
from task_rule_execution import approved_loader_payload  # noqa: E402
import fsm_csv_import_engine as engine  # noqa: E402


TASK_CODE = "HZ_MANAGE_ADDRESS_FORMATS"
TASK_NAME = "Manage Address Formats"
SKILL_PATH = "pillars/cx/customer-data-management/trading-community-foundation/manage-address-formats/SKILL.md"
EXECUTION_ADAPTER = "cx.customer-data-management.trading-community-foundation.manage-address-formats.native-fsm-import"
CREATE_RESOURCE = "/fscmRestApi/resources/11.13.18.05/setupTaskCSVImports"
DEFAULT_PROPERTIES = ROOT / "core" / "auth" / "fusionEnv.properties"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_archive(path: Path) -> None:
    if not zipfile.is_zipfile(path):
        raise ValueError("The supplied package is not a valid ZIP archive.")
    with zipfile.ZipFile(path) as archive:
        members = [item for item in archive.infolist() if not item.is_dir() and item.filename.rsplit("/", 1)[-1] == "ASM_SETUP_CSV_METADATA.xml"]
        if len(members) != 1:
            raise ValueError("FSM ZIP must contain exactly one ASM_SETUP_CSV_METADATA.xml member.")
        root = element_tree.fromstring(archive.read(members[0]))
    names = [(node.text or "").strip() for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "ObjectShortName" and (node.text or "").strip()]
    if names != [TASK_CODE]:
        raise ValueError(f"FSM metadata must contain exactly one ObjectShortName equal to {TASK_CODE}.")


def load_approved_final_data(envelope_path: Path, zip_file: Path) -> dict[str, Any]:
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    payload = approved_loader_payload(envelope.get("preview"), envelope.get("approval"))
    final_data = payload.get("finalData")
    if payload.get("taskCode") != TASK_CODE or payload.get("taskName") != TASK_NAME or payload.get("skillPath") != SKILL_PATH:
        raise ValueError("Task Hook approval does not match Manage Address Formats.")
    if not isinstance(final_data, dict):
        raise ValueError("Task Hook approval does not contain finalData.")
    expected = {"executionRoute": "data-loader", "executionAdapter": EXECUTION_ADAPTER, "packageType": "FSM", "wholeTask": True, "taskCode": TASK_CODE, "taskName": TASK_NAME}
    if any(final_data.get(key) != value for key, value in expected.items()):
        raise ValueError("Task Hook approval does not bind the required Manage Address Formats import contract.")
    if Path(str(final_data.get("absoluteZipPath") or "")).expanduser().resolve() != zip_file.expanduser().resolve():
        raise ValueError("Approved ZIP path does not match the supplied ZIP path.")
    if str(final_data.get("archiveSha256") or "").lower() != sha256_file(zip_file):
        raise ValueError("Approved archive SHA-256 does not match the supplied ZIP bytes.")
    return final_data


def headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}", "REST-Framework-Version": "9"}


def create_import(props: dict[str, str], token: str, content: str, diff_ok: str) -> dict[str, Any]:
    return http_json(props["restBaseUrl"].rstrip("/") + CREATE_RESOURCE, method="POST", json_body={
        "TaskCode": TASK_CODE,
        "SetupTaskCSVImportProcess": [{"TaskCode": TASK_CODE, "FileContent": content, "SourceTargetDiffOkFlag": diff_ok}],
    }, access_token=token, headers=headers(token))


def extract_process_id(response: dict[str, Any]) -> int | None:
    child = response.get("SetupTaskCSVImportProcess")
    if isinstance(child, dict):
        items = child.get("items")
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and item.get("ProcessId") is not None:
                    try:
                        return int(item["ProcessId"])
                    except (TypeError, ValueError):
                        pass
    return engine.extract_process_id(response, "SetupTaskCSVImportProcess")


def exact_revision_mismatch(error: FusionHttpError) -> bool:
    message = error.body.casefold()
    return error.status_code == 400 and all(word in message for word in ("source", "target", "revision")) and ("mismatch" in message or "difference" in message)


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: "<redacted>" if key == "FileContent" else redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


def get_status(props: dict[str, str], token: str, process_id: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    scope = engine.ImportScope("task", TASK_CODE)
    base = props["restBaseUrl"].rstrip("/")
    status = http_json(base + engine.process_resource(scope, process_id) + "?" + urllib.parse.urlencode({"onlyData": "true"}), access_token=token, headers=headers(token))
    results = http_json(base + engine.result_collection_resource(scope, process_id) + "?" + urllib.parse.urlencode({"onlyData": "true", "limit": "25"}), access_token=token, headers=headers(token)).get("items", [])
    return status, [item for item in results if isinstance(item, dict)] if isinstance(results, list) else []


def poll(props: dict[str, str], token: str, process_id: str, wait_seconds: int, poll_interval: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    deadline = time.time() + wait_seconds
    while True:
        status, results = get_status(props, token, process_id)
        code = engine.status_code(results)
        print(f"ProcessCompletedFlag: {status.get('ProcessCompletedFlag')}; StatusCode: {code or '(no result yet)'}; ResultCount: {len(results)}")
        if engine.process_completed(status.get("ProcessCompletedFlag")) or code in engine.TERMINAL_STATUS_CODES or time.time() >= deadline:
            return status, results
        time.sleep(poll_interval)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip-file", required=True, type=Path)
    parser.add_argument("--task-validation-envelope", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--properties", type=Path, default=DEFAULT_PROPERTIES)
    parser.add_argument("--token-cache")
    parser.add_argument("--wait-seconds", type=int, default=180)
    parser.add_argument("--poll-interval", type=int, default=15)
    parser.add_argument("--no-open-browser", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.wait_seconds < 0 or args.poll_interval < 1:
        raise ValueError("wait-seconds must be nonnegative and poll-interval must be positive.")
    validate_archive(args.zip_file)
    final_data = load_approved_final_data(args.task_validation_envelope, args.zip_file)
    props = read_properties(args.properties)
    require_props(props, ["environment", "restBaseUrl"])
    if props["restBaseUrl"].rstrip("/") != str(final_data.get("targetEnvironment") or "").rstrip("/"):
        raise ValueError("Configured target environment does not match the approved targetEnvironment.")
    token = get_access_token(props, token_cache=args.token_cache, open_browser=not args.no_open_browser)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    content = engine.read_zip_as_base64(args.zip_file)
    fallback_used = False
    try:
        response = create_import(props, token, content, "N")
    except FusionHttpError as error:
        if not exact_revision_mismatch(error):
            raise
        fallback_used = True
        response = create_import(props, token, content, "Y")
    (args.output_dir / "manage-address-formats-import-create-response.json").write_text(json.dumps(redact(response), indent=2) + "\n", encoding="utf-8")
    process_id = extract_process_id(response)
    if process_id is None:
        raise RuntimeError("Fusion accepted the import request without a usable ProcessId; no retry was attempted.")
    print(f"Started setup task CSV import process: {process_id}")
    metadata = {"environment": props["environment"], "taskCode": TASK_CODE, "taskName": TASK_NAME, "zipFile": str(args.zip_file.resolve()), "archiveSha256": sha256_file(args.zip_file), "processId": str(process_id), "revisionMismatchFallback": "applied once" if fallback_used else "not needed"}
    (args.output_dir / f"manage-address-formats-import-{process_id}.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    status, results = poll(props, token, str(process_id), args.wait_seconds, args.poll_interval)
    code = engine.status_code(results)
    if not engine.process_completed(status.get("ProcessCompletedFlag")) and code not in engine.TERMINAL_STATUS_CODES:
        print(f"Import process is not complete yet. ProcessId: {process_id}; StatusCode: {code or '(no result yet)'}")
        return 3
    scope = engine.ImportScope("task", TASK_CODE)
    log = http_bytes(props["restBaseUrl"].rstrip("/") + engine.enclosure_resource(scope, str(process_id), "ProcessLog"), access_token=token, headers=headers(token))
    log_path = args.output_dir / f"manage-address-formats-import-{process_id}-process.log"
    log_path.write_bytes(log)
    print(f"StatusCode: {code or '(unknown)'}")
    print(f"Wrote {log_path}")
    return 4 if code in engine.ERROR_STATUS_CODES else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
