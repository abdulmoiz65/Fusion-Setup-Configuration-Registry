"""Repository path helpers for task-level import scripts."""

from __future__ import annotations

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
DEFAULT_PROPERTIES_PATH = FUSION_SKILLS_ROOT / "core" / "auth" / "fusionEnv.properties"


def add_auth_scripts_to_path() -> None:
    auth_scripts = str(AUTH_SCRIPTS_PATH)
    if auth_scripts not in sys.path:
        sys.path.insert(0, auth_scripts)
