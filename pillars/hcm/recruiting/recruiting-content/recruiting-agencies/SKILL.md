---
skill_id: "hcm.recruiting.recruiting-content.recruiting-agencies"
name: "Recruiting Agencies Setup Task Guidance"
description: "Provides task-specific setup guidance for Recruiting Agencies under the Recruiting Content functional area."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Content"
functional_area_code: "ORA_RECRUITING_CONTENT"
task_code: "ORA_IRC_MANAGE_AGENCIES"
task_name: "Recruiting Agencies"
parent_skill_id: "hcm.recruiting.recruiting-content"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM recruiting pillar team"
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
  - "core.data-loader.task-hook"
  - "core.project-mgmt.project-workspace-initializer"
  - "core.runbook"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-content/recruiting-agencies/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-content/recruiting-agencies/current/"
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

# Recruiting Agencies Setup Task Guidance

## Purpose

Safely retrieve, validate, create, and update Recruiting Agency records through the catalog-supported Functional Setup Manager export/import route. This skill manages agency rows only.

## Setup Task Skill Contract

- task_code: `ORA_IRC_MANAGE_AGENCIES`
- task_name: `Recruiting Agencies`
- parent_skill_id: `hcm.recruiting.recruiting-content`
- pillar: `HCM`
- offering: `Recruiting`
- functional_area: `Recruiting Content`
- functional_area_code: `ORA_RECRUITING_CONTENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Recruiting Agencies` under `Recruiting Content`.

## Setup Task Metadata

- Task name: `Recruiting Agencies`
- Task code: `ORA_IRC_MANAGE_AGENCIES`
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
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Recruiting`
- Functional area / Setup Object: `Recruiting Content`
- Setup task name: `Recruiting Agencies`
- Setup task code: `ORA_IRC_MANAGE_AGENCIES`

## Read Order

1. [Input validation](ora-resource/ora_input_validation.md)
2. [Reference lookups](ora-resource/ora_reference_lookups.md)
3. [Defaulting rules](ora-resource/ora_defaulting_rules.md)
4. [Dependency readiness](ora-resource/ora_dependency_readiness.md)
5. [Design enforcement](ora-resource/ora_design_enforcement.md)
6. [Error handling](ora-resource/ora_error_handling.md)
7. [Compiled rule registry](ora-resource/ora_rule_registry.json)

## Supported Operations

- Retrieve all agencies or an exact Agency Name from a fresh target-environment task export.
- Validate a new agency and return `ALREADY_EXISTS` when its exact Agency Name already exists.
- Validate an update and require exactly one exact Agency Name match.
- Generate a candidate FSM ZIP only from a verified target-release export or approved template.
- Hand off an immutable validated ZIP to `core.data-loader` only after approval matches its fingerprint and target.

## Agency Inputs

- Required for Create: Agency Name, Referral Type, and Main Contact.
- Required for Update: exact Agency Name and at least one supported field change.
- Conditional: Exclusivity Length is required when Referral Type is Person Specific.
- Optional: Contract Type, Agency Email, Notes or Address, Create job application on behalf of candidate, and Status.
- Create default: when Status is omitted, set `StatusCode` to `ORA_ACTIVE` before preview.
- Update preservation: retain every exported field not explicitly changed.

## Retrieve Output Mapping

For Retrieve, parse `ORA_IRC_RECRUITING_AGENCIES.csv` by the exact header name. Never map fields by column position, visual order, or inferred value type.

| Customer-facing field | CSV header |
|---|---|
| Agency Name | `AgencyName` |
| Main Contact | `AgencyContact` |
| Agency Email | `AgencyEmail` |
| Status | `StatusCode` |
| Referral Type | `AgencyTypeCode` |
| Contract Type | `ContractTypeCode` |
| Notes or Address | `AgencyNotes` |
| Exclusivity Length | `EmbargoPeriodCode` |
| Inactivation Date | `InactivationDate` |
| Deletion Date | `DeletionDate` |
| Create job application on behalf of candidate | `CreateJaFlag` |

Keep `AgencyContact` and `AgencyEmail` independent: a person's name from `AgencyContact` is Main Contact, while an email address from `AgencyEmail` is Agency Email. Resolve supported lookup codes to their current enabled meanings for display. If a required header is missing or duplicated, stop with `BLOCKED`; do not shift or guess the mapping.

## Guarded Workflow

1. Classify the request as Retrieve, Create, Update, or unsupported. For Create, Update, or import, resolve the project execution context through the dependency-readiness resource before preparing the candidate; delegate missing project or Run Book setup to its owning core workflow.
2. Obtain a fresh immutable export for the intended target and verify exact task/package identity.
3. Resolve supplied Referral Type, Contract Type, and Exclusivity Length as one enabled exact Meaning or LookupCode through `core.fusion-api.apps-common.lookups`.
4. Apply the Create-only status default and the operation-specific exact Agency Name rule.
5. Preserve the verified export structure and build the smallest candidate agency package.
6. Complete core Data Loader preflight and Task Hook validation using the generated task context, then present the target, operation, effective values, and SHA-256 fingerprint for explicit approval.
7. Revalidate the unchanged artifact and approval, then hand off once to `core.data-loader`.
8. Return the requested agency fields using the exact Retrieve Output Mapping and keep technical evidence in internal diagnostics.

Read-only Retrieve uses the shared task exporter and does not require a Run Book or Data Loader Task Hook. Create, Update, and FSM import inherit the current core Data Loader project/Run Book prerequisites. Follow the Project execution context section in `ora-resource/ora_dependency_readiness.md`; the agency skill does not create its own task context or approval envelope. An agency package passing CSV validation is not yet ready for import approval.

## Approval Boundary

Preparing or reviewing a package is not approval to import it. Approval must identify the exact target environment, Agency Name, operation, and immutable ZIP fingerprint. Any artifact or target change invalidates approval.

## Unsupported Operations

- Agent creation, update, retrieval, import/export, coverage, user accounts, passwords, roles, or agency-agent relationships.
- Agency deletion through FSM, REST, database, or an undocumented mechanism.
- `Allow Internal Candidate Search`; return `UNSUPPORTED_AGENCY_OPTION` and instruct the user to maintain it manually in Fusion.
- Direct REST or database agency mutations.
- Invented package members, CSV columns, child rows, keys, status values, defaults, or lifecycle behavior.
- Automatic retry or fallback after a failed, partial, timed-out, conflicting, or uncertain operation.
- Fabricated task contexts, Run Book bindings, project activation state, or Task Hook approval envelopes; bypassing the core execution prerequisites.

## Customer-Facing Outcomes

Use stable outcomes such as `ALREADY_EXISTS`, `NOT_FOUND`, `AMBIGUOUS_AGENCY`, `INVALID_LOOKUP_VALUE`, `EXCLUSIVITY_REQUIRED`, `UNSUPPORTED_AGENCY_OPTION`, `BLOCKED`, and `PROCESS_FAILED`. Give one plain-language correction. Do not expose process or request identifiers, filenames, paths, package members, task codes, rule IDs, match counts, stack traces, SQL/JBO details, or backend evidence in normal user-facing output.




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

Use the parent functional-area skill `hcm.recruiting.recruiting-content` for functional-area sequencing and scope decisions. Do not authenticate, export, generate a production ZIP, or import merely by loading this skill; those actions require their declared routes and gates.
