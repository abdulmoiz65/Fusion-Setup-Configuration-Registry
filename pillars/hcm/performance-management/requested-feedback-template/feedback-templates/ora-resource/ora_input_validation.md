# Feedback Templates Input Validation

Source: Oracle Fusion Cloud Talent Management, Feedback Templates.

General and Performance Goal Feedback Templates are REST-only. Reject FSM/CSV
import/export and HDL/HSDL with `UNSUPPORTED_EXECUTION_CHANNEL`. CSV/workbooks
may supply requirements only. This boundary does not apply to other objects.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Create configuration | Name, template type, Status, Specific Manager Types, Questionnaire | Stop planning | Provide every required field; do not infer a default. | Creating a feedback template | |
| Existing-template identity | One stable ID or exact template name | Stop planning | Resolve exactly one current template; partial-name and multiple matches fail closed. | Updating, deleting, or identity-sensitive review | |
| Questionnaire readiness | One eligible questionnaire | Stop before the dependent preview or execution step, not before source-backed plan/runbook creation | Validate it through the questionnaire provider using exact target-tenant evidence. | Creating a template or changing its questionnaire | resolve_questionnaire_readiness |
| Tenant-specific REST route | Target identity, one declared capability evidence alternative, fresh compatible collection GET, and owner confirmation only when policy explicitly requires it | Exhaust declared alternatives before stopping the dependent preview or execution | Follow ora_reference_lookups.md and retain the evidence basis; do not reuse another environment's route UUID. | Task-declared REST create or update | resolve_feedback_templates_route_supportability |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A feedback template is intended to be available when creating a feedback request | Verify | Set the template status to Active. | |
| New dependent questionnaire, template creation, or questionnaire/type-changing PATCH is proposed | Verify | Require type-specific compatibility in addition to identity and active/latest status; ordinary updates preserve the current association; do not hard-code or substitute an identifier. | resolve_questionnaire_association_compatibility |
| Redwood, goal, notification, TDS, VBS, or security behavior is requested | Verify | Obtain authorized target-tenant readiness evidence before presenting the behavior as available. | resolve_tenant_runtime_readiness |
| A questionnaire change or deletion is requested | Verify | Confirm current Active and in-use state before continuing. | |

When the consultant source provides required create values, questionnaire
readiness, manager-type LOV mapping, profile current-state reads, and
route supportability and REST payload integrity are validation gates for the runbook and agent-owned
validation steps. Execute the declared
read-only REST/provider route before reporting a consultant blocker. For
questionnaires, accept a complete eligible `questionnairesLOV` result or use
the provider identity read to resolve missing evidence; for Specific Manager
Types, use `PER_SUPERVISOR_TYPE` through
`core.fusion-api.apps-common.lookups` and its declared eligibility alternatives.
Apply the resolution procedure in `ora_reference_lookups.md` before escalation.
An omitted field is unknown, not false; explicit restrictions and conflicting
identity evidence still fail. A missing validation route is a skill gap to fix,
not a reason to ask the consultant for ordinary target evidence.

## Field Validation

Known product restrictions apply during intake: Performance Goal Feedback uses
only seeded `PERF_GOAL_QSTNR_V1`; custom goal questionnaire creation/association
is unsupported. The guidance allowing plans with pending tenant validation does
not make an unsupported request executable. General Feedback custom creation
retains the provider validation flow.

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Questionnaire | Require a questionnaire. | Creating a feedback template | |
| Template status | Require Active status for a template that must be available for feedback requests. | The template is intended for feedback requests | |
| Existing-template identity | Require one stable ID or exact name; reject partial or ambiguous results. | Updating, deleting, or identity-sensitive review | |
| Questionnaire | Require an eligible provider-confirmed questionnaire. | Creating a template or changing its questionnaire | resolve_questionnaire_readiness |
| Active/in-use restriction | Permit only name or description changes; block questionnaire changes. | An Active template is in use | |
| Deletion eligibility | Permit deletion only when the template is confirmed not in use. | Deletion is requested | |
| Template-type compatibility | Require eligible output from the local compatibility validator with matching target, type, stage and candidate evidence; unknown is not success. | New dependent questionnaire, template creation, or questionnaire/type-changing PATCH | resolve_questionnaire_association_compatibility |
| Runtime readiness | Require evidence for only the profile, page, role, TDS, VBS, or notification behavior in scope. | Runtime-dependent guidance or activation planning | resolve_tenant_runtime_readiness |
| Goal activation impact | Require an impact summary before previewing activation of a Performance Goal Feedback template. | Activation or replacement is requested | resolve_goal_activation_impact |
| REST approval integrity | Require the JCS SHA-256 digest, exact payload, target environment alias, operation, and relative path in the immutable preview. | REST POST or PATCH is proposed | |


## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FEEDBACK_TEMPLATES.VALIDATE | decision | 10 | validate_input | valid->FEEDBACK_TEMPLATES.ENFORCE;invalid->RETURN_ISSUES | none | stop | A feedback template is being created or changed. Evaluate ora_rest_execution.json evidence_resolution and ora_reference_lookups.md alternatives before classifying a technical dependency as unresolved. |
