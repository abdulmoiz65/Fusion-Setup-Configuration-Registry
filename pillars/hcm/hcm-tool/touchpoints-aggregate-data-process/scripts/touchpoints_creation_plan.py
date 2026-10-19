"""Bind owner task types to an exact canonical Run Book creation plan, offline.

Shared catalog resolution still owns identities. This scoped adapter prevents a
REST-only owner task from receiving the shared generator's Data Loader default.
It neither invents task codes nor changes the core Run Book client.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
import json
from pathlib import Path


def adapt_creation_plan(configuration, canonical):
    requested = configuration.get("creation_tasks")
    if not isinstance(requested, list) or not requested:
        raise ValueError("Selected scope has no catalog-backed initial task; manual-only creation needs a core workflow capability, never an unrelated ESS seed")
    tasks = canonical.get("tasks")
    if not isinstance(tasks, list) or len(tasks) != len(requested):
        raise ValueError("Canonical creation plan must contain exactly the selected catalog-backed tasks")
    result = deepcopy(canonical)
    ordered = []
    for request in requested:
        expected_type = {"rest": "ORA_CHK_MANUAL", "profile-provider": "ORA_CHK_MANUAL", "data-loader": "ORA_CHK_DATA_LOADER",
                         "ess": "ORA_CHK_DATA_LOADER"}.get(request.get("execution_route"))
        if expected_type is None or request.get("task_type") != expected_type:
            raise ValueError("Creation task type must match its declared owner execution route")
        identity = request["catalog_identity"]
        matches = [row for row in result["tasks"] if row.get("task_id") == identity["task_code"]
                   and row.get("name") == identity["task_name"]
                   and row.get("offering") == identity["offering"]
                   and row.get("functional_area") == identity["functional_area"]]
        if len(matches) != 1:
            raise ValueError("Selected owner task must match exactly one canonical task")
        row = matches[0]
        row["taskType"] = expected_type
        row["sequence"] = request["sequence"]
        if request["execution_route"] in ("rest", "profile-provider"):
            row["business_objects"] = []
        ordered.append(row)
    result["tasks"] = ordered
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--configuration-plan", type=Path, required=True)
    parser.add_argument("--canonical-plan", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true", required=True)
    args = parser.parse_args()
    result = adapt_creation_plan(json.loads(args.configuration_plan.read_text()), json.loads(args.canonical_plan.read_text()))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
