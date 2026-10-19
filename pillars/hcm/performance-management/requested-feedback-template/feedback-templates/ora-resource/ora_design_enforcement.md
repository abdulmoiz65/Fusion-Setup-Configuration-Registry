# Feedback Templates Design Enforcement

Source: Oracle Fusion Cloud Talent Management, Feedback Templates.

## Enforcement Order

Apply the evidence alternatives in `ora_reference_lookups.md` before declaring
a technical dependency blocked. A complete eligible LOV result can satisfy
questionnaire identity/lifecycle selection; it does not replace template-type
association compatibility. Omitted optional fields alone are not restrictions.
Explicit negative state, conflicting identity, auth/authz failure, lifecycle
restrictions and required governance remain enforceable regardless of history.

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Specify questionnaire | Specify a questionnaire for the feedback template. |
| 2 | Enable request availability | Set the template status to Active when it must be available for feedback requests. |
| 3 | Respect active in-use restrictions | When an Active template is in use, modify only its name or description; do not change its questionnaire. |
| 4 | Respect inactive behavior | Do not expect new feedback requests to use an Inactive template. |
| 5 | Respect unused-template behavior | Change the questionnaire or delete the template only when the template isn't in use. |
| 6 | Resolve exact identity | For existing-template work, accept only one stable ID or exact name; partial and multiple matches fail closed. |
| 7 | Validate feedback type | Run the type-specific compatibility gate before dependent questionnaire creation and before template association. Require eligible, not merely active/latest. |
| 8 | Assess goal activation impact | Before activating a Performance Goal Feedback template, identify the current intended active template(s) and present the target-tenant impact for approval. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Creating a feedback template | Blocker | | No questionnaire is specified. | Specify a questionnaire. | Yes |
| A feedback template is intended to be available for feedback requests | Blocker | | Template status is not Active. | Set the template status to Active. | Yes |
| An Active feedback template is in use | Blocker | | A questionnaire change is requested. | Modify only the template name or description, or use a template that isn't in use before changing its questionnaire. | No |
| A feedback template is Inactive | Blocker | | A new feedback request is expected to use the template. | Set the template to Active if it must be available for new requests. | Yes |
| A questionnaire change or deletion is requested | Blocker | | The feedback template is in use. | Change the questionnaire or delete the template only when it isn't in use. | No |
| Existing-template work is proposed | Blocker | | The stable ID or exact name does not resolve exactly once. | Supply one exact identity; do not use a partial-name match. | Yes |
| New dependent questionnaire or template association is proposed | Blocker | resolve_questionnaire_association_compatibility | Compatibility is ineligible or unresolved for the effective template type. | Performance Goal Feedback requires seeded PERF_GOAL_QSTNR_V1; reject custom intent during intake. Custom creation/derivation belongs only to General Feedback in this workflow. Resolve target IDs rather than copying examples. | No |
| A Feedback Template mutation is proposed | Blocker | | Channel is not declared REST POST/PATCH, or the exact request lacks current approval. | Reject unsupported channels; validate and approve the immutable REST preview. | No |
| Performance Goal Feedback activation is proposed | Blocker | resolve_goal_activation_impact | Current active-template evidence or the exact activation impact is unresolved, or approval does not cover that effect. | Resolve the impact, show it in the immutable preview, and obtain fresh approval. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_questionnaire_readiness | Creating or changing a questionnaire reference, including Performance Goal Feedback | Exact questionnaire readiness evidence | ora_reference_lookups.md |
| resolve_questionnaire_association_compatibility | New dependent questionnaire, template POST or questionnaire/type-changing PATCH | Eligible result bound to the current target, stage, candidate and effective template type | ora_reference_lookups.md |
| resolve_goal_activation_impact | Activating or replacing a Performance Goal Feedback template | Current active state and activation impact | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FEEDBACK_TEMPLATES.ENFORCE | decision | 20 | design_enforcement | passed->FEEDBACK_TEMPLATES.DONE;blocked->RETURN_ISSUES | FEEDBACK_TEMPLATES.VALIDATE | stop | A feedback template is being created, changed, activated, inactivated, or deleted. |
