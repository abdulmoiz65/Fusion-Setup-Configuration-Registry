# Manage Channel Claim Reasons Gates and Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required input, field length, date, boolean, or response-only-field validation fails | Stop before preview and identify the affected row and corrective field value |
| The reference data set is missing or ambiguous | Stop before preview; create or clarify the reference data set in its own task, then restart the Run Book validation |
| Supplied SetId is malformed, conflicts with code/name, or cannot be verified completely | Stop with row/header evidence; do not treat zero as missing, guess code/name, or fall back from a failed ID lookup. Preserve the original workbook |
| SetId remains in the final loader source or set enrichment changes a pending artifact | Return a preparation/contract blocker; resolve into supported code/name fields before fresh Data Loader preflight, Task Hook validation and approval |
| An existing reason has the same ClaimReasonCode and resolved SetCode | For create, stop as DUPLICATE; for explicit update, continue current-value validation without changing the identity |
| Update target does not exist, is ambiguous, or conflicts with a supplied ID | Stop before preview; never insert, upsert, or choose the first match |
| Update field, key, omission, or null behavior is unsupported by the selected loader | Stop with the exact contract mismatch; do not bypass Data Loader with a direct PATCH |
| Concurrent change is reported or current-value evidence becomes stale before approval | Restart validation and approval. Do not claim atomic lost-update protection unless the selected loader supports a verified concurrency token |
| Fusion rejects or ambiguously completes a core.data-loader-authorized write | Stop without replaying the write and reconcile through fresh FSCR Run Book read-only evidence |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| INPUT_VALIDATION | Required input or a documented type, date, length, boolean, or read-only-attribute check fails | Correct the named field and rebuild the preview |
| DEPENDENCY_BLOCKER | Reference-data-set resolution fails | Resolve the independent prerequisite and rebuild the preview |
| DUPLICATE | A create request matches an existing code/set, or multiple input rows target one record | Correct the source or explicitly request an update; never switch operations automatically |
| NOT_FOUND | Update lookup finds no exact existing code/set match | Correct the identity; do not create a replacement |
| CONTRACT_MISMATCH | Requested update is absent from the operation-specific API or selected loader contract, or null/omission semantics are unproven | Resolve the documented contract before another preview |
| NO_CHANGE | All explicitly requested update values already match Fusion | Report no change and submit nothing for that record |
| APPROVAL_BLOCKER | The exact Data Loader preview is absent, changed, stale, or not explicitly approved | Rebuild the exact preview and obtain new approval |
| FUSION_API | Fusion rejects or cannot confirm the authorized write | Preserve redacted evidence and stop before retry |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before Data Loader authorization | Target environment, create or update operation, existing code and resolved set, supplied SetId resolution and intake-column omission when applicable, create-only defaults where applicable, and exact immutable artifact. For updates show each requested field's before/after value and any explicit clear; preserve the core approval lifecycle |
| After Data Loader initiation | Return the core initiation result, not a claim that rows were updated. On an explicit status request use core.data-loader status/error checks and report per-row created/updated/no-change/failure evidence; no automatic polling |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A direct channelClaimReasons REST POST or PATCH is proposed | Do not perform it. Route approved creates and updates through core.data-loader and its Task Hook lifecycle. |
| Approval is missing or does not match the exact operation, target, and final archive | Do not authorize a Data Loader write. A create approval never authorizes an update. |
| Final task validation discovers enrichment, field removal, changed values, or no-op rows to remove | Stop; correct the preparation source, rerun Data Loader preflight and Task Hook on the new immutable archive, and obtain approval. Never alter an already prepared or approved archive in place. |
| An update sample contains POST fallback rows or values from an unrelated first sample record | Do not submit it. Samples are not target resolution; require exact record lookup, explicit intended changes, and PATCH on every update row. |
| A previous mutation has an uncertain outcome | Do not retry until fresh read-only Run Book reconciliation proves the current state and a new preview is approved. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCR.CONFIRM_CREATE_GATE | decision | 7 | execution_gate | ready->CJMCR.RETURN_CREATE_READY;blocked->RETURN_ISSUES | CJMCR.FIND_BY_CODE | stop | Require create intent and zero exact matches plus POST in the final artifact; ready means eligible for Task Hook preview, never prior user approval. Update intent with no match is NOT_FOUND |
| CJMCR.RETURN_CREATE_READY | terminal | 8 | terminal | none | CJMCR.CONFIRM_CREATE_GATE | stop | Return create validation success to Task Hook; core.data-loader must still obtain and verify approval bound to its immutable artifact before submission |
| CJMCR.CONFIRM_UPDATE_GATE | decision | 9 | execution_gate | ready->CJMCR.RETURN_UPDATE_READY;blocked->RETURN_ISSUES | CJMCR.VALIDATE_UPDATE | stop | Require PATCH, resolved existing identity, only supported intended changes and verified loader omission/null semantics in the final artifact; ready means eligible for Task Hook before/after preview, not permission to write |
| CJMCR.RETURN_UPDATE_READY | terminal | 10 | terminal | none | CJMCR.CONFIRM_UPDATE_GATE | stop | Return update validation success to Task Hook; require its normal immutable-artifact approval and verification before core.data-loader submission |
| CJMCR.RETURN_NO_CHANGE | terminal | 11 | terminal | none | CJMCR.VALIDATE_UPDATE | stop | Return NO_CHANGE without submission; if part of a batch, any archive removing no-op rows requires fresh preflight and Task Hook validation |
| RETURN_ISSUES | terminal | 12 | terminal | none | none | stop | Any validation, dependency, lookup, duplicate, missing-target, contract, or approval requirement fails |
