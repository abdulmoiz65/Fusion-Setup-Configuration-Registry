# Dependency Readiness

## Source

| Source | Location | Used For |
|---|---|---|
| Oracle Valuation Structures | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-structures-and-valuation-units.html | Flexfield prerequisite |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| VS-COSTING-FLEXFIELD | Costing flexfield structure | Yes | Always | Verify | Oracle valuation-structure configuration | | The flexfield structure determines the costing attributes enabled for the valuation structure. | Confirm the Cost Organization attribute and the selected costing attributes are enabled in the flexfield structure. | Enabled costing attributes |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The selected costing attributes are enabled in the costing flexfield structure | No |
| Blocked | A required costing attribute is not enabled in the costing flexfield structure | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VS.CHECK_DEPENDENCIES | decision | 7 | resolve_dependency | ready->VS.ENFORCE_DESIGN;blocked->VS.HANDLE_ISSUE | VS.DEFAULT_CONSIGNED_MODE | stop | Creating or changing a Valuation Structure |
