#!/usr/bin/env python3
"""Return task-list items or export all task-list items to CSV."""
from __future__ import annotations
import argparse, csv, json, sys, urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "core/auth/fusion-oauth-authentication/scripts"))
from fusion_auth import FusionHttpError, get_access_token, http_bytes, read_properties, require_props  # noqa: E402

SEARCH = "/api/boss/extraction/queries/ora/commonSetup/search/v1/$en/setupEntities"
ITEMS = "/api/boss/data/objects/ora/commonSetup/tasks/v1/taskListItems/$views/manageTaskListSearch"
FIELDS = ["PRODUCT", "TASK_LIST_NAME", "TASK_LIST_SHORT_NAME", "DISPLAY_SEQUENCE", "ITEM_TYPE_CODE", "ITEM_TASK_LIST_NAME", "ITEM_TASK_LIST_SHORT_NAME", "ITEM_TASK_NAME", "ITEM_TASK_SHORT_NAME"]
BATCH_SIZE = 100

def rows(body: Any) -> list[dict[str, Any]]:
    if isinstance(body, list): return [x for x in body if isinstance(x, dict)]
    if isinstance(body, dict):
        for key in ("items", "results", "rows", "data", "value"):
            if isinstance(body.get(key), list): return [x for x in body[key] if isinstance(x, dict)]
    return []

def val(row: Any, *keys: str) -> str:
    wanted = {key.casefold() for key in keys}
    if isinstance(row, dict):
        for key, item in row.items():
            if str(key).casefold() in wanted and item not in (None, "") and not isinstance(item, (dict, list)): return str(item)
        for item in row.values():
            found = val(item, *keys)
            if found: return found
    return ""

def nested_val(row: dict[str, Any], relationship: str, *keys: str) -> str:
    """Read a value from a named BOSS relationship without matching siblings."""
    related = row.get(relationship)
    return val(related, *keys) if isinstance(related, dict) else ""

def get(base: str, token: str, endpoint: str, params: dict[str, Any], stats: dict[str, int]) -> Any:
    stats["api_call_count"] += 1
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}, safe="$'=")
    body = http_bytes(base.rstrip("/") + endpoint + ("?" + query if query else ""), access_token=token, headers={"Authorization": f"Bearer {token}"})
    return json.loads(body) if body.strip() else {"items": []}

def paged(base: str, token: str, endpoint: str, params: dict[str, Any], stats: dict[str, int], limit: int = 1000, max_rows: int | None = None) -> list[dict[str, Any]]:
    result, offset = [], 0
    while True:
        page = rows(get(base, token, endpoint, {**params, "$limit": limit, "$offset": offset}, stats)); result.extend(page)
        if max_rows is not None and len(result) >= max_rows: return result[:max_rows]
        if len(page) < limit: return result
        offset += len(page)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--properties", default=str(ROOT / "core/auth/fusionEnv.properties")); parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--preview-limit", type=int, default=25); parser.add_argument("--all", action="store_true"); parser.add_argument("--project-id"); parser.add_argument("--output"); parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.preview_limit < 1: raise ValueError("--preview-limit must be at least 1")
    if args.all and not (args.project_id or args.output): raise ValueError("Full export requires --project-id or --output")
    props = read_properties(Path(args.properties)); require_props(props, ["restBaseUrl", "boss_scope"])
    scoped = dict(props); scoped["scope"] = props["boss_scope"]; token = get_access_token(scoped, token_cache=args.token_cache); stats = {"api_call_count": 0}
    search = {"$filter": "name ~Like '%%'", "businessObjects": "null", "features": "null", "functionalAreas": "null", "offerings": "null", "taskLists": "TASKLIST", "tasks": "null"}
    if args.verbose: print("Subtask 1: retrieving task lists...", file=sys.stderr, flush=True)
    try: lists = paged(props["restBaseUrl"], token, SEARCH, search, stats, 25, None if args.all else args.preview_limit)
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403}: raise
        token = get_access_token(scoped, token_cache=args.token_cache, force_login=True); lists = paged(props["restBaseUrl"], token, SEARCH, search, stats, 25, None if args.all else args.preview_limit)
    if args.verbose: print(f"Subtask 1 complete: retrieved {len(lists)} task lists.", file=sys.stderr, flush=True)
    result, errors = [], []
    indexed: dict[str, dict[str, str]] = {}
    for task_list in lists:
        task_list_id = val(task_list, "taskListId", "id")
        if task_list_id:
            indexed[task_list_id] = {"PRODUCT": val(task_list, "product", "productName"), "TASK_LIST_NAME": val(task_list, "taskListName", "name", "displayName"), "TASK_LIST_SHORT_NAME": val(task_list, "taskListShortName", "shortName", "taskListCode", "code")}
    batch_total = (len(indexed) + BATCH_SIZE - 1) // BATCH_SIZE
    for start in range(0, len(indexed), BATCH_SIZE):
        if not args.all and len(result) >= args.preview_limit: break
        ids = list(indexed)[start:start + BATCH_SIZE]
        batch_number = start // BATCH_SIZE + 1
        if args.verbose: print(f"Subtask 2.{batch_number}/{batch_total}: retrieving items for {len(ids)} task lists...", file=sys.stderr, flush=True)
        try: items = paged(props["restBaseUrl"], token, ITEMS, {"$filter": "taskList.taskListId in (" + ",".join(ids) + ")"}, stats)
        except Exception as exc: errors.append({"taskListIds": ids, "message": str(exc)}); continue
        for item in items:
            task_list_id = val(item, "taskListId")
            base = indexed.get(task_list_id, {})
            result.append({**base, "DISPLAY_SEQUENCE": val(item, "displaySequence"), "ITEM_TYPE_CODE": val(item, "itemTypeCode", "taskListItemTypeCode"), "ITEM_TASK_LIST_NAME": nested_val(item, "itemTaskList", "taskListName"), "ITEM_TASK_LIST_SHORT_NAME": nested_val(item, "itemTaskList", "taskListShortName"), "ITEM_TASK_NAME": nested_val(item, "itemTask", "taskName"), "ITEM_TASK_SHORT_NAME": nested_val(item, "itemTask", "taskShortName")})
            if not args.all and len(result) >= args.preview_limit: break
        if args.verbose: print(f"Subtask 2.{batch_number} complete: collected {len(result)} rows so far.", file=sys.stderr, flush=True)
    if not args.all: print(json.dumps({"row_count": len(result), **stats, "rows": result[:args.preview_limit], "errors": errors}, indent=2, ensure_ascii=False)); return 1 if errors and not result else 0
    target = Path(args.output) if args.output else ROOT / "project" / args.project_id / "artifacts/core/fusion-api/fsm-rest-client/tasklist-tasks" / f"tasklist-tasks-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.csv"; target.parent.mkdir(parents=True, exist_ok=True)
    if args.verbose: print("Subtask 3: writing CSV...", file=sys.stderr, flush=True)
    with target.open("w", newline="", encoding="utf-8") as handle: writer = csv.DictWriter(handle, fieldnames=FIELDS); writer.writeheader(); writer.writerows(result)
    if args.verbose: print(f"Subtask 3 complete: wrote {len(result)} rows to {target}.", file=sys.stderr, flush=True)
    print(json.dumps({"row_count": len(result), **stats, "csv": str(target), "errors": errors}, indent=2, ensure_ascii=False)); return 1 if errors else 0
if __name__ == "__main__":
    try: raise SystemExit(main())
    except Exception as exc: print(f"Error: {exc}", file=sys.stderr); raise SystemExit(1)
