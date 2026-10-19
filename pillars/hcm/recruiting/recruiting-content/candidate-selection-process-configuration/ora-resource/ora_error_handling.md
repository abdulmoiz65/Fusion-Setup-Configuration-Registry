# Candidate Selection Process Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required process, phase, state, or candidate-status name is missing | Stop and request only the missing required business value |
| Process type is not Standard, status is not Draft, or update is requested | Fail closed; do not coerce or convert the request |
| Fresh task-wide export fails, times out, is scoped, identifies a different task, or omits a required dictionary | Stop before uniqueness or custom collision checks; preserve sanitized export/status evidence and do not substitute another source |
| Effective CSP_PROCESS_CODE repeats in input or the verified fresh export has a case-insensitive match | Fail validation for the complete list and disclose the user-defined or derived code plus raw and case-insensitive match counts without modifying it |
| The fresh export does not prove a CSP_SUBPROCESS_CODE matching CSW_ plus 32-uppercase-hexadecimal characters | Stop before client generation; do not invent another subprocess-code shape. |
| The user-authorized successful custom-phase package does not prove the required SettingCode or SettingItemCode pattern, a fresh export collision dictionary is unavailable, or a generated setting identifier collides | Stop before package generation. Do not reuse an identifier from the example package or invent another identifier shape. |
| PHASE_DEFINITION_CODE is missing, nonnumeric, repeated, collides with the verified export, or is a numeric scientific-notation token | Stop and request the affected Oracle-generated identifier. Do not derive or invent it. |
| A required STATE_DEFINITION_CODE is missing, nonnumeric, repeated, collides with the verified export, or is a numeric scientific-notation token | Stop and request the affected Oracle-generated identifier. Do not derive or invent it. |
| A seeded phase or state Code differs from OFFER, HR, REJECTED_EMPLOYER, or WITHDRAWN_BY_CANDIDATE | Stop and restore the matching seeded value verbatim; do not transform or regenerate it. |
| An existing phase or state is requested for reuse | Stop and explain that the supplied reuse package has header-only phase/state rows and a parentless scientific-notation reference; request a clean completed reuse package before adding a reuse path. |
| A candidate-status match is zero or ambiguous, or the candidate-status dictionary is unavailable | Stop and request a disambiguating exported identity or a new completed export; do not create a candidate status. |
| A custom archive omits a required member, has a parentless row, has altered Offer/HR system blocks or seeded codes, has an unproven client-generated subprocess code, or lacks a resolved candidate-status routing mapping | Fail local package validation and do not hand the archive to `core.data-loader`. |
| A supplied translation source language is other than `US` | Stop; the successful custom-phase package establishes only the `US` source-language profile, so do not invoke a live language lookup or construct a substitute value |
| A final archive is ready for execution | Hand it exclusively to `core.data-loader`; do not make a direct pillar import call |
| The local OAuth cache is expired, unavailable, or cannot be refreshed before the final preview | Route through `core.auth.fusion-oauth-authentication` before asking for execution approval. If the normal browser launch is not visible, obtain the sign-in URL through the auth workflow's URL-only mode. Do not expose tokens, cache contents, or authorization codes. |
| The Data Loader initiation receipt does not include an FSM Process Status Details request ID | Report the returned initiation identifier as a Data Loader initiation request only. Do not infer an FSM import request ID. When the user asks for completion evidence, obtain the FSM ProcessLog or a fresh read-only export. |
| Import process fails or partially succeeds | Preserve sanitized ProcessLog and status evidence, reconcile with a fresh read-only export, and do not retry automatically |
| Approval is missing or stale | Stop immediately before the external mutation; a material change requires a new preview and approval |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required values, shape, length, type, or ordering are invalid | Correct the supplied input and revalidate the complete list |
| Transport or export process | The selected task-level export cannot produce a completed current baseline | Preserve sanitized export/status evidence; correct the environment or rerun the read-only export through the selected workflow |
| Lookup or catalog | A resolver returns multiple matches, no approved authority, or an unresolved contract | Stop until authoritative mapping or identity is provided |
| Approval blocker | Package or approval contract is incomplete or stale | Do not submit; use the routed preview and approval workflow |
| Process failed or partial success | A completed import has failures or mixed outcomes | Reconcile actual state through a fresh read-only export; no automatic retry |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Local package preview | Target, operation, archive fingerprint, supported rows, skipped fields, mappings, defaults, system-owned rows, and unresolved items |
| Execution handoff | Token-readiness result without secrets, archive fingerprint, and a clear distinction between the Data Loader initiation receipt and any later FSM Process Status Details request ID |
| Partial or failed import | Per-process success, warning, or failure classification and sanitized ProcessLog/status evidence |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Endpoint, lookup source, import details, or lifecycle behavior is not defined | Do not invent it or call an API |
| A final archive is available | Do not upload, initiate, or verify an import from this pillar skill; `core.data-loader` owns those actions |
| An uncertain POST, upload, import, or partial failure occurs | Do not retry automatically |
| Existing process or reusable object would be changed | Do not update, rename, duplicate, activate, inactivate, delete, or overwrite it |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.VALIDATE_PACKAGE | decision | 110 | execution_gate | valid->CSP.DONE_AUTHORING;invalid->CSP.HANDLE_ISSUES | CSP.CHECK_DESIGN | stop | A candidate package for the complete input list has been produced by the routed runbook |
| CSP.HANDLE_ISSUES | step | 130 | error_handler | handled->CSP.RETURN_ISSUES | none | stop | Any validation, dependency, lookup, design, package, catalog, authorization, process, or verification failure occurs |
| CSP.RETURN_ISSUES | terminal | 140 | terminal | none | CSP.HANDLE_ISSUES | stop | An issue was classified |
| CSP.DONE_AUTHORING | terminal | 150 | terminal | none | CSP.VALIDATE_PACKAGE | stop | A package is locally validated and ready for the separate execution workflow |
| CSP.DONE_VERIFIED | terminal | 160 | terminal | none | CSP.VERIFY_RESULT | stop | Supplied post-import evidence reconciles successfully |
