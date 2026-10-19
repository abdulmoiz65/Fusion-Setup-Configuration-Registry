# Error Handling

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Review | Business result first; only documented fields actually returned; technical identifiers only when useful or requested; baseline-derived evidence labeled separately. |
| Mutation preview | Business outcome, assumptions, exact environment, exact parent/code identity, fresh current state or create absence, requested delta, impact, unchanged configuration, verification read, and approval fingerprint. |
| Approval | One explicit approval bound to the exact immutable preview immediately before one create, update, or delete. |
| Post-change | Fresh exact type/code state or verified deletion absence, preservation comparison, and sanitized project evidence references. |

## Ownership Evidence Refresh

| Situation | What Should Happen |
|---|---|
| Requested LookupType matches no approved prefix | Block the operation and require refreshed approved ownership evidence; do not add a prefix from runtime guesses or a small export. |
| Approved evidence changes the prefix baseline | Replace the versioned baseline as one reviewed unit, then reclassify every affected LookupType before continuing. |
| Module information is absent from current documented metadata | Preserve prefix-based ownership only; do not infer ModuleId or module display name. |

## Error Situations

| Situation | What Should Happen |
|---|---|
| Business outcome is genuinely ambiguous | Ask one concise business-language clarification. |
| LookupType is outside the approved prefix baseline | Report the ownership-mapping gap and stop. |
| Parent or code has no match, multiple matches, a create collision, or uncertain absence | Return sanitized match evidence and stop before preview. |
| Common Lookups response does not establish a field, protection state, or capability | Explain the evidence gap and stop without inference. |
| Translation mutation is requested | Return current translations as read-only information and explain that mutation is unsupported. |
| Approval is absent, stale, or bound to another environment, identity, state, or delta | Rebuild the immutable preview and obtain fresh approval. |
| Authentication or authorization fails | Treat 401 or 403 as auth/authz failure, never absence; follow the core provider's permitted refresh once, then stop if unresolved. |
| Mutation outcome is uncertain | Persist sanitized diagnostics and stop without automatic retry. |
| Verification differs from the approved state | Report the exact sanitized discrepancy and stop without corrective mutation. |
| Project audit persistence fails | Report the intended project location and do not claim durable completion. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing business decision, operation, identity, target, or delta | Ask only for the missing decision. |
| Catalog mismatch | Non-owned prefix, translation mutation, or unsupported route/capability | Explain the task boundary and stop. |
| Auth/authz | Common Lookups cannot authenticate or lacks privilege | Follow its single permitted refresh behavior, then stop. |
| Transport/environment | Provider response or mutation outcome is uncertain | Preserve sanitized evidence and stop without mutation retry. |
| Fusion API | Exact identity, field support, protection, or verification fails | Report current response-grounded evidence. |
| Artifact persistence | Required diagnostic, approval, run, or token record cannot be written | Report the destination and stop before completion. |
| Approval blocker | Exact immutable approval is missing or stale | Regenerate preview and request approval immediately before the action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Non-owned LookupType | Do not read or mutate it through this task. |
| Undocumented API claim | Do not claim ModuleId filtering, ownership discovery, ModuleId, CustomizationLevel, RestAccessSecured, or translation mutation without current documented metadata. |
| Transport shortcut | Do not construct REST URLs, call curl, manage OAuth, use browser automation, or duplicate Common Lookups transport. |
| Identity or protection change | Do not alter LookupType, LookupCode, ownership basis, seed identity, or a protected field. |
| Alternate route | Do not substitute FSM, export/import, direct REST, UI, or another route for unsupported behavior. |
| Uncertain mutation | Do not retry automatically. |
| Sensitive evidence | Do not persist credentials, tokens, headers, or sensitive values. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCL.PREVIEW | decision | 8 | execution_gate | approved_create->CCL.READY_CREATE;approved_update->CCL.READY_UPDATE;approved_delete->CCL.READY_DELETE;missing->CCL.APPROVAL_ISSUES | CCL.ENFORCE | stop | A supported type or code mutation has a complete immutable preview |
| CCL.INPUT_ISSUES | step | 10 | error_handler | disclosed->RETURN_ISSUES | none | stop | Business intake, identity, target, or delta is incomplete or ambiguous |
| CCL.LOOKUP_ISSUES | step | 11 | error_handler | disclosed->RETURN_ISSUES | none | stop | Collection, parent, code, or translation resolution fails |
| CCL.OWNERSHIP_ISSUES | step | 12 | error_handler | disclosed->RETURN_ISSUES | none | stop | LookupType does not match the approved ownership prefix baseline |
| CCL.DESIGN_ISSUES | step | 13 | error_handler | disclosed->RETURN_ISSUES | none | stop | Field support, protection, preservation, translation, or route enforcement fails |
| CCL.APPROVAL_ISSUES | step | 14 | error_handler | disclosed->RETURN_ISSUES | none | stop | Exact immutable approval is absent or stale |
| CCL.POST_CHANGE_ISSUES | step | 15 | error_handler | disclosed->RETURN_ISSUES | none | stop | Post-mutation verification is missing, mismatched, or uncertain |
| CCL.DONE_LIST | terminal | 16 | terminal | none | CCL.CLASSIFY_SCOPE | stop | Complete owned Common Lookup type review is ready |
| CCL.DONE_PARENT | terminal | 17 | terminal | none | CCL.READ_PARENT | stop | Exact owned parent review is complete |
| CCL.DONE_CODES | terminal | 18 | terminal | none | CCL.READ_CODE | stop | Requested owned lookup-code review is complete |
| CCL.DONE_TRANSLATIONS | terminal | 19 | terminal | none | CCL.READ_TRANSLATIONS | stop | Requested read-only translations are returned |
| CCL.READY_CREATE | terminal | 20 | terminal | none | CCL.PREVIEW | stop | Exact approval authorizes one delegated Common Lookups type or code create followed by verification |
| CCL.READY_UPDATE | terminal | 21 | terminal | none | CCL.PREVIEW | stop | Exact approval authorizes one delegated Common Lookups type or code update followed by verification |
| CCL.READY_DELETE | terminal | 22 | terminal | none | CCL.PREVIEW | stop | Exact approval authorizes one delegated Common Lookups type or code delete followed by verification |
| CCL.DONE_CHANGE | terminal | 23 | terminal | none | CCL.VERIFY_RESOURCE | stop | The approved Common Lookup mutation has been freshly verified |
| RETURN_ISSUES | terminal | 24 | terminal | none | none | stop | Business-language error disclosure is complete |
