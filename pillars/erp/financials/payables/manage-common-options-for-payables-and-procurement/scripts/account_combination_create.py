#!/usr/bin/env python3
"""Preview or execute one context-approved GL combination through core HTTP."""
from __future__ import annotations

import argparse
from functools import partial
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from account_combination_preflight import (  # noqa: E402
    DEFAULT_PROPERTIES_PATH, PreflightError, SERVICE_PATH, WORKFLOW,
    VALIDATE_SOAP_ACTION, build_envelope, response_summary,
)


class CreationError(RuntimeError):
    """An account-combination business validation failure."""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--ledger-name", required=True)
    parser.add_argument("--segments", required=True, help="One through 30 hyphen-delimited values.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preview-output", type=Path, help="New local request preview; no authentication or network calls.")
    mode.add_argument("--approval-file", type=Path, help="Workflow approval JSON bound to the complete preview request.")
    parser.add_argument("--properties", type=Path, default=DEFAULT_PROPERTIES_PATH)
    parser.add_argument("--output", type=Path, help="New execution receipt; required with --approval-file.")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--callback-timeout", type=int, default=60)
    parser.add_argument("--token-cache")
    parser.add_argument("--force-login", action="store_true")
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser", default=True)
    args = parser.parse_args(argv)
    if args.approval_file and args.output is None:
        raise CreationError("--approval-file requires --output for a new execution receipt.")
    if args.preview_output and args.output is not None:
        raise CreationError("Use --preview-output alone for local preparation.")

    segments = args.segments.split("-")
    envelope = build_envelope(ledger_name=args.ledger_name, segments=segments, dynamic_insertion="Yes")
    props = WORKFLOW.load_environment(args.properties)
    business = {"ledgerName": args.ledger_name.strip(), "segments": segments, "dynamicInsertion": "Yes"}
    inputs = [args.properties]
    inputs.append(WORKFLOW.token_cache_path(props, args.token_cache))
    if args.preview_output:
        request = WORKFLOW.request_context(props, endpoint=SERVICE_PATH, soap_action=VALIDATE_SOAP_ACTION,
                                       operation="validateAndCreateAccounts", envelope=envelope,
                                       read_only=False, business_context=business)
        WORKFLOW.write_new_json(args.preview_output, {"schemaVersion": "fscr-soap-preview-v1", "request": request},
                            protected_inputs=inputs)
        print(f"Wrote local creation preview to {args.preview_output}; no request submitted.")
        return 0

    try:
        approval = json.loads(args.approval_file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise WORKFLOW.AccountCombinationError("approval_blocker", "Cannot read a valid workflow approval record.") from exc
    inputs.append(args.approval_file)
    receipt = WORKFLOW.execute(
        props, endpoint=SERVICE_PATH, soap_action=VALIDATE_SOAP_ACTION,
        operation="validateAndCreateAccounts", envelope=envelope, read_only=False,
        business_context=business,
        summarize=partial(response_summary, read_only=False, dynamic_insertion="Yes"),
        output=args.output, approval=approval, protected_inputs=inputs,
        token_cache=args.token_cache, force_login=args.force_login, open_browser=args.open_browser,
        timeout=args.timeout, callback_timeout=args.callback_timeout,
    )
    print(f"HTTP {receipt['httpStatus']}; wrote creation receipt to {args.output}")
    if not receipt["valid"]:
        raise CreationError("Fusion did not return a valid account combination; retain the receipt and reconcile before another approved attempt.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except WORKFLOW.AccountCombinationError as exc:
        print(f"Error [{exc.failure_class}]; mayHaveApplied={exc.may_have_applied}: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except (CreationError, PreflightError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
