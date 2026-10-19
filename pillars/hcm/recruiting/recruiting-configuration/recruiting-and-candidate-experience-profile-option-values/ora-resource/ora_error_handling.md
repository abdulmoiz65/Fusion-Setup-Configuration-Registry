# Error Handling

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Review result | Business result first; approved ownership source/version and module display name; only current provider-returned fields; sensitive values redacted; technical identifiers only when useful or requested. |
| Before configured-value mutation | Concise business outcome, current redacted state, requested change, impact, unchanged configuration, exact environment, ProfileOptionName, ownership receipt, level/scope, verification read, and approval fingerprint. |
| Approval | One explicit approval bound to the exact immutable preview immediately before one create, update, or delete. |
| Post-change | Fresh exact scoped state for create/update or verified exact-item absence for delete, plus sanitized diagnostic and project artifact references. |

## Baseline and Crosswalk Refresh Rules

| Situation | What Should Happen |
|---|---|
| Approved Supported Modules page has a newer version or the allowlist is known to be stale | Use Chrome read-only to replace the complete allowlist from the Supported Modules table; include only concrete LBA ModuleId rows and record the new source version and date. |
| Supported Modules page is unavailable or its table is incomplete | Keep the last version labeled with its evidence date, report the refresh blocker, and do not authorize an unlisted ModuleId. |
| Approved ProfileOptionName ownership crosswalk is missing, stale, or incomplete | Obtain a separately approved current artifact containing every required contract field; do not derive mappings from profile names, descriptions, prefixes, effective values, or the ModuleId allowlist. |
| Fusion runtime information is needed | Use Common Profile Options only; never use browser automation against Fusion or duplicate its transport/authentication. |

## Error Situations

| Situation | What Should Happen |
|---|---|
| Business request is genuinely ambiguous | Ask one concise business question; do not require technical vocabulary. |
| Approved ownership crosswalk is absent, stale, ambiguous, or lacks the exact ProfileOptionName | Classify as a catalog mismatch, identify the missing approved evidence, and stop every profile-specific read or mutation. |
| Crosswalk ModuleId is absent from the complete maintained allowlist | Explain that Recruiting ownership is not established and stop without another route. |
| Exact definition has no match or multiple matches | Return sanitized exact-match evidence and stop before configured-value access or mutation. |
| Requested level is not both currently enabled and updatable | Explain the unsupported Site, Product, or User capability and stop. |
| Product technical scope key is absent, stale, or ambiguous | Request current approved scope evidence and stop; do not use a display label. |
| User identity or GUID is absent or ambiguous | Report the provider resolution issue and stop; do not infer identity from a display name. |
| Exact scoped configured value has no match or multiple matches | A no-match may prove create absence only after a complete supported read; otherwise report sanitized evidence and stop. |
| Profile-definition change is requested | Explain that the provider exposes definition reads but this task supports no profile-definition CRUD; do not propose a bypass. |
| Sensitive value would be exposed or persisted | Replace it with a redacted comparison and stop if safe execution cannot preserve confidentiality. |
| Approval is missing, stale, or bound to different environment, ownership, identity, level, scope, state, or delta | Regenerate the immutable preview and obtain fresh exact approval. |
| Mutation response is uncertain | Preserve sanitized diagnostics and stop; do not retry automatically. |
| Fresh verification differs from the approved result | Report the exact sanitized discrepancy and stop without a corrective mutation. |
| Diagnostic, run, approval, or token record cannot be persisted | Report the intended project location and stop before claiming durable completion. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing business outcome, operation, exact ProfileOptionName, environment, selected level/scope, or configured-value delta | Request only the missing decision or value. |
| Catalog mismatch | Missing/stale ownership crosswalk, nonallowlisted ModuleId, unsupported definition change, or unapproved route | Explain the evidence or capability boundary and stop. |
| Auth/authz | Common Profile Options cannot read or mutate with current identity or `FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV` is unavailable for mutation | Follow the delegated provider's permitted cached-token refresh once, then stop if unresolved. |
| Transport/environment | Network response, environment identity, or mutation outcome is uncertain | Persist sanitized evidence and stop without mutation retry. |
| Fusion API | Exact definition, level metadata, configured item, user resolution, or verification state fails | Report current response-grounded evidence and stop. |
| Process timeout | A delegated provider operation times out | Record the environment, operation, elapsed wait, last known status, and safe next-check path; do not retry a mutation. |
| Process failed | A delegated external operation reports failure | Persist sanitized returned diagnostics and external identifiers, then stop. |
| Artifact persistence | Required project audit evidence cannot be written | Report the destination and do not claim completion. |
| Approval blocker | Exact immutable approval is absent or stale | Re-preview and request approval immediately before the one action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Profile-definition request | Do not create, update, delete, or alter the parent profile-option definition. |
| Ownership gap | Do not infer Recruiting ownership from a profile name, prefix, description, value, effective result, module baseline, or user assertion. |
| Level/scope gap | Do not infer editability, Product application keys, UserName, or user GUID. |
| Alternative transport | Do not use direct REST URLs, curl, browser automation, UI, OAuth handling, FSM, export/import, or another route to bypass Common Profile Options or an unsupported request. |
| Uncertain mutation | Do not retry automatically. |
| Sensitive evidence | Do not display or persist credentials, tokens, headers, raw sensitive configured values, or protected payloads. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RPO.PREVIEW | decision | 8 | execution_gate | approved_create->RPO.READY_CREATE;approved_update->RPO.READY_UPDATE;approved_delete->RPO.READY_DELETE;missing->RPO.APPROVAL_ISSUES | RPO.ENFORCE | stop | A supported configured-value mutation has a complete immutable preview |
| RPO.INPUT_ISSUES | step | 10 | error_handler | disclosed->RPO.RETURN_ISSUES | none | stop | Business intake, exact identity, environment, level, scope, operation, or delta is incomplete or ambiguous |
| RPO.EVIDENCE_ISSUES | step | 11 | error_handler | disclosed->RPO.RETURN_ISSUES | none | stop | Required baseline, crosswalk, definition, scope, current-value, or verification dependency is unavailable |
| RPO.OWNERSHIP_ISSUES | step | 12 | error_handler | disclosed->RPO.RETURN_ISSUES | none | stop | Exact ProfileOptionName ownership cannot be established from the approved crosswalk and complete baseline |
| RPO.LOOKUP_ISSUES | step | 13 | error_handler | disclosed->RPO.RETURN_ISSUES | none | stop | Effective-value, definition, configured-item, Product scope, User identity, or verification resolution fails |
| RPO.DESIGN_ISSUES | step | 14 | error_handler | disclosed->RPO.RETURN_ISSUES | none | stop | Definition boundary, level capability, scope, preservation, sensitive-data, or route enforcement fails |
| RPO.APPROVAL_ISSUES | step | 15 | error_handler | disclosed->RPO.RETURN_ISSUES | none | stop | Exact immutable approval is absent or stale |
| RPO.POST_CHANGE_ISSUES | step | 16 | error_handler | disclosed->RPO.RETURN_ISSUES | none | stop | Post-mutation verification is missing, mismatched, or uncertain |
| RPO.DONE_EFFECTIVE | terminal | 17 | terminal | none | RPO.MATCH_OWNERSHIP | stop | Current-session Recruiting-owned effective-value review is complete |
| RPO.DONE_DEFINITION | terminal | 18 | terminal | none | RPO.READ_DEFINITION | stop | Exact approved profile-definition review is complete |
| RPO.DONE_CONFIGURED | terminal | 19 | terminal | none | RPO.RESOLVE_SCOPE | stop | Exact approved configured-value review is complete |
| RPO.READY_CREATE | terminal | 20 | terminal | none | RPO.PREVIEW | stop | Exact approval authorizes one delegated configured-value create followed by fresh verification |
| RPO.READY_UPDATE | terminal | 21 | terminal | none | RPO.PREVIEW | stop | Exact approval authorizes one delegated configured-value update followed by fresh verification |
| RPO.READY_DELETE | terminal | 22 | terminal | none | RPO.PREVIEW | stop | Exact approval authorizes one delegated configured-value delete followed by fresh verification |
| RPO.DONE_CHANGE | terminal | 23 | terminal | none | RPO.VERIFY_VALUE | stop | The approved configured-value mutation has been freshly verified |
| RPO.RETURN_ISSUES | terminal | 24 | terminal | none | none | stop | Business-language error disclosure is complete |
