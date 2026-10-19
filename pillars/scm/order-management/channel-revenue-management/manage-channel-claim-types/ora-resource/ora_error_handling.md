# Manage Channel Claim Types Gates and Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Parent required fields, side applicability, effective dates, or child mapping fields fail validation | Stop before preview and identify the affected parent or child row and corrective field value |
| A child Business Unit ID or name resolves to zero, multiple, inactive, inaccessible, incomplete-page, or conflicting-identity results | Stop before preview; provide the affected child row and require one exact active BusinessUnitId or name, with agreement when both are supplied. Do not guess an ID or create a Business Unit. |
| The reference data set is missing, ambiguous, inaccessible, or has conflicting SetId/SetCode/SetName | Stop before preview; clarify the supplied set identifiers or resolve lookup access; any needed set creation belongs in its own ERP task, then restart Run Book validation |
| An existing type has the same ClaimTypeCode and set identity | Create stops DUPLICATE; explicit update continues existing-target validation |
| Update parent/child is missing, ambiguous, mis-parented, or has conflicting identifiers | Stop NOT_FOUND or INPUT_VALIDATION; never create or reparent as fallback |
| Requested update field, child key/linkage or null/omission semantics lack live loader support | Stop CONTRACT_MISMATCH; retain the requested change and explain the missing contract, never silently discard it or use direct PATCH |
| AR-related optional values are supplied | Preserve the values without lookup and state that FSCR cannot validate their AR dependencies |
| Fusion rejects or ambiguously completes a core.data-loader-authorized write | Stop without replaying the write and reconcile through fresh FSCR Run Book read-only evidence |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| INPUT_VALIDATION | Parent, child mapping, boolean, date, or response-only-attribute check fails | Correct the named field and rebuild the preview |
| DEPENDENCY_BLOCKER | Reference-data-set resolution fails | Resolve the independent prerequisite and rebuild the preview |
| DEPENDENCY_BLOCKER | A Business Unit identity lookup fails or conflicts with a supplied BusinessUnitId | Correct the child Business Unit identity and rebuild the final loader source before preview |
| DUPLICATE | Create matches existing code/set or input repeats one mutation target | Correct source or explicitly request update; never silently change operation |
| NOT_FOUND | Explicit update has no exact existing parent or child | Correct identity; no create fallback |
| CONTRACT_MISMATCH | Unsupported update field, keys, child shape or null encoding | Resolve loader/API support before rebuilding preview |
| NO_CHANGE | All intended parent and child values already match | Submit nothing; partial no-op removal requires fresh final preparation |
| AR_VALIDATION_UNAVAILABLE | An AR-related optional value is supplied | Retain the value for Data Loader and obtain independent AR confirmation outside FSCR; no FSCR lookup is performed |
| APPROVAL_BLOCKER | The exact Data Loader preview is absent, changed, stale, or not explicitly approved | Rebuild the exact preview and obtain new approval |
| FUSION_API | Fusion rejects or cannot confirm the authorized write | Preserve redacted evidence and stop before retry |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before Data Loader authorization | Exact environment, operation, parent code/set and child identity, each changed field before/after, explicit clears, create-only defaults, AR-validation limitation, and exact immutable artifact. Ready nodes permit preview only; Task Hook approval follows successful validation |
| After Data Loader initiation | Return core initiation report, not row success. Do not automatically poll; on requested status retrieve core status/errors and preserve partial successes |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A direct parent or child REST POST or PATCH is proposed | Do not perform it. Route approved creates and updates only through FSCR Run Book/core.data-loader and Task Hook. |
| A final artifact needs correction or current evidence becomes stale | Restart preparation, preflight and Task Hook. Never mutate an approved archive, refresh its lookup evidence after approval, or promise unverified concurrency protection. |
| A child Business Unit ID or name has zero, multiple, inactive, inaccessible, incomplete-page, or conflicting-identity matches | Do not write or infer BusinessUnitId. Stop before final loader-source preparation. |
| An AR dependency lookup is proposed | Do not validate or look up transaction types, credit memo types, chargeback types, receivables activities, or other AR dependencies. |
| Approval is missing or does not match the exact preview | Do not authorize a Data Loader write. |
| A previous mutation has an uncertain outcome | Do not retry until fresh read-only Run Book reconciliation proves the current state and a new preview is approved. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCT.CONFIRM_CREATE_GATE | decision | 11 | execution_gate | ready->CJMCT.RETURN_CREATE_READY;blocked->RETURN_ISSUES | CJMCT.FIND_BY_CODE | stop | Require create intent, no existing parent and POST; missing update target blocks NOT_FOUND. Ready is validation readiness, not prior upload approval |
| CJMCT.RETURN_CREATE_READY | terminal | 12 | terminal | none | CJMCT.CONFIRM_CREATE_GATE | stop | Return create readiness to Task Hook; require its preview, approval and archive verification before core submission |
| CJMCT.CONFIRM_UPDATE_GATE | decision | 13 | execution_gate | ready->CJMCT.RETURN_UPDATE_READY;blocked->RETURN_ISSUES | CJMCT.VALIDATE_UPDATE | stop | Require PATCH, exact existing parent/child identities, only intended changes and verified loader field/key/linkage/omission/null support; ready permits Task Hook preview only |
| CJMCT.RETURN_UPDATE_READY | terminal | 14 | terminal | none | CJMCT.CONFIRM_UPDATE_GATE | stop | Return update readiness; Task Hook approval and immutable archive verification remain required before core submission |
| CJMCT.RETURN_NO_CHANGE | terminal | 15 | terminal | none | CJMCT.VALIDATE_UPDATE | stop | Return NO_CHANGE with no upload; partial no-op removal restarts final preparation |
| RETURN_ISSUES | terminal | 16 | terminal | none | none | stop | Any validation, dependency, lookup, duplicate, missing-target, contract or approval gate fails |
