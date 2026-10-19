# Courses Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| New-child eligibility or exclusivity is unavailable | Block only rows that add or replace a child; preserve unaffected valid rows |
| Person, instructor, facilitator, lifecycle, assignment, lookup, or approval evidence is unresolved | Stop the affected row before mutation and identify the exact gate |
| Instructor serialization is not authoritative | Stop that default-instructor mutation; do not derive it from read-only details |
| A row or current-state fingerprint changes after preview | Invalidate approval and rebuild the affected preview |
| A write outcome is uncertain | Do not retry; reconcile through the confirmed read route first |
| A documented change request times out | Return the operation, sanitized process identity, last status, elapsed time, and next-check guidance |
| Readback differs from the approved preview | Report partial or failed verification without claiming success |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required input, approval, person, resource, live value, assignment impact, or documented lookup is unavailable | Supply or resolve the named blocker |
| UNSUPPORTED | Parent/activity delete, user-facing upsert, or child mutation without eligibility evidence is requested | Select a supported operation or defer the affected row |
| FAILED | Validation, execution, polling, or verification fails | Review sanitized diagnostics before another attempt |
| ALL_GOOD | Approved Course rows and their readback are verified | Return row-specific results and the completed run record |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before mutation | Exact environment, course identity or create key, operation, selected rows, defaults and relationship effects, preview fingerprint, and approval status |
| On failure | Failure class, affected row, current rule, sanitized evidence, verified side effects, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval is absent or stale | Do not call POST, PATCH, copy, lifecycle, activity, or Data Loader write routes |
| A new child lacks eligibility or exclusivity evidence | Do not treat current activities or a submitted label as proof |
| Instructor serialization is absent | Do not manufacture courseDefaultInstructors from readback details |
| Parent delete, activity delete, or user-facing upsert is requested | Do not expose or invoke it |
| A live value or target DFF segment is absent | Do not infer it |
| A fingerprint exists | Do not describe it as ETag, If-Match, or atomic concurrency protection |
| A write result is uncertain | Do not automatically replay the write |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CRS.EXECUTION_GATE | decision | 6 | execution_gate | evidence_available->CRS.EVALUATE_RESULT;blocked->CRS.HANDLE_ERROR | CRS.ENFORCE_DESIGN | stop | A validation-only result or exact approved row set is ready for evaluation |
| CRS.HANDLE_ERROR | step | 8 | error_handler | disclosed->CRS.RETURN_ISSUES | none | stop | A Course row is blocked by validation, dependency, lookup, design, approval, execution, timeout, or verification |
| CRS.RETURN_SUCCESS | terminal | 9 | terminal | none | CRS.EVALUATE_RESULT | stop | Every selected valid row is verified and row-specific results are available |
| CRS.RETURN_ISSUES | terminal | 10 | terminal | none | CRS.HANDLE_ERROR | stop | One or more Course rows cannot safely complete |
