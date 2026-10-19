#!/usr/bin/env python3
"""Create the Field Service task-owned Data Loader Run Book context."""

import argparse
import json
import os
from pathlib import Path
import tempfile
from typing import Any


TASK_PATH = Path(
    "artifacts/pillars/cx/field-service/users-and-security/"
    "manage-hcm-role-provisioning-rules/current/data-loader-run-context.properties"
)
RUNBOOK_RESPONSE_PATH = Path("state/runbook/current/create-runbook-response.json")


def positive_worker_journey_id(value: Any) -> str:
    """Return a valid Fusion WorkerJourneyId without exposing it in output."""

    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError("Run Book response has no valid workerJourneyId.")
    normalized = str(value).strip()
    if not normalized.isdecimal() or int(normalized) < 1:
        raise ValueError("Run Book response has no valid workerJourneyId.")
    return normalized


def read_worker_journey_id(response_path: Path) -> str:
    """Read the sole Run Book identifier required by Data Loader."""

    try:
        response = json.loads(response_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("Run Book response artifact is unavailable or invalid.") from error
    if not isinstance(response, dict):
        raise ValueError("Run Book response artifact must be a JSON object.")
    return positive_worker_journey_id(response.get("workerJourneyId"))


def write_run_context(output_path: Path, worker_journey_id: str) -> None:
    """Atomically write a minimal, project-owned runID context."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=output_path.parent,
        prefix=f".{output_path.name}.",
        suffix=".tmp",
        delete=False,
    ) as temporary:
        temporary.write(f"runID={worker_journey_id}\n")
        temporary.flush()
        os.fsync(temporary.fileno())
        temporary_path = Path(temporary.name)
    os.chmod(temporary_path, 0o600)
    os.replace(temporary_path, output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare the task-owned Data Loader Run Book context."
    )
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--runbook-response", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        project_root = args.project_root.resolve(strict=True)
    except OSError as error:
        raise ValueError("Project root must be an existing directory.") from error
    if not project_root.is_dir():
        raise ValueError("Project root must be an existing directory.")
    response_path = (
        args.runbook_response.resolve(strict=True)
        if args.runbook_response is not None
        else project_root / RUNBOOK_RESPONSE_PATH
    )
    output_path = (
        args.output.resolve()
        if args.output is not None
        else project_root / TASK_PATH
    )
    try:
        output_path.relative_to(project_root)
    except ValueError as error:
        raise ValueError("Data Loader run context must remain inside the project.") from error
    write_run_context(output_path, read_worker_journey_id(response_path))
    print(json.dumps({"prepared": True, "run_context": str(output_path)}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(json.dumps({"prepared": False, "error": str(error)}))
        raise SystemExit(2)
