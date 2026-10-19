# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Core Data Loader or Fusion rejects the requisitioning BU | Stop and request one exact requisitioning BU identity; do not infer a replacement BU |
| Core Data Loader preflight or approval binding fails | Stop before upload; correct the source or approval context and restart the required validation cycle |
| Import fails | Preserve the returned diagnostics and do not retry upload or initiation without fresh validation and approval |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Scope is ambiguous | Do not default to All Business Units or choose a BU |
| Core Data Loader workflow is incomplete | Do not construct a direct REST payload, upload, or initiate a mutation outside `core.data-loader` |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPPAD.EXECUTION_GATE | decision | 5 | execution_gate | ready->EPPPAD.DONE;blocked->EPPPAD.HANDLE_ISSUES | EPPPAD.ENFORCE_DESIGN | stop | Before preview or import |
| EPPPAD.HANDLE_ISSUES | step | 98 | error_handler | handled->EPPPAD.FAILED | none | stop | Any validation, dependency, or enforcement failure |
| EPPPAD.DONE | terminal | 6 | terminal | none | EPPPAD.EXECUTION_GATE | stop | Readiness is complete |
| EPPPAD.FAILED | terminal | 99 | terminal | none | EPPPAD.HANDLE_ISSUES | stop | Failure is disclosed |
