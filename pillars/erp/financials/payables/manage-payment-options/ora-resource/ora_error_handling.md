# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Input, dependency, or design gate fails | Stop before candidate generation or import, retain the missing requirement, and request the exact correction or evidence |
| Preview or import reports an error | Preserve sanitized diagnostics and the immutable candidate identity; do not retry automatically |
| Outcome is uncertain | Do not resubmit; reconcile the original attempt through the central workflow |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input blocked | Required package, scope, or field evidence is absent or invalid | Correct the request or evidence and revalidate |
| Dependency blocked | A prerequisite is unresolved | Resolve the documented prerequisite before preview |
| Design blocked | A safety or governance rule fails | Correct the design contract before preview |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before any candidate import | Exact task, target scope, immutable preview identity, blockers, and required approval boundary |
| On failure | Failure class, sanitized diagnostics reference, and safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing field semantics | Do not infer a value, default, reference lookup, lifecycle operation, or direct-write endpoint |
| Failed or uncertain import | Do not automatically retry or resubmit |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PAYOPT.VALIDATE_INPUT | step | 10 | validate_input | valid->PAYOPT.CHECK_DEPENDENCIES;invalid->PAYOPT.INPUT_BLOCKED | none | stop | Always |
| PAYOPT.CHECK_DEPENDENCIES | step | 20 | resolve_dependency | ready->PAYOPT.ENFORCE_DESIGN;blocked->PAYOPT.DEPENDENCY_BLOCKED | PAYOPT.VALIDATE_INPUT | stop | Always |
| PAYOPT.ENFORCE_DESIGN | step | 30 | design_enforcement | pass->PAYOPT.EXECUTION_GATE;blocked->PAYOPT.DESIGN_BLOCKED | PAYOPT.CHECK_DEPENDENCIES | stop | Always |
| PAYOPT.EXECUTION_GATE | step | 40 | execution_gate | approved_preview->PAYOPT.READY_FOR_DATA_LOADER;not_ready->PAYOPT.EXECUTION_BLOCKED | PAYOPT.ENFORCE_DESIGN | stop | A governed execution request exists |
| PAYOPT.INPUT_BLOCKED | terminal | 50 | terminal | none | none | stop | Input validation fails |
| PAYOPT.DEPENDENCY_BLOCKED | terminal | 60 | terminal | none | none | stop | Dependency readiness fails |
| PAYOPT.DESIGN_BLOCKED | terminal | 70 | terminal | none | none | stop | Design enforcement fails |
| PAYOPT.EXECUTION_BLOCKED | terminal | 80 | terminal | none | none | stop | Execution approval or preview is absent |
| PAYOPT.READY_FOR_DATA_LOADER | terminal | 90 | terminal | none | none | stop | A governed immutable preview and approval are available |
