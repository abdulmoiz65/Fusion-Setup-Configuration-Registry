# Goal Plan Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 0 | Parent Run Book execution control | Match the approved plan fingerprint and prove this is the earliest incomplete applicable task |
| 1 | Goal Plan kind | Resolve `regular` or `primary` and apply the matching dependency set |
| 2 | HR specialist person context | Before create, confirm current person information is complete enough for Goal Plan security and assigner attributes |
| 3 | Review Period | For a regular plan, resolve exactly one period and validate the date envelope; not applicable to Primary |
| 4 | Conditional design references | Resolve active Performance Document Types and code-backed values when used |
| 5 | Eligibility Profile | For a regular plan, resolve existing active Goals Management-compatible profiles when used and identify which are required |
| 6 | Existing worker assignments | For a regular plan, resolve exact active assignments and an explicit population scope for population or assignment |
| 7 | ESS contract | For a regular plan only, verify Assign Goal Plans definition and parameters before assignment handoff |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| GP.RUNBOOK_CONTROL | Parent Run Book execution control | Yes | Any Run Book task execution | Validate | `hcm.goal-management` controlled next-task resolver | resolve_controlled_next_task | Prevents direct entry into a later task | Complete or mark every earlier task Not Applicable and show the next-task preview | Approved plan fingerprint, exact task identity, sequence, execution-control fingerprint |
| GP.PERSON_CONTEXT | Current HR specialist person information | Conditional | Goal Plan create only when current create metadata requires person/assignment payload fields or authorization reports a context failure | Validate | Current worker/person read | current_user_person_context_lookup | Person data can govern Goal Plan security and assigner attributes | Complete missing person information through its owning GHR flow only when required; otherwise record unavailable context as a non-blocking diagnostic | Readiness only; do not persist identifiers |
| GP.REVIEW_PERIOD | Review Period | Conditional | Regular create, date update, activate, or assignment | Lookup | Review Period management read | review_period_lookup | Anchors regular-plan dates and cycle | Supply an exact existing period | ReviewPeriodId, dates, status |
| GP.PRIMARY | Existing Primary Goal Plan | Conditional | Primary create or activation | Lookup | Current `goalPlans` read | primary_goal_plan_lookup | Enforces a single active Primary plan | Resolve existing Primary state before create/activation | Identity, active status, technical dates |
| GP.ELPRO | Existing Goal Management Eligibility Profile; owning maintenance task BEN_MANAGE_ELIGIBILITY_PROFILES | Conditional | Regular-plan eligibility criteria are used | Lookup | Complete paginated `/hcmRestApi/resources/latest/eligibilityProfilesLOV` read, followed by authoritative stored-criteria verification when the source supplies semantic criteria rather than an exact profile name | eligibility_profile_lookup | Prevents invalid population without blocking existing-profile reads on an unavailable mutation provider | Resolve one exact active Goal Management-compatible profile internally; present multiple candidates for selection; maintain only a confirmed missing profile outside Goal Plans | Profile identity, business name, status, usage, match evidence, required flag |
| GP.DOC_TYPES | Performance Document Types | Conditional | Performance integration is requested | Lookup | Performance Management owning skill or current reference read | performance_document_type_lookup | Supports integrated documents | Resolve active types whose From Date is no later than plan start and To Date is no earlier than plan end | Type IDs, names, dates, status |
| GP.WORKERS | Existing person and active assignment | Conditional | Regular-plan population or assignment | Lookup | Current worker and assignment reads | worker_assignment_lookup | Separates worker identity from assignment and population reach | Supply synthetic non-production worker keys and one supported scope | Person and Assignment identity for runtime only; selected/direct/all scope |
| GP.ESS | Assign Goal Plans ESS definition and parameters | Conditional | Regular-plan prepare_assignment | Verify | Current Scheduler metadata or authoritative evidence | assign_goal_plans_job_lookup | Prevents invented job submission | Verify process type `Assign goal plans`, process name equal to the Goal Plan name, resolved effective date (supplied or defaulted to today at preview), exact job definition, and remaining parameters | Job definition, process type/name, effective date, remaining parameters, configured selector and execution approval |
| GP.ESS_PROFILE_OPTIONS | Worker Goal Setting multithread profile options | Conditional | Assignment throughput assessment or tuning is requested | Read/route | `core.fusion-api.apps-common` with the exact supplied `ProfileOptionName` | goal_plan_batch_profile_option_lookup | Explains actual child-process count without changing setup | Read current values; do not tune from this skill and do not change the two minimum-count defaults without authoritative direction | HRG_GP_MAX_THREADS, HRG_GP_MINCOUNT_EACHTHREAD, HRG_GP_MINCOUNT_LASTTHREAD |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Every operation-specific dependency is exact and current | Lookup yes; writes only after approval |
| External route | Worker or Eligibility Profile maintenance is needed | Lookup only in this skill |
| Blocked | Missing, inactive, ambiguous, or unverified dependency | Lookup only |

## Eligibility Profile Provider Readiness

`BEN_MANAGE_ELIGIBILITY_PROFILES` identifies the owning setup task, but a task
code alone is not an executable provider. Its availability is irrelevant to
the read-only resolution of an existing profile. Complete
`eligibility_profile_lookup` first. For profile creation or maintenance after
a confirmed zero match:

1. Discover a canonical provider skill for the task in the refreshed taxonomy
   structure.
2. If none is available, return `PROVIDER_SKILL_UNAVAILABLE` with the task code,
   required operation, and resume context. Do not invent a skill ID, copy an
   unrelated provider, or prepare a live mutation payload.
3. If a provider exists, route through its validation and explicit-approval
   controls.
4. Re-run `eligibility_profile_lookup` after the provider completes and require
   one active Goals Management-compatible profile before resuming Goal Plan.

Until Talent Management portal Step 2 has propagated from `main` through
integration and the product private branch to this feature preview,
provider-dependent maintenance remains blocked; read-only resolution of an
already existing profile remains supported.

## Assignment Batch Profile-Option Guidance

- `HRG_GP_MAX_THREADS` defaults to `4`. Values `0` or `1` create a
  single-threaded process. Values above `8` are reset by Fusion to the default
  `4`; this is a maximum, not a guaranteed child-process count.
- `HRG_GP_MINCOUNT_EACHTHREAD` defaults to `5000`, and
  `HRG_GP_MINCOUNT_LASTTHREAD` defaults to `1000`. InfoDev recommends not
  changing either default.
- Fusion determines the actual thread count from all three values. The parent
  remains paused until its child processes complete. Read or explain these
  values through the canonical profile-option provider when it exists; never
  create a hand-authored common task or change profile options here.

## HDL DAT Dependency Readiness

Before a Goal Plan HDL package can be previewed, obtain structured, timestamped
target-tenant evidence for the Review Period, each referenced worker and active
assignment, eligibility profile, organization, and the Goal Plan document type
when performance-document inclusion is enabled. `GoalPlan.dat` is required;
`GoalPlanTranslation.dat` and `Goal.dat` are optional. A child parent must
either occur earlier in the package or be listed in `existingParents` with
fresh target evidence. Missing mandatory data, an unresolved parent/reference,
or stale evidence is a non-waivable preflight blocker, not a reason to use FSM,
REST, or fabricate an ID after explicit HDL intent. Resolve the authenticated
requester and active primary assignment through the owning current-worker
adapter; do not ask the consultant for a requester Person Number. Resolve the
environment from core configuration and generate evidence/timestamps and the
change manifest internally. Apply only target-defined or semantically safe
defaults to a separate prepared copy and retain provenance for every addition.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_PLANS.DEPENDENCIES | step | 30 | resolve_dependency | ready->GOAL_PLANS.LOOKUPS;missing->GOAL_PLANS.BLOCKED | GOAL_PLANS.VALIDATE | stop | A Goal Plan write or assignment handoff is requested |
