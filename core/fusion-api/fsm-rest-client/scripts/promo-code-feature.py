#!/usr/bin/env python3
"""Return promotion-code solution-bundle feature rows or export them to CSV."""
from __future__ import annotations
import argparse, csv, json, sys, urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "core/auth/fusion-oauth-authentication/scripts"))
from fusion_auth import FusionHttpError, get_access_token, http_bytes, read_properties, require_props  # noqa: E402
BUNDLES = "/api/boss/extraction/queries/ora/commonSetup/features/v1/searchPromotionCodes"
FEATURES = "/api/boss/extraction/queries/ora/commonSetup/features/v1/promotionCodeAssociatedFeatures"
FIELDS = ["PRODUCT", "SOLUTION_BUNDLE_NAME", "SOLUTION_BUNDLE_CODE", "FEATURE_NAME", "FEATURE_CODE"]

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
def get(base: str, token: str, endpoint: str, params: dict[str, Any], stats: dict[str, int]) -> Any:
    stats["api_call_count"] += 1; query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}, safe="$'=")
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
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("--properties", default=str(ROOT / "core/auth/fusionEnv.properties")); p.add_argument("--token-cache", default="auto"); p.add_argument("--preview-limit", type=int, default=25); p.add_argument("--all", action="store_true"); p.add_argument("--project-id"); p.add_argument("--output"); p.add_argument("--verbose", action="store_true"); args = p.parse_args()
    if args.preview_limit < 1: raise ValueError("--preview-limit must be at least 1")
    if args.all and not (args.project_id or args.output): raise ValueError("Full export requires --project-id or --output")
    props = read_properties(Path(args.properties)); require_props(props, ["restBaseUrl", "boss_scope"]); scoped = dict(props); scoped["scope"] = props["boss_scope"]; token = get_access_token(scoped, token_cache=args.token_cache); stats = {"api_call_count": 0}
    if args.verbose: print("Subtask 1: retrieving promotion codes...", file=sys.stderr, flush=True)
    try: bundles = paged(props["restBaseUrl"], token, BUNDLES, {}, stats, 100, None if args.all else args.preview_limit)
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403}: raise
        token = get_access_token(scoped, token_cache=args.token_cache, force_login=True); bundles = paged(props["restBaseUrl"], token, BUNDLES, {}, stats, 100, None if args.all else args.preview_limit)
    if args.verbose: print(f"Subtask 1 complete: retrieved {len(bundles)} promotion codes.", file=sys.stderr, flush=True)
    result, errors = [], []
    for bundle in bundles:
        if not args.all and len(result) >= args.preview_limit: break
        name, code = val(bundle, "promotionCodeName", "solutionBundleName", "name", "displayName"), val(bundle, "promotionCodeShortName", "solutionBundleShortName", "solutionBundleCode", "shortName", "code")
        if not code or "PROMOTION_CODE" not in code: continue
        if args.verbose: print(f"Subtask 2: retrieving features for {code}...", file=sys.stderr, flush=True)
        try: features = paged(props["restBaseUrl"], token, FEATURES, {"promotionCodeShortName": code}, stats)
        except Exception as exc: errors.append({"solutionBundleShortName": code, "message": str(exc)}); continue
        for feature in features:
            result.append({"PRODUCT": val(feature, "product", "productName") or val(bundle, "product", "productName"), "SOLUTION_BUNDLE_NAME": name, "SOLUTION_BUNDLE_CODE": code, "FEATURE_NAME": val(feature, "featureName", "name", "displayName"), "FEATURE_CODE": val(feature, "featureShortName", "featureCode", "shortName", "code")})
            if not args.all and len(result) >= args.preview_limit: break
        if args.verbose: print(f"Subtask 2 complete: collected {len(result)} rows so far.", file=sys.stderr, flush=True)
    if not args.all: print(json.dumps({"row_count": len(result), **stats, "rows": result[:args.preview_limit], "errors": errors}, indent=2, ensure_ascii=False)); return 1 if errors and not result else 0
    target = Path(args.output) if args.output else ROOT / "project" / args.project_id / "artifacts/core/fusion-api/fsm-rest-client/promo-code-feature" / f"promo-code-feature-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.csv"; target.parent.mkdir(parents=True, exist_ok=True)
    if args.verbose: print("Subtask 3: writing CSV...", file=sys.stderr, flush=True)
    with target.open("w", newline="", encoding="utf-8") as f: w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(result)
    if args.verbose: print(f"Subtask 3 complete: wrote {len(result)} rows to {target}.", file=sys.stderr, flush=True)
    print(json.dumps({"row_count": len(result), **stats, "csv": str(target), "errors": errors}, indent=2, ensure_ascii=False)); return 1 if errors else 0
if __name__ == "__main__":
    try: raise SystemExit(main())
    except Exception as exc: print(f"Error: {exc}", file=sys.stderr); raise SystemExit(1)
