# Costing of Payrolls Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Search input or selection failure | Classify as input validation. Report the invalid filter or unresolved LDG/period selection and stop; do not remove that filter or switch to HDL. |
| Search response contract failure | Classify as catalog mismatch when expected fields or the documented finder contract are unavailable. Stop without substituting a session route, browser, or another resource. |
| Search request failure | Classify as auth/authz, transport/environment, or Fusion API as appropriate. Use only the declared client's cached-token refresh-once policy for 401/403; do not implement a separate retry or authentication path. |
| Search partial results | Preserve obtained rows in the active result with complete=false and an errors array. Record failure class, failed resolver/page, sanitized message, and the next check. Do not report complete success, zero matches, or a selected identity. |
| Search returns zero rows | This is not an import error. Return an empty search result with complete=true only after complete pagination, and show the applied filters and effective date. |
| Create finds an active allocation | Classify as input validation and stop Create before preparing DAT files. Present Update or same-start Correct as separate operation choices; do not submit MERGE as an implicit update. Correct is not enabled by this Create workflow. |
| Create identity, flex, or segment lookup fails | Classify as input validation for an unresolved selection, catalog mismatch for an invalid/missing contract, or auth/authz, transport/environment, or Fusion API for a failed read. Missing or incomplete GET results never establish absence. |
| Create load is pending | Return pending with the same accepted Content ID and Request ID through the governed resume context. Do not claim success or submit again. Resume the same loader result before verification. |
| Create load partially succeeds or verification differs | Classify as process failed, preserve per-object outcomes and sanitized expected-versus-actual differences with an errors array, and stop. Do not retry the archive or reinterpret the result as Update. |
| Ambiguous Delete, account-only Delete or Delete (ED Split) requested | Classify as input validation and stop with the bounded scope gap. Only explicit Zap or Delete Record And History selects whole-history deletion. |
| Update scope or verification failure | Reject an unsupported history shape, ambiguous or multiple COST target, account addition/removal, or missing baseline before upload. After loading, preserve partial successes and compare expected versus actual history and account facts; do not replay or convert the request to Correct. |
| Input validation failure | Classify as input validation, identify the missing payroll identity, date, account value, or operation, and stop before archive creation. |
| Correct requested | Classify as input validation because Correct is unsupported by this source-backed HDL contract. Stop before archive creation; do not invoke or require a REST write, REST failure, reconciled-failure flag, or fallback approval. |
| Current template rejects the discriminator, metadata header, or identity | Classify as catalog mismatch and stop. Do not infer a replacement header, source key, source type, segment, or execution route. |
| Archive validation or Task Hook validation fails | Classify as artifact persistence or process failed as appropriate; preserve only sanitized diagnostic facts and stop. |
| Approval is absent, stale, or mismatched | Classify as approval blocker and request approval for the exact immutable archive. |
| Authentication, authorization, transport, or Fusion failure | Classify the failure, retain redacted evidence, and stop. Do not retry an import automatically. |
| Import timeout or ambiguous initiation | Classify as process timeout or transport or environment; do not resubmit until the declared status workflow establishes a safe next action. |
| End Date state or date mismatch | Reject a non-last start, attempted extension or missing end before preparing source. A matching end is a verified no-op. Do not reinterpret the request as Update or Correct. |
| End Date special attribute rejected by the loader | Report catalog mismatch with the exact sanitized error and owning validator layer. Preserve ReplaceLastEffectiveEndDate and the prepared source. Do not alter core.data-loader, remove the attribute, suppress the failure or substitute a route. |
| Zap historical detail or DELETE schema failure | Classify as catalog mismatch; retain the exact failure and owning validator. Resolve missing evidence through declared lookups or loader validation. Do not invent physical keys, suppress schema errors, modify core.data-loader or substitute a REST write. |
| Zap partial success, uncertain result or remaining records | Classify as process failed or process timeout, preserve the original loader reference and partial outcomes, and reconcile remaining state through declared reads. Never replay the deletion automatically. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Required operation, identity, date, or account data is invalid or absent, or a Search filter or LDG/period selection is invalid or unresolved. | Correct the supplied source or selection and repeat validation. |
| catalog mismatch | The current loader template conflicts with the authored discriminator contract, or Search lacks a documented response field or finder contract. | Reconcile the template or task-local lookup guidance before retrying. |
| approval blocker | The immutable archive lacks current approval. | Present the exact preview and obtain approval. |
| auth or authz | Authentication or privilege validation fails. | Resolve access without retrying the import. |
| transport or environment | Connectivity or environment identity fails. | Correct the environment issue and revalidate. |
| Fusion API or process failed | The shared loader rejects or fails the approved import. | Preserve sanitized diagnostics and follow the status workflow. |
| process timeout | The initiated import has no final status within the declared wait. | Stop and use the approved status-check path. |
| artifact persistence | The immutable source or validation artifact cannot be safely prepared. | Stop before handoff. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Search result | Show the selected environment, applied effective date, normalized filters, mapped summary rows, and whether pagination completed. Disclose absent flex/costing values and unresolved selections. State that Search performed reads only. |
| Search evidence | Persist only sanitized diagnostics under the active project workspace and its token-usage policy. Never copy raw responses, session links, headers, captured identifiers, or customer values into reusable skill files. |
| Archive preview | Target environment, Create or Update operation, source identity summary, immutable archive fingerprint, expected effect, and approval requirement. |
| Unsupported Correct | State that this task lacks a source-backed HDL Correct contract and that no REST fallback or prior REST failure is permitted. |
| Failure | Failure class, stage, sanitized message, safe artifact reference when available, and one next action. |
| Handoff | That core.data-loader received the approved archive; do not claim completed configuration before the loader reports it. |
| Create preview | Canonical payroll/LDG identity, PAY, requested start, generated 4712/12/31 end, account counts by subtype and normalized proportions, both DAT members, archive fingerprint, source/schema and Task Hook results, and the exact target environment. Use core.data-loader's approval once, after this concrete preview is ready. |
| Create verification | State verified Create only after terminal loader success and matching parent/account reads. Disclose missing, pending, failed, or mismatched facts without exposing raw account values or credentials in durable diagnostics. |
| Update verification | Report verified success only after the exact load succeeds and both history and account comparisons pass. Retain generic verified contract facts in the skill, not customer values, IDs or temporary paths. |
| End Date preview and verification | Show selected payroll/LDG, unchanged start, current end, requested inclusive end and preservation of accounts/history. Do not claim completed End Date until terminal loader success and history/end-date/next-day comparisons pass. |
| Zap preview | Show the canonical payroll/LDG, selector start, every affected interval and distinct physical account counts by subtype. State that the entire logical record/history and accounts will be deleted and HDL provides no undo. Use one approval for the exact validated archive. |
| Zap verification | Require terminal success for every included business object and complete saved-scope absence checks. No failed or missing GET is proof of deletion; disclose unresolved scope. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Search boundary | Do not invoke HDL, archive generation, import approval, or a write from the Search branch. Do not claim account details, full history, mutation readiness, or import verification from summary search results. |
| Execution route | Do not use direct REST, Generic Costing, ADF REST Business Objects, browser replay, a direct Business Objects route, or a raw upload/import call to mutate. A documented task-local REST GET remains read-only evidence only. |
| Unsupported Correct | Do not satisfy Correct with a REST write, a required REST failure, a reconciled-failure flag, or fallback approval. |
| Identity and template | Do not invent a header, source key, source type, account subtype, account segment, percentage, or a sequence outside the documented consecutive default. |
| Mutation | Do not submit an archive without current validation and fresh approval. |
| Failure | Do not replay an uncertain loader submission or make an undocumented substitute call. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COP.SEARCH.DONE | terminal | 7 | terminal | none | COP.SEARCH.FIND | continue | Search completed with found or empty results and complete pagination; return mapped rows, applied filters, and the effective date. |
| COP.SEARCH.DONE_LDG | terminal | 8 | terminal | none | COP.SEARCH.RESOLVE_LDG | continue | The user requested LDG choices/context only; return complete LDG results with their associated flex values and no payroll search. |
| COP.SEARCH.DONE_PERIOD_TYPES | terminal | 9 | terminal | none | COP.SEARCH.RESOLVE_PERIOD | continue | The user requested period-type choices only; return complete code/label choices and no payroll search. |
| COP.HDL.GATE_CREATE | decision | 40 | execution_gate | submitted->COP.CREATE.RESULT;blocked->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.HDL.ENFORCE_ROUTE,COP.CREATE.VALIDATE_SOURCE | stop | The exact Create archive passed source/schema and Task Hook validation, has current prerequisite evidence and core.data-loader approval, and is handed once to core.data-loader. No direct REST write or second approval flow is permitted. |
| COP.CREATE.PENDING | terminal | 43 | terminal | none | COP.CREATE.RESULT | continue | The same Create load is initiated or pending. Return its governed resume reference; a later authorized status check resumes COP.CREATE.RESULT for that handoff without resubmission. |
| COP.HDL.GATE_UPDATE | decision | 50 | execution_gate | submitted->COP.UPDATE.RESULT;blocked->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.HDL.ENFORCE_ROUTE,COP.UPDATE.VALIDATE_SOURCE | stop | The exact Update archive passed source/schema and Task Hook validation, has fresh core.data-loader approval, and is submitted once through that service. |
| COP.CREATE.DONE | terminal | 60 | terminal | none | COP.CREATE.VERIFY | continue | Create is verified through matching parent and account reads after terminal success for both loaded objects. Persist only redacted run and verification facts. |
| COP.UPDATE.DONE | terminal | 70 | terminal | none | COP.UPDATE.VERIFY | continue | Update is verified: prior history/accounts preserved and the new interval matches the approved change and full carried-forward distribution. |
| COP.HDL.HANDLE_ERROR | step | 80 | error_handler | disclosed->COP.HDL.FAILED | none | stop | Any validation, dependency, design, approval, loader, artifact, or unsupported-operation failure. |
| COP.HDL.FAILED | terminal | 90 | terminal | none | COP.HDL.HANDLE_ERROR | continue | The request stopped with a classified diagnostic and safe next action. |
| COP.UPDATE.PENDING | terminal | 53 | terminal | none | COP.UPDATE.RESULT | continue | Return accepted initiation or pending status with the same loader reference. An explicit later status or verification request resumes COP.UPDATE.RESULT without re-submission. |
| COP.END_DATE.NO_CHANGE | terminal | 24 | terminal | none | COP.END_DATE.CHECK_STATE | continue | The selected latest interval already ends on the requested date; report verified state with no load. |
| COP.END_DATE.GATE | decision | 55 | execution_gate | submitted->COP.END_DATE.RESULT;blocked->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.END_DATE.ENFORCE | stop | Submit the exact parent-only archive once through core.data-loader after source/schema and Task Hook success and fresh approval. No direct mutation route. |
| COP.END_DATE.PENDING | terminal | 57 | terminal | none | COP.END_DATE.RESULT | continue | Return the accepted or pending load reference without polling. An explicit later status or verification request resumes the same result. |
| COP.END_DATE.DONE | terminal | 71 | terminal | none | COP.END_DATE.VERIFY | continue | End Date verified: only the latest end changed, prior history and accounts are unchanged, and the parent is absent the following day. |
| COP.ZAP.GATE | decision | 59 | execution_gate | submitted->COP.ZAP.RESULT;blocked->COP.HDL.HANDLE_ERROR;failed->COP.HDL.HANDLE_ERROR | COP.ZAP.ENFORCE | stop | Hand the exact validated Zap archive once to core.data-loader after its single current destructive approval and Task Hook envelope. No direct mutation route. |
| COP.ZAP.PENDING | terminal | 62 | terminal | none | COP.ZAP.RESULT | continue | Return accepted initiation or pending result with saved complete history/account scope and loader reference. Resume only on an explicit status/verification request; do not poll or resubmit automatically. |
| COP.ZAP.DONE | terminal | 72 | terminal | none | COP.ZAP.VERIFY | continue | Zap verified: the selected logical allocation is absent from complete history and every saved historical start returns zero parents and accounts. |
