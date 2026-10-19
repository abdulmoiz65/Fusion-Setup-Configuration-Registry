# Manage Predefined Links Error Handling

Sources: Confluence page 21736675148, Manage Predefined Links — ORA_IRC_EMP_CAMP_DEEP_LINKS; user-requested FSM export-and-inspect query route.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Active status filter is missing | Stop before export planning and require the filter |
| Task code or CSV export support does not resolve | Stop before creating an export process |
| Export context is missing | Stop and request the target environment and project workspace |
| FSM export fails or times out | Preserve process diagnostics and do not start another export automatically |
| Downloaded archive lacks readable task CSV metadata or rows | Report the artifact persistence or archive-shape failure and do not count links |
| Exported status field or Active representation cannot be established from the content | Report the headers and observed values; do not invent a count |
| Activation or rename target is zero or multiple Draft rows | Stop before archive preparation and require an exact unique target |
| Mutation archive differs from the reviewed baseline except for the approved field | Stop before upload and rebuild the archive |
| Data Loader submission is uncertain | Do not submit again; inspect the resulting import status before another attempt |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Status filter or export context is missing | Supply the missing query input or context |
| Catalog mismatch | Exact task or CSV export support does not resolve | Correct task context before export |
| Process failed | Fusion export process fails or times out | Preserve ProcessId, status, and log; wait for an explicit retry request |
| Artifact persistence | ZIP or extracted CSV cannot be inspected | Report the artifact path and failure |
| Verification blocker | Status field or Active representation is not observable in the exported content | Preserve header/value evidence and obtain the export schema |
| Approval blocker | Immutable activation or rename archive is not previewed and freshly approved | Present the exact archive SHA-256 and await confirmation |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before export | Environment, task code, query filter, project export destination, and read-only scope |
| Before activation or rename import | Exact target row, current ORA_DRAFT status, requested field change, archive path, SHA-256, environment, and post-import verification method |
| After export | ProcessId, final process status, archive path, and inspected CSV metadata/header evidence |
| On successful count | Status field and Active representation used, matching row count, and archive reference |
| When blocked | Failure class, affected stage, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A link-count query is requested | Do not create, import, activate, inactivate, or call undocumented internal services |
| Export outcome is uncertain | Do not automatically create another export process |
| CSV schema is unknown | Do not assume a status column name or status code |
| Activation or rename is requested | Do not upload or initiate the FSM archive until the Data Loader immutable preview is freshly approved |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPL.EXPORT_GATE | decision | 5 | execution_gate | evidence_available->MPL.EVALUATE_EXPORT_RESULT;blocked->MPL.HANDLE_ERROR | MPL.ENFORCE_EXPORT_SCOPE | stop | A current FSM export archive and process evidence are available for inspection |
| MPL.HANDLE_ERROR | step | 14 | error_handler | disclosed->MPL.RETURN_ISSUES | none | stop | Input, catalog, export, archive, or verification behavior is blocked |
| MPL.RETURN_SUCCESS | terminal | 12 | terminal | none | MPL.EVALUATE_EXPORT_RESULT | stop | Current active-link count is derived from inspected export evidence |
| MPL.RETURN_ISSUES | terminal | 15 | terminal | none | MPL.HANDLE_ERROR | stop | A blocked export query or mutation result is disclosed |
| MPL.MUTATION_GATE | decision | 10 | execution_gate | preview_ready->MPL.EVALUATE_MUTATION_RESULT;blocked->MPL.HANDLE_ERROR | MPL.ENFORCE_MUTATION_SCOPE | stop | An immutable activation or rename archive has an exact Data Loader preview and fresh approval |
| MPL.RETURN_MUTATION_SUCCESS | terminal | 13 | terminal | none | MPL.EVALUATE_MUTATION_RESULT | stop | The exact Draft-link activation or rename import is verified |
