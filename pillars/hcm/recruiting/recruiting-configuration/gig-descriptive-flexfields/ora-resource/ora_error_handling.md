# Gig Descriptive Flexfields Error Handling

Global create, copy, update, and disable may use the [verified fallback export contract](ora_gig_global_segment_archive_contract.md), after a selected-environment exact-task export attempt fails, times out, or returns unusable rows. Confirm the complete design and disclose unavailable current-state checks as `UNVERIFIED`. Verification and context-sensitive work require a validated populated current-definition package. Global copy/update/disable use the confirmed fallback rules when fresh evidence is unavailable. Standalone list/inspect still requires a fresh export.

Classify task-local failures, disclose sanitized evidence, and stop before retry. Resource guidance does not authorize Fusion authentication, setup mutation, deployment, export/import, or package reconstruction.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Exact task, DFF, context, or required segment is absent | Return MISSING with the expected identity and stop |
| Multiple contexts, segments, or value sets match | Return AMBIGUOUS and require one exact target |
| A Referral context or another DFF is supplied | Return UNSUPPORTED and do not map or process it |
| Create, update, or copy input is incomplete | Ask for the segment name first if it is absent. Once the name is known, analyse the latest validated matching package or a fresh export and present all derivable values together for confirmation or change; then ask only for any remaining required value. |
| An Inspect/list request cannot produce a valid exact-task export | Return BLOCKED with the export stage and stop without browser, database, direct DFF API, or Referral-artifact fallback |
| A fresh Gig setup-data export is header-only or lacks the IRC_MP_GIGS_DFF/application-821 root row | Global create, copy, update, and disable may use the verified structural contract after an export attempt fails, times out, or returns unusable rows; validate checksum and identity, confirm the complete design, disclose unverified current-state checks, and build exactly one operation-specific Global delta. Verification and context-sensitive work require a validated populated current-definition package; Global copy/update/disable may use the confirmed fallback. For list/inspect, use only a fresh export and report no configured segments when empty. |
| Current-definition, context, or value-set evidence is absent, stale, incomplete, or ambiguous | Return BLOCKED with the exact missing runtime dependency and stop |
| Storage, sequence, identifier, value-set, display, runtime compatibility fails | Return BLOCKED with the exact correction required |
| Delete is requested | Return UNSUPPORTED and offer reversible PlanDisable for the exact segment after confirmation |
| Gig FSM package construction or validation is unproven | Return ARTIFACT_PREPARATION and require the authoritative contract; never infer Referral structure |
| Access is missing or rejected | Return AUTHORIZATION and route to the appropriate setup, deployment, or import owner |
| Approval is absent, stale, or bound to another preview | Return APPROVAL_REQUIRED and stop before mutation |
| Save, deployment, import, transport, or result fails or is uncertain | Preserve sanitized stage, status, identifier, and evidence; stop without automatic retry or resubmission |
| An approved create, update, or copy import is accepted | Keep the acceptance response internal, monitor the request to terminal state, retrieve and read the FSM ProcessLog, and return only the final success or error result |
| Completion monitoring reaches a timeout or cannot obtain terminal evidence | Return the request ID, last status, elapsed wait, and one safe status-check action; do not retry the upload or import |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | One required identity, input, source, segment, or approval is absent | Supply only the missing item |
| AMBIGUOUS | More than one target matches | Resolve one exact target |
| CONFLICT | Existing Gig configuration duplicates or overlaps the proposal | Obtain an explicit design decision |
| BLOCKED | Lookup, compatibility, storage, sequence, or deployment readiness fails | Correct the exact blocker and revalidate |
| UNSUPPORTED | The request crosses task, DFF, context, delete, or execution-route boundaries | Return the supported boundary |
| AUTHORIZATION | Required access is absent or rejected | Route to the responsible security or functional owner |
| APPROVAL_REQUIRED | A mutation lacks approval bound to its exact current preview | Obtain approval immediately before execution |
| ARTIFACT_PREPARATION | The Gig FSM artifact cannot be built from a proven contract | Supply or correct the exact package contract |
| PROCESS_FAILED | Save, export, import, or transport failed or is uncertain | Preserve diagnostics and reconcile state without retry |
| PRODUCT_OR_DEPLOYMENT | Deployment or runtime verification failed or is uncertain | Preserve diagnostics and require approval for a safe next attempt |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input correction | Only the affected business field, why it is invalid, and the next concise question |
| Lookup blocker | Resolver, missing or invalid runtime evidence, exact task and DFF, and one safe correction |
| Readiness rejection | Dependency, sanitized evidence, owner or contract gap, and one safe next action |
| Approval gate | Environment, task, DFF, operation, scope, segment, exact delta or archive filename and SHA-256, and verification plan |
| Post-dispatch failure | Environment, operation, sanitized status, process or request identifier when available, last completed stage, and reconciliation action |
| Verification | Approved scope and segment, checked properties, deployment state when applicable, sanitized outcome, and remaining issues |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Another task, DFF, or Referral context is requested | Do not reuse this contract or mutate Referral skill resources |
| A context lifecycle change is requested | Do not create, rename, delete, or substitute a context |
| A browser, undocumented API, direct REST mutation, or database access is proposed | Do not use it as a fallback |
| A table column, sequence, context, value-set identifier, Module, or identifier grammar is unverified | Do not guess, silently truncate, or infer it |
| A copy API name is derived | Do not append _Copy; append Copy without a separator only after validating the authoritative Gig identifier rule |
| A package contract is missing | Do not invent members, filenames, headers, parents, translations, metadata, encoding, or ZIP structure |
| A Gig export is header-only | Global create, copy, update, and disable may use the verified structural contract after an export attempt fails, times out, or returns unusable rows; validate checksum and identity, confirm the complete design, disclose unverified current-state checks, and build exactly one operation-specific Global delta. Verification and context-sensitive work require a validated populated current-definition package; Global copy/update/disable may use the confirmed fallback. For list/inspect, use only a fresh export and report no configured segments when empty. |
| Approval is missing or stale | Do not save, deploy, upload, or import |
| A state-changing action was dispatched | Do not retry, replay, replace, or resubmit it; status monitoring and ProcessLog retrieval are required only after an accepted create, update, or copy request ID |
| Runtime Gig, applicant, or personal data is observed | Do not persist it in resources or diagnostics |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GIG_DFF.APPROVAL_GATE | decision | 50 | execution_gate | approved->GIG_DFF.EXECUTE;not_required->GIG_DFF.EXECUTE;missing->GIG_DFF.RETURN_ISSUES;stale->GIG_DFF.RETURN_ISSUES | GIG_DFF.ENFORCE_DESIGN | stop | Require approval for any mutation; read-only inspection and planning use not_required |
| GIG_DFF.EXECUTE | decision | 60 | execution_gate | planned->GIG_DFF.RETURN_PLAN_SUCCESS;configured->GIG_DFF.RETURN_SEGMENT_SUCCESS;import_accepted->GIG_DFF.MONITOR_IMPORT;verify_requested->GIG_DFF.VERIFY;failed->GIG_DFF.RETURN_ISSUES;uncertain->GIG_DFF.RETURN_ISSUES;unsupported->GIG_DFF.RETURN_ISSUES | GIG_DFF.APPROVAL_GATE | stop | For create, update, or copy, build and validate the immutable Gig package from the analysed validated package and confirmed inputs; after core.data-loader approval, upload and initiate once and keep an accepted request ID internal for required completion monitoring |
| GIG_DFF.RETURN_PLAN_SUCCESS | terminal | 90 | terminal | none | GIG_DFF.EXECUTE | stop | A supported read-only inspection or plan completed without a Fusion mutation |
| GIG_DFF.RETURN_SEGMENT_SUCCESS | terminal | 91 | terminal | none | GIG_DFF.EXECUTE | stop | An approved segment configuration action completed with reported evidence |
| GIG_DFF.RETURN_IMPORT_SUCCESS | terminal | 93 | terminal | none | GIG_DFF.MONITOR_IMPORT | stop | Terminal status and the reviewed ProcessLog confirm clean completion; report only that the segment operation completed successfully and link the ProcessLog |
| GIG_DFF.RETURN_VERIFY_SUCCESS | terminal | 94 | terminal | none | GIG_DFF.VERIFY | stop | A separate verification request completed against the approved Gig design |
| GIG_DFF.RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any missing input, ambiguity, conflict, blocker, refusal, authorization failure, stale approval, failed action, or uncertain result |
