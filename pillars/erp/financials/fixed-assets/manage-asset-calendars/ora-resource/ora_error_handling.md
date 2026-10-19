# Manage Asset Calendars: Error Handling

## Error Situations

Use the named [Failure Classes](#failure-classes) for recovery. Apply
[Disclosure Rules](#disclosure-rules) and [Refusal Rules](#refusal-rules) to every
situation below.

| Situation | What Should Happen |
|---|---|
| Transport/API failure during an authorized read-only lookup | Apply the Transport/environment recovery in [Failure Classes](#failure-classes). |
| Standard Fusion REST ledger or period lookup is unavailable, incomplete, or ambiguous | Record the sanitized REST result, then request a current same-target export owned by the applicable General Ledger setup task for the ledger-period evidence. Do not probe unverified alternate endpoints; do not use a Fixed Assets export as the ledger-period substitute. |
| A configuration-equivalent calendar exists under a different name | Report each exact calendar name and the fiscal year, periods-per-year, and period-coverage comparison. Stop before Design Preview or ZIP creation until the user chooses reuse or explicitly requests a duplicate. |
| One ledger in a multi-ledger request already exists or differs | Report the exact ledger, calendar, and comparison result. Isolate that track as already complete or awaiting an update-or-new decision; continue validation for unaffected tracks. |
| One complete existing calendar differs from the proposal | Show the exact differing fields and periods, then ask the customer to choose update or create new. Do not treat this as an unresolved lookup. |
| Existing-calendar lookup is multiple, incomplete, unavailable, or has incomplete period rows | Treat the state as unresolved and stop before an update-or-new decision, ZIP preparation, or import. |
| Bulk input has invalid rows | Return a row-level exception report and exclude only the invalid rows from package preparation. Preserve their input keys and validation failures. |
| A bulk batch fails or times out | Apply the Import process recovery in [Failure Classes](#failure-classes). Also preserve the batch manifest, immutable archive identity, and process details; do not resubmit the failed batch or infer success for any dependent period rows. |
| Authentication 401/403 during an authorized read-only lookup | Apply the Authentication recovery in [Failure Classes](#failure-classes). |
| OAuth token expired or login callback did not complete | Record only environment, expiry/callback outcome, and next sign-in action; refresh authentication before polling an existing process, and do not submit a duplicate export without an identified process. |
| Package/member/header/metadata mismatch | Apply the Artifact persistence or Catalog mismatch recovery in [Failure Classes](#failure-classes). |
| FSM CSV parser rejects a row or its field count differs from the header | Apply the Artifact persistence recovery in [Failure Classes](#failure-classes). Report the member, row, expected and actual field counts, and rebuild the affected rows from the exported header. |
| Import timeout or failure | Apply the Import process recovery in [Failure Classes](#failure-classes). |
| Import accepted or related job succeeded but the requested asset calendar is not visible | Apply the Target-state verification failure recovery in [Failure Classes](#failure-classes). Capture the Data Loader request ID, completed FSM process log, and exact requested calendar name. |
| Terminal-successful FSM process but requested calendar fields remain unchanged | Apply the Target-state verification failure recovery in [Failure Classes](#failure-classes). Preserve the immutable archive fingerprint, completed FSM process log, and pre/post target-state evidence. |
| Data Loader/wrapper and setup-task statuses disagree | Apply the Conflicting process status recovery in [Failure Classes](#failure-classes). |
| Post-import FSM process result is pending or times out | Apply the Import process recovery in [Failure Classes](#failure-classes); do not submit a duplicate import or infer that the import failed. |

## Failure Classes

| Failure class | Safe next action |
|---|---|
| Input validation | Return to [ora_input_validation.md](ora_input_validation.md), identify every missing or invalid business value together, and revalidate. |
| Lookup evidence | Return to [ora_reference_lookups.md](ora_reference_lookups.md), retain sanitized diagnostics, and stop until complete target evidence is available. |
| Dependency | Return to [ora_dependency_readiness.md](ora_dependency_readiness.md) and resolve the blocking prerequisite. |
| Design enforcement | Return to [ora_design_enforcement.md](ora_design_enforcement.md) and correct the rejected design. |
| Approval | Keep the immutable archive in review state until explicit approval is received. |
| Import process | Report the task, target environment, process or request ID, last status, elapsed time, and safe next-check path; retain sanitized diagnostics. |
| Transport/environment | For a nonauthentication read-only lookup failure, record sanitized diagnostics and stop before retry. |
| Authentication | For a 401/403 on an authorized read-only lookup, refresh the cached token once and repeat only that lookup. If it still fails, record sanitized diagnostics and stop. |
| Artifact persistence | Stop before preview when package member, header, metadata, or CSV row shape is invalid; reacquire the validated export and rebuild the smallest delta. |
| Catalog mismatch | Stop before preview when a CSV code differs from export metadata; correct to the supported code. |
| Target-state verification failure | The completed FSM process log reports relevant errors, or live target-state evidence does not contain the exact requested calendar or expected material fields. Preserve import, process-log, and target-state comparison evidence, including the scenario-specific details from [Error Situations](#error-situations) and the [post-import disclosure](#disclosure-rules). Resolve the live target-state comparison before any retry decision. |
| Conflicting process status | Treat the import as unresolved rather than succeeded or failed solely from either status. Preserve both statuses, escalate the request-ID/status correlation to the owning Data Loader/FSM team, and require target-state verification before any retry decision. |

## Disclosure Rules

| Situation | What must be shown |
|---|---|
| Pre-import block | Failure class, concise business explanation, owner resource, and next safe action. |
| Import result | Archive identity, target, process or request ID, terminal status, and created, skipped, warned, or failed counts when available. |
| Lookup failure | Environment, read-only purpose, failure class, sanitized message, and next action. |
| Post-import verification | Immutable archive fingerprint, requested calendar name and scope, import/process-log identifiers when available, live target-state comparison, and retry-approval state. |

## Refusal Rules

| Situation | What must not happen |
|---|---|
| Unresolved validation, lookup, dependency, or design rule | Do not prepare or submit an import. |
| Missing approval | Do not submit a live import. |
| Failed, pending, or timed-out import | Do not alter defaults by trial and error or automatically resubmit. |
| Submitted import without verified matching target state | Do not report the asset calendar as created solely because an archive was accepted or a related job succeeded; do not automatically resubmit a target-state verification failure. |
| Conflicting or pending process states | Do not cancel, resume, or resubmit until the exact target-state result or an approved recovery decision is available. |
## Parent Import Handoff

After `core.data-loader` accepts the exact approved immutable FSM package, report **accepted — pending parent verification** and hand off the archive identity and request ID to the Fixed Assets parent. The parent owns status monitoring, FSM ProcessLog review, fresh target-state read-back, and any dependent-task progression. This child skill must not poll the request, declare the calendar complete, or start a dependent task from the accepted state.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CAL.IMPORT_GATE | decision | 60 | execution_gate | approved->CAL.HANDED_OFF_TO_PARENT;blocked->CAL.HANDLE_APPROVAL | CAL.ENFORCE_DESIGN | stop | A reviewed package is proposed for import. |
| CAL.HANDED_OFF_TO_PARENT | terminal | 170 | terminal | none | CAL.IMPORT_GATE | continue | Calendar import is accepted — pending parent verification. |
