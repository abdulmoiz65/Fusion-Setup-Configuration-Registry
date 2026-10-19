# Enterprise Shifts Dependency Readiness

## Source Basis

- Enterprise Shifts Rest Describe, Confluence page 21451526148, version 3
- Enterprise Shifts Test Technical Design Document for FSCIR, Confluence page 21452837175, version 4
- Enterprise Shifts UI does not provide shift deletion, user confirmation, 11 August 2026
- Enterprise Shifts naming, category recommendation, time, reuse, and approval policy, developer-provided, received 18 August 2026
- Enterprise Shift name, field-value precedence, and default-origin display rules, user-provided, received 19 August 2026
- Automatic final Data Loader completion and read-back verification, user-provided, received 19 August 2026
- Dependent-workflow handoff and final-result disclosure policy, user-provided, received 19 August 2026
- Active-workflow-context inspection policy, user-provided, received 19 August 2026
- Generalized dependent-flow resume prompt policy, user-provided, received 19 August 2026
- Start task-authorized Enterprise Shifts Data Loader status requests automatically after approval, user-provided, received 21 August 2026
- Terminal Enterprise Shifts result must include a business-only summary after success or error, user-provided, received 10 September 2026

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Active workflow context | Inspect the current workflow state before treating an Enterprise Shift request as standalone; retain a parent workflow only when its documented task resources establish this Shift as a prerequisite |
| 2 | Target and identity | Bind the exact Fusion target, authenticated user, and task code ORA_HTS_MANAGE_SHIFTS |
| 3 | Shift name and existing shift | Attempt Shift Name construction before exact-name discovery using all valid documented inputs, preserve an explicit Shift Name, and ask directly for Shift Name when construction fails; then show an existing shift only when all configuration values and intended scheduling behavior match |
| 4 | Shift category | Resolve an exact code only when supplied; otherwise provide a category-name recommendation from the shift time and description |
| 5 | Time and duration contract | Validate positive duration, same-day or next-day state, and target-supported nearest-minute time serialization |
| 6 | Writable handoff | Require a separate writable runbook, exact preview, user approval before creation or update, and post-write read verification. The approved handoff must create one new Enterprise Shift or update only the explicitly selected existing Enterprise Shift, applying the approved Shift Name, Shift Category, Work Duration, Unpaid Break Duration, Start Time, and End Time. |
| 7 | Final completion and verification | After an approved asynchronous request is accepted, immediately start the task-authorized Data Loader status request. If it is in progress, automatically issue follow-up status requests to terminal status. On success, read back and compare the Enterprise Shift with the approved configuration before reporting final success. On every terminal success or error outcome, return the task-owned business-only terminal summary; never end with a generic Data Loader status table. |
| 8 | Dependent-workflow handoff | When the active workflow context confirms one documented parent workflow, prompt the user to resume that named parent after the Enterprise Shift is verified. A confirmed resume returns the parent identity and safe resume stage to the orchestrator; it does not start, preview, approve, or submit the dependent operation. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| es_target | Exact Fusion target and task identity | Yes | Always | Satisfied | Selected project environment and nested task manifest |  | Prevent cross-environment or cross-task routing | Confirm the intended environment and Enterprise Shifts task | Environment identity and task code |
| es_active_workflow_context | Active workflow and parent-task relationship | Yes | Always | Lookup | Current workflow state, unfinished parent request, and the parent's applicable task resources | resolve_active_workflow_context | A request made while another setup workflow is active must not be treated as standalone before the parent relationship is checked | When no active parent workflow exists, continue as a standalone Shift request. When one documented parent workflow establishes this Shift as a prerequisite, retain its identity and pending stage. When the context is ambiguous or conflicting, stop and ask for the intended workflow. | Standalone receipt, or verified parent workflow identity, documented prerequisite relationship, approved or pending parent values, and safe resume stage |
| es_existing_shift | Existing shift or create candidacy | Yes | Create or update | Lookup | Explicit Shift Name or documented name construction from supplied, current-conversation, selected-configuration, and configured-default values; enterpriseShifts finder or returned item link | find_enterprise_shift_by_exact_name | Display every retrieved candidate with its Shift Name, Shift Category, Start Time, End Time, Work Duration, Unpaid Break Duration, intended scheduling-behavior comparison, and one classification: exact reusable match, nonmatching candidate requiring specialist review, ambiguous candidate requiring specialist review, or no matching shift / create candidacy. Recommend reuse only for an exact match. | Supply Shift Name only when it cannot be constructed; do not request missing naming inputs. Explicitly select the update target when an update is requested. | Derived or explicit Shift Name; candidate comparison and classification receipt; create-candidacy receipt; or explicit update target |
| es_update_item | Current update target | Yes | Update | Lookup | enterpriseShifts primary-key finder or returned item link | find_enterprise_shift_by_id | PATCH must address exactly one current shift | Supply the exact ShiftId or returned item URL | ShiftId and current comparison receipt |
| es_shift_category | Valid shift-category code or optional category-name recommendation | Conditional | ShiftCategory is supplied or omitted | Lookup | Workforce Scheduling – Common – Manage Common Lookups with LookupType ORA_HTS_ENT_SHIFTS_CATEGORY when supplied; shift time and description when omitted | resolve_shift_category_code | Fusion stores the provider LookupCode rather than the display meaning; a missing category must not block creation | Supply an exact code or meaning for provider resolution, or review the recommendation without submitting a category code | ShiftCategory code or category-name recommendation |
| es_time_contract | Target-supported time and end-day contract | Yes | A time value will be sent | Blocked | Same-target read or controlled non-production validation |  | Describe does not define the exact JSON lexical format or time-zone interpretation | Provide target evidence for nearest-minute serialization and same-day or next-day interpretation | Exact time format and end-day interpretation |
| es_write_handoff | Approved writable runbook and executor | Yes | Any mutation is requested | Verify | Separate runbook owned outside ora-resource authoring |  | These files validate and gate setup facts but do not construct or submit Fusion writes | First present the required business-only Complete Summary. Then transition to the provider-owned immutable preview: Present the immutable preview and obtain explicit user approval before creation or update. For create, authorize exactly one new Enterprise Shift. For update, authorize only the explicitly selected current Enterprise Shift. Apply only the approved Shift Name, Shift Category, Work Duration, Unpaid Break Duration, Start Time, and End Time. | Complete Summary receipt; preview and approval fingerprints; approved operation; target Shift identity for update; approved field values |
| es_final_shift_completion | Final Enterprise Shift completion and read-back verification | Yes | An approved asynchronous create, update, import, or load request has been accepted | Verify | Accepted archive identity, returned request, approved configuration, and exact Shift Name or returned item identity | verify_final_shift_load | Submission acceptance is not final completion. Final success requires a documented terminal success status and a read-back that matches the approved Shift Name, Start Time, End Time, Work Duration, Break Duration, supplied Shift Category, and Shift Status | Immediately start the task-authorized status request; if it reports in progress, automatically issue follow-up status requests until completion. On success, return the saved configuration in the business-only Complete Summary format, including any application-derived total duration or end time and system-populated defaults in Defaults Applied. On failure, timeout, partial success, or mismatch, return a business-only terminal result that identifies the Shift Name, business-friendly outcome, known completed and failed counts when available, and one safe next action. Never end either terminal branch with a generic Data Loader status table. | Terminal status, totals, verified Enterprise Shift details, application-derived total duration or end time when returned, default-origin indicators, comparison result, and terminal business summary receipt |
| es_dependent_workflow_handoff | Verified prerequisite handoff | Conditional | The active workflow context identifies one documented parent workflow that uses the verified Enterprise Shift as a prerequisite | Satisfied | Terminal-success verification result, retained parent workflow identity, and documented prerequisite relationship |  | A verified prerequisite must give the user a clear, named choice to resume its active parent without implying that the dependent workflow has started or been approved | Prompt: Would you like to resume {parent workflow}? On confirmation, return resume_requested with the retained parent identity and safe resume stage. When no verified parent relationship exists, end with the standalone Shift result and no resume prompt. | Verified prerequisite identity, parent-workflow readiness statement, resume prompt, and safe resume stage |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact local manifest or selected-environment fact is already established | Continue |
| Lookup | A documented read-only Fusion lookup is required | Read-only only |
| Verify | A separate runbook, preview, approval, or target test must be inspected | Verification only |
| Blocked | Required time contract, identity, category, or write handoff is missing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ES.CHECK_DEPENDENCIES | decision | 40 | resolve_dependency | ready->ES.ENFORCE_DESIGN;blocked->ES.HANDLE_ERROR | ES.RESOLVE_REFERENCES | stop | After all applicable reference lookups |
