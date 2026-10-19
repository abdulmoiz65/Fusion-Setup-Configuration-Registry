# Goal Plan Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve |
|---|---|---|---|
| Operation | requested_operation | Block | Select one supported route |
| Existing identity | GoalPlanId, immutable external ID, or exact disambiguated key | Block item get and mutations | Run exact Goal Plan lookup |
| Search definition | optional query filters, creation-time window, result limit | Use bounded unfiltered list | Normalize query and disclose returned window/limit |
| Regular create definition | name unique within an active Review Period, inactive status, and an idempotency identity; technical dates are either both explicit or both defaulted from that period | Block regular create | Resolve the exact active Review Period. Default both omitted technical dates from it; reject one supplied technical date or dates outside it. |
| Primary create definition | name, inactive status, `PrimaryGoalPlanFlag=true`, null Review Period, and metadata/template-derived technical dates | Block Primary create | Resolve current contract and existing Primary plan state |
| Population change | regular plan, explicit child operation, exact returned parent/child identity, and operation-specific worker/profile values | Block population | Included worker requires target PersonId, one active AssignmentId, normalized local CascadingLevel (default `"0"`), and current OpenAPI support for `perfGoalIncludedWorkers`; Eligibility Profile association requires a resolved active Goal Management-compatible profile and current OpenAPI support for `perfGoalEligibilityProfiles`; do not map ManagerAssignmentId or ESS intent |
| Assignment | final configured population selector, verified ESS contract, execution approval | Block ESS handoff | Resolve selector configuration and current job metadata |
| Goal Plan deletion assessment | exact plan, assignment count, status, and current delete capability | Block delete guidance | Delete only an unassigned plan and require a separate approval before any execution |
| Assignee deletion assessment | exact regular plan, exact assignees, impact count, and current Manage Assignees capability | Block removal guidance | Preview separately; do not confuse assignee deletion with population-child maintenance |
| Plan-goal functional change | regular plan, one add/duplicate/import/delete intent, exact source and target identities, and a verified current contract | Block plan-goal mutation | Delete requires fresh GoalId,GoalPlanGoalId; import requires exact target/source Goal Plan, Review Period, and target/source MassRequest identities; return unsupported for reorder |
| Plan-goal execution context | `object=goal_plan_template_goal`, one current create contract, and fresh plan/admin context. Use `goalPlans_performanceGoals_child_create` when Goal Plans metadata advertises its child POST; otherwise use `performanceGoalsV2_batch` only with a fresh resolved batch root. | Block plan-goal mutation | Reject inherited `libraryGoals` path/key, Library Goal string Weighting, `PerfCategoryCode`, Library Goal DFF parts, or Library Goal concurrency headers; resolve the Goal Plan contract afresh. |
| Document association change | exact Goal Plan, fresh available-type and association reads, active compatible add type or returned remove identity, and resolved ADF batch root | Block document mutation | Resolve the current child collection and build only a parent-coupled delta batch before preview |
| Assignee removal | fresh exact GoalPlanAssignmentId list, bounded impact, verified `batchDelete` capability, and the action's `goalPlanId=-1` scope sentinel | Block assignee mutation | Search/fetch assignees first, preview exact IDs, then map only those IDs into goalPlanAssignmentIdList |
| Performance-document sync | verified `essProcessTrigger` action; pending current and fetched prior plan state; RequestStatus; Redwood flag; assignee count; document-type change state; and approval for the associated update | Block sync | Derive the runtime action params from the supplied server predicate before the main Goal Plan batch update |

## Dependency-Aware Validation

| Applies When | Result | Next Action |
|---|---|---|
| Goal Plan dates fall outside Review Period dates | Invalid | Correct dates or select another period |
| Goal Plan name duplicates another plan in the same Review Period | Invalid | Choose a name unique within that Review Period |
| Current HR specialist person information is incomplete | Diagnostic unless the current create metadata requires a person/assignment field or current authorization reports an error | Resolve through the owning person-information flow when it is required; do not block a direct scalar create that has no person/assignment payload dependency |
| Primary plan has a Review Period, worker, Eligibility Profile, or goal child | Invalid | Remove the inapplicable field/child request |
| Another Primary Goal Plan is active and activation is requested | Blocked | Inactivate the existing Primary plan in a separate approved operation |
| Exact Eligibility Profile business name has one active Goal Management-compatible match across all LOV pages | Valid | Resolve its ID internally and continue; do not ask the consultant for an ID or require the maintenance provider |
| Exact Eligibility Profile business name has multiple active Goal Management-compatible matches | Needs selection | List business-facing candidate details and request selection; never select the first row |
| Semantic population criteria have exactly one authoritatively verified profile-criteria match | Valid | Resolve that profile internally and continue |
| Semantic population criteria cannot be verified from the LOV or an authoritative criteria-read capability | Needs selection | List relevant active Goal Management-compatible candidates for confirmation; do not infer from profile-name similarity |
| Eligibility Profile has no active Goal Management-compatible match after complete discovery | Blocked | Route creation or maintenance through the owning setup object only when that operation is required |
| Eligibility Profile association targets `perfGoalEligibilityProfiles` for a Goal Plan | Valid when profile resolution and child create metadata are current | Build the payload with resolved `EligibilityProfileId`, derived `RequiredFlag`, and skill-derived `TalentObjectType="GOAL"` |
| Eligibility Profile association is for Check-In, Performance Management, or another product area | Blocked unless its own contract is verified | Do not reuse Goal Plan `TalentObjectType="GOAL"` outside `perfGoalEligibilityProfiles` |
| Worker identity exists but no unique active assignment exists | Blocked | Disambiguate assignment and effective date |
| Included-worker create lacks PersonId or active AssignmentId | Invalid | Resolve the target worker and effective assignment; normalize absent CascadingLevel to `"0"` |
| Included-worker CascadingLevel is outside the local allowed strings | Invalid | Return the value/meaning list in `ora_defaulting_rules.md`; do not call or infer a CascadingLevel LOV |
| Included-worker CascadingLevel label is ambiguous (`All`) or unsupported | Invalid | Ask the consultant for one valid code and return the complete value/meaning list in `ora_defaulting_rules.md`; do not infer a code |
| Included-worker requests a non-Self scope without advertised worker hierarchy evidence | Blocked | Keep default `"0"` executable; obtain current verified hierarchy evidence before accepting the requested non-Self scope |
| Included-worker create includes ManagerAssignmentId | Invalid | Remove it. That field belongs only to `goalPlanAssignees` search filtering |
| Included-worker public child is not exposed by current tenant OpenAPI | Blocked | Do not substitute ESS, an inferred ADF alias, or an undocumented child route |
| Worker creation is requested | Out of scope | Route to GHR/HDL using synthetic non-production data |
| Requested values match fresh state | No change | Return NO_CHANGE without mutation |
| Goal Plan is pending approval | Blocked | Wait for approval completion; proposed goal/plan changes are not final yet |
| Review Period change is requested while assignees remain | Blocked | Delete all assignees in a separate approved Manage Assignees operation, then re-read and retry |
| Goal Plan delete is requested while assigned | Blocked | Preserve the plan and use active/inactive status management |
| A plan-goal duplicate/import/delete request targets Primary | Invalid | Reject it; Primary plans cannot contain plan goals |
| Plan-goal reorder is requested | Unsupported | Return `UNSUPPORTED_UI_BEHAVIOR`; VBCS does not persist reorder, so no REST mutation exists to preview |
| A plan-goal delete identity is absent, stale, or does not match the selected plan | Invalid | Re-read `performanceGoals`; require one returned GoalId,GoalPlanGoalId composite item identity |
| Goal Plan import has an ambiguous Review Period, target/source plan, or MassRequest identity | Blocked | Resolve the current WorkerAssignmentId, then re-resolve the Review Period and source/target plans by exact name before preview |
| Assignee search has no resolved GoalPlanId | Invalid | Resolve one exact Goal Plan by returned ID or exact business identity before the read-only action; Manager and Organization are optional narrowing filters, not substitutes for the plan context |
| Assignee-search manager PersonId resolves to zero or many active assignments | Invalid | Ask for an exact active manager assignment; do not send the PersonId as ManagerAssignmentId or infer a manager from a display name |
| Assignee-search OrganizationId is absent | Valid | Omit the OrganizationId filter and list/count assignees for the resolved Goal Plan, optionally narrowed only by a resolved manager assignment |
| Assignee removal includes an ID not returned by the fresh selected search | Invalid | Remove the unverified ID and re-preview; never derive an ID from display values |
| Assignee batch delete result is not `0` or is absent | Blocked | Re-read all selected IDs, retain sanitized diagnostics, and stop without replaying the action |
| A performance-document sync request has no validated, approved Goal Plan update | Blocked | Re-read current/prior state and obtain approval for the associated update before preparing the pre-batch action |
| Performance-document sync predicate is not satisfied | No change | Do not submit an ESS job; record the evaluated flags and return the action's valid empty result |
| A document association add repeats a fresh associated DocumentTypeId | Invalid | Remove the duplicate request; do not send a create part |
| A document association removal does not match a fresh returned GoalPlanDocumentTypeId | Invalid | Re-read the association collection and disambiguate; do not infer a child key |
| A worker is already in the opposite include/exclude collection | Invalid | Reject the child mutation unless current server metadata explicitly permits the overlap; never silently move or duplicate the worker |
| A child collection batch reports mixed success | Blocked | Re-read the parent and every affected child, report any orphan or partial state, and require an explicit remediation plan before another mutation |
| `created_within_days=N` is supplied | Valid read filter | Resolve `now-N days` through `now` in UTC, page candidates, hydrate missing `CreationDate`, and sort newest first |

## Field Validation

Resolve Basic Details requirements through
the offering-owned Goal Setup Field Resolution support package at
`pillars/hcm/goal-management/goal-management-common/goal-setup-field-resolution/README.md`. A value for a
dropdown or LOV is valid only when one current returned value matches it. A
missing optional field is not a blocker; disclose an advertised default instead.
Business-purpose text is not population evidence.

| Check | What Happens |
|---|---|
| External ID | Require a supplied immutable external ID for automated create only when current metadata has no usable server default expression. When current `GoalPlanExternalId` metadata has `hasDefaultValueExpression=true` and `GoalPlanId` has a server default expression, omit both IDs from the create payload, disclose that Fusion derives the external ID from the generated Goal Plan ID, and use exact Goal Plan name plus associated Review Period duplicate controls before approval. Dates remain create-validation fields, not duplicate-key fields. Never fabricate or silently substitute an ID client-side. The returned generated ID/external ID becomes the immutable post-create identity. |
| Create payload contract | Before preview, extract the exact writable create-field names from the current `goalPlans/describe` response and pass them to `scripts/goal_plan_payload.py:build_goal_plan_create_payload`. Reject any unsupported field locally; in particular, map role access only to the current `GoalAccessLevelCode` field, never `GoalAccessLevel`. |
| Maximum create sequence | Use `build_goal_plan_create_execution_plan`. No enforcement intent produces one create payload with the explicit maximum and no enforcement field. Explicit enforcement produces one approval-bound sequence: create with maximum and no enforcement field, verify the maximum, patch only enforcement, then verify both. A direct create payload containing `EnforceMaximumGoalsInGpFlag=true` is invalid. |
| Minimum create contract | Materialize `PrimaryGoalPlanFlag`, inactive `GoalPlanActiveCode=I`, `StartDate`, and `EndDate`; require `ReviewPeriodId` for a regular plan. Bind approval to environment, operation, request path, identity, and exact steps. Post-create verification must compare every approved create field, not status alone. |
| Primary technical dates | Required by the public create schema but sourced from current metadata or an approved template; never use captured tenant constants |
| Regular technical dates | Resolve the exact active Review Period first. When both `StartDate` and `EndDate` are omitted, default them from its inclusive date range. Preserve a complete explicit pair and validate it is inside the period; reject a partial pair. |
| Goal-setting controls | Explain that post-end restrictions apply to workers only and are cumulative with role access. Resolve this block before generic access/evaluation lookup discovery. Validate an ordered complete date pair within the Goal Plan range; distinguish the post-end add restriction from edit/cancel/delete. If either date is absent, show the corresponding Goal Plan boundary as a proposed value and require confirmation. Do not evaluate `CanDelHRGoal` for date-bound Goal Setting Info phrases. |
| Goal count and weights | A Goal Plan count applies to its performance goals; never ask whether it includes development goals. Minimum cannot exceed maximum. Omit nullable `EnforceMaximumGoalsInGpFlag` unless the source explicitly requests restriction; preserve raw `null` rather than converting it to `false`. Explicit enforcement requires a maximum already persisted before the enforcement PATCH. For create, include the maximum while omitting enforcement, verify it, then patch only enforcement. Count existing managed goals plus proposed/imported goals before enabling enforcement and reject an over-limit result; enforced weight total requires weighting and a 100-percent plan total. |
| Plan goals | Reject on Primary. For regular plans, require goal dates inside plan dates. When adding a selected Performance Library Goal and both dates are omitted, default Start Date and Target Completion Date from the existing Goal Plan; reject a partial pair. Advertise conditional sections only when enabled. |
| Eligibility Profiles | Page all `eligibilityProfilesLOV` rows and retain active participant profiles with Goal Management usage. Resolve an exact supplied business name case-insensitively when it has one match. For semantic criteria, resolve only from authoritative stored-criteria evidence; otherwise present candidates. Keep IDs internal, and do not test mutation-provider availability unless a confirmed missing profile must be created or maintained. For Goal Plan `perfGoalEligibilityProfiles`, derive `TalentObjectType="GOAL"` inside the skill. Derive `RequiredFlag=true` only when the functional requirement explicitly says the profile is required, mandatory, or must be enforced; otherwise default it to `false`. For multiple profiles, apply AND semantics across every profile marked required |
| Assignee scope | Allow only selected employee, direct reports, all reports, selected plus direct reports, or selected plus all reports; process exclusions separately |
| Performance Document Types | Resolve only when the integrated use case requires them; require Active status, From Date no later than plan start, and To Date no earlier than plan end. Reject duplicate, inaccessible, or incompatible associations; add only DocumentTypeId, remove only a returned GoalPlanDocumentTypeId, and use one parent-coupled ADF batch. No generic association edit is supported |
| MASS_REQ context | Only for an existing-plan template-goal operation, resolve the logged-in HR/admin PersonId and AssignmentId from the authenticated session; never treat them as assignee values. A basic Goal Plan create omits these fields and does not block on their resolution unless current create metadata explicitly requires them. |
| Template-goal MassRequestId | Only an existing regular Goal Plan may supply it. Re-read that exact plan immediately before the selected child-create or batch create; reject missing/stale value. New Goal Plan creates omit it entirely |
| Admin assignment context | For an operation that requires caller context, resolve the authenticated caller through the owning current-worker adapter and use its confirmed active primary assignment only. Validate status against current tenant status semantics when available. Do not use a browser display name, `ManagerAssignmentId`, a selected worker assignment, or a cached context. Do not perform this lookup as a prerequisite to a basic Goal Plan create unless current metadata requires caller fields. |
| ESS impact | Validate configured selector and execution approval; ESS determines eligibility at runtime |
| ESS process fields | Require process type `Assign goal plans`, process name equal to one fresh active regular Goal Plan name, a nonblank MassRequestId, Goal Plan Start Date, Goal Plan End Date, resolved effective date (supplied or defaulted to today at preview), configured population selector, and the verified Manage Goal Scheduled Process Scheduler contract |
| Plan goals | Add/duplicate through the current Goal Plans child-create contract when advertised; otherwise use a verified `performanceGoalsV2` batch fallback. Its `Weighting` is numeric and must not be mapped from the Performance Library Goal string schema. Delete only through the fresh `performanceGoals/{GoalId},{GoalPlanGoalId}` returned item path. Import only through `importGoals` with targetMassRequestId, massRequestId, goalPlanId, and reviewPeriodId mapped from fresh returned rows; re-read target goals after a null result. Reorder is unsupported because VBCS does not persist it |
| Plan-goal context switch | Treat every Goal Plan goal request as a new context bind, even after another Goal Management object was handled in the same consultant conversation. Resolve the current child-create contract first; resolve `performanceGoalsV2`, numeric Weighting semantics, and a batch root only if the selected operation falls back to batch. Always obtain fresh Goal Plan/MassRequestId and current HR-admin context before preview. |
| Assignees | Search through the read-only ADF action with GoalPlanId `terms`; append optional OrganizationId `terms`; and append ManagerAssignmentId in its advertised `value` form only after resolving a supplied manager PersonId to one current active assignment. Read `result.items` and string pagination/count in `result.summary`. Batch removal sends `goalPlanId=-1` and only fresh returned GoalPlanAssignmentId values in goalPlanAssignmentIdList. Result `0` requires re-read verification; never submit an ESS assignment |
| Performance-document sync | Invoke only `goalPlans/action/essProcessTrigger` before the main Goal Plan batch update of the approved save. Set mode to EDIT_GOAL_PLAN; require pdRedwoodEnabled=Y, disablePD=N, AssigneeCount greater than zero, and at least one trigger: DocTypesChangedFlag=Y; or active plan with GoalPlanActiveFlagChanged=Y; or non-null EvaluationType, ReviewPeriodId, or EnableWeightingFlag with its corresponding changed flag=Y. Generate all params from pending current and fetched prior state, pass the result to the batch-payload builder, and never copy a UI capture |
| Goal Plan read projection | Use `findByAdvancedSearchQuery` only with its verified display projection: GoalPlanId, GoalPlanName, ReviewPeriodId, ReviewPeriodName, and LastUpdateDate. Do not request `GoalPlanActiveCode` from that action. For status, dates, Review Period filtering, or configuration fields, use GET `goalPlans` with a supported `q` predicate and resource `fields`, then hydrate the item when needed |
| Read pagination | Follow returned offset/hasMore semantics until complete or the disclosed limit is reached |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_PLANS.VALIDATE | decision | 20 | validate_input | read_item->GOAL_PLANS.READ;read_search->GOAL_PLANS.SEARCH;assignee_search->GOAL_PLANS.ASSIGNEE_SEARCH;csv->GOAL_PLANS.CSV_READY;hdl->GOAL_PLANS.HDL_VALIDATE;worker_create->GOAL_PLANS.WORKER_ROUTE;continue->GOAL_PLANS.DEPENDENCIES;invalid->GOAL_PLANS.BLOCKED | GOAL_PLANS.INTAKE | stop | Intake is complete and one operation is selected |
| GOAL_PLANS.HDL_VALIDATE | step | 21 | validate_input | passed->GOAL_PLANS.HDL_READY;invalid->GOAL_PLANS.BLOCKED | GOAL_PLANS.VALIDATE | stop | A DAT/ZIP source and explicit HDL intent both exist |
| GOAL_PLANS.WRITE_ROUTE | decision | 95 | evaluate_result | create->GOAL_PLANS.CREATE_PREVIEW;update->GOAL_PLANS.UPDATE_PREVIEW;activate->GOAL_PLANS.ACTIVATE_PREVIEW;inactivate->GOAL_PLANS.INACTIVATE_PREVIEW;include_worker->GOAL_PLANS.INCLUDE_WORKER_PREVIEW;exclude_worker->GOAL_PLANS.EXCLUDE_WORKER_PREVIEW;associate_profile->GOAL_PLANS.ASSOCIATE_PROFILE_PREVIEW;remove_population->GOAL_PLANS.REMOVE_POPULATION_PREVIEW;functional_change->GOAL_PLANS.FUNCTIONAL_PREVIEW;no_change->GOAL_PLANS.NO_CHANGE;unsupported->GOAL_PLANS.BLOCKED | GOAL_PLANS.REST_PAYLOAD | stop | A mapped Goal Plan or regular-plan population write contract exists |

## HDL DAT Preflight

Run this preflight only when a DAT/ZIP source and explicit HDL intent both
exist. Require `GoalPlan.dat`; treat `GoalPlanTranslation.dat` and `Goal.dat`
as optional. Accept parent-only input and supported `GoalPlan.dat` children:
`GoalPlanDocTypes`, `MassRequest`, `MassRequestAssignment`,
`EligibilityProfileObject`, `MassRequestHierarchy`, `MassRequestExemption`,
`GoalPlanAssignment`, and `GoalPlanGoal`. Validate archive integrity and flat
shape, UTF-8 text, `METADATA`, field counts, template-derived mandatory data,
supported source or user keys, duplicate scoped identities, and operation
agreement. Every child must resolve to an earlier package parent or an exact
target parent. `GoalPlanGoal` and `GoalPlanAssignment` DELETE rows must precede
the parent DELETE. `IncludeInPerfdocFlag=Y` requires a supplied
`GoalPlanDocTypes` component and exact target document-type evidence.

The consultant supplies only the DAT/ZIP and business intent. Resolve the
configured environment, template requirements, target references,
authenticated requester, timestamps, and operation classification internally.
Create a separate prepared copy and record every injected value and its source.
For a parent-only Goal Plan, derive requester Person Number and submission date.
For an explicit Mass Request, derive the requester on `MassRequest` and do not
also add it to `GoalPlan`. Derive `AssignedByPersonNumber` for a supplied
template Goal. Do not overwrite supplied values or guess unresolved business
choices.

For every `MERGE`, the internally generated change manifest must classify the row as an approved
`create` or `update` from a fresh exact target identity lookup; do not infer it
from the verb. A `DELETE` requires a separate approved delete scope and exact
identity. Reject omitted, duplicate, or unresolved identities, unapproved
operation outcomes, and any target-evidence gap as non-waivable errors.


---

# Goal Plan Input Intake

## Accepted Input Formats

| Input Format | What Must Be Provided | Applies To |
|---|---|---|
| Guided request | One operation, environment, and exact Goal Plan identity or create values | One Goal Plan |
| Structured object | Business fields, dependency keys, and operation-specific intent | REST planning or preview |
| Population table | Exact existing-worker selectors and inclusion/exclusion intent | Population planning |
| FSM task ZIP | Task-level export/import ZIP and explicit CSV operation | CSV export or import |
| HDL DAT/ZIP | Supplied `.dat` or flat `.zip` and explicit HDL intent; audit context is resolved internally | `core.data-loader` only after error-free prepared-copy preflight |

## Dependency Inputs

| Field | Mandatory | Purpose | Send in Request Body? | Lookup Rule |
|---|---|---|---|---|
| requested_operation | Yes | Select get, list/search, create, update, activate, inactivate, maintain_population, manage_plan_goal, maintain_document_association, manage_assignees, sync_performance_documents, assess_plan_delete, assess_assignee_delete, prepare_assignment, csv_export, or csv_import | No | Normalize show/fetch to get and find/list to search; delete assessments never imply execution |
| goal_plan_kind | Conditional | Distinguish regular from Primary Goal Plan behavior | `PrimaryGoalPlanFlag` only on create/update payloads | Required for create and kind-sensitive mutations; optional as a read filter; never infer from name for writes |
| query_filters | Optional | Filter a read by name, status, kind, Review Period, dates, creator, or current searchable fields | Search action body only | Reject unsupported fields rather than ignore them |
| created_from, created_to, or created_within_days | Optional | Filter list/search results by `CreationDate` | Search fields or local hydrated filter | Resolve one exact half-open UTC interval and return it |
| result_limit | Optional | Bound returned records | Search pagination | Positive integer; disclose default, truncation, and page completion |
| population_change_kind | Conditional | Select include worker, exclude worker, associate Eligibility Profile, or remove a returned child row | No | Required only for regular-plan `maintain_population` |
| goal_plan_identity or external_id | Conditional | Resolve one target and enforce idempotency | Send a supplied external ID only when provided. When current metadata exposes server default expressions for both `GoalPlanId` and `GoalPlanExternalId`, omit both from create and disclose the server-derived external-ID behavior in the approval preview. | Exact match; never fuzzy-match writes |
| review_period_identity | Conditional | Resolve the required Review Period for a regular plan | Use resolved ID for regular plans; send null for Primary plans | Exact active period whose dates contain a regular plan |
| design controls | Conditional | Define access, goal-setting period, evaluation, HR-assigned-goal handling, weights, and counts | Only map fields advertised as writable by current metadata | Validate interdependent controls before activation |
| plan goal definitions | Optional | Add or import regular-plan goals | Only through current advertised plan-goal capability | For a template goal on an existing regular plan, re-read that exact plan to obtain `MassRequestId`; never require or send it for new-plan create. Dates must fit plan; conditional sections require enabled capabilities; never use on Primary |
| plan-goal operation | Conditional | Add, duplicate-from-source, import, delete, or request reorder for one regular-plan goal | Add through the current advertised child POST, or its verified batch fallback; update through its current item/batch contract; delete through returned `performanceGoals` item identity; import through `importGoals`; reorder has no supported action | Resolve source/target goal identities and MassRequest IDs. Delete requires the returned GoalId,GoalPlanGoalId composite key; import requires target/source plan and Review Period identities; reject reorder because VBCS itself does not persist it |
| execution context | Mandatory for a plan-goal mutation | Exact object and operation being changed | No | Bind `goal_plan_template_goal` plus the resolver-selected create contract before generating any payload. Invalidate inherited Library Goal path/key, field types, DFF parts, and concurrency headers. Resolve a batch root only when the selected fallback requires it, then resolve current plan/admin state. |
| document association operation | Conditional | Add or remove one Performance Document Type association | One approved ADF batch child delta plus its parent update part | Add requires an exact active compatible DocumentTypeId; remove requires the returned GoalPlanDocumentTypeId; a change is a delta add/remove, never a standalone association edit |
| assignee operation | Conditional | Search/fetch assignees or remove selected returned assignee IDs | Verified ADF search or batch-delete action only | Search requires a resolved GoalPlanId. Manager PersonId and department/OrganizationId are independent optional filters; resolve a supplied manager PersonId to one current assignment before mapping the advertised ManagerAssignmentId filter. Removal requires fresh GoalPlanAssignmentId values only. |
| assignee_search_manager_person_id | Optional | Narrow an assignee read to one manager selected by the consultant | Never sent verbatim | Resolve the exact PersonId to one current active manager assignment. If zero/many assignments result, stop and request disambiguation. |
| assignee_search_organization_id | Optional | Narrow an assignee read to the selected Department/Organization UI value | `OrganizationId` filter only | Use only an explicit or current UI-resolved OrganizationId; never infer it from a department display name. |
| performance-document sync intent | Conditional | Trigger guarded pre-batch synchronization with matching performance documents during a Goal Plan update | `params` for the verified action only | Require the pending current and fetched prior Goal Plan values, RequestStatus, Redwood flag, assignee count, and document-type change state |
| eligibility_profile_identity | Conditional | Resolve an existing active Eligibility Profile | Only when current Goal Plan contract requires it | Resolve task BEN_MANAGE_ELIGIBILITY_PROFILES; do not create here |
| worker criteria and assignee scope | Conditional | Maintain a regular-plan population or preview assignment | Only in the applicable returned child collection | Included-worker create requires target `PersonId` and active `AssignmentId`. Normalize omitted `CascadingLevel` to local string `"0"`; validate an explicit value against `ora_defaulting_rules.md`. `ManagerAssignmentId` is only an assignee-search filter, never population input. |
| actual assignee count | Post-execution | Report ESS outcome | No | Never a prerequisite for assignment approval |
| approvals | Conditional | Bind one consequential operation | No | Independent REST, activation, population, ESS, and import approvals |

## Body Field Rules

| Situation | What Happens |
|---|---|
| Regular create is selected | Default inactive and no assignment; require Review Period and dates; create does not imply activation or population |
| Primary create is selected | Set `PrimaryGoalPlanFlag=true`, `ReviewPeriodId=null`, omit worker/profile/goal children, and use metadata/template-derived technical dates |
| Primary defaults are accepted | Enable weighting and leave 100-percent enforcement disabled; preserve explicit supported overrides |
| Update is selected | Preserve omitted values and collections |
| Primary update is selected | Preserve `ReviewPeriodId=null`, technical dates, and omitted values; reject worker/profile/goal child changes |
| Population is selected | Treat inclusion/exclusion save as distinct from ESS assignment |
| Included worker is selected | Use the documented `perfGoalIncludedWorkers` child only when current tenant OpenAPI advertises it; send target PersonId, active AssignmentId, and normalized local CascadingLevel (default `"0"`), then re-read included workers. Never submit ESS or ManagerAssignmentId implicitly. |
| CascadingLevel wording is ambiguous or unsupported | Stop before payload generation; return `0 = Self`, `1 = Direct reports`, `2 = Self and direct reports`, `999999 = All reports`, and `1000000 = Self and all reports`; request one valid code. |
| A test worker does not exist | Route to GHR/HDL; do not create a worker in this skill |
| Primary population or ESS is requested | Reject as not applicable; an active Primary plan is global to active Review Periods |
| ESS definition or parameters are unverified | Mark current_metadata_required and stop before ESS preview or submission. For Assign Goal Plans, use only the verified Manage Goal Scheduled Process contract and do not substitute another Goal Management scheduled process |
| Search transport uses POST | Treat it as a safe read-only action, not as mutation approval |
| Delete Goal Plan is requested | Read assignment/usage state first. Assigned plans cannot be deleted; return guided UI or metadata-gated execution only for an unassigned plan |
| Delete assignees is requested | Treat removal as a consequential, separately approved Manage Assignees operation; it is not population-child removal and never runs through ESS |
| Review Period change is requested | Allow only when no assignees remain; otherwise require separately approved assignee deletion first |
| Plan-goal duplicate is selected | Treat it as a source-goal read plus separately approved current child-create contract; no generic duplicate endpoint is permitted |
| Plan-goal delete is selected | Re-read the target plan's `performanceGoals` collection and use only the returned GoalId,GoalPlanGoalId composite item identity. Submit one approved DELETE, then re-read the collection; no batch payload or inferred GoalId-only path is permitted |
| Plan-goal import is selected | Resolve the current user's WorkerAssignmentId, then resolve the selected Review Period and source Goal Plan by exact names. Map targetMassRequestId, source massRequestId, target goalPlanId, and reviewPeriodId from fresh returned rows; a null action result is a completed synchronous result and requires target-goal re-read verification |
| Plan-goal reorder is selected | Return `UNSUPPORTED_UI_BEHAVIOR`: the VBCS UI does not persist reordering. Do not search for or infer a REST persistence contract |
| Assignee search is selected | Use a read-only ADF action body with empty query and GoalPlanId in `terms`. Append OrganizationId in `terms` only when the Department/Organization filter is selected. When a manager PersonId is supplied, resolve one current manager assignment and append ManagerAssignmentId in its advertised `value` form. Neither optional filter is required. Use the verified display/search fields and bounded offset/limit; read rows from `result.items` and pagination/count from `result.summary`. |
| Assignee deletion is selected | Search and preview exact GoalPlanAssignmentId values; map them as goalPlanAssignmentIdList and use the action's verified `goalPlanId=-1` scope sentinel. Treat result `0` as successful action completion, re-read each selected ID, and do not confuse this with population-child removal or ESS assignment |
| Document association is selected | Re-read available document types and the plan association collection. Map every add with only DocumentTypeId and every removal with only the returned GoalPlanDocumentTypeId; combine relative child parts and the parent Goal Plan update in one approved ADF batch, never a standalone association edit |
| Performance-document sync is selected | Run only as the guarded pre-batch action for the approved Goal Plan update. Build `params` from pending current and fetched prior state, pass the result into main batch payload construction, then invoke the main Goal Plan batch update; an empty action result is a valid no-sync outcome, not an error |
| Goal Plan is pending approval | Block update and explain that proposed goal/plan changes are not final until approval completes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_PLANS.INTAKE | step | 10 | validate_input | complete->GOAL_PLANS.VALIDATE;missing->GOAL_PLANS.BLOCKED | none | stop | Every Goal Plan request |


---

# Goal Plan Bulk Intake

## Accepted Bulk Inputs

| Input Format | What Must Be Provided | How Rows Are Processed |
|---|---|---|
| FSM task ZIP | Unmodified task-level ZIP for explicit export/import | Validate through shared task-level setup skills |
| Population table | Regular-plan key, one child operation, synthetic worker/profile key, effective date when applicable | Resolve and preview every row; no implicit ESS submission |
| Goal Plan table | Plan kind, one operation per row, and idempotency key when automated | Search/diff and approve each mutation route |

## Column Guidance

| Column Type | Allowed Fields | What Happens |
|---|---|---|
| Identity | External ID, exact Goal Plan key, exact synthetic worker key | Reject duplicates and ambiguity |
| Population | Include worker, exclude worker, associate profile with required flag, explicit selected/direct/all-report scope, or remove returned child identity | Route to one exact Goal Plan child collection and separate save from assignment; never flatten hierarchy scope silently |
| Primary | Name, Primary flag, status, metadata/template-derived technical dates | Reject Review Period, worker, profile, goal, and ESS columns |
| Design | Goal-setting controls, access/evaluation, weights, min/max counts, compatible document types, and regular-plan goal definitions | Validate interdependent values and enabled capabilities; reject plan-goal rows for Primary |
| Impact | Fresh configured-selector evidence, execution approval reference and environment/plan/date binding | Required by validate_assignment_impact before ESS payload handoff; no pre-submission employee count or list is required |
| Sensitive | Credentials, cookies, production worker data | Reject and do not persist |

## Preview and Execution Rules

| Gate | Requirement |
|---|---|
| Population | Show adds, removals, unchanged rows, invalid rows, and total impact |
| ESS | Show final selector, exact job contract, and execution approval |
| Import | Validate ZIP and obtain separate import approval |
| Partial failure | Preserve sanitized errors, re-read the parent and every affected child to detect orphan or partially-applied rows, and do not automatically retry uncertain writes |
