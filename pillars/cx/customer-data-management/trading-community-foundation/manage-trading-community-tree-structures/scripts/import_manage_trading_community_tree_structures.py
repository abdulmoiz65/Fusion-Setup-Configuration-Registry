#!/usr/bin/env python3
"""Import the fixed Manage Trading Community Tree Structures FSM package after approval."""

from __future__ import annotations

import importlib.util
from pathlib import Path


TASK_CODE = "ORA_HZ_MANAGE_TREE_STRUCTURES"
TASK_NAME = "Manage Trading Community Tree Structures"
EXECUTION_ADAPTER = (
    "cx.customer-data-management.trading-community-foundation."
    "manage-trading-community-tree-structures.native-fsm-import"
)


def _shared_adapter():
    source = Path(__file__).resolve().parents[2] / "manage-additional-identifier-types" / "scripts" / "import_manage_additional_identifier_types.py"
    specification = importlib.util.spec_from_file_location("additional_identifier_adapter", source)
    if specification is None or specification.loader is None:
        raise RuntimeError("The shared native FSM adapter could not be loaded.")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    module.TASK_CODE = TASK_CODE
    module.TASK_NAME = TASK_NAME
    module.EXECUTION_ADAPTER = EXECUTION_ADAPTER
    module.CREATE_RESOURCE = f"{module.engine.SETUP_TASK_CSV_IMPORTS_RESOURCE}/{TASK_CODE}/child/SetupTaskCSVImportProcess"
    return module


_adapter = _shared_adapter()
validate_fsm_archive = _adapter.validate_fsm_archive
load_approved_final_data = _adapter.load_approved_final_data
main = _adapter.main


if __name__ == "__main__":
    raise SystemExit(main())
