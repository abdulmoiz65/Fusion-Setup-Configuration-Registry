#!/usr/bin/env python3
"""Fetch direct parent-to-child Oracle Fusion feature relationships."""
from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def resolve_repository_roots(script_path: Path) -> tuple[Path, Path]:
    """Return the repository root for a checkout containing ``core``."""
    parents = script_path.resolve().parents

    for parent in parents:
        if (parent / "core").is_dir():
            return parent, parent

    raise RuntimeError(
        "Unable to locate the repository root. Expected a checkout containing core."
    )


REPO_ROOT, FDOS_ROOT = resolve_repository_roots(Path(__file__))
sys.path.insert(0, str(FDOS_ROOT / "core/auth/fusion-oauth-authentication/scripts"))
from fusion_auth import FusionHttpError, get_access_token, http_json, read_properties, require_props  # noqa: E402

HIERARCHIES_ENDPOINT = "/api/boss/data/objects/ora/commonSetup/features/v1/featureHierarchies"
FEATURES_ENDPOINT = "/api/boss/data/objects/ora/commonSetup/features/v1/features"
PAGE_SIZE = 1000
HIERARCHY_PAGE_SIZE = 10000
PRODUCT_BATCH_SIZE = 100
FIELDS = [
    "PRODUCT", "PARENT_FEATURE_NAME", "PARENT_FEATURE_CODE",
    "PARENT_CLASSIFICATION", "DISPLAY_SEQUENCE", "CHILD_FEATURE_NAME",
    "CHILD_FEATURE_CODE", "CHILD_CLASSIFICATION",
]


def records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("items", "results", "rows", "data", "value"):
            candidate = payload.get(key)
            if isinstance(candidate, list):
                return [item for item in candidate if isinstance(item, dict)]
    return []


def field(row: Any, *names: str) -> str:
    if not isinstance(row, dict):
        return ""
    lowered = {str(key).lower(): value for key, value in row.items()}
    for name in names:
        candidate = lowered.get(name.lower())
        if candidate not in (None, "") and not isinstance(candidate, (dict, list)):
            return str(candidate)
    return ""


def nested(row: dict[str, Any], name: str) -> dict[str, Any]:
    return next((value for key, value in row.items() if str(key).lower() == name.lower() and isinstance(value, dict)), {})


def get_page(base_url: str, token: str, endpoint: str, params: dict[str, str], stats: dict[str, int]) -> Any:
    query = urllib.parse.urlencode(params, safe="$'=")
    stats["api_call_count"] += 1
    return http_json(base_url.rstrip("/") + endpoint + "?" + query, access_token=token, headers={"Authorization": "Bearer " + token})


def paged(base_url: str, token: str, endpoint: str, params: dict[str, str], stats: dict[str, int], limit: int = PAGE_SIZE) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    offset = 0
    while True:
        page = records(get_page(base_url, token, endpoint, {**params, "$limit": str(limit), "$offset": str(offset)}, stats))
        output.extend(page)
        if len(page) < limit:
            return output
        offset += limit


def feature_metadata(base_url: str, token: str, parent_codes: set[str], stats: dict[str, int]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for start in range(0, len(parent_codes), PRODUCT_BATCH_SIZE):
        batch = sorted(parent_codes)[start:start + PRODUCT_BATCH_SIZE]
        quoted = ",".join("'" + code.replace("'", "''") + "'" for code in batch)
        result.extend(paged(base_url, token, FEATURES_ENDPOINT, {"$filter": f"featureShortName in ({quoted})"}, stats))
    return result


def sequence_key(value: str) -> tuple[int, float | str]:
    try:
        return (0, float(value))
    except ValueError:
        return (1, value)


def classification(value: str) -> str:
    normalized = value.strip().upper()
    if normalized in {"ROOT_NODE", "OFFERING"}:
        return "Offering"
    if normalized in {"LICENSE", "FUNCTIONAL_AREA", "FUNCTIONAL AREA"}:
        return "Functional Area"
    return "Feature"


def build_rows(hierarchies: list[dict[str, Any]], products: dict[str, str]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    seen: set[tuple[str, ...]] = set()
    for hierarchy in hierarchies:
        parent = nested(hierarchy, "parentFeature")
        child = nested(hierarchy, "childFeature")
        row = {
            "PRODUCT": products.get(field(parent, "featureId"), ""),
            "PARENT_FEATURE_NAME": field(parent, "featureName"),
            "PARENT_FEATURE_CODE": field(parent, "featureShortName"),
            "PARENT_CLASSIFICATION": classification(field(parent, "classification")),
            "DISPLAY_SEQUENCE": field(hierarchy, "displaySequence"),
            "CHILD_FEATURE_NAME": field(child, "featureName"),
            "CHILD_FEATURE_CODE": field(child, "featureShortName"),
            "CHILD_CLASSIFICATION": classification(field(child, "classification")),
        }
        if not row["PARENT_FEATURE_CODE"] or not row["CHILD_FEATURE_CODE"]:
            continue
        identity = tuple(row[column] for column in FIELDS)
        if identity not in seen:
            seen.add(identity)
            result.append(row)
    return sorted(result, key=lambda row: (row["PRODUCT"], row["PARENT_FEATURE_NAME"], sequence_key(row["DISPLAY_SEQUENCE"]), row["CHILD_FEATURE_NAME"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--properties", default=str(FDOS_ROOT / "core/auth/fusionEnv.properties"))
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--parent-feature-code")
    parser.add_argument("--preview-limit", type=int, default=25)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--output")
    parser.add_argument("--project-id")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.preview_limit < 1:
        parser.error("--preview-limit must be positive")
    props = read_properties(Path(args.properties))
    require_props(props, ["restBaseUrl", "boss_scope"])
    scoped = dict(props)
    scoped["scope"] = props["boss_scope"]
    token = get_access_token(scoped, token_cache=args.token_cache)
    stats = {"api_call_count": 0}
    hierarchy_params: dict[str, str] = {"$filter": "feature.featureShortName=parentFeature.featureShortName"}
    if args.parent_feature_code:
        hierarchy_params["$filter"] = f"feature.featureShortName='{args.parent_feature_code}'"
    if args.verbose:
        print("Subtask 1: retrieving feature hierarchy relationships...", file=sys.stderr, flush=True)
    try:
        hierarchy_rows = paged(props["restBaseUrl"], token, HIERARCHIES_ENDPOINT, hierarchy_params, stats, HIERARCHY_PAGE_SIZE)
        parent_codes = {field(nested(row, "parentFeature"), "featureShortName") for row in hierarchy_rows}
        feature_rows = feature_metadata(props["restBaseUrl"], token, parent_codes - {""}, stats)
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403}:
            raise
        token = get_access_token(scoped, token_cache=args.token_cache, force_login=True)
        hierarchy_rows = paged(props["restBaseUrl"], token, HIERARCHIES_ENDPOINT, hierarchy_params, stats, HIERARCHY_PAGE_SIZE)
        parent_codes = {field(nested(row, "parentFeature"), "featureShortName") for row in hierarchy_rows}
        feature_rows = feature_metadata(props["restBaseUrl"], token, parent_codes - {""}, stats)
    if args.verbose:
        print(f"Subtask 1 complete: retrieved {len(hierarchy_rows)} hierarchy rows.", file=sys.stderr, flush=True)
        print(f"Subtask 2 complete: retrieved metadata for {len(feature_rows)} parent features.", file=sys.stderr, flush=True)
    products = {field(row, "featureId"): field(nested(row, "family"), "userModuleName") for row in feature_rows if field(row, "featureId")}
    output = build_rows(hierarchy_rows, products)
    result: dict[str, Any] = {"parent_feature_count": len({row["PARENT_FEATURE_CODE"] for row in output}), **stats, "row_count": len(output)}
    if not args.all:
        result["rows"] = output[:args.preview_limit]
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    target = Path(args.output) if args.output else None
    if target is None:
        if not args.project_id:
            raise ValueError("Full export requires --project-id or --output")
        target = REPO_ROOT / "project" / args.project_id / "artifacts/shared/implementation-planning/parent-child-feature-hierarchy" / ("parent-child-feature-hierarchy-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + ".csv")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(output)
    if args.verbose:
        print(f"Subtask 3 complete: wrote {len(output)} rows to {target}.", file=sys.stderr, flush=True)
    result["csv"] = str(target)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
