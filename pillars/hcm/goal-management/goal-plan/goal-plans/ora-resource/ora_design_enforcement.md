# Goal Plan Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Select one operation | No combined create, activation, population, or assignment |
| 2 | Resolve kind and dependencies | Regular/Primary kind and its period, profile/types, worker, or ESS dependencies are exact |
| 3 | Validate inactive-first and impact | Operation-specific safety rules pass |
| 4 | Bind approval | Final target, dependency state, environment, payload or ESS parameters, and fingerprint are fixed |

## Design Rules

Goal Plans contain performance goals. Source language that states a maximum
performance-goal count maps to `MaximumGoalsNumberInGoalPlan`; do not introduce
an all-goal-types question. Resolve the separate nullable enforcement control
only from explicit restrictive or no-enforcement intent. Omitted enforcement
remains omitted/`null`, never default `false`. When enforcement is explicit,
the maximum must be persisted and verified before the enforcement-only PATCH;
the two writes may share one immutable approval plan bound to the exact stable
business key and ordered payloads. Goal
Setting Info restrictions apply to workers only and remain independent of
`GoalAccessLevelCode`: explicit add and edit/cancel/delete language maps to
both controls, while a non-specific restriction requires consultant selection.
Any missing Goal Setting date is a review-only proposal of the corresponding
Goal Plan boundary and requires confirmation.
Evaluate Goal Setting Info before generic access, evaluation, or HR-assigned
goal action lookup discovery. `CanDelHRGoal` is not a candidate field for
date-bound post-goal-setting-period add/edit/cancel/delete restrictions.

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| GP.DATE.ENVELOPE | Create, update dates, or activate | Blocker | review_period_lookup | Goal Plan dates exceed Review Period | Correct dates or select another period | Yes |
| GP.REGULAR.DATE.DEFAULT | Regular create | Blocker | review_period_lookup | No exact active Review Period, one technical date is supplied, or derived/explicit dates exceed the period | Resolve the period, default both omitted dates from it, or provide a complete in-range pair | Yes |
| GP.NAME.UNIQUE | Regular create or name/period update | Blocker | goal_plan_search | The exact Goal Plan name already exists in the same associated Review Period (`HRG-3120299`); dates do not distinguish it | Choose a unique name for that Review Period or select another Review Period | Yes |
| GP.PERSON.CONTEXT | Template-goal create/update, or a Goal Plan create whose current metadata explicitly requires caller person/assignment fields | Blocker | current_user_person_context_lookup | Required caller context cannot be resolved from the authenticated Fusion session | Complete the owning person-information flow or access setup; never ask the consultant for IDs | Yes |
| GP.PRIMARY.SHAPE | Primary create or update | Blocker | primary_goal_plan_lookup | Review Period, worker, profile, goal, or ESS data is present | Remove regular-plan-only data | Yes |
| GP.PRIMARY.UNIQUE | Primary activation | Blocker | primary_goal_plan_lookup | Another Primary Goal Plan is active | Inactivate the existing Primary plan separately | Yes |
| GP.PRIMARY.DATES | Primary create or date update | Blocker | primary_goal_plan_lookup | Technical dates are copied from a capture or invented | Use current metadata/approved template; preserve on update | Yes |
| GP.PRIMARY.DEFAULTS | Primary create | Error |  | Weighting/enforced-total defaults are missing or contradictory | Default weighting on and 100-percent enforcement off unless explicitly overridden | Yes |
| GP.MAXIMUM.SEMANTICS | Create or update with maximum count | Blocker |  | Count is treated as spanning development/other goal types, enforcement is inferred from count alone, or returned null is converted to false | Treat the count as performance goals in this Goal Plan; preserve nullable enforcement unless intent is explicit | Yes |
| GP.MAXIMUM.PERSISTED | Create or update with explicit maximum enforcement | Blocker | goal_plan_lookup | The approved plan attempts to send enforcement before a fresh read verifies the requested maximum is persisted | Create/update the maximum without enforcement, verify it, then patch enforcement only under the same exact conditional approval plan | Yes |
| GP.PLAN_GOAL.SHAPE | Regular plan goal add/import | Blocker |  | Goal date is outside plan, a partial date pair is supplied, capability is disabled, or target is Primary | For a selected Library Goal, default both omitted dates from the plan; otherwise correct dates/capabilities or remove Primary plan-goal request | Yes |
| GP.ELPRO.ACTIVE | Regular-plan eligibility is used | Blocker | eligibility_profile_lookup | Profile is missing, inactive, ambiguous, or incompatible with Goals Management | Resolve through owning setup task | Yes |
| GP.ELPRO.RESOLUTION | Regular-plan eligibility is used | Blocker | eligibility_profile_lookup | Existing-profile discovery is incomplete, an exact name has multiple matches, semantic criteria are inferred from a name, an ID is requested before name resolution, or provider availability is checked before a confirmed zero match | Read every LOV page; resolve one exact or authoritatively verified match internally; otherwise present candidates or route confirmed missing-profile maintenance | Yes |
| GP.ELPRO.REQUIRED | Multiple Eligibility Profiles | Blocker | eligibility_profile_lookup | Required flags are missing or worker fails any required profile | Mark required profiles explicitly and apply AND semantics | Yes |
| GP.DOC.TYPE.RANGE | Performance integration is used | Blocker | performance_document_type_lookup | Type is inactive or does not cover plan dates | Select a compatible active type | Yes |
| GP.WORKER.EXISTING | Explicit included-worker maintenance | Blocker | worker_assignment_lookup | Unique active assignment is absent | Route worker creation to GHR/HDL or disambiguate | Yes |
| GP.INCLUDED.WORKER.CONTRACT | Include worker | Blocker | worker_assignment_lookup | PersonId, active AssignmentId, normalized local CascadingLevel, or advertised public child is absent; supplied CascadingLevel is invalid; a non-Self scope lacks advertised hierarchy evidence; or ManagerAssignmentId is mapped | Default absent CascadingLevel to `"0"`; validate supplied values through `ora_defaulting_rules.md`; resolve hierarchy only from an advertised worker read; remove ManagerAssignmentId and do not substitute ESS | Yes |
| GP.TEMPLATE.GOAL.CONTEXT | Existing-plan template goal create/update | Blocker | goal_plan_goal_lookup | Exact plan MassRequestId, authenticated caller, active primary admin assignment, or resolver-selected create contract is missing | Re-read exact plan and current admin context, then rebuild the selected child-create or batch payload. Resolve a same-host batch root only when batch is selected. | Yes |
| GP.ESS.CONTRACT | Assignment | Blocker | assign_goal_plans_job_lookup | Job definition or parameters are current_metadata_required | Obtain current authoritative evidence | Yes |
| GP.ESS.IMPACT | Assignment | Blocker |  | Configured selector evidence or execution approval is missing, stale or bound to another target | Run validate_assignment_impact for selector evidence and environment/plan/date binding. ESS computes eligibility; no advance count is required. If an explicit hard cap is required, resolve a supported bounded route | Yes |
| GP.ESS.FIELDS | Assignment | Blocker | assign_goal_plans_job_lookup | Process type/name, job definition, or remaining parameters are missing, or the resolved effective date is invalid | Default an omitted ESS date to today at preview; complete the authoritative ESS contract | Yes |
| GP.PENDING.APPROVAL | Update | Blocker | goal_plan_lookup | Goal Plan is pending approval | Wait for approval completion and re-read | No |
| GP.REVIEW_PERIOD.ASSIGNEES | Review Period update | Blocker | goal_plan_lookup | One or more assignees remain | Delete all assignees separately, re-read, then retry | Yes |
| GP.DELETE.UNASSIGNED | Goal Plan delete | Blocker | goal_plan_lookup | Plan is assigned or delete capability is unverified | Use status management or guided UI after proving zero assignees | Yes |
| GP.STAGE.SEPARATE | Any mutation | Blocker |  | Request combines independent stages, except the declared maximum-then-enforcement sequence | Split independent operations into separate runs and approvals; retain the narrow approval-bound maximum-enforcement sequence | Yes |
| GP.APPROVAL.FRESH | Any mutation or ESS handoff | Blocker |  | Fresh state differs from approved fingerprint | Rebuild preview and approval | Yes |

## Design Lookup Requirements

| Rule ID | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|
| GP.DATE.ENVELOPE | review_period_lookup | Goal Plan dates are used | Period ID, dates, status | ora_reference_lookups.md |
| GP.NAME.UNIQUE | goal_plan_search | Regular create or name/period update | Exact name, Review Period, existing Plan ID | ora_reference_lookups.md |
| GP.PERSON.CONTEXT | current_user_person_context_lookup | Template-goal create/update, or metadata-required Goal Plan create | Authenticated caller's runtime context only | ora_reference_lookups.md |
| GP.PRIMARY.UNIQUE | primary_goal_plan_lookup | Primary create or activation | Existing Primary identity/status and technical dates | ora_reference_lookups.md |
| GP.ELPRO.ACTIVE | eligibility_profile_lookup | Eligibility is used | Internal profile ID, business name, active status, Goal Management usage, complete pagination evidence, and authoritative criteria evidence when matching semantically | ora_reference_lookups.md |
| GP.WORKER.EXISTING | worker_assignment_lookup | Explicit included-worker maintenance | Active assignment at effective date | ora_reference_lookups.md |
| GP.ESS.CONTRACT | assign_goal_plans_job_lookup | Assignment | Job definition and parameters | ora_reference_lookups.md |
| GP.DOC.TYPE.RANGE | performance_document_type_lookup | Performance integration | Active document type and date range | ora_reference_lookups.md |
| GP.TEMPLATE.GOAL.CONTEXT | goal_plan_goal_lookup | Existing-plan template goal | Exact plan and Goal Plan goal context | ora_reference_lookups.md |
| GP.PENDING.APPROVAL | goal_plan_lookup | Explicit maximum enforcement, update, or deletion | Fresh raw maximum and nullable enforcement values, current Goal Plan state, and assignees as applicable | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GOAL_PLANS.DESIGN | decision | 60 | design_enforcement | rest->GOAL_PLANS.REST_DESCRIBE;assignment->GOAL_PLANS.ASSIGNMENT_PREVIEW;blocked->GOAL_PLANS.BLOCKED | GOAL_PLANS.DEFAULTS | stop | Dependencies and defaults are ready |


---

# Goal Plan Design Advisory

## Guidance Sources

| Source Mode | Allowed Sources | When Used |
|---|---|---|
| Packaged | Catalog identities and approved Goal Plan functional contract | Consultant planning |
| Runtime | Current Goal Plan, worker-assignment, reference, and Scheduler metadata | Environment readiness and execution |

## Guidance Topics

| Topic | Advisory Level | What To Explain | Do Not Include |
|---|---|---|---|
| Lifecycle | Strong | Create, activation, population, and assignment are independent | Chained approval or automatic ESS |
| Visibility | Advisory | Default UI overview selects the Review Period with the latest start date; inactive plans remain visible to HR specialists but not selectable by managers/workers | Treating UI default filtering as REST search semantics |
| Primary plan | Strong | Global availability across active Review Periods; no worker, profile, plan-goal, or ESS sections | Treating Primary as a regular plan with a null period only |
| Primary integrations | Strong | Active Primary plans receive Talent Review goals; compatible performance templates/documents create or populate the Primary plan for the document Review Period | Associating the Primary plan itself to one Review Period |
| Goal design controls | Strong | Access, goal-setting window restrictions, evaluation type, HR-assigned-goal delete/cancel access, weighting, and min/max counts are independent design choices | Invented values or collapsing distinct controls |
| Plan goals | Strong | Goal dates stay inside plan dates; optional library, measurement, task, target-outcome, and assignee-edit features require enablement | Adding goals to a Primary plan or treating Import Goals as FSM CSV import |
| Eligibility Profile | Strong | Resolve an active profile owned by BEN_MANAGE_ELIGIBILITY_PROFILES | Embedded profile maintenance |
| Worker handling | Strong | Existing assignment resolution differs from worker creation; population scope distinguishes selected/direct/all-report variants | Real worker examples, stored IDs, or implicit scope |
| ESS | Strong | Goals are not assigned automatically; reruns are additive and excluding workers later does not reverse prior assignments | Unverified job definition or parameters |
| Lifecycle restrictions | Strong | Assigned plans cannot be deleted; pending-approval plans cannot be updated; Review Period changes require zero assignees | Treating inactivation, assignee deletion, and plan deletion as equivalent |
| Batch processing | Advisory | Explain the three HRG_GP profile options and dynamic child count; retain recommended defaults | Tuning profile options from this Goal Plan skill |
| MASS_REQ | Strong | Logged-in HR/admin context is template context only | Treating context IDs as assignees |
| Redwood Goal Center | Strong | UI validation requires `ORA_HCM_VBCS_PWA_ENABLED` and `ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED` enabled | Automatic profile-option changes |

## Output Rules

| Situation | What Happens |
|---|---|
| Dependency ownership is external | Return the owning route and resume context |
| A consultant asks why an inactive plan is missing | Explain role-specific visibility before changing status; no write is implied |
| ESS contract is unverified | Return assignment plan with a blocking current_metadata_required; do not submit |
| Primary plan is requested | Apply Primary-only field/dependency rules and skip population/ESS routes |
| Delete or Review Period change is requested | Read current assignee/approval state, explain the blocker, and use a separately approved guided route unless exact REST metadata exists |
