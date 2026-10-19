# Error Handling

## Business-First Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before create, update, or delete | Business outcome, affected recruiter or candidate experience, intended users, timing, assumptions, impact, and unchanged configuration; technical identifiers only when useful for traceability or requested. |
| Create or update preview | Complete comparison table plus exact target environment, fresh current or uniqueness state, minimal requested delta, impact, verification read, and approval fingerprint. |
| Deletion preview | LookupCode, Meaning, Description, Current State, Impact, and Deletion Status plus exact environment, fresh exact read, and approval fingerprint. |
| Post-change | Fresh exact comparison for create or update, or verified absence from active review after delete, with sanitized diagnostics and artifact references. |

## Approval Rules

| Operation | Required Gate |
|---|---|
| Create | One explicit approval immediately before one delegated create, bound to the immutable preview and fingerprint. |
| Update | One explicit approval immediately before one delegated update, bound to the immutable preview and fingerprint. |
| Delete | First obtain approval of the immutable deletion preview; then obtain a second fresh confirmation immediately before deletion that explicitly names the exact LookupCode and Meaning. |
| Changed preview or stale read | Invalidate prior approval and regenerate the preview and fingerprint; for deletion, repeat both gates. |

## Post-Change Verification

| Operation | Verification | Persistence |
|---|---|---|
| Create | Re-read the exact new LookupCode and compare every returned field with the approved state. | Persist sanitized diagnostics, run metadata, artifact references, and token usage under `project/{project_id}`. |
| Update | Re-read the exact LookupType and LookupCode; verify the approved delta and preservation of every protected and unrequested value. | Persist sanitized diagnostics, run metadata, artifact references, and token usage under `project/{project_id}`. |
| Delete | Run the fixed active review with `includeInactive: false` and verify that the exact entry is no longer returned. | Persist sanitized diagnostics, run metadata, artifact references, and token usage under `project/{project_id}`. |

## Error Situations

| Situation | Failure Class | What Should Happen |
|---|---|---|
| Missing or ambiguous business decision | Input validation | Ask one concise business-language clarification and stop. |
| Another lookup type or unsupported field is requested | Catalog mismatch | Explain the task boundary in business language; do not suggest an alternate unapproved route. |
| Exact code does not resolve, resolves more than once, or creation uniqueness is uncertain | Fusion API | Stop and return the sanitized lookup evidence; do not mutate. |
| Approval is absent, stale, for a different operation, environment, entry, or payload | Approval blocker | Regenerate an immutable preview and request the operation-specific approval. |
| Authentication or authorization fails during delegated Common Lookups work | Auth/authz | Follow the delegated core contract; permit only its single documented cached-token refresh, then stop if unresolved. |
| Transport or Fusion response is uncertain | Transport/environment | Preserve sanitized diagnostics and stop; do not retry a mutation automatically. |
| Post-change read differs from the approved result | Fusion API | Report the exact sanitized mismatch and stop without another mutation. |
| Artifact or run-record persistence fails | Artifact persistence | Report the intended project path and stop before claiming durable completion. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Unsupported mutation | Do not activate, deactivate, change a code, tag, display sequence, seed ownership, or any field outside Meaning, Description, StartDate, and EndDate. |
| Transport shortcut | Do not construct REST URLs, call curl, manage OAuth, use browser automation, or duplicate Common Lookups transport. |
| Broad lookup access | Do not inspect, discover, create, or mutate another lookup type. |
| Oversized payload | Do not send unchanged fields merely because the comparison table displays them. |
| Uncertain mutation outcome | Do not retry create, update, or delete automatically. |
| FSM shortcut | Do not use FSM export/import as the default review or CRUD route. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RIC.PREVIEW_CHANGE | decision | 6 | execution_gate | approved_create->RIC.READY_CREATE;approved_update->RIC.READY_UPDATE;missing->RIC.APPROVAL_ISSUES | RIC.ENFORCE | stop | A supported create or update has a complete immutable preview |
| RIC.PREVIEW_DELETE | decision | 7 | execution_gate | preview_approved->RIC.CONFIRM_DELETE;missing->RIC.APPROVAL_ISSUES | RIC.ENFORCE | stop | An exact deletion has a complete immutable preview |
| RIC.CONFIRM_DELETE | decision | 8 | execution_gate | confirmed->RIC.READY_DELETE;missing->RIC.APPROVAL_ISSUES;stale->RIC.APPROVAL_ISSUES | RIC.PREVIEW_DELETE | stop | The immutable deletion preview has been approved and fresh final confirmation is required |
| RIC.INPUT_ISSUES | step | 11 | error_handler | disclosed->RETURN_ISSUES | none | stop | Business intake or operation selection is incomplete or ambiguous |
| RIC.LOOKUP_ISSUES | step | 12 | error_handler | disclosed->RETURN_ISSUES | none | stop | Current identity, uniqueness, or fixed-scope resolution fails |
| RIC.DESIGN_ISSUES | step | 13 | error_handler | disclosed->RETURN_ISSUES | none | stop | Supported-field, preservation, comparison, or evidence-boundary enforcement fails |
| RIC.APPROVAL_ISSUES | step | 14 | error_handler | disclosed->RETURN_ISSUES | none | stop | Required approval is absent, stale, or does not identify the exact operation and entry |
| RIC.POST_CHANGE_ISSUES | step | 15 | error_handler | disclosed->RETURN_ISSUES | none | stop | A post-create, post-update, or post-delete verification is missing, mismatched, or uncertain |
| RIC.DONE_REVIEW | terminal | 16 | terminal | none | RIC.LIST_ACTIVE | stop | Active interaction-category review is complete |
| RIC.DONE_CHANGE | terminal | 17 | terminal | none | RIC.VERIFY_CHANGE | stop | A create or update has been freshly re-read and verified |
| RIC.DONE_DELETE | terminal | 18 | terminal | none | RIC.VERIFY_DELETE | stop | Deletion absence has been verified in active review |
| RIC.READY_CREATE | terminal | 19 | terminal | none | RIC.PREVIEW_CHANGE | stop | Exact approval authorizes one delegated Common Lookups create followed by required verification |
| RIC.READY_UPDATE | terminal | 20 | terminal | none | RIC.PREVIEW_CHANGE | stop | Exact approval authorizes one delegated Common Lookups update followed by required verification |
| RIC.READY_DELETE | terminal | 21 | terminal | none | RIC.CONFIRM_DELETE | stop | Both deletion confirmations authorize one delegated Common Lookups delete followed by required absence verification |
| RETURN_ISSUES | terminal | 22 | terminal | none | none | stop | Business-language error disclosure is complete |
