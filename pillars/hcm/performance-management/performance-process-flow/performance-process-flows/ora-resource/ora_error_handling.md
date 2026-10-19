# Performance Process Flows Error Handling

Apply this task guidance using current target metadata and the declared execution route.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required field, date, status, boolean, or fixed-value validation fails | Stop before the write, report the invalid field or combination, and correct the request. |
| A request, approval, or import artifact asks to bypass a conditional flag relationship | Apply the documented reset if one exists, then re-evaluate the invariant. Stop before preview, approval, import, or mutation if the payload remains contradictory; do not waive the rule. |
| A duplicate name overlaps effective dates in the same business group | Stop; select the existing flow or change the name or effective period. |
| An in-use flow changes DateFrom or a guarded configuration value | Stop; preserve the current value unless a separately approved service contract authorizes the change. |
| A request includes taskNames or an EFF/DFF child collection | Stop; taskNames is read-only in this REST resource and no EFF/DFF child resource is declared. |
| A feature-gated flag has no matching profile value or its ProfileOptionValue is not Y | Stop before the write and clear the affected feature-gated flag or enable its feature. |
| A task-role TaskCode has no unique process-task definition | Stop before the import; correct the TaskCode and rebuild the task-role rows from the read-only lookup. |
| A task-role name mapping violates the MGREVAL exception | Stop before the import; populate both name fields for every code except MGREVAL, and populate only MgrTaskName for MGREVAL. |
| Worker document acknowledgement incorrectly enables review meetings | Stop before approval or import; set ConductMeetingsFlag and WkrAckReviewMtgFlag to N unless the user explicitly requested those review-meeting behaviors. |
| Fusion rejects FinalFeedbackFlag | Stop before approval or import; set FinalFeedbackFlag to N. Retain requested worker and manager final-feedback behavior only in WkrFinalFeedbckFlag and MgrFinalFeedbackFlag. |
| An FSM CSV member uses blanket quoting | Stop before approval or import; remove quotes from headers and values that do not require CSV escaping, preserve quotes only for values containing a comma, double quote, carriage return, or line feed, then rebuild and revalidate the ZIP. |
| REST DELETE is requested | Stop; the resource explicitly disables delete. |
| A POST, PATCH, SOAP CRUD, or import request fails or has uncertain completion | Do not retry automatically; preserve the sanitized response and reconcile the state through an authorized read-only lookup. |
| Migration import reports processing status or exceptions | Stop and preserve the migration processing status before deciding on a corrected import. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A request violates field, payload, or cross-field constraints. | Correct the request and validate again. |
| Dependency readiness | An existing identity, profile feature state, template period, or child-service route is unresolved. | Resolve the documented dependency; a feature-gated flag requires its profile value to be Y. |
| Design blocker | A documented business, in-use, or REST-route restriction applies. | Correct the design or select the documented alternate route. |
| Fusion API | The REST service returns an error for a submitted request. | Preserve sanitized response evidence; do not replay a mutation automatically. |
| Process failed | Migration import returns processing status or an exception. | Preserve status and correct the source data before an approved retry. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before POST or PATCH | Exact target, normalized writable fields, lookup results, blocked dependencies, and current approval for the intended mutation. |
| After a failed REST or migration operation | Failure class, sanitized response or processing status, side-effect uncertainty, and a safe reconciliation action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| DELETE or taskNames REST mutation is requested | Do not call the disabled DELETE route or invent a writable child REST contract. |
| Feature profile value is missing, ambiguous, or not Y | Do not enable the associated CalendarInviteFlag or AllowShareLockForCalib. |
| A write has an uncertain result | Do not automatically retry it. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_PROCESS_FLOWS.STOP_INVALID | terminal | 70 | terminal | none | none | stop | Input validation fails. |
| PERFORMANCE_PROCESS_FLOWS.STOP_DEPENDENCY | terminal | 80 | terminal | none | none | stop | A required dependency or lookup is unresolved. |
| PERFORMANCE_PROCESS_FLOWS.STOP_DESIGN | terminal | 90 | terminal | none | none | stop | A documented invariant, design, or route restriction applies. |
| PERFORMANCE_PROCESS_FLOWS.DONE | terminal | 100 | terminal | none | PERFORMANCE_PROCESS_FLOWS.ENFORCE | stop | Validation, dependencies, lookups, invariant checks, and design checks pass. |
