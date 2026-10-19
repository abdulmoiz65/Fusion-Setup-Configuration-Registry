#!/usr/bin/env python3
"""Set Oracle Fusion FSM Redwood opt-in status using FSCR OAuth."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SKILL_ID = "shared.implementation-planning.fsm-set-optin.fsm-set-optin"
TRIGGER = "fsm set optin"


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "core" / "auth" / "fusion-oauth-authentication").exists():
            return candidate
    raise RuntimeError("Could not locate repository root with the required layout")


REPO_ROOT = find_repo_root(Path(__file__).resolve())
FUSION_SKILLS_ROOT = REPO_ROOT
AUTH_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "core" / "auth" / "fusion-oauth-authentication" / "scripts"
PROJECT_MGMT_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "core" / "project-mgmt" / "scripts"
DEFAULT_PROPERTIES_PATH = FUSION_SKILLS_ROOT / "core" / "auth" / "fusionEnv.properties"
PROJECTS_ROOT = FUSION_SKILLS_ROOT / "project"
sys.path.insert(0, str(AUTH_SCRIPTS_PATH))
sys.path.insert(0, str(PROJECT_MGMT_SCRIPTS_PATH))

from fusion_auth import (  # noqa: E402
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    FusionHttpError,
    get_access_token,
    read_properties,
    require_props,
)
from fsm_set_optin_engine import (  # noqa: E402
    DEFAULT_PAGE_SIZE,
    OptinError,
    OptinHttpError,
    normalize_action,
    normalize_base_url,
    validate_base_url,
    run_set_optin as run_set_optin_engine,
    slug,
)
from token_usage_logger import append_token_usage_log  # noqa: E402


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_fusion_common_scope(props: dict[str, str]) -> str:
    configured = (
        props.get("fusion_common_features_crud_scope")
        or props.get("fusion_common_scope")
        or props.get("fusionCommonFeaturesCrudScope")
        or props.get("fusionCommonScope")
    )
    if configured:
        return configured
    environment = props.get("environment", "").strip()
    if not environment:
        raise ValueError(
            "Missing fusion common scope. Add fusion_common_features_crud_scope to fusionEnv.properties "
            "or define environment so the default scope can be derived."
        )
    return f"urn:opc:resource:fusion:{environment}:fusion-common/urn:oracle:internal:fusion-common:features:crud"


def props_with_scope(props: dict[str, str], scope: str) -> dict[str, str]:
    scoped = dict(props)
    scoped["scope"] = scope
    return scoped


def project_artifacts_root(project_id: str) -> Path:
    return PROJECTS_ROOT / project_id / "artifacts"


def resolve_project_id(explicit_project_id: str | None = None, default_project_id: str | None = None) -> str:
    if explicit_project_id:
        return explicit_project_id
    env_project_id = os.environ.get("FDOS_PROJECT_ID")
    if env_project_id:
        return env_project_id
    if default_project_id:
        return default_project_id

    candidates = [
        path.parent.parent.name
        for path in PROJECTS_ROOT.glob("*/state/project-state.json")
        if path.parent.parent.name != "_template"
    ]
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise RuntimeError("No project workspace found under project/{project_id}. Pass --project-id.")
    raise RuntimeError(
        "Multiple project workspaces found under project/{project_id}. Pass --project-id or set FDOS_PROJECT_ID."
    )


def default_output_dir(project_id: str, target_type: str, target: str) -> Path:
    return project_artifacts_root(project_id) / "shared" / "implementation-planning" / "fsm-set-optin" / slug(target_type) / slug(target)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set Oracle Fusion FSM Redwood opt-in status.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    parser.add_argument("--base-url", help="Fusion host, UI URL, or REST root on the HTTPS origin configured by restBaseUrl.")
    parser.add_argument("--api-version", default="latest")
    parser.add_argument("--target-type", choices=["offering", "functional-area", "feature"], required=True)
    parser.add_argument("--target", required=True, help="Target display name or short name/code.")
    parser.add_argument("--action", required=True, help="opt-in/enable, opt-out/disable, or set-choices.")
    parser.add_argument("--offering", help="Parent offering name or short name for functional-area or feature targets.")
    parser.add_argument("--offering-id", help="Parent offering ID when already known.")
    parser.add_argument("--feature-choices", help="Comma-separated choice names or short names.")
    parser.add_argument("--output-dir")
    parser.add_argument("--project-id", help="Project workspace ID under project/{project_id}. Defaults to FDOS_PROJECT_ID or environment.")
    parser.add_argument("--dry-run", action="store_true", help="Resolve and build the PATCH/refresh plan without writing.")
    parser.add_argument("--force", action="store_true", help="Override disable safety warnings where allowed.")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE)
    parser.add_argument("--auth-code")
    parser.add_argument("--redirect-url")
    parser.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--boss-token-cache", default="auto")
    parser.add_argument("--fusion-common-token-cache", default="auto")
    parser.add_argument("--force-login", action="store_true")
    parser.add_argument("--access-token", help="Existing standard Fusion REST bearer token. Skips token cache and login for ADF calls.")
    parser.add_argument("--boss-access-token", help="Existing BOSS bearer token. Skips BOSS token cache and login.")
    parser.add_argument("--fusion-common-access-token", help="Existing Fusion Common features CRUD bearer token. Skips token cache and login.")
    parser.add_argument("--open-browser", action="store_true", default=True)
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    return parser.parse_args()


def get_token(
    props: dict[str, str],
    args: argparse.Namespace,
    *,
    access_token_attr: str,
    token_cache_attr: str,
    force_login: bool = False,
) -> str:
    explicit_token = getattr(args, access_token_attr, None)
    if explicit_token:
        return str(explicit_token)
    return get_access_token(
        props,
        redirect_url=args.redirect_url,
        auth_code=args.auth_code,
        open_browser=args.open_browser,
        callback_timeout=args.callback_timeout,
        token_cache=getattr(args, token_cache_attr),
        force_login=args.force_login or force_login,
    )


def get_tokens(props: dict[str, str], args: argparse.Namespace, *, force_login: bool = False) -> dict[str, str | None]:
    require_props(props, ["environment", "restBaseUrl", "scope", "boss_scope"])
    standard_token = get_token(
        props_with_scope(props, props["scope"]),
        args,
        access_token_attr="access_token",
        token_cache_attr="token_cache",
        force_login=force_login,
    )
    boss_token = get_token(
        props_with_scope(props, props["boss_scope"]),
        args,
        access_token_attr="boss_access_token",
        token_cache_attr="boss_token_cache",
        force_login=force_login,
    )
    fusion_common_token = None
    if not args.dry_run:
        fusion_common_token = get_token(
            props_with_scope(props, default_fusion_common_scope(props)),
            args,
            access_token_attr="fusion_common_access_token",
            token_cache_attr="fusion_common_token_cache",
            force_login=force_login,
        )
    return {
        "standard": standard_token,
        "boss": boss_token,
        "fusion_common": fusion_common_token,
    }


def artifact_paths_from_summary(summary: dict[str, Any]) -> list[Path]:
    return [
        Path(str(path))
        for path in (summary.get("processOutputPath"), summary.get("standardReportPath"))
        if path
    ]


def run_set_optin(
    props: dict[str, str],
    args: argparse.Namespace,
    *,
    skill_id: str = SKILL_ID,
    trigger: str = TRIGGER,
    force_login: bool = False,
) -> int:
    args.activity_start_time = getattr(args, "activity_start_time", utc_now())
    project_id = resolve_project_id(args.project_id, props.get("environment"))
    approved_origin = normalize_base_url(props["restBaseUrl"])
    base_url = validate_base_url(args.base_url or props["restBaseUrl"], approved_origin)
    action = normalize_action(args.action)
    output_dir = Path(args.output_dir) if args.output_dir else default_output_dir(project_id, args.target_type, args.target)
    tokens = get_tokens(props, args, force_login=force_login)
    summary = run_set_optin_engine(
        standard_access_token=str(tokens["standard"]),
        boss_access_token=str(tokens["boss"]),
        fusion_common_access_token=str(tokens["fusion_common"]) if tokens["fusion_common"] else None,
        base_url=base_url,
        approved_origin=approved_origin,
        api_version=args.api_version,
        target_type=args.target_type,
        target=args.target,
        action=action,
        offering=args.offering,
        offering_id=args.offering_id,
        feature_choices=args.feature_choices,
        output_dir=output_dir,
        dry_run=args.dry_run,
        force=args.force,
        page_size=args.page_size,
    )
    token_log_path = append_token_usage_log(
        project_id=project_id,
        skill_id=skill_id,
        task=f"Set FSM opt-in: {args.target}",
        trigger=trigger,
        activity_start_time=args.activity_start_time,
        artifact_paths=artifact_paths_from_summary(summary),
        files_read=0,
        estimated_input_tokens=0,
        notes=(
            f"TargetType={args.target_type}; Action={action}; DryRun={args.dry_run}. "
            "Sensitive properties and token cache contents are excluded from estimates."
        ),
    )
    summary["tokenUsageLogPath"] = str(token_log_path)
    print(json.dumps({"ok": True, "summary": summary}, indent=2, ensure_ascii=False, default=str))
    return 0


def main() -> int:
    args = parse_args()
    args.activity_start_time = utc_now()
    props = read_properties(Path(args.properties))
    require_props(props, ["environment", "restBaseUrl"])
    try:
        return run_set_optin(props, args)
    except (FusionHttpError, OptinHttpError) as exc:
        status_code = getattr(exc, "status_code", None)
        if status_code not in {401, 403} or args.access_token or args.boss_access_token or args.fusion_common_access_token:
            raise
        print("Cached access token was rejected by Fusion. Running login flow again.", file=sys.stderr)
        return run_set_optin(props, args, force_login=True)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OptinError, FusionHttpError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        raise SystemExit(1)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        raise SystemExit(1)
