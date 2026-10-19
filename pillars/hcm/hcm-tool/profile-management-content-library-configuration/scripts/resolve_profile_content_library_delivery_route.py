#!/usr/bin/env python3
"""Classify technical XLSX, FSM, or explicit DAT delivery before file creation."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from typing import Iterable, Sequence


SCHEMA_VERSION = "1.0"
MAX_WORKSHEET_PREFIX = 30


class DeliveryRouteError(ValueError):
    """Fail-closed delivery-route input error."""


def _clean(values: Iterable[str], label: str) -> tuple[str, ...]:
    result = []
    seen = set()
    for raw in values:
        if not isinstance(raw, str) or not raw.strip() or raw != raw.strip():
            raise DeliveryRouteError(f"{label} values must be nonblank trimmed strings")
        if any(ord(character) < 32 for character in raw):
            raise DeliveryRouteError(f"{label} values contain unsupported characters")
        if raw not in seen:
            seen.add(raw)
            result.append(raw)
    if not result:
        raise DeliveryRouteError(f"at least one {label} value is required")
    return tuple(result)


def classify_delivery_route(
    discriminators: Iterable[str],
    *,
    root_prefix: str | None = None,
    root_candidates: Iterable[str] = (),
    fsm_route_valid: bool = False,
    fsm_task_code: str | None = None,
    explicit_dat_request: bool = False,
) -> dict:
    """Return a deterministic pre-generation route decision without writing a file."""

    sections = _clean(discriminators, "discriminator")
    prefix_rows = [
        {"discriminator": value, "prefix": value[:MAX_WORKSHEET_PREFIX]}
        for value in sections
    ]
    by_prefix: dict[str, list[str]] = defaultdict(list)
    for row in prefix_rows:
        by_prefix[row["prefix"].casefold()].append(row["discriminator"])
    collisions = [
        {
            "kind": "worksheet-prefix",
            "prefix": next(row["prefix"] for row in prefix_rows if row["prefix"].casefold() == folded),
            "candidates": sorted(candidates),
        }
        for folded, candidates in sorted(by_prefix.items())
        if len(candidates) > 1
    ]

    roots = tuple(root_candidates)
    if root_prefix is not None:
        if not root_prefix or root_prefix != root_prefix.strip():
            raise DeliveryRouteError("root_prefix must be a nonblank trimmed string")
        cleaned_roots = _clean(roots, "root candidate") if roots else ()
        folded_root = root_prefix.casefold()
        matches = [
            value for value in cleaned_roots if value.casefold().startswith(folded_root)
        ]
        if len(matches) > 1:
            collisions.append(
                {
                    "kind": "root-prefix",
                    "prefix": root_prefix,
                    "candidates": sorted(matches),
                }
            )

    collision_detected = bool(collisions)
    if not fsm_route_valid and fsm_task_code is not None:
        raise DeliveryRouteError("fsm_task_code requires a valid FSM route")
    if explicit_dat_request:
        status = "selected"
        selected_route = "dat-preparation"
        next_action = "Prepare a review-only DAT artifact; a separate immutable preview and execution approval are still required."
    elif collision_detected and fsm_route_valid:
        if not fsm_task_code or not fsm_task_code.strip():
            raise DeliveryRouteError("a valid FSM route requires fsm_task_code")
        status = "selected"
        selected_route = "fsm"
        next_action = "Prepare the task-local FSM route after its separate evidence and package gates pass."
    elif collision_detected:
        status = "blocked"
        selected_route = "none"
        next_action = "Explicitly request DAT preparation for the resolved business object; this does not approve import."
    else:
        status = "eligible"
        selected_route = "technical-xlsx"
        next_action = "Continue to populated technical workbook preparation after later implementation-validation gates pass."

    return {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "collision_detected": collision_detected,
        "generated_prefixes": prefix_rows,
        "collisions": collisions,
        "selected_route": selected_route,
        "explicit_dat_request": explicit_dat_request,
        "workbook_created": False,
        "fsm_task_code": fsm_task_code if fsm_route_valid else None,
        "next_action": next_action,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--discriminator", action="append", required=True)
    parser.add_argument("--root-prefix")
    parser.add_argument("--root-candidate", action="append", default=[])
    parser.add_argument("--fsm-route-valid", action="store_true")
    parser.add_argument("--fsm-task-code")
    parser.add_argument("--prepare-dat", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = classify_delivery_route(
            args.discriminator,
            root_prefix=args.root_prefix,
            root_candidates=args.root_candidate,
            fsm_route_valid=args.fsm_route_valid,
            fsm_task_code=args.fsm_task_code,
            explicit_dat_request=args.prepare_dat,
        )
    except DeliveryRouteError as error:
        print(json.dumps({"status": "blocked", "message": str(error)}, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
