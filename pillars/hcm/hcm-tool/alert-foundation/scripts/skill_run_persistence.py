"""Persist Alert Foundation skill-run records without overwriting evidence."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_PATH = Path(__file__).resolve().parents[5] / "schemas" / "skill-run.schema.json"
FORBIDDEN_LITERAL_KEYS = frozenset({"", "$schema", "external_ids"})


class SkillRunPersistenceError(ValueError):
    """Raised when a skill-run record is unsafe or fails its schema contract."""


def _reject_forbidden_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise SkillRunPersistenceError("Skill-run record keys must be strings.")
            if key in FORBIDDEN_LITERAL_KEYS:
                raise SkillRunPersistenceError(f"Unsupported literal key: {key!r}")
            _reject_forbidden_keys(child)
    elif isinstance(value, list):
        for child in value:
            _reject_forbidden_keys(child)


def _schema_validator() -> Draft202012Validator:
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SkillRunPersistenceError("Unable to load the skill-run schema.") from exc
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_skill_run(record: dict[str, Any]) -> None:
    """Reject unsafe or nonconforming records before any filesystem mutation."""
    if not isinstance(record, dict):
        raise SkillRunPersistenceError("Skill-run record must be a JSON object.")
    _reject_forbidden_keys(record)
    if "token_usage" not in record:
        raise SkillRunPersistenceError("Skill-run record must contain token_usage.")
    errors = sorted(_schema_validator().iter_errors(record), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "root"
        raise SkillRunPersistenceError(f"Skill-run schema validation failed at {location}: {first.message}")


def serialize_skill_run(record: dict[str, Any]) -> bytes:
    """Return deterministic, strict JSON only after schema validation."""
    validate_skill_run(record)
    try:
        return (json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise SkillRunPersistenceError("Skill-run record is not safely JSON serializable.") from exc


def write_skill_run(record: dict[str, Any], destination: Path) -> Path:
    """Atomically publish a new record and refuse any existing destination."""
    rendered = serialize_skill_run(record)
    target = Path(destination)
    if target.exists():
        raise FileExistsError(f"Skill-run record already exists: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=target.parent, prefix=f".{target.name}.", delete=False) as stream:
            temp_path = Path(stream.name)
            stream.write(rendered)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temp_path, target)
        except FileExistsError as exc:
            raise FileExistsError(f"Skill-run record already exists: {target}") from exc
        return target
    finally:
        if temp_path is not None:
            try:
                temp_path.unlink()
            except FileNotFoundError:
                pass


def main(argv: list[str] | None = None) -> int:
    """Persist one stdin record without exposing its content on stdout or stderr."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-stdin", action="store_true", required=True,
                        help="Read one JSON skill-run record from standard input.")
    parser.add_argument("--output", required=True, help="New destination for the run record.")
    args = parser.parse_args(argv)
    try:
        record = json.load(sys.stdin)
        write_skill_run(record, Path(args.output))
    except json.JSONDecodeError:
        print(json.dumps({"status": "validation_failed", "failure_class": "input_validation"}))
        return 2
    except SkillRunPersistenceError:
        print(json.dumps({"status": "validation_failed", "failure_class": "input_validation"}))
        return 2
    except OSError as exc:
        print(json.dumps({"status": "failed", "failure_class": "artifact_persistence",
                          "error_type": type(exc).__name__}))
        return 3
    print(json.dumps({"status": "persisted"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
