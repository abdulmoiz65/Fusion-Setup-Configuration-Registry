# Design Enforcement

## Delegation Policy

Do not duplicate or weaken the shared task's archive, privilege, target,
approval, import, or retry controls. The pillar task may only route its fixed
Field Service and Users and Security context to the shared workflow. Any new or
modified archive, scope, source, target, or validation result is a new shared
workflow request.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HRPRFS.ENFORCE_DELEGATION | decision | 3 | design_enforcement | pass->HRPRFS.EXECUTION_GATE;fail->HRPRFS.BLOCKED | HRPRFS.CHECK_SHARED_WORKFLOW | stop | Before returning a task-routed Data Loader approval preview. |
