# Cost Profiles Input Validation

Source: [Oracle Fusion Cloud SCM 26c: Set Up a Cost Profile](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/set-up-a-cost-profile.html).

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Profile identity | Specified Set Name and Cost Profile | Block before preview | Supply the exact set name and profile name | Always | resolve_costing_set_by_exact_name |
| Delete or update identity | Resolved CostProfileId and Cost Profile Code | Block before preview | Resolve CostProfileId using `resolve_cost_profile_id`; when Set Name is absent, proceed only from a unique exact Cost Profile Code result | Delete or update | resolve_cost_profile_id |
| Accounting policy | User Specified Cost Method | Block before preview | Supply the exact cost method | Always | resolve_cost_method_by_exact_meaning |
| Valuation policy | User Specified Valuation Structure Type, Valuation Structure Code, and Cost By | Block before preview | Supply the valuation structure type and select the valuation control attributes and primary or secondary UOM costing | Always | resolve_valuation_structure_type_by_exact_meaning |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Standard or periodic valuation level | Require Cost Organization or Inventory Organization valuation level | Cost Method is Standard cost or Periodic average | |
| Transaction-date processing | Require Process Negative Quantity = Always and Propagate Cost Adjustment deselected | Enforce Processing of Costs by Transaction Date is selected | |
| Cost by UOM | Require a unique exact Cost by UOM lookup result | User Specified Cost By UOM is supplied | resolve_cost_by_uom_by_exact_meaning |
| Process Negative Quantity | Require a unique exact Process Negative Quantity lookup result | User Specified Process Negative Quantity is supplied | resolve_process_negative_quantity_by_exact_meaning |
| Operation Scrap Accounting | Require a unique exact Operation Scrap Accounting lookup result | User Specified Operation Scrap Accounting is supplied | resolve_operation_scrap_accounting_by_exact_meaning |
| Operation Scrap Valuation | Require a unique exact Operation Scrap Valuation lookup result | User Specified Operation Scrap Valuation is supplied | resolve_operation_scrap_valuation_by_exact_meaning |
| Receipt Without Cost | Require one exact Receipt Without Cost lookup result | User Specified Receipt Without Cost is supplied | resolve_receipt_without_cost_by_exact_meaning |
| Unreferenced RMA Receipt Cost | Require a unique exact Unreferenced RMA Receipt Cost lookup result | User Specified Unreferenced RMA Receipt Cost is supplied | resolve_unreferenced_rma_receipt_cost_by_exact_meaning |
| Referenced RMA Cost | Require the documented referenced-RMA lookup to return one result | Always | resolve_referenced_rma_cost |
| Create Accounting for Consigned Transactions | Accept only Y, N, or null; reject any other value | A value is supplied | |
| Consigned Accounting Distribution Basis | Require a unique exact lookup result | User Specified Value for Accounting Distribution Basis is supplied | resolve_consigned_accounting_distribution_basis_by_exact_meaning |
| Valuation Structure Id | Require the resolved Set Id and Valuation Structure Type Code to return one valuation structure | Always | resolve_valuation_structure_id |
| Component Group Id | Require the supplied Set Name and Component Mapping Group Name to return one component group | A Component Mapping Group Name is supplied | resolve_component_group_id |
| Analysis Mapping | Obsolete attribute; do not require, resolve, validate, or map Analysis Mapping values | Always | |
| Boolean payload flags (`AccountIntravaluationUnitTransfersFlag`, `AccountIntraVUPickTransactionEnabled`, `SummarizeCostTransactionsForLotsFlag`, `SummarizeCostTransactionsSerialsFlag`, `EnforceTransactionDateOrderFlag`, `PropagateCostAdjustmentFlag`, and `CreateAccountForConsignedTransactions`) | Case-insensitively translate `Yes`, `Y`, or `true` to `Y`; translate `No`, `N`, or `false` to `N`; retain null when the user value is null; reject any other value | A value is supplied | |
| Create payload code/value completeness | For every non-Consigned `RestAction=POST` record, require populated code and display values for Cost Method, Cost By UOM, Process Negative Quantity, Receipt Without Cost, Referenced RMA Cost, and Unreferenced RMA Receipt Cost. Consigned records must leave both RMA pairs null. Require Operation Scrap Accounting, Operation Scrap Valuation, Provisional Completions, and Provisional Completions for Process Manufacturing only when either member of that pair is supplied. Validate with `validate_cost_profile_create_payload.py`. | Always for create rows | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CP.VALIDATE_INPUT | step | 10 | validate_input | valid->CP.RESOLVE_COSTING_SET;invalid->CP.HANDLE_ERROR | none | stop | Before preview |
