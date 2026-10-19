---
skill_id: "hcm.performance-management.performance-template.performance-templates"
name: "Performance Templates Setup Task Guidance"
description: "Provides task-specific setup guidance for Performance Templates under the Performance Template functional area."
layer: "pillar"
pillar: "HCM"
offering: "Performance Management"
functional_area: "Performance Template"
functional_area_code: "ORA_PERFORMANCE_TEMPLATE"
task_code: "HRA_MANAGE_PERFORMANCE_TEMPLATES"
task_name: "Performance Templates"
parent_skill_id: "hcm.performance-management.performance-template"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM performance management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.apps-common.lookups"
  - "core.fusion-api.apps-common.profile-options"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/performance-management/performance-template/performance-templates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/performance-management/performance-template/performance-templates/current/"
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

# Performance Templates Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Performance Templates` under `Performance Template`.

## Setup Task Skill Contract

- task_code: `HRA_MANAGE_PERFORMANCE_TEMPLATES`
- task_name: `Performance Templates`
- parent_skill_id: `hcm.performance-management.performance-template`
- pillar: `HCM`
- offering: `Performance Management`
- functional_area: `Performance Template`
- functional_area_code: `ORA_PERFORMANCE_TEMPLATE`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Performance Templates` under `Performance Template`.

Apply the [Performance Management](../../SKILL.md) Infer First Intake Policy before requesting setup fields. Preserve stated business decisions in the configuration blueprint, use task-declared lookups for reference values, and identify integrations or operating-process requirements as related work rather than as missing template fields.

### Business-decision provenance

Treat a setup choice as confirmed only when the user explicitly selects it or
it was already an established user decision in the supplied conversation.
Current target configuration, a comparator value, or the assistant's own
recommendation is evidence for a review, not user confirmation. When the user
asks to compare candidates before choosing, keep that choice unresolved until
the user answers. Any later blueprint or review-only preview must label the
candidates and the pending decision; it must not promote the current value or
the recommendation to a confirmed choice.

## Setup Task Metadata

- Task name: `Performance Templates`
- Task code: `HRA_MANAGE_PERFORMANCE_TEMPLATES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. After preparing the final FSM archive, run the pillar-local CSV archive
   validator against those exact bytes:

   ```text
   python pillars/hcm/performance-management/performance-template/performance-templates/scripts/validate_performance_templates_csv.py <final-fsm-archive.zip>
   ```

   The command accepts either the final ZIP or its extracted folder. A nonzero
   exit blocks the import: correct the reported CSV members and rows, rebuild
   the archive, and restart validation. Do not run it against a comparator or
   an earlier draft, and do not change the archive after it passes; any change
   requires another validation run.
5. Run the offering-wide foreign-key validation gate described in
   [CSV Import Guidance](../../csv_import_guidance.md), using
   `--task-code HRA_MANAGE_PERFORMANCE_TEMPLATES` and a fresh reference bundle
   that declares every applicable document type, process flow, role, section,
   questionnaire, and other external reference tuple.
6. Import the same validated FSM archive with `core.data-loader`.

Apply the offering-wide [CSV Import Guidance](../../csv_import_guidance.md)
when preparing an import archive.

Use this task metadata when invoking those skills:

- Offering: `Performance Management`
- Functional area / Setup Object: `Performance Template`
- Setup task name: `Performance Templates`
- Setup task code: `HRA_MANAGE_PERFORMANCE_TEMPLATES`

## CSV Export Result Summary

After a successful export, inspect every `*.csv` member in the downloaded ZIP
or extracted folder. Count data rows only, excluding the header row, and exclude
non-CSV files. Include this in the final response with comma-formatted counts:

The ZIP contains **<total> total data records** across its CSV files.

| File | Records |
| --- | ---: |
| `<CSV filename>` | `<data-row count>` |

## Task-declared REST execution route

FSM CSV import remains the setup-data migration route. For an explicitly
requested live Performance Templates REST operation, use the separate
task-declared contract in
[`ora-resource/ora_rest_execution.md`](ora-resource/ora_rest_execution.md) and
[`ora-resource/ora_rest_execution.json`](ora-resource/ora_rest_execution.json).
The route supports target-Describe-validated `GET`, `POST`, `PATCH`, and child
`DELETE` operations and reuses the shared OAuth service and the shared REST
client's single-request primitive. It never invokes Data Loader for a REST
operation and never creates another Run Book.

Run the task-local wrapper with Python 3.10 or newer. A mutation first produces
an immutable preview bound to the exact environment, method, relative path,
headers, payload, Describe bytes, and contract bytes. A later approval must
name that preview's SHA-256. The wrapper verifies the binding immediately
before one request and does not retry a write. Never construct an approval
record from a plan approval or from a general request to perform mutations.

Standard child `DELETE` operations are supported only when the target Describe
declares the item action and the exact parent and child identities are bound in
an immutable preview with later approval. Root standard `DELETE` remains
rejected when its target Describe omits that item action; use only the declared
root custom delete workflow when explicitly requested and approved. Generic
`upsert` remains disabled because an ambiguous create-or-update effect cannot
be bound safely. The task contract has one narrow `section_upsert` route for a
freshly absent section: it binds an existing `TemplateDefnId`, exactly one new
Describe-validated section, one or more nested Describe-validated role actions,
the target collection `upsert` operation, and the service catalog's
`Upsert-Mode: true` header. It requires an exact pre-read and an independent
readback. The executable contract rejects a sparse section that omits
`SectionDefId`, `SequenceNumber`, or the provider-derived `SectionTypeCode`;
it also requires provider-derived section control defaults and each role
action's rating/share/profile defaults to be present, including explicit
`false` and `null` values where applicable. Materialize the selected Section
Definition and role participation as specified in the defaulting rules before
preview. Do not fall back to ad hoc REST or use this route for arbitrary root
fields.

For every nested create, update, or delete, bind each parent identity from the
fresh read's canonical two-component key. Bind an item identity for update or
delete using the key shape declared for that resource: eligibility-profile
items use the scalar `TalentEligibilityProfileObjectId`; other nested items use
their canonical two-component key. A numeric display ID cannot replace a
composite key. The executable contract rejects an incorrect key shape before
preview; never probe and correct the path with a write.

For every standard item `PATCH` or `DELETE`, copy the fresh response's HTTP
`ETag` value exactly into `if_match`, preserving its enclosing double quotes.
The executable contract rejects wildcard and unquoted values before preview;
do not normalize, strip, or reconstruct an ETag. The `atomic_role_delete`
batch is the documented exception: its batch JSON `ifMatch` values use the
fresh raw token without HTTP-header quotes, as described below.

Because Fusion requires roles during root creation, the task contract binds a
single deep-create payload containing target-Describe-validated `roles` rows.
Materialize both the source-validated `RoleId` and `RoleTypeCode` for every
role row; a role ID without its type can be accepted but saved with a null
role type, preventing a compatible process flow from being assigned. That
payload is a new approval artifact. Omit parent-managed keys, generated keys,
and display fields; never reuse approval for a root-only payload.

For a `QUESTIONNAIRE` template section, include the selected Worker
template-role and each template role that will own a period questionnaire
association as section role actions. Then create each period questionnaire
association separately, binding its `TmplRoleId` to a role with access to that
section. Supply `questionnaire_worker_tmpl_role_id` from the fresh template-role
read so the executable section-upsert contract requires Worker access in the
preview.

Template alerts are unavailable for `ORA_ANYTIME` templates even if the REST
child resource accepts an alert row. Before every alert create, update, or
delete, read and bind the fresh parent `TemplateTypeCode`. Stop a create or
update before preview when it is `ORA_ANYTIME`; explain the product restriction
and do not claim a saved reminder. A guarded delete remains available only to
remove an exact unsupported row already present. The executable contract
requires this approval-bound parent type context for alert mutations.

For an existing template, do not create a new template-role child by itself
when that role must also participate in a section. Fusion validates the
section membership during the role create, while the REST role-action create
requires the server-generated `TmplRoleId`; the two separate REST child calls
cannot form one valid effect. Collect the intended section membership before
any write and route the complete template-role plus section-role-action change
through the validated FSM archive workflow. Preserve every existing parent and
child row required by the FSM graph, reject duplicates, and verify both the new
role and its exact section participation after terminal import success. Never
probe with an isolated role POST or substitute an ad hoc REST sequence.

Removing an existing template role and its last section role action has the
inverse atomicity requirement. Before preview, inventory every role dependency:
all section role actions, period questionnaires bound to its `TmplRoleId`, root
matrix-participant defaults and controls, and the assigned process flow's
participant-selection flags and tasks. If the current process flow requires
the role, obtain an explicit compatible replacement-flow choice first. Do not
silently clear a required process flow when periods exist, and do not infer a
replacement. Remove or replace questionnaire references and clear root role
references under their own approval-bound effects, verifying each one, before
refreshing the two final child ETags. Do not probe with separate child DELETE calls:
the role-action delete can fail while the role still exists, and the role
delete can fail while the action still exists. First clear any root settings
that reference the role and verify that effect. Then obtain fresh raw item ETags
for the exact role action and template role and use the task-declared
`atomic_role_delete` REST batch. The wrapper serializes each ETag as the
batch protocol's one-value `ifMatch` array and uses raw commas in relative item
keys. It binds exactly those two DELETE parts to one
template, forbids wildcard concurrency, orders the role action before the
role, and commits or rolls back the parts as one request. After any response,
perform new exact-identity reads for both deleted children and the preserved
parent/siblings before reporting success. An FSM archive that merely omits the
rows is merge-only and must never be represented as a deletion.

### Read-only template comparisons

When a user asks which existing templates are suitable starting points or asks
to compare templates, preserve the exact business state returned by the
task-declared reads in the user-facing answer. For every shortlisted template,
state the exact `DateFrom` and `DateTo`, status, template type, `InUseFlag`,
`DocumentExistsFlag`, and `PeriodExistsFlag`, then describe only configuration
differences actually read. Identify requested child areas that were not
inspected. A year, "current," "active through" without the start date, or an
inferred lifecycle description does not replace the exact dates and status.

### Related reference-object metadata, lookup, and setup route

Before preparing template periods, sections, items, role actions, eligibility
profiles, questionnaires, rating selections, or their children, use the
allowlisted contract in
[`ora-resource/related_fixture_routes.json`](ora-resource/related_fixture_routes.json)
through `scripts/related_fixture_rest.py`. The adapter reuses shared OAuth and
`request_bytes`; it does not accept a caller-supplied endpoint or HTTP method.

The initial metadata operation is an independent read-only route. It may fetch
only the Describe paths explicitly listed in the contract's `metadata_routes`.
It validates the configured target origin and returned resource identity and
writes a binding and response digest. It does not require a prior Describe,
which avoids a circular discovery requirement.

Related LOV routes are read-only. Fetch every page, require one exact match,
validate the declared identity, status, fixed eligibility values, and
effectivity date, and retain page-level request and response digests. Zero or
multiple exact matches stop only the dependent request. Do not turn a LOV route
into setup CRUD or substitute another endpoint.

Review-period setup is a separate explicit route. Provider ownership remains
Goal Management setup task `ORA_HRG_MANAGE_REVIEW_PERIODS`, as recorded by the
effective setup-task catalog. Use the writable `reviewPeriods` resource for this route; `reviewPeriodsLOV`
is a read-only consumer lookup.
Fetch fresh `reviewPeriods` Describe metadata before every preview; require the
target action and writable fields from those exact bytes, bind Goal Management
ownership in the preview, reject any name collision found by a fresh lookup,
and require an item ETag for update or delete. Execute each approved write once
and verify it with both an exact item read and the consumer LOV. This scoped
route prepares a Performance Template prerequisite; it does not transfer
provider ownership to Performance Management or authorize arbitrary Goal
Management setup.

Other writable related setup is limited to the source-supported Performance
Template Sections and Performance Roles resources and remains owned by their
registered provider skills. Fetch fresh Describe metadata first, validate
writable fields and operations, bind the exact target/method/path/query/payload
and standing or request-specific approval, omit server-managed fields, execute once without
automatic write replay, and verify the resulting identity and state by a fresh
GET. Eligibility profiles, questionnaires, content items, rating models, and
rating levels remain read-only consumers here; route any needed creation to an
existing owning setup skill rather than inventing fields.




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.performance-management.performance-template` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Post-import verification

After Fusion reports an import as successful, include this clickable verification link in the final result: [Open Performance Templates]({restBaseUrl}/fscmUI/redwood/performance/performance-templates/template-search). Resolve `{restBaseUrl}` from the active target Fusion environment and remove any trailing slash; never hard-code an environment URL. The link lets the user verify the data and must not be opened automatically or used to imply an import succeeded before Fusion reports success.
