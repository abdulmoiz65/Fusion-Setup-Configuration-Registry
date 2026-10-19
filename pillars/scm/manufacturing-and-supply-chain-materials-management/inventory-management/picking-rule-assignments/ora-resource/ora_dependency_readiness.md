# Picking Rule Assignments Dependency Readiness

## Source Evidence

| Source | Used For |
|---|---|
| Target-environment Data Loader metadata and sample/validation result | Verifies the registered `inventoryPickingRuleAssignments` BO, its available attributes, and the accepted Rule Name input contract before preparation. |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Existing Picking Rule | Supply a globally unique Picking Rule name that the BO can resolve to `PickingRuleId`. |
| 2 | BO-owned foreign-key resolution | The target-environment registered BO must resolve approved friendly values to the corresponding REST fields before Data Loader execution. |
| 3 | Standard-lookup readiness | Resolve any supplied Item Type, Date Type, and Transaction Action input through the approved read-only lookups. |
| 4 | Data Loader metadata visibility | Confirm that `inventoryPickingRuleAssignments` is published and visible to Data Loader before import preparation. |
| 5 | FSM assignment baseline, when applicable | When an FSM criterion package is selected, obtain a current Picking Rule Assignments export containing the required metadata, parent carrier, and criterion members before package preparation. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| picking_rule_identity | Picking Rule identity | Conditional | `RuleName` is supplied | BO-owned lookup | Target-environment registered BO metadata or validation |  | The validated BO contract must resolve the supplied exact `RuleName` to `PickingRuleId`; otherwise preparation stops. | Supply an exact Picking Rule name and retain the validation result. | `PickingRuleId` or validation diagnostic |
| bo_reference_values | BO foreign-key values | Conditional | Friendly BO attributes are supplied | BO-owned lookup | Registered BO foreign keys |  | BO metadata owns carrier, category, customer, UOM, and ABC group/class resolution. | Supply the corresponding friendly value; do not provide the resolved ID unless the BO contract requires it. | `FreightCarrierId`, `CategoryId`, `CustomerId`, `UOMCode`, `AbcClassId`, `AssignmentGroupId` |
| item_type_lookup | Item Type lookup | Conditional | Item Type is supplied | Lookup | `standardLookupsLOV` | resolve_item_type | The approved standard lookup resolves the supplied Meaning to its canonical code. | Supply an exact Meaning or canonical value. | `ItemType` |
| date_type_lookup | Date Type lookup | Conditional | Date Type is supplied | Lookup | `standardLookupsLOV` | resolve_date_type | The approved standard lookup resolves the supplied Meaning to its canonical code. | Supply an exact Meaning or canonical value. | `DateTypeCode` |
| transaction_action_lookup | Transaction Action lookup | Conditional | Transaction Action is supplied | Lookup | `standardLookupsLOV` | resolve_transaction_action | The approved standard lookup resolves the supplied Meaning to its canonical code. | Supply an exact Meaning or canonical value. | `TransactionActionId` |
| picking_rule_submission_contract | Picking Rule submission behavior | Yes | Before execution readiness | Verify | Target-environment `core.data-loader` sample generation or immutable-source validation result |  | The target environment must prove that the selected `RuleName` input is accepted or identify the required mapping before preparation. | Generate a target-environment sample or validate the immutable source; stop when the Rule Name contract is unavailable or differs. | Accepted Rule Name mapping or validation diagnostic |
| inventory_picking_rule_assignments_bo | Data Loader business object metadata | Yes | Before `core.data-loader` preparation | Verify | Target-environment `core.data-loader` metadata visibility and generated sample or validation result |  | The registered `inventoryPickingRuleAssignments` BO must be visible and usable in the selected target environment. | Generate a target-environment sample or validate the immutable source; stop when the BO is unavailable or unpublished. | Business object discriminator and validation result |
| picking_rule_assignments_fsm_baseline | Current Picking Rule Assignments FSM export | Conditional | An FSM package with `INV_RULE_SELECTION_CRITERION.csv` is selected | Verify | Current `ORA_PICKING_RULE_ASSIGNMENTS` export and receipt |  | The export supplies the authoritative metadata, existing criterion rows, and native headers; its receipt establishes task, source environment, release, and archive identity. | Obtain a current assignment export and receipt; do not reconstruct metadata or criteria from REST attributes. | Assignment export archive, fingerprint, and receipt |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required BO metadata is visible and each supplied approved lookup resolves exactly once. | Continue. |
| Lookup | A supplied standard-lookup value requires read-only normalization. | Read-only lookup only. |
| Blocked | BO metadata or the Rule Name contract is unavailable or differs in the selected target environment, a required FSM baseline is absent, or any lookup is missing or ambiguous. | No. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PRA.CHECK_READINESS | decision | 50 | resolve_dependency | ready->PRA.DATA_LOADER_HANDOFF;blocked->PRA.HANDLE_ERROR | PRA.RESOLVE_TRANSACTION_ACTION | stop | Before Data Loader preparation. |
| PRA.CHECK_FSM_READINESS | step | 51 | resolve_dependency | ready->PRA.FSM_DATALOADER_HANDOFF;blocked->PRA.HANDLE_ERROR | PRA.VALIDATE_FSM_ARCHIVE | stop | Classified FSM archive passed export-baseline and package-readiness checks. |
