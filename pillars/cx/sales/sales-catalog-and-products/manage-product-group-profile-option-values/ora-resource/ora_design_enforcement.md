# Design Enforcement

This resource owns the QSC item-master design policy after the dependency has
resolved. The profile value must use the Site level and the resolved item
master when an organization is provided directly or through an FSM import. The other FSM-only
profile options do not use this design policy.
A removal request has no proposed item master and bypasses this design policy.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm QSC scope | Use QSC_SALES_PRODUCTS_INVENTORY_ORG_ID at the Site level. |
| 2 | Confirm dependency evidence | Use the single resolved item-master organization and its OrganizationCode from the dependency outcome. |
| 3 | Permit execution preparation | Continue only when the direct request or FSM import remains within that scope. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A direct request provides an organization, or a QSC FSM import does, for QSC_SALES_PRODUCTS_INVENTORY_ORG_ID | Blocker | resolve_sales_product_item_master | The profile code or level differs, the supplied code or name is ambiguous, or the required item-master dependency is not satisfied | Use the resolved OrganizationCode as the Site value. Complete the prerequisite setup before retrying when it is unavailable. | Yes, before preview or import approval |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_sales_product_item_master | Before direct QSC preview or QSC import approval | resolved_item_organization | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QSC.PROFILE.DESIGN | decision | 7 | design_enforcement | passed->QSC.PROFILE.EXECUTION_GATE;blocked->QSC.PROFILE.BLOCKED | QSC.PROFILE.DEPENDENCY | stop | Run only when a direct QSC request provides an organization for QSC_SALES_PRODUCTS_INVENTORY_ORG_ID; enforce the direct Site-level design before the execution gate |

For an explicitly requested QSC FSM import, `core.data-loader` enforces the same design rule and
lookup evidence before import approval. The task-local node remains scoped to
direct value-change request because only that route continues to the Apps Common execution
gate.
