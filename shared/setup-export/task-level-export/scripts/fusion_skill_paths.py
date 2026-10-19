"""Repository path helpers for task-level export scripts."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "core" / "auth" / "fusion-oauth-authentication").exists():
            return candidate
    raise RuntimeError("Could not locate repository root with the required layout")


REPO_ROOT = find_repo_root(Path(__file__).resolve())
FUSION_SKILLS_ROOT = REPO_ROOT
AUTH_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "core" / "auth" / "fusion-oauth-authentication" / "scripts"
FSM_CSV_EXPORT_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "shared" / "setup-export" / "fsm-csv-export" / "scripts"
PROJECT_MGMT_SCRIPTS_PATH = FUSION_SKILLS_ROOT / "core" / "project-mgmt" / "scripts"
DEFAULT_PROPERTIES_PATH = FUSION_SKILLS_ROOT / "core" / "auth" / "fusionEnv.properties"
PROJECTS_ROOT = FUSION_SKILLS_ROOT / "project"


def resolve_project_id(explicit_project_id: str | None = None) -> str:
    if explicit_project_id:
        return explicit_project_id
    env_project_id = os.environ.get("FDOS_PROJECT_ID")
    if env_project_id:
        return env_project_id

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


def project_artifacts_root(explicit_project_id: str | None = None) -> Path:
    return PROJECTS_ROOT / resolve_project_id(explicit_project_id) / "artifacts"


def project_exports_root(explicit_project_id: str | None = None) -> Path:
    return PROJECTS_ROOT / resolve_project_id(explicit_project_id) / "exports"


def add_auth_scripts_to_path() -> None:
    auth_scripts = str(AUTH_SCRIPTS_PATH)
    if auth_scripts not in sys.path:
        sys.path.insert(0, auth_scripts)


def add_fsm_csv_export_scripts_to_path() -> None:
    fsm_scripts = str(FSM_CSV_EXPORT_SCRIPTS_PATH)
    if fsm_scripts not in sys.path:
        sys.path.insert(0, fsm_scripts)


def add_project_mgmt_scripts_to_path() -> None:
    project_mgmt_scripts = str(PROJECT_MGMT_SCRIPTS_PATH)
    if project_mgmt_scripts not in sys.path:
        sys.path.insert(0, project_mgmt_scripts)
