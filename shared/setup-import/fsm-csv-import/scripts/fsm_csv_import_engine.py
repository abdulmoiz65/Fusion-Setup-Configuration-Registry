#!/usr/bin/env python3
"""Shared Oracle Fusion FSM CSV import primitives."""

from __future__ import annotations

import base64
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fusion_skill_paths import FUSION_SKILLS_ROOT, add_auth_scripts_to_path

add_auth_scripts_to_path()

from fusion_auth import fusion_rest_get_bytes, fusion_rest_json, fusion_rest_post_json  # noqa: E402


SETUP_TASK_CSV_IMPORTS_RESOURCE = "/fscmRestApi/resources/11.13.18.05/setupTaskCSVImports"
SETUP_OFFERING_CSV_IMPORTS_RESOURCE = "/fscmRestApi/resources/11.13.18.05/setupOfferingCSVImports"
FEATURES_RESOURCE = "/fscmRestApi/resources/11.13.18.05/features"
FEATURE_CATALOG_PATHS = {
    "OFFERING": (
        FUSION_SKILLS_ROOT / "knowledge" / "setup-task-catalog" / "effective" / "Offerings_catalog.json",
    ),
    "FUNCTIONAL_AREA": (
        FUSION_SKILLS_ROOT / "knowledge" / "setup-task-catalog" / "effective" / "Functional_areas_catalog.json",
    ),
}

SUCCESS_STATUS_CODES = {"COMPLETED", "COMPLETED_WARNINGS"}
ERROR_STATUS_CODES = {"COMPLETED_ERRORS"}
TERMINAL_STATUS_CODES = SUCCESS_STATUS_CODES | ERROR_STATUS_CODES


@dataclass(frozen=True)
class ImportScope:
    kind: str
    primary_code: str
    functional_area_code: str | None = None

    @property
    def resource_root(self) -> str:
        if self.kind == "task":
            return SETUP_TASK_CSV_IMPORTS_RESOURCE
        if self.kind in {"offering", "functional-area"}:
            return SETUP_OFFERING_CSV_IMPORTS_RESOURCE
        raise ValueError(f"Unsupported import scope: {self.kind}")

    @property
    def process_child(self) -> str:
        if self.kind == "task":
            return "SetupTaskCSVImportProcess"
        if self.kind in {"offering", "functional-area"}:
            return "SetupOfferingCSVImportProcess"
        raise ValueError(f"Unsupported import scope: {self.kind}")

    @property
    def result_child(self) -> str:
        if self.kind == "task":
            return "SetupTaskCSVImportProcessResult"
        if self.kind in {"offering", "functional-area"}:
            return "SetupOfferingCSVImportProcessResult"
        raise ValueError(f"Unsupported import scope: {self.kind}")

    @property
    def import_label(self) -> str:
        if self.kind == "task":
            return "setup task CSV import"
        if self.kind == "functional-area":
            return "setup functional-area CSV import"
        if self.kind == "offering":
            return "setup offering CSV import"
        raise ValueError(f"Unsupported import scope: {self.kind}")


def slug(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")


def quote_query_value(value: str) -> str:
    return value.replace("'", "''")


def process_completed(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().casefold() in {"true", "y", "yes", "1"}
    if isinstance(value, int):
        return value != 0
    return False


def read_zip_as_base64(zip_file: Path) -> str:
    if not zip_file.exists():
        raise FileNotFoundError(f"ZIP file does not exist: {zip_file}")
    content = zip_file.read_bytes()
    if not content.startswith(b"PK\x03\x04"):
        raise ValueError(f"Expected a ZIP file starting with PK signature: {zip_file}")
    return base64.b64encode(content).decode("ascii")


def create_task_import(
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


def create_offering_import(
    props: dict[str, str],
    access_token: str,
    offering_code: str,
    file_content_base64: str,
    *,
    functional_area_code: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "OfferingCode": offering_code,
        "SetupOfferingCSVImportProcess": [
            {
                "OfferingCode": offering_code,
                "FileContent": file_content_base64,
            }
        ],
    }
    if functional_area_code:
        payload["FunctionalAreaCode"] = functional_area_code
    return fusion_rest_post_json(
        props,
        SETUP_OFFERING_CSV_IMPORTS_RESOURCE,
        access_token=access_token,
        json_body=payload,
    )


def create_import_process(
    props: dict[str, str],
    access_token: str,
    scope: ImportScope,
    file_content_base64: str,
) -> dict[str, Any]:
    if scope.kind == "task":
        return create_task_import(props, access_token, scope.primary_code, file_content_base64)
    return create_offering_import(
        props,
        access_token,
        scope.primary_code,
        file_content_base64,
        functional_area_code=scope.functional_area_code,
    )


def load_feature_catalog(feature_type: str) -> list[dict[str, Any]]:
    catalog_paths = FEATURE_CATALOG_PATHS.get(feature_type, ())
    items: list[dict[str, Any]] = []
    for catalog_path in catalog_paths:
        if not catalog_path.exists():
            continue
        data = json.loads(catalog_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            items.extend(item for item in data if isinstance(item, dict))
        elif isinstance(data, dict) and isinstance(data.get("items"), list):
            items.extend(item for item in data["items"] if isinstance(item, dict))
        else:
            raise RuntimeError(f"Could not find feature entries in {catalog_path}")
    return items


def find_local_feature_codes(
    feature_name: str,
    *,
    feature_type: str,
    limit: int = 25,
) -> list[dict[str, Any]]:
    feature_name_folded = feature_name.casefold()
    exact_matches: list[dict[str, Any]] = []
    contains_matches: list[dict[str, Any]] = []
    for item in load_feature_catalog(feature_type):
        if str(item.get("FeatureType", "")).casefold() != feature_type.casefold():
            continue
        name = str(item.get("FeatureName", ""))
        if not name or not item.get("FeatureCode"):
            continue
        name_folded = name.casefold()
        if name_folded == feature_name_folded:
            exact_matches.append(item)
        elif feature_name_folded in name_folded:
            contains_matches.append(item)
    return (exact_matches + contains_matches)[:limit]


def find_feature_codes(
    props: dict[str, str],
    access_token: str,
    feature_name: str,
    *,
    feature_type: str,
    limit: int = 25,
) -> list[dict[str, Any]]:
    response = fusion_rest_json(
        props,
        FEATURES_RESOURCE,
        access_token=access_token,
        query_params={
            "onlyData": "true",
            "fields": "FeatureName,FeatureCode,FeatureType",
            "q": f"FeatureType='{quote_query_value(feature_type)}';FeatureName LIKE '{quote_query_value(feature_name)}'",
            "limit": str(limit),
        },
    )
    items = response.get("items")
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, dict)]


def resolve_feature_code(
    props: dict[str, str],
    access_token: str,
    feature_name: str,
    *,
    feature_type: str,
    limit: int = 25,
) -> str:
    local_items = find_local_feature_codes(feature_name, feature_type=feature_type, limit=limit)
    if local_items:
        return select_feature_code(local_items, feature_name)
    return select_feature_code(
        find_feature_codes(props, access_token, feature_name, feature_type=feature_type, limit=limit),
        feature_name,
    )


def select_feature_code(items: list[dict[str, Any]], feature_name: str) -> str:
    if not items:
        raise RuntimeError(f"No feature matched {feature_name!r}.")
    exact = [
        item
        for item in items
        if str(item.get("FeatureName", "")).casefold() == feature_name.casefold()
        and item.get("FeatureCode")
    ]
    selected = exact[0] if exact else items[0]
    feature_code = selected.get("FeatureCode")
    if not feature_code:
        raise RuntimeError(f"Matched feature did not include FeatureCode: {selected}")
    return str(feature_code)


def extract_process_id(response: dict[str, Any], process_child: str) -> int | None:
    process_items = response.get(process_child)
    if not isinstance(process_items, list):
        return None
    for item in process_items:
        if isinstance(item, dict) and item.get("ProcessId") is not None:
            return int(item["ProcessId"])
    return None


def process_resource(scope: ImportScope, process_id: str) -> str:
    return f"{scope.resource_root}/{scope.primary_code}/child/{scope.process_child}/{process_id}"


def result_collection_resource(scope: ImportScope, process_id: str) -> str:
    return f"{process_resource(scope, process_id)}/child/{scope.result_child}"


def result_resource(scope: ImportScope, process_id: str) -> str:
    return f"{result_collection_resource(scope, process_id)}/{process_id}"


def enclosure_resource(scope: ImportScope, process_id: str, enclosure_name: str) -> str:
    return f"{result_resource(scope, process_id)}/enclosure/{enclosure_name}"


def get_process_status(
    props: dict[str, str],
    access_token: str,
    scope: ImportScope,
    process_id: str,
) -> dict[str, Any]:
    return fusion_rest_json(
        props,
        process_resource(scope, process_id),
        access_token=access_token,
        query_params={"onlyData": "true"},
    )


def get_result_items(
    props: dict[str, str],
    access_token: str,
    scope: ImportScope,
    process_id: str,
) -> list[dict[str, Any]]:
    response = fusion_rest_json(
        props,
        result_collection_resource(scope, process_id),
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
    scope: ImportScope,
    process_id: str,
    wait_seconds: int,
    poll_interval: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    deadline = time.time() + wait_seconds
    while True:
        process_status = get_process_status(props, access_token, scope, process_id)
        result_items = get_result_items(props, access_token, scope, process_id)
        completed_flag = process_status.get("ProcessCompletedFlag")
        completed = process_completed(completed_flag)
        current_status = status_code(result_items)
        print(
            f"ProcessCompletedFlag: {completed_flag}; "
            f"StatusCode: {current_status or '(no result yet)'}; ResultCount: {len(result_items)}"
        )
        if completed or current_status in TERMINAL_STATUS_CODES:
            return process_status, result_items
        if wait_seconds <= 0 or time.time() >= deadline:
            return process_status, result_items
        time.sleep(poll_interval)


def download_process_log(
    props: dict[str, str],
    access_token: str,
    scope: ImportScope,
    process_id: str,
) -> bytes:
    return fusion_rest_get_bytes(
        props,
        enclosure_resource(scope, process_id, "ProcessLog"),
        access_token=access_token,
    )
