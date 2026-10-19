---
skill_id: "hcm.hcm-tool.profile-rating-model-configuration"
name: "Profile Rating Model Configuration"
description: "Provides guidance, questionnaires, and fillable intake templates for one Oracle HCM Profile Rating Model, or translates a plain-language workforce rating outcome into one reviewed model that can be validated, reused or created, read back, and handed off to Profile Management, Performance Management, Talent Review and Succession, Compensation, or Skills Center. Use for requests about rating-model guidance, a workbook or template to complete, employee proficiency ratings, calculated performance ratings, talent reviews, compensation calibration, or skill progression. Also accept expert JSON or workbook requirements. Do not activate for a generic template request with no Oracle HCM rating-model or rating-scale context, update or delete an existing model, or configure downstream consumers."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Profile Rating Model Configuration"
functional_area_code: "CUSTOM_PROFILE_RATING_MODEL"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "HCM Profile Management pillar team"
version: "0.4.0"
inputs:
  - "project_id"
  - "request_mode"
  - "fusion_environment_context"
  - "business_intent"
  - "workforce_context"
  - "effective_date"
  - "business_exceptions"
  - "rating_model_request"
  - "requirements_source"
  - "template_consumers"
  - "template_level_count"
  - "technical_overrides"
  - "reuse_preference"
  - "execution_intent"
  - "completion_mode"
  - "specialist_approval"
outputs:
  - "profile_rating_model_guidance"
  - "fillable_rating_model_template"
  - "business_intent_summary"
  - "consumer_resolution"
  - "configuration_assumption_ledger"
  - "business_configuration_proposal"
  - "intake_recommendation"
  - "rating_model_requirements_workbook"
  - "normalized_rating_model_requirements"
  - "requirements_validation_result"
  - "existing_model_suitability_result"
  - "reuse_or_create_decision"
  - "rating_model_configuration_blueprint"
  - "immutable_creation_preview"
  - "creation_or_reuse_result"
  - "data_load_monitoring_result"
  - "readback_comparison"
  - "ui_verification_guidance"
  - "consumer_handoffs"
  - "human_friendly_outcome_summary"
  - "implementation_summary"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
  - "shared.validation.setup-data-validator"
  - "core.data-loader"
  - "core.fusion-api.apps-common.profile-options"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.apps-common.profile-options"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run_and_artifact"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "requirements"
  - "setup_task_sequence"
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "requirement"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-rating-model-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-rating-model-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-rating-model-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-rating-model-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
oracle_supplied_guidance_files:
  - purpose: "Rating-model request and workbook validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Profile option, privilege, read, and Data Loader readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Exact current-environment rating-model lookup"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Consumer-derived component defaults"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "V1 design, reuse, and no-update enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Failure classification, disclosure, and retry refusal"
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status:
  source_alignment: "GROW-8116, approved HCM Tool taxonomy and baseline, FA Latest rating-model documentation, and targeted 2607/2607.5 Profile Management source evidence"
  execution_contract: "REST is read-only and capability-gated through a source-backed API version and bounded structured request; the quarterly release label is optional metadata and is never user-required; creation uses core.data-loader through a verified current FSM or Rating Model HDL contract; unlisted talentRatingModels writes are prohibited"
required_setup_tasks:
  - "HRT_MANAGE_PROFILE_RATING_MODELS"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "May generate a standalone fillable guidance workbook without accessing Fusion or requiring an implementation project."
  - "Creates requirements, workbook, validation, blueprint, decision, handoff, report, run, and token-usage artifacts in the selected project workspace."
  - "May read the effective Redwood profile option and Profile Rating Models through approved core skills after route-specific preflight."
  - "May prepare a current FSM or Rating Model HDL source through core.data-loader after requirements and reuse validation."
  - "May initiate one approved creation-only import through core.data-loader after its immutable-preview approval; no direct REST write is permitted."
  - "May perform bounded read-only Data Loader status monitoring and structured rating-model read-back after an approved creation submission."
required_privileges:
  - "HRT_MANAGE_TALENT_PROFILE_RATING_MODEL_PRIV for the source-backed Profile Rating Models UI and REST resource in releases where no separate read privilege is published."
  - "The current Data Loader roles and privileges required for the selected FSM or Rating Model HDL route."
  - "Profile-option read access only when the Redwood UI route is selected."
---

# Profile Rating Model Configuration

## Purpose

Provide no-Fusion guidance and a fillable requirements template when that is
all the user requests. For implementation, start from the workforce outcome the
user wants to enable, resolve the relevant rating-model consumers and comparable
setup, and propose one consistent Profile Rating Model without making the user
name Fusion objects or technical fields. After business review, own the reusable
model header, ordered levels, and applicable review points, ranges, categories,
direct Compensation distributions, and translations. Hand downstream
associations and consumer setup to their owning skills.

## Catalog Identity Migration

The effective HCM Tool catalog names this functional area **Profile Rating
Model Configuration**. Its canonical repository identity is therefore
`hcm.hcm-tool.profile-rating-model-configuration` at
`pillars/hcm/hcm-tool/profile-rating-model-configuration/`.

When resuming an existing project, inspect the legacy artifact location
`project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-rating-model/current/`
only if the canonical location has no current artifact. Treat a legacy artifact
as prior history for this same implementation responsibility, preserve its
version and provenance, and persist all new or updated outputs under the
canonical location. Do not rename, delete, or overwrite legacy project
artifacts automatically.

## Read Order

1. Read [business-first intake and proposal](references/business-first-intake-and-proposal.md) for every conversational request.
2. Read [consumer requirements and handoffs](references/consumer-requirements-and-handoffs.md) while resolving consumers or technical components.
3. Read [the requirements workbook contract](references/profile-rating-model-requirements-workbook.md) for workbook generation, upload, validation, or customer-spreadsheet mapping.
4. Read [source and documentation evidence](references/source-and-documentation-evidence.md) before changing a release-sensitive route or rule.
5. Before validation, preview, or execution, read [the task-node guide](references/task-node-execution.md), select the exact Profile Rating Models entry in `ora-resource/ora_rule_registry.json`, and verify readiness `ready`, graph edges, and source anchors. Stop on any other status.
6. Load `ora-resource/ora_error_handling.md` before preview or any live operation.

## Fixed V1 Boundary

- Process exactly one rating model per request.
- Reuse one exact suitable model or propose one new model.
- Never update or delete an existing model, level, category, review point,
  distribution, or translation.
- Never create downstream template, plan, content-section, profile-type,
  subscriber, meeting, assessment, or Skills Center association.
- Never write through the unlisted `talentRatingModels` REST resource or its
  batch endpoint.
- Use `core.data-loader` for every FSM or HDL import. Its immutable-preview
  approval is the single specialist approval immediately before creation; do
  not add a second approval for the same exact artifact.
- Treat an implementation request as `end_to_end` completion by default. After
  the one approved submission, continue through bounded read-only Data Loader
  monitoring and structured rating-model read-back. Stop at initiation only
  when the user explicitly chooses `submit_only`.
- Stop when current FSM or Rating Model HDL metadata doesn't prove the required
  component hierarchy and attributes.

## Guidance and Fillable Template Mode

Select this mode when the request asks for Profile Rating Model guidance, a
questionnaire, an intake workbook, a blank or fillable template, or something
to complete and return. Rating-model context may be explicit in the request or
already established in the conversation. Do not claim this skill for a generic
request such as “give me templates” when no Oracle HCM rating-model or rating-
scale context exists.

This mode is an offline assisted deliverable, not implementation preflight:

- Give concise completion guidance covering business purpose, intended
  population or process, effective date, intended uses, scale direction, level
  meanings, languages, exceptions, and downstream ownership.
- Generate the workbook immediately without requiring complete requirements,
  an initialized project, Fusion environment, login, quarterly release,
  privilege check, discovery call, runbook, or approval.
- Infer consumers from stated business use when one interpretation is materially
  stronger. When consumers remain unknown, generate the universal template with
  all conditional sheets clearly optional instead of blocking delivery. Ask one
  business-use question only when the user specifically requests a tailored
  template and the answer changes its sheets.
- Use only synthetic examples in the workbook. Do not read Fusion, inspect
  existing models, or imply that an example is the user's approved design.
- Save to an explicitly requested writable location. Without one, use a local
  downloadable delivery location; do not create an implementation project only
  to hold the template. If the user already selected a project and requests
  persistence, save and register it under this skill's normal artifact path.
- State that template generation is complete but implementation readiness is
  not evaluated. When the completed workbook is returned, validate it through
  the normal requirements workflow; only then may discovery, reuse, blueprint,
  preview, approval, or creation begin.

Generate an unscoped universal template:

```bash
python3 scripts/profile_rating_model_requirements.py generate-template \
  --output <writable-directory>/profile-rating-model-intake-template.xlsx
```

For a consumer-tailored template, add one `--consumer <supported-consumer>` per
resolved consumer. Optionally use `--level-count <n>` to create a different
number of fillable scale rows; the default is five. Do not run `generate` with
invented placeholder requirements as a substitute for `generate-template`.

## Business-First Interaction Contract

Start with what the user wants the workforce or business process to accomplish.
Do not begin by presenting a list of Fusion consumers, asking the user to choose
a skill, or requesting model code, component names, import routes, review-point
fields, categories, distributions, or downstream object names.

Accept either:

- a plain-language business statement containing the intended outcome,
  workforce or process context, effective date, and any explicit exception; or
- a complete expert JSON, generated workbook, or reviewed customer workbook.

For a plain-language request, infer the likely consumer or consumer union,
perform only workflow-declared read-only discovery, and create one proposal
whose technical values have source and confidence evidence. Ask one concise
business question only when the missing decision changes the scale's business
meaning, intended use, population, effective timing, or reuse-versus-new result.
Do not ask the user for a technical value that one supported pattern, documented
default, or deterministic naming rule can safely propose for review.

Preserve every explicit technical value supplied by an expert. Expert input
does not bypass discovery, validation, exact-reuse, preview, or approval gates.

## Input Timing

- At intake, require only project/environment context when the workflow needs
  it, the business intent, workforce or process context, effective date, and
  stated exceptions.
- After discovery, collect technical overrides only when the user chooses to
  inspect or correct the proposal; otherwise derive them with provenance.
- Collect `requirements_source` and a normalized `rating_model_request` when
  the proposal is confirmed or an expert source is supplied.
- Default `completion_mode` to `end_to_end` without asking. Set it to
  `submit_only` only when the user explicitly asks not to wait or verify.
- Collect `specialist_approval` only from the later standalone
  `core.data-loader` immutable preview. Never request it during business intake
  or proposal review.

## Consumer Resolution and Intake Path

Resolve Profile Management, Performance Management, Talent Review and
Succession, Compensation, or Skills Center from the user's business language
using the business-first reference. Do not claim that a rating model is used by
a consumer unless the user, a current project decision, or an approved owning
skill's evidence establishes that relationship. Model data alone establishes
scale similarity, not downstream association.

Derive the union of resolved consumer requirements, identify which consumer
requires each component, and stop only when a material conflict or multiple
equally supported interpretations remain after discovery. Recommend a tailored
workbook for multilingual, calculated, category-based, distribution-based,
detailed, or multi-consumer requirements. Generate the workbook whenever the
consultant asks for it, regardless of the recommendation.

## Requirements Workbook

Use the deterministic helper; don't hand-build workbook XML or invent sheets:

For a guidance/template-only request, use `generate-template` as described
above. It deliberately accepts incomplete input and must not be represented as
an implementation validation result.

```bash
python3 scripts/profile_rating_model_requirements.py generate \
  --input <requirements.json> \
  --output <project-artifact-directory>/profile-rating-model-requirements.xlsx
```

Validate normalized JSON or a completed generated workbook:

```bash
python3 scripts/profile_rating_model_requirements.py validate \
  --input <requirements.json-or-xlsx> \
  --output <project-artifact-directory>/requirements-validation.json \
  --normalized-output <project-artifact-directory>/normalized-requirements.json
```

Inspect an existing customer workbook before mapping it:

```bash
python3 scripts/profile_rating_model_requirements.py inspect-mapping \
  --input <customer.xlsx> \
  --output <project-artifact-directory>/workbook-mapping-review.json
```

Treat uncertain, ambiguous, or missing mappings as blockers. Preserve the
uploaded source and prior validated requirements according to project policy;
create a new artifact version for material correction or resubmission.

## Preflight

Before a live read-only discovery or exact-model lookup:

1. Validate project/request identity, one-model scope, a sufficient business
   outcome, workforce or process context, requested effective date, and safe
   local output paths. Technical model fields need not yet be complete for
   discovery.
2. Resolve and display the exact authenticated Fusion environment through the
   active core authentication context. Ignore hosts embedded in supplied links.
   A user-typed hostname, browser address bar, screenshot, or manually supplied
   quarterly release is not sufficient environment evidence. Record the
   quarterly release and its source only when trusted core context or supported
   target metadata already supplies it; otherwise leave it unknown without
   asking the user or blocking this read-only preflight.
3. Select only a source-backed REST API version and path, then use the first
   bounded structured request through the declared core REST client as the
   target capability and effective-access probe. Do not derive a quarterly
   release such as 26C from the REST API version, documentation URL, hostname,
   or calendar date. A successful request proves the required read capability
   and access only for that call; it does not prove the quarterly release, role
   membership, or write access. Discovery is not permission for a write.

Before preview, import, or polling:

1. Validate the confirmed business proposal, assumption ledger, resolved
   consumers, source version, normalized requirements, workbook mappings, and
   local output paths.
2. Verify the current Data Loader roles and privileges, resolve the task catalog
   flags, and prove the current FSM package or Rating Model HDL component
   hierarchy and attributes. Fail closed on absence, ambiguity,
   incompatibility, or unsupported fields.
3. Validate the complete proposed configuration, source/ZIP shape, artifact
   digest, exclusions, consumer handoffs, and read-back assertions.
4. Require the normal `core.data-loader` immutable-preview approval immediately
   before one creation import. Approval is invalid after any target, metadata,
   requirement, source byte, digest, or assertion changes.

Classify a failed preflight as `input_validation`,
`catalog_or_metadata_mismatch`, `auth_expired_or_invalid`,
`authorization_or_privilege`, `transport_or_environment`,
`artifact_persistence`, or `approval_blocker`. Persist a sanitized diagnostic
and stop without switching routes.

## Verification Evidence Contract

- Never require or request a screenshot, browser page, address-bar image, or
  exact user reply as proof of environment identity, UI access, REST access,
  reuse, creation, or completion.
- Do not direct the user to open Setup and Maintenance, select Go to Task, or
  navigate to Profile Rating Models as a substitute for a missing workflow
  capability. Browser and manual-UI navigation are not execution or
  verification routes for this skill.
- This restriction does not prohibit optional UI-verification help in the final
  result. Label that help as supplemental, keep it outside workflow gates, and
  never require the user to perform it or return evidence.
- Treat an unsolicited screenshot or manual UI observation as supplemental,
  unverified context only. Do not mark a gate passed from it, make it a required
  project artifact, or persist environment, tenant, employee, or customer data
  from it.
- Establish environment identity from the active authenticated core context and
  the declared target. Establish effective read access only from a successful
  requested call through the supported read-only contract. Use an authorized
  role-access result only when its owning core skill exposes executable,
  source-backed evidence; otherwise do not claim role assignment.
- Do not ask the user to provide or confirm the quarterly Fusion release during
  read-only preflight. Record it only when trusted core context or supported
  target metadata already provides both the value and its source. An unknown
  quarterly label does not block a source-backed capability probe, and a REST
  API version such as 11.13.18.05 is not a quarterly release such as 26C.
- For exact reuse or post-import completion, use
  `verify_rating_model_result` to record expected, observed, unavailable, and
  different values from a fresh structured read-back. Loader status, UI access,
  user attestation, and screenshots cannot replace that comparison.
- If the authenticated environment, supported read contract, effective access,
  or required read-back coverage cannot be established through the declared
  route, return blocked, incomplete, or failed as applicable. Do not invent a
  manual proof step.

## User-Facing Outcome Contract

The final response belongs to this Profile Rating Model skill. A compact result
returned by `core.data-loader` is supporting technical evidence, not a complete
business outcome by itself. Do not return only a generic loader statement and
its Data Set Name, Content ID, and Request ID.

Lead with one short, human-readable outcome paragraph using the reviewed
proposal, blueprint, execution result, and verification evidence. Include the
known model name and code, intended business use, scale summary, effective
date, target environment for a live operation, and whether downstream
association remains outside this skill. Omit unavailable details instead of
inferring them from an archive name or server identifier.

State the lifecycle result precisely:

- **Guidance or template delivered:** say what was prepared and that no Fusion
  read or write occurred.
- **Proposal or preview ready:** say the model is prepared for review or
  approval and that nothing was submitted.
- **Exact model reused:** say which existing model was verified as an exact
  match, that no model was created or changed, and which downstream owner must
  associate it.
- **Creation initiated:** use this result only for explicit `submit_only` or a
  monitoring timeout. Say the approved model was submitted for processing and
  Fusion accepted the request, but creation or verification is not yet
  confirmed.
- **Created and verified:** use this result only after successful loader status
  and the fresh structured read-back in step 12 match the approved blueprint.
- **Blocked, failed, partial, timed out, or unverified:** say plainly that the
  requested model is not confirmed ready, identify the affected stage, and
  give one actionable next step without implying that creation succeeded.

After the business outcome, show only the useful technical receipt or evidence
in a compact secondary section. For an accepted Data Loader initiation,
preserve the exact Data Set Name, Content ID, and Request ID returned by
`core.data-loader`. For `end_to_end` completion, continue through the separate
post-submission monitoring request below. For `submit_only` or timeout, offer a
later status check as the next action. Do not create a separate summary file
unless the workflow already requires the implementation summary as a durable
project artifact.

For example, an explicit submit-only or timed-out job-profile
proficiency-model load should read like:

> Your five-level Job Profile Proficiency rating model was submitted to the
> approved Fusion environment for creation with the reviewed effective date.
> Fusion accepted the data-load request, but processing is asynchronous, so the
> model is not yet confirmed as created or verified. Job-profile association
> remains a downstream Profile Management step.

Follow that paragraph with the compact loader receipt and one next action.

## Optional UI Verification Guidance

For a live exact-reuse, creation-initiated, created-and-verified, or
verification-failed outcome, add a compact **Verify in Fusion UI (optional)**
section after the business outcome and technical evidence. This is convenience
guidance for a human reviewer; it is not a preflight step, execution route,
approval gate, or replacement for structured read-back.

Build the section from trusted run evidence:

1. Add an **Open Fusion** link using only the exact authenticated environment's
   verified base URL, such as `https://<verified-host>/`. Strip paths, query
   parameters, fragments, control-state values, and other session data. If a
   trusted base URL is unavailable, name the verified environment alias and
   omit the link rather than constructing one from user text or a screenshot.
2. Tell the user to open the **Profiles** work area and select **Profile Rating
   Models**. As an alternative, they can open **Setup and Maintenance**, search
   for **Profile Rating Models** (`HRT_MANAGE_PROFILE_RATING_MODELS`), and
   select **Go to Task**. Do not provide an environment-specific deep link to
   the task page.
3. Tell the user to search by the exact approved model code first, with the
   rating name only as secondary context. Include those two values directly in
   the instructions instead of making the user recover them from a loader
   receipt.
4. Generate a short comparison checklist from the approved blueprint and
   read-back coverage. Always include code, rating name, effective dates, and
   ordered rating levels. Include numeric ratings, review points and ranges,
   categories, distributions, or translations only when they apply to that
   model. Do not ask the user to inspect unrelated fields.
5. For `submitted_not_verified`, explain that the model may not appear until
   processing succeeds and that absence during processing is not proof of
   failure. For `created_and_verified` or exact reuse, state that the optional
   UI review should agree with the structured result already reported.
6. If the user notices a difference, tell them to report the field and observed
   value so the declared structured read-back can be rerun. Do not ask for a
   screenshot, downgrade the existing evidence solely from an unverified UI
   observation, edit the model, or replay creation automatically.

Include these stable Oracle help links in the optional section:

- [How to Create a Rating Model](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/how-to-create-a-rating-model.html)
  for the documented Profiles-work-area navigation and page layout.
- [Rating Models](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/rating-models.html)
  for model concepts and supported components.

Add component-specific links only when the corresponding component is present
in the approved blueprint:

- [Rating Levels](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/rating-levels.html)
- [Review Points](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/review-points.html)
- [Rating Categories](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/rating-categories.html)
- [Distributions](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/distributions.html)

## Post-Submission Monitoring and Verification

An approved implementation request is end-to-end unless the user explicitly
asks to submit without waiting. Before showing the immutable Data Loader
approval preview, disclose that an affirmative submission reply will be
followed by bounded read-only status checking and structured rating-model
read-back. Keep the normal `core.data-loader` submission approval question
unchanged. This disclosure makes status, results, and verification an explicit
part of the parent skill request; it does not broaden the one-time mutation or
authorize a retry.

The initiating `core.data-loader` operation must still end immediately after
its accepted initiation receipt. The Profile Rating Model parent then starts a
new, status-only `core.data-loader` child request using the returned Request ID.
This is a separate declared status request, not automatic polling inside the
initiating Data Loader operation.

For `end_to_end` completion:

1. Poll no more frequently than every 15 seconds for at most 20 minutes. Use
   the current parent run's remaining time when it is shorter. Keep the user
   informed at least once per minute while the request remains active.
2. On each check, use the complete `core.data-loader` status contract. Treat a
   missing data-set record or an active nonterminal result as still processing.
3. Treat the load as successful only when the Data Loader result is terminal,
   reports no failed objects, and returns no actionable errors. A failed,
   partial, completed-with-errors, canceled, or uncertain result stops without
   replaying the submission.
4. After terminal loader success, perform the fresh structured read-back in
   step 12 and compare every exposed material field with the approved
   blueprint. Do not substitute loader status for this comparison.
5. Return `created_and_verified` only when both terminal loader success and the
   structured comparison pass. If the load succeeds but read-back is missing,
   incomplete, or different, return `load_completed_verification_failed` with
   the differences and one reconciliation action.
6. On monitoring timeout, persist the Request ID, last observed status, elapsed
   time, and safe resume stage. Return `submitted_not_verified`; never submit
   the archive again automatically.

For explicit `submit_only`, return after the accepted initiation receipt with
`submitted_not_verified`. Make clear that the user selected submission without
waiting and that a later status and read-back request is required for verified
completion.

## Workflow

The following execution spine applies only after the user requests
implementation or returns a completed template. Guidance/template-only mode
ends after delivering its guidance and workbook.

Execution spine: intent → discovery → proposal → technical validation → exact
comparison → dependency/design gates → Data Loader preview or exact reuse →
approved submission → bounded monitoring → structured read-back → handoff.

### 1. Establish project and request identity

Require an initialized `project_id`, exact environment identity for live reads,
and one `create_or_reuse` request. Reject update, delete, bulk multi-model, and
downstream-configuration requests. Route configuration migration to
`core.data-loader` under this task's FSM or Rating Model HDL contract.

### 2. Capture the business intent

Summarize the desired workforce outcome, intended population or process,
effective date, stated scale meaning, and exceptions in business language. Do
not ask the user to identify a consumer, rating-model component, task, skill,
or loader route. When outcome, population or timing is genuinely unclear, ask
only for that missing business decision.

### 3. Resolve consumers and discovery scope

Use the business-first reference to form a consumer hypothesis and the union of
potential component requirements. Record each interpretation and its business
evidence. If one interpretation is materially stronger, continue without a
consumer-selection question. If two interpretations would produce different
business behavior, ask one plain-language question that explains the difference.

### 4. Discover comparable patterns

After read-only discovery preflight, use `discover_rating_model_patterns` to
inspect current rating-model patterns and any approved current-project evidence.
Rank patterns by requested effective date, scale meaning, language, naming
convention, and business-use evidence. Never infer a consumer association from
model data alone, and never treat a similar pattern as an exact reuse decision.
Zero patterns permits a review-only proposal based on explicit intent and
documented rules; multiple equally supported patterns require one business
choice.

### 5. Build and review an assumption-led proposal

Preserve explicit values first. Then propose values from one supported scoped
pattern, documented product rules, and deterministic generation in that order.
Record every inferred consumer and technical value in the assumption ledger
with source, confidence, materiality, and review status. Do not block merely
because code, name, descriptions, languages, numeric levels, or optional
components were absent from the initial business statement when a safe
review-only proposal can be produced.

Present a short business summary of what will be enabled, the effective date,
the proposed scale, important exclusions, and any downstream handoffs. Offer
`Prepare model` and `Review assumptions`. Use `Create model` only for the later
immutable `core.data-loader` preview. Business proposal confirmation is not
authorization to import.

### 6. Confirm and normalize requirements

Apply confirmed assumptions and corrections, or accept a complete expert JSON,
generated workbook, or reviewed customer workbook. Normalize the confirmed
source to the bundled technical JSON schema. Retain proposal version,
assumption provenance, source workbook/version, and cell coordinates in
traceability records. Any correction starts a new proposal version.

### 7. Validate the normalized configuration

Run the helper and task-rule plan. Require model identity, purpose, population,
dates, languages, ordered unique levels, descriptions, and every
consumer-required value only at this stage. Validate numeric progression,
review points and ranges, calculation precision, categories, direct
distributions, translations, and cross-consumer compatibility. Stop until every
blocking technical issue is resolved.

### 8. Search and classify existing models

Use `find_rating_model_by_exact_identity` only after the exact authenticated
environment is resolved and a bounded request proves the source-backed REST API
version, path, required response coverage, and effective access. Do not require
a quarterly release label for this gate. Compare the full material configuration
required by every selected consumer. Classify candidates as exact, close, or
unsuitable. A name-only match is never exact. Multiple possible matches require
specialist selection and cannot proceed automatically.

### 9. Decide reuse or create

Reuse only one exact suitable model. If a model is close but not equivalent,
list every material difference and recommend a new model or a separately
governed impact review; never modify the existing model in V1. If no exact model
exists, build one complete configuration blueprint with only required
components and trace every value to its source.

### 10. Prepare the supported creation source

Keep `dataloader_import_mode: FSM` as the catalog route. Before preparing an
artifact, use `core.data-loader` to confirm the current task/package contract or
the current HCM Data Loader `Rating Model` hierarchy through View Business
Objects. Do not guess the hierarchy, worksheet, DAT component, field, ZIP, or
operation. A missing or incomplete contract is an `approval_blocker` and ends
the run with the blueprint intact.

#### Rating Model HDL source-format guard

When the proven creation route is HCM Data Loader, use the same read-only View
Business Objects result to check the intended root discriminator before asking
`core.data-loader` to generate a source file. Compare unique registered
top-level identities in this order: exact discriminator first, then longer
discriminators that begin with the exact value.

If exactly one `RatingModel` root exists but one or more other registered
top-level discriminators also begin with `RatingModel`, treat a new map-free
XLSX as unsupported for this Profile Rating Model run. This is a predictable
XLSX root-resolution collision, not evidence that the rating-model blueprint or
Fusion business-object metadata is invalid. Detect it before file generation;
do not generate or validate the map-free XLSX and then report Business Object
Validation as failed.

Use an already-proven FSM task/package route when it can represent the complete
blueprint. Otherwise explain the source-format constraint and offer
`Prepare DAT source`. Generate DAT only after the user has clearly and
explicitly requested DAT, whether by that action or equivalent words. A generic
`Prepare model`, `submit`, or approval of the business proposal does not select
DAT. After the explicit DAT request, let `core.data-loader` generate and
validate the exact `RatingModel` DAT source from live metadata; never hand-build
the DAT, rename the root worksheet, add a legacy workbook map, or weaken
business-object validation. If neither a complete FSM package nor an explicitly
requested DAT source is available, stop with the validated blueprint intact and
identify the source-format decision as the only blocker.

### 11. Preview, approve, and create once

Show the confirmed business outcome and proposal version, assumption ledger,
resolved consumers, source requirements/workbook version, validation, search
result, reuse decision, full proposed configuration, exclusions, downstream
ownership, handoffs, environment, operation, artifact digest, and read-back
plan. Invoke the normal `core.data-loader` preview. Only its current standalone
approval for the unchanged immutable artifact authorizes one import. Never
automatically retry a POST, upload, import, loader, or uncertain create.
Treat the returned Data Loader initiation report as the technical receipt for
this child operation. Unless the user selected `submit_only`, do not end the
Profile Rating Model run at this point; enter Post-Submission Monitoring and
Verification as a separate read-only child request.

### 12. Monitor, read back, and compare

After an approved creation, apply the Post-Submission Monitoring and
Verification contract. Once Data Loader reaches terminal success, use the
approved read path to retrieve the saved code, name, description, dates,
levels, numeric values, review points, ranges, categories, direct
distributions, and translations that the current contract exposes. Compare
them with the approved blueprint. Missing read coverage or any difference
blocks verified completion; don't report success from the import status alone.

### 13. Produce handoffs and persist the run

Create one structured handoff per resolved consumer using the reference
contract. Persist the business-intent summary, consumer resolution, assumption
ledger, proposal and review status, normalized requirements, validation, reuse
decision, blueprint, approval/import references, Data Loader monitoring result,
read-back comparison, optional UI-verification guidance, handoffs,
human-friendly outcome summary, implementation summary, skill run, and token
usage. Redact tokens, credentials, opaque URLs, internal IDs, ETags, and
sensitive customer rows.

## Error and Resume Discipline

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_expired_or_invalid`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `approval_blocker`.

Refresh a cache-managed token once after 401 or 403. Do not retry a second
authorization failure. Retry only bounded read-only transport failures. On a
loader timeout, record the environment, operation, task code, ProcessId or
requestId, last status, elapsed wait, and one safe next check. On resume,
revalidate changed evidence and never reuse stale approval.

## Refusal Rules

Ask one business question, then stop before proposal confirmation when:

- the desired outcome, intended population or process, or effective date is
  missing and cannot be derived safely;
- two or more consumer interpretations or scale patterns are equally supported
  and would produce materially different business behavior;
- the scale's direction or level meaning is genuinely ambiguous.

Do not stop initial intake merely because Fusion consumers, model code, name,
description, languages, numeric values, optional components, import format, or
downstream object names were not supplied.

Stop before exact lookup, preview, or creation when:

- a consumer or level meaning/order remains unresolved after proposal review;
- an inferred material value lacks provenance or remains unreviewed;
- a workbook or customer column can't be mapped safely;
- required values, translations, numeric ratings, review points, ranges,
  categories, or distributions are missing or conflicting;
- ranges overlap, contain an unexplained precision gap, or reverse boundaries;
- distribution percentages are invalid or minimum exceeds maximum;
- multiple existing models could satisfy the request;
- the request requires update, delete, or downstream setup;
- no source-backed REST API version and path is available, the bounded read
  capability probe fails or lacks required coverage, or the current FSM/HDL
  contract is absent, incomplete, unlisted for the proposed write, or
  incompatible with observed target capabilities;
- the immutable preview, approval, artifact digest, or environment changed.

Return the unresolved question, affected consumer, source/cell, options,
business impact, supported recommendation, and specialist decision required.

## Setup Task

Use [Profile Rating Models](profile-rating-models.md)
(`HRT_MANAGE_PROFILE_RATING_MODELS`) for catalog identity and setup-data
routing. Task-local validation and readiness rules are under `ora-resource/`.
