---
task_code: "ORA_DOS_MANAGE_SUPPLY_EXECUTION_DOCUMENT_CREATION_RULES"
task_name: "Manage Supply Execution Document Creation Rules"
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

# Manage Supply Execution Document Creation Rules

- **Task code:** `ORA_DOS_MANAGE_SUPPLY_EXECUTION_DOCUMENT_CREATION_RULES`
- **Purpose:** Define when an eligible transfer request uses a purchase order instead of a transfer order.
- **Execution rule:** The user completes the approved change manually on the Manage Execution Document Creation Rules page reached through Oracle Fusion Setup and Maintenance; no API, import, automated configuration, or browser automation.

Use the standard manual workflow in [SKILL.md](../../../../shared/common/manual-tasks/SKILL.md).

Provide manual steps directly from this task using the user’s supplied values. Stay within the documented guidance, identify missing details, and do not create separate guides or project artifacts solely to explain the steps.

## Manual Steps

1. Confirm your target environment and release, approved rule name/description, purchasing requirement, source/destination values, and safe test data. These steps cover a new transfer-to-buy rule for one source/destination inventory or warehouse pair. Do not substitute sample organizations or extend the rule to unapproved pairs. Resolve missing values or a different requirement with your functional owner before changing configuration.
2. Confirm the source organization's supplier and supplier-site association. Exclude transfers sourced from requisition lines; their purchasing-versus-transfer decision is made at requisition entry.
3. Confirm party-data maintenance with the responsible administrator. The documented process is **Maintain Party and Location Current Record Information**, with **Synchronization Type** set to **Party and Location**, other parameters empty, and a schedule of at least once daily. Review existing scheduling first; missing prerequisite setup requires a separately approved manual change.
4. In Setup and Maintenance, select the Manufacturing and Supply Chain Materials Management offering and Supply Chain Orchestration functional area, then open this task. Its page is named Manage Execution Document Creation Rules. If access is unavailable, stop for setup/security administrator review. Review existing rules and resolve overlapping conditions with your functional owner; do not assume priority.
5. Before creating a rule, obtain administrator confirmation of the initial create control, exact condition/action entity selections, and final save/activation sequence for your UI. The documented procedure does not establish those controls or publication requirements. Stop if these details are unavailable; do not assume they match another task.
6. Using the confirmed create control, enter the approved name and description. Build an AND condition requiring requested supply type `Transfer`, the approved source organization, and the approved destination organization. In the Do statement, change the requested supply type to `Buy`. Verify each entity selection; do not use the Order Management shipping action from the defaulting/enrichment task.
7. Review the complete rule with your functional owner, then follow the confirmed save/activation sequence manually. Stop if the UI differs or any required detail is unresolved. A saved rule is not evidence that a purchasing document has been created.

## Manual Validation Guidance

- Reopen the persisted rule and verify the source/destination values, AND logic, incoming transfer type, and outgoing buy type.
- In an approved nonproduction flow, test a matching eligible request. Inspect its supply type, resulting purchasing document, and supplier/site associated with the source organization; record actual document references.
- Test a nonmatching source/destination pair against its agreed baseline. Transfer is the documented default, but other rules or setup can affect the outcome. Exclude requisition-origin scenarios from this conversion test.
- If processing fails, capture the displayed diagnostic for the responsible owner. Do not repeatedly submit requests or alter unrelated setup. Any modification/deletion for recovery requires separate approval and a confirmed procedure.
- Record the rule identifier/name, environment, approval reference, test transaction references, expected and actual results, and reviewer decision. Mark unexecuted checks as not run.
