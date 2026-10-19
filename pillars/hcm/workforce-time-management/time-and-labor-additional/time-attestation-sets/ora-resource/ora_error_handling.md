# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Fresh same-task export cannot be obtained or validated | Stop before package preparation and preserve the redacted validation evidence. |
| FSM evidence does not prove the import route | Stop and rebuild only after the route is documented by a fresh export. |
| An update ZIP includes another set, omits an existing child row without an approved removal, or changes an existing child outside scope | Stop before Core Data Loader handoff and rebuild the ZIP with the selected parent and complete reconciled child collection. |
| Core Data Loader reports a missing or stale preview or approval | Return the exact validated ZIP to Core Data Loader; do not create a task-local preview or approval prompt. |
| A populated attestation row has a blank or invalid Display Level | Stop before Core Data Loader handoff; require Day, Detail, or Time Card. |
| Complete Business Summary is missing, incomplete, or includes technical or unverified content | Stop before Core Data Loader handoff and regenerate the business-only summary from verified structured values. |
| Validated ZIP link is missing or displayed before the summary and defaults | Stop before Core Data Loader handoff; show the Complete Business Summary, Defaults Applied, then the direct validated ZIP link. |
| Import fails, partially succeeds, times out, or is uncertain | Preserve redacted diagnostics, reconcile current state through the documented read or fresh-export path, and stop. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required export, ZIP shape, keys, or approved row scope is absent or invalid | Correct the source evidence or rebuild; do not submit. |
| Catalog mismatch | The effective catalog remains UNKNOWN or conflicts with package evidence | Record the mismatch and stop pending confirmed routing guidance. |
| Approval blocker | Core Data Loader reports that its preview or approval is missing, stale, or does not identify the current package | Return to the Core Data Loader workflow. |
| Summary disclosure | The business-only summary or validated ZIP ordering is incomplete | Regenerate the required disclosure before Core Data Loader handoff. |
| Process failed | Import reports failure, partial success, timeout, or uncertain completion | Preserve diagnostics, reconcile, and stop without automatic retry. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Core Data Loader handoff | The exact validated FSM ZIP and the completed task-local validation result. |
| Before Core Data Loader approval | The Complete Business Summary and Defaults Applied, followed immediately by a direct link to the exact validated ZIP. |
| Import outcome | Result status, elapsed wait, available process identifiers, redacted diagnostics, and reconciliation result. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Route is not proven | Do not substitute REST, HCM Data Loader, or another import mechanism. |
| Import outcome is failed, partial, timed out, or uncertain | Do not automatically retry or submit another package. |
| A Complete Business Summary is presented | Do not expose IDs, codes, keys, internal identifiers, opaque links, request IDs, fingerprints, REST fields, API paths, methods, payload fields, DAT columns, directives, discriminators, database columns, resolver names, rule IDs, task-node names, internal statuses, technical file names, raw Boolean values, warnings, diagnostics, or technical notes. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAS_CORE_DATA_LOADER_HANDOFF | step | 50 | execution_gate | handed_off->TAS_INPUT_READY;blocked->RETURN_ISSUES | TAS_ENFORCE_FIELDS | stop | The exact validated FSM ZIP is handed to Core Data Loader, which owns immutable preview, approval, and submission |
| TAS_INPUT_READY | terminal | 60 | terminal | none | TAS_CORE_DATA_LOADER_HANDOFF | stop | Task-local validation completed; Core Data Loader owns the remaining import lifecycle |
| RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | Validation, lookup, defaulting, package enforcement, or Core Data Loader handoff cannot proceed |
