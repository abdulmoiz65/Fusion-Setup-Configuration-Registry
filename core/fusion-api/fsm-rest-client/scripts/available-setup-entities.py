#!/usr/bin/env python3
"""Print available Fusion features, or export all available features to CSV."""
from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
AUTH = ROOT / "core" / "auth" / "fusion-oauth-authentication" / "scripts"
sys.path.insert(0, str(AUTH))
from fusion_auth import FusionHttpError, get_access_token, http_json, read_properties, require_props  # noqa: E402

ENDPOINT = "/api/boss/extraction/queries/ora/commonSetup/search/v1/$en/setupEntities"
ENTITY_CONFIG = {
    "feature": ("features", "FEATURE", ["Feature Name", "Feature Shortname (Code)", "Product"], ("featureName", "name", "displayName"), ("featureShortName", "shortName", "featureCode", "code")),
    "functional-area": ("functionalAreas", "FUNCTIONALAREA", ["Functional Area Name", "Functional Area Shortname (Code)", "Product"], ("functionalAreaName", "name", "displayName"), ("functionalAreaShortName", "shortName", "functionalAreaCode", "code")),
    "business-object": ("businessObjects", "BUSINESSOBJECT", ["Business Object Name", "Business Object Shortname (Code)", "Product"], ("businessObjectName", "name", "displayName"), ("businessObjectShortName", "shortName", "businessObjectCode", "code")),
    "offering": ("offerings", "OFFERING", ["Offering Name", "Offering Shortname (Code)", "Product"], ("offeringName", "name", "displayName"), ("offeringShortName", "shortName", "offeringCode", "code")),
    "task-list": ("taskLists", "TASKLIST", ["Task List Name", "Task List Shortname (Code)", "Product"], ("taskListName", "name", "displayName"), ("taskListShortName", "shortName", "taskListCode", "code")),
    "task": ("tasks", "TASK", ["Task Name", "Task Shortname (Code)", "Product"], ("taskName", "name", "displayName"), ("taskShortName", "shortName", "taskCode", "code")),
}


def ci(row: dict[str, Any], *keys: str) -> str:
    values = {str(key).casefold(): value for key, value in row.items()}
    for key in keys:
        value = values.get(key.casefold())
        if value not in (None, ""):
            return str(value)
    return ""


def rows(body: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("items", "Items", "results", "Results", "rows", "Rows", "data", "Data", "value", "Value"):
        if isinstance(body.get(key), list):
            return [item for item in body[key] if isinstance(item, dict)]
    return []


def more(body: dict[str, Any]) -> bool:
    return str(ci(body, "hasMore", "hasMoreRecords", "hasMoreResults", "hasNext")).casefold() in {"true", "1", "yes"}


def request(base: str, token: str, limit: int, offset: int, selector: str, selector_value: str) -> dict[str, Any]:
    params = {"$filter": "name ~Like '%%'", "businessObjects": "null", "features": "null", "functionalAreas": "null", "offerings": "null", "taskLists": "null", "tasks": "null", "$limit": str(limit), "$offset": str(offset)}
    params[selector] = selector_value
    return http_json(f"{base.rstrip('/')}{ENDPOINT}?{urllib.parse.urlencode(params)}", access_token=token, headers={"Authorization": f"Bearer {token}"})


def records(base: str, token: str, fetch_all: bool, entity: str) -> tuple[list[dict[str, str]], list[str]]:
    selector, selector_value, headers, name_keys, code_keys = ENTITY_CONFIG[entity]
    limit, offset, output = 25, 0, []
    while True:
        body = request(base, token, limit, offset, selector, selector_value)
        page = rows(body)
        output.extend({headers[0]: ci(item, *name_keys), headers[1]: ci(item, *code_keys), headers[2]: ci(item, "product", "productName", "productDisplayName")} for item in page)
        if not fetch_all or not more(body) or not page:
            return output, headers
        offset += len(page)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entity", choices=sorted(ENTITY_CONFIG), default="feature")
    parser.add_argument("--all", action="store_true", help="Fetch all pages and write a project CSV.")
    parser.add_argument("--project-id")
    parser.add_argument("--properties", default=str(ROOT / "core" / "auth" / "fusionEnv.properties"))
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.all and not args.project_id:
        raise ValueError("--project-id is required with --all")
    if args.dry_run:
        print(f"Would GET {ENDPOINT} with $limit=25; {'paginate and write CSV' if args.all else 'print the first 25 rows'}.")
        return 0
    props = read_properties(Path(args.properties)); require_props(props, ["restBaseUrl", "boss_scope"])
    scoped = dict(props); scoped["scope"] = props["boss_scope"]
    token = get_access_token(scoped, token_cache=args.token_cache)
    try:
        output, headers = records(props["restBaseUrl"], token, args.all, args.entity)
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403}: raise
        output, headers = records(props["restBaseUrl"], get_access_token(scoped, token_cache=args.token_cache, force_login=True), args.all, args.entity)
    if not args.all:
        print(json.dumps(output, indent=2, ensure_ascii=False)); return 0
    project = ROOT / "project" / str(args.project_id)
    if not project.is_dir(): raise ValueError(f"Project workspace does not exist: {project}")
    folder = project / "artifacts" / "core" / "fusion-api" / "fsm-rest-client" / f"available-{args.entity}s"; folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"available-{args.entity}s-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers); writer.writeheader(); writer.writerows(output)
    print(f"Retrieved {len(output)} features. CSV: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try: raise SystemExit(main())
    except Exception as exc: print(f"Error: {exc}", file=sys.stderr); raise SystemExit(1)
