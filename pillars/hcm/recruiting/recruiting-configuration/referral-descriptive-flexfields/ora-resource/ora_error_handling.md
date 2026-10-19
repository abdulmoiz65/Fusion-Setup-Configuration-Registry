# Referral Descriptive Flexfields Error Handling

Classify failures, disclose the exact blocker without sensitive runtime data, and stop before retry. A registry plan or approval gate does not authorize URL debugging, direct REST or DFF API access, database action, package reconstruction, or automatic deployment.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Exact task, DFF, protected context, or required existing segment is not found | Return MISSING with the expected identity and stop |
| More than one task, DFF, context, segment, or value set matches | Return AMBIGUOUS with the conflicting identities and stop |
| PlanCreate, PlanUpdate, or copy for a Global or Employee Referral segment is missing an applicable user-owned input | Ask for the segment name first when absent. Once known, analyse the latest validated matching package or a fresh export, present all derivable values together for confirmation or change, and ask only for any remaining required value without showing internal workflow diagnostics |
| Segment identity or business purpose duplicates existing configuration | Return CONFLICT and request an explicit design decision |
| Segment code exceeds 30 characters, or API Name / SegmentIdentifier violates its length, leading-letter, alphanumeric-only, or reserved-word rule | Return BLOCKED, propose a valid field-specific candidate, and require requester confirmation before rebuilding the archive |
| Storage is occupied or incompatible, or sequence is duplicated | Return BLOCKED and require a valid alternative; never overwrite |
| Existing value set is unresolved or incompatible, or a new value set is missing a required UI field | Return BLOCKED and ask only for the exact existing selection or the next required new-value-set field |
| Another context or protected-context rename, deletion, or creation is requested | Return UNSUPPORTED; allow context-sensitive work only within existing EMPLOYEE_REFERRAL |
| Agency Referral or another context is matched during Referral DFF segment retrieval | Return UNSUPPORTED for those context rows, retain Global rows, and continue with context-sensitive rows only if the exact EMPLOYEE_REFERRAL code and Employee Referral display name can be verified uniquely; otherwise report the Employee Referral portion as MISSING or AMBIGUOUS |
| The read-only segment CSV export cannot be created, downloaded, extracted, or validated | Return BLOCKED with the failed export stage and stop; do not debug the pod URL or fall back to a direct REST or DFF API |
| A Global PlanCreate export fails, times out, or returns headers without usable rows | Offer the verified historical-package contract fallback. Continue only after the requester confirms the full suggested design and the preview labels duplicate, column-occupancy, sequence-occupancy, and target value-set existence checks as unverified. Build one delta-only Global row and never treat historical rows as current state. |
| A header-only export is followed by Inspect/list | Say `No Referral DFF segments are currently configured.` Keep the unavailable-current-definition state internal. |
| A failed export, or a header-only export followed by copy, update, disable, verify, or EMPLOYEE_REFERRAL work | Return BLOCKED. The historical Global package contract cannot supply current rows or protected-context evidence. |
| Task is not visible or access is rejected | Return AUTHORIZATION and route to the Recruiting security owner |
| Save, deployment, export, import, transport, or result is failed or uncertain | Return PROCESS_FAILED or PRODUCT_OR_DEPLOYMENT, preserve sanitized diagnostics, reconcile current state, and stop without automatic retry |
| Approval is absent or does not match the current preview fingerprint | Return APPROVAL_REQUIRED and stop before the state-changing handoff |
| Final FSM archive construction or validation fails | Return ARTIFACT_PREPARATION with the exact failed package check and stop; never invent the missing contract or structure |
| The historical fallback package is absent, its SHA-256 or archive-derived member structure differs, or historical custom/audit values would enter the requested delta | Return ARTIFACT_PREPARATION and stop; do not reconstruct the package from memory or submit it |
| A create archive has a blank ShortPrompt or missing, nonpositive, or conflicting SequenceNumber | Return ARTIFACT_PREPARATION, collect corrected transport-required values, rebuild the archive, invalidate prior approval, and show a new checksum preview |
| Upload or initiation fails or returns an uncertain result before an accepted request ID exists | Return the exact failed or uncertain stage and stop; do not retry or resubmit automatically |
| An approved create, update, or copy import is accepted | Keep the acceptance response internal, monitor the request to terminal state, retrieve and read the FSM ProcessLog, and return only the final success or error result |
| Completion monitoring reaches a timeout or cannot obtain terminal evidence | Return the request ID, last status, elapsed wait, and one safe status-check action; do not retry the upload or import |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | One required exact identity, input, current definition, segment, contract, or approval is absent | Supply or resolve only the missing item |
| AMBIGUOUS | Multiple targets match | Resolve one exact target |
| CONFLICT | Existing configuration duplicates or overlaps the proposed segment | Obtain an explicit design decision |
| BLOCKED | Compatibility, storage, sequence, value-set, sandbox, or deployment readiness fails | Correct the named blocker and generate a new preview |
| UNSUPPORTED | Request crosses the exact task, DFF, scope, context, mutation, database, or execution-route boundary | Return the supported boundary; do not substitute another path |
| AUTHORIZATION | Required access is absent or rejected | Route to the Recruiting security owner |
| APPROVAL_REQUIRED | A state-changing handoff lacks approval bound to its exact current preview | Obtain explicit approval immediately before the handoff |
| PROCESS_FAILED | A save, export, import, or transport failed or returned an uncertain result | Preserve diagnostics, reconcile state, and stop without retry |
| PRODUCT_OR_DEPLOYMENT | Deployment failed, is uncertain, or reports an unresolved diagnostic | Preserve diagnostics, inspect deployment state, and require approval for a safe next attempt |
| ARTIFACT_PREPARATION | The final FSM CSV/ZIP can't be built or validated from an established contract | Correct the named package issue or provide the missing contract; do not submit |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input rejection | For an invalid supplied value, show only the affected business field, why that value is not accepted, and the concise correction prompt; keep exact task and workflow diagnostics internal unless the user asks for technical details |
| Missing segment-change input | Show only the next interactive business question and its concise choices when applicable; do not show MISSING, task-node IDs, action types, execution paths, registry state, a full checklist, or no-action commentary |
| CSV route rejection | Exact task code, export stage, sanitized process status, artifact or extraction state, and safe retry path through shared.setup-export.task-level-export |
| Readiness rejection | Dependency status, sanitized evidence, unresolved owner or contract, and the safe next action |
| Design rejection | Exact proposed rule, current conflicting configuration identity, blocker, and permitted correction |
| Approval gate | Target environment, exact task and DFF identity, operation, scope, segment identity, proposed delta, unresolved items, verification plan, and immutable preview fingerprint |
| Failure after a state-changing action | Environment, operation, sanitized diagnostic, known or uncertain result, last completed stage, and read-only reconciliation action |
| Verification result | Approved segment identity and scope, checked properties, deployment state, sanitized test outcome, reporting-owner result when applicable, and any remaining issue |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Another task or DFF is requested | Do not reuse this contract or substitute the generic Common Manage Descriptive Flexfields task |
| Another context or context lifecycle change is requested | Do not create a context or rename or delete EMPLOYEE_REFERRAL |
| Referral DFF segments are requested | Do not exclude Global rows; do not return Agency Referral or any other unsupported context's rows, and do not label Agency Referral as EMPLOYEE_REFERRAL |
| A pod URL, browser, developer tools, direct DFF API, or direct REST operation is proposed for segment information or changes | Do not open, debug, probe, scrape, construct, or send it; use only the declared workflow |
| Database access is proposed | Do not use direct database reads or writes as a runtime dependency |
| Value-set selection or design is incomplete | Do not infer an internal value-set identifier, Module, validation type, value data type, or values. Ask only for the next required UI field; API Name and Description remain optional |
| PlanCreate or PlanUpdate inputs are incomplete | Do not infer, silently default, preview, or configure the segment; ask for the missing user-owned fields and preserve authoritative unchanged properties during PlanUpdate |
| A copy API Name is being derived | Do not append `_Copy` because underscore is invalid for SegmentIdentifier. Append `Copy` without a separator, validate the full identifier, and ask for a different confirmed value when it is invalid or longer than 30 characters |
| Interactive input collection is active | Do not dump all missing fields, repeat answered questions, expose internal workflow state, or add status and next-action narration around the prompt |
| A required read-only segment CSV export is unavailable or invalid | Do not list segments, guess current rows, or fall back to URL debugging or direct APIs. For Global create/copy/update/disable, use the historical structural contract after an attempted export and operation-specific confirmation; it cannot supply a verified current segment list. |
| Historical Global package fallback is active | Do not claim that the code, column, sequence, or value set is unique, unused, present, or current. Do not use historical segment rows, audit identities, timestamps, submitter, process ID, or environment provenance as target-environment facts. |
| Save, deployment, import, transport, or result is failed or uncertain | Do not retry automatically or assume rollback succeeded |
| Approval is missing or stale | Do not perform or hand off a state-changing action |
| An upload or initiation has been dispatched | Do not retry, replay, replace, or resubmit it; status monitoring and ProcessLog retrieval are required only after an accepted create, update, or copy request ID |
| Runtime or referral data is observed | Do not write it into resource files, diagnostics, or authoring evidence |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| REFERRAL_DFF.APPROVAL_GATE | decision | 50 | execution_gate | approved->REFERRAL_DFF.EXECUTE;not_required->REFERRAL_DFF.EXECUTE;missing->REFERRAL_DFF.RETURN_ISSUES;stale->REFERRAL_DFF.RETURN_ISSUES | REFERRAL_DFF.ENFORCE_DESIGN | stop | Require approval bound to the current preview immediately before a state-changing handoff; read-only inspection and planning use not_required |
| REFERRAL_DFF.EXECUTE | decision | 60 | execution_gate | completed->REFERRAL_DFF.RETURN_SUCCESS;import_accepted->REFERRAL_DFF.MONITOR_IMPORT;verify_requested->REFERRAL_DFF.VERIFY;failed->REFERRAL_DFF.RETURN_ISSUES;uncertain->REFERRAL_DFF.RETURN_ISSUES;unsupported->REFERRAL_DFF.RETURN_ISSUES | REFERRAL_DFF.APPROVAL_GATE | stop | Build and validate the final FSM archive from the analysed current-definition package or the qualified historical Global structural contract plus confirmed delta; after core.data-loader approval, upload and initiate exactly once and keep an accepted request ID internal for required completion monitoring |
| REFERRAL_DFF.RETURN_SUCCESS | terminal | 90 | terminal | none | REFERRAL_DFF.EXECUTE | stop | A supported non-import action completed with verified evidence |
| REFERRAL_DFF.RETURN_IMPORT_SUCCESS | terminal | 91 | terminal | none | REFERRAL_DFF.MONITOR_IMPORT | stop | Terminal status and the reviewed ProcessLog confirm clean completion; report only that the segment operation completed successfully and link the ProcessLog |
| REFERRAL_DFF.RETURN_VERIFY_SUCCESS | terminal | 92 | terminal | none | REFERRAL_DFF.VERIFY | stop | A separately requested verification completed with verified evidence |
| REFERRAL_DFF.RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any failure, refusal, missing input, ambiguity, conflict, authorization failure, blocked dependency, stale approval, or uncertain result |
