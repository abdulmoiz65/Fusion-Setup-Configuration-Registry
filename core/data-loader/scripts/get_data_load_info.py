#!/usr/bin/env python3
"""Query Fusion dataLoaderDataSets and dataSetErrors for an initiation request."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Callable

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from upload_and_initiate import (
    DEFAULT_CONFIG,
    DataLoadError,
    get_json,
    post_json,
    read_config,
)
import data_loader_report
import data_loader_metadata as metadata


DATA_SETS_PATH = "/hcmRestApi/resources/latest/dataLoaderDataSets"
DATA_SET_ERRORS_PATH = "/hcmRestApi/resources/latest/dataSetErrors"
FAILED_LINES_PATH = DATA_SETS_PATH + "/{data_set_id}/child/failedLines"
DATA_SET_ALL_OBJECTS_PATH = DATA_SETS_PATH + "/{data_set_id}/child/dataSetAllObjects"
FBDI_PROCESS_HIERARCHY_PATH = (
    DATA_SETS_PATH + "/{data_set_id}/action/reviewProcessHierarchy"
)
FBDI_PROCESS_PATH = DATA_SETS_PATH + "/{data_set_id}/child/processes/{process_id}"
FBDI_PROCESS_LOG_PATH = (
    FBDI_PROCESS_PATH
    + "/child/processLogs/{attachment_document_id}/enclosure/FileContents"
)
FAILED_LINES_QUERY = {
    "fields": "UIName,FileLine,Message,MessageText,MessageUserDetails",
    "finder": "findByBusinessObject",
    "q": "MessageText!='-1'",
    "onlyData": "true",
}
DATA_SET_ALL_OBJECTS_QUERY = {
    "fields": "BusObjFileDiscriminator,UIUserKey,Message,MessageText,MessageUserDetails",
    "finder": "findErrorMessageDetails",
    "q": (
        "OriginatingProcess in ('LOAD','VALIDATION','ORA_ROLLBACK') "
        "and MessageText != '-1'"
    ),
    "onlyData": "true",
}
FSM_PROCESS_LOG_PATH = (
    "/fscmRestApi/resources/latest/setupTaskCSVImports/{task_code}"
    "/child/SetupTaskCSVImportProcess/{request_id}"
    "/child/SetupTaskCSVImportProcessResult/{request_id}/enclosure/ProcessLog"
)
PAGE_LIMIT = 500
UCM_CONTENT_ID_PATTERN = re.compile(r"UCMFA[0-9]+")
FSM_SOURCE_TYPE = "FSM"
FBDI_SOURCE_TYPE = "FBDI"
CX_IMPORT_SOURCE_TYPE = "ORA_CX_IMPORT"
FSM_TASK_CODE_PATTERN = re.compile(r"[A-Za-z0-9_]+")
DEFAULT_DIAGNOSTIC_LOG_ROOT = Path.home() / ".codex" / "data-loader-status-logs"

Getter = Callable[..., Any]
Poster = Callable[..., Any]


def _positive_integer(value: str | int, label: str) -> str:
    rendered = str(value).strip()
    if not rendered.isdigit() or int(rendered) <= 0:
        raise DataLoadError("status-input", f"{label} must be a positive integer.")
    return rendered


def _data_set_lookup(value: str | int) -> tuple[str, str, str]:
    rendered = str(value).strip()
    if rendered.isdigit():
        request_id = _positive_integer(rendered, "Request ID")
        return "RequestId", request_id, f"DataSetRequestId={request_id}"
    if UCM_CONTENT_ID_PATTERN.fullmatch(rendered):
        return "UcmContentId", rendered, f"UcmContentId='{rendered}'"
    raise DataLoadError(
        "status-input",
        "Provide a positive initiation Request ID or a UCM Content ID in the form UCMFA followed by digits.",
    )


def _default_diagnostic_log_output_dir(identifier: str | int) -> Path:
    """Return the durable Codex-managed diagnostics directory for one lookup."""
    lookup_field, lookup_value, _ = _data_set_lookup(identifier)
    return DEFAULT_DIAGNOSTIC_LOG_ROOT / f"{lookup_field.lower()}-{lookup_value}"


def _get_all_items(
    path: str,
    query_filter: str,
    config: dict[str, str],
    *,
    stage: str,
    getter: Getter = get_json,
) -> list[dict[str, Any]]:
    return _get_all_items_with_params(
        path,
        {"q": query_filter, "onlyData": "true"},
        config,
        stage=stage,
        getter=getter,
    )


def _get_all_items_with_params(
    path: str,
    query_params: dict[str, str],
    config: dict[str, str],
    *,
    stage: str,
    getter: Getter = get_json,
) -> list[dict[str, Any]]:
    offset = 0
    collected: list[dict[str, Any]] = []

    while True:
        query = urllib.parse.urlencode(
            {**query_params, "limit": str(PAGE_LIMIT), "offset": str(offset)}
        )
        response = getter(
            config["host"] + path + "?" + query,
            config["auth"],
            stage=stage,
        )
        if not isinstance(response, dict):
            raise DataLoadError(stage, "Endpoint returned a malformed response object.")
        items = response.get("items")
        has_more = response.get("hasMore")
        if not isinstance(items, list) or not isinstance(has_more, bool):
            raise DataLoadError(
                stage,
                "Endpoint response must contain an items array and boolean hasMore value.",
                response={"offset": offset},
            )
        for item in items:
            if not isinstance(item, dict):
                raise DataLoadError(stage, "Endpoint returned a non-object item.")
            collected.append(item)
        if not has_more:
            return collected
        if not items:
            raise DataLoadError(
                stage,
                "Endpoint pagination did not advance.",
                response={"offset": offset},
            )
        offset += len(items)


def _fsm_process_log_url(data_set: dict[str, Any], host: str) -> tuple[str, str, str]:
    """Build the current FSM ProcessLog URL from a resolved data-set item."""
    task_code = str(data_set.get("FsmTaskCode") or "").strip()
    request_id = str(data_set.get("FsmMigRequestId") or "").strip()
    if not FSM_TASK_CODE_PATTERN.fullmatch(task_code):
        raise DataLoadError(
            "fsm-process-log",
            "FSM data set did not contain a valid FsmTaskCode for ProcessLog retrieval.",
        )
    request_id = _positive_integer(request_id, "FsmMigRequestId")
    return (
        host.rstrip("/")
        + FSM_PROCESS_LOG_PATH.format(task_code=task_code, request_id=request_id),
        task_code,
        request_id,
    )


def _data_set_name(data_set: dict[str, Any], index: int) -> str:
    return str(
        data_set.get("DataSetName")
        or data_set.get("UIName")
        or data_set.get("BusinessObject")
        or f"data-set-{index}"
    )


def _safe_process_log_name(data_set_name: str, request_id: str, index: int) -> str:
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", data_set_name).strip(".-")
    return f"{stem or 'fsm-data-set'}-fsm-{request_id}-{index}.log"


def _safe_non_fsm_error_log_name(data_set_name: str, index: int) -> str:
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", data_set_name).strip(".-")
    return f"{stem or 'data-set'}-errors-{index}.log"


def _safe_fbdi_process_log_name(
    data_set_name: str, process_name: str, index: int
) -> str:
    data_set_stem = re.sub(r"[^A-Za-z0-9._-]+", "-", data_set_name).strip(".-")
    process_stem = re.sub(r"[^A-Za-z0-9._-]+", "-", process_name).strip(".-")
    return (
        f"{data_set_stem or 'fbdi-data-set'}-fbdi-"
        f"{process_stem or 'ess-process'}-{index}.log"
    )


def _fbdi_process_label(process_name: Any) -> str:
    rendered = str(process_name or "").strip()
    return {
        "ORA_FBDI_IMPORT": "FBDI Import",
        "ORA_FBDI_LOAD": "FBDI Load",
    }.get(rendered, rendered or "ESS process")


def _safe_cx_import_error_log_name(data_set_name: str, index: int) -> str:
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", data_set_name).strip(".-")
    return f"{stem or 'cx-import-data-set'}-cx-import-errors-{index}.log"


def _cx_import_business_objects_path(data_set_id: str) -> str:
    return DATA_SETS_PATH + f"/{data_set_id}/child/cxImportBusinessObjects"


def _cx_import_error_self_path(value: Any, config: dict[str, str]) -> str:
    if not isinstance(value, dict):
        raise DataLoadError("cx-import-errors", "CX Import error details were malformed.")
    links = value.get("links")
    if not isinstance(links, list):
        raise DataLoadError("cx-import-errors", "CX Import error details did not include a self link.")
    href = next(
        (
            item.get("href")
            for item in links
            if isinstance(item, dict) and item.get("rel") == "self" and item.get("href")
        ),
        None,
    )
    if not isinstance(href, str):
        raise DataLoadError("cx-import-errors", "CX Import error details did not include a self link.")
    parsed = urllib.parse.urlsplit(href)
    configured = urllib.parse.urlsplit(config["host"])
    if parsed.netloc and (parsed.scheme, parsed.netloc) != (
        configured.scheme,
        configured.netloc,
    ):
        raise DataLoadError("cx-import-errors", "CX Import error self link used an unexpected host.")
    if not parsed.path.startswith("/hcmRestApi/"):
        raise DataLoadError("cx-import-errors", "CX Import error self link used an unexpected path.")
    return parsed.path


def _cx_import_error_items(value: Any, config: dict[str, str], *, getter: Getter) -> list[dict[str, Any]]:
    if not isinstance(value, dict):
        raise DataLoadError("cx-import-errors", "CX Import error details were malformed.")
    items = value.get("items")
    has_more = value.get("hasMore")
    if not isinstance(items, list) or not isinstance(has_more, bool):
        raise DataLoadError("cx-import-errors", "CX Import error details did not contain paginated items.")
    if not has_more:
        if not all(isinstance(item, dict) for item in items):
            raise DataLoadError("cx-import-errors", "CX Import error details contained an invalid item.")
        return items
    return _get_all_items_with_params(
        _cx_import_error_self_path(value, config),
        {},
        config,
        stage="cx-import-errors",
        getter=getter,
    )


def _readable_fsm_process_log(content: bytes) -> str:
    """Decode a ProcessLog and normalize escaped control characters for reading."""
    text = content.decode("utf-8", errors="replace")
    return (
        text.replace("\\r\\n", "\n")
        .replace("\\n", "\n")
        .replace("\\r", "\n")
        .replace("\\t", "\t")
        .replace("\\/", "/")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )


def _log_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\r\n", "\n").replace("\r", "\n")


def _log_label(label: str, value: Any, *, fallback: str = "Not provided") -> str:
    text = _log_text(value)
    if not text.strip():
        text = fallback
    lines = text.split("\n")
    return "\n".join(
        [f"{label}: {lines[0]}", *(f"  {line}" for line in lines[1:])]
    )


def _log_record(title: str, fields: tuple[tuple[str, Any], ...]) -> str:
    lines = [title]
    for label, value in fields:
        if label == "Additional Details" and not _log_text(value).strip():
            continue
        lines.append(_log_label(label, value))
    return "\n".join(lines)


def _log_technical_record(index: int, value: Any) -> str:
    text = _log_text(value)
    indented = "\n".join(f"    {line}" for line in text.split("\n"))
    return f"Failed Line Error {index} source record:\n{indented}"


def _section_error(log: dict[str, Any], section: str) -> str | None:
    for item in log.get("sectionErrors") or []:
        if isinstance(item, dict) and item.get("section") == section and item.get("error"):
            return str(item["error"])
    return None


def _log_problem(row: dict[str, Any]) -> Any:
    """Prefer resolved MessageText, then a useful Message, without losing diagnostics."""
    message_text = _log_text(row.get("MessageText")).strip()
    if message_text and message_text != "-1" and not re.search(r"\{[^{}]+\}", message_text):
        return message_text
    message = _log_text(row.get("Message")).strip()
    return message or message_text


def _render_non_fsm_error_log(log: dict[str, Any]) -> str:
    failed_lines = [
        item for item in log.get("failedLines") or [] if isinstance(item, dict)
    ]
    object_errors = [
        item for item in log.get("dataSetAllObjects") or [] if isinstance(item, dict)
    ]
    failed_lines_error = _section_error(log, "failedLines")
    object_errors_error = _section_error(log, "dataSetAllObjects")

    def summary_value(rows: list[dict[str, Any]], error: str | None) -> str:
        return "Unavailable" if error else str(len(rows))

    parts = [
        "Data Loader Error Log",
        "",
        _log_label("Data Set", log.get("dataSetName") or "Unknown data set"),
        "",
        "Summary",
        _log_label(
            "Failed-line errors",
            summary_value(failed_lines, failed_lines_error),
        ),
        _log_label(
            "Data-set object errors",
            summary_value(object_errors, object_errors_error),
        ),
    ]

    parts.extend(("", "Failed Line Errors", ""))
    if failed_lines_error:
        parts.append(_log_label("Unavailable", failed_lines_error))
    elif failed_lines:
        parts.append(
            "\n\n".join(
                _log_record(
                    f"Error {index}",
                    (
                        ("Business Object", row.get("UIName")),
                        ("Problem", _log_problem(row)),
                        ("Additional Details", row.get("MessageUserDetails")),
                    ),
                )
                for index, row in enumerate(failed_lines, start=1)
            )
        )
    else:
        parts.append("No additional failed-line errors were returned.")

    parts.extend(("", "Data Set Object Errors", ""))
    if object_errors_error:
        parts.append(_log_label("Unavailable", object_errors_error))
    elif object_errors:
        parts.append(
            "\n\n".join(
                _log_record(
                    f"Error {index}",
                    (
                        ("Business Object", row.get("BusObjFileDiscriminator")),
                        ("User Key", row.get("UIUserKey")),
                        ("Problem", _log_problem(row)),
                        ("Additional Details", row.get("MessageUserDetails")),
                    ),
                )
                for index, row in enumerate(object_errors, start=1)
            )
        )
    else:
        parts.append("No additional object-level errors were returned.")

    technical_records = [
        _log_technical_record(index, row.get("FileLine"))
        for index, row in enumerate(failed_lines, start=1)
        if _log_text(row.get("FileLine")).strip()
    ]
    if technical_records:
        parts.extend(("", "Technical Details", "", "\n\n".join(technical_records)))
    return "\n".join(parts) + "\n"


def _render_cx_import_error_log(log: dict[str, Any]) -> str:
    parts = [
        "CX Import Error Log",
        "",
        _log_label("Data Set", log.get("dataSetName") or "Unknown data set"),
    ]
    section_errors = [
        item for item in log.get("sectionErrors") or [] if isinstance(item, dict)
    ]
    business_objects = [
        item for item in log.get("businessObjects") or [] if isinstance(item, dict)
    ]
    parts.extend(("", "Business Object Errors", ""))
    if business_objects:
        for index, business_object in enumerate(business_objects, start=1):
            errors = [
                item
                for item in business_object.get("errors") or []
                if isinstance(item, dict)
            ]
            parts.extend(
                (
                    f"Business Object {index}",
                    _log_label("Business Object", business_object.get("businessObjectName")),
                    _log_label("Source File", business_object.get("fileName")),
                    _log_label("Errors", len(errors)),
                )
            )
            for error_index, error in enumerate(errors, start=1):
                parts.extend(
                    (
                        "",
                        _log_record(
                            f"Error {error_index}",
                            (
                                ("Record Number", error.get("FileRecordNumber")),
                                ("Error Code", error.get("ErrorCode")),
                                ("Error Type", error.get("ErrorTypeMeaning") or error.get("ErrorType")),
                                ("Error Message", error.get("ErrorMessage")),
                            ),
                        ),
                    )
                )
            parts.append("")
    else:
        parts.append("No CX Import error records were returned.")
    if section_errors:
        parts.extend(("CX Import Diagnostic Availability", ""))
        parts.extend(
            _log_label(str(item.get("section") or "Unavailable"), item.get("error"))
            for item in section_errors
            if item.get("error")
        )
    return "\n".join(parts).rstrip() + "\n"


def write_fsm_process_logs(result: dict[str, Any], output_dir: Path) -> None:
    """Persist retrieved FSM ProcessLogs as readable downloadable text files."""
    logs = [item for item in result.get("fsmProcessLogs") or [] if isinstance(item, dict)]
    if not logs:
        return
    output_dir.mkdir(parents=True, exist_ok=True)
    for index, log in enumerate(logs, start=1):
        try:
            content = log.get("content")
            if not isinstance(content, bytes):
                raise ValueError("ProcessLog response was not binary content.")
            output_path = output_dir / _safe_process_log_name(
                str(log.get("dataSetName") or "fsm-data-set"),
                str(log.get("fsmMigRequestId") or "unknown"),
                index,
            )
            temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
            temporary_path.write_text(_readable_fsm_process_log(content), encoding="utf-8")
            os.chmod(temporary_path, 0o600)
            temporary_path.replace(output_path)
            log["outputPath"] = str(output_path.resolve())
            log["fileName"] = output_path.name
        except Exception as exc:
            result.setdefault("fsmProcessLogErrors", []).append(
                {
                    "dataSetName": log.get("dataSetName") or "FSM data set",
                    "error": f"FSM ProcessLog could not be saved: {exc}",
                }
            )


def write_fbdi_process_logs(result: dict[str, Any], output_dir: Path) -> None:
    """Persist downloaded FBDI ESS logs as readable, complete text files."""
    logs = [item for item in result.get("fbdiProcessLogs") or [] if isinstance(item, dict)]
    if not logs:
        return
    output_dir.mkdir(parents=True, exist_ok=True)
    for index, log in enumerate(logs, start=1):
        try:
            content = log.get("content")
            if not isinstance(content, bytes):
                raise ValueError("ESS process-log response was not binary content.")
            output_path = output_dir / _safe_fbdi_process_log_name(
                str(log.get("dataSetName") or "fbdi-data-set"),
                str(
                    log.get("processLabel")
                    or _fbdi_process_label(log.get("processName"))
                ),
                index,
            )
            temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
            temporary_path.write_text(
                _readable_fsm_process_log(content), encoding="utf-8"
            )
            os.chmod(temporary_path, 0o600)
            temporary_path.replace(output_path)
            log["outputPath"] = str(output_path.resolve())
            log["fileName"] = output_path.name
        except Exception as exc:
            result.setdefault("fbdiProcessLogErrors", []).append(
                {
                    "dataSetName": log.get("dataSetName") or "FBDI data set",
                    "processName": log.get("processName") or "ESS process",
                    "stage": "Log file",
                    "error": f"FBDI ESS log could not be saved: {exc}",
                }
            )


def write_non_fsm_error_logs(result: dict[str, Any], output_dir: Path) -> None:
    """Persist qualifying non-FSM diagnostics as readable text logs."""
    logs = [item for item in result.get("nonFsmErrorLogs") or [] if isinstance(item, dict)]
    if not logs:
        return
    output_dir.mkdir(parents=True, exist_ok=True)
    for index, log in enumerate(logs, start=1):
        try:
            output_path = output_dir / _safe_non_fsm_error_log_name(
                str(log.get("dataSetName") or "data-set"), index
            )
            temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
            temporary_path.write_text(_render_non_fsm_error_log(log), encoding="utf-8")
            os.chmod(temporary_path, 0o600)
            temporary_path.replace(output_path)
            log["outputPath"] = str(output_path.resolve())
            log["fileName"] = output_path.name
        except Exception as exc:
            result.setdefault("nonFsmErrorLogErrors", []).append(
                {
                    "dataSetName": log.get("dataSetName") or "Data set",
                    "error": f"Data Loader error log could not be saved: {exc}",
                }
            )


def write_cx_import_error_logs(result: dict[str, Any], output_dir: Path) -> None:
    """Persist qualifying CX Import diagnostics as readable text files."""
    logs = [item for item in result.get("cxImportErrorLogs") or [] if isinstance(item, dict)]
    if not logs:
        return
    output_dir.mkdir(parents=True, exist_ok=True)
    for index, log in enumerate(logs, start=1):
        try:
            output_path = output_dir / _safe_cx_import_error_log_name(
                str(log.get("dataSetName") or "cx-import-data-set"), index
            )
            temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
            temporary_path.write_text(_render_cx_import_error_log(log), encoding="utf-8")
            os.chmod(temporary_path, 0o600)
            temporary_path.replace(output_path)
            log["outputPath"] = str(output_path.resolve())
            log["fileName"] = output_path.name
        except Exception as exc:
            result.setdefault("cxImportErrorLogErrors", []).append(
                {
                    "dataSetName": log.get("dataSetName") or "CX Import data set",
                    "error": f"CX Import error log could not be saved: {exc}",
                }
            )


def _cx_import_error_log(
    data_set_id: str,
    data_set_name: str,
    config: dict[str, str],
    *,
    getter: Getter,
) -> dict[str, Any] | None:
    log: dict[str, Any] = {
        "dataSetName": data_set_name,
        "businessObjects": [],
        "sectionErrors": [],
    }
    try:
        business_objects = _get_all_items_with_params(
            _cx_import_business_objects_path(data_set_id),
            {"expand": "all"},
            config,
            stage="cx-import-business-objects",
            getter=getter,
        )
    except DataLoadError as exc:
        log["sectionErrors"].append(
            {"section": "cxImportBusinessObjects", "error": exc.message}
        )
        return log

    for business_object in business_objects:
        try:
            errors = _cx_import_error_items(
                business_object.get("cxImportErrors"), config, getter=getter
            )
        except DataLoadError as exc:
            log["sectionErrors"].append(
                {
                    "section": str(
                        business_object.get("BusinessObjectName")
                        or business_object.get("FileName")
                        or "cxImportErrors"
                    ),
                    "error": exc.message,
                }
            )
            continue
        if errors:
            log["businessObjects"].append(
                {
                    "businessObjectName": business_object.get("BusinessObjectName"),
                    "fileName": business_object.get("FileName"),
                    "errors": errors,
                }
            )
    return log if log["businessObjects"] or log["sectionErrors"] else None


def _fbdi_process_log_error(
    data_set_name: str,
    process_name: str,
    stage: str,
    message: str,
) -> dict[str, str]:
    return {
        "dataSetName": data_set_name,
        "processName": process_name,
        "stage": stage,
        "error": message,
    }


def _fbdi_process_logs(
    data_set_id: str,
    data_set_name: str,
    config: dict[str, str],
    *,
    getter: Getter,
    poster: Poster,
    bytes_getter: Getter,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    logs: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    hierarchy_path = FBDI_PROCESS_HIERARCHY_PATH.format(data_set_id=data_set_id)
    try:
        response = poster(
            config["host"] + hierarchy_path,
            {},
            config["auth"],
            stage="fbdi-process-hierarchy",
        )
        if not isinstance(response, dict) or not isinstance(response.get("result"), str):
            raise DataLoadError(
                "fbdi-process-hierarchy",
                "FBDI process hierarchy returned a malformed result.",
            )
        try:
            processes = json.loads(response["result"])
        except json.JSONDecodeError as exc:
            raise DataLoadError(
                "fbdi-process-hierarchy",
                "FBDI process hierarchy result was not valid JSON.",
            ) from exc
        if not isinstance(processes, list):
            raise DataLoadError(
                "fbdi-process-hierarchy",
                "FBDI process hierarchy result was not an array.",
            )
    except DataLoadError as exc:
        return logs, [
            _fbdi_process_log_error(
                data_set_name, "ESS process hierarchy", "Process hierarchy", exc.message
            )
        ]

    seen_process_ids: set[str] = set()
    for process in processes:
        if not isinstance(process, dict):
            errors.append(
                _fbdi_process_log_error(
                    data_set_name,
                    "ESS process",
                    "Process hierarchy",
                    "FBDI process hierarchy contained a malformed process entry.",
                )
            )
            continue
        process_name = str(process.get("process") or "ESS process").strip() or "ESS process"
        process_label = _fbdi_process_label(process_name)
        try:
            process_id = _positive_integer(process.get("processId"), "Process ID")
        except DataLoadError:
            errors.append(
                _fbdi_process_log_error(
                    data_set_name,
                    process_label,
                    "Process hierarchy",
                    "FBDI process hierarchy contained an invalid process identifier.",
                )
            )
            continue
        if process_id in seen_process_ids:
            continue
        seen_process_ids.add(process_id)
        process_path = FBDI_PROCESS_PATH.format(
            data_set_id=data_set_id, process_id=process_id
        )
        try:
            detail = getter(
                config["host"] + process_path,
                config["auth"],
                stage="fbdi-process-detail",
            )
            if not isinstance(detail, dict):
                raise DataLoadError(
                    "fbdi-process-detail",
                    "FBDI process detail returned a malformed response.",
                )
            raw_attachment_id = detail.get("AttachmentDocumentId")
            if raw_attachment_id in (None, ""):
                continue
            try:
                attachment_id = _positive_integer(
                    raw_attachment_id, "AttachmentDocumentId"
                )
            except DataLoadError as exc:
                raise DataLoadError(
                    "fbdi-process-detail",
                    "FBDI process detail returned an invalid log attachment identifier.",
                ) from exc
            log_path = FBDI_PROCESS_LOG_PATH.format(
                data_set_id=data_set_id,
                process_id=process_id,
                attachment_document_id=attachment_id,
            )
            content = bytes_getter(
                config["host"] + log_path,
                config["auth"],
                stage="fbdi-process-log",
            )
            if not isinstance(content, bytes):
                raise DataLoadError(
                    "fbdi-process-log",
                    "FBDI ESS log endpoint returned non-binary content.",
                )
            logs.append(
                {
                    "dataSetName": data_set_name,
                    "processName": process_name,
                    "processLabel": process_label,
                    "processStatus": process.get("status"),
                    "businessObject": process.get("businessObject"),
                    "content": content,
                }
            )
        except DataLoadError as exc:
            errors.append(
                _fbdi_process_log_error(
                    data_set_name,
                    process_label,
                    "ESS log retrieval",
                    exc.message,
                )
            )
    return logs, errors


def get_data_load_info(
    identifier: str | int,
    config_path: Path = DEFAULT_CONFIG,
    *,
    auth_options: dict[str, Any] | None = None,
    getter: Getter = get_json,
    poster: Poster = post_json,
    bytes_getter: Getter = metadata.get_bytes,
) -> dict[str, Any]:
    lookup_field, lookup_value, query_filter = _data_set_lookup(identifier)
    config = read_config(config_path, **(auth_options or {}))

    data_sets = _get_all_items(
        DATA_SETS_PATH,
        query_filter,
        config,
        stage="data-loader-data-sets",
        getter=getter,
    )

    errors: list[dict[str, Any]] = []
    non_fsm_error_logs: list[dict[str, Any]] = []
    cx_import_error_logs: list[dict[str, Any]] = []
    fbdi_process_logs: list[dict[str, Any]] = []
    fbdi_process_log_errors: list[dict[str, str]] = []
    queried_data_set_ids: list[str] = []
    seen_data_set_ids: set[str] = set()
    for data_set_index, data_set in enumerate(data_sets, start=1):
        raw_data_set_id = data_set.get("DataSetId")
        if raw_data_set_id in (None, ""):
            raise DataLoadError(
                "data-loader-data-sets",
                "dataLoaderDataSets item did not contain DataSetId.",
                response={lookup_field: lookup_value},
            )
        data_set_id = _positive_integer(raw_data_set_id, "DataSetId")
        if data_set_id in seen_data_set_ids:
            continue
        seen_data_set_ids.add(data_set_id)
        queried_data_set_ids.append(data_set_id)
        errors.extend(
            _get_all_items(
                DATA_SET_ERRORS_PATH,
                f"DataSetId={data_set_id}",
                config,
                stage="data-set-errors",
                getter=getter,
            )
        )
        if str(data_set.get("SourceType") or "").strip() == CX_IMPORT_SOURCE_TYPE:
            cx_import_log = _cx_import_error_log(
                data_set_id,
                _data_set_name(data_set, data_set_index),
                config,
                getter=getter,
            )
            if cx_import_log is not None:
                cx_import_error_logs.append(cx_import_log)
            continue
        if str(data_set.get("SourceType") or "").strip() == FBDI_SOURCE_TYPE:
            process_logs, process_log_errors = _fbdi_process_logs(
                data_set_id,
                _data_set_name(data_set, data_set_index),
                config,
                getter=getter,
                poster=poster,
                bytes_getter=bytes_getter,
            )
            fbdi_process_logs.extend(process_logs)
            fbdi_process_log_errors.extend(process_log_errors)
        if str(data_set.get("SourceType") or "").strip() != FSM_SOURCE_TYPE:
            diagnostic_log: dict[str, Any] = {
                "dataSetName": _data_set_name(data_set, data_set_index),
                "failedLines": [],
                "dataSetAllObjects": [],
                "sectionErrors": [],
            }
            diagnostic_specs = (
                (
                    "failedLines",
                    FAILED_LINES_PATH.format(data_set_id=data_set_id),
                    FAILED_LINES_QUERY,
                    "failed-lines",
                ),
                (
                    "dataSetAllObjects",
                    DATA_SET_ALL_OBJECTS_PATH.format(data_set_id=data_set_id),
                    DATA_SET_ALL_OBJECTS_QUERY,
                    "data-set-all-objects",
                ),
            )
            for section, path, params, stage in diagnostic_specs:
                try:
                    diagnostic_log[section] = _get_all_items_with_params(
                        path, params, config, stage=stage, getter=getter
                    )
                except DataLoadError as exc:
                    diagnostic_log["sectionErrors"].append(
                        {"section": section, "error": exc.message}
                    )
            if any(
                diagnostic_log[section]
                for section in (
                    "failedLines",
                    "dataSetAllObjects",
                    "sectionErrors",
                )
            ):
                non_fsm_error_logs.append(diagnostic_log)

    fsm_process_logs: list[dict[str, Any]] = []
    fsm_process_log_errors: list[dict[str, str]] = []
    for index, data_set in enumerate(data_sets, start=1):
        if str(data_set.get("SourceType") or "").strip() != FSM_SOURCE_TYPE:
            continue
        data_set_name = _data_set_name(data_set, index)
        try:
            process_log_url, task_code, fsm_mig_request_id = _fsm_process_log_url(
                data_set, config["host"]
            )
            content = bytes_getter(
                process_log_url,
                config["auth"],
                stage="fsm-process-log",
            )
            if not isinstance(content, bytes):
                raise DataLoadError(
                    "fsm-process-log", "FSM ProcessLog endpoint returned non-binary content."
                )
            fsm_process_logs.append(
                {
                    "dataSetName": data_set_name,
                    "fsmTaskCode": task_code,
                    "fsmMigRequestId": fsm_mig_request_id,
                    "content": content,
                }
            )
        except DataLoadError as exc:
            fsm_process_log_errors.append(
                {"dataSetName": data_set_name, "error": exc.message}
            )

    return {
        lookup_field: lookup_value,
        "dataSetCount": len(data_sets),
        "queriedDataSetIds": queried_data_set_ids,
        "dataSets": data_sets,
        "errorCount": len(errors),
        "dataSetErrors": errors,
        "nonFsmErrorLogs": non_fsm_error_logs,
        "nonFsmErrorLogErrors": [],
        "cxImportErrorLogs": cx_import_error_logs,
        "cxImportErrorLogErrors": [],
        "fbdiProcessLogs": fbdi_process_logs,
        "fbdiProcessLogErrors": fbdi_process_log_errors,
        "fsmProcessLogs": fsm_process_logs,
        "fsmProcessLogErrors": fsm_process_log_errors,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Query dataLoaderDataSets and dataSetErrors for a Fusion initiation "
            "Request ID or UCM Content ID."
        )
    )
    parser.add_argument(
        "identifier",
        help="Initiation RequestId or UCM ContentId returned by the data-load workflow.",
    )
    parser.add_argument(
        "--status-only",
        action="store_true",
        help=(
            "Return current status with object counts when available; Fusion errors "
            "expand the output with full diagnostics."
        ),
    )
    metadata.add_oauth_arguments(parser)
    parser.add_argument(
        "--inline-output",
        type=Path,
        help="Deprecated compatibility option; inline HTML rendering is disabled.",
    )
    parser.add_argument(
        "--diagnostic-log-output-dir",
        "--fsm-process-log-output-dir",
        dest="diagnostic_log_output_dir",
        type=Path,
        help=(
            "Directory for downloaded FSM ProcessLogs and generated non-FSM error logs; "
            "overrides the default per-request Codex diagnostics directory."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = get_data_load_info(
            args.identifier,
            args.properties,
            auth_options=metadata.oauth_kwargs(args),
        )
    except DataLoadError as exc:
        data_loader_report.emit_inline_or_markdown(
            exc,
            "error",
            args.inline_output,
            data_loader_report.render_error_report,
            stream=sys.stderr,
        )
        return 1

    try:
        diagnostic_log_output_dir = (
            args.diagnostic_log_output_dir.expanduser()
            if args.diagnostic_log_output_dir is not None
            else _default_diagnostic_log_output_dir(args.identifier)
        )
        write_fsm_process_logs(result, diagnostic_log_output_dir)
        write_fbdi_process_logs(result, diagnostic_log_output_dir)
        write_non_fsm_error_logs(result, diagnostic_log_output_dir)
        write_cx_import_error_logs(result, diagnostic_log_output_dir)
    except (DataLoadError, OSError) as exc:
        if isinstance(exc, OSError):
            exc = DataLoadError("artifact-persistence", f"Invalid diagnostic output directory: {exc}")
        data_loader_report.emit_inline_or_markdown(
            exc, "error", args.inline_output, data_loader_report.render_error_report, stream=sys.stderr
        )
        return 1

    data_loader_report.emit_inline_or_markdown(
        result,
        "status",
        args.inline_output,
        lambda value: data_loader_report.render_status_report(
            value, status_only=args.status_only
        ),
        status_only=args.status_only,
        stream=sys.stdout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
