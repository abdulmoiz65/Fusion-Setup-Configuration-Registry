# Goal Plan Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Primary assignment status is absent | Return GOAL_PLAN_ADMIN_STATUS_UNKNOWN; distinguish missing evidence from inactive status. Preserve any user assumption separately; it cannot satisfy the verified template-goal contract |
| Worker item lookup returns 404 | Check the returned opaque item link and collection capability through the declared core route before claiming the API is unavailable |
| Eligible count unavailable before ESS | Expected: ESS evaluates eligibility. Proceed with approved selector and parameters; report actual count afterward |
| ESS succeeds but assignment reconciliation is absent or mismatched | Keep verification_pending or assignment_mismatch; preserve request ID and partial results, never automatically resubmit or delete |
| Missing or ambiguous dependency | Stop and return the owning route plus resume context |
| Current tenant exposes neither a Goal Plans `performanceGoals` child POST nor a same-host ADF batch fallback | Return `GOAL_PLAN_CREATE_CONTRACT_GAP`; record the missing create capability and do not ask the consultant for a route or reuse another tenant's capture |
| Batch fallback is selected but current tenant does not expose one same-host ADF batch root | Return `GOAL_PLAN_RUNTIME_CONTRACT_GAP`; record the missing resolver capability and do not ask the consultant for a runtime URL or reuse another tenant's capture |
| Authenticated caller cannot be resolved to one active primary assignment | Return `GOAL_PLAN_ADMIN_CONTEXT_GAP`; record the missing current-user resolver and do not request IDs from the consultant |
| A target-required field remains blank after safe enrichment | Return `MISSING_MANDATORY_DATA`; identify the unresolved business value and do not invent it or load the original source |
| A supplied nonblank value conflicts with a derived/default candidate | Preserve the supplied value, report the conflict in preview, and require correction when target validation rejects it; never overwrite it silently |
| HDL DAT is supplied but no executable `core.data-loader` route exists | Return `HDL_ROUTE_GAP`; record the missing provider/contract and do not substitute REST or ask the consultant for a route |
| HDL is selected without a DAT/ZIP source | Select `hdl_generate`; resolve and validate the Goal Plan rows, then have Core Data Loader generate the current-metadata source and immutable ZIP |
| DAT/ZIP is corrupt, unsafe, malformed, missing mandatory data, or contains an unsupported component | Preserve and reject it. If business intent is complete and unambiguous, rebuild a separate generated source through Core; otherwise return the file, component, line when available, validation code, and corrective action. No issue is waivable. |
| Goal Plan child has no package or target parent | Return `MISSING_PARENT`; require a parent row or fresh `existingParents` evidence |
| Goal Plan parent delete precedes a `GoalPlanGoal` or `GoalPlanAssignment` delete | Return `DELETE_ORDER`; require explicit child deletion first |
| Population child identity or operation is unavailable | Stop before preview; do not guess a child path or row key |
| Existing Eligibility Profile lookup was not paginated to completion | Return `ELIGIBILITY_PROFILE_LOOKUP_INCOMPLETE`; do not declare the profile missing or invoke the maintenance provider |
| Exact Eligibility Profile name returns more than one active Goal Management-compatible row | Return `ELIGIBILITY_PROFILE_AMBIGUOUS` with business-facing candidate details; never select the first row or ask for an ID when the displayed attributes can disambiguate it |
| Semantic population criteria are supplied but stored profile criteria cannot be read authoritatively | Return `ELIGIBILITY_PROFILE_SELECTION_REQUIRED` with relevant active Goal Management-compatible candidates; do not infer a match from the profile name |
| Complete existing-profile discovery returns no active Goal Management-compatible match | Return `ELIGIBILITY_PROFILE_MISSING`; route to `BEN_MANAGE_ELIGIBILITY_PROFILES` only when creation or maintenance is requested, and do not report its provider availability as a lookup failure |
| Primary request contains regular-plan sections | Reject before payload mapping and report the inapplicable fields |
| Goal Plan create or update sends maximum and enforcement before the maximum is persisted | Reject locally before preview. Build the declared conditional sequence: save maximum without enforcement, verify it, then patch enforcement only. |
| Staged maximum configuration returns a failed, uncertain, or mismatched result | Preserve the exact verified partial state, stop the remaining sequence, invalidate the unexecuted portion of the approval, and require a fresh remediation preview. Never retry either write automatically. |
| Assign Goal Plans ESS job or parameters are not verified | Stop before assignment ESS preview or submission |
| ESS submit command is still running or has no incremental output | Retain and poll the same local command session. Do not classify the request as missing, start reconciliation, or submit again. |
| Accepted-request checkpoint exists | Read its request ID and resume status tracking only; a second submission is prohibited. |
| Submission checkpoint is absent after the submit command reaches a terminal local failure | Recover from a valid Core submission-result artifact bound to the same Goal Management attempt and environment; checkpoint its request ID and monitor only. If no valid result exists, return `UNKNOWN_AFTER_SUBMISSION`, preserve diagnostics and the approved payload digest, and do not resubmit or create another run directory. Manual or supported authoritative request discovery is a last-resort reconciliation path. |
| ESS polling reaches its bounded timeout | Return `ASSIGNMENT_PENDING` with request ID, last status, and elapsed time. Leave the Run Book task incomplete and resume the same request later without a new write approval. |
| ESS returns terminal success | Persist the request-ID execution result and perform fresh assignee reconciliation through `verify_assignment_outcome`; only its verified result permits `ASSIGNMENT_VERIFIED` and dependent Run Book task completion. |
| Goal Plan is pending approval | Stop update; changes are not final until approval completes |
| Assigned Goal Plan deletion is requested | Block delete and offer active/inactive status management |
| Review Period change is requested with assignees | Block update until all assignees are removed in a separate approved operation |
| A Goal Plan child batch is partially applied | Re-read the Goal Plan and all requested child collections, disclose orphan/partial rows, and stop for an explicit remediation preview; never replay the batch automatically |
| Plan-goal reorder is requested | Return `UNSUPPORTED_UI_BEHAVIOR`: VBCS itself does not persist reorder. Do not treat it as a contract gap or infer a path/payload |
| Plan-goal delete is ambiguous or returns a failure | Re-read the target `performanceGoals` collection using the fresh GoalId,GoalPlanGoalId identity, disclose whether the row remains, and stop; never replay DELETE automatically |
| Plan-goal import action returns an error or ambiguous result | Re-read target goals, retain only sanitized action diagnostics, and stop for remediation; never replay import automatically |
| A document association batch is partial or ambiguous | Re-read the Goal Plan and `associatedPerfDocumentTypes` collection, compare each requested DocumentTypeId/GoalPlanDocumentTypeId delta with fresh rows, disclose partial state, and stop for an explicit remediation preview; never replay the batch automatically |
| Assignee batch delete returns nonzero, mixed, or ambiguous result | Re-read every requested GoalPlanAssignmentId, preserve the status of each, retain sanitized action diagnostics, and never replay the batch automatically |
| Performance-document sync returns an empty result | Return NO_CHANGE with the evaluated predicate inputs; it means no ESS request ID was produced and is not a failure |
| Performance-document sync fails or is ambiguous | Stop before the main Goal Plan batch update, report the safe action status and current/prior Goal Plan state, and do not resubmit automatically or add ESS polling to this action |
| Assignee deletion lacks an exact application/REST capability | Return guided UI requirements; do not substitute population-child DELETE |
| REST or ESS timeout/ambiguous response | Return UNKNOWN_AFTER_SUBMISSION and reconcile without replay |
| One approval covers multiple updates but an ADF batch contract is not explicitly advertised for those operations | Keep the approval group and build ordered metadata-supported PATCH requests. Do not infer a batch root or combine operations merely because approval is singular. |
| Parent execution control is missing, stale, or identifies a later Run Book task | Return `RUNBOOK_SEQUENCE_BLOCKED`; the task cannot be entered until every earlier applicable task is Completed or Not Applicable and the next-task preview has been shown. |
| PD-sync action fails | Capture sanitized action diagnostics and fresh Goal Plan state; do not treat an empty result as failure |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing identity, configured selector, or contradictory stages | Correct intake |
| Approval blocker | Required operation-specific approval is absent or stale | Re-preview |
| Process timeout | ESS polling deadline expires | Report last status and next-check path |
| Process failed | ESS returns failure | Retrieve sanitized process diagnostics; do not resubmit automatically |
| Unknown after submission | REST/ESS outcome cannot be proven | Reconcile by safe read/status only |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| REST preview | Environment, operation, target, dependencies, before/after values, mapping report, and fingerprint |
| ESS preview | Environment, exact job, parameters, selector, execution approval, and fingerprint |
| Failure | Stage, class, message, safe request ID/status, elapsed time, and recommended action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Saving population | Do not infer or submit assignment |
| Missing worker | Do not create a worker in this skill |
| Unverified ESS contract | Do not fabricate job parameters or submit |
| Assignment rerun | Do not claim that rerun updates prior goals or reverses earlier assignments for newly excluded workers |
| Profile-option tuning | Do not change HRG_GP multithread options from the Goal Plan skill |
| Ambiguous submission | Do not retry automatically |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_PLANS.CSV_READY | terminal | 500 | terminal | none | GOAL_PLANS.VALIDATE | stop | CSV route is ready |
| GOAL_PLANS.HDL_READY | terminal | 505 | terminal | none | GOAL_PLANS.HDL_VALIDATE | stop | Error-free HDL task preflight is ready for `core.data-loader` preview |
| GOAL_PLANS.WORKER_ROUTE | terminal | 510 | terminal | none | GOAL_PLANS.VALIDATE | stop | Worker creation must route to GHR/HDL |
| GOAL_PLANS.NO_CHANGE | terminal | 520 | terminal | none | GOAL_PLANS.WRITE_ROUTE | stop | Fresh values already match |
| GOAL_PLANS.DONE_READ | terminal | 530 | terminal | none | GOAL_PLANS.READ | stop | Read completed |
| GOAL_PLANS.DONE_SEARCH | terminal | 531 | terminal | none | GOAL_PLANS.SEARCH | stop | Bounded search completed, including an empty result |
| GOAL_PLANS.DONE_CREATED | terminal | 540 | terminal | none | GOAL_PLANS.CREATE_POST_WRITE_ROUTE | stop | Inactive create, including any approved staged maximum enforcement, verified |
| GOAL_PLANS.DONE_UPDATED | terminal | 550 | terminal | none | GOAL_PLANS.UPDATE | stop | Update verified |
| GOAL_PLANS.DONE_ACTIVATED | terminal | 560 | terminal | none | GOAL_PLANS.ACTIVATE | stop | Activation verified |
| GOAL_PLANS.DONE_INACTIVATED | terminal | 570 | terminal | none | GOAL_PLANS.INACTIVATE | stop | Inactivation verified |
| GOAL_PLANS.DONE_INCLUDED_WORKER | terminal | 580 | terminal | none | GOAL_PLANS.INCLUDE_WORKER | stop | Included-worker child create verified without ESS |
| GOAL_PLANS.DONE_EXCLUDED_WORKER | terminal | 590 | terminal | none | GOAL_PLANS.EXCLUDE_WORKER | stop | Excluded-worker child create verified without ESS |
| GOAL_PLANS.DONE_PROFILE_ASSOCIATED | terminal | 600 | terminal | none | GOAL_PLANS.ASSOCIATE_PROFILE | stop | Eligibility Profile child association verified without ESS |
| GOAL_PLANS.DONE_POPULATION_REMOVED | terminal | 610 | terminal | none | GOAL_PLANS.REMOVE_POPULATION | stop | Returned population child delete verified without ESS |
| GOAL_PLANS.DONE_DOCUMENT_ASSOCIATED | terminal | 611 | terminal | none | GOAL_PLANS.FUNCTIONAL_MUTATION | stop | Returned document association create verified by fresh collection read |
| GOAL_PLANS.DONE_DOCUMENT_REMOVED | terminal | 612 | terminal | none | GOAL_PLANS.FUNCTIONAL_MUTATION | stop | Returned document association delete verified by fresh collection read |
| GOAL_PLANS.DONE_ASSIGNEE_SEARCH | terminal | 615 | terminal | none | GOAL_PLANS.ASSIGNEE_SEARCH | stop | Bounded Goal Plan assignee search completed |
| GOAL_PLANS.DONE_FUNCTIONAL_CHANGE | terminal | 616 | terminal | none | GOAL_PLANS.FUNCTIONAL_MUTATION | stop | One approved functional-flow mutation was verified |
| GOAL_PLANS.DONE_PD_SYNC_SUBMITTED | terminal | 617 | terminal | none | GOAL_PLANS.FUNCTIONAL_MUTATION | stop | PD synchronization action returned a non-empty ESS request ID |
| GOAL_PLANS.DONE_PD_SYNC_NO_CHANGE | terminal | 618 | terminal | none | GOAL_PLANS.FUNCTIONAL_MUTATION | stop | PD synchronization action completed with an empty result and no ESS submission |
| GOAL_PLANS.DONE_ASSIGNEES_REMOVED | terminal | 619 | terminal | none | GOAL_PLANS.FUNCTIONAL_MUTATION | stop | Assignee batch delete result `0` was verified by fresh assignee read |
| GOAL_PLANS.ASSIGNMENT_READY | decision | 620 | execution_gate | checkpointed->GOAL_PLANS.ASSIGNMENT_SUBMITTED;uncertain->GOAL_PLANS.UNKNOWN;failed->GOAL_PLANS.BLOCKED | GOAL_PLANS.ASSIGNMENT_APPROVAL | stop | Verified ESS handoff is approved and the Goal Management adapter owns the attempt/checkpoint while unchanged Core submits once |
| GOAL_PLANS.ASSIGNMENT_SUBMITTED | decision | 621 | execution_gate | terminal_success->GOAL_PLANS.ASSIGNMENT_VERIFIED;timeout->GOAL_PLANS.ASSIGNMENT_PENDING;terminal_failure->GOAL_PLANS.BLOCKED;uncertain->GOAL_PLANS.UNKNOWN | GOAL_PLANS.ASSIGNMENT_READY | stop | The accepted request ID is durably checkpointed and only request-ID status tracking may continue |
| GOAL_PLANS.ASSIGNMENT_PENDING | terminal | 622 | terminal | none | GOAL_PLANS.ASSIGNMENT_SUBMITTED | stop | Bounded polling ended before terminal status; retain request ID for read-only resume and leave the Run Book task incomplete |
| GOAL_PLANS.ASSIGNMENT_VERIFIED | terminal | 623 | terminal | none | GOAL_PLANS.ASSIGNMENT_SUBMITTED | stop | The same checkpointed request has persisted terminal success and fresh verified assignee reconciliation before the dependent Run Book task may complete |
| GOAL_PLANS.UNKNOWN | terminal | 630 | terminal | none | none | stop | A submitted operation has an ambiguous outcome |
| GOAL_PLANS.BLOCKED | terminal | 640 | terminal | none | none | stop | A dependency, approval, impact, or contract blocks the request |
