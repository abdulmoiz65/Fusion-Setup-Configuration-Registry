---
skill_id: "cx.sales.accounts-and-contacts.manage-customer-center-lookups"
name: "Manage Customer Center Lookups Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Customer Center Lookups under the Accounts and Contacts functional area."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Accounts and Contacts"
functional_area_code: "ORA_SVC_ACCOUNTS_AND_CONTACTS"
task_code: "ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS"
task_name: "Manage Customer Center Lookups"
parent_skill_id: "cx.sales.accounts-and-contacts"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX sales pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/accounts-and-contacts/manage-customer-center-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/accounts-and-contacts/manage-customer-center-lookups/current/"
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

# Manage Customer Center Lookups Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Customer Center Lookups` under `Accounts and Contacts`.

## Setup Task Skill Contract

- task_code: `ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS`
- task_name: `Manage Customer Center Lookups`
- parent_skill_id: `cx.sales.accounts-and-contacts`
- pillar: `CX`
- offering: `Sales`
- functional_area: `Accounts and Contacts`
- functional_area_code: `ORA_SVC_ACCOUNTS_AND_CONTACTS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Customer Center Lookups` under `Accounts and Contacts`.

## Setup Task Metadata

- Task name: `Manage Customer Center Lookups`
- Task code: `ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS`
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
5. For an FSM ZIP, preserve the archive unchanged, require the exact case-sensitive member basename `ASM_SETUP_CSV_METADATA.xml`, and require exactly one metadata task identity equal to `ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS`.
6. Let Core Data Loader prepare the final immutable upload artifact, then invoke its `data-load` Task Hook immediately before approval and upload. Require the Task Hook validation envelope to remain bound to that archive's SHA-256.
7. Require the user's separate explicit approval of the exact immutable preview. Any source, archive, environment, task identity, validation result, or approval change restarts the Core Data Loader and Task Hook lifecycle.
8. Core Data Loader owns UCM upload, initiation payload construction, endpoint and FSM routing selection, accepted-request reporting, and later status diagnostics. This pillar skill must not select an adapter, endpoint, loader routing field, or retry policy.

Use this task metadata:

- Offering: `Sales`
- Functional area / Setup Object: `Accounts and Contacts`
- Setup task name: `Manage Customer Center Lookups`
- Setup task code: `ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS`

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

Use the parent functional-area skill `cx.sales.accounts-and-contacts` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Ownership and review

- Owner: CX Sales pillar team.
- Functional reviewer: CX Sales Pillar Lead or an Accounts and Contacts SME.
- Framework reviewer: FSCR A-Team/core reviewer.
- QA reviewer: required when lookup read, mutation, validation, export, or import behavior changes.

Reviewer guidance is in the body because the current manifest schema has `owner_team` but no reviewer field.

## Task-specific lookup baseline

| Lookup type | Meaning | Configuration level | Evidence and restriction |
|---|---|---|---|
| `ZCA_ACCOUNT_TYPE` | Type of Account | User | Standard REST returned `U`; permit describe-backed User maintenance. |
| `ZCA_ACCT_SRCH_RECORD_SET` | Sales Account Search Filter Record Sets | User | Standard REST returned `U`; permit describe-backed User maintenance. |
| `ZCA_CONTACT_TYPE` | Type of Contact Account | User | Standard REST returned `U`; permit describe-backed User maintenance. |
| `ZCA_HOUSEHOLD_TYPE` | Type of Household Account | User | Standard REST returned `U`; permit describe-backed User maintenance. |
| `ZCA_RECORD_TYPE` | Record Type attribute values for Customer Picker | User | Standard REST returned `U`; permit describe-backed User maintenance. |
| `ZCA_RESOURCE_FUNCTION` | Team Member Function | User | Standard REST returned `U`; permit describe-backed User maintenance. |
| `ZCA_SALES_ACCOUNT_STATUS` | Sales Account Status | User | Standard REST returned `U`; permit describe-backed User maintenance. |
| `ZMM_NOTE_TYPE` | Note Type | Extensible | Standard REST returned `E`; protect seeded codes and tags. |

Task membership was supplied from the configured Fusion task page and every exact member was independently retrieved from `standardLookups` on 2026-08-07. Official Oracle Sales documentation places this task under Sales, Accounts and Contacts. Reconfirm category and configuration level with a current GET; do not extend the inventory by prefix or module inference. See [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md).

The effective catalog also exposes this task code under Customer Loyalty / Accounts and Contacts and Sales Marketing / Customer Center. This skill intentionally owns only the Oracle-documented Sales / Accounts and Contacts occurrence. Do not route it through Customer Data Management, duplicate its task metadata under another offering, or treat another occurrence as equivalent without explicit catalog-backed orchestration.

## Supported and unsupported operations

| Request | Support |
|---|---|
| List lookup types belonging to this task | Supported for the eight exact baseline members. |
| Show codes/values or retrieve one exact code | Read-only without approval after exact membership and Standard-category resolution. |
| Create a custom code | Conditional for a confirmed User type or a permitted Extensible custom code after duplicate, seed, configuration, and describe checks. |
| Update meaning, description, dates, display sequence, enabled state, or tag | Conditional only for the named field at the strict intersection of Oracle configuration rules and current describe metadata. |
| Delete a code | Conditional only for a proven custom code in a confirmed User or permitted Extensible type. |
| Export task setup data | Supported through `shared.setup-export.task-level-export` because the exact catalog CSV flag is `Y`. |
| Validate and import task setup data | Supported through `core.data-loader` only after shared validation, Task Hook validation of the exact immutable archive, and separate explicit approval. |
| Change lookup type/code identity, configuration level, category, module, security, or seeded identity | Unsupported. |

Never silently upsert. Reject a custom code beginning with `ORA_`. Treat `CreatedBy == SEED_DATA_FROM_APPLICATION` as seeded-origin evidence; use `LastUpdatedBy` only for audit.

## Configuration-level and manual mutation contract

- User (the seven `ZCA_*` types): permit REST-described `Meaning`, `Description`, `DisplaySequence`, `EnabledFlag`, dates, and `Tag`; permit supported custom create/delete after duplicate and seed checks.
- Extensible (`ZMM_NOTE_TYPE`): permit REST-described `Meaning`, `Description`, and `DisplaySequence`; permit state/date/create/delete only for a proven custom code. Do not change `Tag`.
- Keep lookup type and code identity, module, security, configuration level, category, and seeded identity immutable even when a describe field appears writable.

Every manual mutation must:

1. Resolve exactly one configured Fusion environment.
2. GET the exact lookup type and exact code when applicable.
3. Retrieve or use current cached describe metadata for Standard lookup codes.
4. Validate task membership, configuration level, `CreatedBy` seeded-origin evidence, dates, reserved prefix, and named writable fields.
5. Show one exact redacted preview containing environment, method, endpoint, before/after values, payload, impact, and preview fingerprint.
6. Require explicit approval bound to that environment, target, method, payload, and fingerprint.
7. Send exactly one POST, PATCH, or DELETE through `core.fusion-api.apps-common` and `core.fusion-api.rest-api-client`.
8. Never automatically retry a mutation and never enable upsert.
9. Verify with a separate GET.
10. Report verified success, unverified success, refusal, or classified failure distinctly.

Read-only listing and retrieval require no approval.

## Task CSV export contract

Route export to `shared.setup-export.task-level-export` with exact `TaskCode: ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS`. The exporter creates one task CSV export, captures and monitors `ProcessId`, downloads immutable `FileContent` only after success, retrieves `ProcessLog` after failure, and saves the ZIP or diagnostic under the supplied project workspace.

## FSM ZIP validation and import contract

1. Run `shared.validation.setup-data-validator` and `shared.validation.reference-data-validator` for task-local setup and reference checks.
2. Route the import only to `core.data-loader`; this pillar skill supplies the exact task context and rules but never selects or invokes an import adapter or endpoint.
3. Detect an FSM ZIP only when a member has the exact case-sensitive basename `ASM_SETUP_CSV_METADATA.xml`.
4. Reject missing, duplicate, unreadable, encrypted, unsafe-path, or ambiguous metadata.
5. Parse metadata without rewriting the archive and require exactly one task identity equal to `ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS`.
6. Preserve the archive bytes and SHA-256 through validation, Task Hook preview, approval, and execution.
7. After Core Data Loader prepares the final immutable upload artifact, require its `data-load` Task Hook to evaluate this task's compiled `ora-resource` rules and issue the validation envelope bound to the exact archive SHA-256.
8. Require a later standalone explicit approval of that exact immutable preview. A changed source, archive, environment, task identity, rule result, or approval invalidates the envelope and restarts validation.
9. Let Core Data Loader own UCM upload, FSM initiation routing and payload construction, accepted-request reporting, and any later status or ProcessLog retrieval. Do not reconstruct its envelope or locally choose an endpoint, adapter, routing field, or retry behavior.
10. Submit only once under the current Core Data Loader contract. If Task Hook validation or approval is missing, stale, or mismatched, stop with `approval_blocker` before any POST.
11. Treat a later Run Book or Journey `updateProgress` failure as a separate synchronization result. Do not change an accepted FSM import to failed, and never retry or resubmit the import because progress synchronization failed.

## Natural prompts

- `Show the Customer Center Lookups in the configured environment.`
- `Show the values for <lookup meaning or exact lookup type>.`
- `Add lookup code <code> with meaning <meaning> to <lookup type>.`
- `Change the meaning of <code> in <lookup type>.`
- `Disable <code> in <lookup type>.`
- `Delete custom lookup code <code> from <lookup type>.`
- `Export Manage Customer Center Lookups setup data.`
- `Validate and import this Manage Customer Center Lookups export.`

Resolve an unambiguous request directly without asking the user to select an internal operation name.

## Error and diagnostic contract

| Failure class | Use |
|---|---|
| `input_validation` | Missing environment, invalid code/date/flag, changed artifact, or unsafe ZIP. |
| `catalog_or_metadata_mismatch` | Task membership, parent context, category, level, describe, exact TaskCode, CSV flag, or adapter cannot be proven. |
| `auth_expired_or_invalid` | Cached authentication rejected; refresh once only under repository cache policy. |
| `authorization_or_privilege` | Access remains denied or the task/resource privilege is missing. |
| `transport_or_environment` | Environment, VPN, DNS, or connection failure; retry only bounded reads. |
| `fusion_api_error` | Fusion rejects the one approved request; report status and ECID when available. |
| `process_timeout` | Polling expires; preserve TaskCode, ProcessId, last status, elapsed time, and next-check path. |
| `process_failed` | Export/import completes with errors; preserve ProcessLog/status and partial results. |
| `artifact_persistence` | A required artifact, diagnostic, run record, or token log cannot be saved. |
| `approval_blocker` | Preview is missing, stale, changed, or declined. |

Never persist credentials, tokens, authorization headers, customer data, signed URLs, or sensitive payloads.

## Synthetic behavior checks

| Scenario | Expected result |
|---|---|
| Exact task read | Return only the eight confirmed Standard types and their current levels. |
| Unknown or prefix-inferred type | Refuse task attribution and manual maintenance. |
| User custom-code update | Exact GET, describe/seed validation, one preview, approval, one mutation, separate GET verification. |
| Seeded Extensible state/delete request | Refuse before preview. |
| Wrong-task FSM ZIP | Refuse before import because metadata does not equal `ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS`. |
| Task-local import route selection | Refuse before POST; Core Data Loader owns endpoint, adapter, routing-field, and retry selection. |
| Missing or stale Task Hook validation envelope | Fail closed with `approval_blocker`; do not upload, initiate, or reconstruct an envelope. |
| Valid exact-task FSM archive | Preserve bytes and hash, pass exact task context to Core Data Loader, complete Task Hook validation and separate approval, then let Core Data Loader execute once. |

## Persistence

When `project_id` is supplied, persist artifacts under the manifest paths, append a run record under `project/{project_id}/state/runs`, and append token usage under the shared token log. Repository-only authoring does not create a project workspace. Fail closed when required authority, membership, metadata, privilege, adapter, approval, or safe destination evidence is absent.
