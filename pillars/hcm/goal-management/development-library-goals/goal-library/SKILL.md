---
skill_id: "hcm.goal-management.development-library-goals.goal-library"
name: "Goal Library Setup Task Guidance"
description: "Provides task-specific setup guidance for Goal Library under the Development Library Goals functional area."
layer: "pillar"
pillar: "HCM"
offering: "Goal Management"
functional_area: "Development Library Goals"
functional_area_code: "ORA_DEVELOPMENT_LIBRARY_GOALS"
task_code: "HRG_MANAGE_GOAL_LIBRARY"
task_name: "Goal Library"
parent_skill_id: "hcm.goal-management.development-library-goals"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM goal management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "goal_management_execution_control"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
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
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/development-library-goals/goal-library/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/development-library-goals/goal-library/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: []
---

# Development Library Goal Setup Task Guidance

## Goal Library variant routing

This is the Development Library Goals variant of the shared Goal Library task.
After its own feature and metadata preflight, route it by this manifest's exact
functional area rather than by the shared task code or task name alone.

## Purpose

For create-status intent and post-create activation decisions, follow
[the lifecycle follow-up contract](../../goal-management-common/lifecycle-follow-up.md).
Before handing off a create or marking its Run Book task complete, persist and
validate that contract's task-level follow-up record for the verified Development
goals. If source status was omitted and creates are inactive, state the
activation-or-retain-inactive choice in the handoff; do not silently close it.

Before a preview, use the offering-owned Goal Setup Field Resolution support
package at `pillars/hcm/goal-management/goal-management-common/goal-setup-field-resolution/README.md`
for natural-language Library Goal requirements. Goal Name is the required
business input; all other fields are optional unless current metadata requires
them. A supplied qualifier may map to any supported writable field only after
one field/LOV match; otherwise ask for the target field.

Accept a `confirmed` proposed Goal Name as a normal create value. Never send a
`proposed` or `naming_decision_required` name in a configuration preview.

Support `get`, `list`, `search`, `create`, `update`, `activate`,
`inactivate`, `delete`, `list_translations`, `update_translation`,
`read_decimal_weight_policy`, `csv_export`, and `csv_import` for Development
Library Goals. Treat every request as the development variant; do not accept a
caller-supplied variant that asks for another product branch.

Execute item and read-only advanced-search requests through the core REST
client without write approval. Do not use Chrome as a data transport.

## Best-practice context

Consult sections 2-7, 11, and 17 of the [HCM Goal Management best-practice
reference](../../goal-management-common/best-practice-rules/hcm-goal-management/README.md)
for Career Development and Profile Management prerequisites, scope, inactive
staging, copied-goal behavior, restrictions, outcomes, LOV/search
configuration, and lifecycle checks. The reference is advisory: current Oracle
documentation, target-tenant metadata, and this task contract govern the
`DEVELOPMENT` variant, payload, approval, and validation rules.

## Greenfield HDL DAT route

FSM CSV import remains a setup-data route and must not be used to create a
new Development Library Goal. Enter HDL only when the Goal Management router
returns `hdl_generate` or `hdl_dat_preflight`; otherwise retain REST as the
normal-volume default. For `hdl_generate`, resolve and validate every business
row first, including the same required-field, defaulting, duplicate, type,
status, audience/availability, restriction, date, key, and relationship rules
used by REST. Then pass the rows to `core.data-loader` to generate a current
target-metadata source and immutable ZIP. The consultant need not supply a DAT.
For `hdl_dat_preflight`, preserve and validate the supplied source. Follow
`pillars/hcm/goal-management/goal-management-common/hdl-source-generation.md`; no validation
failure is waivable in either mode.

For root-only Library Goal creates in these two HDL routes, execute the
`Deterministic Library Goal create resolver (HDL only)` procedure in
`../../goal-management-common/hdl-source-generation.md`. Use `hdl_dat_preflight.py --requirements`
with `profile=development_library_goal`; its local JSON catalog and owner policy
resolve technical fields and owner selection without asking the consultant.
Read the catalog/schema/policy through that resolver, validate against the full
live template, and pass the resulting validated fragment to Core Data Loader.
Do not use this resolver for REST or other flows. The existing resolved-context
preflight remains authoritative for updates and multi-component bundles.

Require `ContentItem.dat`; `ContentItemTranslation.dat` is optional.
`ContentItemRelationship.dat` is optional but required to link supplied
`GOAL_MEASUREMENTS` rows to a `GOAL` row. Require local corruption, encoding,
`METADATA`, field-count, mandatory-field, source/user-key, relationship, and
operation checks. Require `ContextName=GOAL` for the library goal and the
current-template field mapped to `DEVELOPMENT`. Current target-tenant Content
Item template, context, value-set/lookup, relationship, and supplied-language
evidence are prerequisites. When `ContentItemTranslation.dat` is supplied,
validate every translation against a package or confirmed target parent, the
target base language, enabled languages, and current translation template.
Reject orphan, duplicate-language, disabled-language, and base-language rows.
`core.data-loader` owns archive creation, preflight, preview, approval, upload,
and reconciliation; do not replace that route with FSM, REST, or browser data
entry.

For `hdl_dat_preflight`, before `core.data-loader` can build the immutable preview, run
`pillars/hcm/goal-management/goal-management-common/scripts/hdl_dat_preflight.py` against the
consultant source and internally resolved runtime context. Preserve the source
and enrich a separate prepared copy with target-defined defaults, generated
create source keys, the `GOAL` context, the selected `DEVELOPMENT`
discriminator, and dates only where the target/Oracle contract makes them safe.
Generate the change manifest internally; the consultant never supplies it.
Include an internally generated `validationTime`; evidence is non-waivable when it is later than that
time or older than the allowed window (24 hours by default). Pass the resulting error-free report in
`finalData.hdlValidation` and set `finalData.format=goal-management-hdl-dat`.
After creating the exact immutable archive, `core.data-loader` must add its
SHA-256 as `finalData.archiveSha256` before Task Hook preview. Task preflight
must never fabricate a digest for a future archive.
No validation failure is waivable.

## Variant boundary

The catalog task is `HRG_MANAGE_GOAL_LIBRARY`, and the runtime resource is the
shared `libraryGoals` REST collection. In this Goal Management functional area, the
required discriminator is `TypeCode=DEVELOPMENT`. Map `DevCategoryCode` only
when the user supplies it or current metadata marks it required; do not block
an otherwise valid request because that optional field is omitted. Current
environment describe/OpenAPI must still confirm the requested operation and
updateability. If it contradicts or omits the development fields or operation,
fail closed with evidence.

Do not create or mutate Performance Library Goals in this task. Return a
blocked route message that directs performance requests to the sibling
Performance Library Goals functional area.

## Lifecycle

For explicit REST batch intent, read [REST batch workflow](../../goal-management-common/rest-batch.md).
Reuse this variant's validated create/update bodies and activation prerequisites.
Resolve parent CRUD batch eligibility through the maintained Goal Management
capability resolver plus current Library Goal describe methods. Do not require a
`batchEnabled` field on the collection or reuse the search action's flag. Default
transport and HDL batch upload routing remain unchanged.

Before any mutation preview, require an `allowed` Goal Management execution
control whose exact task identity, Development Library Goals functional area,
sequence, skill path, and approved plan fingerprint match this task. A direct
instruction to create or activate a Development Library Goal does not override
an earlier unfinished Run Book task. Missing, stale, stopped, or mismatched
control returns `BLOCKED` before target lookup or payload preparation.

For automated create, preserve a supplied `GoalExternalId` exactly and validate
it against its current metadata maximum length; never silently alter it. When
it is too long, present compliant suggestions and require user selection before
rebuilding the preview. When `GoalExternalId` is omitted and current metadata
has `hasDefaultValueExpression=true` for both `GoalId` and `GoalExternalId`,
omit both fields from the create payload, use exact `GoalName` plus
`TypeCode=DEVELOPMENT` duplicate controls, disclose that Fusion derives
`GoalExternalId` from generated `GoalId`, and verify the two returned values
match after create. If that metadata condition is absent, use exact duplicate
controls and require an explicit duplicate-risk acknowledgement; never invent
an ID. Update only explicitly requested values and preserve measures,
tasks, target outcomes, translations, and DFF unless the request changes them.
Use `scripts/library_goal_payload.py` before every create preview. It must
materialize `StatusCode=I`, `Visible=ALL`, and `TypeCode=DEVELOPMENT` into the
exact payload when omitted. These are key create invariants, not optional
omissions. Never preview, submit, verify, or complete a create with a null
lifecycle or role audience. `AvailableTo` is read-only verification output;
`Visible=ALL` must verify as “HR specialist, manager, and worker.”
Activation and inactivation have separate approvals. Prefer inactivation when
references cannot be proven absent; delete requires zero-reference evidence and
separate approval. Re-read and verify after every approved write.
For status changes, call `build_status_update_preview` with the fresh returned
opaque Library Goal item path and current operation contract. Do not require or
infer an ADF batch root when current metadata advertises an item PATCH. For
multiple updates, call `build_update_execution_preview`: one approval group may
contain any positive number of fully resolved operations, while the helper
selects PATCH or an explicitly batch-enabled ADF contract independently from
approval wording. Never construct a composite item URL. Bind the internal
fingerprint to environment, ordered operations, resolved requests, identities,
preconditions, and payloads. After create, compare every approved
field—including description, dates, and scope—not only status and visibility.
An HTTP 201 is not completion. The fresh created row must match Goal Name,
TypeCode, StatusCode, Visible, Available To meaning, and every approved scope
field. A null or mismatched key value returns `INVALID_CREATED_STATE`, blocks
Run Book completion, and must not trigger an automatic replacement create.

Translation operations are development-goal operations. Resolve the trusted
current translation runtime root from current `describe.openapi` resources
`libGoalTranslations` and `libGoalTaskTranslations`. Patch only explicit
translated fields, preserve the base-language parent, and never persist a
tenant runtime revision, composite key, or ETag. The decimal-weight policy is
obtained only through the external Profile Options capability
`core.fusion-api.apps-common.profile-options`; this task must return
`PROVIDER_SKILL_UNAVAILABLE` when that provider cannot be discovered.

## Outcomes

Return exactly one of `READ`, `CREATED_INACTIVE`, `UPDATED`, `ACTIVATED`,
`INACTIVATED`, `DELETED`, `CSV_READY`, `NO_CHANGE`, `MISSING`, `BLOCKED`,
`FAILED`, or `UNKNOWN_AFTER_SUBMISSION`.

## Business duplicate comparison

Before any HDL or standard create, follow [the shared duplicate identity contract](../../goal-management-common/duplicate-identity.md). Use its executable helper for candidate comparison and incoming-row checks. An exact name within Development type is a duplicate regardless of dates.
