---
skill_id: "hcm.global-human-resources.locations.manage-locations"
name: "Manage Locations Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Locations under the Locations functional area. Use when the user asks to plan, validate, or execute this task's declared scope; do not use it for unrelated HCM configuration."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Locations"
functional_area_code: "ORA_LOCATIONS"
task_code: "PER_MANAGE_LOCATIONS"
task_name: "Manage Locations"
parent_skill_id: "hcm.global-human-resources.locations"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "Location"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
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
  - "hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
  - "core.fusion-api.ess-job-submitter"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
  - "core.fusion-api.ess-job-submitter"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
oracle_supplied_guidance_files:
  - purpose: "Input validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Reference resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Defaulting rules"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Design enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Failure handling"
    location: "ora-resource/ora_error_handling.md"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/locations/manage-locations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/locations/manage-locations/current/"
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
  - "May enable the required Oracle Search profile values through their owning task."
  - "May submit and monitor the declared Oracle Search ESS processes."
required_privileges: []
---

# Manage Locations Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Locations` under `Locations`.

## Task Overview

Use this task to plan and govern `Manage Locations` configuration in Global Human Resources.

- **Task identity:** `PER_MANAGE_LOCATIONS` — Manage Locations.
- **Scope:** HCM → Global Human Resources → Locations.
- **Catalog routing:** CSV export/import support is `Y`; the declared Data Loader mode is `REST` with `Location`.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `PER_MANAGE_LOCATIONS`
- task_name: `Manage Locations`
- parent_skill_id: `hcm.global-human-resources.locations`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Locations`
- functional_area_code: `ORA_LOCATIONS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `Location`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and Location source data
must be authored, validated, or submitted.

1. Confirm `Location` as the exact registered Data Loader business object.
2. Generate the editable XLSX, attribute-details workbook, and key-fields workbook through `core.data-loader` using current live metadata. Keep those three artifacts together for the same authoring pass.
3. Treat the live workbook sections as the complete schema for this task: `Location`, `LocationOtherAddress`, `LocationExtraInfo`, and `LocationLegislative`. Do not invent a section, omit a supplied section from schema review, or reuse a stale template.
4. Before a CUD handoff, reconcile every supplied attribute in every included section to one exact attribute in that section's live attribute-details sheet. Resolve its value, data type, reference/lookup contract, key role, and applicable effective-date/context rule. For an edit or delete, include the live surrogate key for every edited object exposed by its actual section: `LocationId`, `LocationExtraInfoId`, or `LocationLegId`; resolve `LocAddressUsageId` as address evidence, but never emit a MAIN address as `LocationOtherAddress`. Block unknown, ambiguous, duplicate-target, response-only, or unresolved attributes; do not rely on REST write payload construction.
5. Author MAIN address values on the `Location` row for create and MAIN-address edit. Resolve the country-specific layout first and map only returned layout attributes to current `Location` loader headers. Use `LocationOtherAddress` only for an explicitly requested non-MAIN additional-address edit, keyed by its `LocAddressUsageId`.
6. Include `LocationOtherAddress`, `LocationExtraInfo`, or `LocationLegislative` only when the user explicitly changes that object. For an included EFF object, resolve the current context and every supplied segment against its matching live section; use `HCM_LOC` for `LocationExtraInfo` and `HCM_LOC_LEG` for `LocationLegislative`. Require `FLEX:PER_LOCATION_INFORMATION_EFF` to equal that row's `LeiInformationCategory` and `FLEX:PER_LOCATION_LEG_EFF` to equal that row's `LleInformationCategory`; `Global Data Elements` is valid only when it is the row's resolved context. EFF segment names, labels, data types, lengths, precision, allowed values, and values are dynamic: never hardcode a segment name or infer a segment contract from a prior location or prior run.
7. Carry the resolved Location identity, selected reference-data set, effective date, and any resolved reference values into each included row. For edits, never omit a live surrogate object ID: resolve and carry `LocationId`, `LocationExtraInfoId`, and `LocationLegId` for edited rows; retain `LocAddressUsageId` in the address-resolution evidence, but do not place it in a MAIN child row. User-key alternatives alone are create-only for this task's edit contract.
8. Write Data Loader dates in `YYYY/MM/DD` format. For create or edit, apply the requested `EffectiveStartDate` to the base row and each included child or EFF row. For date-effective delete, the requested date identifies the history row to remove; the root MERGE dates are instead the predecessor start and selected end derived from complete history.
9. For a date-effective edit, never copy, preserve, or default the prior or create `ActionReasonCode`. The action reason is optional: omit it unless the user explicitly supplies an update reason, then resolve that supplied value independently as valid for the new effective date.
10. When `ShipToSiteFlag` is `Y`, omit `ShipToLocationId`, `ShipToLocationCode`, and `ShipToLocationSetCode`. When it is `N`, supply either one resolved `ShipToLocationId` or the resolved pair `ShipToLocationCode` and `ShipToLocationSetCode`; block partial, conflicting, copied, or unresolved references.
11. For root `Location.TimezoneName`, start from the selected MAIN-address `TimezoneCode`, match exactly one enabled `timezonesLOV` row, and write that row's exact `Name`. Never write the code, `LongName`, `ShortName`, or the `locationsV2` display text to `TimezoneName`. Do not author MAIN time zone through `LocationOtherAddress.TimezoneCode`.
12. Submit the reviewed XLSX to `core.data-loader`; it removes columns blank in every authored data row, validates every included section and header against the same live schema, converts the frozen workbook to DAT internally, and rejects any generated DAT line over Fusion's 4000-character limit. DAT is not the authored approval source.
13. Follow `core.data-loader` source-key, mapping, validation, immutable preview, and approval guidance. A CUD may be posted only after this all-section, all-supplied-attribute reconciliation passes, every supplied value satisfies its current live type/length/precision/allowed-value contract, and the immutable preview is approved.

## Date-Effective Location Delete

Location does not support ZAP or a root `DELETE` Data Loader operation. Reject a ZAP or physical-delete request during intake as `UNSUPPORTED`: do not resolve history, build a loader artifact, request approval, or invoke `core.data-loader`. A supported delete request is only a date-effective deletion of one explicitly selected non-first Location history split.

1. Read every page of `hcmDateEffectiveObjectHistory` using `LocationHistoryDef`, and resolve exactly one user-selected `EffectiveStartDate`. Require its `FirstSplitFlag` to be false and resolve its immediately preceding history row.
2. Build the delete range from history, not from the selected row alone: set the root `Location` MERGE `EffectiveStartDate` to the predecessor's start and `EffectiveEndDate` to the selected row's end. Never delete the first history row.
3. Generate the full current Location workbook with exactly one `Data Loader Directives` instruction, `SET PURGE_FUTURE_CHANGES Y`, and exactly one root `Location` MERGE row. The row must carry the fresh root identity tuple `LocationId`, `SetCode`, and `LocationCode`, plus the derived date range. `LocationId` alone is not a valid date-effective-delete source: the runtime Location translation entity requires `LocationCode`; retain the resolved `SetCode` with it. Do not include `ActionReasonCode`, address, `LocationOtherAddress`, ExtraInfo, Legislative, or any changed business values.
4. Reject a root `DELETE` row, a ZAP request, an unbounded range, a selected first split, incomplete history, or any mixed MERGE/DELETE source for the Location. After the load, re-read complete history: removed starts must be absent, the predecessor must extend to the derived end, and all other rows must be unchanged.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Locations` under `Locations`.

## Setup Task Metadata

- Task name: `Manage Locations`
- Task code: `PER_MANAGE_LOCATIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `Location`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `Location` as the BusinessObject.

## CRUD Routing

- Run export only when explicitly requested.
- Read and name-fragment searches use `/hcmRestApi/resources/{version}/locationsV2`.
- For create, edit, or delete, run applicable declared reads and task rules, then invoke `core.data-loader` with the task metadata, project context, business object, operation, and resolved business values. Follow it through immutable ZIP preview without stopping at an intermediate step, then wait for standalone `approve`; ask only for unresolved business input.
- For a name-fragment search, pass the user-supplied value to the documented `like` filter; never hardcode a search term.

## Oracle Search Ingestion

When Oracle Search setup or re-ingestion is explicitly requested, perform these steps in order:

1. Resolve site-level `HRC_ELASTIC_SEARCH_ENABLED` through `hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values` and site-level `ORA_PER_ORACLE_SEARCH_LOCATIONSLOV_ENABLED` through the same task.
2. Before any side effect, prepare an immutable execution plan containing the target environment; each profile option's current and requested site value (include a profile write only when the current value is not `Y`); the initial-ingestion payload `JobDefinition://oracle/apps/ess/fnd/applcore/FndOSCSIndexIngestJob`, `application=FscmEss`, and `submit.argument1=fa-hcm-location`; the ACL payload `JobDefinition://oracle/apps/ess/hcm/users/ComputeUsersACL`, `application=EarHcmEss`, `submit.argument1=LOGGED_IN_USERS`, and `submit.argument2=N`; polling window and interval; and the `/hcmRestApi/resources/latest/locationsLovV2` verification.
3. Obtain one explicit batch approval immediately before the first profile write or ESS submission. That approval authorizes only the immutable plan's required profile updates, the two named ESS submissions, their polling, and final verification. Do not ask again between those approved steps.
4. Execute continuously: update and re-read each included profile value; submit **ESS job to create index definition and perform initial ingest to OSCS**, then poll its exact request ID at the approved interval until a terminal status; only after a successful terminal status, submit **Compute Users ACL** and poll its exact request ID at the approved interval until a terminal status; only after both terminal statuses are successful, read `/hcmRestApi/resources/latest/locationsLovV2` and require returned results.

The batch approval satisfies delegated profile-value and ESS approval gates only for the exact plan. Stop on a rejected, failed, timed-out, or uncertain profile update or ESS process; do not continue, substitute another route, or retry automatically. A changed payload, a new mutation, or any retry requires a fresh approval. Persist both ESS request IDs and terminal results.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Locations`
- Setup task name: `Manage Locations`
- Setup task code: `PER_MANAGE_LOCATIONS`




## Uniform Authoring and Read Contract

- Interpret each supplied business attribute within its intended parent or child section using the current operation-specific Data Loader metadata and REST `describe`. Match the exact technical name first, then an exact normalized display label or declared alias, then one unique case-, space-, and punctuation-insensitive match. If multiple fields remain plausible, show their business labels and ask the user to choose; if none match, report the field as unsupported. Never guess or copy a value between fields.
- For create or edit, map only resolved user values to the exact business-object section, resolve references through declared task resolvers, preserve omitted existing values, and author only requested or operation-required rows and fields through the existing mutation route.
- Determine mandatory input only from current operation-specific metadata and operation-required business identity. Never require or populate a nonmandatory field merely because it appears in a template, example, or response. EFF or Additional Information contexts and segments are always optional and must never be requested as a prerequisite; emit an EFF row only when the user explicitly requests that change, using only its resolved context, identity, changed values, and any fields current metadata requires for that included row.
- Never hard-code a business value from an example. Apply a fixed default only when the task defaulting rules and current metadata confirm it for the exact operation; otherwise omit an optional field or ask only when current metadata marks it required. Fixed technical discriminators are allowed only where the task contract requires them to identify the exact business-object section.
- For a normal read, present business-facing labels and values. Do not show WHO or history columns such as `CreatedBy`, `CreationDate`, `LastUpdatedBy`, `LastUpdateDate`, or `LastUpdateLogin`, or primary/surrogate identifiers, unless the user explicitly asks for them; retain identifiers internally for linking and mutation.
- When the user asks for complete details, read the exact parent without a restrictive field projection, expand every task-supported child or EFF collection by following server-returned links, paginate every collection, and return all current business attributes and child values after the same WHO/ID filtering. State when no supported child collection exists or none is returned; never invent a child path.

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

Use the parent functional-area skill `hcm.global-human-resources.locations` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.
