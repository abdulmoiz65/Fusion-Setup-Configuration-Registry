# Payroll Components Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A Correct, Update, Delete, or unlisted lifecycle mutation is requested | Return PCOMP_HDL_ROUTE_FROZEN before mutation-specific lookup, DAT authoring, preview, approval, upload, or initiation. |
| End Date, translation Create, Calculation Card reference, or specific-tax-unit assignment is requested | Return UNSUPPORTED before DAT authoring because the delivered native contract lacks the required date behavior, action, field, or discriminator. |
| Parent Create duplicate proof is incomplete | Complete pagination and exact Deduction Code plus LDG comparison; do not treat a partial zero as READY. |
| Parent Create duplicate proof finds one or more exact matches | Return CONFLICT and ask for a different business code or offer a read of the existing row. |
| A required LDG, group, parent, context, or business value is missing | Return NEEDS_INPUT and run only the applicable declared read-only resolver. |
| A resolver returns zero required target rows | Return NOT_FOUND and preserve the supplied business value and scope; do not guess. |
| A resolver returns multiple exact target rows | Return AMBIGUOUS and show only distinguishing business attributes; never expose IDs. |
| Child duplicate proof is incomplete | Return CATALOG_MISMATCH and stop before DAT authoring. |
| Child duplicate proof finds one or more exact business-key matches | Return CONFLICT and stop before DAT authoring. |
| A child Create has no Source System Owner selection | Return NEEDS_INPUT and run the Fusion common-lookup resolver; never default or hardcode an owner. |
| The Source System Owner lookup has zero eligible rows | Return NOT_FOUND and stop before source-ID allocation. |
| A supplied Source System Owner code is inactive, reserved, overlength, or otherwise invalid | Return INPUT_VALIDATION and require another Fusion LOV selection. |
| A supplied Source System Owner meaning matches multiple eligible codes | Return AMBIGUOUS, show the codes only as disambiguators, and require one exact selection. |
| A Source System Owner change or loss of eligibility after artifact validation is known or reported by the user | Return STALE_PLAN and rebuild through core/data-loader; do not add an approval-time refresh lookup. |
| Data Loader rejects a lookup-valid selected source owner | Return PROCESS_FAILED with the core report and preserved sanitized diagnostics; do not select another owner or retry automatically. |
| Calculation Factor Create targets production before direct native QA evidence is retained | Return QA_EVIDENCE_REQUIRED for that target and direct the case to the designated nonproduction QA environment. |
| Current metadata, template, field order, hierarchy, normal core validation evidence, or immutable bytes differ from the contract | Return CATALOG_MISMATCH and preserve sanitized evidence for contract review. |
| Authentication or authorization fails before dispatch | Return AUTH_AUTHZ and delegate to the current core authentication policy. If its permitted refresh is unavailable or still fails, stop and ask the authorized user to refresh the configured session or correct privileges; never inspect or expose token-cache contents. |
| Transport or service availability fails before dispatch | Return TRANSPORT_ENVIRONMENT; preserve sanitized diagnostics and resume only after recovery and fresh validation. |
| Core classifies a post-boundary failure as possibly having crossed the write boundary | Return OUTCOME_UNKNOWN, preserve known receipt/request identifiers, and reconcile the original operation read-only; never replay automatically. A definitive UCM upload rejection follows the core no-load-initiated report instead. |
| Data Loader reports terminal failure | Return PROCESS_FAILED, retrieve sanitized request detail and process log when available, and do not replay without a new plan and approval. |
| Data Loader succeeds but exact product REST read-back is absent or mismatched | Return CONTRACT_INCOMPLETE, preserve evidence, and do not replay. |
| A later operation fails after an earlier separate archive succeeded | Return PARTIAL_COMMIT and reconcile every dispatched request independently; never claim atomic rollback. |
| Secret or session material appears in persistent state | Return SECRET_EXPOSURE, stop, remove it from artifacts, and notify the authorized owner when rotation may be required. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| NEEDS_INPUT | A user-owned business value is absent | Collect or resolve only that requirement |
| INPUT_VALIDATION | An authored value violates the declared format or safe DAT representation | Explain the field rule and collect a corrected value |
| NOT_FOUND | A required exact target lookup returns zero rows | Report the business scope and stop |
| AMBIGUOUS | Multiple exact target rows remain | Present business-facing distinctions and require selection |
| CONFLICT | A Create duplicate exists | Stop; use a new identity or read the existing row |
| STALE_PLAN | Target, lookup, template, duplicate proof, archive, or fingerprint changed | Invalidate approval and rerun core preparation plus Task Hook validation |
| CATALOG_MISMATCH | Current source behavior conflicts with the compiled contract | Stop and review the contract with sanitized evidence |
| QA_EVIDENCE_REQUIRED | A Fusion-valid same-shape Create case lacks direct native proof for the requested environment class | Use only the designated verified nonproduction QA target until evidence is retained |
| UNSUPPORTED | The delivered native shape lacks the required action, field, discriminator, or date behavior | Record future-work scope; do not substitute REST writes |
| PCOMP_HDL_ROUTE_FROZEN | The mutation is outside the current create-only allowlist | Stop before mutation preparation |
| AUTH_AUTHZ | Session identity, privilege, or data security blocks a pre-dispatch read | User refreshes the session or corrects access, then all stale reads are rebuilt |
| TRANSPORT_ENVIRONMENT | Network or service failure occurs before dispatch | Resume only after recovery and fresh preflight |
| OUTCOME_UNKNOWN | A failure occurs after a write may have crossed the boundary | Reconcile the original operation only; zero automatic retries |
| PROCESS_FAILED | Fusion reports terminal loader failure | Preserve process detail/log and diagnose before any new approved operation |
| CONTRACT_INCOMPLETE | Loader success lacks the required exact business state | Preserve evidence and review the contract; do not replay |
| PARTIAL_COMMIT | Separate earlier requests may have succeeded | Reconcile each request and report partial results |
| SECRET_EXPOSURE | Sensitive material entered persistent output | Stop, redact/remove, and follow security handling |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation or lookup blocker | Business field or scope, result category, safe reason, and the next corrective action |
| Approval-required result | Use the complete authoritative core/data-loader Markdown report verbatim; keep the task preview and artifact digest internal and do not add task-local output |
| Loader timeout or unavailable status | Return the complete authoritative core/data-loader helper report verbatim; add no task-local fields or restyling |
| Loader failure | Return the complete authoritative core/data-loader helper report verbatim; preserve task-specific evidence internally and add no task-local output |
| Reconciliation result | Business-facing expected versus observed values and final classification; keep IDs, source keys, links, credentials, and token data internal |
| Explicitly requested task-owned diagnostic file | Persist only the requested sanitized task-validation facts when the requester names a specific output file; never create or augment a core loader report or run artifact |

## Dispatch and Later Status Verification

The task hands its immutable unapproved plan to `core/data-loader` and adds no
task-local transport, upload, initiation, retry, polling, or output behavior.
Core owns approval rendering, persisted artifact verification, Task Hook
envelopes, upload, initiation, its narrowly documented recoverable fallback,
and the accepted-initiation report. Do not automatically poll after accepted
initiation. A later status request uses the core status workflow against the
original request and returns its helper report verbatim. After authoritative
loader success, a separate explicit business-verification request may apply
this task's exact read-back and return only the task reconciliation result; do
not prepend or append it to a core helper report. An uncertain write is never
replayed.

## Reconciliation Rules

| Operation | Authoritative Read-Back |
|---|---|
| create_parent | Require one intended loader row loaded and zero failed, then completely discover the exact Deduction Code plus LDG and issue the exact parent item GET. Compare component code, name, LDG, Component Group, Display Sequence, and all-tax-units behavior. |
| create_reference_t | Require one intended child row loaded and zero failed, then completely paginate the fresh child collection and require exactly one row matching parent, LDG, context, UsageType T, Sequence, and Display in Overview. Retain the generated identity and operation source key internally. |
| create_reference_c | Require one intended child row loaded and zero failed, then completely paginate the fresh child collection and require exactly one row matching parent, LDG, context, UsageType C, Sequence, and Display in Overview. Retain the generated identity and operation source key internally. |

A mismatch after authoritative loader success is `CONTRACT_INCOMPLETE`. An
exact read-back moves the task reconciliation to `succeeded` and returns only
business-facing results. This is a separate read-only result, not an addition
to any core/data-loader helper report. No reconciliation read authorizes
another mutation.

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Target or reference is unresolved | Do not author a DAT, fabricate an ID, or ask the user for a surrogate ID. |
| The immutable artifact, internal Task Hook preview, envelope, or required core approval is absent, changed, or stale | Do not upload or initiate Data Loader. |
| A write response is uncertain | Do not replay upload or initiation automatically. |
| Product REST or historical HAR shows a write shape | Do not use it as a mutation fallback for this task. |
| Current metadata includes additional fields or actions | Do not broaden the create allowlist automatically. |
| An unexpected field is supplied | Do not silently strip it; classify and disclose the blocker. |
| A token, credential, cookie, CSRF value, or session file is encountered | Do not print, inspect, copy, or persist its contents. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PCOMP.EXECUTION_GATE | decision | 7 | execution_gate | read_only_ready->PCOMP.DONE_READ_ONLY;controlled_plan_ready->PCOMP.READY_FOR_CONFIRMATION;blocked->PCOMP.HANDLE_ERROR | none | stop | Read-only validation completed, or all Create validation, dependency, lookup, default, native-contract, and design checks completed |
| PCOMP.HANDLE_ERROR | step | 8 | error_handler | disclosed->PCOMP.RETURN_ISSUES | none | continue | A prior node reports a blocking or failed outcome |
| PCOMP.READY_FOR_CONFIRMATION | terminal | 9 | terminal | none | PCOMP.EXECUTION_GATE | continue | A supported Create archive passed Task Hook validation and is returned to core/data-loader for its approval lifecycle |
| PCOMP.DONE_READ_ONLY | terminal | 10 | terminal | none | PCOMP.EXECUTION_GATE | continue | A requested read or reconciliation is complete |
| PCOMP.RETURN_ISSUES | terminal | 11 | terminal | none | none | continue | Blocking or failure details are safely disclosed |
