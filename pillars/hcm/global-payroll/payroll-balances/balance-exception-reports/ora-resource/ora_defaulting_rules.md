# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| BaseBalExcepReportName | BalExcepReportName | A report is created or updated and no base report name is supplied | No | |
| ConsolidationSetId | `#null` in the FSM CSV; blank in the conceptual definition | No definition-level consolidation restriction is intended | No | This is optional. Keep `ConsolidationSetName` blank; use the FSM null sentinel for the omitted identifier column. |
| PayrollId | `#null` in the FSM CSV; blank in the conceptual definition | No definition-level payroll restriction is intended;a payroll remains required only when running the report | No | This is optional at definition. Keep `PayrollName` blank; use the FSM null sentinel for the omitted identifier column. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEXR.APPLY-BASE-NAME-DEFAULT | step | 9 | apply_default | applied->BEXR.ENFORCE-FSM-DESIGN;skipped->BEXR.ENFORCE-FSM-DESIGN | BEXR.VERIFY-FSM-TEMPLATE | stop | A validated report definition is being prepared |
