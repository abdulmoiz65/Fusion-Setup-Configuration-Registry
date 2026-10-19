# Shifts and Schedules Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| execution_direction | data_loader_execution | The end user omits execution_direction | Yes; the only accepted override is ora_rest_execution | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SS.SELECT_EXECUTION_DIRECTION | step | 10 | apply_default | selected->SS.VALIDATE_INPUT | none | stop | Every workbook-backed request |
