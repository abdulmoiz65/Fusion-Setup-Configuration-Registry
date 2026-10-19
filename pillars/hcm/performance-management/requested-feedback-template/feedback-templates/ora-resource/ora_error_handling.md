# Feedback Templates Error Handling

Source: Oracle Fusion Cloud Talent Management, Feedback Templates.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Explicit CSV/FSM import/export or HDL/HSDL execution for Feedback Templates | Return UNSUPPORTED_EXECUTION_CHANNEL, explain supported REST inspection/create/update, and ask whether the user wants a separately requested REST plan. Do not silently convert the request or create import artifacts. Questionnaire provider routing is a separate object workflow. |
| Missing conversational creation decisions | Return clarification_required with named missing business fields, follow-up questions and confirmed values. Ask these questions, merge explicit replies into the original input, and rerun offline planning; do not request tenant IDs or invent values. |
| Ordinary update includes QuestionnaireId or TemplateType | Return ASSOCIATION_ACTION_REQUIRED and explain that association changes use associate with compatibility validation and a new exact preview. Do not add unchanged association fields to bypass this distinction. |
| In-use template ordinary edit includes protected fields | Return LIFECYCLE_BLOCKED; explain that only name/description edits are allowed while in use. Offer a supported name/description edit or a separately reviewed unused-template configuration. Do not change lifecycle state to force the requested update. |
| Missing goal attributes or goal activation impact evidence | Ask for missing business goal attributes and resolve their source-backed mapping; if impact evidence is missing, perform the declared review before approval. Do not ask the user to invent verification flags. |
| Ordinary update has no changed value | Report NO_CHANGE and explain the current values already match; no mutation or repeat approval is needed. |
| Existing-questionnaire scope changes to creation | Reclassify offline, refresh the mapping with HRT_MANAGE_QUESTIONNAIRES before Feedback Templates, preserve approved design values, and persist a new provider handoff. Do not resume from the old existing-reference plan. |
| Questionnaire inspection fails on an unused optional component | Record SKILL_LIMITATION and the exact helper, stage, component, optionality evidence, requested component scope and failure message. Provider/import readiness is unresolved; do not assert a tenant defect or recommend administrator repair solely from zero attributes. |
| Metadata helper supports fallback but provider or import contract does not | Record SKILL_LIMITATION for the contract mismatch. Route to the provider owner; do not synthesize schema or invoke a loader from this folder. |
| Supplied Questionnaire metadata is newer than a retained failure | Follow Questionnaire metadata recovery in ora_rest_execution.md through the existing provider. Obtain fresh strict target validation and record a new outcome; the supplied file alone cannot clear the blocker or establish creation. |
| A downloaded template contains an Oracle generation error and no METADATA | Preserve the sanitized error and file identity as diagnostic evidence, not an import schema. Block only the dependent requested or target-required operation. A QuestionnaireTemplate generation failure does not establish that ordinary Questionnaire creation is unavailable. |
| Fresh strict Questionnaire metadata succeeds after sample synthesis failed | Retain the older failure as history and continue the provider's remaining current validation gates. Empty unused optional attributes do not invalidate a real UCM schema by themselves; requested and target-required component evidence remains mandatory. |
| Questionnaire provider returns blocked, failed, partial or uncertain | Preserve the outcome and stop dependent association before reads or writes. A retained eligible LOV does not override an unresolved creation result. Require provider verification and fresh association checks before resuming. |
| Custom questionnaire requested for Performance Goal Feedback | Return GOAL_FEEDBACK_SEEDED_QUESTIONNAIRE_REQUIRED during intake. Explain that only seeded Performance Goal Feedback (PERF_GOAL_QSTNR_V1) is supported. Do not create or retry; recommend Not Applicable for a pre-existing unsupported replacement task. |
| Required goal-feedback seed is absent | Return SEEDED_QUESTIONNAIRE_MISSING as a prerequisite failure. Do not create, clone or load a replacement. |
| Compatibility validator returns ineligible | Record VALIDATION_FAILED with the exact failed constraint. Stop the dependent questionnaire creation or association; no silent substitution. |
| Compatibility validator returns unresolved | Exhaust declared identity/readiness evidence alternatives, then record SKILL_LIMITATION. The known seeded-only Performance Goal Feedback restriction remains enforced; missing target evidence cannot authorize custom creation or association. |
| Fusion returns HRA-960540 / HRA_TMPLT_QUESTIONNAIRE_INVLD | Record Fusion API failure and invalidate the rejected candidate/type evidence. Preserve created questionnaires and verify the template by exact read. For Performance Goal Feedback, explain the seeded-only rule; no custom derivation, rename or retry workaround is supported. |
| A feedback template has no questionnaire | Stop and specify a questionnaire. |
| A template must be available for feedback requests but isn't Active | Stop and set the template status to Active. |
| A questionnaire change is requested for an Active template that is in use | Stop; only the template name and description can be modified. |
| A new feedback request is expected to use an Inactive template | Stop; inactive templates can't be used to create feedback requests. |
| A questionnaire change or deletion is requested for a template that is in use | Stop; change the questionnaire or delete the template only when it isn't in use. |
| Existing-template identity is missing, partial, or ambiguous | Stop; require one stable ID or exact name and resolve exactly one current template. |
| A questionnaire is missing, unsuitable, or unresolved | Stop; resolve readiness through the questionnaire provider without creating or maintaining a questionnaire here. |
| Performance-goal feedback has an unresolved questionnaire | Stop; require target-tenant provider evidence for the unique intended active/latest questionnaire; do not hard-code or substitute an identifier. |
| Requested Redwood, goals, notification, TDS, VBS, or security behavior is unverified | Stop the dependent recommendation, preview, or activation plan; record the missing target-tenant evidence and use the active workflow's authorized provider route. |
| Performance Goal Feedback activation could affect another template | Stop before mutation; show the current active-template evidence and exact impact, then obtain fresh approval for the immutable preview. |
| A template, profile, role, page, or notification behavior differs from the reference | Classify as transport or environment evidence mismatch; record the tenant/release evidence and follow current Oracle documentation and the task contract. |
| Template FSM/CSV import/export, HDL/HSDL, or Data Loader is requested | Return `UNSUPPORTED_EXECUTION_CHANNEL`; do not execute or silently switch to a REST write. |
| A task-declared REST create or update is requested | Use the REST contract only after its exact target, identity, questionnaire, manager-type, lifecycle, payload, and approval gates pass. |
| A tenant-specific REST route lacks capability evidence or a fresh compatible collection GET | Apply all applicable alternatives in ora_reference_lookups.md; stop only the dependent preview/write if still unresolved. Ask for owner confirmation only when explicitly required by policy; no import/export fallback exists. |
| A REST preview has no RFC 8785 JCS SHA-256 digest or the stored digest cannot be reproduced from the preserved canonical payload | Stop before approval or write; regenerate the preview with the declared canonicalization. Mark historical requests with unavailable canonical bytes as unverifiable rather than claiming a digest match. |
| A REST delete or other undeclared REST operation is requested | Stop; Feedback Templates declares no REST delete or other operation contract. |

## Error Classifications

Before escalation, persist the attempted declared reads, returned facts,
missing fields, alternatives evaluated, and exact remaining dependency.
Missing optional metadata is not a negative state. A zero-row secondary
questionnaire query does not invalidate an independently complete eligible
LOV result; conflicting or explicitly ineligible evidence does.
Use `RESOLVED`, `CUSTOMER_DECISION_REQUIRED`, `SKILL_LIMITATION`, or
`VALIDATION_FAILED` as the resolution outcome alongside the failure class.
Continue independent tasks. Do not ask consultants to retrieve ordinary
technical evidence that the declared workflow can obtain.

For Questionnaire metadata failures, distinguish observed transport facts from
diagnosis. An HTTP 200 with zero attachment attributes proves only that the
query returned no attributes. Establish whether the component is requested or
required and whether the failure came from inspection, sample synthesis or
actual import validation. A helper exception alone does not establish
catalog_mismatch or a required Business Object Attribute Update. Recommend
tenant remediation only when the owning provider has evidence that the
required target contract is defective. Otherwise report the exact upstream
limitation without promising that excluding an optional component fixes import.

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required questionnaire is absent or a needed template is not Active. | Correct the template details and validate again. |
| Design blocker | An in-use or inactive-template restriction applies. | Follow the documented template lifecycle restriction. |
| Identity resolution | A template does not resolve exactly once. | Obtain a stable ID or exact name and repeat the provider-backed read. |
| Dependency readiness | Questionnaire readiness or state is unknown. | Resolve and validate without performing questionnaire CRUD here. |
| Contract gap | An undeclared REST operation or unsupported execution channel is requested. | Stop that operation and explain the declared REST-only template scope. |
| Authorization or privilege | The declared target GET returns 401/403, or the approved POST/PATCH returns 401/403. | Stop with auth/authz diagnostics. A denied write retains its attempt marker and is never retried automatically; do not infer write access from a role name or request an unavailable privilege receipt. |
| Approval blocker | Activation, REST mutation, overwrite, or retry lacks current approval for its exact effect. | Stop until fresh explicit approval is available. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Planning review | Questionnaire requirement, requested status, template use status, requested change, and any lifecycle restriction. |
| Execution request | The missing source-backed execution contract and the safe next action. |
| Tenant discrepancy | The exact target-tenant evidence, current Oracle documentation consulted, task-contract constraint, and recommended next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| External catalog advertises CSV/export/import support | Record `catalog_mismatch`; this task remains REST-only. Stop any downstream handoff requiring FSM/Data Loader. |
| REST operation is absent, disabled, or uses a different target path | Do not POST, PATCH, DELETE, retry, or substitute a captured tenant-specific path. |
| Active template is in use | Do not propose changing its questionnaire. |
| Template is in use | Do not propose deleting it or changing its questionnaire. |
| Runtime HDL/HSDL or REST is discussed | Do not treat FeedbackRequest transaction support as permission to configure Feedback Templates. |
| Tenant lookup contract is TBD | Do not perform or imply a Fusion lookup from this task-local guidance. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RETURN_ISSUES | terminal | 30 | terminal | none | none | stop | Input validation or a documented design check fails, or applicable declared evidence alternatives are exhausted. Distinguish CUSTOMER_DECISION_REQUIRED, SKILL_LIMITATION and VALIDATION_FAILED. |
| FEEDBACK_TEMPLATES.DONE | terminal | 40 | terminal | none | FEEDBACK_TEMPLATES.ENFORCE | stop | All applicable documented checks pass. |
