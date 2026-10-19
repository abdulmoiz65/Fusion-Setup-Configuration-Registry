#!/usr/bin/env python3
"""Standalone Task Validator entry point for Data Loader task-routed imports."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, IO, Sequence

from task_rule_execution import (
    TaskRuleContractError,
    approve_task_preview,
    approved_loader_payload,
    build_task_preview,
    resolve_task_rules_from_context,
)


SKILL_ROOT = Path(__file__).resolve().parent.parent
REPOSITORY_ROOT = SKILL_ROOT.parents[2]


def _positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a positive integer") from error
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def _read_json_object(stream: IO[str], description: str) -> dict[str, Any]:
    try:
        value = json.load(stream)
    except json.JSONDecodeError as error:
        raise TaskRuleContractError(f"{description} is not valid JSON: {error.msg}.") from error
    if not isinstance(value, dict):
        raise TaskRuleContractError(f"{description} must be a JSON object.")
    return value


def _read_override(value: dict[str, Any]) -> bool:
    override = value.get("allowReadinessOverride", False)
    if not isinstance(override, bool):
        raise TaskRuleContractError(
            "allowReadinessOverride must be a JSON boolean when supplied."
        )
    return override


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as source:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as error:
        raise TaskRuleContractError(f"Prepared archive could not be read: {path}") from error
    return digest.hexdigest()


def _approved_archive_payload(envelope: dict[str, Any], archive_sha256: str) -> dict[str, Any]:
    payload = approved_loader_payload(envelope.get("preview"), envelope.get("approval"))
    final_data = payload.get("finalData")
    if not isinstance(final_data, dict):
        raise TaskRuleContractError("Approved task payload finalData must be a JSON object.")
    expected = final_data.get("archiveSha256")
    if not isinstance(expected, str) or not expected.strip():
        raise TaskRuleContractError("Approved task payload must include finalData.archiveSha256.")
    if expected.casefold() != archive_sha256.casefold():
        raise TaskRuleContractError("Approved task payload does not match the prepared archive SHA-256.")
    return payload


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve-task-rules", allow_abbrev=False)
    resolve.add_argument("--task-context", required=True, type=Path)
    resolve.add_argument("--task-name", required=True)
    resolve.add_argument("--sequence", required=True, type=_positive_int)
    resolve.add_argument("--allow-readiness-override", action="store_true")

    for name, help_text in (
        ("build-task-preview", "Build a Data Loader task-validation preview."),
        ("approve-task-preview", "Record approval of a Task Validator preview."),
        ("approved-loader-payload", "Return the approved Data Loader payload."),
    ):
        command = commands.add_parser(name, help=help_text, allow_abbrev=False)
        command.add_argument("--input-stdin", required=True, action="store_true")

    verify = commands.add_parser("verify-approved-archive", allow_abbrev=False)
    verify.add_argument("--input-stdin", required=True, action="store_true")
    verify.add_argument("--archive", required=True, type=Path)
    return parser.parse_args(argv)


def main(
    argv: Sequence[str] | None = None,
    *,
    stdin: IO[str] = sys.stdin,
    stdout: IO[str] = sys.stdout,
    stderr: IO[str] = sys.stderr,
) -> int:
    args = parse_args(argv)
    try:
        if args.command == "resolve-task-rules":
            result = resolve_task_rules_from_context(
                repository_root=REPOSITORY_ROOT,
                task_context_path=args.task_context,
                task_name=args.task_name,
                sequence=args.sequence,
                allow_readiness_override=args.allow_readiness_override,
            )
        elif args.command == "build-task-preview":
            envelope = _read_json_object(stdin, "Task preview input")
            context_path = envelope.get("taskContextPath")
            sequence = envelope.get("sequence")
            override = _read_override(envelope)
            if not isinstance(context_path, str) or not context_path.strip():
                raise TaskRuleContractError("Task preview input requires taskContextPath.")
            if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 1:
                raise TaskRuleContractError("Task preview input requires a positive integer sequence.")
            plan = resolve_task_rules_from_context(
                repository_root=REPOSITORY_ROOT,
                task_context_path=Path(context_path),
                task_name=envelope.get("taskName"),
                sequence=sequence,
                allow_readiness_override=override,
            )
            result = build_task_preview(
                repository_root=REPOSITORY_ROOT,
                skill_path=plan["skillPath"],
                task_name=plan["taskName"],
                final_data=envelope.get("finalData"),
                rule_results=envelope.get("ruleResults"),
                allow_readiness_override=override,
                task_code=plan["taskCode"],
            )
        elif args.command == "approve-task-preview":
            result = approve_task_preview(_read_json_object(stdin, "Task approval input").get("preview"))
        elif args.command == "approved-loader-payload":
            envelope = _read_json_object(stdin, "Approved loader input")
            result = approved_loader_payload(envelope.get("preview"), envelope.get("approval"))
        else:
            result = _approved_archive_payload(
                _read_json_object(stdin, "Approved archive input"), _sha256_file(args.archive)
            )
        json.dump(result, stdout, ensure_ascii=False)
        stdout.write("\n")
        return 0
    except (TaskRuleContractError, OSError, ValueError) as error:
        print(str(error), file=stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
