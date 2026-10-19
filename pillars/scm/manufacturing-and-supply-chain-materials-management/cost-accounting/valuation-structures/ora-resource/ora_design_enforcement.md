# Design Enforcement

## Source

| Source | Location | Used For |
|---|---|---|
| Oracle Valuation Structures | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-structures-and-valuation-units.html | Granularity, type, cost-method, and post-transaction rules |
| Oracle Valuation Structure Rules | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-structure-rules.html | Mandatory and optional attribute-change constraints |
| Oracle Valuation Units | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-units.html | Automatic generation recommendation and manual-unit rationale |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Set cost granularity | Select costing attributes that produce the intended lowest cost-maintenance level. |
| 2 | Confirm cost-method compatibility when an item cost profile is in scope | For a standard-cost or periodic-average-cost item cost profile, limit the associated valuation structure to Cost Organization or Cost Organization - Inventory Organization. This is an association check, not a valuation-structure creation prerequisite. |
| 3 | Confirm inventory compatibility | Ensure costing attributes are consistent with inventory attributes and are not more granular than inventory on hand. |
| 4 | Select valuation-unit behavior | Prefer automatic unit generation; use manual units only when entities must share a common cost. |
| 5 | Enforce consigned mode | Require AUTO when the resolved Valuation Structure Type Code is CONSIGNED. |
| 6 | Protect processed history | Do not add or delete costing attributes after transactions are performed against the valuation structure. |

## Design Rules

| Applies When | Severity | Required Lookup | What Blocks Preview | Fix Allowed? | User Guidance |
|---|---|---|---|---|---|
| Always | Error | | Cost Organization is not included, or selected costing attributes are incompatible with inventory attributes or more granular than inventory on hand | Yes, before transactions | Include Cost Organization and redesign the attribute set to match inventory control. |
| The cost profile uses standard cost or periodic average cost | Error | | The valuation structure is more granular than Cost Organization - Inventory Organization | Yes, before transactions | Use Cost Organization or Cost Organization - Inventory Organization only. |
| Project or Task is selected | Error | | Project-Driven Supply Chain is not opted in and set up | Yes | Complete Project-Driven Supply Chain setup or remove Project and Task. |
| An item lacks a costing attribute used by the valuation structure | Error | | The missing attribute is mandatory | Yes, subject to processed-history restriction | Make the attribute optional only when permitted; an optional missing attribute produces a Null valuation-unit value. |
| A prior transaction used the valuation structure | Error | | The change adds or deletes a costing attribute | No | Create a safe future-state design; do not change the processed valuation structure. |
| A manual valuation-unit design is proposed | Warning | | The design does not require grouping entities to share a common cost | Yes | Use automatic generation unless manual grouping is required. |
| The resolved Valuation Structure Type Code is CONSIGNED | Error | | The resolved Valuation Structure Mode Code is not AUTO | Yes, by using AUTO | Use AUTO for a CONSIGNED valuation structure. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VS.ENFORCE_DESIGN | decision | 8 | design_enforcement | compliant->VS.COMPLETE;blocked->VS.HANDLE_ISSUE | VS.CHECK_DEPENDENCIES | stop | Creating or changing a Valuation Structure |
