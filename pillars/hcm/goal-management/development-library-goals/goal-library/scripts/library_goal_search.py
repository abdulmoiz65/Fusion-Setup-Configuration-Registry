#!/usr/bin/env python3
"""Build supported findByAdvancedSearchQuery request bodies for Development Library Goals."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "goal-management-common/scripts"))
from library_goal_search_contract import build_search_payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="", help="Free-text GoalName search term.")
    parser.add_argument("--status-code", help="Optional exact library-goal status code.")
    parser.add_argument("--supported-filter-field", action="append", default=[], help="Field supported by current action metadata")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--offset", type=int, default=0)
    args = parser.parse_args()
    if args.limit <= 0 or args.offset < 0:
        parser.error("--limit must be positive and --offset must be nonnegative")
    try:
        payload = build_search_payload(query=args.query, status_code=args.status_code, limit=args.limit,
                                       offset=args.offset, supported_filter_fields=args.supported_filter_field)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
