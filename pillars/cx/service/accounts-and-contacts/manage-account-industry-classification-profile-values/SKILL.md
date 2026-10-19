---
skill_id: "cx.service.accounts-and-contacts.manage-account-industry-classification-profile-values"
name: "Manage Account Industry Classification Profile Values Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Account Industry Classification Profile Values under the Accounts and Contacts functional area."
layer: "pillar"
pillar: "CX"
offering: "Service"
functional_area: "Accounts and Contacts"
functional_area_code: "ORA_SVC_ACCOUNTS_AND_CONTACTS"
task_code: "ORA_SVC_MANAGE_ACCT_IND_CLASS"
task_name: "Manage Account Industry Classification Profile Values"
parent_skill_id: "cx.service.accounts-and-contacts"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX service pillar team"
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
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.fusion-api.apps-common"
  - "core.auth.fusion-oauth-authentication"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/service/accounts-and-contacts/manage-account-industry-classification-profile-values/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/accounts-and-contacts/manage-account-industry-classification-profile-values/current/"
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

# Manage Account Industry Classification Profile Values Setup Task Guidance

## Purpose

Manage the Industry Classification Category profile-option value used for account industry classification.
## Setup Task Skill Contract

- task_code: `ORA_SVC_MANAGE_ACCT_IND_CLASS`
- task_name: `Manage Account Industry Classification Profile Values`
- parent_skill_id: `cx.service.accounts-and-contacts`
- pillar: `CX`
- offering: `Service`
- functional_area: `Accounts and Contacts`
- functional_area_code: `ORA_SVC_ACCOUNTS_AND_CONTACTS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Account Industry Classification Profile Values` under `Accounts and Contacts`.

## Setup Task Metadata

- Task name: `Manage Account Industry Classification Profile Values`
- Task code: `ORA_SVC_MANAGE_ACCT_IND_CLASS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``




## FSM Contract

### FND_APP_PROFILE_OPTION

- `ProfileOptionName`: Set to MOT_INDUSTRY_CLASS_CATEGORY. Do not create a profile option definition through this workflow.
- `ApplicationId`: Retain the exported application ID for MOT_INDUSTRY_CLASS_CATEGORY.
- `ModuleId`: Retain the exported module ID for MOT_INDUSTRY_CLASS_CATEGORY.
- `Description`: Retain the exported description for MOT_INDUSTRY_CLASS_CATEGORY.
- `SqlValidation`: Retain the exported SQL validation for MOT_INDUSTRY_CLASS_CATEGORY.
- `StartDateActive`: Retain the exported start date for MOT_INDUSTRY_CLASS_CATEGORY.
- `EndDateActive`: Retain the exported end date for MOT_INDUSTRY_CLASS_CATEGORY.
- `UserProfileOptionName`: Retain the exported user-facing name for MOT_INDUSTRY_CLASS_CATEGORY.
- `CreationDate`: Retain the exported value.
- `CreatedBy`: Retain the exported value.
- `LastUpdateDate`: Retain the exported value unless the same approved package updates the profile option definition.
- `LastUpdatedBy`: Retain the exported value unless the same approved package updates the profile option definition.
- `LastUpdateLogin`: Retain the exported value.

### ORA_FND_APP_PROFILE_OPTION_LEVEL

- `FND_APP_PROFILE_OPTION.ProfileOptionName`: Set to MOT_INDUSTRY_CLASS_CATEGORY.
- `FND_APP_PROFILE_OPTION.ApplicationId`: Retain the exported application ID for MOT_INDUSTRY_CLASS_CATEGORY.
- `LevelName`: Retain the exported supported profile level for MOT_INDUSTRY_CLASS_CATEGORY. When no supported level is supplied for a task-owned profile-value row, default to SITE.
- `UpdateableFlag`: Retain the exported value; do not enable an unsupported profile level.
- `EnabledFlag`: Retain the exported value; do not enable an unsupported profile level.
- `CreationDate`: Retain the exported value.
- `CreatedBy`: Retain the exported value.
- `LastUpdateDate`: Retain the exported value.
- `LastUpdatedBy`: Retain the exported value.
- `LastUpdateLogin`: Retain the exported value.

### FND_APP_PROFILE_VALUE

- `FND_APP_PROFILE_OPTION.ProfileOptionName`: Set to MOT_INDUSTRY_CLASS_CATEGORY.
- `FND_APP_PROFILE_OPTION.ApplicationId`: Retain the exported application ID for MOT_INDUSTRY_CLASS_CATEGORY.
- `LevelName`: Retain the exported supported profile level for MOT_INDUSTRY_CLASS_CATEGORY. When no supported level is supplied for a task-owned profile-value row, default to SITE.
- `LevelValue`: Retain the exported level value for the selected profile level. When LevelName defaults to SITE and no level value is supplied, default to SITE.
- `ProfileOptionValue`: Set to the approved Industry Classification Category value. Present the value for approval before import; do not infer a value when the intended category or documented semantics are insufficient.
- `CreationDate`: Retain the exported value.
- `CreatedBy`: Retain the exported value.
- `LastUpdateDate`: Set to the current date and time for an approved value update.
- `LastUpdatedBy`: Set to the current user for an approved value update.
- `LastUpdateLogin`: Retain the exported value unless same-task package evidence requires an update.
## Use Cases

### View Account Industry Classification Profile Value

View the effective Industry Classification Category profile value for the current authenticated user session.

1. Read MOT_INDUSTRY_CLASS_CATEGORY with core.fusion-api.apps-common using the Profile Values REST resource and ProfileOptionNameFinder.
2. Return ProfileOptionName and the effective ProfileOptionValue for the current user session.

### View Account Industry Classification Profile Values

View the effective Industry Classification Category profile value for the requested account-industry-classification scope.

1. Read MOT_INDUSTRY_CLASS_CATEGORY with core.fusion-api.apps-common using the Profile Values REST resource.
2. Return ProfileOptionName and ProfileOptionValue when resolved; identify a profile option that is not REST exposed separately.
3. Do not infer a site or user value from a missing REST response.

### Update Account Industry Classification Profile Value

Update an approved Industry Classification Category profile-option value at its supported profile level.

1. Read the current effective profile value with core.fusion-api.apps-common using the Profile Values REST resource when MOT_INDUSTRY_CLASS_CATEGORY is REST exposed.
2. Validate MOT_INDUSTRY_CLASS_CATEGORY, the proposed value, and the target profile level against the documented semantics and the task export metadata.
3. Export profile-option setup data with shared.setup-export.task-level-export.
4. Use the completed export of the same setup task as the package baseline; preserve its package structure and modify only the approved MOT_INDUSTRY_CLASS_CATEGORY profile-value row.
5. Validate the FSM package with shared.validation.setup-data-validator.
6. Import the approved ZIP with core.data-loader.
7. Verify the effective updated value with a fresh Profile Values REST read when MOT_INDUSTRY_CLASS_CATEGORY is REST exposed; otherwise verify the persisted value with a fresh task export.

### Create Account Industry Classification Profile Option

Create an Industry Classification Category profile option definition.

Not supported. This setup task manages the MOT_INDUSTRY_CLASS_CATEGORY profile value; do not create profile option definitions through REST or FSM without a separately documented profile-option-definition workflow.

### Delete Account Industry Classification Profile Option

Delete an Industry Classification Category profile option definition.

Not supported. This setup task manages the MOT_INDUSTRY_CLASS_CATEGORY profile value; do not delete profile option definitions through REST or FSM.
## Guard Rails

1. Require an authenticated Fusion user context before any Fusion operation; use `core.auth.fusion-oauth-authentication`.
2. Do not use `core.fusion-api.rest-api-client` to create, update, or delete records.
3. Do not use `shared.setup-import.task-level-import` to create, update, or delete records.
## Supported Operations

1. `view`: Read the effective authenticated-session value through `core.fusion-api.apps-common` when `MOT_INDUSTRY_CLASS_CATEGORY` is REST exposed; do not infer a configured value from a missing response.
2. `update`: Update one explicitly approved supported-level profile value through the task-owned FSM workflow.
3. `create_profile_option` and `delete_profile_option`: Not supported; this task does not create or delete the profile-option definition.
4. `export`, `import`, and `validate`: Use the catalog-backed CSV/FSM routes declared below.

Do not use this skill to create or alter profile-option definitions, infer an undocumented valid value, or bulk-update unrelated profile options.

## Supported Profile Options

This task owns exactly this profile option in the validated `cptcpuwqy` task inventory:

| Profile Option Code | Display Name |
|---|---|
| `MOT_INDUSTRY_CLASS_CATEGORY` | Industry Classification Category |

For `view` or `update`, require this exact code. For FSM validation, reject profile-option rows owned by another task. If a completed export omits this code, report `export_content_discrepancy`; do not call a structurally valid ZIP corrupt and do not invent the omitted row.

## Oracle Documentation

Use Oracle's [Overview of Territory Account Assignment](https://docs.oracle.com/en/cloud/saas/sales/faswa/overview-of-territory-account-assignment.html) as the current public reference for how the Industry Classification Category profile value affects primary industry, organization type, and auxiliary classification assignment attributes. Confirm the exact profile definition and classification category before preparing a change.

## View and Change Profile Option Values

For `view`, use `core.fusion-api.apps-common` and the authenticated-session `profileValues` resource only when `MOT_INDUSTRY_CLASS_CATEGORY` is REST exposed. It is not a configured-value write route, and an absent response does not establish a configured site or user value.

For `update`, display the target environment, profile option code, level, persisted current value from a fresh task export, proposed value, and supported-level evidence. Require explicit approval bound to those exact values before building the FSM package. Do not retry an import automatically. Verify the persisted value with a fresh task export; additionally read the effective value when the option is REST exposed.

Treat a missing task-owned profile-value row, an unsupported profile level, a privilege rejection, or an invalid value as a stop condition. Do not substitute a browser or direct REST client for the task-owned FSM workflow.

For an import, hand the exact immutable FSM ZIP and confirmed target environment to `core.data-loader`. Consume its existing FSM validation, approval, adapter, execution, and error contract unchanged. This task skill must not add its own package-origin check, release-compatibility policy, adapter option, or FSM metadata rewrite.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Service`
- Functional area / Setup Object: `Accounts and Contacts`
- Setup task name: `Manage Account Industry Classification Profile Values`
- Setup task code: `ORA_SVC_MANAGE_ACCT_IND_CLASS`

## FSM Data Loader Package Requirements

1. Read the task's fsm_contract first when it is present. Treat its objects and field guidance as the task-specific starting point for classifying each requested change as an existing-root update, new root, existing-child update, new child of an existing parent, new relationship, or mixed package change.
2. Read `ASM_SETUP_CSV_METADATA.xml` in the task export package for business objects, XML paths, node sequence, attributes, scope, and relationships; reconcile it with the task's fsm_contract when one is present.
3. Use the fsm_contract object and field guidance together with metadata-defined node sequence and relationships to determine package order and required object coverage.
4. Verify the selected baseline or template package includes the members, file names, structure, headers, encoding, scope, relationship rows, and fsm_contract objects and fields required for the requested change.
5. Treat a completed export of this same setup task as authoritative evidence for package structure, headers, node order, key and linkage shape, and generated-identity handling. Use it to corroborate the fsm_contract and record provenance for copied template values.
6. For existing-row updates, retain exported identities and all unchanged values, parent rows, child rows, and relationships required by the fsm_contract and package evidence; do not carry unrelated baseline rows into the change package unless they are required for import integrity. Change only approved fields.
7. For a new child or relationship, retain the existing parent identity and use only linkage, keys, and required values specified by the fsm_contract or confirmed by same-task package evidence.
8. For greenfield rows, construct the create contract from the fsm_contract, task-specific documented requirements, `ASM_SETUP_CSV_METADATA.xml`, a completed export of this same task, and supported preview or dry-run results where available.
9. An export whose data CSV members contain only headers is valid structural evidence for a greenfield contract, not an automatic blocker. Use the fsm_contract, exported package structure, and explicit supported inputs to construct the rows; stop only when required fields, keys, relationships, or values remain unresolved or validation rejects the package.
10. Populate every root, child, scoped, localized, and relationship object required by the fsm_contract or confirmed package contract. Populate approved business keys, required values, and reference values; omit generated identities unless explicitly required.
11. Classify every populated fsm_contract field as request-provided, documented requirement, export-derived structural value, export-derived template value, generated or omittable, or unresolved.
12. A fsm_contract field may be omitted only when it is documented as generated or optional, is absent or consistently blank in semantically comparable exports of this same task, or is accepted as omitted by supported preview or dry-run validation. Do not infer a value solely from a field name or description.
13. Do not copy identities, reference keys, parent keys, scope values, localized values, lookup codes, or behavior-changing settings unless the fsm_contract, request, documented guidance, or approved compatible template default explicitly supports the value.
14. Verify every non-generated parent, lookup, code, scope, locale, and related-object reference required by the fsm_contract against approved same-task package evidence or the workflow's documented resolver; include required parents or relationship rows only when the package contract requires them.
15. Build the complete package required by the fsm_contract and package evidence; never use a child-only package or infer fields, defaults, identities, or relationships from another task or object type.
16. Validate package members, fsm_contract objects and fields, metadata, keys, scopes, references, relationships, node order, field-value provenance, and approved changes before import; confirm that no baseline identity, template-only setting, or unrelated row is introduced or modified unintentionally. Use preview or dry-run validation when available.
17. Stop when a required fsm_contract field or object, identity rule, parent-child linkage, scope, dependency, or behavior-changing setting remains unresolved and lacks an explicit approved value or sufficient same-task evidence. Do not block for fields evidenced as generated or validated-omittable.
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

Use the parent functional-area skill `cx.service.accounts-and-contacts` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
