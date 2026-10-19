# Manage Organization Hierarchies and Classifications Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Omitted hierarchy type | Preserve the reconciled current target value | Update request | No | resolve_current_org_hierarchy_setup |
| Omitted classifications | Preserve the complete reconciled current selected set | Update request | No | resolve_current_org_hierarchy_setup |
| New internal hierarchy row | `ORA_PJF_NO_TREE_STRUCTURE` (None) | UI initialization finds no hierarchy row; creates and commits the row immediately | No existing row is overwritten; require the approved customer decision before FSCR preview | resolve_allowed_hierarchy_type |
| Default tree, version, and starting organization | No default | Organization or department hierarchy | No | resolve_default_org_hierarchy |
| Values outside approved scope | Preserve current target state | Every update or import preview | No | resolve_current_org_hierarchy_setup |
| Import execution route | Template-gated FSM through core.data-loader | Supported additive import is requested | No | verify_org_hierarchy_fsm_package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OHCL.APPLY_DEFAULTS | step | 7 | apply_default | prepared->OHCL.ENFORCE_DESIGN;blocked->OHCL.HANDLE_ERROR | OHCL.CHECK_DEPENDENCIES | stop | Preserve omitted and out-of-scope values without inventing a hierarchy design |

## Refined Defaults

- **BP-009 — Required evidence:** Default to an organization hierarchy when the business unit has multiple cost centers, owning or expenditure organizations, cross-charge, indirect-cost allocation, or meaningful reporting or security requirements.

## UI Behavior Boundaries

Opening the hierarchy page when no hierarchy row exists initializes and saves None. Do not open live configuration merely to inspect an absent setup. Existing rows are not reset by that initialization.

Accepting a hierarchy-type change resets the default-hierarchy selection. A Department hierarchy offers department starting organizations; other supported hierarchy choices use their applicable organization selection. Re-resolve requested tree, version and starting organization instead of discarding explicitly supplied working values.

Saving a changed valid default hierarchy can replace both owning and expenditure hierarchy details across business units. Selecting None uses tree ORA_PJF_NO_TREE, version -1 and starting organization -1. Disclose the full business-unit impact; this UI behavior does not authorize FSCR to update existing BUs or add internal values to an import template. Preserve the template-gated route and approved scope. The business-policy preference above is distinct from product initialization.
