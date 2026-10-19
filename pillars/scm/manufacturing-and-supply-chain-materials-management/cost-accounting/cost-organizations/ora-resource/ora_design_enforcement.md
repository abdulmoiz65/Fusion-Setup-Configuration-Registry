# Design Enforcement

## Source

- User-provided update policy: during an update operation, only Cost Organization Name and Status are allowed to change.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Identify update fields | Identify the requested mutable fields for the selected existing Cost Organization. |
| 2 | Enforce permitted fields | Permit only CostOrganizationName and Status; reject every other requested mutable field. |
| 3 | Bind approval preview | Show the exact CostOrganizationCode and the permitted requested changes in the immutable Data Loader approval preview. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Updating an existing Cost Organization | Error | | The update includes a mutable field other than CostOrganizationName or Status, or includes neither permitted field. | Use CostOrganizationCode solely to select the existing Cost Organization, then supply one or both permitted fields only. | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCO.UPDATE_ALLOWED_FIELDS | decision | 13 | design_enforcement | passed->CCO.UPDATE_APPROVAL_GATE;blocked->CCO.HANDLE_ISSUE | CCO.UPDATE_NORMALIZE_STATUS | stop | Updating an existing Cost Organization; only CostOrganizationName and Status may be changed |
