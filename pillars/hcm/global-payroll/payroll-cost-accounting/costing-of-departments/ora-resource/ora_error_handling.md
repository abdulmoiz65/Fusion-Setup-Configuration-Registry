# Department Costing Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required input, exact identity, KFF validation, or effective date is missing, or a Create/effective-dated Update generated SubTypeSequence is invalid. | Classify as input_validation and stop before package generation. |
| A documented GET is malformed, incomplete, unauthorized, or ambiguous. | Classify as catalog_or_metadata_mismatch, auth_authz, or transport_environment and stop. Refresh a cached token once only for a read. |
| Data Loader source/schema or Task Hook validation fails. | Classify as catalog_or_metadata_mismatch or process_failed; preserve redacted diagnostics and do not substitute a route. |
| A loader result fails, times out, or does not verify through GET. | Classify as process_timeout or process_failed; stop without retry and require a new preview and approval. |
| A direct REST mutation or unsupported operation is requested. | Classify as approval_blocker or input_validation and state that only Create, Update, End Date, and Zap HDL are in scope. |
| End Date lacks a separate requested end date, targets a non-last interval, or would extend the selected interval. | Classify as input_validation; request the missing date or correct target. Do not reinterpret End Date as an effective-dated Update. |
| The Data Loader wrapper rejects ReplaceLastEffectiveEndDate because it is absent from CostAllocationV3's ordinary metadata. | Classify as catalog_or_metadata_mismatch and report a shared-validator limitation with the exact sanitized error. Keep the required special attribute and prepared source; stop before upload. Do not modify the wrapper, suppress validation, remove the attribute, replace it with a SET directive, or use a different route. |
| Zap has incomplete history/detail evidence, a missing physical identity, or an unvalidated DELETE contract. | Classify as catalog_or_metadata_mismatch and stop before handoff. Resolve the missing evidence through the declared lookup or Data Loader validation; do not invent keys or substitute a REST mutation. |
| Zap partially succeeds, has an uncertain loader result, or leaves a parent/history record after reported success. | Classify as process_failed, or process_timeout for a timed-out check. Preserve the accepted handoff reference and partial outcome. Reconcile status and remaining state through authorized reads before any newly requested preview; never replay the original deletion automatically. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required source key, account value, date, or approval is missing, or a generated sequence is not positive and consecutive from 1. | Request the missing business fact; generate the sequence from supplied account-row order. |
| catalog_or_metadata_mismatch | Official key shape, KFF metadata, or loader schema differs. | Stop and correct the source contract. |
| auth_authz | A read cannot authenticate or authorize after one refresh. | Request the required read privilege. |
| transport_environment | Read transport fails. | Preserve redacted diagnostics and retry only the documented read when safe. |
| process_timeout | Loader has no terminal result in the permitted wait. | Stop and report the safe next-check path. |
| process_failed | Loader result or verification is unsuccessful. | Do not retry without a new preview and approval. |
| approval_blocker | Archive approval is absent, stale, or mismatched. | Present the exact immutable archive again. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| HDL preview | Sanitized environment, Create, Update, End Date, or Zap operation, official identity fingerprint, archive fingerprint, expected effect, and fresh approval requirement. For End Date, show the selected start, current end, requested inclusive end, and preservation of prior history/accounts. For Zap, show the Department/LDG, selector start, every affected interval, and distinct account counts by subtype, including COST, SUSP, and DFLT when present; disclose that the entire logical record/history will be deleted and HDL provides no undo. |
| Verification | Requested scope, redacted expected-versus-actual state, and safe next action. |
| Failure | Failure class, stage, redacted artifact reference, and one safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Mutation route | Do not use REST POST, PATCH, PUT, DELETE, genericCosting Data Loader business objects, raw UCM/import endpoints, browser replay, or FSM. |
| Approval | Do not hand off an archive without current approval bound to its exact immutable fingerprint. |
| Retry | Do not automatically retry an import or replay an uncertain mutation. |
| Diagnostics | Do not persist or disclose credentials, tokens, hosts, raw payloads, account values, or technical identifiers. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCP.HDL_GATE_CREATE | decision | 80 | execution_gate | submitted->DCP.RESULT_CREATE;blocked->DCP.HANDLE_ERROR;failed->DCP.HANDLE_ERROR | DCP.ENFORCE_DESIGN | stop | The immutable Create archive passed source/schema and Task Hook validation, has fresh approval, and is handed once to core.data-loader. |
| DCP.DONE_QUERY | terminal | 70 | terminal | none | DCP.VERIFY_QUERY | continue | The read-only query result is persisted with redacted facts. |
| DCP.DONE_CREATE | terminal | 110 | terminal | none | DCP.VERIFY_CREATE | continue | The verified Create effect is persisted with redacted facts. |
| DCP.HDL_GATE_UPDATE | decision | 120 | execution_gate | submitted->DCP.RESULT_UPDATE;blocked->DCP.HANDLE_ERROR;failed->DCP.HANDLE_ERROR | DCP.ENFORCE_DESIGN | stop | The immutable Update archive passed source/schema and Task Hook validation, has fresh approval, and is handed once to core.data-loader. |
| DCP.DONE_UPDATE | terminal | 150 | terminal | none | DCP.VERIFY_UPDATE | continue | The verified Update effect is persisted with redacted facts. |
| DCP.HDL_GATE_END_DATE | decision | 151 | execution_gate | submitted->DCP.RESULT_END_DATE;blocked->DCP.HANDLE_ERROR;failed->DCP.HANDLE_ERROR | DCP.ENFORCE_DESIGN | stop | The immutable parent-only End Date archive passed source/schema and Task Hook validation, has current approval and unchanged target state, and is handed once to core.data-loader. A wrapper rejection takes the blocked path before upload. |
| DCP.PENDING_END_DATE | terminal | 153 | terminal | none | DCP.RESULT_END_DATE | continue | Return accepted initiation or pending status with the core.data-loader resume reference. Do not poll automatically; a later explicit status/verification request resumes DCP.RESULT_END_DATE for the same handoff. |
| DCP.DONE_END_DATE | terminal | 155 | terminal | none | DCP.VERIFY_END_DATE | continue | End Date is verified: the selected parent ends on the requested date, is absent the next day, and prior history/accounts remain unchanged. |
| DCP.HDL_GATE_ZAP | decision | 156 | execution_gate | submitted->DCP.RESULT_ZAP;blocked->DCP.HANDLE_ERROR;failed->DCP.HANDLE_ERROR | DCP.ENFORCE_DESIGN | stop | The exact Zap archive passed source/schema and Task Hook validation, has current destructive approval and unchanged complete history/detail evidence, and is handed once to core.data-loader. |
| DCP.PENDING_ZAP | terminal | 158 | terminal | none | DCP.RESULT_ZAP | continue | Return accepted initiation or pending status with the core.data-loader resume reference and saved pre-load scope. Do not poll automatically; a later explicit status/verification request resumes DCP.RESULT_ZAP for the same handoff, without re-entering creation or re-resolving the deleted record. |
| DCP.HANDLE_ERROR | step | 160 | error_handler | disclosed->DCP.FAILED | none | stop | Any validation, lookup, package, loader, verification, or persistence failure. |
| DCP.DONE_ZAP | terminal | 165 | terminal | none | DCP.VERIFY_ZAP | continue | The selected logical allocation is absent from complete history and from every captured historical effective date after a successful complete load. |
| DCP.FAILED | terminal | 170 | terminal | none | DCP.HANDLE_ERROR | continue | The request stopped with a classified diagnostic and safe next action. |
