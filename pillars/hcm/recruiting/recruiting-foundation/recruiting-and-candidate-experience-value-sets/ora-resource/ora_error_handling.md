# Error Handling

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Review result | Business result first; only fields returned by the current API; API ModuleId and baseline-derived module display name where available; technical identifiers only when useful or requested. |
| Before child mutation | Concise business-language outcome, current state, requested change, assumptions, impact, unchanged configuration, exact target environment, parent and child identity, verification read, and approval fingerprint. |
| Approval | One explicit approval bound to the exact immutable preview immediately before one create, update, or delete. |
| Post-change | Fresh exact child state for create/update or verified exact-child absence for delete, plus sanitized diagnostic and project artifact references. |

## Baseline Refresh Rules

| Situation | What Should Happen |
|---|---|
| Approved Supported Modules page has a newer version or the allowlist is known to be stale | Use Chrome read-only to replace the complete allowlist from the Supported Modules table; include only concrete LBA ModuleId rows and record the new source version and date. |
| Supported Modules page is unavailable or its table is incomplete | Keep the last version labeled with its evidence date, report the refresh blocker, and do not authorize an unlisted ModuleId. |
| Fusion runtime information is needed | Use Common Value Sets or the restricted root-pagination fallback; never use browser automation against Fusion. |

## Error Situations

| Situation | What Should Happen |
|---|---|
| Business request is genuinely ambiguous | Ask one concise business question; do not require technical vocabulary. |
| Exact ValueSetCode is missing for a particular value set | Ask for the exact code and stop; do not infer it from a label, description, prefix, or approximate match. |
| Root listing returns `hasMore=true` without usable offset or limit and Common Value Sets has no safe continuation | Classify as a pagination blocker and stop without guessing parameters. |
| Exact root or child has no match or multiple matches | Return the sanitized match evidence and stop before mutation. |
| Current root response lacks ModuleId | Explain that module-scoped ownership cannot be evaluated and stop. |
| ModuleId is outside the allowlist | Explain that the value set is outside this Recruiting task and stop without another route. |
| Parent validation behavior, child capability, requested field, or protection state is not established | Explain the unsupported boundary and stop without inferring editability. |
| Root-definition change is requested | Explain that Common Value Sets supports root reads but not root definition CRUD; do not propose direct REST, UI, or FSM bypass. |
| Approval is missing, stale, or bound to different identities, environment, state, or delta | Regenerate the immutable preview and obtain fresh exact approval. |
| Mutation response is uncertain | Preserve sanitized diagnostics and stop; do not retry automatically. |
| Fresh verification differs from the approved result | Report the exact sanitized discrepancy and stop without a corrective mutation. |
| Diagnostic, run, approval, or token record cannot be persisted | Report the intended project location and stop before claiming durable completion. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing business decision, operation, exact code, environment, or child delta | Request only the missing decision. |
| Catalog mismatch | Another task, unsupported root definition, nonallowlisted ModuleId, or unapproved route | Explain the boundary and stop. |
| Auth/authz | Common Value Sets or restricted REST client cannot read or mutate with current privileges | Follow the delegated provider's permitted token-refresh behavior once, then stop if unresolved. |
| Transport/environment | Page continuation, network response, or mutation outcome is uncertain | Persist sanitized evidence and stop without mutation retry. |
| Fusion API | Exact resource, capability, protection, or verification state fails | Report current response-grounded evidence and stop. |
| Artifact persistence | Required project audit evidence cannot be written | Report the destination and do not claim completion. |
| Approval blocker | Exact immutable approval is absent or stale | Re-preview and request approval immediately before the one action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Root-definition request | Do not create, update, delete, or alter a root value-set definition. |
| Unsupported child capability | Do not infer manageability merely because a child resource exists. |
| Ownership gap | Do not infer Recruiting ownership from a value-set code, name, description, prefix, export, or user assertion. |
| Identity shortcut | Do not derive a child identifier from its value or require numeric root discovery when the user supplied an exact ValueSetCode. |
| Alternative transport | Do not use curl, browser automation, FSM, export/import, UI, or another route to bypass the supported boundary. |
| Uncertain mutation | Do not retry automatically. |
| Sensitive evidence | Do not persist credentials, tokens, headers, or sensitive values. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RVS.PREVIEW | decision | 8 | execution_gate | approved_create->RVS.READY_CREATE;approved_update->RVS.READY_UPDATE;approved_delete->RVS.READY_DELETE;missing->RVS.APPROVAL_ISSUES | RVS.ENFORCE | stop | A supported child mutation has a complete immutable preview |
| RVS.INPUT_ISSUES | step | 10 | error_handler | disclosed->RETURN_ISSUES | none | stop | Business intake, exact code, environment, or operation is incomplete or ambiguous |
| RVS.LOOKUP_ISSUES | step | 11 | error_handler | disclosed->RETURN_ISSUES | none | stop | Pagination, root, validation-metadata, or child resolution fails |
| RVS.OWNERSHIP_ISSUES | step | 12 | error_handler | disclosed->RETURN_ISSUES | none | stop | Current ModuleId ownership cannot be established from the complete baseline |
| RVS.DESIGN_ISSUES | step | 13 | error_handler | disclosed->RETURN_ISSUES | none | stop | Root boundary, child capability, field support, preservation, or route enforcement fails |
| RVS.APPROVAL_ISSUES | step | 14 | error_handler | disclosed->RETURN_ISSUES | none | stop | Exact immutable approval is absent or stale |
| RVS.POST_CHANGE_ISSUES | step | 15 | error_handler | disclosed->RETURN_ISSUES | none | stop | Post-mutation verification is missing, mismatched, or uncertain |
| RVS.DONE_ROOT_REVIEW | terminal | 16 | terminal | none | RVS.MATCH_SCOPE | stop | Recruiting-owned root review is complete |
| RVS.DONE_VALIDATION | terminal | 17 | terminal | none | RVS.READ_VALIDATION | stop | Requested validation-table metadata review is complete |
| RVS.DONE_CHILD_REVIEW | terminal | 18 | terminal | none | RVS.RESOLVE_CHILD | stop | Requested child-value review is complete |
| RVS.READY_CREATE | terminal | 19 | terminal | none | RVS.PREVIEW | stop | Exact approval authorizes one delegated Common Value Sets child create followed by fresh verification |
| RVS.READY_UPDATE | terminal | 20 | terminal | none | RVS.PREVIEW | stop | Exact approval authorizes one delegated Common Value Sets child update followed by fresh verification |
| RVS.READY_DELETE | terminal | 21 | terminal | none | RVS.PREVIEW | stop | Exact approval authorizes one delegated Common Value Sets child delete followed by fresh verification |
| RVS.DONE_CHANGE | terminal | 22 | terminal | none | RVS.VERIFY_CHILD | stop | The approved child mutation has been freshly verified |
| RETURN_ISSUES | terminal | 23 | terminal | none | none | stop | Business-language error disclosure is complete |
