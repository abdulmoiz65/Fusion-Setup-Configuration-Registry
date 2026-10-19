# Manage Expense Report Templates Error Handling

## Failure Handling

| Situation | Failure Class | Handling |
|---|---|---|
| Missing/invalid value or contradictory document values | input_validation | Show object, field, source cell/page, value, constraint and correction; retain accepted values and resume the selected chat/Excel medium |
| Missing or unsupported CSV field/member/relationship | catalog_mismatch | Identify the exact unsupported field; do not silently drop it or claim packaging is complete |
| Authentication/privilege failure | auth/authz | Follow core authentication policy; refresh cached-token 401/403 once where allowed; never print credentials |
| Endpoint, connectivity or target mismatch | transport/environment | Preserve redacted evidence and stop; no alternate route |
| Rejected request | Fusion API | Retain response summary and ECID when available; do not replay a mutation |
| Requested status retrieval times out | process_timeout | Retain the returned Request ID and last known status; stop and report the retrieval failure; never resubmit or reuse the baseline ProcessId |
| Import completes with errors or reviewable warnings | process_failed | Use Data Loader status/error retrieval and available FSM ProcessLogs; disclose affected records and allow correction; preserve partial successes |
| Candidate/review/contract cannot be persisted or output already exists | artifact_persistence | Stop before live submission and use a valid new versioned path |
| Exact import approval is absent or stale | approval_blocker | Present the final ZIP, CSV review and delta; request approval only after validation passes |

A transient read-only result/artifact retrieval may receive one bounded retry,
including a transient 404 before recording a report as unavailable. Do not
automatically re-submit an export or import. Do not label a true completion
flag without terminal result evidence as import success or failure.
An accepted load still running is normal in-progress state, not a timeout or
failure. Check it only on an explicit subsequent status/results request.

## Correction and Resume

For partial intake, keep accepted values and return only the unresolved gaps.
For a rejected candidate, apply corrections, revalidate, refresh the baseline
where state may have changed, and regenerate the ZIP/review/preview. Prior
approval is invalid after any material change.

For failed or partially successful imports, retrieve and explain available
diagnostics, reconcile actual state with a fresh export, preserve successful
records, and build only remaining intended changes. An already-created record
must not be submitted again as a create. Show the corrected package for new
approval. Do not require restarting all intake or reselecting the medium.

Report success only from terminal import evidence; distinguish accepted
initiation, import completion, and post-import verification. Return the core
helper's Markdown unchanged. Retain the loader Request ID separately from the
baseline and verification export ProcessIds. On verification mismatch, retain
evidence and return to correction; there is no automatic rollback.

## Review and Execution Boundary

Before approval, link the actual ZIP, raw CSV files, CSV review workbook and
exact delta with the target and TaskCode. A contextual affirmative approves
only those bytes. Require Data Loader persisted preflight before Task Hook,
then approve and verify its retained preview. Submit through Data Loader with
both `--approved-preflight-envelope` and `--task-validation-envelope`; do not
call the shared task-level importer. Do not require duplicate approval or
rerun business validation after approval. Keep envelope paths and hashes internal.

The graph's READY_IMPORT terminal hands off to the manifest's explicit
submission procedure and later requested status/verification procedure. It does
not mean import success. Accepted initiation ends the current load request
without polling; later status requests use the loader's returned Request ID.
During Task Hook validation, this gate is recorded as pending external
approval; it must not execute submission or recursively validate itself.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EXMERT.REVIEW_APPROVAL | step | 11 | execution_gate | approved->EXMERT.READY_IMPORT;modify->EXMERT.NEEDS_CORRECTION;pending->EXMERT.AWAITING_APPROVAL | EXMERT.VALIDATE_CANDIDATE | stop | All values and exact ZIP passed validation; let implementor review every CSV and approve the immutable import |
| EXMERT.READY_IMPORT | terminal | 12 | terminal | none | EXMERT.REVIEW_APPROVAL | stop | Exact approval received; submit once through Data Loader with persisted preflight and verified Task Hook envelope; stop on acceptance; check results only on a later explicit request |
| EXMERT.NEEDS_INPUT | terminal | 13 | terminal | none | none | stop | Retain base values, source selections and medium; ask only for missing input |
| EXMERT.NEEDS_CORRECTION | terminal | 14 | terminal | none | none | stop | Retain accepted values, show actionable issues, accept corrections and revalidate |
| EXMERT.AWAITING_APPROVAL | terminal | 15 | terminal | none | none | stop | Retain final ZIP and complete CSV review while awaiting exact-artifact import approval |
| EXMERT.BLOCKED | terminal | 16 | terminal | none | none | stop | Retain diagnostics for the failed preflight, baseline, route, build, import or verification step |
