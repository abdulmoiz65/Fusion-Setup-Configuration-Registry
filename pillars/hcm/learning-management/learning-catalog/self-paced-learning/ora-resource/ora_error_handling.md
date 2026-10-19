# Self-Paced Learning Error Handling

The task fails closed, preserves row-scoped evidence, and never turns an
uncertain mutation into an automatic write retry.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required input or applicable dependency is missing | Stop before payload construction for the affected row and return the exact missing value or evidence |
| Data Loader registration, template, component, or selected operation is missing or ambiguous | Block the mutation; do not substitute the similarly named Direct REST collection or silently choose another business object |
| A Direct REST mutation is requested without a named exception or current unsupported-operation evidence | Stop before preview and return the missing route evidence; never fall back automatically |
| Zero or multiple exact identity results occur | Stop the affected operation and return sanitized match evidence; do not select the first result |
| A row is invalid in a multi-row request | Exclude that row, show its correction, and continue planning independently valid rows without hiding the failure |
| Preview or current-state fingerprint is stale | Invalidate row and aggregate approval, re-read state, rebuild the preview, and request new approval |
| Approval is denied, absent, stale, or does not accept a preview-only omission | Do not issue the mutation; return the denial or missing acceptance without side effects |
| A mutation returns an authentication or authorization error | Do not replay the write; refresh authentication only for a new safe read and reconcile first |
| A mutation result is uncertain because of timeout, disconnect, or ambiguous response | Stop remaining writes, do not retry, and reconcile through exact safe reads |
| Change-request or content processing exceeds the bounded poll window | Return sanitized process identifiers, last status, elapsed time, known effects, and a safe next read |
| Readback differs from the approved preview | Report partial, failed, or indeterminate verification and preserve the mismatch without claiming success |
| Deep-insert content readback does not show status ORA_ACTIVE and autoCommit Y | Report failed or indeterminate verification; do not patch the derived fields or claim content readiness |
| Activation readback is not Active with DraftExists N and PublishedExists Y, or the content source changed | Report failed or indeterminate activation, preserve the original content evidence, and do not invoke publish as a substitute |
| Target metadata lacks a requested detail | Do not infer a field, enabled lookup value, DFF segment, opaque hash, action body, or concurrency contract |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required input, approval, exact reference, or applicable contract evidence is unavailable | Supply or resolve the named blocker |
| AMBIGUOUS | More than one exact or otherwise indistinguishable required target exists | Provide a stronger identifier and rebuild the preview |
| STALE | Approved fingerprint no longer matches the target or included row manifest | Refresh evidence and approve the new preview |
| UNSUPPORTED | The requested operation, field, content behavior, association, or serialization lacks an approved contract | Select supported behavior or update the source contract |
| DENIED | Approval was denied or applicable access is unavailable | End without mutation or obtain the required authorization |
| PARTIAL | Some approved effects are verified but one or more expected effects are not | Reconcile the exact row and do not replay writes automatically |
| FAILED | Validation, execution, polling, or readback conclusively fails | Review sanitized diagnostics before a new attempt |
| INDETERMINATE | Safe readback cannot establish whether the mutation occurred | Preserve evidence, stop the batch, and investigate before any new attempt |
| ALL_GOOD | Every expected persisted effect is verified and protected state remains unchanged | Return the completed row and run records |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before mutation | Exact target, operation, item create key or returned identity, row set and exclusions, before and after values, dependencies, lifecycle and learner effects, content reference, fingerprint, and approval state |
| Demo omission | Objective and Ideal Learner text, the fact that neither will be sent or persisted through this REST contract, and explicit omission acceptance |
| On partial or uncertain result | Row identifier, operation, sanitized request correlation or process identifiers, verified effects, unknown effects, last safe read, and next read-only action |
| On failure | Failure category, stage, sanitized identifiers, known side effects, blocker, and one safe corrective action |

## Retry Rules

| Activity | Retry Behavior |
|---|---|
| Safe read before any mutation | A bounded read retry may occur after transient failure when it cannot create or change data |
| Data Loader upload or initiation, POST, PATCH, DELETE, publish, reprocess, content upload, or content mutation | No automatic write retries; submit the approved artifact or request once |
| Authentication refresh after a write response is uncertain | Refresh may support reconciliation reads only; it must not replay the write |
| Bounded asynchronous polling | Repeat only documented status reads until terminal state or timeout; polling is not mutation retry |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval is absent, denied, stale, or scope-mismatched | Do not call POST, PATCH, DELETE, publish, reprocess, upload, or content mutation |
| A supported create or update is requested | Do not bypass core.data-loader or treat raw REST Describe as Data Loader registration evidence |
| Data Loader does not support an operation | Do not use Direct REST unless the task skill names the exact exception and the approved preview includes that route |
| UI activation is requested | Do not invoke the collection publish action; use a supported Data Loader update or the exact returned-item activation PATCH exception |
| Objective or Ideal Learner is generated | Do not invent a REST field or map the value into description, DFF, or another field |
| Returned opaque link is absent | Do not construct an item hash, composite child URL, or guessed key |
| Target lookup or language evidence is absent | Do not infer a code from a user-facing meaning or label |
| A fingerprint exists | Do not describe it as ETag, If-Match, or atomic conditional-write protection |
| A write result is uncertain | Do not automatically retry it and do not continue the batch |
| An HCM list is resolved | Do not claim its identity proves a writable Learning Catalog association |
| Upsert metadata appears in Describe | Do not expose upsert as a user-facing operation in this release |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SPL.AUTHORIZE_EXECUTION | decision | 60 | execution_gate | approved->SPL.EVALUATE_RESULT;evidence_available->SPL.EVALUATE_RESULT;denied->SPL.HANDLE_ERROR;stale->SPL.HANDLE_ERROR;blocked->SPL.HANDLE_ERROR | SPL.ENFORCE_DESIGN | stop | A fresh validation-only result or exact immutable mutation preview reaches its final authorization gate |
| SPL.HANDLE_ERROR | step | 80 | error_handler | disclosed->SPL.RETURN_ISSUES | none | stop | Any validation, dependency, lookup, design, approval, execution, timeout, or verification condition is blocked or uncertain |
| SPL.RETURN_SUCCESS | terminal | 90 | terminal | none | SPL.EVALUATE_RESULT | stop | Every requested validation result or persisted effect is verified |
| SPL.RETURN_ISSUES | terminal | 100 | terminal | none | SPL.HANDLE_ERROR | stop | One or more blockers, failures, partial effects, or unknown outcomes require disclosure |
