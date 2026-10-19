# Shifts and Schedules Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Filled workbook template or Work Schedules sheet is missing, unreadable, or incomplete | Stop before preview and identify the missing worksheet, row, or field. |
| A design rule blocks the proposed schedule, shift, absence, holiday, or capacity change | Return the exact SS rule ID, blocking condition, and correction allowed before preview. |
| A parent work schedule or shift lacks its documented identity/body fields, or an item lacks `itemId`, conditional `shiftLabel` or `nonWorkingReasonLabel`, or required repeat values | Classify as input validation and do not construct or send a REST request. |
| REST authentication or authorization fails during an approved read | Stop and report auth/authz; one cached-token refresh is allowed only for a read. |
| REST transport, API, process, or timeout failure occurs | Preserve redacted diagnostics and do not retry POST, PUT, PATCH, DELETE, or import without idempotency and explicit approval. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Workbook intake, schedule, or shift data is missing or invalid | Correct the identified workbook data and rerun validation. |
| Approval blocker | A design rule fails, REST execution contract is incomplete, or live approval is absent | Correct the design or provide the missing contract and approval; do not execute. |
| Auth/authz | An approved read is denied | Verify environment identity and privileges before one safe read retry. |
| Transport/environment | A supported endpoint cannot be reached | Check connectivity and retry only a known idempotent read. |
| Fusion API | A supported Oracle REST call returns an error | Preserve redacted response evidence and correct the request; do not automatically retry a write. |
| Process timeout | A process remains nonterminal beyond its declared wait | Report task code, process or request ID, last status, elapsed wait, and next-check path; do not resubmit. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation result | Workbook sheet and rows assessed, rule IDs evaluated, blocking conditions, and allowed corrections. |
| REST preview | Target environment, exact method and endpoint, immutable payload or import artifact, identity rule, expected impact, and approval fingerprint. |
| Failure | Failure class, stage, task code, redacted evidence, external IDs when available, and recommended action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Workbook or design validation fails | Do not preview, import, or execute. |
| Documented parent or work-schedule item fields, current-state baselines, or live approval are missing | Do not infer identifiers or payload values, and do not POST, PUT, DELETE, or import. |
| Write outcome is uncertain | Do not replay the write; reconcile with a supported read-only contract first. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SS.HANDLE_ERROR | step | 50 | error_handler | handled->SS.RETURN_ISSUES | none | stop | Any input, design, approval, auth, transport, API, process, or timeout failure |
| SS.READY | terminal | 60 | terminal | none | SS.LOOKUP_CURRENT_SHIFT_ITEMS | continue | Workbook, selected execution direction, design validation, and required REST baseline lookup passed; execution still requires its route-specific preview and approval gate |
| SS.RETURN_ISSUES | terminal | 70 | terminal | none | none | continue | A blocking issue was classified and disclosed |
