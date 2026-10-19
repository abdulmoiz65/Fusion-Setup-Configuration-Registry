#!/usr/bin/env python3
"""Resolve offering/functional-area codes and import FSM setup data from CSV."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "shared" / "setup-import" / "fsm-csv-import").exists():
            return candidate
    raise RuntimeError("Could not locate repository root with the required layout")


REPO_ROOT = find_repo_root(Path(__file__).resolve())
FUSION_SKILLS_ROOT = REPO_ROOT
FSM_IMPORT_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "shared" / "setup-import" / "fsm-csv-import" / "scripts"
AUTH_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "core" / "auth" / "fusion-oauth-authentication" / "scripts"
sys.path.insert(0, str(FSM_IMPORT_SCRIPTS_PATH))
sys.path.insert(0, str(AUTH_SCRIPTS_PATH))

from fusion_auth import (  # noqa: E402
    DEFAULT_CALLBACK_TIMEOUT_SECONDS,
    FusionHttpError,
    get_access_token,
    read_properties,
    require_props,
)
from fusion_skill_paths import DEFAULT_PROPERTIES_PATH, project_artifacts_root  # noqa: E402
from fsm_csv_import_engine import (  # noqa: E402
    ERROR_STATUS_CODES,
    TERMINAL_STATUS_CODES,
    ImportScope,
    create_import_process,
    download_process_log,
    extract_process_id,
    process_completed,
    read_zip_as_base64,
    resolve_feature_code,
    slug,
    status_code,
    wait_for_result,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import Fusion setup data for a functional area from a CSV ZIP package.")
    parser.add_argument("--properties", default=str(DEFAULT_PROPERTIES_PATH))
    offering = parser.add_mutually_exclusive_group(required=True)
    offering.add_argument("--offering-code")
    offering.add_argument("--offering-name")
    functional_area = parser.add_mutually_exclusive_group(required=True)
    functional_area.add_argument("--functional-area-code")
    functional_area.add_argument("--functional-area-name")
    parser.add_argument("--zip-file", required=True, help="Path to the setup data ZIP file to import.")
    parser.add_argument("--search-limit", type=int, default=25)
    parser.add_argument("--wait-seconds", type=int, default=180)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--project-id", help="Project workspace ID under project/{project_id}.")
    parser.add_argument("--output-dir")
    parser.add_argument("--auth-code")
    parser.add_argument("--redirect-url")
    parser.add_argument("--callback-timeout", type=int, default=DEFAULT_CALLBACK_TIMEOUT_SECONDS)
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--force-login", action="store_true")
    parser.add_argument("--access-token")
    parser.add_argument("--open-browser", action="store_true", default=True)
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    return parser.parse_args()


def get_token(props: dict[str, str], args: argparse.Namespace, *, force_login: bool = False) -> str:
    if args.access_token:
        return str(args.access_token)
    return get_access_token(
        props,
        redirect_url=args.redirect_url,
        auth_code=args.auth_code,
        open_browser=args.open_browser,
        callback_timeout=args.callback_timeout,
        token_cache=args.token_cache,
        force_login=args.force_login or force_login,
    )


def resolve_scope_feature_code(
    props: dict[str, str],
    access_token: str,
    *,
    code: str | None,
    name: str | None,
    feature_type: str,
    search_limit: int,
) -> str:
    if code:
        return code
    if not name:
        raise ValueError("Feature name or code is required.")
    feature_code = resolve_feature_code(props, access_token, name, feature_type=feature_type, limit=search_limit)
    print(f"{feature_type.title().replace('_', ' ')} FeatureCode: {feature_code} ({name})")
    return feature_code


def default_output_dir(project_id: str | None, offering_code: str, functional_area_code: str) -> Path:
    if project_id:
        root = project_artifacts_root(project_id)
    else:
        root = FUSION_SKILLS_ROOT / "project" / "_adhoc" / "artifacts"
    return (
        root
        / "shared"
        / "setup-import"
        / "functional-area-import"
        / slug(offering_code)
        / slug(functional_area_code)
    )


def run_import(props: dict[str, str], access_token: str, args: argparse.Namespace) -> int:
    offering_code = resolve_scope_feature_code(
        props,
        access_token,
        code=args.offering_code,
        name=args.offering_name,
        feature_type="OFFERING",
        search_limit=args.search_limit,
    )
    functional_area_code = resolve_scope_feature_code(
        props,
        access_token,
        code=args.functional_area_code,
        name=args.functional_area_name,
        feature_type="FUNCTIONAL_AREA",
        search_limit=args.search_limit,
    )
    scope = ImportScope(
        kind="functional-area",
        primary_code=offering_code,
        functional_area_code=functional_area_code,
    )
    zip_file = Path(args.zip_file)
    file_content_base64 = read_zip_as_base64(zip_file)

    response = create_import_process(props, access_token, scope, file_content_base64)
    process_id = extract_process_id(response, scope.process_child)
    if not process_id:
        raise RuntimeError(f"Fusion did not return a ProcessId: {response}")
    print(f"Started functional-area CSV import process: {process_id}")

    output_dir = (
        Path(args.output_dir)
        if args.output_dir
        else default_output_dir(args.project_id, offering_code, functional_area_code)
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = (
        output_dir
        / f"{props['environment']}_setup_functional_area_csv_import_{slug(offering_code)}_{slug(functional_area_code)}_{process_id}.json"
    )
    metadata_path.write_text(
        json.dumps(
            {
                "environment": props["environment"],
                "scope": scope.kind,
                "offeringCode": offering_code,
                "functionalAreaCode": functional_area_code,
                "zipFile": str(zip_file),
                "processId": str(process_id),
                "apiResource": scope.resource_root,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    process_status, result_items = wait_for_result(
        props,
        access_token,
        scope,
        str(process_id),
        args.wait_seconds,
        args.poll_interval,
    )
    current_status = status_code(result_items)
    if not process_completed(process_status.get("ProcessCompletedFlag")) and current_status not in TERMINAL_STATUS_CODES:
        print("Import process is not complete yet.")
        print(f"OfferingCode: {offering_code}")
        print(f"FunctionalAreaCode: {functional_area_code}")
        print(f"ProcessId: {process_id}")
        print(f"StatusCode: {current_status or '(no result yet)'}")
        print("Polling stopped. Ask to retry this ProcessId before retrieving import process artifacts.")
        print(f"Wrote {metadata_path}")
        return 3

    raw_content = download_process_log(props, access_token, scope, str(process_id))
    log_path = (
        output_dir
        / f"{props['environment']}_setup_functional_area_csv_import_{slug(offering_code)}_{slug(functional_area_code)}_{process_id}_process_log.txt"
    )
    log_path.write_bytes(raw_content)

    print(f"StatusCode: {current_status or '(unknown)'}")
    print(f"Wrote {metadata_path}")
    print(f"Wrote {log_path} ({len(raw_content)} bytes)")
    return 4 if current_status in ERROR_STATUS_CODES else 0


def main() -> int:
    args = parse_args()
    props = read_properties(Path(args.properties))
    require_props(props, ["environment", "restBaseUrl"])
    access_token = get_token(props, args)
    try:
        return run_import(props, access_token, args)
    except FusionHttpError as exc:
        if exc.status_code not in {401, 403} or args.access_token:
            raise
        print("Cached access token was rejected by Fusion. Running login flow again.", file=sys.stderr)
        access_token = get_token(props, args, force_login=True)
        return run_import(props, access_token, args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
