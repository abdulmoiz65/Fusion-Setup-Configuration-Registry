# Requested Feedback Template Unstructured Input Extraction

Use this resource when a consultant supplies source material in DOCX, PDF,
PPT/PPTX, XLS/XLSX/CSV, plain text, Markdown, screenshots, ZIP, or mixed
source-pack inputs.

## Source inventory

Record each source with:

| Field | Required | Notes |
|---|---:|---|
| `source_id` | Yes | Stable local identifier for traceability |
| `path_or_reference` | Yes | Preserve the supplied file/folder path or attachment label |
| `source_type` | Yes | `docx`, `pdf`, `pptx`, `xlsx`, `csv`, `text`, `markdown`, `screenshot`, `zip`, or `unknown` |
| `extraction_status` | Yes | `read`, `partial`, `blocked`, or `reference_only` |
| `source_reference` | Yes when available | Page, slide, worksheet/row, paragraph, screenshot, file, or folder |
| `contains_candidate_data` | Yes | True only when creation, update, delete, import, or dependency values are visible |
| `notes` | No | Missing OCR, damaged file, screenshot-only limitation, or ambiguity |

If a source is screenshot-only, extract visible facts conservatively and mark
values with low visual confidence as review-needed. Do not treat screenshot UI
labels as tenant metadata unless they are readable and relevant to the target
implementation.

## Fact extraction

Before task mapping, classify General Feedback versus Performance Goal Feedback
and run the task wrapper's offline `plan_requirements` action. Performance Goal
Feedback permits only the seeded `PERF_GOAL_QSTNR_V1` questionnaire. Record a
requested custom questionnaire as an unsupported requirement and explain why;
do not convert it into a questionnaire creation/association task or silently
substitute the seed as fulfillment of the custom requirement. For supported
goal-template creation, plan seed lookup and verification. For General Feedback,
retain the requested existing/custom questionnaire and provider route.

Apply the functional-area profile baseline independently of extracted source
facts. Every Run Book plan must carry the prerequisites
`HRA_REQUEST_FEEDBACK_ENABLED = Y` and
`ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED = Y`. When target reads are available,
omit the profile task only if both exact SITE values are verified as `Y`.
Otherwise add one leading `Manage Administrator Profile Values` task with both
profile codes in its notes. Do not require the consultant source to repeat this
PM-controlled baseline, and do not create one duplicate setup task per profile.

Extract facts into these groups before mapping tasks:

| Group | Examples | Mapping behavior |
|---|---|---|
| Scope | Requested Feedback Template, Feedback Templates, questionnaire prerequisite, Performance Goal Feedback | Determines owning route |
| Operation intent | create, update, inactivate, delete, import, validate, reference-only | Drives approval and readiness |
| Template identifiers | template name, type, status, description/comments, availability | Required for setup validation |
| Questionnaire evidence | questionnaire name, version, active/latest state, eligibility, template dependency | Validate through owning provider |
| Manager and participant behavior | specific manager types, feedback participant context, performance-goal feedback impact | Keep within Feedback Templates or route separately |
| Dependency evidence | security, notifications, profile or feature readiness, performance document integration | Route to dependencies or blockers |
| Data artifacts | workbook rows, CSV rows, supplied setup documents | Extract requirements only; never submit as template import data |
| Decisions | naming conflicts, in-use template changes, missing values, destructive action choices | Present to user before runbook creation or execution |

Do not infer tenant-specific IDs, questionnaire identifiers, active template
selection, privileges, notification settings, or approval behavior from generic
examples. When a source supplies the business value, such as a questionnaire
name, profile option code, or manager-type label, carry that value into the
configuration plan and runbook. Resolve its target-tenant identity, eligibility,
current value, LOV code, route evidence, or REST payload later as an
agent-owned validation step before the dependent external action.

## Requested Feedback Template cues

| Cue in source | Task route | Notes |
|---|---|---|
| Feedback Template, template type, active/inactive status, specific manager type, questionnaire reference | `hcm.performance-management.requested-feedback-template.feedback-templates` | Consult the best-practice topic map before guidance |
| Performance Goal Feedback or goal-feedback template activation | `hcm.performance-management.requested-feedback-template.feedback-templates` | Require target-tenant activation-impact evidence |
| Questionnaire Template or Questionnaire create/update/delete | Owning questionnaire provider | Separate route; creation for Requested Feedback applies only to General Feedback, never a custom goal-feedback substitute |
| Runtime Request Feedback transaction or `FeedbackRequest` data | Runtime feedback provider when available | Does not authorize Feedback Template setup |
| Participant feedback in performance documents | Owning Performance Document provider | Keep separate from Requested Feedback Template setup |
| Anytime feedback, check-in templates, performance roles, process flows, performance document types, performance templates, sections | Owning Performance Management task | Separate route and approval scope |
| CSV/workbook requirements for Feedback Templates | Feedback Templates REST planning task | Source values only; no file upload/import |
| Explicit template CSV/FSM import/export or HDL/HSDL request | Unsupported channel | Return `UNSUPPORTED_EXECUTION_CHANNEL`; preserve source evidence without executing |

## Conflict handling

Block runbook creation only when the task set itself is ambiguous, source files
are unreadable, required source values are missing or conflicting, destructive
intent is ambiguous, the configured target environment cannot be identified
from available project configuration, or the mapping cannot preserve complete
source coverage.

Allow runbook creation with pending validation steps when the task is clear but
a future execution step still needs questionnaire readiness, LOV resolution,
profile current-state checks, target-tenant evidence, approval, route supportability,
immutable REST preview, or a business decision.
Capture those items in the readiness summary as agent-owned validation or
approval gates, not as consultant blockers.

Never combine separate operations just because they were found in one document.
Separate Feedback Templates, questionnaire lifecycle, runtime feedback,
performance document, and other Performance Management work into independently
approvable tasks.
