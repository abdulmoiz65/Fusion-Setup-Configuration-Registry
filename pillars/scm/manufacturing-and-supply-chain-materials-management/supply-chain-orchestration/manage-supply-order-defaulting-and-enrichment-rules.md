---
task_code: "ORA_DOS_MANAGE_SUPPLY_ORDER_DEFAULTING_AND_ENRICHMENT_RULES"
task_name: "Manage Supply Order Defaulting and Enrichment Rules"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-orchestration"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Supply Chain Orchestration"
functional_area_code: "ORA_DOS_SUPPLY_CHAIN_ORCH"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Supply Order Defaulting and Enrichment Rules

- **Task code:** `ORA_DOS_MANAGE_SUPPLY_ORDER_DEFAULTING_AND_ENRICHMENT_RULES`
- **Purpose:** Define when eligible transfer orders pass through Oracle Order Management.
- **Execution rule:** The user completes the approved change manually on the Manage Supply Order Defaulting and Enrichment Rules page in Oracle Fusion Setup and Maintenance; no API, import, automated configuration, or browser automation.

Use the standard manual workflow in [SKILL.md](../../../../shared/common/manual-tasks/SKILL.md).

Provide manual steps directly from this task using the user’s supplied values. Stay within the documented guidance, identify missing details, and do not create separate guides or project artifacts solely to explain the steps.

## Manual Steps

1. Confirm your target environment and release, approved rule name, condition attributes/operators/values, desired action, and safe test data. These steps cover a new transfer-routing rule, not a work-order rule or an existing rule's modification/deletion. If your requirement differs or values are missing, resolve the gap with your functional owner before changing configuration.
2. In Setup and Maintenance, select the Manufacturing and Supply Chain Materials Management offering and Supply Chain Orchestration functional area, then open this task. If access is unavailable, stop for setup/security administrator review. Review existing rules and resolve overlapping conditions with your functional owner; do not assume rule priority.
3. Confirm the transfer is eligible for Order Management routing. Exclude back-to-back sales-demand transfers, return transfers, intraorganization transfers, and expense-destination transfers originating from requisitions.
4. Before entering a change, obtain the administrator-confirmed final save/activation sequence for your UI. The documented steps establish condition/action entry, not the final persistence or publication controls. Stop if the necessary controls or current-release behavior are unconfirmed.
5. Choose **Create New Rule** and enter your approved **Rule Name**. In the IF area, choose **New Condition**, search for the requested supply type, and select the Supply Line-level attribute. Set equality with `Transfer`, then accept the dialog. Check the entity path because similar attribute names can appear at different hierarchy levels.
6. Choose **Then > Do**, then **New Action > Perform an Action**. Select the Order Management shipping action, set its shipment flag to `Yes`, and accept the dialog. Add only approved condition restrictions through the hierarchy/search mechanism. A transfer-only condition is broad; do not apply it without approval of that scope.
7. Compare the complete condition and action with the approved change, then follow the confirmed save/activation sequence manually. Accepting an action dialog alone does not prove that the rule is saved or active. If the UI differs or a required detail remains unclear, stop for administrator clarification rather than guessing.

## Manual Validation Guidance

- Reopen the persisted rule and compare its name, attribute entity paths, conditions, and action with the approved change.
- In an approved nonproduction flow, test an eligible matching transfer and inspect the linked sales order and Order Management routing. Confirm downstream prerequisites before interpreting failures.
- Test a comparable nonmatching case against its agreed baseline; other rules may still apply.
- Record the rule identifier/name, environment, test transaction references, expected and actual results, and reviewer decision. Mark unexecuted checks as not run; a saved rule alone is not a runtime pass.
