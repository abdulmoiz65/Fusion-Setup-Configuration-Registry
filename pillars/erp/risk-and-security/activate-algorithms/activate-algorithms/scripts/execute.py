#!/usr/bin/env python3
"""Preview, publish, or inventory Risk Management algorithms for Activate Algorithms."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / "core" / "project-mgmt" / "scripts"))

from token_usage_logger import append_token_usage_log


SKILL_ID = "erp.risk-and-security.activate-algorithms.activate-algorithms"
PROVIDED_ALGORITHMS = "/api/boss/data/objects/ora/riskMgmtRisk/advancedControlsCore/v1/providedAlgorithms"
ALGORITHM_CONTEXTS = "/api/boss/data/objects/ora/riskMgmtRisk/advancedControlsCore/v1/algorithmContexts"
ALGORITHM_CONTEXTS_BULK = f"{ALGORITHM_CONTEXTS}/$bulk"
ACCESS_ALGORITHM_CONTEXTS = "/api/boss/data/objects/ora/riskMgmtRisk/accessControls/v1/accessAlgorithmContexts"
ACCESS_ALGORITHM_CONTEXTS_BULK = f"{ACCESS_ALGORITHM_CONTEXTS}/$bulk"
TRANSACTION_ALGORITHM_CONTEXTS = "/api/boss/data/objects/ora/riskMgmtRisk/transactionControls/v1/transactionAlgorithmContexts"
TRANSACTION_ALGORITHM_CONTEXTS_BULK = f"{TRANSACTION_ALGORITHM_CONTEXTS}/$bulk"
PROVIDED_ACCESS_ALGORITHMS = "/api/boss/data/objects/ora/riskMgmtRisk/accessControls/v1/providedAccessAlgorithms"
PROVIDED_TRANSACTION_ALGORITHMS = "/api/boss/data/objects/ora/riskMgmtRisk/transactionControls/v1/providedTransactionAlgorithms"
ALL_ALGORITHMS = "/api/boss/extraction/queries/ora/riskMgmtRisk/advancedControlsCore/v1/allAlgorithms"
DEFAULT_REFERENCE_CODE_WORKBOOK = Path(__file__).resolve().parents[1] / "reference-data" / "algorithms.xlsx"
ACTIVE_MODULES_HANDOFF_SOURCE = "ACTIVE_MODULES_IDENTIFICATION"
REFERENCE_CODE_COLUMN = "Reference Code"
REFERENCE_CODE_PATTERN = re.compile(r"AL\.\d{5}\.ORA")
XLSX_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
INLINE_ALGORITHM_TABLE_LIMIT = 25
ALGORITHM_TABLE_HEADERS = ["Business process", "Algorithm", "Reference", "Status", "Action"]
NO_ELIGIBLE_ALGORITHMS_MESSAGE = (
    "No eligible provided algorithms were found for the confirmed business processes. "
    "No publication is needed."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def checksum(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def canonical_digest(value: Any) -> str:
    return checksum(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def response_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    items = payload.get("items", payload.get("Items", []))
    if not isinstance(items, list):
        raise ValueError("BOSS collection response did not contain an items array")
    return [item for item in items if isinstance(item, dict)]


def q(value: str) -> str:
    return value.replace("'", "''")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--environment", required=True)
    parser.add_argument(
        "--active-modules-handoff",
        help="Optional confirmed handoff from Activate Algorithms' internal Identify Active Modules phase. When omitted, the runner reuses the latest confirmed handoff for the environment or blocks until that phase is completed and confirmed.",
    )
    parser.add_argument(
        "--reference-code-workbook",
        default=str(DEFAULT_REFERENCE_CODE_WORKBOOK),
        help="Workbook containing the Reference Code allow-list. Defaults to the maintained Activate Algorithms workbook.",
    )
    parser.add_argument("--mode", choices=("preview", "live"), default="preview")
    parser.add_argument(
        "--published-inventory",
        action="store_true",
        help="List all currently published Risk Management algorithms in the selected environment.",
    )
    # The digest is an internal approval-integrity control.  The orchestration
    # layer supplies it after recording the customer's plain-language approval;
    # customers must never be asked to copy or manage it.
    parser.add_argument("--approved-plan-digest", help=argparse.SUPPRESS)
    parser.add_argument("--core-response", action="append", default=[], help="Repeat as request_id=Core-result.json.")
    parser.add_argument("--request-plan-output", help="Path for the next Core BOSS request manifest.")
    args = parser.parse_args()
    if Path(args.project_id).name != args.project_id or args.project_id in {".", ".."}:
        parser.error("--project-id must be a single project directory name")
    if args.mode == "live" and not args.approved_plan_digest:
        parser.error("--approved-plan-digest is required for live publication")
    if args.mode == "preview" and args.approved_plan_digest:
        parser.error("--approved-plan-digest is valid only with --mode live")
    if args.published_inventory and args.mode != "preview":
        parser.error("--published-inventory is read-only and requires --mode preview")
    return args


def core_request_id(method: str, endpoint: str, query: dict[str, str] | None = None, body: dict[str, Any] | None = None, headers: dict[str, str] | None = None) -> str:
    material = {"method": method, "endpoint": endpoint, "query": query or {}, "body": body, "headers": headers or {}}
    return f"boss-{hashlib.sha256(json.dumps(material, sort_keys=True, separators=(',', ':')).encode()).hexdigest()[:16]}"


def core_request(method: str, endpoint: str, query: dict[str, str] | None = None, body: dict[str, Any] | None = None, headers: dict[str, str] | None = None) -> dict[str, Any]:
    request = {"id": core_request_id(method, endpoint, query, body, headers), "service": "boss", "method": method, "endpoint": endpoint}
    if query:
        request["query"] = query
    if body is not None:
        request["body"] = body
    if headers:
        request["headers"] = headers
    return request


class CoreResponseRequired(Exception):
    def __init__(self, request: dict[str, Any]) -> None:
        self.request = request
        super().__init__(f"Core result is required for {request['id']}")


class CoreResponseError(Exception):
    def __init__(self, status_code: int, endpoint: str) -> None:
        self.status_code = status_code
        self.endpoint = endpoint
        super().__init__(f"Core result for {endpoint} reported HTTP {status_code}")


class BulkResponseError(RuntimeError):
    """Describe a bulk response failure and, when available, its item indexes."""

    def __init__(self, message: str, failed_indexes: list[int] | None = None) -> None:
        self.failed_indexes = failed_indexes
        super().__init__(message)


class CoreResponsesRequired(Exception):
    def __init__(self, requests: list[dict[str, Any]]) -> None:
        self.requests = requests
        super().__init__(f"Core results are required for {len(requests)} requests")


class CoreResultClient:
    """Local Core-result interpreter; it never performs HTTP or OAuth work."""

    def __init__(self, args: argparse.Namespace) -> None:
        self.responses: dict[str, dict[str, Any]] = {}
        for specification in getattr(args, "core_response", []):
            request_id, separator, result_path = specification.partition("=")
            if not separator or not request_id or not result_path or request_id in self.responses:
                raise ValueError("--core-response must be a unique request_id=Core-result.json")
            value = json.loads(Path(result_path).read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                raise ValueError(f"Core result {request_id} must be a JSON object")
            self.responses[request_id] = value

    def _result(self, method: str, endpoint: str, query: dict[str, str] | None = None, body: dict[str, Any] | None = None, headers: dict[str, str] | None = None) -> tuple[dict[str, Any], dict[str, str], int]:
        request = core_request(method, endpoint, query, body, headers)
        request_id = request["id"]
        if request_id not in self.responses:
            raise CoreResponseRequired(request)
        result = self.responses[request_id]
        status = result.get("status", 200)
        if not isinstance(status, int):
            raise ValueError(f"Core result {request_id} has an invalid status")
        payload = result.get("body", result)
        if not isinstance(payload, dict):
            raise ValueError(f"Core result {request_id} must contain an object body")
        response_headers = result.get("headers", {})
        if not isinstance(response_headers, dict) or not all(isinstance(key, str) and isinstance(value, str) for key, value in response_headers.items()):
            raise ValueError(f"Core result {request_id} has invalid headers")
        if status >= 400:
            raise CoreResponseError(status, endpoint)
        return payload, response_headers, status

    def get(self, endpoint: str, query: dict[str, str]) -> tuple[dict[str, Any], dict[str, str]]:
        payload, headers, _ = self._result("GET", endpoint, query)
        return payload, headers

    def write(self, method: str, endpoint: str, body: dict[str, Any], headers: dict[str, str] | None = None) -> int:
        _, _, status = self._result(method, endpoint, body=body, headers=headers)
        return status

    def write_response(self, method: str, endpoint: str, body: dict[str, Any]) -> tuple[dict[str, Any], int]:
        payload, _, status = self._result(method, endpoint, body=body)
        return payload, status

    def has_response(self, request: dict[str, Any]) -> bool:
        return request["id"] in self.responses

    def payload_for(self, request: dict[str, Any]) -> dict[str, Any]:
        payload, _, _ = self._result(
            request["method"],
            request["endpoint"],
            request.get("query"),
            request.get("body"),
            request.get("headers"),
        )
        return payload


def load_active_modules(path: Path) -> tuple[set[str], bool, str]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict) or value.get("confirmed") is not True:
        raise ValueError("Identify Active Modules input must be a confirmed JSON object")
    levels = value.get("active_process_level_twos")
    if not isinstance(levels, list) or not all(isinstance(item, str) and item.strip() for item in levels):
        raise ValueError("Identify Active Modules input must contain non-empty active_process_level_twos")
    is_mock = value.get("source") == "MOCK_ACTIVE_MODULES"
    return {item.strip() for item in levels}, is_mock, checksum(raw)


def active_modules_handoff_folder(project_root: Path) -> Path:
    return project_root / "artifacts" / "pillars" / "erp" / "risk-and-security" / "activate-algorithms" / "activate-algorithms" / "current"


def latest_confirmed_active_modules_handoff(project_root: Path, environment: str) -> Path | None:
    """Find the newest genuine Identify Active Modules handoff for this environment.

    Activate Algorithms deliberately does not accept an unconfirmed proposal from automatic
    discovery. The active-process list controls the later publication scope.
    """

    candidates: list[tuple[float, Path]] = []
    for path in active_modules_handoff_folder(project_root).glob("active-modules-handoff-confirmed-*.json"):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            levels = value.get("active_process_level_twos") if isinstance(value, dict) else None
            if (
                value.get("source") == ACTIVE_MODULES_HANDOFF_SOURCE
                and value.get("confirmed") is True
                and value.get("environment") == environment
                and isinstance(levels, list)
                and all(isinstance(item, str) and item.strip() for item in levels)
            ):
                candidates.append((path.stat().st_mtime, path))
        except (OSError, json.JSONDecodeError, AttributeError):
            continue
    return max(candidates, default=(0.0, None), key=lambda candidate: candidate[0])[1]


def persist_active_modules_dependency_blocked(project_root: Path, args: argparse.Namespace, started_at: str) -> None:
    """Leave a compact blocker record when the confirmed prerequisite is unavailable."""

    timestamp = utc_now()
    suffix = timestamp.replace(":", "").replace("-", "")
    target = active_modules_handoff_folder(project_root)
    diagnostic_path = target / f"active-modules-confirmation-required-{suffix}.json"
    run_path = project_root / "state" / "runs" / f"{SKILL_ID}-awaiting-active-modules-confirmation-{suffix}.json"
    diagnostic = {
        "skill_id": SKILL_ID,
        "stage": "active_modules_handoff_resolution",
        "status": "blocked",
        "failure_class": "approval_blocker",
        "environment": args.environment,
        "message": "No confirmed active-process handoff is available for this environment.",
        "recommended_action": "Complete and confirm Activate Algorithms' internal Identify Active Modules phase for this environment, then rerun the local publisher.",
    }
    write_json(diagnostic_path, diagnostic)
    write_json(run_path, {
        "skill_id": SKILL_ID,
        "stage": "active_modules_handoff_resolution",
        "status": "blocked",
        "failure_class": "approval_blocker",
        "environment": args.environment,
        "artifacts": [str(diagnostic_path.relative_to(project_root))],
        "recommended_action": diagnostic["recommended_action"],
    })
    append_token_usage_log(
        project_id=args.project_id,
        skill_id=SKILL_ID,
        task="Obtain internal Identify Active Modules active-process handoff",
        trigger="Activate Algorithms missing confirmed internal active-process handoff",
        activity_start_time=started_at,
        artifact_paths=[diagnostic_path, run_path],
        files_read=0,
        estimated_input_tokens=1,
        notes="Activate Algorithms' internal Identify Active Modules phase has no confirmed handoff for this environment. The local publisher stopped before algorithm evaluation and issued no Fusion operation.",
        root=ROOT,
    )


def resolve_active_modules_input(args: argparse.Namespace, project_root: Path, started_at: str) -> Path | None:
    if args.active_modules_handoff:
        return Path(args.active_modules_handoff)
    confirmed = latest_confirmed_active_modules_handoff(project_root, args.environment)
    if confirmed:
        return confirmed
    persist_active_modules_dependency_blocked(project_root, args, started_at)
    return None


def column_index(reference: str) -> int:
    value = 0
    for character in re.match(r"[A-Z]+", reference).group(0):
        value = value * 26 + ord(character) - ord("A") + 1
    return value - 1


def xlsx_cell_value(cell: ElementTree.Element, shared_strings: list[str]) -> str:
    cell_type = cell.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.iter(XLSX_NS + "t"))
    raw = cell.findtext(XLSX_NS + "v") or ""
    return shared_strings[int(raw)] if cell_type == "s" and raw else raw


def read_first_worksheet_rows(path: Path) -> list[list[str]]:
    """Read customer workbook values without transforming or persisting JSON."""

    with zipfile.ZipFile(path) as workbook:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in workbook.namelist():
            root = ElementTree.fromstring(workbook.read("xl/sharedStrings.xml"))
            shared_strings = ["".join(node.text or "" for node in item.iter(XLSX_NS + "t")) for item in root.findall(XLSX_NS + "si")]
        sheet = ElementTree.fromstring(workbook.read("xl/worksheets/sheet1.xml"))
    rows: list[list[str]] = []
    for row in sheet.findall(".//" + XLSX_NS + "row"):
        values: list[str] = []
        for cell in row.findall(XLSX_NS + "c"):
            index = column_index(cell.get("r", "A1"))
            values.extend([""] * max(0, index - len(values)))
            values.append(xlsx_cell_value(cell, shared_strings).strip())
        rows.append(values)
    return rows


def load_reference_code_workbook(path: Path) -> tuple[set[str], str]:
    if not path.is_file() or path.suffix.casefold() != ".xlsx":
        raise ValueError("Reference Code allow-list workbook must name an existing .xlsx file")
    raw = path.read_bytes()
    rows = read_first_worksheet_rows(path)
    if not rows:
        raise ValueError("Reference Code allow-list workbook is empty")
    header_indexes = [index for index, value in enumerate(rows[0]) if value == REFERENCE_CODE_COLUMN]
    if len(header_indexes) != 1:
        raise ValueError(f"Reference Code allow-list workbook must contain exactly one {REFERENCE_CODE_COLUMN!r} column")

    column = header_indexes[0]
    allowlist: set[str] = set()
    for source_row, values in enumerate(rows[1:], start=2):
        reference_code = values[column].strip() if column < len(values) else ""
        if not REFERENCE_CODE_PATTERN.fullmatch(reference_code):
            continue
        if reference_code in allowlist:
            raise ValueError(f"Reference Code allow-list workbook row {source_row} duplicates reference code {reference_code}")
        allowlist.add(reference_code)
    if not allowlist:
        raise ValueError("Reference Code allow-list workbook contains no exact reference codes")
    return allowlist, checksum(raw)


# BOSS does not support an OData-style $expand parameter.  Relationships are
# expanded by asking for their dotted fields.  These are deliberately explicit:
# the detailed view's defaults do not include an AlgorithmContext's publication
# state nor the associated process Level 2 value needed for the local match.
PROVIDED_ALGORITHM_FIELDS = (
    "id,referenceCode,name,type,modeType,resultType,"
    "algorithmReferenceDataAttributes.algorithmReferenceType,"
    "algorithmReferenceDataAttributes.referenceKey,"
    "algorithmReferenceDataAttributes.processDataValue.levelTwo"
)
PROVIDED_ALGORITHMS_PAGE_SIZE = 100
CONTEXT_PAGE_SIZE = 100
ACCESS_TYPES = {"SOD_ACCESS_MONITOR", "SENSITIVE_ACCESS_MONITOR"}
TRANSACTION_TYPES = {"TRANSACTION_MONITOR", "CONFIGURATION_MONITOR"}
REQUIRED_RESULT_TYPE = "EXPORT_FILE"
ACCESS_CONTEXT_CREATE_FIELDS = ("userProvisionFlag", "resultType", "taskType", "taskAutocloseFlag")
TRANSACTION_CONTEXT_CREATE_FIELDS = (
    "userProvisionFlag",
    "resultType",
    "taskType",
    "taskAutocloseFlag",
    "resultAggregate",
    "userAssignmentType",
    "logic",
)


def provided_algorithms_query(offset: int, process_level_twos: set[str]) -> dict[str, str]:
    if not process_level_twos:
        raise ValueError("At least one confirmed active Level 2 process is required")
    level_two_values = ",".join(f"'{q(level_two)}'" for level_two in sorted(process_level_twos))
    return {
        "$fields": PROVIDED_ALGORITHM_FIELDS,
        "$limit": str(PROVIDED_ALGORITHMS_PAGE_SIZE),
        "$offset": str(offset),
        "$sortBy": "id:asc",
        "$filter": "algorithmReferenceDataAttributes[algorithmReferenceType='Process' AND referenceKey='PROCESSES.ORA' AND processDataValue.levelTwo IN (" + level_two_values + ")]",
    }


def paginated_items(client: CoreResultClient, endpoint: str, query_for_offset: Any) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    offset = 0
    while True:
        payload, _ = client.get(endpoint, query_for_offset(offset))
        page = response_items(payload)
        items.extend(page)
        if payload.get("hasMore") is not True:
            return items
        if not page:
            raise ValueError(f"{endpoint} reported hasMore but returned an empty page")
        offset += len(page)


def items_for_active_processes(client: CoreResultClient, active_levels: set[str]) -> list[dict[str, Any]]:
    """Read the one filtered provided-algorithm collection, 100 records per page."""

    return paginated_items(client, PROVIDED_ALGORITHMS, lambda offset: provided_algorithms_query(offset, active_levels))


def algorithm_process_level_twos(algorithm: dict[str, Any], active_levels: set[str]) -> set[str]:
    """Return active Level 2 associations from the explicitly expanded fields."""

    references = algorithm.get("algorithmReferenceDataAttributes")
    if not isinstance(references, dict):
        raise ValueError("Provided algorithm did not return expanded algorithmReferenceDataAttributes")
    reference_items = response_items(references)
    levels: set[str] = set()
    for reference in reference_items:
        if reference.get("algorithmReferenceType") != "Process" or reference.get("referenceKey") != "PROCESSES.ORA":
            continue
        process_data_value = reference.get("processDataValue")
        if not isinstance(process_data_value, dict):
            continue
        level_two = process_data_value.get("levelTwo")
        if isinstance(level_two, str) and level_two in active_levels:
            levels.add(level_two)
    return levels


def collect_allowlisted_algorithms(client: CoreResultClient, active_levels: set[str], allowlist: set[str]) -> list[dict[str, Any]]:
    """Return provided, allow-listed candidates from the one Level-2-filtered collection."""

    candidates: dict[str, dict[str, Any]] = {}
    for algorithm in items_for_active_processes(client, active_levels):
        reference_code = algorithm.get("referenceCode")
        if not isinstance(reference_code, str) or reference_code not in allowlist:
            continue
        process_level_twos = algorithm_process_level_twos(algorithm, active_levels)
        if not process_level_twos:
            raise ValueError(f"Allow-listed provided algorithm {reference_code} did not return an expanded active Level 2 process association")
        algorithm_id = algorithm.get("id")
        algorithm_type = algorithm.get("type")
        if algorithm_id is None or not str(algorithm_id).strip() or not isinstance(algorithm_type, str):
            raise ValueError(f"Allow-listed provided algorithm {reference_code} did not expose an id and type")
        candidate = candidates.setdefault(reference_code, {
            "algorithm_id": str(algorithm_id),
            "algorithm_name": algorithm.get("name"),
            "algorithm_number": str(int(reference_code.split(".")[1])),
            "reference_code": reference_code,
            "algorithm_type": algorithm_type,
            "process_level_twos": set(),
            "provided_mode": algorithm.get("modeType"),
            "provided_result_type": algorithm.get("resultType"),
            "source_evidence": "Reference Code allow-list",
            "mapping_source": "reference_code_allowlist",
        })
        if candidate["algorithm_id"] != str(algorithm_id) or candidate["algorithm_type"] != algorithm_type:
            raise ValueError(f"Reference code {reference_code} resolved to conflicting provided algorithms")
        candidate["process_level_twos"].update(process_level_twos)
    return [{**candidate, "process_level_twos": sorted(candidate["process_level_twos"])} for _, candidate in sorted(candidates.items())]


def context_etag(context: dict[str, Any]) -> str | None:
    metadata = context.get("$context")
    etag = metadata.get("etag") if isinstance(metadata, dict) else None
    return etag if isinstance(etag, str) and etag else None


def chunks(values: list[str], size: int = CONTEXT_PAGE_SIZE) -> list[list[str]]:
    return [values[start:start + size] for start in range(0, len(values), size)]


def ids_query(algorithm_ids: list[str], fields: str | None) -> dict[str, str]:
    query = {"$filter": f"id IN ({','.join(algorithm_ids)})", "$limit": str(CONTEXT_PAGE_SIZE), "$offset": "0", "$sortBy": "id:asc"}
    if fields:
        query["$fields"] = fields
    return query


PARENT_CONTEXT_FIELDS = "id,modeType,resultType,userProvisionFlag,taskType,taskAutocloseFlag,resultAggregate,userAssignmentType"
ACCESS_CONTEXT_FIELDS = PARENT_CONTEXT_FIELDS
TRANSACTION_CONTEXT_FIELDS = f"{PARENT_CONTEXT_FIELDS},logic"
ACCESS_SOURCE_FIELDS = "id,userProvisionFlag,resultType,taskType,taskAutocloseFlag"
TRANSACTION_SOURCE_FIELDS = f"{ACCESS_SOURCE_FIELDS},resultAggregate,userAssignmentType,logic"
ACCESS_PARENT_REFRESH_FIELDS = "id,modeType,resultType,timeUpdated"
ACCESS_CONTEXT_REFRESH_FIELDS = f"{ACCESS_CONTEXT_FIELDS},timeUpdated"


def candidate_ids(candidates: list[dict[str, Any]], algorithm_types: set[str]) -> list[str]:
    return sorted((candidate["algorithm_id"] for candidate in candidates if candidate["algorithm_type"] in algorithm_types), key=int)


def requests_for_ids(endpoint: str, ids: list[str], fields: str | None) -> list[dict[str, Any]]:
    return [core_request("GET", endpoint, ids_query(group, fields)) for group in chunks(ids)]


def pending_requests(client: CoreResultClient, requests: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [request for request in requests if not client.has_response(request)]


def read_rows_by_ids(client: CoreResultClient, endpoint: str, ids: list[str], fields: str | None, *, require_all: bool) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for request in requests_for_ids(endpoint, ids, fields):
        payload, _ = client.get(endpoint, request["query"])
        for row in response_items(payload):
            identifier = row.get("id")
            if identifier is None:
                raise ValueError(f"{endpoint} returned a row without id")
            key = str(identifier)
            if key in rows:
                raise ValueError(f"{endpoint} returned duplicate id {key}")
            rows[key] = row
    unexpected = set(rows).difference(ids)
    if unexpected:
        raise ValueError(f"{endpoint} returned unexpected ids")
    if require_all and set(rows) != set(ids):
        raise ValueError(f"{endpoint} did not return every requested id")
    return rows


def pending_context_state_requests(client: CoreResultClient, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ids = sorted((candidate["algorithm_id"] for candidate in candidates), key=int)
    requests = requests_for_ids(ALGORITHM_CONTEXTS, ids, PARENT_CONTEXT_FIELDS)
    requests.extend(requests_for_ids(ACCESS_ALGORITHM_CONTEXTS, candidate_ids(candidates, ACCESS_TYPES), ACCESS_CONTEXT_FIELDS))
    requests.extend(requests_for_ids(TRANSACTION_ALGORITHM_CONTEXTS, candidate_ids(candidates, TRANSACTION_TYPES), TRANSACTION_CONTEXT_FIELDS))
    return pending_requests(client, requests)


def context_state(client: CoreResultClient, candidates: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    ids = sorted((candidate["algorithm_id"] for candidate in candidates), key=int)
    return (
        read_rows_by_ids(client, ALGORITHM_CONTEXTS, ids, PARENT_CONTEXT_FIELDS, require_all=False),
        read_rows_by_ids(client, ACCESS_ALGORITHM_CONTEXTS, candidate_ids(candidates, ACCESS_TYPES), ACCESS_CONTEXT_FIELDS, require_all=False),
        read_rows_by_ids(client, TRANSACTION_ALGORITHM_CONTEXTS, candidate_ids(candidates, TRANSACTION_TYPES), TRANSACTION_CONTEXT_FIELDS, require_all=False),
    )


def missing_context_ids(candidates: list[dict[str, Any]], parent_rows: dict[str, dict[str, Any]], access_rows: dict[str, dict[str, Any]], transaction_rows: dict[str, dict[str, Any]]) -> tuple[list[str], list[str]]:
    missing_access: list[str] = []
    missing_transaction: list[str] = []
    for candidate in candidates:
        identifier = candidate["algorithm_id"]
        typed_rows = access_rows if candidate["algorithm_type"] in ACCESS_TYPES else transaction_rows
        if candidate["algorithm_type"] not in ACCESS_TYPES | TRANSACTION_TYPES:
            continue
        if algorithm_is_published(candidate, parent_rows.get(identifier), typed_rows.get(identifier)):
            continue
        if (identifier in parent_rows) != (identifier in typed_rows):
            raise ValueError(f"Algorithm {candidate['reference_code']} returned inconsistent parent and typed contexts")
        if identifier not in typed_rows:
            (missing_access if candidate["algorithm_type"] in ACCESS_TYPES else missing_transaction).append(identifier)
    return missing_access, missing_transaction


def pending_context_source_requests(client: CoreResultClient, missing_access: list[str], missing_transaction: list[str]) -> list[dict[str, Any]]:
    requests = requests_for_ids(PROVIDED_ACCESS_ALGORITHMS, missing_access, ACCESS_SOURCE_FIELDS)
    requests.extend(requests_for_ids(PROVIDED_TRANSACTION_ALGORITHMS, missing_transaction, TRANSACTION_SOURCE_FIELDS))
    return pending_requests(client, requests)


def create_payload(identifier: str, source: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    payload = {"id": int(identifier), **{field: source.get(field) for field in fields}}
    payload["resultType"] = REQUIRED_RESULT_TYPE
    return payload


def effective_value(context: dict[str, Any] | None, field: str, provided_value: Any) -> Any:
    value = context.get(field) if isinstance(context, dict) else None
    return value if value not in {None, ""} else provided_value


def algorithm_is_published(candidate: dict[str, Any], parent_context: dict[str, Any] | None, typed_context: dict[str, Any] | None) -> bool:
    """Return whether any supplied algorithm or context source is published."""

    return candidate.get("provided_mode") == "PUBLISHED" or (
        isinstance(parent_context, dict) and parent_context.get("modeType") == "PUBLISHED"
    ) or (
        isinstance(typed_context, dict) and typed_context.get("modeType") == "PUBLISHED"
    )


def classify(candidate: dict[str, Any], parent_rows: dict[str, dict[str, Any]], access_rows: dict[str, dict[str, Any]], transaction_rows: dict[str, dict[str, Any]], access_sources: dict[str, dict[str, Any]], transaction_sources: dict[str, dict[str, Any]]) -> dict[str, Any]:
    result = {key: candidate[key] for key in ("algorithm_number", "algorithm_name", "algorithm_id", "reference_code", "algorithm_type", "process_level_twos", "source_evidence", "mapping_source")}
    identifier = candidate["algorithm_id"]
    if candidate["algorithm_type"] in ACCESS_TYPES:
        context, source, kind, create_fields = access_rows.get(identifier), access_sources.get(identifier), "access", ACCESS_CONTEXT_CREATE_FIELDS
    elif candidate["algorithm_type"] in TRANSACTION_TYPES:
        context, source, kind, create_fields = transaction_rows.get(identifier), transaction_sources.get(identifier), "transaction", TRANSACTION_CONTEXT_CREATE_FIELDS
    else:
        result.update({"classification": "failed_read_or_validation", "reason": "Algorithm type is not supported by the publication workflow."})
        return result
    parent_context = parent_rows.get(identifier)
    if algorithm_is_published(candidate, parent_context, context):
        result.update({
            "current_effective_mode": "PUBLISHED",
            "current_result_type": effective_value(context, "resultType", candidate.get("provided_result_type")),
            "context_kind": kind,
            "classification": "already_published",
            "reason": "The provided algorithm or one of its contexts is already published.",
        })
        return result
    if (identifier in parent_rows) != (context is not None):
        result.update({"classification": "failed_read_or_validation", "reason": "The algorithm's shared and type-specific contexts are inconsistent."})
        return result
    mode = effective_value(context, "modeType", candidate.get("provided_mode"))
    result_type = effective_value(context, "resultType", candidate.get("provided_result_type"))
    result.update({"current_effective_mode": mode, "current_result_type": result_type, "context_kind": kind})
    if context is None:
        if source is None:
            result.update({"classification": "failed_read_or_validation", "reason": "The provided type-specific algorithm settings could not be confirmed."})
        else:
            result.update({"classification": "ready_to_publish", "operation": "CREATE", "create_payload": create_payload(identifier, source, create_fields), "expected_result_type": REQUIRED_RESULT_TYPE, "reason": "No customer algorithm context exists."})
    elif mode in {None, "", "DRAFT", "ARCHIVE"} and context_etag(context):
        result.update({"classification": "ready_to_publish", "operation": "UPDATE", "bulk_etag": context_etag(context), "reason": "Existing non-published configuration will be published without changing its result action."})
    elif mode in {None, "", "DRAFT", "ARCHIVE"}:
        result.update({"classification": "failed_read_or_validation", "reason": "The current algorithm context did not provide a concurrency token for publication."})
    else:
        result.update({"classification": "skipped_non_export_result_action", "reason": "Existing algorithm configuration is not eligible for publication."})
    return result


def publication_plan(items: list[dict[str, Any]], environment: str, active_modules_checksum: str, allowlist_checksum: str) -> dict[str, Any]:
    actions = [{key: item[key] for key in ("algorithm_number", "reference_code", "algorithm_id", "algorithm_type", "context_kind", "operation", "expected_result_type") if key in item} for item in items if item.get("classification") == "ready_to_publish"]
    plan = {"skill_id": SKILL_ID, "environment": environment, "active_modules_checksum_sha256": active_modules_checksum, "reference_code_workbook_checksum_sha256": allowlist_checksum, "actions": actions}
    plan["digest_sha256"] = canonical_digest(plan)
    return plan


def bulk_request(endpoint: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    return core_request("POST", f"{endpoint}/$bulk", body={"items": items})


def access_create_request(items: list[dict[str, Any]]) -> dict[str, Any] | None:
    actions = [item for item in items if item.get("classification") == "ready_to_publish" and item.get("context_kind") == "access" and item.get("operation") == "CREATE"]
    return bulk_request(ACCESS_ALGORITHM_CONTEXTS, [{"$operation": "CREATE", **item["create_payload"]} for item in actions]) if actions else None


def transaction_publication_request(items: list[dict[str, Any]]) -> dict[str, Any] | None:
    actions = [item for item in items if item.get("classification") == "ready_to_publish" and item.get("context_kind") == "transaction"]
    if not actions:
        return None
    bulk_items: list[dict[str, Any]] = []
    for item in actions:
        if item["operation"] == "CREATE":
            bulk_items.append({"$operation": "CREATE", **item["create_payload"], "modeType": "PUBLISHED"})
        else:
            bulk_items.append({"$operation": "UPDATE", "$id": item["algorithm_id"], "$context": {"etag": item["bulk_etag"]}, "modeType": "PUBLISHED"})
    return bulk_request(TRANSACTION_ALGORITHM_CONTEXTS, bulk_items)


def validate_bulk_response(payload: dict[str, Any], expected_count: int) -> None:
    responses = payload.get("items")
    if not isinstance(responses, list) or len(responses) != expected_count:
        actual = len(responses) if isinstance(responses, list) else 0
        raise BulkResponseError(f"Algorithm-context bulk response returned {actual} item(s); expected {expected_count}")
    failed_indexes = [index for index, response in enumerate(responses) if not isinstance(response, dict) or not isinstance(response.get("$statusCode"), int) or not 200 <= response["$statusCode"] < 300]
    if failed_indexes:
        raise BulkResponseError(f"Algorithm-context bulk response contains non-success item(s) at indexes: {','.join(map(str, failed_indexes))}", failed_indexes)


def execute_bulk(client: CoreResultClient, request: dict[str, Any] | None) -> int | None:
    if request is None:
        return None
    response, status = client.write_response(request["method"], request["endpoint"], request["body"])
    validate_bulk_response(response, len(request["body"]["items"]))
    return status


def access_refresh_requests(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ids = sorted((item["algorithm_id"] for item in items if item.get("classification") == "ready_to_publish" and item.get("context_kind") == "access"), key=int)
    return requests_for_ids(ACCESS_ALGORITHM_CONTEXTS, ids, ACCESS_CONTEXT_REFRESH_FIELDS) + requests_for_ids(ALGORITHM_CONTEXTS, ids, ACCESS_PARENT_REFRESH_FIELDS)


def access_parent_publication_request(items: list[dict[str, Any]], refreshed_access: dict[str, dict[str, Any]], refreshed_parent: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    bulk_items: list[dict[str, Any]] = []
    for item in items:
        if item.get("classification") != "ready_to_publish" or item.get("context_kind") != "access":
            continue
        identifier = item["algorithm_id"]
        typed_context = refreshed_access.get(identifier)
        parent_context = refreshed_parent.get(identifier)
        if typed_context is None or parent_context is None:
            raise RuntimeError("Access publication refresh did not return every target context")
        mode = typed_context.get("modeType")
        if mode == "PUBLISHED":
            continue
        if mode not in {None, "", "DRAFT", "ARCHIVE"}:
            raise RuntimeError("Access algorithm changed after preview; prepare a fresh preview before publication")
        etag = context_etag(parent_context)
        if not etag:
            raise RuntimeError("Access parent context did not return a fresh change identifier")
        publication = {"$operation": "UPDATE", "$id": identifier, "$context": {"etag": etag}, "modeType": "PUBLISHED"}
        if item["operation"] == "CREATE":
            publication["resultType"] = REQUIRED_RESULT_TYPE
        bulk_items.append(publication)
    return bulk_request(ALGORITHM_CONTEXTS, bulk_items) if bulk_items else None


def effective_verification_requests(client: CoreResultClient, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ids = sorted((item["algorithm_id"] for item in items if item.get("classification") == "ready_to_publish"), key=int)
    requests = requests_for_ids(ALL_ALGORITHMS, ids, None)
    return pending_requests(client, requests)


def verify_effective_algorithms(client: CoreResultClient, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Verify each changed algorithm, rereading only IDs omitted from a bounded page."""

    actions = [item for item in items if item.get("classification") == "ready_to_publish"]
    ids = sorted((item["algorithm_id"] for item in actions), key=int)
    verified: dict[str, dict[str, Any]] = {}
    for request in requests_for_ids(ALL_ALGORITHMS, ids, None):
        payload, _ = client.get(ALL_ALGORITHMS, request["query"])
        for row in response_items(payload):
            identifier = row.get("id")
            if identifier is not None and str(identifier) in ids:
                verified[str(identifier)] = row
    omitted = [identifier for identifier in ids if identifier not in verified]
    singleton_requests = [core_request("GET", ALL_ALGORITHMS, ids_query([identifier], None)) for identifier in omitted]
    pending = [request for request in singleton_requests if not client.has_response(request)]
    if pending:
        raise CoreResponsesRequired(pending)
    for request in singleton_requests:
        payload, _ = client.get(ALL_ALGORITHMS, request["query"])
        rows = response_items(payload)
        if len(rows) == 1 and rows[0].get("id") is not None:
            verified[str(rows[0]["id"])] = rows[0]
    results: list[dict[str, Any]] = []
    for item in actions:
        verified_row = verified.get(item["algorithm_id"])
        is_published = verified_row and verified_row.get("modeType") == "PUBLISHED"
        has_expected_result = item["operation"] != "CREATE" or (
            verified_row and verified_row.get("resultType") == REQUIRED_RESULT_TYPE
        )
        status = "published" if is_published and has_expected_result else "failed"
        result = {"algorithm_number": item["algorithm_number"], "reference_code": item.get("reference_code"), "algorithm_id": item["algorithm_id"], "status": status}
        if status == "failed":
            result["message"] = "The changed context could not be verified as published."
            result["verification_failed"] = True
        results.append(result)
    return results


def publish_ready_items(client: CoreResultClient, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Run the ordered typed bulk workflow and verify its effective publication state."""

    actions = [item for item in items if item.get("classification") == "ready_to_publish"]
    if not actions:
        return []
    current_request: dict[str, Any] | None = None
    try:
        access_create = access_create_request(items)
        if access_create and not client.has_response(access_create):
            raise CoreResponseRequired(access_create)
        current_request = access_create
        execute_bulk(client, access_create)

        transaction_publish = transaction_publication_request(items)
        if transaction_publish and not client.has_response(transaction_publish):
            raise CoreResponseRequired(transaction_publish)
        current_request = transaction_publish
        execute_bulk(client, transaction_publish)

        refresh_requests = pending_requests(client, access_refresh_requests(items))
        if refresh_requests:
            raise CoreResponsesRequired(refresh_requests)
        access_ids = candidate_ids(actions, ACCESS_TYPES)
        refreshed_access = read_rows_by_ids(client, ACCESS_ALGORITHM_CONTEXTS, access_ids, ACCESS_CONTEXT_REFRESH_FIELDS, require_all=True)
        refreshed_parent = read_rows_by_ids(client, ALGORITHM_CONTEXTS, access_ids, ACCESS_PARENT_REFRESH_FIELDS, require_all=True)
        access_publish = access_parent_publication_request(items, refreshed_access, refreshed_parent)
        if access_publish and not client.has_response(access_publish):
            raise CoreResponseRequired(access_publish)
        current_request = access_publish
        execute_bulk(client, access_publish)

        verification_requests = effective_verification_requests(client, items)
        if verification_requests:
            raise CoreResponsesRequired(verification_requests)
        return verify_effective_algorithms(client, items)
    except (CoreResponseRequired, CoreResponsesRequired):
        raise
    except BulkResponseError as exc:
        if current_request and exc.failed_indexes is not None:
            results = []
            for index in exc.failed_indexes:
                bulk_items = current_request["body"]["items"]
                if index >= len(bulk_items):
                    continue
                identifier = bulk_items[index].get("$id", bulk_items[index].get("id"))
                if identifier is not None:
                    results.append({"algorithm_id": str(identifier), "status": "failed", "message": str(exc)})
            if results:
                return results
        return [{"status": "failed", "message": str(exc)}]
    except Exception as exc:
        return [{"status": "failed", "message": str(exc)}]
    return [{"algorithm_number": item["algorithm_number"], "reference_code": item.get("reference_code"), "algorithm_id": item["algorithm_id"], "status": "published"} for item in actions]


def algorithm_label(item: dict[str, Any]) -> str:
    """Return a customer-readable algorithm name without implementation details."""

    return str(item.get("algorithm_name") or item.get("catalog_algorithm_name") or "Unnamed algorithm")


def reference_label(item: dict[str, Any]) -> str:
    """Return the customer-readable reference for an algorithm row."""

    return str(item.get("reference_code") or item.get("algorithm_number") or "—")


def process_names(item: dict[str, Any]) -> tuple[str, ...]:
    """Return each business process associated with an algorithm."""

    values = item.get("process_level_twos")
    if isinstance(values, list):
        names = {value.strip() for value in values if isinstance(value, str) and value.strip()}
        if names:
            return tuple(sorted(names))
    return ("Unmapped process",)


def process_label(item: dict[str, Any]) -> str:
    """Return a readable process label for compatibility with existing callers."""

    return ", ".join(process_names(item))


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    """Render a compact consultant-facing Markdown table."""

    def escape_cell(value: str) -> str:
        return str(value).replace("|", "\\|").replace("\r\n", "\n").replace("\r", "\n").replace("\n", " ")

    divider = ["---"] * len(headers)
    lines = ["| " + " | ".join(escape_cell(header) for header in headers) + " |", "| " + " | ".join(divider) + " |"]
    lines.extend("| " + " | ".join(escape_cell(cell) for cell in row) + " |" for row in rows)
    return "\n".join(lines)


def consultant_outcome(item: dict[str, Any], mode: str, live_results: list[dict[str, Any]] | None = None) -> str | None:
    """Return the allowed customer outcome for an item and its verified live result."""

    classification = item.get("classification")
    if classification == "ready_to_publish":
        if mode == "preview":
            return "Publish"
        result_by_id = {str(result.get("algorithm_id")): result for result in live_results or [] if result.get("algorithm_id") is not None}
        result = result_by_id.get(str(item.get("algorithm_id")))
        if result is None:
            return "Not published"
        if result.get("status") == "published":
            return "Published"
        return "Not published"
    if classification == "already_published":
        return "Already published"
    return "Not published"


def algorithm_status_and_action(item: dict[str, Any], mode: str, live_results: list[dict[str, Any]] | None = None) -> tuple[str, str] | None:
    """Return the safe customer-facing status and action for one algorithm."""

    outcome = consultant_outcome(item, mode, live_results)
    if outcome is None:
        return None
    if outcome == "Publish":
        return "Not published", "Publish"
    if outcome == "Already published":
        return "Already published", "—"
    return outcome, "—"


def sorted_algorithm_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(items, key=lambda item: (process_label(item), algorithm_label(item)))


def group_items_by_process(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Group algorithms under each associated process in stable display order."""

    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        for process in process_names(item):
            grouped.setdefault(process, []).append(item)
    return {process: sorted(grouped[process], key=algorithm_label) for process in sorted(grouped)}


def algorithm_table_rows(mode: str, items: list[dict[str, Any]], live_results: list[dict[str, Any]] | None = None, actionable_only: bool = False) -> list[list[str]]:
    """Return sorted customer-facing algorithm rows for an action or complete table."""

    rows = []
    for item in sorted_algorithm_items(items):
        status_and_action = algorithm_status_and_action(item, mode, live_results)
        if status_and_action is None:
            continue
        status, action = status_and_action
        if actionable_only and action == "—":
            continue
        rows.append([process_label(item), algorithm_label(item), reference_label(item)])
    return rows


def render_algorithm_table(rows: list[list[str]]) -> str:
    """Render process, algorithm, and reference rows."""

    return markdown_table(["Business process", "Algorithm", "Reference"], rows)


def render_algorithm_review_table(mode: str, environment: str, items: list[dict[str, Any]], live_results: list[dict[str, Any]] | None = None) -> str:
    """Render the persisted complete consultant-facing algorithm register."""

    if not items:
        return NO_ELIGIBLE_ALGORITHMS_MESSAGE
    lines = [f"# Activate Algorithms — Complete Register ({environment})"]
    ready = [item for item in items if item.get("classification") == "ready_to_publish"]
    if ready:
        lines.extend(["", render_actionable_groups(ready, mode, live_results, limit=None)])
    not_published = [item for item in items if item.get("classification") not in {"ready_to_publish", "already_published"}]
    if not_published:
        rows = [[process, algorithm_label(item), reference_label(item)] for process, grouped_items in group_items_by_process(not_published).items() for item in grouped_items]
        lines.extend(["", "Algorithms not published", markdown_table(["Business process", "Algorithm", "Reference"], rows)])
    return "\n".join(lines)


def render_actionable_groups(items: list[dict[str, Any]], mode: str, live_results: list[dict[str, Any]] | None, *, limit: int | None) -> str:
    """Render actionable algorithms by process, optionally limiting each group."""

    section_title = "Algorithms to publish — not published" if mode == "preview" else "Algorithms in this publication"
    lines = [f"## {section_title}"]
    for process, grouped_items in group_items_by_process(items).items():
        heading = f"{process} — {len(grouped_items)} algorithm(s) to publish" if mode == "preview" else f"{process} — {len(grouped_items)} algorithm(s)"
        lines.extend(["", f"### {heading}"])
        shown = grouped_items if limit is None else grouped_items[:limit]
        rows = []
        for item in shown:
            row = [algorithm_label(item), reference_label(item)]
            if mode == "live":
                row.append(consultant_outcome(item, mode, live_results) or "Not published")
            rows.append(row)
        lines.append(markdown_table(["Algorithm", "Reference"] + (["Outcome"] if mode == "live" else []), rows))
        if limit is not None and len(grouped_items) > limit:
            lines.append(f"… {len(grouped_items) - limit} more to publish in {process}.")
    return "\n".join(lines)


def render_user_summary(mode: str, environment: str, items: list[dict[str, Any]], live_results: list[dict[str, Any]], review_path: Path | None = None) -> str:
    """Render the only terminal output intended for a customer-facing run."""

    if mode == "preview" and not items:
        return NO_ELIGIBLE_ALGORITHMS_MESSAGE
    title = "Preview" if mode == "preview" else "Publication results"
    lines = [f"# Activate Algorithms — {title} ({environment})"]
    ready = [item for item in items if item.get("classification") == "ready_to_publish"]
    if mode == "preview":
        lines.append(f"{len(ready)} algorithm(s) to publish.")
    needs_input = [item for item in items if item.get("classification") == "failed_read_or_validation"]

    if mode == "preview" and ready:
        lines.extend(["", render_actionable_groups(ready, mode, live_results, limit=10)])
    elif mode == "preview":
        lines.append("\nNo publication approval is needed from this preview.")

    if needs_input:
        lines.append("\nSome algorithms are not published because their current setup could not be confirmed. Those algorithms were not changed. Restore the required environment information, then review the preview again.")

    if mode == "preview" and ready:
        lines.append(f"\nNext action: review the proposed algorithms. The complete list is available on request. Do you approve publishing these {len(ready)} algorithms in {environment}?")

    if mode == "live":
        published = [result for result in live_results if result.get("status") == "published"]
        not_published = [item for item in items if consultant_outcome(item, mode, live_results) == "Not published"]
        unattributed_failure = any(result.get("status") == "failed" and result.get("algorithm_id") is None for result in live_results)
        if unattributed_failure:
            lines.append("\nNot published: the publication result could not be attributed to a specific algorithm. No additional write was made.")
        else:
            lines.append(f"\nPublished: {len(published)} algorithm(s) were verified.")
            if not_published:
                lines.append(f"Not published: {len(not_published)} algorithm(s).")

    if mode == "live" and ready:
        lines.append("A complete actionable review is available on request.")

    return "\n".join(lines)


def render_discovery_in_progress(environment: str) -> str:
    """Render the only consultant-safe message before a preview is complete."""
    return "I’m checking the current setup. I’ll return with a complete review or a clear next action."


def persist(project_root: Path, args: argparse.Namespace, started_at: str, active_modules_checksum: str, allowlist_checksum: str, mock: bool, items: list[dict[str, Any]], plan: dict[str, Any], live_results: list[dict[str, Any]]) -> tuple[Path, Path | None, Path, Path]:
    timestamp = utc_now()
    suffix = timestamp.replace(":", "").replace("-", "")
    target = active_modules_handoff_folder(project_root)
    report_path = target / f"{args.mode}-{suffix}.json"
    review_path: Path | None = None
    run_path = project_root / "state" / "runs" / f"{SKILL_ID}-{args.mode}-{suffix}.json"
    report = {"skill_id": SKILL_ID, "mode": args.mode, "environment": args.environment, "generated_at": timestamp, "active_modules_source_is_mock": mock, "active_modules_checksum_sha256": active_modules_checksum, "reference_code_workbook_checksum_sha256": allowlist_checksum, "plan": plan, "summary": dict(Counter(item["classification"] for item in items)), "algorithms": items, "live_results": live_results, "write_operations_issued": [item for item in live_results if item.get("status") == "published"]}
    write_json(report_path, report)
    artifact_paths = [report_path, run_path]
    if args.mode != "preview" or items:
        review_path = target / f"{args.mode}-{suffix}-consultant-review.md"
        review_path.write_text(render_algorithm_review_table(args.mode, args.environment, items, live_results) + "\n", encoding="utf-8")
        artifact_paths.append(review_path)
    token_path = append_token_usage_log(project_id=args.project_id, skill_id=SKILL_ID, task="Activate algorithms", trigger="Activate Algorithms state-aware preview" if args.mode == "preview" else "Explicit approved Activate Algorithms live publication", activity_start_time=started_at, artifact_paths=artifact_paths, files_read=2, estimated_input_tokens=max(1, (Path(args.active_modules_handoff).stat().st_size + Path(args.reference_code_workbook).stat().st_size) // 4), notes="GET-only provided-algorithm discovery with pages of 100, active-Level-2 filtering, and grouped type-specific context reads; no per-algorithm state reads or Fusion mutation issued." if args.mode == "preview" else "Ordered type-specific BOSS bulk mutations were verified without automatic write retries.", root=ROOT)
    read_endpoints = [PROVIDED_ALGORITHMS, ALGORITHM_CONTEXTS, ACCESS_ALGORITHM_CONTEXTS, TRANSACTION_ALGORITHM_CONTEXTS] if args.mode == "preview" else [PROVIDED_ALGORITHMS, ALGORITHM_CONTEXTS, ACCESS_ALGORITHM_CONTEXTS, TRANSACTION_ALGORITHM_CONTEXTS, ALL_ALGORITHMS]
    run_artifacts = [str(report_path.relative_to(project_root)), str(token_path.relative_to(project_root))]
    if review_path is not None:
        run_artifacts.append(str(review_path.relative_to(project_root)))
    write_json(run_path, {"skill_id": SKILL_ID, "mode": args.mode, "status": "completed_with_exceptions" if any(item["classification"].startswith("failed") for item in items) else "completed", "environment": args.environment, "started_at": started_at, "completed_at": timestamp, "artifacts": run_artifacts, "read_endpoints": read_endpoints, "write_endpoints": [] if args.mode == "preview" else [ACCESS_ALGORITHM_CONTEXTS, TRANSACTION_ALGORITHM_CONTEXTS, ALGORITHM_CONTEXTS]})
    return report_path, review_path, run_path, token_path


def pending_discovery_requests(client: CoreResultClient, active_levels: set[str]) -> list[dict[str, Any]]:
    """Return the next missing page from the single active-Level-2 collection."""

    collections = [(PROVIDED_ALGORITHMS, lambda offset: provided_algorithms_query(offset, active_levels))]
    missing: list[dict[str, Any]] = []
    for endpoint, query_for_offset in collections:
        offset = 0
        while True:
            request = core_request("GET", endpoint, query_for_offset(offset))
            if not client.has_response(request):
                missing.append(request)
                break
            payload = client.payload_for(request)
            page = response_items(payload)
            if payload.get("hasMore") is not True:
                break
            if not page:
                raise ValueError(f"{endpoint} reported hasMore but returned an empty page")
            offset += len(page)
    return missing


def published_inventory_query(offset: int) -> dict[str, str]:
    """Return the stable pagination query for the environment-wide algorithm inventory."""

    return {"$limit": "100", "$offset": str(offset), "$sortBy": "id:asc"}


def pending_published_inventory_requests(client: CoreResultClient) -> list[dict[str, Any]]:
    """Return the next missing page for the read-only published-algorithm inventory."""

    offset = 0
    while True:
        request = core_request("GET", ALL_ALGORITHMS, published_inventory_query(offset))
        if not client.has_response(request):
            return [request]
        payload = client.payload_for(request)
        page = response_items(payload)
        if payload.get("hasMore") is not True:
            return []
        if not page:
            raise ValueError(f"{ALL_ALGORITHMS} reported hasMore but returned an empty page")
        offset += len(page)


def published_inventory_rows(client: CoreResultClient) -> list[dict[str, str]]:
    """Return the complete, customer-readable set of published algorithms from the environment inventory."""

    rows: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    offset = 0
    while True:
        payload, _ = client.get(ALL_ALGORITHMS, published_inventory_query(offset))
        page = response_items(payload)
        for algorithm in page:
            if algorithm.get("modeType") != "PUBLISHED":
                continue
            identifier = algorithm.get("id")
            if identifier is None or not str(identifier).strip():
                raise ValueError("Published algorithm inventory returned a row without an id")
            identifier_text = str(identifier)
            if identifier_text in seen_ids:
                raise ValueError(f"Published algorithm inventory returned duplicate id {identifier_text}")
            seen_ids.add(identifier_text)
            rows.append({
                "name": str(algorithm.get("name") or algorithm.get("algorithmName") or "Unnamed algorithm"),
                "reference": str(algorithm.get("referenceCode") or algorithm.get("algorithmNumber") or "—"),
                "type": str(algorithm.get("type") or algorithm.get("algorithmType") or "—"),
                "result": str(algorithm.get("resultType") or "—"),
            })
        if payload.get("hasMore") is not True:
            break
        if not page:
            raise ValueError(f"{ALL_ALGORITHMS} reported hasMore but returned an empty page")
        offset += len(page)
    return sorted(rows, key=lambda row: (row["name"], row["reference"]))


def render_published_inventory(environment: str, rows: list[dict[str, str]]) -> str:
    """Render the customer-readable published-algorithm inventory."""

    if not rows:
        return f"No published algorithms were found in {environment}."
    return "\n".join([
        f"Published Algorithms ({environment})",
        "",
        markdown_table(
            ["Algorithm", "Reference", "Type", "Result"],
            [[row["name"], row["reference"], row["type"], row["result"]] for row in rows],
        ),
    ])


def persist_published_inventory(project_root: Path, args: argparse.Namespace, started_at: str, rows: list[dict[str, str]]) -> Path | None:
    """Persist an auditable inventory result and its optional customer-readable register."""

    timestamp = utc_now()
    suffix = timestamp.replace(":", "").replace("-", "")
    target = active_modules_handoff_folder(project_root)
    report_path = target / f"published-inventory-{suffix}.json"
    run_path = project_root / "state" / "runs" / f"{SKILL_ID}-published-inventory-{suffix}.json"
    write_json(report_path, {
        "skill_id": SKILL_ID,
        "mode": "published_inventory",
        "environment": args.environment,
        "generated_at": timestamp,
        "published_algorithms": rows,
    })
    artifact_paths = [report_path, run_path]
    review_path: Path | None = None
    if rows:
        review_path = target / f"published-inventory-{suffix}-consultant-review.md"
        review_path.write_text(render_published_inventory(args.environment, rows) + "\n", encoding="utf-8")
        artifact_paths.append(review_path)
    token_path = append_token_usage_log(
        project_id=args.project_id,
        skill_id=SKILL_ID,
        task="List published algorithms",
        trigger="Explicit read-only published-algorithm inventory",
        activity_start_time=started_at,
        artifact_paths=artifact_paths,
        files_read=0,
        estimated_input_tokens=1,
        notes="Read-only paginated allAlgorithms inventory filtered locally to published algorithms; no Fusion mutation issued.",
        root=ROOT,
    )
    run_artifacts = [str(report_path.relative_to(project_root)), str(token_path.relative_to(project_root))]
    if review_path is not None:
        run_artifacts.append(str(review_path.relative_to(project_root)))
    write_json(run_path, {
        "skill_id": SKILL_ID,
        "mode": "published_inventory",
        "status": "completed",
        "environment": args.environment,
        "started_at": started_at,
        "completed_at": timestamp,
        "artifacts": run_artifacts,
        "read_endpoints": [ALL_ALGORITHMS],
        "write_endpoints": [],
    })
    return review_path


def write_missing_request_manifest(request_path: Path, environment: str, requests: list[dict[str, Any]]) -> None:
    unique_requests = list({request["id"]: request for request in requests}.values())
    manifest: dict[str, Any] = {"environment": environment, "requests": unique_requests}
    mutation_requests = [request for request in unique_requests if isinstance(request.get("body"), dict)]
    if mutation_requests:
        if len(mutation_requests) != 1:
            raise ValueError("A Core request manifest may emit only one mutation body")
        mutation = mutation_requests[0]
        if mutation["method"] != "POST":
            raise ValueError("Activate Algorithms mutation requests must use POST")
        body_path = request_path.with_name(f"{request_path.stem}-body.json")
        write_json(body_path, mutation_requests[0]["body"])
        manifest["execution_body_path"] = str(body_path)
        manifest["core_client_request"] = {
            "service": "boss",
            "method": "POST",
            "endpoint": mutation["endpoint"],
            "body_file": str(body_path),
        }
    write_json(request_path, manifest)


def main() -> int:
    args = parse_args()
    started_at = utc_now()
    project_root = ROOT / "project" / args.project_id
    if not project_root.is_dir():
        raise ValueError(f"Initialized project workspace does not exist: {project_root}")
    client = CoreResultClient(args)
    if args.published_inventory:
        try:
            missing_inventory = pending_published_inventory_requests(client)
            if missing_inventory:
                raise CoreResponsesRequired(missing_inventory)
            rows = published_inventory_rows(client)
        except (CoreResponseRequired, CoreResponsesRequired) as needed:
            request_path = Path(args.request_plan_output) if args.request_plan_output else active_modules_handoff_folder(project_root) / f"published-inventory-request-{utc_now().replace(':', '').replace('-', '')}.json"
            requests = [needed.request] if isinstance(needed, CoreResponseRequired) else needed.requests
            write_missing_request_manifest(request_path, args.environment, requests)
            print("I’m retrieving the published algorithm inventory. I’ll return with the complete list or a clear next action.")
            return 2
        except CoreResponseError:
            print("The published algorithm inventory could not be read. No algorithms were changed.")
            return 1
        review_path = persist_published_inventory(project_root, args, started_at, rows)
        if len(rows) > INLINE_ALGORITHM_TABLE_LIMIT and review_path is not None:
            print(f"There are {len(rows)} published algorithms in {args.environment}.\n\n[Open the complete published algorithm inventory]({review_path})")
        else:
            print(render_published_inventory(args.environment, rows))
        return 0
    active_modules_input = resolve_active_modules_input(args, project_root, started_at)
    if active_modules_input is None:
        print(
            f"\nActivate Algorithms needs confirmation of the selected business processes in {args.environment}. "
            "Confirm the business process selection, then return to prepare the preview. "
            "No algorithms were evaluated or changed."
        )
        return 2
    args.active_modules_handoff = str(active_modules_input)
    active_levels, mock, active_modules_checksum = load_active_modules(active_modules_input)
    allowlist, allowlist_checksum = load_reference_code_workbook(Path(args.reference_code_workbook))
    if args.mode == "live" and mock:
        raise ValueError("Live publication is blocked while the Identify Active Modules handoff source is MOCK_ACTIVE_MODULES")
    try:
        missing_discovery = pending_discovery_requests(client, active_levels)
        if missing_discovery:
            raise CoreResponsesRequired(missing_discovery)
        candidates = collect_allowlisted_algorithms(client, active_levels, allowlist)
        missing_context_reads = pending_context_state_requests(client, candidates)
        if missing_context_reads:
            raise CoreResponsesRequired(missing_context_reads)
        parent_rows, access_rows, transaction_rows = context_state(client, candidates)
        missing_access, missing_transaction = missing_context_ids(candidates, parent_rows, access_rows, transaction_rows)
        missing_source_reads = pending_context_source_requests(client, missing_access, missing_transaction)
        if missing_source_reads:
            raise CoreResponsesRequired(missing_source_reads)
        access_sources = read_rows_by_ids(client, PROVIDED_ACCESS_ALGORITHMS, missing_access, ACCESS_SOURCE_FIELDS, require_all=True)
        transaction_sources = read_rows_by_ids(client, PROVIDED_TRANSACTION_ALGORITHMS, missing_transaction, TRANSACTION_SOURCE_FIELDS, require_all=True)
        items: list[dict[str, Any]] = []
        for row in candidates:
            try:
                items.append(classify(row, parent_rows, access_rows, transaction_rows, access_sources, transaction_sources))
            except Exception as exc:
                items.append({"algorithm_number": row["algorithm_number"], "algorithm_name": row["algorithm_name"], "reference_code": row["reference_code"], "process_level_twos": row["process_level_twos"], "classification": "failed_read_or_validation", "reason": str(exc)})
        plan = publication_plan(items, args.environment, active_modules_checksum, allowlist_checksum)
        if args.mode == "live" and plan["digest_sha256"] != args.approved_plan_digest:
            raise ValueError("The current publication plan digest does not match --approved-plan-digest; rerun preview and obtain approval again")
        live_results = publish_ready_items(client, items) if args.mode == "live" else []
    except (CoreResponseRequired, CoreResponsesRequired) as needed:
        request_path = Path(args.request_plan_output) if args.request_plan_output else active_modules_handoff_folder(project_root) / f"core-request-{utc_now().replace(':', '').replace('-', '')}.json"
        requests = [needed.request] if isinstance(needed, CoreResponseRequired) else needed.requests
        write_missing_request_manifest(request_path, args.environment, requests)
        print(render_discovery_in_progress(args.environment))
        return 2
    except CoreResponseError as error:
        if error.status_code == 403 and error.endpoint == PROVIDED_ALGORITHMS:
            print("The current setup could not be read because required access is unavailable. No algorithms were changed.")
            return 1
        raise
    _, review_path, _, _ = persist(project_root, args, started_at, active_modules_checksum, allowlist_checksum, mock, items, plan, live_results)
    print(render_user_summary(args.mode, args.environment, items, live_results, review_path))
    return 1 if any(item["classification"].startswith("failed") for item in items) or any(item.get("status") == "failed" for item in live_results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
