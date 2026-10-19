"""Rebuild CPQ readiness through the existing Task Hook lifecycle.

Validate task context and rule evidence before preview and upload. This module
never grants approval; the durable CPQ guard owns approval and nonce consumption.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Mapping

try:
    import cpq_approval_contract as contract
    from cpq_execution import target_identity
except ModuleNotFoundError:
    from scripts import cpq_approval_contract as contract
    from scripts.cpq_execution import target_identity

from cpq_live_contract import CORE_ROOT

HOOK_SCRIPTS = CORE_ROOT / "data-loader" / "task-hook" / "scripts"
if str(HOOK_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(HOOK_SCRIPTS))
import task_hook  # noqa: E402

TASK_CODE = "ORA_CPQ_SETUP_ASSISTANT"
SKILL_PATH = "pillars/cx/configure-price-quote/company-profile/cpq-setup-assistant/SKILL.md"
_INPUT_KEYS = {"taskContextPath", "taskName", "sequence", "finalData", "ruleResults", "allowReadinessOverride"}
_MAX_INPUT_BYTES = 1024 * 1024


def prepare(path: Path, preflight: Mapping[str, Any]) -> dict[str, Any]:
    """Rebuild readiness through Task Hook, without creating any approval."""
    try:
        with path.open("rb") as source:
            content = source.read(_MAX_INPUT_BYTES + 1)
        if len(content) > _MAX_INPUT_BYTES:
            raise contract.ContractError("CPQ Task Hook input exceeds the supported size.")
        value = json.loads(content)
        if not isinstance(value, dict) or set(value) - _INPUT_KEYS:
            raise contract.ContractError("CPQ guard requires Task Hook preview input, not an approval envelope.")
        if value.get("allowReadinessOverride", False) is not False:
            raise contract.ContractError("CPQ stage validation cannot waive its required readiness checks.")
        result = task_hook.build_data_load_preview(value)
        plan, preview = result["taskValidation"], result["preview"]
        if (
            plan.get("taskValidationStatus") != "ready"
            or plan.get("taskCode") != TASK_CODE or preview.get("taskCode") != TASK_CODE
            or plan.get("skillPath") != SKILL_PATH
            or preview.get("executionRoute") != "data-loader"
        ):
            raise contract.ContractError("CPQ requires its exact ready Task Hook route; missing or unrelated guidance cannot authorize a stage.")
        binding = task_hook.require_runbook_binding(preview.get("runbookBinding"))
        if (
            binding["workerJourneyId"] != preflight.get("runID")
            or target_identity(binding["serverUrl"]) != target_identity(preflight.get("host"))
        ):
            raise contract.ContractError("CPQ Task Hook Run Book and target differ from the final preflight.")
        final_data = preview.get("finalData")
        if not isinstance(final_data, dict) or final_data.get("archiveSha256") != preflight.get("archiveSha256"):
            raise contract.ContractError("CPQ Task Hook evidence does not cover the final prepared archive.")
        # The recomputed timestamp is not evidence of a user decision. Bind the
        # actual validated content, including all finalData and rule results.
        preview = {key: item for key, item in preview.items() if key != "generatedAt"}
        return json.loads(contract.canonical_bytes({"preview": preview, "taskValidation": plan}))
    except (OSError, ValueError, KeyError, TypeError) as error:
        if isinstance(error, contract.ContractError):
            raise
        raise contract.ContractError("CPQ Task Hook validation failed; correct the task input and readiness evidence before approval.") from error

