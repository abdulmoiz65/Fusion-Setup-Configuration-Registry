# Feedback Templates Dependency Readiness

Source: Request Feedback Template Best-Practice Reference, sections 4–19.

## Required Dependency Order

Classify seeded-only Performance Goal Feedback versus General Feedback before
adding dependencies. A custom goal questionnaire is an unsupported requirement,
not a dependency to create. Plan lookup of `PERF_GOAL_QSTNR_V1` instead for a
supported goal-template request; missing seed data never enables creation.

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Mandatory Request Feedback profiles | Verify `HRA_REQUEST_FEEDBACK_ENABLED = Y` and `ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED = Y`; when either is not verified as `Y`, the parent plan adds one leading Manage Administrator Profile Values task and completes its separately approved profile route before a dependent template mutation. |
| 2 | Scope classification | Distinguish Feedback Template setup from questionnaire lifecycle, FeedbackRequest runtime transactions, participant feedback, and anytime feedback. |
| 3 | Questionnaire | Carry the source questionnaire name into the plan/runbook; prove template-type compatibility before provider creation, then revalidate after creation before association. Identity and lifecycle readiness alone are insufficient. |
| 4 | Tenant capability | For requested runtime behavior in scope, obtain authorized target-tenant evidence for page mode, other profiles, TDS/VBS, roles, alerts, and goal access. |
| 5 | Lifecycle | Resolve exact template identity and current status/in-use state before planning a change. |
| 6 | Consequential activation | For Performance Goal Feedback, assess the current intended active template and the impact of activation before approval. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| request_feedback_profiles | Request Feedback and Redwood Request Feedback SITE values | Yes | Every Requested Feedback Template Run Book and every Feedback Templates mutation | Verify | Exact `profileOptions` definitions and `siteProfileOptionValues` reads through `core.fusion-api.apps-common.profile-options` | resolve_request_feedback_profiles | PM requires both capabilities enabled before dependent setup execution. | Treat `Y` as verified no-change; otherwise use the parent's one-task profile route and separately approved exact writes. | Both exact codes, current SITE values, desired `Y`, evidence references, write/readback status |
| questionnaire_association_compatibility | Template-type-specific eligibility | Yes | New dependent questionnaire, template creation or questionnaire/type-changing PATCH | Verify | Provider-verified same-target evidence under ora_reference_lookups.md | resolve_questionnaire_association_compatibility | A creatable questionnaire is not necessarily eligible for this feedback-template type. | Resolve supported constraints before creating it; do not silently substitute. | Stage, type, target, rule, candidate, evidence references and validator result |
| questionnaire_readiness | Eligible questionnaire | Yes | Creating a template or changing its questionnaire | Verify | Complete eligible `GET /hcmRestApi/resources/11.13.18.05/questionnairesLOV` result or conditional provider identity read under ora_reference_lookups.md | resolve_questionnaire_readiness | A template requires a usable questionnaire. | Resolve the source reference using the declared alternatives before escalation. | Current questionnaire identity and eligibility basis |
| specific_manager_type | Specific Manager Types | Yes | Creating a template or changing its manager types | Verify | `PER_SUPERVISOR_TYPE` via `core.fusion-api.apps-common.lookups` | resolve_specific_manager_type | A template requires a target-valid manager type. | Resolve the source label or code through the routed lookup API before treating the value as unresolved. | Canonical manager-type code, display label, active/selectable evidence |
| tenant_runtime_readiness | Target-tenant runtime prerequisites | Conditional | Redwood, goals, notifications, TDS, VBS, or security behavior is in scope | Verify | Authorized target-tenant evidence; lookup contract TBD | resolve_tenant_runtime_readiness | Release labels alone do not prove tenant behavior. | Obtain approved read-only evidence through the active workflow; do not infer profile values or access. | UI mode, relevant profiles, TDS/VBS state, role evidence |
| goal_activation_impact | Active Performance Goal Feedback template impact | Conditional | Activating or replacing a Performance Goal Feedback template | Verify | Authorized target-tenant evidence; lookup contract TBD | resolve_goal_activation_impact | Activation can affect other goal-feedback templates. | Show the exact tenant impact and obtain fresh approval before a supported mutation. | Current active template evidence, intended change, impact summary |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Dependency readiness | A required questionnaire, target-tenant capability, or activation impact is verified. | No; this reference does not create an execution route. |
| Dependency blocker | Explicit validation failed or evidence remains unresolved after all applicable declared alternatives. | No; stop only the dependent external step. Report a technical skill limitation separately from a missing business value or required governance decision. |

Manager readiness accepts the eligibility alternatives in
`ora_reference_lookups.md`; a separate selectable flag is not mandatory.
Mark a dependency resolved with its selected evidence basis and retain it with
the preview. Do not reopen it merely because a different evidence alternative
is unavailable. Revalidate when relevant target state or evidence freshness changes.
