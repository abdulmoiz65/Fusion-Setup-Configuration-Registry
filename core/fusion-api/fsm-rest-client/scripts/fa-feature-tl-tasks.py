#!/usr/bin/env python3
"""Return the FA_FEATURE_TL_Tasks preview or export its complete CSV."""
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
sys.path.insert(0, str(ROOT / "core/auth/fusion-oauth-authentication/scripts"))
from fusion_auth import FusionHttpError, get_access_token, http_bytes, read_properties, require_props  # noqa: E402

FEATURES = "/api/boss/data/objects/ora/commonSetup/features/v1/features"
ASSOCIATIONS = "/api/boss/extraction/queries/ora/commonSetup/features/v1/associatedTasksAndTaskListsByFeature"
FIELDS = ["PRODUCT", "FILTER_NAME", "CLASSIFICATION", "AVAILABLE_RELEASE_VERSION", "EXPIRATION_RELEASE_VERSION", "TASK_LIST_NAME", "TASK_NAME"]
PAGE_SIZE = 1000


def rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("items", "results", "rows", "data", "value"):
            if isinstance(payload.get(key), list):
                return [item for item in payload[key] if isinstance(item, dict)]
    return []


def value(item: Any, *keys: str) -> str:
    wanted = {key.casefold() for key in keys}
    if isinstance(item, dict):
        for key, candidate in item.items():
            if str(key).casefold() in wanted and candidate not in (None, "") and not isinstance(candidate, (dict, list)):
                return str(candidate)
        for candidate in item.values():
            found = value(candidate, *keys)
            if found:
                return found
    elif isinstance(item, list):
        for candidate in item:
            found = value(candidate, *keys)
            if found:
                return found
    return ""


def classification(feature: dict[str, Any]) -> str:
    """Map BOSS feature classification to the report's two supported values."""
    return "Functional Area" if value(feature, "classification", "featureClassification").casefold() == "license" else "Feature"


def request(base: str, token: str, endpoint: str, params: dict[str, Any], stats: dict[str, int]) -> Any:
    query = urllib.parse.urlencode({key: item for key, item in params.items() if item is not None}, safe="$'=")
    stats["api_call_count"] += 1
    body = http_bytes(base.rstrip("/") + endpoint + ("?" + query if query else ""), access_token=token, headers={"Authorization": f"Bearer {token}"})
    return json.loads(body) if body.strip() else {"items": []}


def paged(base: str, token: str, endpoint: str, params: dict[str, Any], stats: dict[str, int], stop_after: int | None = None) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    offset = 0
    while True:
        limit = min(PAGE_SIZE, stop_after - len(output)) if stop_after else PAGE_SIZE
        page = rows(request(base, token, endpoint, {**params, "$limit": limit, "$offset": offset}, stats))
        output.extend(page)
        if not page or len(page) < limit or (stop_after and len(output) >= stop_after):
            return output
        offset += len(page)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--properties", default=str(ROOT / "core/auth/fusionEnv.properties"))
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--preview-limit", type=int, default=25)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--project-id")
    parser.add_argument("--output")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def full_output_path(args: argparse.Namespace) -> Path:
    if args.output:
        return Path(args.output)
    if not args.project_id:
        raise ValueError("Full export requires --project-id or --output")
    project = ROOT / "project" / args.project_id
    if not project.is_dir():
        raise ValueError(f"Project workspace does not exist: {project}")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return project / "artifacts/core/fusion-api/fsm-rest-client/fa-feature-tl-tasks" / f"fa-feature-tl-tasks-{stamp}.csv"


def main() -> int:
    args = parse_args()
    if args.preview_limit < 1:
        raise ValueError("--preview-limit must be at least 1")
    props = read_properties(Path(args.properties)); require_props(props, ["restBaseUrl", "boss_scope"])
    scoped = dict(props); scoped["scope"] = props["boss_scope"]
    token = get_access_token(scoped, token_cache=args.token_cache)
    stats = {"api_call_count": 0}
    if args.verbose:
        print("Subtask 1: retrieving feature metadata...", file=sys.stderr, flush=True)
    try:
        features = paged(props["restBaseUrl"], token, FEATURES, {}, stats, None if args.all else args.preview_limit)
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403}:
            raise
        token = get_access_token(scoped, token_cache=args.token_cache, force_login=True)
        features = paged(props["restBaseUrl"], token, FEATURES, {}, stats, None if args.all else args.preview_limit)
    if args.verbose:
        print(f"Subtask 1 complete: retrieved {len(features)} features.", file=sys.stderr, flush=True)

    result: list[dict[str, str]] = []
    errors: list[dict[str, str]] = []
    target = full_output_path(args) if args.all else None
    if target:
        target.parent.mkdir(parents=True, exist_ok=True)
    handle = target.open("w", newline="", encoding="utf-8") if target else None
    writer = csv.DictWriter(handle, fieldnames=FIELDS) if handle else None
    if writer:
        writer.writeheader()
    for feature in features:
        if not args.all and len(result) >= args.preview_limit:
            break
        code = value(feature, "featureShortName", "shortName", "featureCode", "code")
        if not code:
            continue
        base = {
            "PRODUCT": value(feature, "product", "productName", "userModuleName"),
            "FILTER_NAME": value(feature, "featureName", "filterName", "name", "displayName"),
            "CLASSIFICATION": classification(feature),
            "AVAILABLE_RELEASE_VERSION": value(feature, "availableReleaseVersion"),
            "EXPIRATION_RELEASE_VERSION": value(feature, "expirationReleaseVersion"),
        }
        if args.verbose:
            print(f"Subtask 2: retrieving task associations for {code}...", file=sys.stderr, flush=True)
        try:
            associations = paged(props["restBaseUrl"], token, ASSOCIATIONS, {"featureShortName": code}, stats)
        except FusionHttpError as exc:
            if exc.status_code not in {401, 403}:
                errors.append({"featureShortName": code, "endpoint": "associatedTasksAndTaskListsByFeature", "message": str(exc)})
                continue
            token = get_access_token(scoped, token_cache=args.token_cache, force_login=True)
            try:
                associations = paged(props["restBaseUrl"], token, ASSOCIATIONS, {"featureShortName": code}, stats)
            except Exception as retry_exc:
                errors.append({"featureShortName": code, "endpoint": "associatedTasksAndTaskListsByFeature", "message": str(retry_exc)})
                continue
        except Exception as exc:
            errors.append({"featureShortName": code, "endpoint": "associatedTasksAndTaskListsByFeature", "message": str(exc)})
            continue
        for association in associations:
            row = {**base, "TASK_LIST_NAME": value(association, "taskListName"), "TASK_NAME": value(association, "taskName")}
            result.append(row)
            if writer:
                writer.writerow(row)
            if not args.all and len(result) >= args.preview_limit:
                break
        if args.verbose:
            print(f"Subtask 2 complete: collected {len(result)} rows so far.", file=sys.stderr, flush=True)
    if handle:
        handle.close()

    if not args.all:
        preview = result[:args.preview_limit]
        print(json.dumps({"row_count": len(preview), "api_call_count": stats["api_call_count"], "rows": preview, "errors": errors}, indent=2, ensure_ascii=False))
        return 1 if errors and not preview else 0
    if args.verbose:
        print(f"Subtask 3 complete: wrote {len(result)} rows to {target}.", file=sys.stderr, flush=True)
    print(json.dumps({"row_count": len(result), "api_call_count": stats["api_call_count"], "csv": str(target), "errors": errors}, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
