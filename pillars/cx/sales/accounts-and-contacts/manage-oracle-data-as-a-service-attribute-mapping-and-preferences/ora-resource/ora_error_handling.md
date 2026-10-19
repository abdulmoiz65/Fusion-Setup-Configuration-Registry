# Error Handling

Classify failures without exposing credentials or replaying an uncertain FSM
submission. Preserve every server-issued process identifier for status-only
continuation.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Seeded catalog validation fails | Stop before package preparation and report the failed manifest, hash, schema, row-count, or uniqueness check |
| Requested row is absent or duplicated | Stop and report the exact composite key; do not choose a similar row |
| Fusion attribute metadata is unavailable or incomplete | Stop before package preparation; report the sanitized target, exact object, response completeness evidence, and required read privilege without falling back to a static list |
| Fusion object or attribute is invalid | Stop and report the selected key plus exact effective object/attribute pair; do not suggest or select a similar attribute automatically |
| User asks for display during real-time enrichment | Explain that **Display During Real-time Enrichment** is separate from **Don't Apply Blank Values** and **Don't Overwrite**; do not infer a substitute FSM field |
| Fresh export fails or times out | Preserve TaskCode, ProcessId, last status, elapsed time, ZIP or ProcessLog path, and status-only continuation |
| Package preparation fails | Stop before Data Loader preview and report the member, row key, field, or ZIP safety check |
| Approval-bound ZIP or preview changes | Invalidate approval and rebuild validation plus the Data Loader preview |
| Import response is uncertain | Do not resubmit; reconcile read-only with the captured process identifier or request window |
| Import fails or times out | Preserve target, TaskCode, ProcessId, last status, elapsed time, and ProcessLog when available; do not retry automatically |
| Post-import verification differs | Report the exact key, field, expected value, observed value, and import ProcessId without another mutation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Change document, baseline, ZIP, metadata, schema, row key, field, or fingerprint is invalid | Correct the exact input and rebuild the preview |
| catalog_mismatch | Fixed task identity or CSV members differ from the local catalog | Stop and review the task/source asset; do not infer a substitute |
| catalog_mismatch | Live object metadata is incomplete or an effective object/attribute pair has no exact match | Correct the pair or metadata-access gap and rerun fresh discovery |
| auth_authz | Authentication remains invalid after one permitted refresh or privileges are denied | Reauthenticate or obtain required access, then start with a fresh preview |
| transport_environment | Network, host, or response certainty fails | Reconcile read-only; require fresh approval before any new mutation |
| fusion_api | Fusion rejects export/import process creation or result retrieval | Preserve sanitized response details and ECID when available |
| process_timeout | Existing process is nonterminal at the polling deadline | Stop polling and offer status-only continuation for the same ProcessId |
| process_failed | Fusion reports terminal errors | Retrieve ProcessLog/result and correct the reported issue |
| artifact_persistence | Required ZIP, preview, result, log, or run record cannot be written | Stop and repair the exact project path before continuing |
| approval_blocker | Data Loader approval is absent, stale, or mismatched | Present one fresh immutable preview through Data Loader |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before export approval | Source environment, fixed task name/code, unfiltered scope, output path, and one-process impact |
| Before Data Loader import approval | Target environment, selected keys and fields, before/after values, ZIP path, SHA-256, validation result, and task name/code |
| Process accepted | Environment, operation, task code, ProcessId, and current status |
| Timeout or terminal failure | Environment, operation, task code, ProcessId, last status, elapsed time, failure class, diagnostic path, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing exact key or allowlisted fields | Do not infer a row or field from a display label or similar name |
| Display During Real-time Enrichment request | Do not treat it as **Don't Apply Blank Values** or **Don't Overwrite**, and do not place it in the FSM change document |
| New row, deletion, reset, or whole-baseline request | Do not build or submit a package |
| Unrequested rows are present | Do not use a whole export or full seeded catalog as the import payload |
| Approval is missing or stale | Do not invoke the Data Loader-owned import action |
| An import outcome is uncertain | Do not replay the request before status reconciliation |
| Sensitive values are present | Do not print or persist tokens, credentials, authorization headers, or raw environment-specific source metadata |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| DAAS.APPROVAL | decision | 5 | execution_gate | approved->DAAS.READY;declined->DAAS.ISSUES | DAAS.ENFORCE_SELECTED_ROWS | stop | Exact Data Loader preview is ready for one import approval |
| DAAS.READY | terminal | 6 | terminal | none | DAAS.APPROVAL | continue | Validation and Data Loader approval are complete |
| DAAS.ERROR | step | 7 | error_handler | handled->DAAS.ISSUES | none | continue | Validation, dependency, lookup, enforcement, export, package, import, verification, or persistence fails |
| DAAS.ISSUES | terminal | 8 | terminal | none | none | continue | Request has unresolved inputs, approval, execution, verification, or persistence issues |
