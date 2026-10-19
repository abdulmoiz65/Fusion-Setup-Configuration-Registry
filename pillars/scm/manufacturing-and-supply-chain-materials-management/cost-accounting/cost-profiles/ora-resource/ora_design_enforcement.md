# Cost Profiles Design Enforcement

Source: [Oracle Fusion Cloud SCM 26c: Set Up a Cost Profile](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/set-up-a-cost-profile.html).

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Identity and accounting policy | Provide the profile set, profile name, and cost method |
| 2 | Cost-adjustment applicability | Validate Propagate Cost Adjustment against the selected cost method |
| 3 | Valuation compatibility | Validate valuation structure against the selected cost method |
| 4 | Transaction processing compatibility | Validate options that have documented method-dependent restrictions |
| 5 | Consigned applicability | Validate attributes that are exclusive to or inapplicable for the Consigned valuation structure type |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Propagate Cost Adjustment is selected | Error | | Cost Method is not Actual cost | Deselect Propagate Cost Adjustment or select Actual cost | Yes |
| Cost Method is Standard cost or Periodic average | Error | | Valuation Structure Code is more granular than Cost Organization or Inventory Organization | Select a supported valuation level | Yes |
| Enforce Processing of Costs by Transaction Date is selected | Error | | Process Negative Quantity is not Always or Propagate Cost Adjustment is selected | Set the documented compatible options | Yes |
| Account Intravaluation Unit Pick Transactions is selected | Error | | Account Intravaluation Unit Transfers is not selected | Select transfers first or deselect pick transactions | Yes |
| Valuation Structure Type Code is CONSIGNED | Error | | Process Negative Quantity is not To Zero | Set Process Negative Quantity to To Zero | Yes |
| Valuation Structure Type Code is CONSIGNED | Error | | Operation Scrap Accounting, Operation Scrap Valuation, Account Intravaluation Unit Pick Transactions, Provisional Completions, Provisional Completions for Process Manufacturing, Referenced RMA Cost, or Unreferenced RMA Receipt Cost contains a value | Clear the inapplicable attributes; they must be null for consigned valuation structures | Yes |
| Valuation Structure Type Code is not CONSIGNED | Error | | Consigned Accounting Distribution Basis or Create Accounting for Consigned Transactions contains a value | Clear both attributes; they must be null outside consigned valuation structures | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CP.ENFORCE_DESIGN | decision | 30 | design_enforcement | passed->CP.DONE;blocked->CP.HANDLE_ERROR | CP.RESOLVE_VALUATION_STRUCTURE_ID | stop | Before preview |
