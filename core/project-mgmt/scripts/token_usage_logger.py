#!/usr/bin/env python3
"""Append default token usage estimates for project workspace updates."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


ESTIMATION_METHOD = "chars/4 estimate"
HEADER = (
    "| Activity Start Time | Skill ID | Task | Trigger | Artifacts Written | "
    "Files Read | Estimated Input Tokens | Estimated Output Tokens | "
    "Estimated Total Tokens | Estimation Method | Notes |\n"
    "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |\n"
)


def repo_root() -> Path:
    for candidate in (Path.cwd(), *Path.cwd().parents):
        if (candidate / "project").exists() and (candidate / "core").exists():
            return candidate
    return Path.cwd()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def estimate_path_tokens(path: Path) -> int:
    if not path.exists() or not path.is_file():
        return 0
    return max(1, path.stat().st_size // 4)


def token_log_path(project_id: str, root: Path | None = None) -> Path:
    base = root or repo_root()
    return (
        base
        / "project"
        / project_id
        / "artifacts"
        / "shared"
        / "token-usage"
        / "current"
        / "token-usage-log.md"
    )


def append_token_usage_log(
    *,
    project_id: str,
    skill_id: str,
    task: str,
    trigger: str,
    activity_start_time: str,
    artifact_paths: list[Path],
    files_read: int = 0,
    estimated_input_tokens: int = 0,
    estimated_output_tokens: int | None = None,
    estimation_method: str = ESTIMATION_METHOD,
    notes: str = "",
    root: Path | None = None,
) -> Path:
    """Append a repository-standard token usage row for a workspace update."""

    base = root or repo_root()
    resolved_artifacts = [path if path.is_absolute() else base / path for path in artifact_paths]
    output_tokens = (
        sum(estimate_path_tokens(path) for path in resolved_artifacts)
        if estimated_output_tokens is None
        else estimated_output_tokens
    )
    total_tokens = estimated_input_tokens + output_tokens
    relative_artifacts = [
        str(path.relative_to(base)) if path.is_absolute() and path.is_relative_to(base) else str(path)
        for path in resolved_artifacts
    ]
    artifact_note = "Artifacts: " + ", ".join(relative_artifacts) if relative_artifacts else "No artifacts listed."
    full_notes = f"{artifact_note} {notes}".strip()

    log_path = token_log_path(project_id, base)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists() or not log_path.read_text(encoding="utf-8").strip():
        log_path.write_text(HEADER, encoding="utf-8")

    row = (
        f"| {markdown_cell(activity_start_time)} | {markdown_cell(skill_id)} | "
        f"{markdown_cell(task)} | {markdown_cell(trigger)} | {len(artifact_paths)} | "
        f"{files_read} | {estimated_input_tokens} | {output_tokens} | {total_tokens} | "
        f"{markdown_cell(estimation_method)} | {markdown_cell(full_notes)} |\n"
    )
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(row)
    return log_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--skill-id", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--activity-start-time", default=utc_now())
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--files-read", type=int, default=0)
    parser.add_argument("--estimated-input-tokens", type=int, default=0)
    parser.add_argument("--estimated-output-tokens", type=int)
    parser.add_argument("--estimation-method", default=ESTIMATION_METHOD)
    parser.add_argument("--notes", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    log_path = append_token_usage_log(
        project_id=args.project_id,
        skill_id=args.skill_id,
        task=args.task,
        trigger=args.trigger,
        activity_start_time=args.activity_start_time,
        artifact_paths=[Path(path) for path in args.artifact],
        files_read=args.files_read,
        estimated_input_tokens=args.estimated_input_tokens,
        estimated_output_tokens=args.estimated_output_tokens,
        estimation_method=args.estimation_method,
        notes=args.notes,
    )
    print(f"Wrote {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
