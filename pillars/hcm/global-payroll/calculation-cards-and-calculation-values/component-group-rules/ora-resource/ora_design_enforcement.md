# Design Enforcement

Component Group Rules is a legacy entry point. This task records only a task-local redirect decision. It does not execute the destination skill or encode a cross-task transition.

## Enforcement Order

| Sequence | Step | What Must Happen |
| --- | --- | --- |
| 1 | Recognize legacy entry point | Treat every request selected as Component Group Rules as a redirect request. |
| 2 | Stop legacy execution | Do not use the legacy CSV export, CSV import, Data Loader, Fusion API, browser, or generated legacy workflow. |
| 3 | Build routing handoff | Preserve only the normalized implementation objective and return the exact requested-task, target-task, target-skill, and router identities. |
| 4 | End the current task | Transition to CGR.REDIRECTED and return the handoff to the invoking Implementation Router so it can start a fresh Payroll Components task run. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
| --- | --- | --- | --- | --- | --- |
| Always | Blocker |  | The current task attempts to process Component Group Rules locally, invoke Payroll Components directly, encode a cross-task transition, reuse legacy execution state, or claim one-to-one feature parity | End this task as REDIRECTED and return the exact Payroll Components handoff to router.implementation-router | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CGR.REDIRECT | step | 1 | design_enforcement | redirected->CGR.REDIRECTED | none | stop | Always |
