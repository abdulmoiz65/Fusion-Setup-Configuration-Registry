# Costing of Elements Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Lookup input or selection failure | Return missing business selectors, unresolved candidates or the invalid filter while preserving the requested operation. Do not require unresolved HDL keys before discovery or broaden the search. |
| Search request failure | Classify auth/authz, transport/environment or Fusion API failures. Delegate the single cached-token 401/403 refresh to the shared client; do not add another retry or authentication path. |
| Search response or route mismatch | Classify catalog mismatch for missing fields, invalid pagination, conflicting result keys, or unavailable rewritten resource/finder. Stop without reverting to rv, browser replay or an undocumented endpoint. |
| Search partial result | Preserve obtained rows in memory with complete=false, errors and next_offset. Report the failed resolver/page and safe resume context, including requested_operation. Partial evidence cannot satisfy any operation's identity requirements. |
| Operation target not found or ambiguous | Return not found or candidate selection without entering HDL validation. An empty search is not proof that a new eligibility costing can be created. |
| HDL input validation failure | Classify as input validation, identify the missing element identity, date, CostInfoV3 value, account value, or operation, and stop before archive creation. |
| Unsupported operation scope | Correct account/date/new-input changes and split-only, account-only or CostInfo-only deletion stop as unsupported. Supported EL/LIV corrections and complete-history Zap follow their own HDL branches. Never substitute a REST write. |
| End Date range or scope invalid | Classify input validation for missing end date, non-latest target, extension, incompatible independent intervals or unrelated value changes. Missing/ambiguous EL/LIV evidence is a catalog mismatch. Stop the complete operation; do not silently fall back to allocation-only, reinterpret as Update or infer a closing date. |
| End Date special attribute rejected by Data Loader | Classify catalog mismatch, identify the affected component, disclose the exact sanitized wrapper error and retain all prepared DATs/ZIP with loader_validated=false. Do not remove ReplaceLastEffectiveEndDate, drop a component, patch the validator, substitute SET, upload or request approval as though validation passed. This limitation does not erase the authored End Date contract. |
| Runtime values or history are incomplete | Classify malformed/missing KFF, LOV, child collections or conflicting intervals as catalog mismatch; invalid requested values as input validation. Retain valid inputs and request only the unresolved business value. |
| Costing read proportions | Normalize only through the documented percentage contract. A malformed/unknown unit blocks; never use a value-size heuristic. |
| Loader template retrieval fails | Report object and failing metadata/download stage. A single capped unfiltered page cannot establish that the object is unavailable; use the declared targeted loader resolution. Do not invent IDs, replay historical URLs or modify the shared client to bypass a schema failure. |
| Current template rejects an ordinary discriminator, metadata header, or identity | Classify as catalog mismatch and stop. Do not infer a replacement header, source key, segment, or execution route. |
| Archive validation or Task Hook validation fails | Classify as artifact persistence or process failed as appropriate; preserve only sanitized diagnostic facts and stop. |
| Approval is absent, stale, or mismatched | Classify as approval blocker and request approval for the exact immutable archive. |
| End Date freshness or verification failure | Before submission, changed/incomplete state is an approval blocker and invalidates the saved approval without altering the approved archive. After submission, a failed comparison is an unverified/partial result; report missing or changed facts and never replay the load. |
| Authentication, authorization, transport, or Fusion failure | Classify the failure, retain redacted evidence, and stop. Do not retry an import automatically. |
| Import timeout or ambiguous initiation | Classify as process timeout or transport or environment; do not resubmit until the declared status workflow establishes a safe next action. |
| Zap history or target mismatch | Classify missing/incomplete history, physical IDs, child expansions, misaligned/shared CostInfo or conflicting duplicates as catalog mismatch; an unmatched selector is input validation. Stop before preparing a partial deletion. Empty allocation history is not proof that independent CostInfo is absent. |
| Zap DELETE validation failure | Identify the failing object/source type, rejected key or capability as catalog mismatch. Keep sanitized diagnostics and stop the entire handoff. Do not remove EL/LIV, invent SourceId or PM-specific keys, trial alternative DELETEs, suppress validation or use the End Date artifact-only exception. |
| Zap pending approval | An intact validated preview waiting for the single core.data-loader destructive approval is an expected pause, not a failed load. Resume the saved COE.ZAP.GATE; do not rebuild the ZIP or repeat preapproval discovery. |
| Zap partial or uncertain load | Retain per-object/row results and known successful deletions. Return partial/failed/unverified with the same accepted identifiers and one reconciliation action. No automatic replay, replacement archive or imported payment-source recovery behavior. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Required operation, identity, date, or account data is invalid or absent. | Correct the supplied source and repeat validation. |
| catalog mismatch | The current loader template conflicts with the authored discriminator contract. | Reconcile against the current approved template. |
| approval blocker | The immutable archive lacks current approval. | Present the exact preview and obtain approval. |
| auth or authz | Authentication or privilege validation fails. | Resolve access without retrying the import. |
| transport or environment | Connectivity or environment identity fails. | Correct the environment issue and revalidate. |
| Fusion API or process failed | The shared loader rejects or fails the approved import. | Preserve sanitized diagnostics and follow the status workflow. |
| process timeout | The initiated import has no final status within the declared wait. | Stop and use the approved status-check path. |
| artifact persistence | The immutable source or validation artifact cannot be safely prepared. | Stop before handoff. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Search result | Show the business result columns, applied filters, effective date and completeness from the lookup contract. Empty complete results and unresolved LDG filters are distinct outcomes. |
| Search diagnostics | Retain only sanitized status, stage, failure class, resolver, pagination state and next action in any required audit record. Do not persist HAR contents, customer result rows, tokens, cookies, internal IDs or audit usernames. |
| Archive preview | Use core.data-loader's report for the target environment, requested operation, business changes and exact validated archive. Keep fingerprints and preflight envelopes internal; do not add a second approval. |
| End Date artifact result | State the complete allocation/EL/LIV target set, each current end and the common requested inclusive end, submitted row counts and any already-closed targets omitted from the change set. Include preserved values, DAT/ZIP links and loader validation status. Artifact prepared is not Fusion End Date completed. |
| Zap preview | Use the loader's exact-archive preview to show environment, element/eligibility/LDG, full earliest-start/latest-end span, historical interval count and allocation/EL/LIV/account DELETE counts. State that the supplied start is a selector and all selected logical history will be removed while source setup and unrelated data remain. |
| Zap completed | Report completion only after all submitted DELETE targets succeeded and Zap Verification passed. Disclose that EL/LIV confirmation combines explicit loader success with saved-scope read-back; an absent parent is not an independent orphan CostInfo query. |
| Operation lookup complete | Retain resolved keys internally and continue the original Create/Update/Correct/End Date workflow without asking the user to re-enter them. If another requirement blocks preparation, report that remaining requirement and the completed discovery. |
| Unsupported write after discovery | Show the resolved business identity and explain which requested operation lacks a write contract. Do not label completed GETs as a completed mutation. |
| Failure | Failure class, stage, sanitized message, safe artifact reference when available, and one next action. |
| Handoff | That core.data-loader received the approved archive; do not claim completed configuration before the loader reports it. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Execution route | Do not use direct REST, Generic Costing, ADF REST Business Objects, browser replay, a direct Business Objects route, or a raw upload/import call to mutate. Only the named read-only LOV POST actions supplement the declared GETs; they never authorize genericCosting CRUD or batch writes. |
| Unsupported writes | Out-of-scope Correct and partial-object/split deletion must not continue to an archive, REST write or another operation's approval gate. |
| Approval resume | Resume the matching retained preview and immutable bytes; do not restart identity discovery, re-render or replace the archive. End Date additionally runs COE.END_DATE.RECHECK_STATE for the same identity. Zap freshness completed before its approval preview and is restored with the saved run. Changed or incomplete evidence/artifacts invalidate approval and require new preparation. |
| Identity and template | Do not invent a header, source key, selector, account subtype, account segment, percentage, or a sequence outside the documented consecutive default. |
| Mutation | Do not submit an archive without current validation and fresh approval. |
| Failure | Do not replay an uncertain loader submission or make an undocumented substitute call. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COE.SEARCH.DONE | terminal | 11 | terminal | none | COE.SEARCH.RETURN_TO_OPERATION | continue | Return the complete list or empty result only for requested_operation=Search. Other operations use identity resolution instead of this terminal. |
| COE.ZAP.GATE | decision | 38 | execution_gate | approved->COE.ZAP.SUBMIT;awaiting_approval->COE.ZAP.AWAITING_APPROVAL;validated_only->COE.ZAP.VALIDATED;blocked->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.ZAP.REFRESH | stop | Apply Zap Scope and Handoff. Validation-only returns its validated deliverables without approval/upload. Execution requires persisted preflight and Task Hook preview for the complete destructive scope before awaiting_approval. Contextual approval restores this gate and completed preparation, then verifies exact bytes and bound context through core.data-loader; no duplicate pillar confirmation, discovery or rebuild. |
| COE.ZAP.SUBMIT | decision | 39 | execution_gate | submitted->COE.ZAP.PENDING;blocked->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.ZAP.GATE | stop | Hand off the exact approved immutable DELETE archive once through core.data-loader with its preserved preflight and taskValidationEnvelope. Bind accepted identifiers to the complete target inventory and baseline; no automatic retries or polling. |
| COE.HDL.GATE_CREATE | decision | 40 | execution_gate | approved->COE.HDL.READY_CREATE;blocked->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.HDL.ENFORCE_ROUTE | stop | A Create archive passed validation and has fresh approval for core.data-loader handoff. |
| COE.HDL.GATE_UPDATE | decision | 50 | execution_gate | approved->COE.HDL.READY_UPDATE;blocked->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.HDL.ENFORCE_ROUTE | stop | An Update archive passed validation and has fresh approval for core.data-loader handoff. |
| COE.HDL.GATE_CORRECT | decision | 55 | execution_gate | approved->COE.HDL.READY_CORRECT;blocked->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.HDL.ENFORCE_ROUTE | stop | Supported Correct archive and Task Hook have passed; use the single current core.data-loader approval. |
| COE.HDL.GATE_END_DATE | decision | 56 | execution_gate | approved->COE.END_DATE.RECHECK_STATE;blocked->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.HDL.ENFORCE_ROUTE | stop | Require the complete End Date change-set archive with full loader/schema and Task Hook validation for every member plus the single core.data-loader approval bound to exact bytes, environment and the allocation/EL/LIV expected result. Approved proceeds to the separate state recheck; this gate performs no reads or submission. Artifact-only output cannot enter it. |
| COE.END_DATE.SUBMIT | decision | 58 | execution_gate | submitted->COE.END_DATE.PENDING;blocked->COE.HDL.HANDLE_ERROR;failed->COE.HDL.HANDLE_ERROR | COE.END_DATE.RECHECK_STATE | stop | Require unchanged state and still-valid exact-artifact approval; submit once through core.data-loader. Capture the actual accepted load reference. An ambiguous or failed initiation stops with diagnostics and never automatically replays. |
| COE.HDL.READY_CREATE | terminal | 60 | terminal | none | COE.HDL.GATE_CREATE | continue | The approved Create archive is ready for core.data-loader handoff. |
| COE.ZAP.DONE | terminal | 64 | terminal | none | COE.ZAP.VERIFY | continue | All submitted DELETE targets succeeded and Zap Verification passed for the complete selected logical history, accounts and EL/LIV. Report preserved eligibility/unrelated state and the independent CostInfo verification boundary. |
| COE.ZAP.STATUS_REPORTED | terminal | 65 | terminal | none | COE.ZAP.RESULT | continue | Return the bound shared loader success report for status-only intent. Business verification was not performed; do not claim confirmed historical removal. |
| COE.ZAP.STATUS_PENDING | terminal | 66 | terminal | none | COE.ZAP.RESULT | continue | Return the bound pending/not-yet-available loader result and retain resume context. No resubmission or automatic polling. |
| COE.ZAP.VALIDATED | terminal | 68 | terminal | none | COE.ZAP.GATE | continue | Explicit validation-only completed with validated sources and archive, without upload or destructive approval. Later execution requires current loader preflight, Task Hook preview and approval. |
| COE.ZAP.PENDING | terminal | 69 | terminal | none | COE.ZAP.SUBMIT | continue | Return the accepted core.data-loader initiation report and save its actual identifiers with the immutable archive and pre-load baseline. Explicit status/verification enters COE.ZAP.VALIDATE_RESUME without submission. |
| COE.HDL.READY_UPDATE | terminal | 70 | terminal | none | COE.HDL.GATE_UPDATE | continue | The approved Update archive is ready for core.data-loader handoff. |
| COE.ZAP.AWAITING_APPROVAL | terminal | 71 | terminal | none | COE.ZAP.GATE | continue | Preparation, complete-target validation, persisted preflight, Task Hook preview and freshness are complete. Return the loader approval-required report; contextual approval resumes the same COE.ZAP.GATE with its completed prerequisites and exact bytes. |
| COE.END_DATE.STATUS_REPORTED | terminal | 72 | terminal | none | COE.END_DATE.RESULT | continue | Return the shared loader success report for an explicit status-only request. Business readback has not been performed; do not claim verified End Date values. |
| COE.END_DATE.STATUS_PENDING | terminal | 73 | terminal | none | COE.END_DATE.RESULT | continue | Return the shared loader pending/not-yet-available result with the retained resume reference. No business verification or resubmission occurred. |
| COE.END_DATE.DONE | terminal | 74 | terminal | none | COE.END_DATE.VERIFY | continue | The bound End Date comparisons passed. For complete_costing report the common verified end for CostAllocation, CostInformation EL and every existing LIV, with preserved values/history. Earlier artifacts retain the limited verification report defined in End Date Read Comparisons; never infer child closure from absence of the allocation. |
| COE.HDL.READY_CORRECT | terminal | 75 | terminal | none | COE.HDL.GATE_CORRECT | continue | Hand off the exact approved correction archive to core.data-loader; this is not completed Fusion costing. |
| COE.END_DATE.PENDING | terminal | 76 | terminal | none | COE.END_DATE.SUBMIT | continue | Return the accepted core.data-loader initiation report and retain the actual load reference bound to the archive and pre-load baseline. A later explicit status/verification request enters COE.END_DATE.VALIDATE_RESUME; never resubmit or poll automatically. |
| COE.END_DATE.PREPARED | terminal | 77 | terminal | none | COE.HDL.VALIDATE_SOURCE | continue | Explicit artifact_only request completed with local source checks and the End Date change-set DAT/ZIP links for the complete target set; loader_validated=false and no upload. Future submission requires full validation and fresh approval. |
| COE.END_DATE.VALIDATION_BLOCKED | terminal | 78 | terminal | none | COE.HDL.VALIDATE_SOURCE | continue | Retain all prepared DATs/ZIP and report the component and exact special-attribute validation failure as catalog mismatch. Not loader-approved, not uploaded and not a completed End Date. |
| COE.END_DATE.UNCHANGED | terminal | 79 | terminal | none | COE.HDL.CHECK_SCOPE | continue | Complete history/detail confirms the latest allocation, EL and every existing LIV already end on the requested date. Return verified no-op for the complete target set; no archive or submission. |
| COE.HDL.HANDLE_ERROR | step | 80 | error_handler | disclosed->COE.HDL.FAILED | none | stop | Shared handler for Search and HDL failures; preserve partial Search evidence and classify the failing stage. |
| COE.HDL.FAILED | terminal | 90 | terminal | none | COE.HDL.HANDLE_ERROR | continue | The request stopped with a classified diagnostic and safe next action. |
| COE.SEARCH.NEEDS_INPUT | terminal | 91 | terminal | none | COE.SEARCH.VALIDATE_INPUT | continue | Request only missing lookup selectors/date, End Date requested end or Zap selector start/LDG, retaining requested_operation; resume common validation when supplied. |
| COE.SEARCH.LDG_NOT_FOUND | terminal | 92 | terminal | none | COE.SEARCH.RESOLVE_LDG | continue | Report no matching LDG and request corrected text or an explicit LDG ID. No element search was run. |
| COE.SEARCH.NEEDS_LDG_SELECTION | terminal | 93 | terminal | none | COE.SEARCH.RESOLVE_LDG | continue | Show candidate names and request selection; resume the LDG resolver with the same context. |
| COE.SEARCH.PARTIAL | terminal | 94 | terminal | none | COE.SEARCH.FETCH | continue | Report complete=false and next_offset. Resume the same lookup with unchanged requested_operation, filters, date and environment; never continue to HDL from partial results. |
| COE.IDENTITY.NEEDS_SELECTION | terminal | 95 | terminal | none | COE.IDENTITY.SELECT | continue | Show candidate business identities, request selection and retain the original operation. Resume identity selection only with matching complete evidence. |
| COE.IDENTITY.NOT_FOUND | terminal | 96 | terminal | none | COE.IDENTITY.SELECT | continue | Report no matching eligibility identity; ask for corrected selectors. Do not infer a new element, eligibility, code or costing source. |
| COE.OPERATION.UNSUPPORTED | terminal | 97 | terminal | none | none | continue | Return resolved identity and the unsupported operation or scope; reached from operation selection or scope validation. No archive or mutation occurred. |
| COE.END_DATE.NEEDS_RESUME_INPUT | terminal | 98 | terminal | none | COE.END_DATE.VALIDATE_RESUME | continue | Request only missing load-to-artifact binding or baseline context for read-only verification. Do not substitute a new End Date, reconstruct a supposed pre-load baseline or upload again. |
| COE.ZAP.NEEDS_RESUME_INPUT | terminal | 99 | terminal | none | COE.ZAP.VALIDATE_RESUME | continue | Request only missing accepted-load binding, immutable target inventory or pre-load evidence. Do not reconstruct deleted physical targets, start a new Zap or upload again. |
