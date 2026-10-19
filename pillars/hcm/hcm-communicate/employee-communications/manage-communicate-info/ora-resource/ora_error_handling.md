# Manage Communicate Info Error Handling

This executable error-handling scope covers campaign-number FSM CSV export and import through the routed Data Loader workflow.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Campaign Number Generation Method is missing or unsupported | Stop before archive preparation and require Automatic or Manual |
| Campaign Number Starting Value fails ^[1-9][0-9]*$ | Reject the blank, zero, negative, signed, decimal, whitespace-containing, or non-numeric value before archive preparation and retain the current value |
| The FSM archive is invalid or differs from the reviewed archive | Stop before upload and rebuild the immutable preview from the current export |
| Fusion rejects upload or import initiation | Report the failed stage and returned diagnostic; do not retry automatically |
| Import initiation result is uncertain | Do not submit again until a fresh task-level CSV export establishes the current value |
| Task-level CSV readback does not match the requested generation method | Report the current and requested values; do not prepare another change without a new preview and approval |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | The generation method is missing or unsupported, or a supplied starting value is invalid | Correct the input and rerun validation |
| Catalog mismatch | The task does not resolve exactly once or CSV export/import support is not Y | Stop and correct the catalog or task selection |
| Approval blocker | The exact environment, operation, archive, SHA-256, or explicit approval is missing or stale | Regenerate the immutable preview and obtain explicit approval |
| Fusion API | Fusion rejects the UCM upload or import initiation | Preserve the returned diagnostic and correct the documented cause before a new approved attempt |
| Process failed | The FSM import process reports failure when status is explicitly requested | Retrieve the ProcessLog, disclose the failure, and require a new preview before retry |
| Verification blocker | A fresh task-level CSV export is unavailable or does not match the requested value | Report the unverified boundary and do not retry automatically |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before upload and import initiation | Exact target environment, task code, current and proposed values, immutable archive path, SHA-256, and the requirement for explicit approval |
| After accepted initiation | Data Set Name, Content ID, and Request ID returned by Fusion; do not poll automatically |
| During requested verification | Current generation-method backing value and starting value from a fresh task-level CSV export |
| When a failure blocks continuation | Failure class, failed stage, safe next action, and available process diagnostic without credentials or token content |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Campaign-number mutation is requested | Do not call internal ADF DataControl operations; use the task-routed FSM Data Loader workflow |
| The archive or approval no longer matches | Do not upload; generate a new immutable preview and approval |
| A live mutation has an uncertain outcome | Do not retry until task-level CSV readback establishes the current value |
| Only the generation method is requested to change | Do not modify the starting value or any other configuration |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCI.EXECUTION_GATE | decision | 6 | execution_gate | evidence_available->MCI.EVALUATE_RESULT;blocked->MCI.HANDLE_ERROR | MCI.ENFORCE_DESIGN | stop | An exact immutable FSM archive and its current approval or verification evidence are evaluated |
| MCI.HANDLE_ERROR | step | 8 | error_handler | disclosed->MCI.RETURN_ISSUES | none | stop | Any required input, dependency, design, approval, execution, or verification condition is blocked |
| MCI.RETURN_SUCCESS | terminal | 9 | terminal | none | MCI.EVALUATE_RESULT | stop | The routed FSM action or requested readback completed with the required source-backed evidence |
| MCI.RETURN_ISSUES | terminal | 10 | terminal | none | MCI.HANDLE_ERROR | stop | One or more blockers prevent safe completion |
