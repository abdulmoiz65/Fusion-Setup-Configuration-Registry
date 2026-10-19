---
skill_id: "erp.financials.legal-structures.manage-legal-reporting-unit"
name: "Manage Legal Reporting Unit Setup Task Guidance"
description: "Prepares and validates country-level Legal Reporting Unit setup with optional explicit jurisdiction and registration under Legal Structures."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Legal Structures"
functional_area_code: "ORA_ASK_LEGAL_STRUCTURES"
task_code: "XLE_MANAGE_LEGAL_REPORTING_UNIT"
task_name: "Manage Legal Reporting Unit"
parent_skill_id: "erp.financials.legal-structures"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.2.1"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/legal-structures/manage-legal-reporting-unit/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/legal-structures/manage-legal-reporting-unit/current/"
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
  - "Creates scoped export processes and downloads baseline packages through the selected shared export workflow."
  - "Performs routed read-only Fusion reference lookups and prepares local FSM archives; core.data-loader owns approved upload and import."
required_privileges:
  - "Fusion privileges to create and retrieve setup task CSV exports."
  - "Read access to the legal-entity, territory, address-geography, jurisdiction, and legal-reporting-unit references used by the applicable branch."
---

# Manage Legal Reporting Unit Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Legal Reporting Unit` under `Legal Structures`.

## Setup Task Skill Contract

- task_code: `XLE_MANAGE_LEGAL_REPORTING_UNIT`
- task_name: `Manage Legal Reporting Unit`
- parent_skill_id: `erp.financials.legal-structures`
- pillar: `ERP`
- offering: `Financials`
- functional_area: `Legal Structures`
- functional_area_code: `ORA_ASK_LEGAL_STRUCTURES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Legal Reporting Unit` under `Legal Structures`.

### Supported Creation Scope

Create country-level LRUs under an existing parent legal entity. Resolve the selected country through `territoriesLOV` and `addressGeographies` using the lookup rules in [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md). Country geography code and its matching transient must be populated; non-country territories remain outside this creation scope until the blank-code import/re-export test in [ora_design_enforcement.md](ora-resource/ora_design_enforcement.md) is validated.

Jurisdiction is optional. Omitted or blank means null: do not default it and do not add a registration child. If explicitly supplied, resolve it without an identifying-only restriction and require a registration number and one legal address from the fresh scoped export. Ask the user to choose among ambiguous candidates. Jurisdiction-to-LRU-geography association is not checked in this scope and must not introduce another confirmation gate.

Use a fresh parent-scoped export for the unchanged parent, package contract, existing-row checks, and any selected legal address. Do not require unrelated existing LRUs or sample addresses, and do not copy the parent jurisdiction or country into the new LRU as defaults. A suitable exported parent address can be reused when the registration branch applies.

## Setup Task Metadata

- Task name: `Manage Legal Reporting Unit`
- Task code: `XLE_MANAGE_LEGAL_REPORTING_UNIT`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Resolve the existing parent legal entity or explicit parent set, then export setup task data with `shared.setup-export.task-level-export` using the ordered scoped request below. Verify scope metadata and root rows before accepting the baseline.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Load the task-local `ora-resource/ora_rule_registry.json` and run its referenced input, lookup, dependency, defaulting, design, error-handling, and final-package-readiness checks. The ora-resource graph validates the candidate; it does not create a Fusion mutation.
5. Prepare the FSM archive locally using the contract below.
6. Hand the exact final archive to `core.data-loader` only after the local workflow returns `READY_FOR_DATA_LOADER_PREVIEW`.

Use this task metadata when invoking those skills:

- Offering: `Financials`
- Functional area / Setup Object: `Legal Structures`
- Setup task name: `Manage Legal Reporting Unit`
- Setup task code: `XLE_MANAGE_LEGAL_REPORTING_UNIT`

### Scoped Export Order and Multiple Parents

Resolve each requested parent through `verify_lru_parent_entity` before export.
Use the returned numeric `LegalEntityId` as the string `AttributeValue` for
`BusinessObjectCode: XLE_ENTITY_PROFILE` and `AttributeName: LEGAL_ENTITY_ID`.
The CSV parent key remains `LegalEntityIdentifier`; neither that identifier nor
the display name replaces the physical scope ID in the REST request.

For one parent, send only `Set1`. For several explicitly selected parents,
send one criterion per distinct parent ID, using `Set1`, `Set2`, and so on.
Each LRU input still resolves to exactly one parent; a combined export must
not cause global name matching or cross-parent row/address inheritance.
Do not add an LRU-level filter for new-LRU creation: the parent scope supplies
the existing siblings needed for collision and main-history checks.

Send `POST /fscmRestApi/resources/11.13.18.05/setupTaskCSVExports` with root keys
in this exact serialized order: `TaskCode`, `SetupTaskCSVExportCriteria`,
`SetupTaskCSVExportProcess`. Criteria and process are root siblings. Preserve
insertion order and do not sort JSON keys. The two numeric IDs below are
illustrative; replace both with IDs resolved in the selected environment:

```json
{
  "TaskCode": "XLE_MANAGE_LEGAL_REPORTING_UNIT",
  "SetupTaskCSVExportCriteria": [
    {
      "TaskCode": "XLE_MANAGE_LEGAL_REPORTING_UNIT",
      "BusinessObjectCode": "XLE_ENTITY_PROFILE",
      "AttributeSet": "Set1",
      "AttributeName": "LEGAL_ENTITY_ID",
      "AttributeValue": "300000000000101"
    },
    {
      "TaskCode": "XLE_MANAGE_LEGAL_REPORTING_UNIT",
      "BusinessObjectCode": "XLE_ENTITY_PROFILE",
      "AttributeSet": "Set2",
      "AttributeName": "LEGAL_ENTITY_ID",
      "AttributeValue": "300000000000102"
    }
  ],
  "SetupTaskCSVExportProcess": [
    { "TaskCode": "XLE_MANAGE_LEGAL_REPORTING_UNIT" }
  ]
}
```

Use the shared task-level exporter with `--data --export-criteria-file` when
creating through its CLI; that file contains only the criteria array, not the
whole body. The shared engine preserves criteria-first root order. The shared
workflow may instead select `core.fusion-api.rest-api-client --body-file` for
the complete ordered body, followed by the shared result helper with only the
returned `ProcessId`. Record the exact body/hash and target before creating a
process. Do not submit another POST to poll, and do not fall back to an
unscoped export if scoped acquisition fails.

After successful download, verify `ASM_SETUP_CSV_METADATA.xml` declares this
task and target/release, and that its scope rows identify
`XLE_ENTITY_PROFILE / LEGAL_ENTITY_ID` with exactly the requested numeric IDs
in `ScopeValueBoAttributeValueCode`. Reconcile these IDs through the resolver
receipt to the complete `LegalEntityIdentifier` set in
`XLE_ENTITY_PROFILE.csv`; require every selected root and reject unexpected
roots. Compare sets, not returned row order. Check child parent keys against that set and partition existing LRU,
registration, collision and history checks by parent. Reject absent, partial,
wrong-task, or broad scope evidence even if Fusion reports success.

`XLE_LE_LEGAL_ADDRESS.csv` is a reference member and can contain addresses
beyond the selected parents. Use its actual rows and the address resolver's
country/ambiguity checks; do not assume every address belongs to every parent
or that all future exports have the same address coverage. Preserve unchanged
rows and metadata when building the candidate archive.

### Local-Only FSM Package Preparation

This assisted workflow prepares a package locally and stops before upload or any Fusion mutation.

1. Require a fresh, same-target, same-release, successful same-task FSM export as the immutable baseline. Bind the exact environment and task identity, current `ASM_SETUP_CSV_METADATA.xml`, exact CSV member hierarchy, exact header spelling and order, and the exported encoding.
2. Re-run the complete task ora-resource graph against the reviewed inputs and baseline. Fail closed with a task-specific package-contract gap if any source, mapping, value, member hierarchy, header, encoding, carrier, country mapping, or parent/child rule is missing or ambiguous; do not invent a package contract.
3. Build the smallest supported country-only delta from the task resources. Preserve the exact unchanged legal-entity parent row; author the supported `XLE_ETB_PROFILE.csv` delta. Add one complete, authority-free registration child only for an explicitly supplied and resolved jurisdiction with registration number and selected exported address; otherwise add no registration child. Add zero candidate rows to `ORA_XLE_LEGAL_REPORTING_UNIT_REGISTRATION_FUNCTION.csv`, preserving any existing rows or the header-only member when empty. Preserve every unrelated row and untouched archive member. Reject non-country geography and never emit a partial registration child.
4. Do not copy physical IDs, audit fields, object-version fields, ESS fields, or service-owned values from the baseline or another row. Copy a value only when the task resources explicitly authorize it as a carrier.
5. Produce a ZIP-valid immutable FSM archive, its SHA-256 digest, a member inventory, a row/member semantic diff against the baseline, and a sanitized package-preparation receipt containing no secrets or sensitive payload values.
6. Any source, mapping, value, package byte, member inventory, or hash change invalidates this preview state and requires the full validation and package-preparation workflow to run again.
7. On success, return `READY_FOR_DATA_LOADER_PREVIEW`. Do not claim `READY_FOR_IMPORT` or approval. Stop before upload or mutation and hand the exact immutable archive to `core.data-loader`, which owns Task Hook validation, preview, explicit approval, archive-hash verification, upload, and initiation.


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

Use the parent functional-area skill `erp.financials.legal-structures` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
