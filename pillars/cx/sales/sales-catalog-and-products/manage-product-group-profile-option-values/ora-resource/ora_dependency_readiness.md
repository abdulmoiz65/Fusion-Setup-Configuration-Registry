# Dependency Readiness

The proposed item master must already exist before
`QSC_SALES_PRODUCTS_INVENTORY_ORG_ID` receives a value through a direct Site-value
change or an FSM import. This task validates the prerequisite but never creates
it. The other FSM-only profile options do not evaluate this dependency.
A removal request does not select an item master and bypasses this dependency.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Item-master availability | Resolve the proposed code or name as exactly one active master organization through the documented live lookup. |
| 2 | Profile value preparation | Use the resolved organization identity to prepare the direct QSC Site-value preview or approve the QSC FSM import. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| QSC.PROFILE.ITEM_MASTER_ORGANIZATION | Intended item master organization | Yes | A direct request provides an organization, or a QSC FSM import does, for QSC_SALES_PRODUCTS_INVENTORY_ORG_ID | Verify | Exactly one active Inventory Organizations record for the proposed code or name | resolve_sales_product_item_master | The profile value selects the item master that supplies sales products | Resolve the supplied code or name; do not create a prerequisite or substitute another source | resolved_item_organization |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Missing dependency | The code or name lookup returns zero active master-organization matches | No |
| Blocker | The code or name lookup returns multiple matches, a code/name conflict, or access/data security prevents validation | No |
| Satisfied | One live lookup resolves the proposed item master | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QSC.PROFILE.DEPENDENCY | decision | 6 | resolve_dependency | satisfied->QSC.PROFILE.DESIGN;blocked->QSC.PROFILE.BLOCKED | QSC.PROFILE.ITEM_ORGANIZATION | stop | Run only when a direct QSC request provides an organization for QSC_SALES_PRODUCTS_INVENTORY_ORG_ID; confirm the resolved item master exists before profile-value execution planning |

For an explicitly requested QSC FSM import, `core.data-loader` invokes the same dependency and
lookup requirements before import approval. The task-local node remains scoped
to a direct value-change request because only that route continues to the Apps Common execution
gate.
