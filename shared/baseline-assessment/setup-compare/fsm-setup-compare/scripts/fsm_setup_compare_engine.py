"""Shared Oracle Fusion setup compare engine.

This module owns the low-level setupMigrationProcesses compare mechanics for
task, offering, and functional-area setup ZIP comparisons. Callers supply an
OAuth access token produced by the FSCR Fusion OAuth authentication skill.
"""

from __future__ import annotations

import sys
import json
import re
import time
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, parse, request


sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "core/auth/fusion-oauth-authentication/scripts"))
from fusion_auth import authorized_urlopen, require_authorized_rest_url


ACTION_CONTENT_TYPE = "application/vnd.oracle.adf.action+json"
UPLOAD_PROCESS_TYPE = "MIGRATOR_UPLOAD_VB_FLOW"
COMPARE_PROCESS_TYPE = "COMPARE_REQUEST"
CODE_VALUE_RE = re.compile(r"^[A-Z0-9][A-Z0-9_.:-]*$")

SUCCESS_STATUSES = {"COMPLETED", "COMPLETED_WARNINGS", "SUCCESS", "SUCCEEDED"}
FAILURE_STATUSES = {"COMPLETED_ERRORS", "FAILED", "ERROR", "CANCELLED", "CANCELED"}
WAIT_STATUSES = {"NOT_STARTED", "IN_PROGRESS", "RUNNING", "QUEUED", "PENDING"}

DEFAULT_ARTIFACTS = [
    "COMPARISON_RESULTS_XML",
    "COMPARISON_REPORT",
    "COMPARISON_RESULTS_REPORT",
    "COMPARISON_PROCESS_SUMMARY_REPORT",
    "COMPARISON_PROCESS_STATUS_DETAILS",
]

ARTIFACT_ENCLOSURES = {
    "COMPARISON_PROCESS_STATUS_DETAILS": "FileContentClob",
}

ARTIFACT_EXTENSIONS = {
    "COMPARISON_RESULTS_XML": ".xml",
    "COMPARISON_REPORT": ".bin",
    "COMPARISON_RESULTS_REPORT": ".bin",
    "COMPARISON_PROCESS_SUMMARY_REPORT": ".bin",
    "COMPARISON_PROCESS_STATUS_DETAILS": ".log",
    "COMPARISON_DIAGNOSTICS_PACKAGE_ZIP": ".zip",
}

STANDARD_REPORT_TEMPLATE = """## Summary
- Action: <action>
- Overall status: <overallStatus>
- Compare environment: <compareEnvironment>
- Entity type: <entityType>
- Object: <objectName>
- Compare process ID: <compareProcessId>

## Process Details
| Step | Process ID | Status | Name |
| --- | --- | --- | --- |
| <step> | <processId> | <status> | <name> |

## Results
| Business object | Source 1 count | Source 2 count | Mismatch count | Match count | Total count |
| --- | ---: | ---: | ---: | ---: | ---: |
| <businessObject> | <source1Count> | <source2Count> | <mismatchCount> | <matchCount> | <totalCount> |

## Artifacts
| Artifact | Download link or status |
| --- | --- |
| <artifactName> | <downloadLinkOrStatus> |

## Warnings and Errors
- <warningOrNone>
"""


class CompareError(RuntimeError):
    """Raised for expected compare workflow failures."""


class CompareHttpError(CompareError):
    """Raised when Fusion returns an HTTP error."""

    def __init__(self, status_code: int, method: str, url: str, body: bytes) -> None:
        self.status_code = status_code
        self.method = method
        self.url = url
        self.body = body
        super().__init__(f"HTTP {status_code} for {method} {redacted_url(url)}: {body_preview(body)}")


@dataclass
class HttpResult:
    status: int
    headers: Any
    body: bytes
    url: str

    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")

    def json(self) -> Any:
        return json.loads(self.text())


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def redact(value: str) -> str:
    value = re.sub(r"Authorization:\s*Bearer\s+[A-Za-z0-9._~+/=-]+", "Authorization: Bearer <redacted>", value, flags=re.I)
    value = re.sub(r"Bearer\s+[A-Za-z0-9._~+/=-]+", "Bearer <redacted>", value, flags=re.I)
    return value


def redacted_url(url: str) -> str:
    return redact(url)


def body_preview(body: bytes, limit: int = 1200) -> str:
    text = body.decode("utf-8", errors="replace")
    if len(text) > limit:
        text = text[:limit] + "...<truncated>"
    return redact(text)


def normalize_resource_root(raw: str, api_version: str = "latest") -> str:
    raw = raw.strip().rstrip("/")
    if not raw:
        raise CompareError("Base URL is required.")
    if not re.match(r"^[a-z][a-z0-9+.-]*://", raw, flags=re.I):
        raw = "https://" + raw
    parsed = parse.urlsplit(raw)
    if not parsed.netloc:
        raise CompareError(f"Invalid base URL or host: {raw}")
    prefix = f"{parsed.scheme}://{parsed.netloc}"
    marker = "/fscmRestApi/resources/"
    if marker in parsed.path:
        before, after = parsed.path.split(marker, 1)
        version = after.split("/", 1)[0] or api_version
        return f"{prefix}{before}{marker}{version}".rstrip("/")
    return f"{prefix}/fscmRestApi/resources/{api_version}".rstrip("/")


def resource_root_from_props(props: dict[str, str], base_url: str | None = None, api_version: str = "latest") -> str:
    require_authorized_rest_url(props, base_url or props["restBaseUrl"])
    root = normalize_resource_root(base_url or props["restBaseUrl"], api_version)
    require_authorized_rest_url(props, root)
    return root


def http_call(
    access_token: str,
    method: str,
    url: str,
    data: bytes | None = None,
    content_type: str | None = None,
    accept: str = "application/json, */*",
    timeout: int = 120,
) -> HttpResult:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": accept,
    }
    if content_type:
        headers["Content-Type"] = content_type
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with authorized_urlopen(None, req, timeout=timeout, access_token=access_token) as resp:
            return HttpResult(resp.status, resp.headers, resp.read(), url)
    except error.HTTPError as exc:
        body = exc.read()
        raise CompareHttpError(exc.code, method, url, body) from exc
    except error.URLError as exc:
        raise CompareError(f"Network error for {method} {redacted_url(url)}: {redact(str(exc))}") from exc


def post_json(
    access_token: str,
    url: str,
    payload: dict[str, Any],
    content_type: str = ACTION_CONTENT_TYPE,
) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    result = http_call(access_token, "POST", url, data=data, content_type=content_type)
    try:
        parsed = result.json()
    except json.JSONDecodeError as exc:
        raise CompareError(f"Expected JSON from POST {redacted_url(url)}, got: {body_preview(result.body)}") from exc
    if not isinstance(parsed, dict):
        raise CompareError(f"Expected JSON object from POST {redacted_url(url)}, got: {type(parsed).__name__}")
    return parsed


def get_json(access_token: str, url: str) -> dict[str, Any]:
    result = http_call(access_token, "GET", url)
    try:
        parsed = result.json()
    except json.JSONDecodeError as exc:
        raise CompareError(f"Expected JSON from GET {redacted_url(url)}, got: {body_preview(result.body)}") from exc
    if not isinstance(parsed, dict):
        raise CompareError(f"Expected JSON object from GET {redacted_url(url)}, got: {type(parsed).__name__}")
    return parsed


def get_bytes(access_token: str, url: str) -> HttpResult:
    return http_call(access_token, "GET", url, accept="*/*")


def result_node(data: dict[str, Any]) -> dict[str, Any]:
    node = data.get("result", data)
    if isinstance(node, dict):
        return node
    return {"result": node}


def as_id(value: Any) -> str:
    if value is None or value == "":
        raise CompareError("Expected an ID value but received an empty value.")
    return str(value)


def json_number_if_possible(value: str) -> int | str:
    return int(value) if re.fullmatch(r"\d+", value) else value


def validate_zip(path: Path) -> None:
    if not path.exists():
        raise CompareError(f"ZIP file does not exist: {path}")
    if not path.is_file():
        raise CompareError(f"ZIP path is not a file: {path}")
    if not zipfile.is_zipfile(path):
        raise CompareError(f"File is not a readable ZIP archive: {path}")


def action_url(root: str, action_name: str) -> str:
    return f"{root}/setupMigrationProcesses/action/{action_name}"


def create_file_blob(access_token: str, root: str, zip_path: Path) -> tuple[str, dict[str, Any]]:
    payload = {
        "ProcessType": UPLOAD_PROCESS_TYPE,
        "FileName": zip_path.name,
    }
    data = post_json(access_token, f"{root}/setupMigrationProcessFiles", payload, content_type="application/json")
    node = result_node(data)
    process_id = node.get("ProcessId") or node.get("processId") or node.get("FileKey") or node.get("fileKey")
    if not process_id:
        raise CompareError(f"Create file blob did not return ProcessId/FileKey: {compact_json(node)}")
    return as_id(process_id), node


def upload_file_blob(access_token: str, root: str, process_id: str, zip_path: Path) -> dict[str, Any]:
    url = f"{root}/setupMigrationProcessFiles/{parse.quote(process_id, safe='')}/enclosure/FileContentBlob"
    result = http_call(
        access_token,
        "PUT",
        url,
        data=zip_path.read_bytes(),
        content_type="application/octet-stream",
        accept="application/json, */*",
    )
    parsed: dict[str, Any] = {"httpStatus": result.status}
    if result.body.strip():
        try:
            maybe_json = result.json()
            if isinstance(maybe_json, dict):
                parsed.update(maybe_json)
            else:
                parsed["bodyPreview"] = body_preview(result.body)
        except json.JSONDecodeError:
            parsed["bodyPreview"] = body_preview(result.body)
    return parsed


def code_fields(
    *,
    task_code: str | None,
    offering_code: str | None,
    functional_area_code: str | None,
) -> dict[str, str | None]:
    return {
        "taskCode": task_code,
        "offeringCode": offering_code,
        "functionalAreaCode": functional_area_code,
    }


def looks_like_code(value: str | None) -> bool:
    return bool(value and CODE_VALUE_RE.fullmatch(value.strip()))


def code_value_as_name(value: str | None) -> str | None:
    if value and not looks_like_code(value):
        return value.strip()
    return None


def lookup_items(access_token: str, url: str) -> list[dict[str, Any]]:
    data = get_json(access_token, url)
    items = data.get("items")
    if isinstance(items, list):
        return [item for item in items if isinstance(item, dict)]
    if isinstance(data.get("Items"), list):
        return [item for item in data["Items"] if isinstance(item, dict)]
    return []


def first_present(item: dict[str, Any], aliases: tuple[str, ...]) -> Any:
    for alias in aliases:
        if alias in item and item[alias] not in (None, ""):
            return item[alias]
    return None


def exact_or_single_match(
    items: list[dict[str, Any]],
    name_fields: tuple[str, ...],
    code_fields_: tuple[str, ...],
    name: str,
) -> str | None:
    if not items:
        return None
    exact = [item for item in items if str(first_present(item, name_fields) or "").casefold() == name.casefold()]
    candidates = exact or items
    codes: list[str] = []
    for item in candidates:
        code = first_present(item, code_fields_)
        if code and str(code) not in codes:
            codes.append(str(code))
    if len(codes) == 1:
        return codes[0]
    choices = [
        {
            "name": first_present(item, name_fields),
            "code": first_present(item, code_fields_),
            "type": first_present(item, ("FeatureType", "featureType")),
        }
        for item in candidates[:10]
    ]
    raise CompareError(f"Lookup for {name!r} returned multiple matches; provide the code explicitly. Matches: {compact_json(choices)}")


def lookup_task_code(access_token: str, root: str, task_name: str) -> str:
    q = f"TaskName='{task_name}'"
    url = f"{root}/setupTasks?{parse.urlencode({'q': q})}"
    code = exact_or_single_match(
        lookup_items(access_token, url),
        ("TaskName", "taskName"),
        ("TaskCode", "taskCode"),
        task_name,
    )
    if not code:
        raise CompareError(f"Could not find a task code for {task_name!r}; provide --task-code.")
    return code


def lookup_feature_code(access_token: str, root: str, feature_type: str, feature_name: str) -> str:
    q = f"FeatureType='{feature_type}';FeatureName='{feature_name}'"
    url = f"{root}/features?{parse.urlencode({'fields': 'FeatureName,FeatureCode,FeatureType', 'q': q})}"
    code = exact_or_single_match(
        lookup_items(access_token, url),
        ("FeatureName", "featureName"),
        ("FeatureCode", "featureCode"),
        feature_name,
    )
    if not code:
        label = "offering" if feature_type == "OFFERING" else "functional area"
        raise CompareError(f"Could not find a {label} code for {feature_name!r}; provide the code explicitly.")
    return code


def validate_codes(entity_type: str, task_code: str | None, offering_code: str | None, functional_area_code: str | None) -> None:
    if entity_type == "TASK" and not task_code:
        raise CompareError("Task compare requires --task-code or a resolvable task name/object name.")
    if entity_type == "OFFERING" and not offering_code:
        raise CompareError("Offering compare requires --offering-code or a resolvable offering name/object name.")
    if entity_type == "FUNCTIONAL_AREA":
        missing = []
        if not offering_code:
            missing.append("--offering-code or --offering-name")
        if not functional_area_code:
            missing.append("--functional-area-code or --functional-area-name/object-name")
        if missing:
            raise CompareError("Functional Area compare requires " + " and ".join(missing) + ".")


def resolve_codes(
    *,
    access_token: str,
    root: str,
    entity_type: str,
    object_name: str,
    task_name: str | None = None,
    task_code: str | None = None,
    offering_name: str | None = None,
    offering_code: str | None = None,
    functional_area_name: str | None = None,
    functional_area_code: str | None = None,
    no_lookup_code: bool = False,
) -> tuple[dict[str, str | None], list[dict[str, str]]]:
    code_resolution: list[dict[str, str]] = []
    if no_lookup_code:
        validate_codes(entity_type, task_code, offering_code, functional_area_code)
        return code_fields(
            task_code=task_code,
            offering_code=offering_code,
            functional_area_code=functional_area_code,
        ), code_resolution

    if entity_type == "TASK":
        lookup_name = task_name or code_value_as_name(task_code) or (None if task_code else object_name)
        if lookup_name:
            task_code = lookup_task_code(access_token, root, lookup_name)
            code_resolution.append({"entityType": "TASK", "name": lookup_name, "code": task_code})

    if entity_type == "OFFERING":
        lookup_name = offering_name or code_value_as_name(offering_code) or (None if offering_code else object_name)
        if lookup_name:
            offering_code = lookup_feature_code(access_token, root, "OFFERING", lookup_name)
            code_resolution.append({"entityType": "OFFERING", "name": lookup_name, "code": offering_code})

    if entity_type == "FUNCTIONAL_AREA":
        offering_lookup_name = offering_name or code_value_as_name(offering_code)
        if offering_lookup_name:
            offering_code = lookup_feature_code(access_token, root, "OFFERING", offering_lookup_name)
            code_resolution.append({"entityType": "OFFERING", "name": offering_lookup_name, "code": offering_code})

        functional_area_lookup_name = functional_area_name or code_value_as_name(functional_area_code) or (
            None if functional_area_code else object_name
        )
        if functional_area_lookup_name:
            functional_area_code = lookup_feature_code(access_token, root, "FUNCTIONAL_AREA", functional_area_lookup_name)
            code_resolution.append(
                {"entityType": "FUNCTIONAL_AREA", "name": functional_area_lookup_name, "code": functional_area_code}
            )

    validate_codes(entity_type, task_code, offering_code, functional_area_code)
    return code_fields(
        task_code=task_code,
        offering_code=offering_code,
        functional_area_code=functional_area_code,
    ), code_resolution


def create_upload(
    access_token: str,
    root: str,
    file_blob_id: str,
    codes: dict[str, str | None],
    source_cfg_created_by_flow: str | None,
) -> tuple[str, str, dict[str, Any]]:
    payload: dict[str, Any] = {
        "type": COMPARE_PROCESS_TYPE,
        **codes,
        "fileBlobId": json_number_if_possible(file_blob_id),
    }
    if source_cfg_created_by_flow:
        payload["additionalProperties"] = {
            "sourceCfgCreatedByFlow": source_cfg_created_by_flow,
        }
    data = post_json(access_token, action_url(root, "createUpload"), payload)
    node = result_node(data)
    if node.get("returnCode"):
        raise CompareError(f"createUpload returned {node.get('returnCode')}: {compact_json(node)}")
    upload_id = node.get("migRequestId") or node.get("processId") or node.get("ProcessId")
    if not upload_id:
        raise CompareError(f"createUpload did not return migRequestId/processId: {compact_json(node)}")
    name = node.get("processName") or node.get("cfgPackageName") or node.get("processDesc") or str(upload_id)
    return as_id(upload_id), str(name), node


def retrieve_compare_name(
    access_token: str,
    root: str,
    object_name: str,
    source1_name: str,
    source2_name: str,
) -> tuple[str, dict[str, Any]]:
    payload = {
        "objectName": object_name,
        "source1Name": source1_name,
        "source2Name": source2_name,
    }
    data = post_json(access_token, action_url(root, "retrieveCompareProcessName"), payload)
    node = result_node(data)
    compare_name = node.get("compareProcessName") or f"{source1_name} compared to {source2_name}"
    return str(compare_name), node


def submit_compare(
    access_token: str,
    root: str,
    source1_id: str,
    source2_id: str,
    request_name: str,
    codes: dict[str, str | None],
) -> tuple[str, dict[str, Any]]:
    payload: dict[str, Any] = {
        "source1Id": json_number_if_possible(source1_id),
        "source2Type": "MIG_REQUEST_ID",
        "source2Id": json_number_if_possible(source2_id),
        **codes,
        "requestName": request_name,
    }
    data = post_json(access_token, action_url(root, "submitCompare"), payload)
    node = result_node(data)
    process_id = node.get("processId") or node.get("ProcessId")
    if not process_id:
        raise CompareError(f"submitCompare did not return processId: {compact_json(node)}")
    return as_id(process_id), node


def compare_artifact_url(root: str, process_id: str, file_type: str, enclosure: str | None = None) -> str:
    enclosure = enclosure or ARTIFACT_ENCLOSURES.get(file_type, "FileContentBlob")
    composite = f"ProcessType={COMPARE_PROCESS_TYPE}@@@ProcessId={process_id}@@@FileType={file_type}"
    return f"{root}/setupMigrationProcessFiles/{composite}/enclosure/{enclosure}"


def extract_status(value: Any) -> str | None:
    if isinstance(value, dict):
        for key in ("processStatus", "ProcessStatus", "StatusCode", "status", "Status", "state", "State"):
            if value.get(key):
                return str(value[key]).upper()
        if value.get("ProcessCompletedFlag") is True:
            return "COMPLETED"
        for nested_key in ("result", "items"):
            nested = value.get(nested_key)
            if isinstance(nested, list) and nested:
                found = extract_status(nested[0])
                if found:
                    return found
            elif isinstance(nested, dict):
                found = extract_status(nested)
                if found:
                    return found
    if isinstance(value, str):
        upper = value.upper()
        for status in sorted(SUCCESS_STATUSES | FAILURE_STATUSES | WAIT_STATUSES, key=len, reverse=True):
            if status in upper:
                return status
    return None


def try_get_json(access_token: str, url: str) -> tuple[dict[str, Any] | None, str | None]:
    try:
        return get_json(access_token, url), None
    except CompareError as exc:
        return None, str(exc)


def try_get_text_or_bytes(access_token: str, url: str) -> tuple[HttpResult | None, str | None]:
    try:
        return get_bytes(access_token, url), None
    except CompareError as exc:
        return None, str(exc)


def poll_compare(
    access_token: str,
    root: str,
    process_id: str,
    interval_seconds: int,
    timeout_minutes: int,
) -> tuple[str, dict[str, Any]]:
    deadline = time.monotonic() + timeout_minutes * 60
    attempts = 0
    last: dict[str, Any] = {}
    process_urls = [
        f"{root}/setupMigrationProcesses/ProcessType={COMPARE_PROCESS_TYPE}@@@ProcessId={process_id}",
        f"{root}/setupMigrationProcesses/{parse.quote(process_id, safe='')}",
    ]
    status_artifact_url = compare_artifact_url(root, process_id, "COMPARISON_PROCESS_STATUS_DETAILS", "FileContentClob")
    result_xml_url = compare_artifact_url(root, process_id, "COMPARISON_RESULTS_XML", "FileContentBlob")

    while time.monotonic() < deadline:
        attempts += 1
        for url in process_urls:
            data, err = try_get_json(access_token, url)
            if data is not None:
                status = extract_status(data)
                last = {"source": "setupMigrationProcesses", "response": data, "status": status}
                if status in SUCCESS_STATUSES:
                    return status, last
                if status in FAILURE_STATUSES:
                    raise CompareError(f"Compare process ended with {status}: {compact_json(data)}")
                if status:
                    print(f"Poll {attempts}: {status}")
                    break
            elif err:
                last = {"source": "setupMigrationProcesses", "error": err}

        status_result, status_err = try_get_text_or_bytes(access_token, status_artifact_url)
        if status_result is not None and status_result.body:
            text = status_result.text()
            status = extract_status(text)
            last = {"source": "COMPARISON_PROCESS_STATUS_DETAILS", "status": status, "preview": redact(text[:2000])}
            if status in SUCCESS_STATUSES:
                return status, last
            if status in FAILURE_STATUSES:
                raise CompareError(f"Compare status details indicate {status}: {redact(text[:2000])}")
            if status:
                print(f"Poll {attempts}: {status}")
        elif status_err:
            last = {"source": "COMPARISON_PROCESS_STATUS_DETAILS", "error": status_err}

        result_xml, xml_err = try_get_text_or_bytes(access_token, result_xml_url)
        if result_xml is not None and result_xml.body:
            last = {
                "source": "COMPARISON_RESULTS_XML",
                "status": "COMPLETED",
                "completionSignal": "COMPARISON_RESULTS_XML available",
            }
            return "COMPLETED", last
        elif xml_err:
            last = {"source": "COMPARISON_RESULTS_XML", "error": xml_err}

        print(f"Poll {attempts}: waiting for compare process {process_id}")
        time.sleep(interval_seconds)

    raise CompareError(f"Timed out waiting for compare process {process_id}. Last status: {compact_json(last)}")


def filename_from_content_disposition(header_value: str | None) -> str | None:
    if not header_value:
        return None
    match = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?', header_value, flags=re.I)
    if not match:
        return None
    return Path(parse.unquote(match.group(1))).name


def safe_filename(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_") or "artifact"


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "setup-compare"


def download_artifacts(
    access_token: str,
    root: str,
    process_id: str,
    output_dir: Path,
    artifact_names: list[str],
) -> tuple[list[dict[str, Any]], list[str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[dict[str, Any]] = []
    warnings: list[str] = []
    for file_type in artifact_names:
        file_type = file_type.strip().upper()
        if not file_type:
            continue
        enclosure = ARTIFACT_ENCLOSURES.get(file_type, "FileContentBlob")
        url = compare_artifact_url(root, process_id, file_type, enclosure)
        try:
            result = get_bytes(access_token, url)
        except CompareError as exc:
            warnings.append(f"Could not download optional artifact {file_type}: {exc}")
            continue
        if not result.body:
            warnings.append(f"Artifact {file_type} was empty.")
            continue
        filename = filename_from_content_disposition(result.headers.get("Content-Disposition"))
        if not filename:
            filename = f"compare_{process_id}_{safe_filename(file_type)}{ARTIFACT_EXTENSIONS.get(file_type, '.bin')}"
        target = output_dir / safe_filename(filename)
        target.write_bytes(result.body)
        downloaded.append(
            {
                "fileType": file_type,
                "enclosure": enclosure,
                "path": str(target.resolve()),
                "bytes": len(result.body),
                "httpStatus": result.status,
            }
        )
    return downloaded, warnings


def artifact_label(file_type: str) -> str:
    labels = {
        "COMPARISON_RESULTS_XML": "Comparison results XML",
        "COMPARISON_REPORT": "Comparison report",
        "COMPARISON_RESULTS_REPORT": "Comparison results report",
        "COMPARISON_PROCESS_SUMMARY_REPORT": "Process summary report",
        "COMPARISON_PROCESS_STATUS_DETAILS": "Process status details",
        "COMPARISON_DIAGNOSTICS_PACKAGE_ZIP": "Diagnostics package",
    }
    return labels.get(file_type, file_type.replace("_", " ").title())


def markdown_cell(value: Any) -> str:
    if value is None or value == "":
        return "-"
    text = str(value).replace("\n", " ").replace("|", "\\|")
    return text.strip() or "-"


def markdown_link(path: str) -> str:
    target = str(Path(path).resolve())
    return f"[{Path(target).name}]({target})"


def child_texts(element: ET.Element) -> dict[str, str]:
    return {
        child.tag.rsplit("}", 1)[-1]: (child.text or "").strip()
        for child in list(element)
    }


def parse_int_if_possible(value: str | None) -> int | str | None:
    if value is None or value == "":
        return None
    return int(value) if re.fullmatch(r"-?\d+", value) else value


def first_text(fields: dict[str, str], names: tuple[str, ...]) -> str | None:
    for name in names:
        if fields.get(name):
            return fields[name]
    return None


def parse_comparison_counts(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    xml_path = None
    for artifact in artifacts:
        if artifact.get("fileType") == "COMPARISON_RESULTS_XML" and artifact.get("path"):
            xml_path = Path(str(artifact["path"]))
            break
    if not xml_path or not xml_path.exists():
        return []

    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError:
        return []

    rows: list[dict[str, Any]] = []
    seen: set[tuple[tuple[str, Any], ...]] = set()
    for element in root.iter():
        fields = child_texts(element)
        if not fields:
            continue
        business_object = first_text(
            fields,
            ("NodePath", "BusinessObjectName", "BusinessObjectShortName", "ObjectName", "ObjectCode"),
        )
        counts = {
            "source1Count": parse_int_if_possible(first_text(fields, ("Source1Count", "SourceOneCount"))),
            "source2Count": parse_int_if_possible(first_text(fields, ("Source2Count", "SourceTwoCount"))),
            "mismatchCount": parse_int_if_possible(first_text(fields, ("MismatchCount", "DiscrepancyCount"))),
            "matchCount": parse_int_if_possible(first_text(fields, ("MatchCount",))),
            "totalCount": parse_int_if_possible(first_text(fields, ("TotalCount",))),
        }
        if not business_object or not any(value is not None for value in counts.values()):
            continue
        row = {"businessObject": business_object, **counts}
        marker = tuple(sorted(row.items()))
        if marker not in seen:
            seen.add(marker)
            rows.append(row)
    return rows


def report_process_rows(summary: dict[str, Any]) -> list[str]:
    rows: list[str] = []
    for upload in summary.get("uploads", []):
        source = markdown_cell(upload.get("source"))
        rows.append(
            "| "
            + " | ".join(
                [
                    f"Source {source} upload",
                    markdown_cell(upload.get("uploadProcessId")),
                    "Registered",
                    markdown_cell(upload.get("sourceName")),
                ]
            )
            + " |"
        )
    if summary.get("compareProcessId"):
        rows.append(
            "| "
            + " | ".join(
                [
                    "Compare",
                    markdown_cell(summary.get("compareProcessId")),
                    markdown_cell(summary.get("finalStatus")),
                    markdown_cell(summary.get("compareProcessName")),
                ]
            )
            + " |"
        )
    return rows or ["| - | - | - | - |"]


def report_result_rows(summary: dict[str, Any]) -> list[str]:
    rows: list[str] = []
    for result in summary.get("objectCounts", []):
        rows.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(result.get("businessObject")),
                    markdown_cell(result.get("source1Count")),
                    markdown_cell(result.get("source2Count")),
                    markdown_cell(result.get("mismatchCount")),
                    markdown_cell(result.get("matchCount")),
                    markdown_cell(result.get("totalCount")),
                ]
            )
            + " |"
        )
    return rows or ["| No object-level counts parsed | - | - | - | - | - |"]


def report_artifact_rows(summary: dict[str, Any]) -> list[str]:
    rows: list[str] = []
    artifacts = summary.get("artifacts", [])
    downloaded = {artifact.get("fileType"): artifact for artifact in artifacts if artifact.get("fileType")}
    expected = list(dict.fromkeys([*DEFAULT_ARTIFACTS, *[str(artifact.get("fileType")) for artifact in artifacts if artifact.get("fileType")]]))
    for file_type in expected:
        artifact = downloaded.get(file_type)
        status = markdown_link(str(artifact["path"])) if artifact and artifact.get("path") else "Unavailable"
        rows.append(f"| {markdown_cell(artifact_label(file_type))} | {status} |")
    if summary.get("processOutputPath"):
        rows.append(f"| Sanitized process output JSON | {markdown_link(str(summary['processOutputPath']))} |")
    return rows or ["| - | - |"]


def report_warning_rows(summary: dict[str, Any]) -> list[str]:
    warnings = summary.get("warnings", [])
    if not warnings:
        return ["- None reported."]
    rows = []
    for warning in warnings:
        match = re.search(r"optional artifact ([A-Z0-9_]+)", str(warning))
        if match:
            rows.append(f"- {match.group(1)} was unavailable.")
        else:
            rows.append(f"- {markdown_cell(redact(str(warning)).split(' for GET ', 1)[0])}")
    return rows


def render_standard_report(summary: dict[str, Any]) -> str:
    report = STANDARD_REPORT_TEMPLATE
    replacements = {
        "<action>": "Compared two FSM setup ZIP packages",
        "<overallStatus>": markdown_cell(summary.get("finalStatus")),
        "<compareEnvironment>": markdown_cell(summary.get("environmentResourceRoot")),
        "<entityType>": markdown_cell(summary.get("entityType")),
        "<objectName>": markdown_cell(summary.get("objectName")),
        "<compareProcessId>": markdown_cell(summary.get("compareProcessId")),
        "| <step> | <processId> | <status> | <name> |": "\n".join(report_process_rows(summary)),
        "| <businessObject> | <source1Count> | <source2Count> | <mismatchCount> | <matchCount> | <totalCount> |": "\n".join(report_result_rows(summary)),
        "| <artifactName> | <downloadLinkOrStatus> |": "\n".join(report_artifact_rows(summary)),
        "- <warningOrNone>": "\n".join(report_warning_rows(summary)),
    }
    for placeholder, value in replacements.items():
        report = report.replace(placeholder, value)
    return report.rstrip() + "\n"


def make_request_plan(
    *,
    root: str,
    zip1: Path,
    zip2: Path,
    object_name: str,
    entity_type: str,
    codes: dict[str, str | None],
    source_cfg_created_by_flow: str | None,
) -> dict[str, Any]:
    upload_payload = {"type": COMPARE_PROCESS_TYPE, **codes, "fileBlobId": "<fileBlobId>"}
    if source_cfg_created_by_flow:
        upload_payload["additionalProperties"] = {"sourceCfgCreatedByFlow": source_cfg_created_by_flow}
    return {
        "environmentResourceRoot": root,
        "auth": {"type": "FSCR OAuth bearer token", "value": "<redacted>"},
        "objectName": object_name,
        "entityType": entity_type,
        "steps": [
            {"operation": "create file blob", "fileName": zip1.name},
            {"operation": "upload file blob", "zip": str(zip1)},
            {"operation": "create file blob", "fileName": zip2.name},
            {"operation": "upload file blob", "zip": str(zip2)},
            {"operation": "create upload", "payloadShape": upload_payload},
            {"operation": "retrieve compare process name"},
            {"operation": "submit compare"},
            {"operation": "poll compare process"},
            {"operation": "download compare artifacts"},
        ],
    }


def run_compare(
    *,
    access_token: str,
    root: str,
    zip1: Path,
    zip2: Path,
    object_name: str,
    entity_type: str,
    output_dir: Path,
    task_name: str | None = None,
    task_code: str | None = None,
    offering_name: str | None = None,
    offering_code: str | None = None,
    functional_area_name: str | None = None,
    functional_area_code: str | None = None,
    no_lookup_code: bool = False,
    source_cfg_created_by_flow: str | None = None,
    poll_interval_seconds: int = 20,
    timeout_minutes: int = 60,
    no_poll: bool = False,
    skip_downloads: bool = False,
    include_diagnostics: bool = False,
    artifact_names: list[str] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    zip1 = zip1.expanduser().resolve()
    zip2 = zip2.expanduser().resolve()
    validate_zip(zip1)
    validate_zip(zip2)

    if dry_run:
        codes = code_fields(task_code=task_code, offering_code=offering_code, functional_area_code=functional_area_code)
        return make_request_plan(
            root=root,
            zip1=zip1,
            zip2=zip2,
            object_name=object_name,
            entity_type=entity_type,
            codes=codes,
            source_cfg_created_by_flow=source_cfg_created_by_flow,
        )

    codes, code_resolution = resolve_codes(
        access_token=access_token,
        root=root,
        entity_type=entity_type,
        object_name=object_name,
        task_name=task_name,
        task_code=task_code,
        offering_name=offering_name,
        offering_code=offering_code,
        functional_area_name=functional_area_name,
        functional_area_code=functional_area_code,
        no_lookup_code=no_lookup_code,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {
        "environmentResourceRoot": root,
        "objectName": object_name,
        "entityType": entity_type,
        "codes": codes,
        "codeResolution": code_resolution,
        "zipFiles": [str(zip1), str(zip2)],
        "fileBlobs": [],
        "uploads": [],
        "warnings": [],
    }

    print("Creating file blob for ZIP 1...")
    blob1_id, blob1_response = create_file_blob(access_token, root, zip1)
    summary["fileBlobs"].append({"source": 1, "zip": str(zip1), "fileBlobId": blob1_id, "response": blob1_response})

    print("Uploading ZIP 1...")
    summary["fileBlobs"][0]["uploadResponse"] = upload_file_blob(access_token, root, blob1_id, zip1)

    print("Creating file blob for ZIP 2...")
    blob2_id, blob2_response = create_file_blob(access_token, root, zip2)
    summary["fileBlobs"].append({"source": 2, "zip": str(zip2), "fileBlobId": blob2_id, "response": blob2_response})

    print("Uploading ZIP 2...")
    summary["fileBlobs"][1]["uploadResponse"] = upload_file_blob(access_token, root, blob2_id, zip2)

    print("Creating upload process for ZIP 1...")
    upload1_id, upload1_name, upload1_response = create_upload(
        access_token,
        root,
        blob1_id,
        codes,
        source_cfg_created_by_flow,
    )
    summary["uploads"].append({"source": 1, "uploadProcessId": upload1_id, "sourceName": upload1_name, "response": upload1_response})

    print("Creating upload process for ZIP 2...")
    upload2_id, upload2_name, upload2_response = create_upload(
        access_token,
        root,
        blob2_id,
        codes,
        source_cfg_created_by_flow,
    )
    summary["uploads"].append({"source": 2, "uploadProcessId": upload2_id, "sourceName": upload2_name, "response": upload2_response})

    print("Retrieving compare process name...")
    compare_name, name_response = retrieve_compare_name(access_token, root, object_name, upload1_name, upload2_name)
    summary["compareProcessName"] = compare_name
    summary["retrieveCompareProcessNameResponse"] = name_response

    print("Submitting compare...")
    compare_process_id, submit_response = submit_compare(access_token, root, upload1_id, upload2_id, compare_name, codes)
    summary["compareProcessId"] = compare_process_id
    summary["submitCompareResponse"] = submit_response

    if no_poll:
        summary["finalStatus"] = "SUBMITTED"
        summary["pollingSkipped"] = True
    else:
        print(f"Polling compare process {compare_process_id}...")
        status, status_detail = poll_compare(access_token, root, compare_process_id, poll_interval_seconds, timeout_minutes)
        summary["finalStatus"] = status
        summary["statusDetail"] = status_detail

    artifacts = list(artifact_names or DEFAULT_ARTIFACTS)
    if include_diagnostics and "COMPARISON_DIAGNOSTICS_PACKAGE_ZIP" not in artifacts:
        artifacts.append("COMPARISON_DIAGNOSTICS_PACKAGE_ZIP")

    if not skip_downloads and summary.get("finalStatus") != "SUBMITTED":
        print("Downloading compare artifacts...")
        downloaded, warnings = download_artifacts(access_token, root, compare_process_id, output_dir, artifacts)
        summary["artifacts"] = downloaded
        summary["objectCounts"] = parse_comparison_counts(downloaded)
        summary["warnings"].extend(warnings)

    process_output = output_dir / f"compare_{summary.get('compareProcessId', 'submitted')}_process_output.json"
    standard_report = output_dir / f"compare_{summary.get('compareProcessId', 'submitted')}_standard_report.md"
    summary["processOutputPath"] = str(process_output.resolve())
    summary["standardReportPath"] = str(standard_report.resolve())
    standard_report.write_text(render_standard_report(summary), encoding="utf-8")
    process_output.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary
