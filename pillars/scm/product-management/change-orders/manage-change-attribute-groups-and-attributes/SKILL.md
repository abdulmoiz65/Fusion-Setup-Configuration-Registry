---
skill_id: "scm.product-management.change-orders.manage-change-attribute-groups-and-attributes"
name: "Manage Change Attribute Groups and Attributes Setup Task Guidance"
description: "Prepares FSM CSV packages from requested change attributes and routes validation, import, and deployment for EGO_CHANGE_EFF (application 10010) under Product Management Change Orders."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Change Orders"
functional_area_code: "EGO_CHANGE_ORDERS"
task_code: "ORA_MANAGE_CHANGE_ATTRIBUTE_GROUPS_AND_ATTRIBUTES"
task_name: "Manage Change Attribute Groups and Attributes"
parent_skill_id: "scm.product-management.change-orders"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM product management pillar team"
version: "0.2.2"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "attribute_definitions"
  - "attribute_group_and_change_type_assignment"
  - "setup_data_artifacts"
  - "fusion_environment_context"
  - "eff_task_context"
  - "flexfield_deployment_context"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "prepared_fsm_csv_package"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.apps-common.extensible-flexfields"
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
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/change-orders/manage-change-attribute-groups-and-attributes/current/fsm-package/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/change-orders/manage-change-attribute-groups-and-attributes/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/change-orders/manage-change-attribute-groups-and-attributes/current/"
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
side_effects:
  - "Creates project-local FSM CSV files and a ZIP package from Oracle task templates and the requested attribute definitions."
  - "Delegated workflows may export EFF setup data, import an approved FSM CSV archive, or submit an approval-gated EGO_CHANGE_EFF deployment."
required_privileges:
  - "Fusion privileges required by the selected setup-task export, Data Loader, and EFF deployment workflows"
---

# Manage Change Attribute Groups and Attributes Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Change Attribute Groups and Attributes` under `Change Orders`, using the Extensible Flexfield `EGO_CHANGE_EFF`.

## Setup Task Skill Contract

- task_code: `ORA_MANAGE_CHANGE_ATTRIBUTE_GROUPS_AND_ATTRIBUTES`
- task_name: `Manage Change Attribute Groups and Attributes`
- parent_skill_id: `scm.product-management.change-orders`
- pillar: `SCM`
- offering: `Product Management`
- functional_area: `Change Orders`
- functional_area_code: `EGO_CHANGE_ORDERS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Change Attribute Groups and Attributes` under `Change Orders`.

## Extensible Flexfields Routing

Read the core [Extensible Flexfields skill](../../../../../core/fusion-api/apps-common/extensible-flexfields/SKILL.md)
and its [extensible-flexfields.md reference](../../../../../core/fusion-api/apps-common/extensible-flexfields/references/extensible-flexfields.md)
before routing EFF setup-data or deployment work. Delegate to
`core.fusion-api.apps-common.extensible-flexfields` with this task context:

| Context | Value |
| --- | --- |
| Flexfield type | `EFF` |
| Flexfield code | `EGO_CHANGE_EFF` |
| Flexfield usage code | `EGO_CHANGE_DL` (fixed for this task) |
| Application ID | `10010` (fixed for this task) |
| Task code | `ORA_MANAGE_CHANGE_ATTRIBUTE_GROUPS_AND_ATTRIBUTES` |
| Task name | `Manage Change Attribute Groups and Attributes` |
| Offering | `Product Management` |
| Functional area | `Change Orders` (`EGO_CHANGE_ORDERS`) |
| Task sequence | Positive sequence resolved from the project setup plan |

Pass the confirmed target environment and preserve this exact identity through
export, import, validation, deployment, and status checks. Apply the core
reference's eligibility gate, including both export/import support flags.
Stop on missing or conflicting task context; do not select a task by name alone.

This skill owns FSM source preparation from the user's attribute definitions;
the user does not need to supply a completed CSV file or import ZIP. Request the
task's template/spec package through `shared.setup-export.task-level-export` as
an explicit preparation step. Use normal data-export mode for an explicitly
requested current-configuration baseline.

Prepare the package using the workflow below. For import, require the resulting
nonempty, valid ZIP containing the exact-case `ASM_SETUP_CSV_METADATA.xml` member
and task CSV files. Freeze the completed ZIP bytes after preparation and
route through `core.data-loader` with `requested_operation: FSM CSV Import`, the
validated ZIP path, target environment, and exact task context with positive
sequence. Data Loader owns Task Hook validation and the approval-preview
lifecycle; do not add a duplicate pillar approval or call import endpoints directly.

## Prepare the FSM CSV Package

Run this assisted preparation workflow when the request supplies attribute
definitions instead of an import package. A missing user-supplied ZIP is not a
blocker: obtain the source template and create the CSV files and ZIP here.

1. Read the project requirements and exact task context. Use application ID
   `10010`, flexfield code `EGO_CHANGE_EFF`, and flexfield usage code
   `EGO_CHANGE_DL`. Always use `EGO_CHANGE_DL` for `FlexfieldUsageCode`
   in usage, context-usage, page, and page-context association rows, including
   prefixed parent-key columns. Reuse this existing usage; do not create a usage
   named `EGO_CHANGE_EFF` or ask the user to rediscover the usage code.
   Capture attribute names and types,
   the containing attribute group/context, and the requested change type. When
   the user calls the containing group a "segment", interpret it as the group
   containing the named attributes and record that interpretation. Distinguish
   attribute scope from assignment to All Change Types; never broaden a named
   change-type assignment solely because the request says "global".
2. Reuse a matching Oracle-produced template/spec package already selected for
   this project, or obtain one through
   [Task Level Export](../../../../../shared/setup-export/task-level-export/SKILL.md).
   Pass task code `ORA_MANAGE_CHANGE_ATTRIBUTE_GROUPS_AND_ATTRIBUTES`, offering
   `Product Management`, functional area `Change Orders`, and the active project
   ID to `export_setup_task_csv.py` in its default template/spec mode. Follow
   that workflow's catalog checks, authentication, process timeout, and download
   handling. Keep the original package unchanged under the project's exports.
3. Inspect the package metadata, CSV headers, and supplied specification/help
   before writing rows. Derive file names, keys, supported type codes, required
   columns, relationships, and formatting from that source. Do not invent an
   XML manifest, CSV schema, storage column, value set, or target category ID.
   Use the latest task-specific Oracle guidance for field semantics. Resolve
   reusable defaults from the source; ask only for required business choices
   that cannot be resolved, not for the user to construct the CSV package.
4. Populate a working copy with rows for the requested group/context, attributes,
   and supported change-type associations. Map String, Number, and Date to the
   template's actual codes. Validate name uniqueness, type-compatible storage
   and value sets, required fields, and parent-child keys. Existing value sets
   must be available before EFF import; any newly required value sets need their
   own catalog-routed setup step before the EFF package is imported.
5. For EGO_CHANGE_EFF, use the exact Change Order Type as CategoryCode
   (user-confirmed mapping); for example, ExampleEngineeringChangeOrder maps to ExampleEngineeringChangeOrder.
   Preserve case. Use the fixed `FlexfieldUsageCode` `EGO_CHANGE_DL`; resolve
   an existing PageCode from setup evidence or choose a new PageCode when the
   user requests a new page. Resolve inherited
   contexts from available authoritative setup evidence. Include context/category and page associations
   where represented by the task's CSV contract. Check UI page visibility as
   well as group membership. If a required assignment is outside this package's
   supported objects, record the exact remaining step and resolve its catalog
   task through the project router; do not fabricate columns or claim assignment
   complete merely because the attributes were created.
6. Write CSVs using a CSV-aware writer, preserving the source headers, member
   paths, encoding, and date/number formats. Retain every CSV member; leave a
   header-only file for an unused object. Preserve the original
   `ASM_SETUP_CSV_METADATA.xml` bytes and non-data package members. Create the
   new ZIP under this skill's project `current/fsm-package/` artifact folder,
   with no additional enclosing folder. Verify member paths, parseable CSVs,
   row widths, keys, references, requested row counts, and metadata integrity.
7. Persist the package, source provenance, field mappings/defaults, row-count
   summary, and validation findings in the project artifact index. Route shared
   checks to `shared.validation.setup-data-validator` and
   `shared.validation.reference-data-validator`, then hand the finished ZIP to
   Data Loader preflight and its Task Hook before showing import approval.
   Record the final archive checksum; any subsequent change requires fresh
   validation and approval. Source preparation itself does not import or deploy.

If template retrieval fails or a required field/association remains unsupported,
record the actual failure and the next action. Retain completed preparation
artifacts and name the unresolved requirement rather than asking for a prepared
ZIP as the default remedy.

## Report the Execution Result

The user explicitly requested execution results as part of this task's workflow.
For this skill, that standing request authorizes read-only result checks after
an approved import; do not require a separate "what was the result" message.
This task-specific user instruction takes precedence over the generic Data
Loader default of stopping at the submission receipt. Keep all import and
deployment approval gates unchanged.

1. After Data Loader accepts submission, retain its returned Request ID and
   report that the import was submitted, not that configuration is complete.
2. Follow Data Loader's status workflow using
   `core/data-loader/scripts/get_data_load_info.py <request-id> --status-only`.
   Retrieve the data-set status, errors, and FSM ProcessLog through that helper;
   do not infer success from the initiation response alone.
3. While the import is pending or running, check at 10-second intervals for up
   to 300 seconds. Stop on terminal success, failure, a lookup error, or timeout.
   Never resubmit an import or upload as a monitoring retry. On timeout, report
   the last observed status and Request ID and wait for a user-requested recheck.
4. Report the final observed status with total, loaded, and failed counts. For
   failures, explain the actionable validation errors and affected attributes
   or privileges in plain language, link the downloaded ProcessLog, and state
   the next correction. Keep raw stack traces in the log. If result retrieval
   fails, report the outcome as unknown rather than successful.
5. Distinguish import completion from deployment and effective configuration.
   Do not deploy a failed or incomplete import or claim that imported security
   privileges are effective before the required deployment and access checks.
   For a separately approved deployment, also retrieve and report its terminal
   result under the deployment/status workflow below.

### Source guidance

- [Oracle FSM CSV package handling](https://docs.oracle.com/en/cloud/saas/applications-common/26b/oafsm/using-functional-setup-manager.pdf):
  see **Manage Setup Using CSV File Packages** for editing and repackaging.
- [Oracle change-type EFF setup](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faipr/configure-extensible-flexfields-for-change-types.html):
  see context inheritance, value-set prerequisites, and category/page associations.

## EGO_CHANGE_EFF Deployment and Status

Follow **REST Deployment and Status** in the core reference for deployment of
the already-configured `EGO_CHANGE_EFF`. After a successful import, enter this
workflow; stop if the import failed or remains incomplete.

- Always pass `application_id: 10010` for `EGO_CHANGE_EFF` deployment and status.
  This is the task's established application ID; do not ask the user to supply
  it. Use `/fscmUI/applcoreApi/latest/flexfields/metadata/deploy/10010/EFF/EGO_CHANGE_EFF`
  for deployment and `/fscmUI/applcoreApi/latest/flexfields/metadata/getDeploymentState/10010/EFF/EGO_CHANGE_EFF`
  for status through the core workflow.
- Pass `flexfield_code: EGO_CHANGE_EFF` and default `forceDeployment` to the
  string `"false"`; accept only the reference's string values `"true"` or `"false"`.
- Delegate deployment and status transport to `core.fusion-api.rest-api-client`
  through the core EFF workflow. Present the exact target environment, resolved
  POST endpoint, and immutable payload, then obtain explicit approval immediately
  before deployment. Import approval does not approve deployment.
- Preserve the same identifiers for status. Poll only when requested, following
  the reference's 10-second interval and 300-second limit. Stop on `DEPLOYED`,
  terminal failure, deployment error, or timeout; do not retry a POST without
  explicit approval.
- Return export/import artifact references and process outcomes, and capture
  deployment `jobId`, `jobStatus`, `deploymentStatus`, `validationStatus`,
  `validationReport`, and `deploymentErrorMessage` in project validation/run
  artifacts. Follow the core workflow's failure classification and redaction rules.

## Setup Task Metadata

- Task name: `Manage Change Attribute Groups and Attributes`
- Task code: `ORA_MANAGE_CHANGE_ATTRIBUTE_GROUPS_AND_ATTRIBUTES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Obtain the task template with `shared.setup-export.task-level-export` and
   create the FSM CSV package using **Prepare the FSM CSV Package** when the
   input is attribute definitions. Reuse an explicitly supplied valid task ZIP
   when the request is to import that package.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import the prepared setup task package with `core.data-loader`.
5. Follow **Report the Execution Result** to check and report the import outcome.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Change Orders`
- Setup task name: `Manage Change Attribute Groups and Attributes`
- Setup task code: `ORA_MANAGE_CHANGE_ATTRIBUTE_GROUPS_AND_ATTRIBUTES`
- Flexfield code: `EGO_CHANGE_EFF`
- Flexfield usage code: `EGO_CHANGE_DL` (always use for this task)
- Application ID: `10010`

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `attribute_definitions`: requested attribute names, data types, and supplied properties.
- `attribute_group_and_change_type_assignment`: group/context name and target change type.
- `setup_data_artifacts`: optional existing source template, baseline, or import ZIP;
  when absent, this skill obtains a template and prepares the FSM CSV package.
- `fusion_environment_context`: confirmed target environment for the selected workflow.
- `eff_task_context`: exact task identity above and positive project task sequence.
- `flexfield_deployment_context`: fixed application ID `10010` and `EGO_CHANGE_EFF`,
  with optional force value, when deployment or status is requested.

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `prepared_fsm_csv_package`: generated task CSVs and immutable import ZIP with
  source provenance, mappings, and validation findings.
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `scm.product-management.change-orders` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
