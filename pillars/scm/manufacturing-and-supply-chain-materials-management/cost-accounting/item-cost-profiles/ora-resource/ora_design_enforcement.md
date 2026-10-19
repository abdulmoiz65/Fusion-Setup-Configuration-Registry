# Design Enforcement

## Source

| Source | Location | Used For |
|---|---|---|
| Oracle Fusion Cloud SCM 26c | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/cost-profiles-default-cost-profiles-and-item-cost-profiles.html | Reusable Cost Profile and Cost Profile Set design practice for Item Cost Profile assignments |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve dependencies | Complete the applicable Item Cost Profile dependency and reference checks. |
| 2 | Apply reusable Cost Profile policy | Use an approved reusable Cost Profile for the applicable policy rather than treating every item assignment as a reason to create a separate profile. |
| 3 | Apply Cost Profile Set sharing | Use the Cost Profile Set to share the approved profile definition when Cost Organizations follow the same costing rules. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An Item Cost Profile assignment is being designed | Best practice | | A distinct Cost Profile is proposed only because the assignment is for a different item, without a documented policy difference | Reuse the approved Cost Profile that implements the same policy; do not create one profile per item. | Yes, select the approved reusable profile. |
| Multiple Cost Organizations follow the same costing policy | Best practice | | Equivalent profiles are maintained separately without a policy reason | Share the approved profile definition through its Cost Profile Set. | Yes, align the assignment to the approved shared profile. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ICP.ENFORCE_LOADER_PAYLOAD_CONTRACT | decision | 8 | design_enforcement | valid->ICP.READY_FOR_REST_IMPORT;invalid->ICP.HANDLE_ISSUE | ICP.RESOLVE_CONSIGNED_COST_PROFILE | stop | Applying Item Cost Profile design practice |
