---
skill_id: "cx.customer-data-management.trading-community-foundation.manage-trading-community-common-lookups"
name: "Manage Trading Community Common Lookups Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Trading Community Common Lookups under the Trading Community Foundation functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "HZ_MANAGE_TRADING_COMMUNITY_COMMON_LOOKUPS"
task_name: "Manage Trading Community Common Lookups"
parent_skill_id: "cx.customer-data-management.trading-community-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX customer data management pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-trading-community-common-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-trading-community-common-lookups/current/"
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

# Manage Trading Community Common Lookups

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Trading Community Common Lookups` under `Trading Community Foundation`.

## Setup Task Skill Contract

- task_code: `HZ_MANAGE_TRADING_COMMUNITY_COMMON_LOOKUPS`
- task_name: `Manage Trading Community Common Lookups`
- parent_skill_id: `cx.customer-data-management.trading-community-foundation`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Trading Community Foundation`
- functional_area_code: `ORA_HZ_CDM_FOUNDATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Trading Community Common Lookups` under `Trading Community Foundation`.

## Setup Task Metadata

- Task name: `Manage Trading Community Common Lookups`
- Task code: `HZ_MANAGE_TRADING_COMMUNITY_COMMON_LOOKUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task.

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Route every import exclusively through `core.data-loader`.
5. For an FSM ZIP, preserve the archive unchanged, require the exact case-sensitive member basename `ASM_SETUP_CSV_METADATA.xml`, and require exactly one metadata task identity equal to `HZ_MANAGE_TRADING_COMMUNITY_COMMON_LOOKUPS`.
6. Let Core Data Loader prepare the final immutable upload artifact, then invoke its `data-load` Task Hook immediately before approval and upload. Require the Task Hook validation envelope to remain bound to that archive's SHA-256.
7. Require the user's separate explicit approval of the exact immutable preview. Any source, archive, environment, task identity, validation result, or approval change restarts the Core Data Loader and Task Hook lifecycle.
8. Core Data Loader owns UCM upload, initiation payload construction, endpoint and FSM routing selection, accepted-request reporting, and later status diagnostics. This pillar skill must not select an adapter, endpoint, loader routing field, or retry policy.

Use this task metadata:

- Offering: `Customer Data Management`
- Functional area / Setup Object: `Trading Community Foundation`
- Setup task name: `Manage Trading Community Common Lookups`
- Setup task code: `HZ_MANAGE_TRADING_COMMUNITY_COMMON_LOOKUPS`

## Inputs

- `natural_language_request`
- `fusion_environment_context`
- `lookup_type_or_meaning`
- `lookup_code_and_named_changes`
- `setup_data_artifact`
- `project_id`

## Outputs

- `lookup_result`
- `setup_data_result`
- `diagnostics`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.customer-data-management.trading-community-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Ownership and review

- Owner: CX Customer Data Management pillar team.
- Functional reviewer: CX Customer Data Management Pillar Lead or a Trading Community Foundation SME.
- Framework reviewer: FSCR A-Team/core reviewer.
- QA reviewer: required when lookup read, mutation, validation, export, or import behavior changes.

Reviewer guidance is in the body because the current manifest schema has `owner_team` but no reviewer field.

## Task-specific lookup baseline

| Lookup type | Meaning or scope | Configuration level | Evidence and restriction |
|---|---|---|---|
| `CODE_STATUS` | Code Status | System (`S`) | Fixed OOTB task member; Standard lookup. |
| `CONTACT_TYPE` | Contact Method | User (`U`) | Fixed OOTB task member; Standard lookup. |
| `CONTACT_USAGE` | Contact Usage | User (`U`) | Fixed OOTB task member; Standard lookup. |
| `DATA_CLOUD_STATUS` | Enrichment Status | System (`S`) | Fixed OOTB task member; Standard lookup. |
| `HZ_COMPOSITE_EVENT_TRACKING` | Composite Events | System (`S`) | Fixed OOTB task member; Standard lookup. |
| `HZ_CREATED_BY_MODULES` | Trading Community Architecture Created By Module | Extensible (`E`) | Fixed OOTB task member; Standard lookup. |
| `HZ_FORMAT_DELIMITERS` | Name and Address Format Delimiter | System (`S`) | Fixed OOTB task member; Standard lookup. |
| `HZ_NAME_INTERFACE_COLUMNS` | Name Interface Column | System (`S`) | Fixed OOTB task member; Standard lookup. |
| `HZ_NUMBERING_MGMT_OPTIONS` | Numbering Management Options | System (`S`) | Fixed OOTB task member; Standard lookup. |
| `HZ_PARTY_CERT_LEVEL` | Party Certification Level | User (`U`) | Fixed OOTB task member; Standard lookup. |
| `HZ_PARTY_CERT_REASON` | Party Certification Reason | User (`U`) | Fixed OOTB task member; Standard lookup. |
| `HZ_PREFERENCE` | Party Preferences | User (`U`) | Fixed OOTB task member; Standard lookup. |
| `HZ_STATUS` | Record Status | System (`S`) | Fixed OOTB task member; Standard lookup. |
| `HZ_STYLE_ENTITIES` | Style Entity | System (`S`) | Fixed OOTB task member; Standard lookup. |
| `MAX_NO_OF_INTERACT_UOM_CODE` | Unit of Measure for Interaction | User (`U`) | Fixed OOTB task member; Standard lookup. |
| `MONTH` | Month | System (`S`) | Fixed OOTB task member; Standard lookup. |
| `OWNER_TABLE_NAME` | Owner Table Name | System (`S`) | Fixed OOTB task member; Standard lookup. |
| `OWN_RENT_IND` | Property Ownership Indicator | User (`U`) | Fixed OOTB task member; Standard lookup. |
| `PARTY_TYPE` | Party Type | System (`S`) | Fixed OOTB task member; Standard lookup. |
| `PREFERENCE_CODE` | Contact Preference Code | User (`U`) | Fixed OOTB task member; Standard lookup. |
| `PREFERENCE_TOPIC_TYPE` | Preference Topic Type | User (`U`) | Fixed OOTB task member; Standard lookup. |
| `REASON_CODE` | Reason Code | User (`U`) | Fixed OOTB task member; Standard lookup. |
| `REGISTRY_STATUS` | Registry Status | System (`S`) | Fixed OOTB task member; Standard lookup. |
| `REQUESTED_BY` | Requested By | User (`U`) | Fixed OOTB task member; Standard lookup. |
| `SUBJECT_TABLE` | Subject Table | Extensible (`E`) | Fixed OOTB task member; Standard lookup. |
| `TCA_OWNER_TABLE` | Owner Table | System (`S`) | Fixed OOTB task member; Standard lookup. |

This is a closed 26-type OOTB inventory established by the exact-task Fusion UI and reconfirmed by read-only GETs from the configured environment. The task does not provide an operation for adding a lookup type. All 26 types resolve through `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}`. A current GET must reconfirm the category and configuration level before a live operation. Missing or changed evidence is `catalog_or_metadata_mismatch`; never add a type based on prefix, module, or meaning. See [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md).

Current Oracle Sales REST consumer descriptions also associate `ZCA_COMMON_RATE_TYPE` and `ZCA_COMMON_CORPORATE_CURRENCY` with this setup task, but neither appears in the reviewed exact-task 26-type inventory. Treat both as unresolved evidence rather than task members: do not list or mutate them through this skill until an exact-task page, immutable task export, or other authoritative task-membership source reconciles the difference.

## Supported and unsupported operations

| Request | Support |
|---|---|
| List lookup types belonging to this task | Return the closed 26-type baseline and current read results; never add a task member. |
| Show codes and values or retrieve one exact code | Read-only, no approval, after exact task membership and lookup-category resolution. |
| Create a custom code | Conditional for a confirmed User type or an allowed Extensible custom code after duplicate, seed, configuration, and describe checks. |
| Update a lookup type | Conditional at the intersection of configuration-level rules and current REST describe; identity, category, configuration, module, and REST-security fields remain protected. |
| Update a lookup code | Conditional at the intersection of configuration-level rules, seeded origin, and current REST describe. |
| Delete a code | Conditional only for a proven custom code in a confirmed User or permitted Extensible type. |
| Export task setup data | Supported through `shared.setup-export.task-level-export` because the exact catalog CSV flag is `Y`. |
| Validate and import task setup data | Supported through `core.data-loader` only after shared validation, Task Hook validation of the exact immutable archive, and separate explicit approval. |
| Change lookup type/code identity, configuration level, category, module, REST security, or seeded identity | Unsupported; refuse before preview. |
| Add or delete a lookup type | Unsupported; the task inventory is fixed. |

Never silently upsert. Reject a custom code beginning with `ORA_`. Treat `CreatedBy == SEED_DATA_FROM_APPLICATION` as seeded-origin evidence. `LastUpdatedBy` identifies only the most recent updater and must never convert a seeded code into a custom code.

## Configuration-level and manual mutation contract

- System: no code creation/deletion, enabled-state, date, display-sequence, description, tag, or structural change. Permit only `Meaning` when current REST describe also marks it updatable.
- Extensible: permit `Meaning`, `Description`, and `DisplaySequence` when current REST describe supports them. Permit `EnabledFlag`, `StartDateActive`, and `EndDateActive` only for proven custom codes. Permit custom-code creation/deletion after seeded-origin checks. Do not update `Tag` or seeded identity.
- User: permit REST-described `Meaning`, `Description`, `DisplaySequence`, `EnabledFlag`, `StartDateActive`, `EndDateActive`, and `Tag`. Permit supported custom-code creation/deletion, keep identities immutable, and never classify a seeded-origin code as custom.
- Category is `standardLookups` for all 26 confirmed members. If a current exact GET no longer resolves there, stop; do not fall through to another category.
- Build every PATCH from only the named fields allowed by the exact configuration level and current REST describe. Never include `ModuleId`, `RestAccessSecured`, `CustomizationLevel`, `LookupType`, or `LookupCode` in a PATCH.

Every manual mutation must:

1. Resolve exactly one configured Fusion environment.
2. GET the exact lookup type and exact code when applicable.
3. Retrieve or use current cached describe metadata for the resolved resource family.
4. Validate task membership, Standard category, configuration level, `CreatedBy` seeded origin, reserved prefix for creation, and current REST-described writable fields.
5. Show one exact redacted preview containing environment, method, endpoint, before/after values, payload, impact, and preview fingerprint.
6. Require explicit approval bound to that environment, target, method, payload, and fingerprint.
7. Send exactly one POST, PATCH, or DELETE through `core.fusion-api.apps-common` and `core.fusion-api.rest-api-client`.
8. Never automatically retry a mutation and never enable upsert.
9. Verify with a separate GET.
10. Report verified success, unverified success, refusal, or classified failure distinctly.

Read-only listing and retrieval require no approval.

## Task CSV export contract

Route export to `shared.setup-export.task-level-export` with exact `TaskCode: HZ_MANAGE_TRADING_COMMUNITY_COMMON_LOOKUPS`. The owning exporter must create one task CSV export, capture and monitor its `ProcessId`, download immutable `FileContent` only after success, retrieve `ProcessLog` after failure, and save the ZIP or diagnostic under the supplied project workspace. Do not implement export HTTP, polling, or ZIP processing here.

## FSM ZIP validation and import contract

1. Run `shared.validation.setup-data-validator` and `shared.validation.reference-data-validator` for task-local setup and reference checks.
2. Route the import only to `core.data-loader`; this pillar skill supplies the exact task context and rules but never selects or invokes an import adapter or endpoint.
3. Detect an FSM ZIP only when a member has the exact case-sensitive basename `ASM_SETUP_CSV_METADATA.xml`.
4. Reject missing, duplicate, unreadable, encrypted, unsafe-path, or ambiguous metadata.
5. Parse metadata without rewriting the archive and require exactly one task identity equal to `HZ_MANAGE_TRADING_COMMUNITY_COMMON_LOOKUPS`.
6. Preserve the archive bytes and SHA-256 through validation, Task Hook preview, approval, and execution.
7. After Core Data Loader prepares the final immutable upload artifact, require its `data-load` Task Hook to evaluate this task's compiled `ora-resource` rules and issue the validation envelope bound to the exact archive SHA-256.
8. Require a later standalone explicit approval of that exact immutable preview. A changed source, archive, environment, task identity, rule result, or approval invalidates the envelope and restarts validation.
9. Let Core Data Loader own UCM upload, FSM initiation routing and payload construction, accepted-request reporting, and any later status or ProcessLog retrieval. Do not reconstruct its envelope or locally choose an endpoint, adapter, routing field, or retry behavior.
10. Submit only once under the current Core Data Loader contract. If Task Hook validation or approval is missing, stale, or mismatched, stop with `approval_blocker` before any POST.
11. Treat a later Run Book or Journey `updateProgress` failure as a separate synchronization result. Do not change an accepted FSM import to failed, and never retry or resubmit the import because progress synchronization failed.

## Natural prompts

- `Show the Trading Community Common Lookups in the configured environment.`
- `Show the values for <lookup meaning or exact lookup type>.`
- `Add lookup code <code> with meaning <meaning> to <lookup type>.`
- `Change the meaning of <code> in <lookup type>.`
- `Set the display sequence of <code> in <lookup type> to <number>.`
- `Disable <code> in <lookup type>.`
- `Delete custom lookup code <code> from <lookup type>.`
- `Export Manage Trading Community Common Lookups setup data.`
- `Validate and import this Manage Trading Community Common Lookups export.`

Resolve an unambiguous request directly; do not ask the user to choose an internal operation name.

## Error and diagnostic contract

| Failure class | Use |
|---|---|
| `input_validation` | Missing environment, invalid code/date/flag, field disallowed by configuration or current REST describe, changed artifact, or unsafe ZIP. |
| `catalog_or_metadata_mismatch` | Task membership, category, level, describe, exact TaskCode, CSV flag, or adapter contract cannot be proven. |
| `auth_expired_or_invalid` | Cached authentication rejected; refresh once only under repository cache policy. |
| `authorization_or_privilege` | Access remains denied or the task/resource privilege is missing. |
| `transport_or_environment` | Environment, VPN, DNS, or connection failure. Retry only bounded reads. |
| `fusion_api_error` | Fusion rejects the one approved request; report status and ECID when available. |
| `process_timeout` | Export/import polling window expires; preserve TaskCode, ProcessId, last status, and next-check path. |
| `process_failed` | Export/import completes with errors; preserve ProcessLog/status and partial results. |
| `artifact_persistence` | A required ZIP, diagnostic, result, run record, or token log cannot be saved. |
| `approval_blocker` | Preview is missing, stale, changed, or declined. |

Durable diagnostics include status, stage, failure class, message, recommended action, environment, redacted endpoint, artifact references, ProcessId/ECID, completed checks, and verified side effects. Never persist credentials, tokens, authorization headers, customer data, signed URLs, or sensitive payloads.

## Synthetic behavior checks

| Scenario | Expected result |
|---|---|
| General task read | Return exactly the closed 26-type baseline and current read results; do not infer additions. |
| System field other than Meaning | Refuse before preview even if generic REST describe marks it updatable. |
| Configuration-and-describe-supported update | Exact GET, Standard category/level/seed/describe validation, one preview, approval, one PATCH, and separate GET verification. |
| Wrong-task FSM ZIP | Refuse before import because metadata does not equal `HZ_MANAGE_TRADING_COMMUNITY_COMMON_LOOKUPS`. |
| Task-local import route selection | Refuse before POST; Core Data Loader owns endpoint, adapter, routing-field, and retry selection. |
| Missing or stale Task Hook validation envelope | Fail closed with `approval_blocker`; do not upload, initiate, or reconstruct an envelope. |
| Valid exact-task FSM archive | Preserve bytes and hash, pass exact task context to Core Data Loader, complete Task Hook validation and separate approval, then let Core Data Loader execute once. |

## Persistence

When `project_id` is supplied, persist artifacts under the manifest paths, append a run record under `project/{project_id}/state/runs`, and append token usage under the shared token log. Repository-only authoring does not create a project workspace. Fail closed when required authority, membership, category, metadata, privilege, adapter, approval, or safe destination evidence is absent.
