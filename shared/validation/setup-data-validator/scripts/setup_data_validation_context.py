"""Resolve setup-data validation context from pillar skill metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "core" / "auth" / "fusion-oauth-authentication").exists():
            return candidate
    raise RuntimeError("Could not locate repository root with the required layout")


REPO_ROOT = find_repo_root(Path(__file__).resolve())
FUSION_SKILLS_ROOT = REPO_ROOT
FSM_EXPORT_SCRIPTS = FUSION_SKILLS_ROOT / "shared" / "setup-export" / "fsm-csv-export" / "scripts"
if str(FSM_EXPORT_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(FSM_EXPORT_SCRIPTS))

from fusion_skill_paths import project_artifacts_root  # noqa: E402
from pillar_skill_metadata import (  # noqa: E402
    PillarSkillMetadata,
    kebab_case,
    parent_skill_chain,
    repo_relative,
    resolve_task_skill_metadata,
)


GUIDANCE_PATTERNS = ("ora_*.md", "ora-*.md")


def metadata_to_dict(metadata: PillarSkillMetadata | None) -> dict[str, str] | None:
    if metadata is None:
        return None
    return {
        "path": repo_relative(metadata.path),
        "skill_id": metadata.skill_id,
        "offering": metadata.offering,
        "functional_area": metadata.functional_area,
        "functional_area_code": metadata.functional_area_code,
        "task_code": metadata.task_code,
        "task_name": metadata.task_name,
    }


def first_heading(content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return ""


def find_task_guidance_files(task_metadata: PillarSkillMetadata) -> list[Path]:
    task_dir = task_metadata.path.parent
    matches: dict[Path, Path] = {}
    for pattern in GUIDANCE_PATTERNS:
        for path in task_dir.glob(pattern):
            if path.is_file():
                matches[path.resolve()] = path
    return sorted(matches.values(), key=lambda item: item.name.casefold())


def load_task_guidance(task_metadata: PillarSkillMetadata, *, include_content: bool = False) -> list[dict[str, str]]:
    guidance: list[dict[str, str]] = []
    for path in find_task_guidance_files(task_metadata):
        content = path.read_text(encoding="utf-8")
        item = {
            "path": repo_relative(path),
            "file_name": path.name,
            "title": first_heading(content),
        }
        if include_content:
            item["content"] = content
        guidance.append(item)
    return guidance


def build_validation_context(
    *,
    task_code: str | None = None,
    task_name: str | None = None,
    offering: str | None = None,
    functional_area: str | None = None,
    functional_area_code: str | None = None,
    project_id: str | None = None,
    include_guidance_content: bool = False,
) -> dict[str, Any]:
    task_metadata = resolve_task_skill_metadata(
        task_code=task_code,
        task_name=task_name,
        offering=offering,
        functional_area=functional_area,
        functional_area_code=functional_area_code,
    )
    if task_metadata is None:
        return {
            "resolved": False,
            "fallback_to_oracle_docs_required": True,
            "error": "No matching pillar setup-task metadata was found.",
            "requested": {
                "task_code": task_code or "",
                "task_name": task_name or "",
                "offering": offering or "",
                "functional_area": functional_area or "",
                "functional_area_code": functional_area_code or "",
            },
        }

    skill_chain = parent_skill_chain(task_metadata)
    guidance_files = load_task_guidance(task_metadata, include_content=include_guidance_content)
    task_slug = kebab_case(task_metadata.task_name or task_metadata.task_code)
    output_dir = (
        project_artifacts_root(project_id)
        / "shared"
        / "validation"
        / "setup-data-validator"
        / task_slug
        / "current"
    )

    return {
        "resolved": True,
        "fallback_to_oracle_docs_required": not guidance_files,
        "validation_output_dir": repo_relative(output_dir),
        "metadata": metadata_to_dict(task_metadata),
        "skill_chain": {
            "offering": metadata_to_dict(skill_chain["offering"]),
            "functional_area": metadata_to_dict(skill_chain["functional_area"]),
            "task": metadata_to_dict(skill_chain["task"]),
        },
        "guidance_files": guidance_files,
    }


def print_summary(context: dict[str, Any]) -> None:
    if not context["resolved"]:
        print(context["error"])
        print("Fallback to Oracle documentation references is required.")
        return

    metadata = context["metadata"]
    print(f"Task: {metadata['task_name']} ({metadata['task_code']})")
    print(f"Offering: {metadata['offering']}")
    print(f"Functional area: {metadata['functional_area']} ({metadata['functional_area_code']})")
    print(f"Task metadata: {metadata['path']}")
    print(f"Validation output: {context['validation_output_dir']}")
    print(f"Task-local guidance files: {len(context['guidance_files'])}")
    for item in context["guidance_files"]:
        title = f" - {item['title']}" if item["title"] else ""
        print(f"- {item['path']}{title}")
    if context["fallback_to_oracle_docs_required"]:
        print("Fallback to Oracle documentation references is required.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-code")
    parser.add_argument("--task-name")
    parser.add_argument("--offering")
    parser.add_argument("--functional-area")
    parser.add_argument("--functional-area-code")
    parser.add_argument("--project-id")
    parser.add_argument("--include-guidance-content", action="store_true")
    parser.add_argument("--json", action="store_true", help="Print validation context as JSON.")
    args = parser.parse_args()

    context = build_validation_context(
        task_code=args.task_code,
        task_name=args.task_name,
        offering=args.offering,
        functional_area=args.functional_area,
        functional_area_code=args.functional_area_code,
        project_id=args.project_id,
        include_guidance_content=args.include_guidance_content,
    )

    if args.json:
        print(json.dumps(context, indent=2))
    else:
        print_summary(context)


if __name__ == "__main__":
    main()
