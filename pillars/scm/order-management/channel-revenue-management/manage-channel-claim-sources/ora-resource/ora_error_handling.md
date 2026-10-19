# Manage Channel Claim Sources Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Invalid input, unsupported columns, aliases, nulls or missing baseline | Classify input validation; report worksheet/row/field without sensitive payloads; stop before readiness |
| Missing/ambiguous parent or child, lookup mismatch or ineligible reference set | Classify input validation; return issues; never create a missing update target. Apply the default-reference resolver's set-sharing rule before reporting a mismatch; a differing set alone is not an error |
| API field absent from live loader contract | Classify catalog mismatch; report unsupported field/operation/linkage and stop; no direct REST fallback |
| Predefined accounting edit or unknown predefined state | Report blocked design validation; do not remove the requested edit silently or change SeededFlag |
| Duplicate create | Stop; no POST retry and no Upsert-Mode |
| No effective change | Return NO_CHANGE; no upload, approval request or mutation |
| Readiness succeeds | Return CREATE_READY, CHILD_CREATE_READY or UPDATE_READY to Task Hook, not execution success. Normal core.data-loader preview and approval remain mandatory |
| Approval absent or not bound to exact environment/operation/archive/context/envelope | Classify approval blocker; stop before submission; newly requested changes or fresh artifacts require fresh validation and approval. Original-source edits alone do not alter the intact approved artifact; after approval verify saved integrity/context only, not live references or task rules |
| Auth/authz or transport/environment failure | Delegate diagnostic and bounded safe-read handling to core.data-loader; never infer write permission or retry writes |
| Fusion API error or partial batch failure | Preserve successful rows and errors array; report failed units without replaying successful ones; inspect errors under the loader workflow |
| Process timeout or process failed | Return environment, operation, request/process ID, last status and elapsed wait via the loader's sanitized diagnostics; status check is the next step, not resubmission |
| Uncertain POST/PATCH or upload result | Reconcile with declared read-only target lookups and loader status; never automatically replay or resubmit. New attempt requires explicit approval |
| Verification differs from requested changes | Report unverified/partial outcome; do not claim completion from HTTP acceptance or job initiation |
| Artifact persistence failure | Classify artifact persistence; stop, retain safe resume stage and recover persistence before continuing |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validated preview | Exact environment, create/update operation, parent/child scope, requested before/after values, omitted-field preservation, immutable artifact fingerprint, validation result and any loader limitations |
| Task handoff | Task code ORA_CJM_MANAGE_CLAIM_SOURCES and name Manage Channel Claim Sources; terminal/current Rule ID; completed path and outcomes; sanitized evidence; missing items; verified side effects; one next action |
| Diagnostics | Use existing project/core recording and redaction; no credentials, raw payloads, token caches, protected URLs or sensitive customer values in repository resources |
| Retry/concurrency | No promise of automatic rollback, transactional parent/child atomicity or concurrency protection beyond documented loader capabilities; stale evidence discovered during preapproval preparation triggers a new cycle, not extra live checks after approval |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCS.CONFIRM_CREATE | decision | 8 | execution_gate | ready->CJMCS.RETURN_CREATE_READY;blocked->RETURN_ISSUES | CJMCS.VALIDATE_CHANGES | stop | Explicit create with no duplicate; validated immutable artifact and supported loader shape; readiness only, not approval |
| CJMCS.CONFIRM_UPDATE | decision | 9 | execution_gate | ready->CJMCS.RETURN_UPDATE_READY;blocked->RETURN_ISSUES | CJMCS.VALIDATE_CHANGES | stop | Explicit update with verified existing targets, nonempty diff, PATCH and supported loader shape; readiness only, not approval |
| CJMCS.RETURN_CREATE_READY | terminal | 10 | terminal | none | CJMCS.CONFIRM_CREATE | stop | Return CREATE_READY for loader preview and approval |
| CJMCS.RETURN_UPDATE_READY | terminal | 11 | terminal | none | CJMCS.CONFIRM_UPDATE | stop | Return UPDATE_READY for loader preview and approval |
| CJMCS.RETURN_NO_CHANGE | terminal | 12 | terminal | none | CJMCS.VALIDATE_CHANGES | stop | Return NO_CHANGE without submission |
| CJMCS.CONFIRM_CHILD_CREATE | decision | 14 | execution_gate | ready->CJMCS.RETURN_CHILD_CREATE_READY;blocked->RETURN_ISSUES | CJMCS.VALIDATE_CHANGES | stop | Explicit child create; verified existing parent, zero child duplicates, valid child values, exact live-supported child POST/linkage and immutable child-only artifact; no parent mutation; readiness is not upload approval |
| CJMCS.RETURN_CHILD_CREATE_READY | terminal | 15 | terminal | none | CJMCS.CONFIRM_CHILD_CREATE | stop | Return CHILD_CREATE_READY for separate loader preview and approval |
| RETURN_ISSUES | terminal | 16 | terminal | none | none | stop | Return blocking issues without write |
