# Reservation Priority for Sales Orders Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate export-derived package | Confirm that the FSM package uses the official task template and a current setup baseline. |
| 2 | Verify migration compatibility | Confirm that the source and target Order Management instances are at the same release level. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An FSM import is requested for Reservation Priority page setup | Critical | None | The package was not derived from the official task export/template, or the source and target Order Management instances are not at the same release level. | Export the setup from the source instance and migrate it through the reviewed configuration package. | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RESERVATION_PRIORITY.VALIDATE_FSM_MIGRATION | step | 30 | design_enforcement | compatible_migration->RETURN_SUCCESS;incompatible_migration->RETURN_ISSUES | RESERVATION_PRIORITY.FSM_IMPORT_PREVIEW | stop | An FSM import is requested for Reservation Priority page setup. |
