#!/usr/bin/env python3
"""Persist one Product Management index execution continuation state."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile
from uuid import uuid4


REPOSITORY_ROOT = Path(__file__).resolve().parents[6]
PROJECTS_ROOT = REPOSITORY_ROOT / "project"
STATE_RELATIVE_PATH = Path(
    "artifacts/pillars/scm/product-management/index-management/"
    "manage-product-management-indexes/current/index-execution-state.json"
)

STATES = frozenset(
    {
        "data_load_submitted",
        "data_load_pending",
        "data_load_succeeded",
        "readback_verified",
        "ess_approval_pending",
        "ess_submitted",
        "ess_skipped",
        "blocked",
    }
)

TRANSITIONS = {
    None: {"data_load_submitted", "ess_approval_pending", "blocked"},
    "data_load_submitted": {"data_load_pending", "data_load_succeeded", "blocked"},
    "data_load_pending": {"data_load_pending", "data_load_succeeded", "blocked"},
    "data_load_succeeded": {"readback_verified", "blocked"},
    "readback_verified": {"ess_approval_pending", "blocked"},
    "ess_approval_pending": {"ess_submitted", "ess_skipped", "blocked"},
    "ess_submitted": set(),
    "ess_skipped": set(),
    "blocked": set(),
}
TERMINAL_STATES = frozenset({"ess_submitted", "ess_skipped", "blocked"})


class StateError(ValueError):
    """Raised when an execution state or transition is unsafe."""


class ArtifactPersistenceError(RuntimeError):
    """Raised when durable state cannot be safely persisted."""


def _nonblank(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise StateError(f"{field} must be one nonblank string.")
    return value.strip()


def _request_id(value: object) -> str:
    text = _nonblank(value, "data_loader_request_id")
    if not text.isdecimal() or int(text) <= 0:
        raise StateError("data_loader_request_id must be a positive integer.")
    return text


def _load(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ArtifactPersistenceError("unable to read index execution state") from error
    if not isinstance(value, dict) or value.get("schema_version") != "1.0":
        raise StateError("index execution state must be a schema_version 1.0 object.")
    state = value.get("state")
    if state not in STATES:
        raise StateError("index execution state has an unsupported state.")
    _nonblank(value.get("canonical_index_name"), "canonical_index_name")
    return value


def state_path_for_project(project_root: Path) -> Path:
    """Return the sole registered continuation-state path for one project."""
    try:
        root = project_root.resolve()
        if root.parent != PROJECTS_ROOT.resolve() or not root.name:
            raise StateError("project_root must be an existing project/{project_id} workspace.")
        if not root.is_dir():
            raise StateError("project_root must be an existing directory.")

        current = root
        for component in STATE_RELATIVE_PATH.parts[:-1]:
            current = current / component
            if current.exists():
                if current.is_symlink() or not current.is_dir():
                    raise ArtifactPersistenceError("index execution state directory is unsafe")
            else:
                current.mkdir()
            if not current.resolve().is_relative_to(root):
                raise ArtifactPersistenceError(
                    "index execution state directory is outside the project workspace"
                )

        target = current / STATE_RELATIVE_PATH.name
        if target.is_symlink() or not target.parent.resolve().is_relative_to(root):
            raise ArtifactPersistenceError("index execution state path is unsafe")
        return target
    except OSError as error:
        raise ArtifactPersistenceError("unable to prepare index execution state path") from error


def transition(
    current: dict[str, object] | None,
    *,
    event: str,
    canonical_index_name: str | None,
    data_loader_request_id: str | None,
    artifact_refs: list[str],
) -> dict[str, object]:
    if event not in STATES:
        raise StateError("event must name a supported execution state.")
    previous = current.get("state") if current else None
    if event not in TRANSITIONS[previous]:
        raise StateError(f"Cannot transition from {previous or 'new'} to {event}.")

    canonical = (
        _nonblank(canonical_index_name, "canonical_index_name")
        if canonical_index_name is not None
        else _nonblank(current.get("canonical_index_name") if current else None, "canonical_index_name")
    )
    if current is not None and canonical != current["canonical_index_name"]:
        raise StateError("canonical_index_name cannot change during an invocation.")
    request_id = data_loader_request_id or (current or {}).get("data_loader_request_id")
    if event in {"data_load_submitted", "data_load_pending", "data_load_succeeded", "readback_verified"}:
        request_id = _request_id(request_id)
    elif request_id is not None:
        request_id = _request_id(request_id)
    if current is not None and request_id != current.get("data_loader_request_id"):
        raise StateError("data_loader_request_id cannot change during an invocation.")

    refs = list((current or {}).get("artifact_refs") or [])
    for ref in artifact_refs:
        if not isinstance(ref, str) or not ref.strip():
            raise StateError("artifact references must be nonblank strings.")
        if ref not in refs:
            refs.append(ref)
    return {
        "schema_version": "1.0",
        "canonical_index_name": canonical,
        "state": event,
        "data_loader_request_id": request_id,
        "artifact_refs": refs,
        "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def _write(path: Path, state: dict[str, object]) -> None:
    temporary: Path | None = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as handle:
            json.dump(state, handle, indent=2, sort_keys=True)
            handle.write("\n")
            temporary = Path(handle.name)
        temporary.replace(path)
    except OSError as error:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
        raise ArtifactPersistenceError("unable to persist index execution state") from error


def _archive_terminal(path: Path, current: dict[str, object]) -> Path:
    """Move a terminal invocation into history before starting another one."""
    if current["state"] not in TERMINAL_STATES:
        raise StateError("A new invocation requires a terminal prior state.")
    history = path.parent / "history"
    try:
        if history.is_symlink():
            raise ArtifactPersistenceError("index execution history path is unsafe")
        history.mkdir(exist_ok=True)
        if not history.is_dir() or not history.resolve().is_relative_to(path.parent.resolve()):
            raise ArtifactPersistenceError("index execution history path is unsafe")
        archived = history / f"index-execution-state-{uuid4().hex}.json"
        path.replace(archived)
        return archived
    except OSError as error:
        raise ArtifactPersistenceError("unable to archive index execution state") from error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        required=True,
        type=Path,
        help="Existing project/{project_id} workspace; the state path is derived from it.",
    )
    parser.add_argument("--event", required=True, choices=sorted(STATES))
    parser.add_argument("--canonical-index-name")
    parser.add_argument("--data-loader-request-id")
    parser.add_argument("--artifact-ref", action="append", default=[])
    parser.add_argument(
        "--start-new",
        action="store_true",
        help="Archive a terminal prior invocation and start a separately requested index.",
    )
    args = parser.parse_args(argv)
    try:
        state_path = state_path_for_project(args.project_root)
        current = _load(state_path)
        if args.start_new and args.event not in TRANSITIONS[None]:
            raise StateError("--start-new requires an initial invocation event.")
        if args.start_new and current is None:
            raise StateError("--start-new requires a terminal prior invocation.")
        result = transition(
            None if args.start_new else current,
            event=args.event,
            canonical_index_name=args.canonical_index_name,
            data_loader_request_id=args.data_loader_request_id,
            artifact_refs=args.artifact_ref,
        )
        archived = _archive_terminal(state_path, current) if args.start_new else None
        try:
            _write(state_path, result)
        except ArtifactPersistenceError:
            if archived is not None:
                try:
                    archived.replace(state_path)
                except OSError:
                    pass
            raise
    except StateError as error:
        parser.error(str(error))
    except ArtifactPersistenceError:
        print(
            json.dumps(
                {
                    "status": "failed",
                    "failure_class": "artifact_persistence",
                    "message": "Unable to persist index execution state.",
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
