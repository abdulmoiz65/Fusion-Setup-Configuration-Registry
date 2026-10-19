#!/usr/bin/env python3
"""Shared Oracle Fusion FSM CSV export primitives."""

from __future__ import annotations

import base64
import binascii
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fusion_skill_paths import FUSION_SKILLS_ROOT, add_auth_scripts_to_path

add_auth_scripts_to_path()

from fusion_auth import fusion_rest_get_bytes, fusion_rest_json, fusion_rest_post_json  # noqa: E402


SETUP_TASK_CSV_EXPORTS_RESOURCE = "/fscmRestApi/resources/11.13.18.05/setupTaskCSVExports"
SETUP_TASK_CSV_TEMPLATE_EXPORTS_RESOURCE = "/fscmRestApi/resources/11.13.18.05/setupTaskCSVTemplateExports"
SETUP_OFFERING_CSV_EXPORTS_RESOURCE = "/fscmRestApi/resources/11.13.18.05/setupOfferingCSVExports"
SETUP_OFFERING_CSV_TEMPLATE_EXPORTS_RESOURCE = "/fscmRestApi/resources/11.13.18.05/setupOfferingCSVTemplateExports"
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
TASK_EXPORT_CRITERIA_FIELDS = {
    "TaskCode",
    "BusinessObjectCode",
    "AttributeSet",
    "AttributeName",
    "AttributeValue",
    "ProcessId",
}


@dataclass(frozen=True)
class ExportScope:
    kind: str
    primary_code: str
    functional_area_code: str | None = None
    template_only: bool = False

    @property
    def resource_root(self) -> str:
        if self.kind == "task":
            if self.template_only:
                return SETUP_TASK_CSV_TEMPLATE_EXPORTS_RESOURCE
            return SETUP_TASK_CSV_EXPORTS_RESOURCE
        if self.kind in {"offering", "functional-area"}:
            if self.template_only:
                return SETUP_OFFERING_CSV_TEMPLATE_EXPORTS_RESOURCE
            return SETUP_OFFERING_CSV_EXPORTS_RESOURCE
        raise ValueError(f"Unsupported export scope: {self.kind}")

    @property
    def process_child(self) -> str:
        if self.kind == "task":
            if self.template_only:
                return "SetupTaskCSVTemplateExportProcess"
            return "SetupTaskCSVExportProcess"
        if self.kind in {"offering", "functional-area"}:
            if self.template_only:
                return "SetupOfferingCSVTemplateExportProcess"
            return "SetupOfferingCSVExportProcess"
        raise ValueError(f"Unsupported export scope: {self.kind}")

    @property
    def result_child(self) -> str:
        if self.kind == "task":
            if self.template_only:
                return "SetupTaskCSVTemplateExportProcessResult"
            return "SetupTaskCSVExportProcessResult"
        if self.kind in {"offering", "functional-area"}:
            if self.template_only:
                return "SetupOfferingCSVTemplateExportProcessResult"
            return "SetupOfferingCSVExportProcessResult"
        raise ValueError(f"Unsupported export scope: {self.kind}")

    @property
    def code_field(self) -> str:
        if self.kind == "task":
            return "TaskCode"
        if self.kind in {"offering", "functional-area"}:
            return "OfferingCode"
        raise ValueError(f"Unsupported export scope: {self.kind}")

    @property
    def export_label(self) -> str:
        return "CSV template export" if self.template_only else "CSV export"


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


def decode_file_content(raw_content: bytes) -> bytes:
    if raw_content.startswith(b"PK\x03\x04"):
        return raw_content
    normalized = b"".join(raw_content.split())
    try:
        return base64.b64decode(normalized, validate=True)
    except binascii.Error:
        return raw_content


def normalize_task_export_criteria(
    criteria: list[dict[str, Any]] | None,
    task_code: str,
) -> list[dict[str, Any]]:
    """Validate task export criteria and bind each entry to its parent task."""
    if criteria is None:
        return []
    if not isinstance(criteria, list):
        raise ValueError("SetupTaskCSVExportCriteria must be a JSON array.")
    if not criteria:
        return []

    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(criteria, 1):
        if not isinstance(item, dict):
            raise ValueError(f"SetupTaskCSVExportCriteria item {index} must be a JSON object.")
        unknown_fields = set(item) - TASK_EXPORT_CRITERIA_FIELDS
        if unknown_fields:
            raise ValueError(
                "SetupTaskCSVExportCriteria item "
                f"{index} contains unsupported field(s): {', '.join(sorted(unknown_fields))}."
            )
        criterion = dict(item)
        criterion_task_code = criterion.get("TaskCode")
        if criterion_task_code is not None and str(criterion_task_code).casefold() != task_code.casefold():
            raise ValueError(
                f"SetupTaskCSVExportCriteria item {index} TaskCode {criterion_task_code!r} "
                f"does not match selected task code {task_code!r}."
            )
        criterion["TaskCode"] = task_code
        normalized.append(criterion)
    return normalized


def create_task_export(
    props: dict[str, str],
    access_token: str,
    task_code: str,
    *,
    criteria: list[dict[str, Any]] | None = None,
    template_only: bool = False,
) -> dict[str, Any]:
    if criteria and template_only:
        raise ValueError("SetupTaskCSVExportCriteria is supported only for setup task data exports, not template/spec exports.")
    scope = ExportScope(kind="task", primary_code=task_code, template_only=template_only)
    normalized_criteria = normalize_task_export_criteria(criteria, task_code)
    payload = {"TaskCode": task_code}
    if normalized_criteria:
        payload["SetupTaskCSVExportCriteria"] = normalized_criteria
    payload[scope.process_child] = [{"TaskCode": task_code}]
    return fusion_rest_post_json(
        props,
        scope.resource_root,
        access_token=access_token,
        json_body=payload,
    )


def create_offering_export(
    props: dict[str, str],
    access_token: str,
    offering_code: str,
    *,
    functional_area_code: str | None = None,
    criteria: list[dict[str, Any]] | None = None,
    template_only: bool = False,
) -> dict[str, Any]:
    scope = ExportScope(
        kind="functional-area" if functional_area_code else "offering",
        primary_code=offering_code,
        functional_area_code=functional_area_code,
        template_only=template_only,
    )
    payload: dict[str, Any] = {
        "OfferingCode": offering_code,
        scope.process_child: [{"OfferingCode": offering_code}],
    }
    if functional_area_code:
        payload["FunctionalAreaCode"] = functional_area_code
    if criteria:
        payload["SetupOfferingCSVExportCriteria"] = criteria
    return fusion_rest_post_json(
        props,
        scope.resource_root,
        access_token=access_token,
        json_body=payload,
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
    matches = exact_matches + contains_matches
    return matches[:limit]


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


def create_export_process(
    props: dict[str, str],
    access_token: str,
    scope: ExportScope,
    *,
    task_export_criteria: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if scope.kind == "task":
        return create_task_export(
            props,
            access_token,
            scope.primary_code,
            criteria=task_export_criteria,
            template_only=scope.template_only,
        )
    if task_export_criteria:
        raise ValueError("SetupTaskCSVExportCriteria is supported only for task-scoped exports.")
    return create_offering_export(
        props,
        access_token,
        scope.primary_code,
        functional_area_code=scope.functional_area_code,
        template_only=scope.template_only,
    )


def process_resource(scope: ExportScope, process_id: str) -> str:
    return f"{scope.resource_root}/{scope.primary_code}/child/{scope.process_child}/{process_id}"


def result_collection_resource(scope: ExportScope, process_id: str) -> str:
    return f"{process_resource(scope, process_id)}/child/{scope.result_child}"


def result_resource(scope: ExportScope, process_id: str) -> str:
    return f"{result_collection_resource(scope, process_id)}/{process_id}"


def enclosure_resource(scope: ExportScope, process_id: str, enclosure_name: str) -> str:
    return f"{result_resource(scope, process_id)}/enclosure/{enclosure_name}"


def get_process_status(
    props: dict[str, str],
    access_token: str,
    scope: ExportScope,
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
    scope: ExportScope,
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
    scope: ExportScope,
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


def download_result(
    props: dict[str, str],
    access_token: str,
    scope: ExportScope,
    process_id: str,
    *,
    download_log: bool = False,
) -> tuple[bytes, str]:
    enclosure_name = "ProcessLog" if download_log else "FileContent"
    raw_content = fusion_rest_get_bytes(
        props,
        enclosure_resource(scope, process_id, enclosure_name),
        access_token=access_token,
    )
    if download_log:
        return raw_content, enclosure_name
    return decode_file_content(raw_content), enclosure_name


def write_export_artifact(
    props: dict[str, str],
    scope: ExportScope,
    process_id: str,
    content: bytes,
    *,
    output_dir: Path,
    is_log: bool,
) -> Path:
    suffix = "process_log.txt" if is_log else "zip"
    export_type = "csv_template_export" if scope.template_only else "csv_export"
    if scope.kind == "task":
        name = f"{props['environment']}_setup_task_{export_type}_{slug(scope.primary_code)}_{process_id}.{suffix}"
    else:
        area_part = f"_{slug(scope.functional_area_code)}" if scope.functional_area_code else ""
        name = f"{props['environment']}_setup_offering_{export_type}_{slug(scope.primary_code)}{area_part}_{process_id}.{suffix}"
    output_path = output_dir / name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(content)
    return output_path
