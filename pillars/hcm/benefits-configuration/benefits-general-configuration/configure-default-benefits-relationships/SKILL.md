---
skill_id: "hcm.benefits-configuration.benefits-general-configuration.configure-default-benefits-relationships"
name: "Configure Default Benefits Relationships Setup Task Guidance"
description: "Provides task-specific setup guidance for Configure Default Benefits Relationships under the Benefits General Configuration functional area."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits General Configuration"
functional_area_code: "ORA_BENEFITS_GENERAL_CONFIGURATION"
task_code: "BEN_MANAGE_LEGAL_ENTITY_INFORMATION"
task_name: "Configure Default Benefits Relationships"
parent_skill_id: "hcm.benefits-configuration.benefits-general-configuration"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM benefits configuration pillar team"
version: "0.1.0"
inputs:
  - "country"
  - "usage"
  - "from_date"
  - "to_date"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "resolved_fsm_csv_row"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/configure-default-benefits-relationships/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-general-configuration/configure-default-benefits-relationships/current/"
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

# Configure Default Benefits Relationships Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Configure Default Benefits Relationships` under `Benefits General Configuration`.

## Setup Task Skill Contract

- task_code: `BEN_MANAGE_LEGAL_ENTITY_INFORMATION`
- task_name: `Configure Default Benefits Relationships`
- parent_skill_id: `hcm.benefits-configuration.benefits-general-configuration`
- pillar: `HCM`
- offering: `Benefits Configuration`
- functional_area: `Benefits General Configuration`
- functional_area_code: `ORA_BENEFITS_GENERAL_CONFIGURATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Configure Default Benefits Relationships` under `Benefits General Configuration`.

## Restricted User Input Contract

Accept only the following user-supplied values for each default-benefits
relationship row:

| User input | Required | Format and rule |
|---|---|---|
| Country | Yes | Full country name; resolve it through the Territory LOV before preparing the FSM CSV. |
| Usage | Yes | Benefits system usage meaning; resolve it through the common lookup LOV before preparing the FSM CSV. |
| From Date | Yes | Date in `YYYY-MM-DD` format. |
| To Date | Yes | Date in `YYYY-MM-DD` format and not earlier than From Date. |

Do not accept user input for any other `ORA_BENEFIT_PROGRAM_LEGAL_ENTITY_DEFAULTS.csv`
column. Preserve the template header and apply the required system defaults and
derived benefit relation name below.

Reject a request that supplies any value for `AddPriAsgnTreatCd`,
`MultiAssignmentFlag`, `AddAsgnTreatCd`, or `BenefitRelationName`. These are
system-controlled columns: the first three use the required defaults and
`BenefitRelationName` is derived only from the resolved product code.

## Reference Lookups and FSM CSV Mapping

Perform the following read-only lookups through
`core.fusion-api.rest-api-client`, with `REST-Framework-Version: 9`, before
building the FSM CSV row. These lookups validate and translate user-facing
values; they do not authorize an import.

| User input | Read-only Fusion lookup | Exact-match rule | Resolved value | FSM CSV column |
|---|---|---|---|---|
| Country | `GET /fscmRestApi/resources/11.13.18.05/territoriesLOV` | Retrieve `TerritoryShortName` and `TerritoryCode`; require exactly one row whose `TerritoryShortName` exactly equals the supplied Country. | `TerritoryCode` | `LegislationCode` |
| Usage | `GET /fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=BEN_SYS_CODE` | Retrieve `Meaning` and `LookupCode`; require exactly one row whose `Meaning` exactly equals the supplied Usage. | `LookupCode` | `ProductCd` |
| From Date | No lookup | Validate the supplied date. | Supplied From Date | `DateFrom` |
| To Date | No lookup | Validate the supplied date and require it to be on or after From Date. | Supplied To Date | `DateTo` |

Follow all returned pages before deciding that a lookup has zero, one, or more
than one exact match. A zero or multiple match, an invalid date, a reversed
date range, an authentication or authorization failure, or an unexpected
response shape blocks CSV preparation. Never select the first LOV result or
substitute a country or usage code supplied by the user.

The resulting `ORA_BENEFIT_PROGRAM_LEGAL_ENTITY_DEFAULTS.csv` row is limited
to this mapping:

| FSM CSV column | Source |
|---|---|
| `LegislationCode` | `TerritoryCode` returned for Country |
| `ProductCd` | `LookupCode` returned for Usage from lookup type `BEN_SYS_CODE` |
| `DateFrom` | Validated From Date |
| `DateTo` | Validated To Date |

## Required FSM Defaults and Benefit Relation Name

Always populate these FSM CSV attributes with the stated values. They are
system defaults, not user inputs, and may not be overridden.

| FSM CSV column | Required value |
|---|---|
| `AddPriAsgnTreatCd` | `Y` |
| `MultiAssignmentFlag` | `N` |
| `AddAsgnTreatCd` | `DEFAULT` |

Derive `BenefitRelationName` from the resolved `ProductCd` only:

| Resolved `ProductCd` | `BenefitRelationName` |
|---|---|
| `BEN_OAB` | `DFLT` |
| `BEN_UNRST` | `UNRST` |

If the resolved product code is not listed, stop before CSV preparation; do
not invent a benefit relation name or accept one from the user.

## Setup Task Metadata

- Task name: `Configure Default Benefits Relationships`
- Task code: `BEN_MANAGE_LEGAL_ENTITY_INFORMATION`
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

- Offering: `Benefits Configuration`
- Functional area / Setup Object: `Benefits General Configuration`
- Setup task name: `Configure Default Benefits Relationships`
- Setup task code: `BEN_MANAGE_LEGAL_ENTITY_INFORMATION`




## Inputs

- `country`
- `usage`
- `from_date`
- `to_date`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `resolved_fsm_csv_row`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.benefits-configuration.benefits-general-configuration` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
