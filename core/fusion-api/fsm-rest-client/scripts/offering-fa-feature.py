#!/usr/bin/env python3
"""Fetch offering/FA/feature rows through the BOSS hierarchy extractions."""
from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FDOS_ROOT = Path(__file__).resolve().parents[4]
REPO_ROOT = FDOS_ROOT
sys.path.insert(0, str(FDOS_ROOT / "core/auth/fusion-oauth-authentication/scripts"))
from fusion_auth import FusionHttpError, get_access_token, http_json, read_properties, require_props  # noqa: E402

BASE = "/api/boss/extraction/queries/ora/commonSetup/features/v1"
OFFERINGS_ENDPOINT = "/api/boss/data/objects/ora/commonSetup/features/v1/features/$views/availableOfferings"
FA_ENDPOINT = BASE + "/availableFunctionalAreasByOffering"
FEATURE_ENDPOINT = BASE + "/availableFeaturesByOffering"
FA_META_ENDPOINT = BASE + "/$en/searchFunctionalAreas"
FEATURE_META_ENDPOINT = BASE + "/$en/searchFeatures"
DEPENDENCY_ENDPOINT = "/api/boss/data/objects/ora/commonSetup/features/v1/dependencies"
ENRICHMENT_BATCH_SIZE = 50
FIELDS = [
    "OFFERING", "FA_FEATURE", "PRODUCT_FAMILY", "PRODUCT", "CLASSIFICATION",
    "PATH", "FOF_AVAILABLE_RELEASE_VERSION", "FOF_EXPIRATION_RELEASE_VERSION",
]


def rows(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        for key in ("items", "results", "rows", "data", "value"):
            if isinstance(value.get(key), list):
                return [item for item in value[key] if isinstance(item, dict)]
    return []


def text(row: dict[str, Any], *keys: str) -> str:
    lowered = {str(key).lower(): value for key, value in row.items()}
    for key in keys:
        value = lowered.get(key.lower())
        if value not in (None, ""):
            return str(value)
    return ""


def get_json(base_url: str, token: str, endpoint: str, params: dict[str, Any]) -> Any:
    query = urllib.parse.urlencode({key: value for key, value in params.items() if value is not None})
    url = base_url.rstrip("/") + endpoint + ("?" + query if query else "")
    return http_json(url, access_token=token, headers={"Authorization": "Bearer " + token})


def is_empty_json_response(error: RuntimeError) -> bool:
    """Return whether the shared JSON client rejected a zero-byte response."""
    message = str(error)
    prefix = "Expected JSON from "
    marker = ", got:"
    return message.startswith(prefix) and marker in message and not message.rsplit(marker, 1)[1].strip()


def paged(base_url: str, token: str, endpoint: str, params: dict[str, Any], limit: int = 100) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    offset = 0
    while True:
        try:
            response = get_json(base_url, token, endpoint, {**params, "$limit": limit, "$offset": offset})
        except RuntimeError as exc:
            if is_empty_json_response(exc):
                return result
            raise
        page = rows(response)
        result.extend(page)
        if len(page) < limit:
            return result
        offset += limit


def quoted_feature_filter(codes: set[str], field_name: str = "featureShortName") -> str:
    quoted = ",".join("'" + code.replace("'", "''") + "'" for code in sorted(codes))
    return f"{field_name} in ({quoted})"


def metadata_index(base_url: str, token: str, endpoint: str, codes: set[str]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    sorted_codes = sorted(codes)
    for start in range(0, len(sorted_codes), ENRICHMENT_BATCH_SIZE):
        batch = set(sorted_codes[start:start + ENRICHMENT_BATCH_SIZE])
        for row in paged(base_url, token, endpoint, {"$filter": quoted_feature_filter(batch)}):
            code = text(row, "featureShortName")
            if code:
                result[code] = row
    return result


def dependency_index(base_url: str, token: str, codes: set[str]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    sorted_codes = sorted(codes)
    for start in range(0, len(sorted_codes), ENRICHMENT_BATCH_SIZE):
        batch = set(sorted_codes[start:start + ENRICHMENT_BATCH_SIZE])
        filter_value = "availableFlag=true and " + quoted_feature_filter(batch, "feature.featureShortName")
        for dependency in paged(base_url, token, DEPENDENCY_ENDPOINT, {"$filter": filter_value}):
            feature = dependency.get("feature")
            if isinstance(feature, dict) and text(feature, "featureShortName"):
                result[text(feature, "featureShortName")] = dependency
    return result


def merge_batch_csvs(batch_dir: Path, target: Path) -> dict[str, Any]:
    batch_files = sorted(batch_dir.glob("offering-fa-feature-[0-9][0-9]-[0-9][0-9].csv"))
    if not batch_files:
        raise ValueError(f"No offering-fa-feature batch CSVs found in {batch_dir}")
    target.parent.mkdir(parents=True, exist_ok=True)
    row_count = 0
    with target.open("w", newline="", encoding="utf-8") as target_handle:
        writer = csv.DictWriter(target_handle, fieldnames=FIELDS)
        writer.writeheader()
        for batch_file in batch_files:
            with batch_file.open(newline="", encoding="utf-8") as batch_handle:
                reader = csv.DictReader(batch_handle)
                if reader.fieldnames != FIELDS:
                    raise ValueError(f"Unexpected CSV header in {batch_file}")
                for row in reader:
                    writer.writerow({field: row.get(field, "") for field in FIELDS})
                    row_count += 1
    return {"csv": str(target), "batch_count": len(batch_files), "row_count": row_count, "errors": []}


def display_path(path: str, names: dict[str, str], offering_name: str) -> str:
    parts = [part for part in path.strip("/").split("/") if part]
    return "/".join([offering_name] + [names.get(part, part) for part in parts[1:]]) if parts else offering_name


def build_rows(offering: dict[str, Any], fas: list[dict[str, Any]], features: list[dict[str, Any]], fa_meta: dict[str, dict[str, Any]], feature_meta: dict[str, dict[str, Any]], dependencies: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    offering_code = text(offering, "featureShortName")
    offering_name = text(offering, "featureName") or offering_code
    names = {offering_code: offering_name}
    for row in fas + features:
        code = text(row, "childFeatureShortName", "featureShortName")
        name = text(row, "childFeatureName", "featureName")
        if code and name:
            names[code] = name
    direct_fa_codes = {
        text(row, "childFeatureShortName", "featureShortName")
        for row in fas
        if len([part for part in text(row, "path").strip("/").split("/") if part]) == 2
    }
    output: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in fas + features:
        code = text(row, "childFeatureShortName", "featureShortName")
        name = text(row, "childFeatureName", "featureName")
        if not code or not name or code in seen:
            continue
        seen.add(code)
        meta = fa_meta.get(code, {}) if code in direct_fa_codes else feature_meta.get(code, {})
        dependency = dependencies.get(code, {})
        path = text(row, "path")
        output.append({
            "OFFERING": offering_name,
            "FA_FEATURE": name,
            "PRODUCT_FAMILY": text(meta, "productFamily", "familyModuleGUID", "product_family"),
            "PRODUCT": text(meta, "product"),
            "CLASSIFICATION": "Functional Area" if code in direct_fa_codes else "Feature",
            "PATH": display_path(path, names, offering_name),
            "FOF_AVAILABLE_RELEASE_VERSION": text(dependency, "availableReleaseVersion") or text(row, "availableReleaseVersion"),
            "FOF_EXPIRATION_RELEASE_VERSION": text(dependency, "expirationReleaseVersion") or text(row, "expirationReleaseVersion"),
        })
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--properties", default=str(FDOS_ROOT / "core/auth/fusionEnv.properties"))
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--offering-short-name")
    parser.add_argument("--preview-limit", type=int, default=25)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--offering-offset", type=int, default=0)
    parser.add_argument("--offering-limit", type=int)
    parser.add_argument("--skip-metadata-enrichment", action="store_true")
    parser.add_argument("--skip-dependency-enrichment", action="store_true")
    parser.add_argument("--merge-batches-dir", type=Path)
    parser.add_argument("--output")
    parser.add_argument("--project-id")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.preview_limit < 1:
        parser.error("--preview-limit must be positive")
    if args.offering_offset < 0:
        parser.error("--offering-offset must be zero or positive")
    if args.offering_limit is not None and args.offering_limit < 1:
        parser.error("--offering-limit must be positive")
    if args.merge_batches_dir:
        if not args.output:
            parser.error("--merge-batches-dir requires --output")
        print(json.dumps(merge_batch_csvs(args.merge_batches_dir, Path(args.output)), indent=2))
        return 0
    props = read_properties(Path(args.properties))
    require_props(props, ["restBaseUrl", "boss_scope"])
    scoped = dict(props)
    scoped["scope"] = props["boss_scope"]
    token = get_access_token(scoped, token_cache=args.token_cache)
    if args.verbose:
        print("Subtask 1: retrieving available offerings...", file=sys.stderr, flush=True)
    try:
        offerings = paged(props["restBaseUrl"], token, OFFERINGS_ENDPOINT, {})
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403}:
            raise
        token = get_access_token(scoped, token_cache=args.token_cache, force_login=True)
        offerings = paged(props["restBaseUrl"], token, OFFERINGS_ENDPOINT, {})
    if args.verbose:
        print(f"Subtask 1 complete: retrieved {len(offerings)} offerings.", file=sys.stderr, flush=True)
    selected = [row for row in offerings if not args.offering_short_name or text(row, "featureShortName") == args.offering_short_name]
    if args.offering_short_name and not selected:
        raise ValueError(f"Offering not found in availableOfferings: {args.offering_short_name}")
    if args.offering_offset or args.offering_limit is not None:
        end = None if args.offering_limit is None else args.offering_offset + args.offering_limit
        selected = selected[args.offering_offset:end]
    if not args.all:
        selected = selected[:5]
    errors: list[dict[str, str]] = []
    calls = 1
    hierarchy_rows: list[tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]] = []
    for index, offering in enumerate(selected, start=1):
        code = text(offering, "featureShortName")
        if args.verbose:
            print(f"Retrieving hierarchy {index}/{len(selected)}: {code}", file=sys.stderr, flush=True)
        fas: list[dict[str, Any]] = []
        features: list[dict[str, Any]] = []
        try:
            fas = paged(props["restBaseUrl"], token, FA_ENDPOINT, {"parentShortName": code})
            calls += 1
        except Exception as exc:
            errors.append({"offering": code, "endpoint": "functional_areas", "message": str(exc)})
        try:
            features = paged(props["restBaseUrl"], token, FEATURE_ENDPOINT, {"parentShortName": code})
            calls += 1
        except Exception as exc:
            errors.append({"offering": code, "endpoint": "features", "message": str(exc)})
        hierarchy_rows.append((offering, fas, features))

    direct_fa_codes = {
        text(row, "childFeatureShortName", "featureShortName")
        for _, fas, _ in hierarchy_rows
        for row in fas
        if len([part for part in text(row, "path").strip("/").split("/") if part]) == 2
    }
    returned_codes = {
        text(row, "childFeatureShortName", "featureShortName")
        for _, fas, features in hierarchy_rows
        for row in fas + features
        if text(row, "childFeatureShortName", "featureShortName")
    }
    print(
        f"Scoped hierarchy retrieval complete: {len(selected)} offering(s), "
        f"{len(returned_codes)} returned feature code(s). Beginning bounded enrichment.",
        file=sys.stderr,
        flush=True,
    )
    if args.verbose:
        print("Subtask 2: enriching returned metadata and release dependencies...", file=sys.stderr, flush=True)
    fa_meta = {} if args.skip_metadata_enrichment else metadata_index(props["restBaseUrl"], token, FA_META_ENDPOINT, direct_fa_codes)
    feature_meta = {} if args.skip_metadata_enrichment else metadata_index(props["restBaseUrl"], token, FEATURE_META_ENDPOINT, returned_codes - direct_fa_codes)
    dependencies = {} if args.skip_dependency_enrichment else dependency_index(props["restBaseUrl"], token, returned_codes)
    if args.verbose:
        print("Subtask 2 complete: bounded enrichment data retrieved.", file=sys.stderr, flush=True)
    output: list[dict[str, str]] = []
    target = Path(args.output) if args.output else None
    writer = None
    handle = None
    if args.all:
        if target is None:
            if not args.project_id:
                raise ValueError("Full export requires --project-id or --output")
            folder = REPO_ROOT / "project" / args.project_id / "artifacts/shared/implementation-planning/offering-fa-feature-catalog"
            target = folder / ("offering-fa-feature-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + ".csv")
        target.parent.mkdir(parents=True, exist_ok=True)
        handle = target.open("w", newline="", encoding="utf-8")
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
    try:
        for offering, fas, features in hierarchy_rows:
            if fas or features:
                offering_rows = build_rows(offering, fas, features, fa_meta, feature_meta, dependencies)
                output.extend(offering_rows)
                if writer and handle:
                    writer.writerows(offering_rows)
                    handle.flush()
    finally:
        if handle:
            handle.close()
    if not args.all:
        print(json.dumps({"offering_count": len(selected), "api_call_count": calls, "row_count": len(output), "rows": output[:args.preview_limit], "errors": errors}, indent=2, ensure_ascii=False))
        return 1 if errors and not output else 0
    print(json.dumps({"csv": str(target), "offering_count": len(selected), "api_call_count": calls, "row_count": len(output), "errors": errors}, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
