# Goal Plan Reference Lookups

## Administrator evidence and route gaps

`resolve_active_primary_admin` is a pure validator, not a caller-discovery API.

For authenticated administrator context, use Core REST to GET
`{hcmRuntimeRoot}/workerAssignmentsLOV` with `finder=findMyAssignments`,
`onlyData=true`, and
`fields=AssignmentId,AssignmentPrimaryFlag,AssignmentType,BusinessUnitId,LegalEntityId,LegislationCode,PersonId,AssignmentName,AssignmentStatusType`.
Resolve the runtime root from the active tenant; never copy a captured host,
`rv:` revision, or real person identifiers into a reusable artifact. Complete
pagination and pass the returned `items` envelope to `resolve_active_primary_admin`.
Select exactly one active primary assignment; return PersonId and AssignmentId
from that same row. This proves caller identity, not HR privileges. Missing or
ambiguous primary assignments require a diagnostic, not guessed identifiers.
Invoke only for operations that require caller context; population-based ESS
does not require administrator IDs or individual eligible-worker IDs.

### OAuth handoff and submission recovery

Use one serialized `core.auth.fusion-oauth-authentication` login before ESS.
If automatic browser opening fails, run its login script with
`--no-open-browser --callback-timeout 300` using unbuffered output or a PTY.
Open the exact generated authorization URL in the existing Chrome session,
obtaining OS execution permission when needed. Keep the same callback process
alive; tenant-home sign-in alone does not complete this OAuth flow. Do not
reconstruct the URL or change its scope/state. Confirm Login complete before
submission; never print or persist tokens in artifacts. For an occupied callback
port, identify the process and terminate only a confirmed stale process owned
by this workflow with the required permissions; do not kill by port alone.
Use project-local watchdog heartbeat files and the shared ledger logger with
appropriate filesystem permission. If ledger recording fails after Oracle
accepts ESS, repair telemetry separately and track the checkpoint request ID;
never submit again to repair a logging failure.
Use the declared core REST client only after metadata and identity preflight
select a supported worker lookup. User-supplied PersonId/AssignmentId can select
records for verification but do not prove the authenticated caller's identity.
Resolve opaque item keys from returned links; one numeric-key item 404 does not
prove that the Workers collection is unavailable. Distinguish auth/privilege,
item-key, missing caller adapter and missing assignment status diagnostics.
The validator accepts list or `items` assignment envelopes; complete pagination
first. Missing status is unknown, not inactive. Record a user-approved active
assumption separately; never manufacture `AssignmentIsActivePrimary=true` from
it. The current template-goal contract still requires verified active-primary
evidence. If the declared caller adapter is absent, report a technical route gap
once; do not ask the user to sign in repeatedly or implement auth in this pillar.

Apply [Goal Management Dependent Setup Routing](../../../goal-management-common/dependent-setup-routing.md)
to every shared or cross-product reference. This task may read dependencies
for validation; dependency maintenance is an independent owner-routed task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_controlled_next_task | Before executing a Run Book task | Approved plan and fingerprint, resolved task queue, current task statuses | Local `pillars/hcm/goal-management/goal-management-common/scripts/plan_guided_next_actions.py::resolve_controlled_next_task` | Exact task identity, sequence, execution-control fingerprint | Use the existing parent resolver; require this task to be the earliest incomplete applicable task | Allowed Goal Management execution control | Stop on missing, stale, or mismatched control; do not bypass the parent queue |
| goal_plan_resource_route | Before the first Goal Plan management request | Connected environment | GET `/hcmRestApi/resources/latest/goalPlans/describe` through the core REST client | Collection, search action, item and child links, supported methods | Expected `goalPlans` resource on the configured host; numeric-release canonical links are acceptable server resolution | In-memory `resourceRoot=/hcmRestApi/resources/latest` and operation contract | If unavailable, resolve one trusted current runtime fallback; reject `rv:null` and never invent or persist the root |
| goal_plan_search | Name-based candidate search or create idempotency | Normalized name query, `GoalPlanName` search field, limit, offset | POST `{resourceRoot}/goalPlans/action/findByAdvancedSearchQuery` | Search projection only: `GoalPlanId`, `GoalPlanName`, `ReviewPeriodId`, `ReviewPeriodName`, `LastUpdateDate`, and pagination from `result.summary` | Use a non-empty name query, page every candidate up to the disclosed limit, and locally match the exact Goal Plan name within the associated Review Period; dates do not distinguish duplicates | Candidate rows and query window | Return empty READ or block only when the selected route/query contract is unavailable |
| goal_plan_detail_list | List by Review Period, Primary-state check, or any request needing status/dates/configuration | `ReviewPeriodId` or another resource-query predicate, fields, limit, offset | GET `{resourceRoot}/goalPlans?fields={supportedResourceFields}&q=ReviewPeriodId={ReviewPeriodId}` | Full collection fields such as GoalPlanId, GoalPlanName, Description, StartDate, EndDate, GoalPlanActiveCode, GoalPlanActiveCodeMeaning, PrimaryGoalPlanFlag, ReviewPeriodId, and configuration flags | Use the collection query for field-rich filtering; page returned collection values and locally apply any remaining rule | Candidate detail rows and query window | Return empty READ or block only when the selected route/query contract is unavailable |
| goal_plan_lookup | Existing target, create idempotency, or staged maximum enforcement is required | GoalPlanId, external ID, or exact name plus kind/period | Use the name-search projection for candidate IDs; then GET `{resourceRoot}/goalPlans/{GoalPlanId}?fields=*` or the fresh returned item link | Search identity fields first; hydrate full identity, status, dates, configuration, concurrency fields, `MaximumGoalsNumberInGoalPlan`, and raw nullable `EnforceMaximumGoalsInGpFlag` from the item route | Exact external ID preferred; otherwise exact disambiguated business key. Before enforcement, require the fresh maximum to equal the approved value; preserve `null` exactly and never coerce it to `false`. | GoalPlanId and fresh state | Return MISSING, require disambiguation, or stop the staged sequence when the persisted maximum differs |
| goal_plan_goal_lookup | Template-goal create/update, delete, or post-create/import verification | Exact target GoalPlanId and optional Goal name | First GET the exact `{resourceRoot}/goalPlans/{GoalPlanId}?fields=GoalPlanId,GoalPlanName,ReviewPeriodId,PrimaryGoalPlanFlag,StartDate,EndDate,MassRequestId`, then GET `{hcmRuntimeRoot}/goalPlans/{GoalPlanId}/child/performanceGoals` or a fresh returned child link | Fresh projected plan `MassRequestId`, GoalId, GoalPlanGoalId, GoalName, dates, DisplaySequence, pagination, returned item link | Validate the exact regular plan and projected MassRequestId with `scripts/goal_plan_runtime.py:resolve_goal_plan_mass_request_id`. An omitted key is incomplete projection, distinct from explicit null. Page current rows; identify exactly one goal by returned child identity, never a display label alone | Runtime-only MassRequestId plus fresh GoalId,GoalPlanGoalId identity and before/after rows | Re-read with the explicit projection if a compact response omitted the key; block a projected null/invalid MassRequestId or ambiguous goal selection; re-read the collection after every successful create/update |
| template_goal_source_lookup | Add a selected Performance Library Goal to an existing regular Goal Plan | Exact active Performance Library Goal identity | Read the exact selected Library Goal through its current returned item/action contract | Fresh source identity, copied eligible fields, status, and optional source dates | Select exactly one active Performance Library Goal visible to the current administrator. Map its runtime identity only as `ReferenceContentItemId`; never reuse its Library Goal item key, batch path, ETag, or parent schema | Runtime-only source identity and copied-field diff | Block zero/many/inactive/inaccessible sources or unsupported copied fields |
| plan_goal_addition_mode | Add a Goal Plan goal | Explicit `library` or `non_library` intent | Current Goal Plan goal metadata and, for library mode, the source lookup | Addition kind, ReferenceContentItemId, supported scalar fields, and dates | `library` requires the exact fresh source identity as non-null `ReferenceContentItemId`; `non_library` omits it or retains only explicit null | Runtime-only mapped payload fields | Block absent library reference, non-library non-null reference, or unspecified mode; never infer mode from a name |
| goal_plan_import_context_lookup | Plan-goal import is requested | Current WorkerAssignmentId, exact Review Period name, exact target/source Goal Plan names | GET `{hcmRuntimeRoot}/reviewPeriodsLOV?finder=findReviewPeriodsForGoals;WorkerAssignmentId={currentWorkerAssignmentId}` then GET `{hcmRuntimeRoot}/goalPlansLOV?finder=findGoalPlansForRPandAssignment;ReviewPeriodId={ReviewPeriodId}` with current supported exclusion/query filtering | ReviewPeriodId, ReviewPeriodName, GoalPlanId, GoalPlanName, MassRequestId, PrimaryGoalPlanFlag, Status, dates, pagination | Resolve one Review Period and distinct exact regular source/target plans; map their MassRequestId values | targetMassRequestId, massRequestId, goalPlanId, reviewPeriodId | Block zero/many matches, same source/target, Primary, inactive, or missing MassRequestId |
| current_user_person_context_lookup | Template-goal create/update; Goal Plan HDL preparation requiring requester/assigned-by fields; or basic REST Goal Plan create only when current create metadata requires caller fields | Authenticated caller identity plus the current worker route | Read `{hcmRuntimeRoot}/workerAssignmentsLOV` with `finder=findMyAssignments` from the active authenticated Fusion session, then validate it with `scripts/goal_plan_runtime.py:resolve_active_primary_admin` | Logged-in PersonId, PersonNumber, exactly one active primary AssignmentId, effective status, security/assigner context | For HDL, place PersonNumber only in the applicable prepared-copy requester/assigned-by field and retain assignment evidence only in the runtime audit context. For REST `performanceGoalsV2`, retain only runtime PersonId/AssignmentId. Do not invoke for a basic REST create that has no caller fields. | Runtime-only person/assignment context and prepared-copy provenance | Return `GOAL_PLAN_ADMIN_CONTEXT_GAP` only after the authenticated-caller route cannot resolve one active primary assignment; do not ask the consultant for IDs, use ManagerAssignmentId, or substitute a selected-worker assignment |
| primary_goal_plan_lookup | Primary create or activation is requested | `PrimaryGoalPlanFlag=true` | Goal Plan read/search contract | Identity, active status, ReviewPeriodId, technical dates | Resolve every Primary row and exactly one active row at most | Existing Primary state and reusable technical bounds | Block activation if another Primary is active |
| review_period_lookup | Goal Plan depends on a period | Exact period name or ID | Review Period management read; LOV only for ID resolution | ReviewPeriodId, dates, status | Exactly one usable period | Review Period contract values | Block on zero, many, or inactive result |
| eligibility_profile_lookup | Regular-plan eligibility is requested | Exact profile business name, or semantic population criteria plus authoritative verified profile-criteria matches | GET the current validated `eligibilityProfilesLOV` route with `onlyData=true`, fields `AsmtToUseCd,BnftCagrPrtnCd,Description,EligyPrflId,Name,ProfileType,StatCd`, and bounded `limit`/`offset`; repeat until `hasMore=false`. When only semantic criteria are supplied, use an available authoritative profile-criteria read capability after the LOV candidate read; the LOV name alone is not criteria evidence. | Profile identity, name, description, active status, participant profile type, Goal Management usage, pagination evidence, and verified criteria evidence when semantic matching is used | Retain only `StatCd=A`, `ProfileType=PRTP`, and `BnftCagrPrtnCd=GOAL`. For a supplied name, require exactly one exact case-insensitive `Name` match across all pages. For semantic criteria, require exactly one candidate whose stored criteria were authoritatively verified to match; never resolve from fuzzy or lexical name similarity. | Internal EligibilityProfileId plus business name, status, usage, and match evidence | One match: resolve internally and continue without requesting an ID. Multiple matches: list business-facing candidate name, description, status, and usage and request selection; do not select the first row. Zero matches: report missing, then route creation/maintenance to `BEN_MANAGE_ELIGIBILITY_PROFILES` only if requested. Criteria unavailable: list relevant active Goal candidates for confirmation instead of claiming no profile exists. |
| performance_document_type_lookup | Performance integration is requested | Exact document-type key and plan dates | GET `{hcmRuntimeRoot}/talentPerformanceDocumentTypes?limit={pageLimit}` | DocumentTypeId, DocumentTypeName, DateFrom, DateTo, Status, StatusMeaning, InUseFlag, pagination | Page current results; select exactly one Active type with DateFrom no later than plan start and DateTo no earlier than plan end | Runtime-only DocumentTypeId and coverage result | Block or omit integration by user decision |
| goal_plan_document_association_lookup | Document association add, removal, or verification is requested | Exact GoalPlanId | GET `{hcmRuntimeRoot}/goalPlans/{GoalPlanId}/child/associatedPerfDocumentTypes` or the fresh returned child link | DocumentTypeId, GoalPlanDocumentTypeId, GoalPlanId, Name, pagination, returned child links | Page current rows; add checks DocumentTypeId uniqueness and remove selects exactly one returned GoalPlanDocumentTypeId | Fresh association rows and child identities for the approved batch | Return an empty association set for a read; block ambiguous removal or unavailable collection |
| worker_assignment_lookup | Population or assignment is requested | Person key, assignment key, effective date | `workersLov` / `getall_workersLov` or current worker and assignment read routes | PersonId, AssignmentId, status, primary indicator, effective dates; only current advertised hierarchy evidence if present | Included-worker create requires one active target AssignmentId. Normalize omitted CascadingLevel to `"0"`; validate a supplied value locally and use hierarchy evidence only for non-Self scope | Runtime-only worker context | Block ambiguity, unsupported explicit value, or non-Self scope lacking hierarchy evidence; never call a CascadingLevel LOV, persist real identifiers, or map ManagerAssignmentId |
| assign_goal_plans_job_lookup | Assignment handoff is requested | Current environment and exact active regular Goal Plan | Current Scheduler route validation plus authoritative Manage Goal Scheduled Process evidence | Job definition `JobDefinition://oracle/apps/ess/hcm/goals/core/ScheduleProcessJobDef`, application `EarHcmEss`, product `HRG`, mode `ASSIGN_GOAL_PLANS`, single Goal Plan name, plan dates, MassRequestId, effective date, and verified positional parameters | Submit one Goal Plan per request. Process type is `Assign goal plans`; process name equals the fresh Goal Plan name; effective date is resolved at preview (supplied or defaulted to today) and pinned through approval; the numeric option flag is the verified Assign Goal Plans option argument and is not purge days | Complete ESS request payload and preview fingerprint | Block submission if the active plan read, MassRequestId, dates, effective date, or positional contract is unavailable |
| goal_plan_batch_profile_option_lookup | Assignment throughput is being assessed | Current environment | Canonical provider for `HRG_MANAGE_WORKER_GOAL_SETTING_PROFILE_OPTIONS` when available | HRG_GP_MAX_THREADS, HRG_GP_MINCOUNT_EACHTHREAD, HRG_GP_MINCOUNT_LASTTHREAD | Exact current values; read-only in this skill | Current values and derived explanation | Return TAXONOMY_REFRESH_REQUIRED/provider blocker; never create a common task here |
| goal_plan_assignee_search | Assignee search, delete assessment, assignee removal, or post-ESS assignment reconciliation | Resolved GoalPlanId and exact GoalPlanName; optional manager PersonId; optional Department/OrganizationId; display/search fields; offset; limit | Resolve current Goal Plan Assignees metadata first. Prefer its advertised read-only finder: GET `{hcmRuntimeRoot}/goalPlanAssignees?finder=findByAdvanceSearch;GoalPlanId={GoalPlanId}` with bounded `limit`/`offset`; otherwise use the advertised POST `{hcmRuntimeRoot}/goalPlanAssignees/action/findByAdvancedSearchQuery`. If either server route fails before returning a result and current metadata marks GoalPlanName queryable, use GET `{hcmRuntimeRoot}/goalPlanAssignees?q=GoalPlanName='{exactGoalPlanName}'` with bounded pagination. | Returned GoalPlanAssignmentId, GoalPlanName, and minimal count/pagination evidence; retain PersonId, PersonNumber, display, manager, organization, and assignment values in runtime memory only | The finder must advertise GoalPlanId as required. For reconciliation, page to `hasMore=false`, require every returned GoalPlanName to match the fresh selected plan, and bind that result to the verified configured population selector; never infer legal entity from labels or persist individual identities. For the action fallback, send empty query and GoalPlanId in terms. The exact-name fallback is valid only after an exact duplicate-free Goal Plan identity read and only when every returned row repeats that exact name. | Sanitized actual count, pagination state, fresh-read state, plan/scope-match evidence, and no persisted person identities | Return empty READ when no assignees match; stop only on unresolved Goal Plan, ambiguous requested manager/organization criteria, missing GoalPlanId finder contract, incomplete pagination, or a non-exact GoalPlanName fallback row |
| goal_plan_functional_contract_lookup | Plan-goal, document association, or sync action is requested | Exact operation and target | Current Goal Plans describe/OpenAPI and current returned runtime URLs | Child `performanceGoals` create action, returned GoalId,GoalPlanGoalId, `associatedPerfDocumentTypes`, returned GoalPlanDocumentTypeId, `importGoals`, `essProcessTrigger`, allowed methods/media types, and the current/prior Goal Plan values used by the PD-sync predicate | For a goal create, pass current describe plus same-host runtime URLs only to `scripts/goal_plan_runtime.py:resolve_template_goal_create_contract`. It selects the advertised child POST first; it resolves `adfBatchRoot` only for a needed fallback. Discard any Library Goal route, item key, payload schema, Weighting type, DFF part, or concurrency header | Relative path, action schema, item/child identity, media type, concurrency contract, and context-binding record; runtime batch root only when fallback selected | Return `GOAL_PLAN_CREATE_CONTRACT_GAP` when neither create route is available; do not borrow a capture from another tenant, use UI discovery, or ask the consultant for a route |

## Foundation Profile-Option Delegation

A consultant request to inspect or maintain an exact profile option is not a
Goal Plan mutation. Pass the supplied `profile_option_code` unchanged as
`ProfileOptionName` to external capability
`core.fusion-api.apps-common.profile-options` through the parent profile-option
routing contract. Query current definition or effective value before proposing
a provider-owned change. If the requested foundation work needs a code and none
is supplied, ask the consultant for the exact profile option code; do not
substitute the Goal Plan throughput or Redwood-readiness examples. Return
`validation_gap` for an unknown or ambiguous code and
`PROVIDER_SKILL_UNAVAILABLE` when the provider is unavailable.

## Foundation Lookup Delegation

This task does not assert a Goal Plan-specific foundation lookup type. Route a
consultant-supplied exact lookup type/code to external capability
`core.fusion-api.apps-common.lookups` through the parent
lookup-routing contract; do not infer a lookup type from a Goal Plan display
field or send a lookup mutation through a Goal Plans payload.

## Foundation Value-Set Delegation

Route a consultant-supplied exact value-set code to
external capability `core.fusion-api.apps-common.value-sets`
through the parent value-set routing contract. Do not infer a value set from a
Goal Plan display field or send a value-set mutation through a Goal Plans payload.

## Foundation Flexfield Delegation

A consultant-supplied exact Descriptive Flexfield code is not a Goal Plan
payload field. Route it through `core.fusion-api.apps-common` using
external capability `core.fusion-api.apps-common.descriptive-flexfields`
using `HRG_MANAGE_WORKFORCE_GOALS_DESCRIPTIVE_FLEXFIELD` and the parent
flexfield routing contract. The confirmed `HRG_GOAL_PLANS_B` code is routing evidence,
not authority to infer contexts, segments, or runtime attributes; configure
only through the common provider's governed setup-task workflow.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A real worker identifier is resolved | Use only in memory for the approved runtime and redact durable evidence |
| Worker does not exist | Return external GHR/HDL route; do not create here |
| Profile or document type has many matches | Stop and request disambiguation |
| ESS metadata is absent | Assignment may be planned but not submitted |
| A tenant URL or runtime router path is supplied | Discard the host/router UUID and retain only the supported relative resource contract |
| Standard `latest` route is available | Keep `resourceRoot` release-independent; do not replace it with a numeric release from returned links |
| Standard route is unavailable | Resolve one same-host current runtime fallback, reject `rv:null`, keep it in memory only, and finish fallback before preview |
| Authentication is not ready | Run one harmless serialized request; do not start parallel OAuth-dependent commands against the shared callback |
| Search action is HTTP POST | Classify it as READ because the query action has no setup side effect; no mutation approval is required |
| Goal Plan search needs status, dates, configuration, or a Review Period filter | Use the `goalPlans` GET collection query and its resource fields. The advanced-search action has a separate projection: send only `GoalPlanId`, `GoalPlanName`, `ReviewPeriodId`, `ReviewPeriodName`, and `LastUpdateDate` in `displayFields`; never send resource-only `GoalPlanActiveCode` (or infer that every collection attribute is a search attribute). |
| Creation-time filter is requested | Resolve an exact UTC interval, hydrate missing detail fields, filter locally, and sort newest first |
| Eligibility Profile maintenance is requested | Discover the canonical `BEN_MANAGE_ELIGIBILITY_PROFILES` provider; return `PROVIDER_SKILL_UNAVAILABLE` with resume context when it is absent, and never treat the LOV resolver as a mutation provider |
| Goal Plan deletion or Review Period change is requested | Hydrate assignee count and approval status before guidance; never infer zero assignees from an omitted field |
| Assignment rerun is requested | Read current included goals, selected/excluded population, and prior assignment evidence; disclose additive behavior and that later exclusion does not remove earlier assignments |
| Assignee search or removal is requested | Use `goalPlanAssignees` only after current describe confirms it. Search is a read-only ADF action with `query`, `filters`, `displayFields`, `searchFields`, `offset`, and `limit`. GoalPlanId is required; Organization and resolved manager-assignment filters are independent optional refinements. Do not use the VBCS service alias as an API URL |
| Assignee batch delete is requested | Map `goalPlanId=-1` exactly as the verified action scope sentinel and map only fresh returned GoalPlanAssignmentId values to goalPlanAssignmentIdList. Result `0` is successful action completion; re-read selected IDs after one submission and never replay a nonzero or ambiguous result |
| Goal Plan action is requested | `importGoals` and `essProcessTrigger` are ADF action POSTs. Generate the body from current action metadata and fresh state; client-captured parameters are evidence, not a durable payload template |
| Maximum enforcement is requested during create | Bind one approval to the exact environment, stable name+Review Period business key, create payload containing the maximum but omitting enforcement, enforcement-only PATCH, and both verification reads. Resolve the returned item ID after create; continue only when the fresh maximum equals the approved value. An absent enforcement requirement ends after create and leaves the nullable flag omitted/`null`. |
| Plan-goal import is requested | Resolve the current session's WorkerAssignmentId through the existing person/assignment context route. Use `reviewPeriodsLOV` for exact Review Period resolution and `goalPlansLOV` for distinct exact regular source/target plans; map both returned MassRequestIds into `importGoals`, submit once, and re-read target goals after its null result |
| Plan-goal delete is requested | Re-read the target `performanceGoals` child collection and delete only its fresh returned composite item path. A GoalId by itself is insufficient; re-read after one submission and do not replay an ambiguous delete |
| Template-goal create/update is requested | Re-read the exact existing regular plan for `MassRequestId`, then resolve the logged-in admin through a fresh worker/assignment read. For create, use the public `performanceGoals` child POST only when current Goal Plans metadata advertises it; use ADF batch only when the selected operation requires it. Never use `ManagerAssignmentId` or cached runtime metadata. Re-read the Goal Plan performanceGoals collection after success |
| Document association mutation is requested | Resolve the ADF batch root and current child collection first. Add one relative `associatedPerfDocumentTypes` create part with DocumentTypeId only or remove one returned child item with a null payload, and combine it with the parent update part; re-read the collection after one submission |
| PD-sync action is evaluated | Send `essProcessTrigger` only when the documented server predicate is true. Treat a non-empty result as the submitted request ID and an empty result as a completed no-sync result; do not add ESS polling to this Goal Plan route |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_PLANS.LOOKUPS | step | 40 | reference_lookup | resolved->GOAL_PLANS.DEFAULTS;unresolved->GOAL_PLANS.BLOCKED | GOAL_PLANS.DEPENDENCIES | stop | Operation-specific references must be resolved |
| GOAL_PLANS.SEARCH | step | 26 | reference_lookup | found->GOAL_PLANS.DONE_SEARCH;empty->GOAL_PLANS.DONE_SEARCH;unavailable->GOAL_PLANS.BLOCKED | GOAL_PLANS.VALIDATE | stop | list/search is selected, including creation-time filters |


---

# Goal Plan REST and ESS Execution

## Runtime Sources

| Source | Purpose |
|---|---|
| `/hcmRestApi/resources/latest/goalPlans/describe` | Preferred release-independent Goal Plan collection, attributes, operations, and returned child links |
| Trusted current REST link/metadata or approved OpenAPI | Fallback only when the standard `latest` resource is unavailable; resolve one same-host current runtime contract and reject `rv:null` |
| Current Goal Plans describe/OpenAPI plus returned runtime links | Goal Plan goal create/update contract for regular plans. For create, use the advertised `goalPlans/{GoalPlanId}/child/performanceGoals` POST first. Use relative `performanceGoalsV2` paths and a resolved ADF root only when current metadata selects the batch fallback. Never hardcode a tenant host, runtime revision, or release suffix. |
| core.fusion-api.ess-job-submitter | Submit and monitor a separately approved verified Assign Goal Plans job |
| shared setup export/import skills | Catalog-supported FSM CSV routes |

## Execution Contract

| Situation | What Happens |
|---|---|
| Create | For a regular plan, resolve one active Review Period first. When both technical plan dates are omitted, default them from its inclusive range; preserve a complete explicit pair and reject a partial pair. Then search by supplied idempotency key when present; otherwise, when current `GoalPlanId` and `GoalPlanExternalId` metadata both expose server default expressions, use exact Goal Plan name plus associated Review Period duplicate controls, disclose the server-derived External ID behavior, map no client-generated ID, and create inactive only |
| List/search | Use the read-only advanced-search action only for name-based candidate discovery, with its verified search projection. For Review Period filtering or status/dates/configuration, use the read-only `goalPlans` collection query with supported resource fields; hydrate item details when necessary, then return a sanitized list |
| Update | Patch explicit changes and preserve omitted values |
| Activate or inactivate | Use an independent preview and approval; never chain from create |
| Maintain population | For a regular plan, POST one included-worker, excluded-worker, or Eligibility Profile child, or DELETE one freshly returned child row; never invoke ESS |
| Prepare assignment | Preview impact, verify job definition and parameters, then hand off to the core ESS submitter after separate approval |
| Assess Goal Plan delete | Read assignment/approval state and current capability. Assigned plans are not deletable; return guided UI unless an exact governed REST delete contract is advertised |
| Assess assignee delete | Read exact assignees and impact, then return a separately approved Manage Assignees guided route; do not reuse population-child DELETE |
| Add Goal Plan goal | Treat as a governed regular Goal Plan update in planning and approval. If current Goal Plans metadata advertises the child create, POST the exact payload to `goalPlans/{GoalPlanId}/child/performanceGoals`; otherwise require a separately resolved ADF batch create contract. |
| Primary Goal Plan | Set `PrimaryGoalPlanFlag=true`, keep `ReviewPeriodId=null`, omit population/goal children, and never prepare assignment |

## Endpoint

| Action | Method | Path |
|---|---|---|
| Search Goal Plan names | POST (read-only action) | `{resourceRoot}/goalPlans/action/findByAdvancedSearchQuery` with non-empty name query and only `GoalPlanId`, `GoalPlanName`, `ReviewPeriodId`, `ReviewPeriodName`, and `LastUpdateDate` in `displayFields`; parse `result.items` and `result.summary` |
| List/filter Goal Plans | GET | `{resourceRoot}/goalPlans?fields={supportedResourceFields}&q={supportedPredicate}`; use this route for `ReviewPeriodId` filtering or fields such as `GoalPlanActiveCode`, dates, and configuration flags |
| Read | GET | `{resourceRoot}/goalPlans/{GoalPlanId}?fields=*` or the fresh returned item path; expand requested children when needed |
| Create regular or Primary | POST | `{resourceRoot}/goalPlans`, directly or as the validated batch collection root required by current metadata |
| Update, activate, or inactivate | PATCH or current validated update operation | `{resourceRoot}/goalPlans/{GoalPlanId}` using fresh concurrency state; a validated batch update may use the same relative item path |
| Add Goal Plan template goal | POST public child collection when advertised | `{resourceRoot}/goalPlans/{GoalPlanId}/child/performanceGoals` with a current metadata-supported body. It requires current plan `MassRequestId`, active HR-admin context, and a non-null `ReferenceContentItemId` for a Library Goal; dates default from the plan when omitted. |
| Update Goal Plan goal | Current item or dynamically resolved ADF batch operation | Use the current advertised goal-item update operation. If it is an ADF batch update, use `{adfBatchRoot}/` with `parts[0].path="/performanceGoalsV2/{GoalId}"` or the fresh returned item path and `parts[0].operation="update"`. |
| List Goal Plan goals | GET | `{hcmRuntimeRoot}/goalPlans/{GoalPlanId}/child/performanceGoals` or the fresh returned child link; GoalId and GoalPlanGoalId together form the returned delete item identity |
| Delete Goal Plan goal | DELETE | `{hcmRuntimeRoot}/goalPlans/{GoalPlanId}/child/performanceGoals/{GoalId},{GoalPlanGoalId}` or the exact fresh returned child item link; no request body and no GoalId-only path |
| Include worker | POST public child create when current tenant OpenAPI exposes it | `/hcmRestApi/resources/latest/goalPlans/{GoalPlanId}/child/perfGoalIncludedWorkers` (or the same current resolved resource root). Body contains only target `PersonId`, active `AssignmentId`, and normalized string `CascadingLevel`; map `newIncludeWorker.CascadingLevel`, defaulting to `"0"`. Never derive it from workersLov; never `ManagerAssignmentId` or ESS assignment fields. Re-read the child collection after success. |
| Exclude worker | POST or validated batch child create | `{resourceRoot}/goalPlans/{GoalPlanId}/child/perfGoalExcludedWorkers` |
| Associate Eligibility Profile | POST or validated batch child create | `{resourceRoot}/goalPlans/{GoalPlanId}/child/perfGoalEligibilityProfiles`; body maps resolved `EligibilityProfileId`, derived `RequiredFlag`, and skill-derived `TalentObjectType="GOAL"` based on tenant-validated runtime evidence for this Goal Management child only |
| Remove population child | DELETE | Fresh returned item path under the matching child collection |
| Assign Goal Plans | ESS | Exact job definition and parameter contract current_metadata_required until verified |
| Search Goal Plan assignees | POST (read-only ADF action) | `{hcmRuntimeRoot}/goalPlanAssignees/action/findByAdvancedSearchQuery` with empty query and GoalPlanId in `terms`. Append OrganizationId in `terms` only when the Department/Organization UI filter is selected. If a consultant supplies manager PersonId, resolve one current active assignment and append ManagerAssignmentId in its advertised `value` form. Include the supported displayFields/searchFields and bounded offset/limit; parse `result.items` and `result.summary`. |
| Delete Goal Plan assignees | POST (ADF action) | `{hcmRuntimeRoot}/goalPlanAssignees/action/batchDelete` with `goalPlanId=-1` and a metadata-mapped goalPlanAssignmentIdList of fresh returned IDs only. Result `0` is successful action completion; re-read each selected ID after one submission |
| List import Review Periods | GET | `{hcmRuntimeRoot}/reviewPeriodsLOV?finder=findReviewPeriodsForGoals;WorkerAssignmentId={currentWorkerAssignmentId}`; resolve the selected exact ReviewPeriodId |
| List import source plans | GET | `{hcmRuntimeRoot}/goalPlansLOV?finder=findGoalPlansForRPandAssignment;ReviewPeriodId={ReviewPeriodId}` with current supported filtering; resolve distinct exact regular source/target plans and their MassRequestId values |
| Import Plan goals | POST (ADF action) | `{hcmRuntimeRoot}/goalPlans/action/importGoals` with metadata-mapped targetMassRequestId, massRequestId, goalPlanId, and reviewPeriodId after exact target/source/review-period resolution; null result is completed and requires target-goal re-read verification |
| Sync performance documents | POST (ADF action) | `{resourceRoot}/goalPlans/action/essProcessTrigger` after a verified Goal Plan update and separate approval |
| Duplicate a Plan goal | Current metadata action/batch only | Do not infer a generic duplicate endpoint; read the source and use the verified create contract |
| Reorder a Plan goal | Unsupported UI behavior | VBCS does not persist reorder. Return `UNSUPPORTED_UI_BEHAVIOR`; do not infer or probe a REST write |
| List Performance Document Types | GET | `{hcmRuntimeRoot}/talentPerformanceDocumentTypes?limit={pageLimit}`; page returned results and select only an Active type whose dates cover the Goal Plan |
| List Goal Plan document associations | GET | `{hcmRuntimeRoot}/goalPlans/{GoalPlanId}/child/associatedPerfDocumentTypes` or the fresh returned child link; use returned GoalPlanDocumentTypeId only for removal |
| Maintain document association | POST ADF batch root | `{adfBatchRoot}/` with relative `parts`: add path `/goalPlans/{GoalPlanId}/child/associatedPerfDocumentTypes`, operation `create`, and payload mapped only as DocumentTypeId; remove path `/goalPlans/{GoalPlanId}/child/associatedPerfDocumentTypes/{returnedGoalPlanDocumentTypeId}`, operation `delete`, and null payload. Include the parent Goal Plan update part in the same batch; no standalone association edit |

## Required Media Type

Select the media type before sending the first request. Do not probe Fusion by
cycling through content types after a failure.

| Request shape | Required header |
|---|---|
| Top-level JSON object contains a `parts` array, including validated Goal Plan or `performanceGoalsV2` batch create/update | `Content-Type: application/vnd.oracle.adf.batch+json` |
| Custom action path contains `/action/`, including `findByAdvancedSearchQuery` | `Content-Type: application/vnd.oracle.adf.action+json` |
| Ordinary entity or child POST, PUT, or PATCH with a JSON body | `Content-Type: application/json` |
| Ordinary GET with no body | `Accept: application/json`; omit request `Content-Type` |

Batch classification has precedence whenever the top-level `parts` array is
present. Otherwise, the search/list endpoint above is always an ADF action and
must use the action media type. Fail closed if the selected header conflicts
with the path or payload shape. This selection does not combine or relax the
independent mutation and ESS approval gates.

Set `resourceRoot=/hcmRestApi/resources/latest` when current describe metadata
advertises the expected Goal Plan operation. Numeric-release canonical links
are expected server resolution and must not be hardcoded. If the standard route
is unavailable, resolve one trusted current runtime fallback before preview,
reject `rv:null`, and never switch roots after approval. Never store a fallback
host, runtime revision, language/release suffix, object IDs, or returned
concurrency headers. Execute all calls through
`core.auth.fusion-oauth-authentication` and
`core.fusion-api.rest-api-client`. Let those core services resolve the standard
repository environment properties and secure per-user token cache. Chrome is
limited to an OAuth sign-in handoff or an explicitly requested UI test.

### ADF batch root resolution

Most non-batch REST reads, describes, ordinary creates, and ordinary patches
should continue to use `{resourceRoot}`. For top-level `parts` ADF batch calls,
do not assume `{resourceRoot}/` can parse the request. If a batch operation is
required and the ADF runtime root has not already been resolved for the current
session, resolve it before the mutation preview from a trusted same-host
runtime/OpenAPI link, such as a returned ADF runtime self/canonical URL or a
successful `describe.openapi` route.

Use this runtime shape only after resolution:

```text
{host}/hcmRestApi/rest/rv:{runtimeRevision}/en/{release}:{sequence}/
```

Use every path component only from the current runtime route; do not document,
cache, or persist a concrete revision or release/sequence. Keep `parts[].path`
relative, for example `/performanceGoalsV2` or
`/goalPlans/{GoalPlanId}`. If no trusted runtime root can be resolved, stop
with a runtime-route blocker instead of probing write endpoints.

Establish authentication with one harmless serialized request before multiple
metadata/data calls. Do not launch first-use commands in parallel and never
parallelize mutations.

The search POST is semantically read-only and bypasses all mutation approval
nodes. Create, update, status, population, delete, import, and ESS operations
never do.

## Primary Goal Plan payload rules

| Operation | Required mapping | Must be absent or preserved |
|---|---|---|
| Create | `GoalPlanName`, `PrimaryGoalPlanFlag=true`, `ReviewPeriodId=null`, inactive `GoalPlanActiveCode`, metadata/template-derived `StartDate`/`EndDate`, `EnableWeightingFlag=true`, and `EnforceGoalWeightFlag=false`; include other explicitly requested writable scalar fields | Omit `perfGoalIncludedWorkers`, `perfGoalExcludedWorkers`, `perfGoalEligibilityProfiles`, and `performanceGoals` |
| Update | Fresh `GoalPlanId` item path and only explicit writable scalar changes; preserve `PrimaryGoalPlanFlag=true`, null Review Period, omitted fields, and existing technical dates | Do not add regular-plan children or copy a runtime batch envelope, tenant host, object ID, or ETag into durable artifacts |
| Activate/inactivate | Patch only the supported status field after the single-active-Primary check and separate approval | No population or ESS action |

## Functional Payload and Capability Rules

| Area | Mapping or validation rule |
|---|---|
| Regular identity | Require the exact Goal Plan name to be unique within its associated Review Period; dates are validated separately and do not distinguish duplicates (`HRG-3120299`) |
| Goal-setting controls | Map `GoalSettingStartDate`, `GoalSettingEndDate`, `RestrictGoalCreationFlag`, and `RestrictGoalUpdateFlag` independently only when current metadata advertises them. The two restriction flags apply to workers only; validate a complete ordered pair within Goal Plan dates and require confirmation of any proposed missing boundary. |
| Evaluation and access | Preserve or explicitly map `EvaluationType`, `GoalAccessLevelCode`, and `CanDelHRGoal` against current allowed values. Goal access remains independent of worker-only Goal Setting Info restrictions. |
| Weight and count | Validate `EnableWeightingFlag` before `EnforceGoalWeightFlag`; validate optional goal-count fields and require `MaximumGoalsNumberInGoalPlan` before `EnforceMaximumGoalsInGpFlag=true` |
| Plan goals | Never map for Primary. For regular plans, keep goal dates inside plan dates and include only enabled library, measurement, task, target-outcome, and assignee-edit sections |
| Import Goals | Treat as an application capability for copying goals from another plan, not as FSM CSV import and not as a generic REST batch. Resolve the selected Review Period using current WorkerAssignmentId, then map targetMassRequestId, source massRequestId, target goalPlanId, and reviewPeriodId from the distinct fresh plan/period rows |
| Multiple profiles | Map each returned profile association independently and retain the required flag; all required profiles use AND semantics |
| Population scope | Preserve the exact selected/direct/all-report scope and exclusions; do not reduce a hierarchy scope to a single worker row |
| Document types | Require Active status and full date coverage before association. Re-read current associations, add only a non-associated DocumentTypeId, remove only the returned GoalPlanDocumentTypeId, and include the parent update as another relative part in the same ADF batch |

## Assignment and Rerun Semantics

- Goal Plan goals are not assigned automatically. The documented Scheduler
  fields are process type `Assign goal plans`, process name equal to the Goal
  Plan name, and a resolved effective date (supplied or defaulted to today at
  preview and retained through approval). The exact technical job definition
  and any remaining parameter mapping stay blocked until verified.
- A rerun adds included goals for newly selected workers and newly included
  goals for selected workers. Already assigned goals are unchanged. Workers
  excluded after an earlier run retain those goals; removal requires a
  separate, explicitly approved action.
- The multithread parent remains paused until all child processes complete.
  `HRG_GP_MAX_THREADS` is only the maximum; actual child count is derived with
  `HRG_GP_MINCOUNT_EACHTHREAD` and `HRG_GP_MINCOUNT_LASTTHREAD`. Profile-option
  maintenance is not performed by this skill.

## Functional-flow REST contracts

| Functional flow | Contract status | Execution rule |
|---|---|---|
| Assignee search | Verified ADF action | POST `goalPlanAssignees/action/findByAdvancedSearchQuery` with empty query and GoalPlanId `terms`. Department UI selection maps to optional OrganizationId `terms`. A supplied manager PersonId is first resolved to one active assignment, then maps to optional ManagerAssignmentId in its advertised `value` form. Send the verified display/search fields, page `result.summary`, and treat an empty result as a completed read. |
| Assignee batch delete | Verified ADF action | POST `goalPlanAssignees/action/batchDelete` with `goalPlanId=-1` and fresh returned GoalPlanAssignmentId values only. Preview exact count/impact; result `0` is successful action completion and requires re-read after one submission |
| Import goals | Verified ADF action | Resolve the current WorkerAssignmentId, selected Review Period, and distinct exact regular source/target plans through `reviewPeriodsLOV` and `goalPlansLOV`. POST `importGoals` with targetMassRequestId, massRequestId, goalPlanId, and reviewPeriodId; a null result is completed, then re-read target goals to verify |
| Performance-document sync | Verified guarded pre-batch action | POST `goalPlans/action/essProcessTrigger` as an ADF action with a `params` object before the main `goalPlans/batch` update. Map mode, disablePD from RequestStatus, pdRedwoodEnabled, AssigneeCount, pending Goal Plan values, and current-vs-prior changed flags. Submit only when mode is EDIT_GOAL_PLAN, pdRedwoodEnabled is Y, disablePD is N, AssigneeCount is greater than zero, and a documented change trigger is true. Pass the result into main batch-payload construction: a non-empty result is the submitted ESS request ID; an empty result is a valid no-sync outcome and requires no ESS polling |
| Plan-goal duplicate | Current public child route evidenced | Read the source goal and existing plan goals; use the advertised child-create contract and block only if current metadata no longer advertises it and no current batch fallback exists. |
| Plan-goal delete | Verified child delete | GET fresh `performanceGoals` rows, then DELETE the returned `GoalId,GoalPlanGoalId` composite item path with no body. Re-read the target collection after one submission; never use GoalId alone or retry an ambiguous deletion |
| Plan-goal reorder | Unsupported UI behavior | VBCS itself does not persist reorder. Return `UNSUPPORTED_UI_BEHAVIOR`; do not treat it as a pending REST gap or infer a write |
| Document associations and child updates | Verified ADF batch child delta | Read `talentPerformanceDocumentTypes` and fresh `associatedPerfDocumentTypes` rows. Add with only DocumentTypeId; delete with the returned GoalPlanDocumentTypeId and null payload. Keep child paths relative, include the parent update part in the same approved ADF batch, and re-read the collection after one submission; no standalone association edit |

## Goal Plan Goal Create-Contract Selection

Use this section whenever the consultant asks to add or update a performance
goal inside an existing regular Goal Plan. This is an update to the Goal Plan
configuration scope. Resolve the current Goal Plans create contract before
constructing a body: an advertised public child POST is preferred; the
`performanceGoalsV2` ADF batch endpoint is a fallback, not a universal route.

### Context-binding gate

Before building a first-goal request, establish a new runtime execution
context:

| Bind | Required value | Must be discarded from a prior Library Goal context |
|---|---|---|
| Business object | `goal_plan_template_goal` | `libraryGoals` root/path and composite Library Goal key |
| Create payload contract | `goalPlans_performanceGoals_child_create` when current metadata advertises its child POST; otherwise `performanceGoalsV2_batch` only with a resolved fallback | Library Goal parent fields such as `PerfCategoryCode` and string Weighting |
| Runtime identity | Fresh regular Goal Plan, Review Period, MassRequestId, and current HR-admin PersonId/primary AssignmentId | Library Goal identity, child links, and DFF assumptions |
| Route and concurrency | Current child POST action/media type or, only for batch fallback, fresh batch-root output and its advertised header rule | Library Goal ETag/changeIndicator interpretation or `If-Match` rule |

The create contract is a resolver output, not a consultant input and not a
durable literal. Call `resolve_template_goal_create_contract` with current
Goal Plans describe/OpenAPI data. If it cannot find an advertised child POST
or a current batch fallback, return `GOAL_PLAN_CREATE_CONTRACT_GAP`; do not use
browser discovery, borrow a root from another object, or construct a revision.
If a batch root is selected, bind it only to this single preview/approval
fingerprint.

### Add Goal Plan goal

1. Re-read the exact existing Goal Plan by ID immediately before payload
   construction with `fields=GoalPlanId,GoalPlanName,ReviewPeriodId,PrimaryGoalPlanFlag,StartDate,EndDate,MassRequestId`
   (the `TEMPLATE_GOAL_PLAN_FIELDS` projection in `scripts/goal_plan_runtime.py`).
   Use `resolve_goal_plan_mass_request_id` to verify exact identity, a regular
   plan with Review Period, and one current positive `MassRequestId`. A compact
   response that omits the key requires this projected read; an explicit null
   after projection is a real missing-context blocker. `MassRequestId` is
   applicable only here; a new Goal Plan create must omit it.
2. Re-read the Review Period and verify the Goal Plan dates and requested goal
   dates are inside the Review Period and Goal Plan envelopes. For a selected
   Performance Library Goal, re-read the source and set `ReferenceContentItemId`
   from its fresh returned identity. When both template-goal dates are omitted,
   default them from the existing Goal Plan Start Date and End Date; preserve a
   complete explicit pair and reject a partial pair.
3. Resolve the authenticated HR/admin through the owning current-worker adapter
   from a fresh worker/assignment read and use that admin's confirmed active
   primary `AssignmentId`, along with its
   `PersonId`, only as request context. These values are not selected worker
   population, Eligibility Profile membership, `ManagerAssignmentId`, or ESS
   assignment. Never resolve it from a browser-visible display name.
4. When the current contract advertises the public child create, submit the
   direct body to `{resourceRoot}/goalPlans/{GoalPlanId}/child/performanceGoals`
   using its advertised media type. Only when that contract is absent may the
   preview use the ADF batch body below against a resolved `adfBatchRoot`. Do
   not hardcode a host, `rv:*`, language, release suffix, sequence, object ID,
   or returned ETag in durable skill content.
5. After a successful response, re-read the Goal Plan
   `performanceGoals` collection and verify the created row before reporting
   success. Never infer success from an HTTP status alone.

The following ADF envelope is the **batch fallback only**:

```http
POST {adfBatchRoot}/
Content-Type: application/vnd.oracle.adf.batch+json
```

```json
{
  "parts": [
    {
      "id": "Create-goal-1",
      "path": "/performanceGoalsV2",
      "operation": "create",
      "payload": {
        "PersonId": "<current-hr-admin-person-id>",
        "AssignmentId": "<current-hr-admin-active-assignment-id>",
        "GoalPlanId": "<goal-plan-id>",
        "ReferenceContentItemId": "<selected-library-goal-id>",
        "ReviewPeriodId": "<review-period-id>",
        "PercentCompletion": "0",
        "RequestContext": "AdminUI",
        "GoalSourceCode": "HR",
        "GoalVersionTypeCode": "MASS_REQ",
        "MassRequestId": "<goal-plan-mass-request-id>",
        "PriorityCode": "<resolved-priority-code>",
        "GoalName": "<goal-name>",
        "Description": "<plain-description>",
        "SuccessCriteria": "<p>success criteria html</p>",
        "StartDate": "YYYY-MM-DD",
        "TargetCompletionDate": "YYYY-MM-DD",
        "Weighting": 100,
        "CategoryCode": "<resolved-category-code>",
        "Comments": "<p>comments html</p>",
        "AllowKeyAttrUpdateFlag": true,
        "AllowDelGoalCode": "<resolved-delete-access-code>",
        "perfGoalMeasurements": [],
        "perfGoalAttachments": []
      }
    }
  ]
}
```

`SuccessCriteria` and `Comments` are accepted as HTML strings only when the
selected current child or batch schema advertises them. Do not send them
through child/enclosure links unless a separate current working contract has
been verified for that specific operation.

`adfBatchRoot` is environment-specific and must be resolved at runtime. Working
captures show the shape `{host}/hcmRestApi/rest/rv:{runtimeRevision}/en/{release}:{sequence}/`
with relative `parts[].path` values such as `/performanceGoalsV2`. Store only
this resolution rule, never the resolved host, revision, language, release, or
sequence.

### Update Goal Plan goal

For an existing goal row, first resolve the exact `GoalId` through
`performanceGoalsV2` or the Goal Plan's returned goal association details.
Then use one ADF batch update with top-level `parts` and preserve omitted
values. Use the fresh item path returned by Fusion when available; otherwise
use the verified relative path `/performanceGoalsV2/{GoalId}`. Show before and
after values and require an independent approval fingerprint.

`Weighting` in this Goal Plan goal contract is numeric. It is a different
object and schema from a Performance Library Goal parent, whose update part is
under `/libraryGoals/{freshReturnedItemKey}` and whose `Weighting` is a string.
Do not move a batch part, payload field type, composite key, or DFF child part
between those contracts. Include `perfGoalsDFF` only when the selected Goal
Plan goal operation explicitly requests DFF data and fresh metadata advertises
the required child operation.

### Update Goal Plan scalar fields by batch

When a captured working contract or current metadata requires ADF batch for
Goal Plan scalar update, use:

```http
POST {adfBatchRoot}/
Content-Type: application/vnd.oracle.adf.batch+json
```

```json
{
  "parts": [
    {
      "id": "Update-goalPlan",
      "path": "/goalPlans/{GoalPlanId}",
      "operation": "update",
      "payload": {
        "...": "only explicitly requested writable fields"
      }
    }
  ]
}
```

This batch shape is not a license to combine operations. Goal Plan scalar
updates, Goal Plan goal creates, activation, population changes, and ESS
submission each need their own preview and approval unless the user has
approved one exact unchanged multi-part request.

## Preview Pattern

| Step | Requirement |
|---|---|
| 1 | Cache lean current Goal Plan attributes from describe |
| 2 | Generate saved mapped payload and mapping report for one selected REST operation |
| 3 | Show dependency state, operation-specific before/after values, population impact, environment, and exact payload or ESS parameters; retain the fingerprint internally |
| 4 | Apply the [shared Goal Management approval convention](../../../goal-management-common/approval-convention.md). Accept a clear contextual affirmative only for one immediately preceding unchanged preview, identified operation, or explicitly combined batch; never require the consultant to repeat the fingerprint |

## Live Pattern

| Step | Requirement |
|---|---|
| 1 | Re-read target and dependencies; stale state invalidates approval |
| 2 | Submit one REST mutation or one ESS job; never combine them |
| 3 | Re-read REST state with `fields=*` or an explicit complete parent/child field set, or poll ESS within configured timeout, and classify the outcome |
| 4 | Never replay an ambiguous REST or ESS submission automatically |

## ESS Handoff Contract

`GOAL_PLANS.ASSIGNMENT_READY` is a governed handoff terminal, not an ESS write
node. Goal Plans must route the following inputs to
`core.fusion-api.ess-job-submitter`; it must not replay the captured Scheduler
JSON or call `/ess/rest/scheduler/v1/requests` directly.

| Dependent-skill input | Goal Plan source and gate |
|---|---|
| `fusion_environment_context` | Current configured target environment, matching all fresh Goal Plan reads and the approved preview. |
| `request_payload` | Complete Scheduler body whose `jobDefinitionId`, `application`, optional request fields, and `requestParameters` mapping have been verified from current authoritative evidence. The raw sample is not a source of truth. |
| `execution_options` | Approved timeout, polling, and submit-only/monitoring behavior. |
| Handoff audit evidence retained by Goal Plans | Fresh regular-plan `GoalPlanId`, `GoalPlanName`, `MassRequestId`, process type `Assign goal plans`, resolved effective date (supplied or defaulted to today at preview), current configured population selector and ESS execution approval. |

The dependent skill submits and tracks the exact `request_payload`, returning a
sanitized request ID and status. Use the Goal Management adapter
`scripts/goal_plan_ess_handoff.py` with approved payload, environment, and a stable
project-local run directory. It owns the attempt record and checkpoint; Core
receives only supported arguments: `--submit-only --retries 0 --output` for
submission, then request-ID-only bounded polling with a distinct
execution-result output. Treat a still-running local command session or empty
incremental output as pending local execution and continue that same session.
After the accepted-request checkpoint exists, every continuation reads its
request ID and performs tracking only. A pre-existing checkpoint forbids a new
submit call. Before invoking Core, the adapter saves the effective payload digest
and environment and locks the run directory. If checkpoint finalization failed,
recover the request ID from the valid Core submission result in that same run.
An existing attempt without a recoverable result is unknown and must not be
resubmitted. Never pass `--submission-checkpoint` to Core. If the job definition or any parameter mapping cannot be verified,
do not invoke the dependent skill: return a blocker with the unresolved
contract field and preserve the assignment evidence for resume.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_PLANS.READ | step | 25 | reference_lookup | found->GOAL_PLANS.DONE_READ;missing->GOAL_PLANS.BLOCKED | GOAL_PLANS.VALIDATE | stop | get is selected |
| GOAL_PLANS.REST_DESCRIBE | step | 70 | reference_lookup | ready->GOAL_PLANS.REST_PAYLOAD;unavailable->GOAL_PLANS.BLOCKED | GOAL_PLANS.DESIGN | stop | A REST mutation is selected |
| GOAL_PLANS.REST_PAYLOAD | step | 80 | reference_lookup | mapped->GOAL_PLANS.WRITE_ROUTE;rejected->GOAL_PLANS.BLOCKED | GOAL_PLANS.REST_DESCRIBE | stop | Current Goal Plan metadata is available |
| GOAL_PLANS.CREATE_PREVIEW | decision | 100 | reference_lookup | reviewed->GOAL_PLANS.CREATE_APPROVAL;blocked->GOAL_PLANS.BLOCKED | GOAL_PLANS.REST_PAYLOAD, GOAL_PLANS.WRITE_ROUTE | stop | create is selected |
| GOAL_PLANS.CREATE_APPROVAL | decision | 110 | reference_lookup | approved->GOAL_PLANS.CREATE;declined->GOAL_PLANS.BLOCKED | GOAL_PLANS.CREATE_PREVIEW | stop | Final inactive-create preview is reviewed |
| GOAL_PLANS.CREATE | step | 120 | reference_lookup | verified->GOAL_PLANS.CREATE_POST_WRITE_ROUTE;ambiguous->GOAL_PLANS.UNKNOWN;failed->GOAL_PLANS.BLOCKED | GOAL_PLANS.CREATE_APPROVAL | stop | Approved create is ready |
| GOAL_PLANS.CREATE_POST_WRITE_ROUTE | decision | 121 | evaluate_result | complete->GOAL_PLANS.DONE_CREATED;maximum_persisted_enforcement_pending->GOAL_PLANS.ENFORCE_MAXIMUM | GOAL_PLANS.CREATE | stop | The approved create is verified and the staged maximum-enforcement plan is evaluated |
| GOAL_PLANS.ENFORCE_MAXIMUM | step | 122 | reference_lookup | verified->GOAL_PLANS.DONE_CREATED;ambiguous->GOAL_PLANS.UNKNOWN;failed->GOAL_PLANS.BLOCKED | GOAL_PLANS.CREATE_POST_WRITE_ROUTE | stop | One approved staged create verified the requested maximum and explicit enforcement remains pending |
| GOAL_PLANS.UPDATE_PREVIEW | decision | 130 | reference_lookup | reviewed->GOAL_PLANS.UPDATE_APPROVAL;blocked->GOAL_PLANS.BLOCKED | GOAL_PLANS.REST_PAYLOAD, GOAL_PLANS.WRITE_ROUTE | stop | update is selected |
| GOAL_PLANS.UPDATE_APPROVAL | decision | 140 | reference_lookup | approved->GOAL_PLANS.UPDATE;declined->GOAL_PLANS.BLOCKED | GOAL_PLANS.UPDATE_PREVIEW | stop | Final update preview is reviewed |
| GOAL_PLANS.UPDATE | step | 150 | reference_lookup | verified->GOAL_PLANS.DONE_UPDATED;ambiguous->GOAL_PLANS.UNKNOWN;failed->GOAL_PLANS.BLOCKED | GOAL_PLANS.UPDATE_APPROVAL | stop | Approved update is ready |
| GOAL_PLANS.ACTIVATE_PREVIEW | decision | 160 | reference_lookup | reviewed->GOAL_PLANS.ACTIVATE_APPROVAL;blocked->GOAL_PLANS.BLOCKED | GOAL_PLANS.REST_PAYLOAD, GOAL_PLANS.WRITE_ROUTE | stop | activate is independently selected |
| GOAL_PLANS.ACTIVATE_APPROVAL | decision | 170 | reference_lookup | approved->GOAL_PLANS.ACTIVATE;declined->GOAL_PLANS.BLOCKED | GOAL_PLANS.ACTIVATE_PREVIEW | stop | Final activation preview is reviewed |
| GOAL_PLANS.ACTIVATE | step | 180 | reference_lookup | verified->GOAL_PLANS.DONE_ACTIVATED;ambiguous->GOAL_PLANS.UNKNOWN;failed->GOAL_PLANS.BLOCKED | GOAL_PLANS.ACTIVATE_APPROVAL | stop | Approved activation is ready |
| GOAL_PLANS.INACTIVATE_PREVIEW | decision | 190 | reference_lookup | reviewed->GOAL_PLANS.INACTIVATE_APPROVAL;blocked->GOAL_PLANS.BLOCKED | GOAL_PLANS.REST_PAYLOAD, GOAL_PLANS.WRITE_ROUTE | stop | inactivate is independently selected |
| GOAL_PLANS.INACTIVATE_APPROVAL | decision | 200 | reference_lookup | approved->GOAL_PLANS.INACTIVATE;declined->GOAL_PLANS.BLOCKED | GOAL_PLANS.INACTIVATE_PREVIEW | stop | Final inactivation preview is reviewed |
| GOAL_PLANS.INACTIVATE | step | 210 | reference_lookup | verified->GOAL_PLANS.DONE_INACTIVATED;ambiguous->GOAL_PLANS.UNKNOWN;failed->GOAL_PLANS.BLOCKED | GOAL_PLANS.INACTIVATE_APPROVAL | stop | Approved inactivation is ready |
| GOAL_PLANS.INCLUDE_WORKER_PREVIEW | decision | 220 | reference_lookup | reviewed->GOAL_PLANS.INCLUDE_WORKER_APPROVAL;blocked->GOAL_PLANS.BLOCKED | GOAL_PLANS.REST_PAYLOAD, GOAL_PLANS.WRITE_ROUTE | stop | include_worker is selected for a regular plan |
| GOAL_PLANS.INCLUDE_WORKER_APPROVAL | decision | 230 | reference_lookup | approved->GOAL_PLANS.INCLUDE_WORKER;declined->GOAL_PLANS.BLOCKED | GOAL_PLANS.INCLUDE_WORKER_PREVIEW | stop | Final included-worker change is reviewed |
| GOAL_PLANS.INCLUDE_WORKER | step | 240 | reference_lookup | verified->GOAL_PLANS.DONE_INCLUDED_WORKER;ambiguous->GOAL_PLANS.UNKNOWN;failed->GOAL_PLANS.BLOCKED | GOAL_PLANS.INCLUDE_WORKER_APPROVAL | stop | Approved included-worker child create is ready |
| GOAL_PLANS.EXCLUDE_WORKER_PREVIEW | decision | 250 | reference_lookup | reviewed->GOAL_PLANS.EXCLUDE_WORKER_APPROVAL;blocked->GOAL_PLANS.BLOCKED | GOAL_PLANS.REST_PAYLOAD, GOAL_PLANS.WRITE_ROUTE | stop | exclude_worker is selected for a regular plan |
| GOAL_PLANS.EXCLUDE_WORKER_APPROVAL | decision | 260 | reference_lookup | approved->GOAL_PLANS.EXCLUDE_WORKER;declined->GOAL_PLANS.BLOCKED | GOAL_PLANS.EXCLUDE_WORKER_PREVIEW | stop | Final excluded-worker change is reviewed |
| GOAL_PLANS.EXCLUDE_WORKER | step | 270 | reference_lookup | verified->GOAL_PLANS.DONE_EXCLUDED_WORKER;ambiguous->GOAL_PLANS.UNKNOWN;failed->GOAL_PLANS.BLOCKED | GOAL_PLANS.EXCLUDE_WORKER_APPROVAL | stop | Approved excluded-worker child create is ready |
| GOAL_PLANS.ASSOCIATE_PROFILE_PREVIEW | decision | 280 | reference_lookup | reviewed->GOAL_PLANS.ASSOCIATE_PROFILE_APPROVAL;blocked->GOAL_PLANS.BLOCKED | GOAL_PLANS.REST_PAYLOAD, GOAL_PLANS.WRITE_ROUTE | stop | associate_profile is selected for a regular plan |
| GOAL_PLANS.ASSOCIATE_PROFILE_APPROVAL | decision | 290 | reference_lookup | approved->GOAL_PLANS.ASSOCIATE_PROFILE;declined->GOAL_PLANS.BLOCKED | GOAL_PLANS.ASSOCIATE_PROFILE_PREVIEW | stop | Final profile association is reviewed |
| GOAL_PLANS.ASSOCIATE_PROFILE | step | 300 | reference_lookup | verified->GOAL_PLANS.DONE_PROFILE_ASSOCIATED;ambiguous->GOAL_PLANS.UNKNOWN;failed->GOAL_PLANS.BLOCKED | GOAL_PLANS.ASSOCIATE_PROFILE_APPROVAL | stop | Approved Eligibility Profile child create is ready |
| GOAL_PLANS.REMOVE_POPULATION_PREVIEW | decision | 310 | reference_lookup | reviewed->GOAL_PLANS.REMOVE_POPULATION_APPROVAL;blocked->GOAL_PLANS.BLOCKED | GOAL_PLANS.REST_PAYLOAD, GOAL_PLANS.WRITE_ROUTE | stop | remove_population is selected for a returned regular-plan child row |
| GOAL_PLANS.REMOVE_POPULATION_APPROVAL | decision | 320 | reference_lookup | approved->GOAL_PLANS.REMOVE_POPULATION;declined->GOAL_PLANS.BLOCKED | GOAL_PLANS.REMOVE_POPULATION_PREVIEW | stop | Final population-child removal is reviewed |
| GOAL_PLANS.REMOVE_POPULATION | step | 330 | reference_lookup | verified->GOAL_PLANS.DONE_POPULATION_REMOVED;ambiguous->GOAL_PLANS.UNKNOWN;failed->GOAL_PLANS.BLOCKED | GOAL_PLANS.REMOVE_POPULATION_APPROVAL | stop | Approved returned child deletion is ready |
| GOAL_PLANS.ASSIGNEE_SEARCH | step | 335 | reference_lookup | found->GOAL_PLANS.DONE_ASSIGNEE_SEARCH;empty->GOAL_PLANS.DONE_ASSIGNEE_SEARCH;unavailable->GOAL_PLANS.BLOCKED | GOAL_PLANS.VALIDATE | stop | A bounded Goal Plan assignee search is selected |
| GOAL_PLANS.FUNCTIONAL_PREVIEW | decision | 336 | reference_lookup | reviewed->GOAL_PLANS.FUNCTIONAL_APPROVAL;blocked->GOAL_PLANS.BLOCKED | GOAL_PLANS.REST_PAYLOAD, GOAL_PLANS.WRITE_ROUTE | stop | One plan-goal, document association, assignee removal, or performance-document sync action has a verified contract |
| GOAL_PLANS.FUNCTIONAL_APPROVAL | decision | 337 | reference_lookup | approved->GOAL_PLANS.FUNCTIONAL_MUTATION;declined->GOAL_PLANS.BLOCKED | GOAL_PLANS.FUNCTIONAL_PREVIEW | stop | Final functional-flow preview is reviewed |
| GOAL_PLANS.FUNCTIONAL_MUTATION | step | 338 | reference_lookup | verified->GOAL_PLANS.DONE_FUNCTIONAL_CHANGE;assignees_removed->GOAL_PLANS.DONE_ASSIGNEES_REMOVED;document_associated->GOAL_PLANS.DONE_DOCUMENT_ASSOCIATED;document_removed->GOAL_PLANS.DONE_DOCUMENT_REMOVED;sync_submitted->GOAL_PLANS.DONE_PD_SYNC_SUBMITTED;sync_no_change->GOAL_PLANS.DONE_PD_SYNC_NO_CHANGE;ambiguous->GOAL_PLANS.UNKNOWN;failed->GOAL_PLANS.BLOCKED | GOAL_PLANS.FUNCTIONAL_APPROVAL | stop | Approved current-metadata functional action is ready |
| GOAL_PLANS.ASSIGNMENT_PREVIEW | decision | 340 | reference_lookup | reviewed->GOAL_PLANS.ASSIGNMENT_APPROVAL;blocked->GOAL_PLANS.BLOCKED | GOAL_PLANS.DESIGN | stop | regular-plan prepare_assignment is selected and the ESS contract is verified |
| GOAL_PLANS.ASSIGNMENT_APPROVAL | decision | 350 | reference_lookup | approved->GOAL_PLANS.ASSIGNMENT_READY;declined->GOAL_PLANS.BLOCKED | GOAL_PLANS.ASSIGNMENT_PREVIEW | stop | Configured population selector and ESS parameters are reviewed |


---

# Goal Plan Captured API Path Reference

This reference normalizes the supplied working REST captures. Stable paths are
shown without a tenant host, `rv:` revision, release suffix, or captured IDs.
Values in a raw sample are examples, never durable contract constants.

| Purpose | Method | Stable path | Runtime values and payload guidance |
|---|---|---|---|
| Name search | POST | `/goalPlans/action/findByAdvancedSearchQuery` | ADF action body includes `query`, `filters`, `displayFields`, `limit`, and `offset`. |
| Search Goal Plan assignees | POST | `/goalPlanAssignees/action/findByAdvancedSearchQuery` | Read-only ADF action. Send `query: ""`, GoalPlanId in `filters[].terms`, the verified display/search projection, and offset/limit. Department UI selection maps to optional OrganizationId in `terms`. A manager PersonId is resolved at runtime to one current active assignment before the optional ManagerAssignmentId filter is sent in its advertised `value` form. `result.summary` supplies count/paging and `result.items` supplies fresh GoalPlanAssignmentId values. |
| Eligibility Profile LOV | GET | `/eligibilityProfilesLOV` | Search terms and pagination are runtime query inputs. |
| Worker LOV configuration | GET | `/hcmRestApi/redwood/{release}/hcmLovConfig?lovName=workersLov` | `{release}` is runtime-specific; the stable service operation is `hcmLovConfig` for worker selection only. It does not provide or validate CascadingLevel. |
| Read worker/direct reports | GET | `/publicWorkers/{PersonId}` | `PersonId` is from current identity or selected worker context; request only needed fields/expansion. |

`CascadingLevel` is supplied directly as a local string in an include-worker
payload (the capture demonstrates `"2"`); it has no captured LOV endpoint.
Default omitted values to `"0"`, validate the local value set in
`ora_defaulting_rules.md`, and use worker hierarchy data only when a current
advertised worker read exposes it.
| Create Goal Plan | POST | `/goalPlans` | Body contains only metadata-supported Goal Plan fields. A captured `ReviewPeriodId` is resolved from the selected current period. |
| Read Goal Plan/Mass Request | GET | `/goalPlans/{GoalPlanId}` | `GoalPlanId` comes from the selected/fresh Goal Plan; use `fields` and child expansion only as needed. |
| Include/exclude worker or associate eligibility profile | POST | `/goalPlans/{GoalPlanId}/child/{childCollection}` | `{childCollection}` is the advertised/fresh returned child link: `perfGoalIncludedWorkers`, `perfGoalExcludedWorkers`, or `perfGoalEligibilityProfiles`. Worker and profile IDs are runtime-resolved. For `perfGoalEligibilityProfiles`, the payload maps resolved `EligibilityProfileId`, derived `RequiredFlag`, and skill-derived `TalentObjectType="GOAL"` based on tenant-validated runtime evidence. Do not apply this value to other products' eligibility-profile associations without their own verified contract. ADF batch captures retain relative `parts[].path` only. |
| Update Goal Plan | PATCH or ADF batch update | `/goalPlans/{GoalPlanId}` | Resolve current metadata and concurrency state. For batch, resolve the current ADF batch root and retain a relative part path only. |
| List Performance Document Types | GET | `/talentPerformanceDocumentTypes` | Page current results and select active types whose dates cover the plan. |
| List document associations | GET | `/goalPlans/{GoalPlanId}/child/associatedPerfDocumentTypes` | Use the fresh returned collection/item link and returned association ID for removal. |
| List Goal Plans | GET | `/goalPlans` | Query fields, predicates, order, limit, and offset are runtime inputs. |
| Create template goal | POST | `/goalPlans/{GoalPlanId}/child/performanceGoals` when current Goal Plans metadata advertises it | Resolve fresh Goal Plan `MassRequestId` and authenticated caller context. A library-backed addition has non-null `ReferenceContentItemId`; an independently authored goal does not. Default omitted goal dates from the Goal Plan. |
| Create template-goal fallback / update | Current batch operation | `/performanceGoalsV2` or `/performanceGoalsV2/{GoalId}` as a relative batch part | Resolve the current ADF batch root only when create lacks the advertised child POST or current update metadata selects batch. Resolve fresh Goal Plan `MassRequestId`, current admin context, and returned `GoalId` as applicable. |

## Weight-update schema boundary

For an existing Goal Plan template/mass-request Performance Goal, the batch
update part belongs under `/performanceGoalsV2/{GoalId}` and `Weighting` is a
number. This is not the Performance Library Goal contract: never use
`/libraryGoals`, `PerfCategoryCode`, a Library Goal composite item key, or a
Library Goal string Weighting value. A `perfGoalsDFF` part may be used only for
an explicitly requested current-metadata-supported DFF change; do not copy an
empty DFF part from a capture.
| List Goal Plan goals | GET | `/goalPlans/{GoalPlanId}/child/performanceGoals` | `GoalPlanId` is current. Returned `GoalId` and `GoalPlanGoalId` form the goal-row identity. |
| Submit Goal Plan assignment | Dependent-skill route | `core.fusion-api.ess-job-submitter` → `/ess/rest/scheduler/v1/requests` | This is an ESS service path, not a Goal Plans resource path. Use Manage Goal Scheduled Process with job definition `JobDefinition://oracle/apps/ess/hcm/goals/core/ScheduleProcessJobDef`, application `EarHcmEss`, product `HRG`, and mode `ASSIGN_GOAL_PLANS`. Build values from the selected current active regular Goal Plan and approved effective date. |

The ordinary Goal Plan collection uses `{resourceRoot}`. ADF batch calls use a
separately resolved current same-host batch root; neither root is persisted.

## Mutation preflight and verification

Before every Goal Plan or Goal Plan child mutation, resolve current
`/goalPlans/describe` metadata. For template-goal create, select the advertised
child POST before considering a batch fallback; resolve a same-host batch root
only when the selected operation needs it. Confirm the advertised method,
writable fields, media type, child/action link, and concurrency behavior. For a new Goal Plan, run
the exact duplicate/Review Period checks first; it has no target item to GET.
For update, status, population, document association, or plan-goal operations,
immediately GET the parent and, when relevant, its child collection before
preview/submission. Use fresh returned IDs, links, `MassRequestId`, and ETag or
other optimistic-lock state when supplied. Re-read the changed parent or child
after one submission. The ESS request follows its separate current-metadata
and approval gate; a captured scheduler body is not a preflight substitute.

## Narrow-delta payload rule

Captured Goal Plan update and batch bodies are field examples, not reusable
templates. A create maps only current metadata-required fields plus explicitly
requested supported optional fields. A parent update maps only the requested
scalar changes; it must not replay dates, status, review period, weighting,
restrictions, DFF rows, or other captured values merely because they were in a
successful update.

Population and document-association changes are one explicit child delta at a
time. Use one current returned child link/ID and a body only for that child;
do not resend sibling population or association rows. A `performanceGoalsV2`
batch contains only the explicit goal or goal-child part(s) being changed and
must not copy unrelated parent parts, DFF parts, measurement rows, or captured
goal fields. The scheduler request is built only from current verified ESS
metadata; do not replay its captured parameter list.

## ESS dependent-skill routing

Goal Plans owns business readiness; `core.fusion-api.ess-job-submitter` owns
ESS REST submission and tracking. Do not pass the captured Scheduler JSON to
the dependent skill. Build the handoff from fresh approved state:

| Handoff field | Source and rule |
|---|---|
| `fusion_environment_context` | Current configured target environment; it must match the environment used for Goal Plan reads and the approval preview. |
| `assignment_evidence.goal_plan_id`, `goal_plan_name`, `mass_request_id` | Fresh exact regular Goal Plan read. `MassRequestId` is mandatory for assignment and is never copied from the capture. |
| `assignment_evidence.process_type`, `effective_date` | Business intent `Assign goal plans` plus the explicitly approved effective date. |
| `assignment_evidence.population_selector` | Fresh configured selector and execution approval. ESS calculates eligibility; actual counts are recorded after execution. |
| `request_payload` | Complete ESS body produced from the verified Assign Goal Plans Scheduler contract: `submit.argument1=ASSIGN_GOAL_PLANS`; `submit.argument2=GoalPlanName`; `submit.argument3=null`; `submit.argument4=StartDate`; `submit.argument5=EndDate`; `submit.argument6=MassRequestId`; `submit.argument7=null`; `submit.argument8=null`; `submit.argument9-submit.argument11` omitted values; `submit.argument12=approved effective date`; `submit.argument13=Assign goal plans`; `submit.argument14=null`; `submit.argument15=null`; `submit.argument16` omitted value; `submit.argument17=verified Assign Goal Plans option flag`. Include display attributes only for the same semantic values. |
| `execution_options` | Approved wait/poll/timeout behavior for the dependent skill. |

Invoke the dependent skill only after the exact `request_payload` and separate
ESS approval are available. It submits once and returns request ID/status; the
Goal Plan flow persists sanitized assignment evidence and that result. If the
current Scheduler contract cannot be verified, return the assignment route as
blocked and do not manufacture a payload.

## Additional lifecycle, child-maintenance, validation, and verification examples

| Purpose | Method | Stable path | Guard and verification |
|---|---|---|---|
| Activate or inactivate a plan | PATCH or current validated update | `/goalPlans/{GoalPlanId}` | Status-only narrow delta after fresh plan/dependency read and separate approval; re-read the plan. |
| Remove a population child | DELETE | Fresh returned item link under `/goalPlans/{GoalPlanId}/child/{childCollection}` | Resolve one current child identity, submit once after approval, then re-read that collection. |
| Add/remove document association | POST ADF batch root | Relative `/goalPlans/{GoalPlanId}/child/associatedPerfDocumentTypes` path | Use current `DocumentTypeId` for add or returned `GoalPlanDocumentTypeId` for removal; include only the approved child delta and required parent batch part; re-read associations. |
| Delete a Goal Plan goal | DELETE | `/goalPlans/{GoalPlanId}/child/performanceGoals/{GoalId},{GoalPlanGoalId}` | Both returned IDs are required; never construct a GoalId-only path. Re-read plan goals after one delete. |
| Search/delete assignees | POST ADF action | `/goalPlanAssignees/action/findByAdvancedSearchQuery` or `/goalPlanAssignees/action/batchDelete` | Use fresh returned assignee IDs and the current advertised request schema; preview/approve deletion separately and re-read selected rows. |
| Validate dependencies | GET | `/reviewPeriodsLOV`, `/eligibilityProfilesLOV`, `/talentPerformanceDocumentTypes`, and worker routes | Resolve exact current IDs and active/date-compatible dependencies before a related mutation. |
| Verify a Goal Plan or child write | GET | `/goalPlans/{GoalPlanId}` plus affected fresh child link | Confirm only the approved delta changed; for batch goal writes, re-read the matching returned goal row. |
