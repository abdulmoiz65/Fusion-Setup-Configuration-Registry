# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Package, parent-child, or semantic gate fails | Stop before candidate preparation and state the exact missing package fact or documented contract |
| Preview or import reports an error | Preserve sanitized diagnostics and the immutable candidate identity; do not retry automatically |
| Outcome is uncertain | Do not resubmit; reconcile the original attempt through the central workflow |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input blocked | Exact package structure or parent-child linkage is invalid | Correct the package or linkage and revalidate |
| Design blocked | Field lifecycle semantics or governed execution evidence is missing | Obtain the documented evidence or approval boundary before preview |
| Execution blocked | Immutable preview or explicit approval is absent | Complete the central preview and approval workflow |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before any candidate import | Exact task, target scope, immutable preview identity, known blockers, and required approval boundary |
| On failure | Failure class, sanitized diagnostics reference, and safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing field semantics | Do not infer required values, defaults, field types, allowable values, updateability, resolver behavior, or direct-write endpoints |
| Failed or uncertain import | Do not automatically retry or resubmit |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CALENDAR.VALIDATE_INPUT | step | 10 | validate_input | valid->CALENDAR.ENFORCE_DESIGN;invalid->CALENDAR.INPUT_BLOCKED | none | stop | Always |
| CALENDAR.ENFORCE_DESIGN | decision | 20 | design_enforcement | ready->CALENDAR.EXECUTION_GATE;blocked->CALENDAR.DESIGN_BLOCKED | CALENDAR.VALIDATE_INPUT | stop | Always |
| CALENDAR.EXECUTION_GATE | decision | 30 | execution_gate | approved_preview->CALENDAR.READY_FOR_DATA_LOADER;not_ready->CALENDAR.EXECUTION_BLOCKED | CALENDAR.ENFORCE_DESIGN | stop | A governed execution request exists |
| CALENDAR.INPUT_BLOCKED | terminal | 40 | terminal | none | none | stop | Package or parent-child validation fails |
| CALENDAR.DESIGN_BLOCKED | terminal | 50 | terminal | none | none | stop | A package or semantic evidence blocker is reached |
| CALENDAR.READY_FOR_DATA_LOADER | terminal | 60 | terminal | none | CALENDAR.EXECUTION_GATE | stop | A governed immutable preview and explicit approval are available |
| CALENDAR.EXECUTION_BLOCKED | terminal | 70 | terminal | none | none | stop | Execution approval or preview is absent |
