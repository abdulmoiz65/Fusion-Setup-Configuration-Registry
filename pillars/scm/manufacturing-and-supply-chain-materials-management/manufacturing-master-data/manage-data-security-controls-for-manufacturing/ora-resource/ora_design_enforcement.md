# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Control-data scope | Keep exactly one existing control-data row and restrict it to WORK_DEFINITION. |
| 2 | Centralized execution boundary | Submit only the immutable validated ZIP through the core.data-loader workflow after current approval. |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| SEC.DESIGN.WORK_DEFINITION_ONLY | Every update request | Blocker | | The validated row is not the sole WORK_DEFINITION control-data object | Correct the target to WORK_DEFINITION. | Yes |
| SEC.DESIGN.UPDATE_ONLY | Every update request | Blocker | | The request proposes to create or delete a row, the value is not Y or N, or RestAction is not PATCH | Stop; this task changes DataSecurityEnabledFlag only for the existing WORK_DEFINITION control. | No |
| SEC.DESIGN.CENTRAL_DATA_LOADER_REST | Every Data Loader REST update | Blocker | | The ZIP was not produced by core.data-loader validation, differs from the approved immutable artifact, or an executor bypasses core.data-loader | Use only the validated task ZIP and the centrally authorized core.data-loader workflow. | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SEC.DESIGN | step | 4 | design_enforcement | ok->SEC.DONE;failure->SEC.FAILED | SEC.DEPENDENCIES | stop | Validated Data Loader REST artifact is complete |
