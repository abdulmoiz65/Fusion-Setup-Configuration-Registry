#!/usr/bin/env python3
"""Run Shifts and Schedules through the shared Field Service workflow."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TASK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TASK_ROOT.parents[1] / "scripts"))
from task_orchestration import WorkflowBlocked, run
from task_adapter import ShiftsAndSchedulesAdapter

ROOT = Path(__file__).resolve().parents[6]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--execution-direction", choices=("data_loader_execution", "ora_rest_execution"))
    parser.add_argument("--mode", choices=("preview", "execute"), default="preview")
    parser.add_argument("--approve-checksum")
    parser.add_argument("--allow-delete", action="store_true")
    parser.add_argument("--properties", type=Path, default=ROOT / "core/auth/fusionEnv.properties")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.allow_delete:
            raise WorkflowBlocked(
                "DELETE is not available through the current shared Field Service runner; "
                "do not execute an item deletion without a runner that enforces its explicit acknowledgement gate."
            )
        result = run(
            ShiftsAndSchedulesAdapter(),
            args.workbook,
            args.execution_direction,
            args.mode,
            args.approve_checksum,
            args.properties,
            args.output,
            include_exact_preview=True,
        )
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, WorkflowBlocked) as error:
        print(f"Shifts and Schedules workflow blocked: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
