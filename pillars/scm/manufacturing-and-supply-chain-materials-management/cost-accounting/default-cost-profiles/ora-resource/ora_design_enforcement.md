# Default Cost Profiles Design Enforcement

Source: [Oracle Fusion Cloud SCM 26c: Set Up a Default Cost Profile](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/set-up-a-default-cost-profile.html).

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate periodic-average compatibility | When any resolved type-specific cost profile has `CostMethodCode = PERIODIC_AVERAGE`, require the resolved cost book's `PeriodicAverageFlag` to be `Y`. |
| 2 | Review new-item profile behavior | Assess the selected New Item Profile Creation setting before preview. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any resolved Asset, Expense, or Consigned Cost Profile has `CostMethodCode = PERIODIC_AVERAGE` | Error | resolve_cost_book_by_cost_organization | No cost book was resolved, or the resolved cost book's `PeriodicAverageFlag` is not `Y` | Provide a cost book with `PeriodicAverageFlag = Y` or select cost profiles whose `CostMethodCode` is not `PERIODIC_AVERAGE` | Yes |
| The implementation uses file-based data import or ADF Desktop Integrator to import cost data | Recommendation | | None; Oracle documents this as a recommendation | Set New Item Profile Creation to Automatic so the preprocessor assigns the default cost profile to new items and the item cost profiles can be used by the cost processor | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_cost_book_by_cost_organization | Any resolved Asset, Expense, or Consigned Cost Profile has CostMethodCode = PERIODIC_AVERAGE | PeriodicAverageFlag | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCP.ENFORCE_PERIODIC_AVERAGE_COST_BOOK | decision | 30 | design_enforcement | passed->DCP.ENFORCE_IMPORT_RECOMMENDATION;blocked->DCP.HANDLE_ERROR | DCP.RESOLVE_CONSIGNED_COST_PROFILE | stop | Before preview when any resolved type-specific cost profile has `CostMethodCode = PERIODIC_AVERAGE` |
| DCP.ENFORCE_IMPORT_RECOMMENDATION | decision | 31 | design_enforcement | passed->DCP.DONE;blocked->DCP.HANDLE_ERROR | DCP.ENFORCE_PERIODIC_AVERAGE_COST_BOOK | stop | Before preview |
