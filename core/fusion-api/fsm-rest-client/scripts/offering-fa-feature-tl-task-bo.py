#!/usr/bin/env python3
"""Export the offering → FA/feature → task list → task → BO mapping."""
from __future__ import annotations

import argparse
import csv
import http.client
import json
import signal
import socket
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FDOS_ROOT = Path(__file__).resolve().parents[4]
REPO_ROOT = FDOS_ROOT
sys.path.insert(0, str(FDOS_ROOT / "core/auth/fusion-oauth-authentication/scripts"))
from fusion_auth import request_context, require_authorized_rest_url, FusionHttpError, get_access_token, http_json, read_properties, require_props  # noqa: E402

OFFERINGS = "/api/boss/data/objects/ora/commonSetup/features/v1/features/$views/availableOfferings"
FEATURE_BASE = "/api/boss/extraction/queries/ora/commonSetup/features/v1"
FA_HIERARCHY = FEATURE_BASE + "/availableFunctionalAreasByOffering"
FEATURE_HIERARCHY = FEATURE_BASE + "/availableFeaturesByOffering"
FEATURE_DETAILS = "/api/boss/data/objects/ora/commonSetup/features/v1/features"
ASSOCIATED = FEATURE_BASE + "/associatedTasksAndTaskListsByFeature"
TASKS_BY_LIST = "/api/boss/extraction/queries/ora/commonSetup/tasks/v1/tasksByTaskList"
TASK_LIST_SEARCH = "/api/boss/extraction/queries/ora/commonSetup/search/v1/$en/setupEntities"
TASK_LIST_ITEMS = "/api/boss/data/objects/ora/commonSetup/tasks/v1/taskListItems/$views/manageTaskListSearch"
BUSINESS_OBJECTS = "/api/boss/data/objects/ora/commonSetup/businessObjects/v1/businessObjects"
FIELDS = [
    "OFFERING", "FA_FEATURE", "PRODUCT_FAMILY", "PRODUCT", "CLASSIFICATION",
    "TASK_LIST_NAME", "TASK_NAME", "BUSINESS_OBJECT_NAME", "PATH",
]
PAGE_SIZE = 1000
TASK_LIST_ITEM_BATCH_SIZE = 100
REQUEST_TIMEOUT_SECONDS = 60
GET_RETRY_COUNT = 3
MAX_REQUESTS_PER_CONNECTION = 20


class BossGetClient:
    """Keep one HTTPS connection open for the high-volume read-only export."""

    def __init__(self, base: str, token: str) -> None:
        self.context = request_context(None, token)
        require_authorized_rest_url(self.context, base)
        parsed = urllib.parse.urlsplit(base)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError(f"Expected an HTTPS BOSS base URL, got: {base}")
        self.host = parsed.hostname
        self.port = parsed.port or 443
        self.base_path = parsed.path.rstrip("/")
        self.token = token
        self.connection: http.client.HTTPSConnection | None = None
        self.request_count = 0

    def close(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None
        self.request_count = 0

    def get_json(self, endpoint: str, params: dict[str, Any]) -> Any:
        query = urllib.parse.urlencode({key: value for key, value in params.items() if value is not None}, safe="$'=")
        target = self.base_path + endpoint + (("?" + query) if query else "")
        host = f"[{self.host}]" if ":" in self.host else self.host
        url = f"https://{host}:{self.port}{target}"
        require_authorized_rest_url(self.context, url)
        for attempt in range(GET_RETRY_COUNT):
            previous_alarm_handler: Any = None
            try:
                if self.request_count >= MAX_REQUESTS_PER_CONNECTION:
                    self.close()
                previous_alarm_handler = signal.getsignal(signal.SIGALRM)
                signal.signal(signal.SIGALRM, lambda _signum, _frame: (_ for _ in ()).throw(TimeoutError("request deadline exceeded")))
                signal.setitimer(signal.ITIMER_REAL, REQUEST_TIMEOUT_SECONDS)
                if self.connection is None:
                    self.connection = http.client.HTTPSConnection(self.host, self.port, timeout=REQUEST_TIMEOUT_SECONDS)
                self.connection.request("GET", target, headers={"Authorization": "Bearer " + self.token, "Accept": "application/json"})
                response = self.connection.getresponse()
                body = response.read()
                self.request_count += 1
                if response.status >= 400:
                    raise FusionHttpError(response.status, url, body.decode("utf-8", errors="replace"))
                if not body.strip():
                    return {}
                return json.loads(body.decode("utf-8"))
            except FusionHttpError:
                raise
            except (http.client.HTTPException, OSError, socket.timeout, TimeoutError) as exc:
                self.close()
                if attempt == GET_RETRY_COUNT - 1:
                    raise RuntimeError(f"Failed calling {url} after {GET_RETRY_COUNT} attempts: {exc}") from exc
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
                if previous_alarm_handler is not None:
                    signal.signal(signal.SIGALRM, previous_alarm_handler)
        raise AssertionError("unreachable")


GET_CLIENTS: dict[tuple[str, str], BossGetClient] = {}


def rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        return next(([row for row in payload[key] if isinstance(row, dict)] for key in ("items", "results", "rows", "data", "value") if isinstance(payload.get(key), list)), [])
    return []


def val(row: Any, *keys: str) -> str:
    if not isinstance(row, dict):
        return ""
    wanted = {key.lower().split(".")[-1] for key in keys}
    for key, item in row.items():
        if str(key).lower() in wanted and item not in (None, "") and not isinstance(item, (dict, list)):
            return str(item)
    for item in row.values():
        if isinstance(item, dict):
            found = val(item, *keys)
            if found:
                return found
    return ""


def values(row: Any, *keys: str) -> set[str]:
    wanted = {key.lower().split(".")[-1] for key in keys}
    found: set[str] = set()
    if isinstance(row, dict):
        for key, item in row.items():
            if str(key).lower() in wanted and item not in (None, "") and not isinstance(item, (dict, list)):
                found.add(str(item))
            else:
                found.update(values(item, *keys))
    elif isinstance(row, list):
        for item in row:
            found.update(values(item, *keys))
    return found


def get(base: str, token: str, endpoint: str, params: dict[str, Any], stats: dict[str, int]) -> Any:
    stats["api_call_count"] += 1
    client = GET_CLIENTS.setdefault((base, token), BossGetClient(base, token))
    return client.get_json(endpoint, params)


def paged(base: str, token: str, endpoint: str, params: dict[str, Any], stats: dict[str, int]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    offset = 0
    while True:
        page = rows(get(base, token, endpoint, {**params, "$limit": PAGE_SIZE, "$offset": offset}, stats))
        result.extend(page)
        if len(page) < PAGE_SIZE:
            return result
        offset += PAGE_SIZE


def display_path(path: str, names: dict[str, str], offering: str) -> str:
    parts = [part for part in path.strip("/").split("/") if part]
    display = "/".join([offering] + [names.get(part, part) for part in parts[1:]]) if parts else offering
    return "/" + display.strip("/")


def feature_details(base: str, token: str, codes: set[str], stats: dict[str, int]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for index in range(0, len(codes), 100):
        batch = sorted(codes)[index:index + 100]
        quoted = ",".join("'" + code.replace("'", "''") + "'" for code in batch)
        for row in paged(base, token, FEATURE_DETAILS, {"$filter": f"featureShortName in ({quoted})"}, stats):
            code = val(row, "featureShortName")
            if code:
                result[code] = row
    return result


def sql_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def task_list_id_filter(ids: list[str]) -> str:
    formatted = [item if item.isdigit() else sql_literal(item) for item in ids]
    return "taskList.taskListId in (" + ",".join(formatted) + ")"


def task_list_search_params() -> dict[str, str]:
    return {
        "$filter": "name ~Like '%%'",
        "businessObjects": "null",
        "features": "null",
        "functionalAreas": "null",
        "offerings": "null",
        "taskLists": "TASKLIST",
        "tasks": "null",
    }


def all_task_lists(base: str, token: str, stats: dict[str, int]) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for task_list in paged(base, token, TASK_LIST_SEARCH, task_list_search_params(), stats):
        code = val(task_list, "taskListShortName", "shortName", "taskListCode", "code")
        task_list_id = val(task_list, "taskListId", "id")
        if code and task_list_id:
            indexed[code] = {
                "taskListId": task_list_id,
                "taskListName": val(task_list, "taskListName", "name", "displayName"),
            }
    return indexed


def task_list_items_by_ids(base: str, token: str, ids: list[str], stats: dict[str, int]) -> dict[str, list[dict[str, Any]]]:
    indexed: dict[str, list[dict[str, Any]]] = {task_list_id: [] for task_list_id in ids}
    for index in range(0, len(ids), TASK_LIST_ITEM_BATCH_SIZE):
        batch = ids[index:index + TASK_LIST_ITEM_BATCH_SIZE]
        for item in paged(base, token, TASK_LIST_ITEMS, {"$filter": task_list_id_filter(batch)}, stats):
            task_list_id = val(item, "taskListId")
            if task_list_id:
                indexed.setdefault(task_list_id, []).append(item)
    return indexed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--properties", default=str(FDOS_ROOT / "core/auth/fusionEnv.properties"))
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--offering-short-name")
    parser.add_argument("--offering-offset", type=int, default=0)
    parser.add_argument("--offering-limit", type=int)
    parser.add_argument("--node-offset", type=int, default=0)
    parser.add_argument("--node-limit", type=int)
    parser.add_argument("--preview-limit", type=int, default=25)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--output")
    parser.add_argument("--project-id")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def validate(args: argparse.Namespace) -> None:
    if args.preview_limit < 1 or args.offering_offset < 0 or args.node_offset < 0:
        raise ValueError("Limits must be positive; offsets cannot be negative")
    if args.offering_limit is not None and args.offering_limit < 1 or args.node_limit is not None and args.node_limit < 1:
        raise ValueError("Limits must be positive; offsets cannot be negative")


def main() -> int:
    args = parse_args()
    validate(args)
    props = read_properties(Path(args.properties))
    require_props(props, ["restBaseUrl", "boss_scope"])
    auth = dict(props)
    auth["scope"] = props["boss_scope"]
    token = get_access_token(auth, token_cache=args.token_cache)
    stats = {"api_call_count": 0}
    try:
        if args.verbose:
            print("Fetching offerings...", file=sys.stderr, flush=True)
        offerings = paged(props["restBaseUrl"], token, OFFERINGS, {}, stats)
        if args.verbose:
            print("Fetching business objects...", file=sys.stderr, flush=True)
        business_objects = paged(props["restBaseUrl"], token, BUSINESS_OBJECTS, {}, stats)
    except FusionHttpError as exc:
        raise RuntimeError(f"Initial mapping request failed: {exc}") from exc
    task_bos: dict[str, set[str]] = {}
    bo_names: dict[str, str] = {}
    for business_object in business_objects:
        bo_id = val(business_object, "businessObjectId", "businessObjectShortName")
        if bo_id:
            bo_names[bo_id] = val(business_object, "businessObjectName")
            for task_id in values(business_object, "taskId", "itemTaskId", "setupTaskId"):
                task_bos.setdefault(task_id, set()).add(bo_id)
    selected = [row for row in offerings if not args.offering_short_name or val(row, "featureShortName") == args.offering_short_name]
    if args.offering_short_name and not selected:
        raise ValueError(f"Offering not found: {args.offering_short_name}")
    selected = selected[args.offering_offset:]
    if args.offering_limit is not None:
        selected = selected[:args.offering_limit]
    if not args.all:
        selected = selected[:5]
    association_cache: dict[str, list[dict[str, Any]]] = {}
    list_cache: dict[str, list[dict[str, Any]]] = {}
    task_list_directory: dict[str, dict[str, str]] | None = None
    output: list[dict[str, str]] = []
    errors: list[dict[str, str]] = []
    seen: set[tuple[str, ...]] = set()
    node_count = 0
    target = None
    writer = None
    handle = None
    if args.all:
        if not args.output and not args.project_id:
            raise ValueError("Full export requires --project-id or --output")
        suffix = f"-batch-{args.offering_offset}" if args.offering_limit is not None else ""
        if args.node_limit is not None:
            suffix += f"-node-{args.node_offset}"
        target = Path(args.output) if args.output else REPO_ROOT / "project" / str(args.project_id) / "artifacts/shared/implementation-planning/offering-fa-feature-tl-task-bo" / ("offering-fa-feature-tl-task-bo-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + suffix + ".csv")
        target.parent.mkdir(parents=True, exist_ok=True)
        handle = target.open("w", newline="", encoding="utf-8")
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
    try:
        for offering_index, offering in enumerate(selected, start=1):
            code = val(offering, "featureShortName")
            name = val(offering, "featureName") or code
            if args.verbose:
                print(f"Fetching hierarchy {offering_index}/{len(selected)}: {code}", file=sys.stderr, flush=True)
            fa_rows: list[dict[str, Any]] = []
            feature_rows: list[dict[str, Any]] = []
            try:
                fa_rows = paged(props["restBaseUrl"], token, FA_HIERARCHY, {"parentShortName": code}, stats)
            except Exception as exc:
                errors.append({"offering": code, "endpoint": "functional_areas", "message": str(exc)})
            try:
                feature_rows = paged(props["restBaseUrl"], token, FEATURE_HIERARCHY, {"parentShortName": code}, stats)
            except Exception as exc:
                errors.append({"offering": code, "endpoint": "features", "message": str(exc)})
            names = {code: name}
            nodes: dict[str, tuple[str, dict[str, Any]]] = {}
            for classification, collection in (("Functional Area", fa_rows), ("Feature", feature_rows)):
                for item in collection:
                    child = val(item, "childFeatureShortName", "featureShortName")
                    child_name = val(item, "childFeatureName", "featureName")
                    if child:
                        nodes.setdefault(child, (classification, item))
                        names[child] = child_name or child
            node_count += len(nodes)
            if args.verbose:
                print(f"Fetching product details: {code}", file=sys.stderr, flush=True)
            try:
                details = feature_details(props["restBaseUrl"], token, set(nodes), stats)
            except Exception as exc:
                errors.append({"offering": code, "endpoint": "feature_details", "message": str(exc)})
                details = {}
            node_items = list(nodes.items())[args.node_offset:]
            if args.node_limit is not None:
                node_items = node_items[:args.node_limit]
            if args.all:
                task_list_ids: dict[str, str] = {}
                for feature_code, (classification, hierarchy) in node_items:
                    if feature_code not in association_cache:
                        if args.verbose:
                            print(f"Fetching task associations: {feature_code}", file=sys.stderr, flush=True)
                        try:
                            association_cache[feature_code] = paged(props["restBaseUrl"], token, ASSOCIATED, {"featureShortName": feature_code}, stats)
                        except Exception as exc:
                            errors.append({"offering": code, "feature": feature_code, "endpoint": "task_associations", "message": str(exc)})
                            association_cache[feature_code] = []
                    for association in association_cache[feature_code]:
                        list_code = val(association, "taskListShortName")
                        list_id = val(association, "taskListId")
                        if list_code and list_id:
                            task_list_ids[list_code] = list_id
                missing_list_codes = sorted({
                    list_code
                    for feature_code, _ in node_items
                    for association in association_cache.get(feature_code, [])
                    for list_code in [val(association, "taskListShortName")]
                    if list_code and list_code not in task_list_ids
                })
                if missing_list_codes:
                    if task_list_directory is None:
                        if args.verbose:
                            print("Resolving task list ids in bulk...", file=sys.stderr, flush=True)
                        try:
                            task_list_directory = all_task_lists(props["restBaseUrl"], token, stats)
                        except Exception as exc:
                            errors.append({"offering": code, "endpoint": "task_list_search", "message": str(exc)})
                            task_list_directory = {}
                    for list_code in missing_list_codes:
                        list_id = task_list_directory.get(list_code, {}).get("taskListId")
                        if list_id:
                            task_list_ids[list_code] = list_id
                uncached_ids = sorted({list_id for list_code, list_id in task_list_ids.items() if list_code not in list_cache})
                if uncached_ids:
                    if args.verbose:
                        batch_count = ((len(uncached_ids) - 1) // TASK_LIST_ITEM_BATCH_SIZE) + 1
                        print(f"Fetching task-list items in {batch_count} batch(es) for {len(uncached_ids)} task lists...", file=sys.stderr, flush=True)
                    try:
                        items_by_id = task_list_items_by_ids(props["restBaseUrl"], token, uncached_ids, stats)
                        for list_code, list_id in task_list_ids.items():
                            if list_code not in list_cache:
                                list_cache[list_code] = items_by_id.get(list_id, [])
                    except Exception as exc:
                        errors.append({"offering": code, "endpoint": "task_list_items", "message": str(exc)})
                # Keep the association itself when its list could not be
                # resolved in bulk.  Do not reintroduce one HTTP call per
                # task list during a complete export.
                for feature_code, _ in node_items:
                    for association in association_cache.get(feature_code, []):
                        list_code = val(association, "taskListShortName")
                        if list_code and list_code not in list_cache:
                            list_cache[list_code] = []
            for feature_code, (classification, hierarchy) in node_items:
                if not args.all and len(output) >= args.preview_limit:
                    break
                if feature_code not in association_cache:
                    if args.verbose:
                        print(f"Fetching task associations: {feature_code}", file=sys.stderr, flush=True)
                    try:
                        association_cache[feature_code] = paged(props["restBaseUrl"], token, ASSOCIATED, {"featureShortName": feature_code}, stats)
                    except Exception as exc:
                        errors.append({"offering": code, "feature": feature_code, "endpoint": "task_associations", "message": str(exc)})
                        association_cache[feature_code] = []
                meta = details.get(feature_code, {})
                base = {
                    "OFFERING": name,
                    "FA_FEATURE": val(hierarchy, "childFeatureName", "featureName") or val(meta, "featureName"),
                    "PRODUCT_FAMILY": val(meta, "productFamily", "familyModuleGUID", "product_family"),
                    "PRODUCT": val(meta, "product", "userModuleName"),
                    "CLASSIFICATION": classification,
                    "PATH": display_path(val(hierarchy, "path"), names, name),
                }
                for association in association_cache[feature_code]:
                    list_code = val(association, "taskListShortName")
                    if list_code and list_code not in list_cache:
                        try:
                            list_cache[list_code] = paged(props["restBaseUrl"], token, TASKS_BY_LIST, {"taskListShortName": list_code}, stats)
                        except Exception as exc:
                            errors.append({"offering": code, "task_list": list_code, "endpoint": "tasks_by_task_list", "message": str(exc)})
                            list_cache[list_code] = []
                    for task in list_cache.get(list_code) or [association]:
                        task_ids = values(task, "taskId", "itemTaskId", "setupTaskId")
                        bo_ids: set[str] = set()
                        for task_id in task_ids:
                            bo_ids.update(task_bos.get(task_id, set()))
                        for bo_id in bo_ids or {""}:
                            item = {**base, "TASK_LIST_NAME": val(association, "taskListName"), "TASK_NAME": val(task, "itemTaskName", "taskName") or val(association, "taskName"), "BUSINESS_OBJECT_NAME": bo_names.get(bo_id, "")}
                            key = tuple(item[field] for field in FIELDS)
                            if key not in seen:
                                seen.add(key)
                                output.append(item)
                                if writer and handle:
                                    writer.writerow(item)
                                    handle.flush()
                                if not args.all and len(output) >= args.preview_limit:
                                    break
                        if not args.all and len(output) >= args.preview_limit:
                            break
                    if not args.all and len(output) >= args.preview_limit:
                        break
    finally:
        if handle:
            handle.close()
    result: dict[str, Any] = {"offering_count": len(selected), "node_count": node_count, **stats, "row_count": len(output), "errors": errors}
    if not args.all:
        result["rows"] = output[:args.preview_limit]
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if errors and not output else 0
    result["csv"] = str(target)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
