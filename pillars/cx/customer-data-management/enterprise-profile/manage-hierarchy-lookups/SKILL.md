---
skill_id: "cx.customer-data-management.enterprise-profile.manage-hierarchy-lookups"
name: "Manage Hierarchy Lookups Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Hierarchy Lookups under the Enterprise Profile functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Enterprise Profile"
functional_area_code: "ORA_ASK_ENTERPRISE_PROFILE"
task_code: "HZ_MANAGE_HIERARCHY_LOOKUPS"
task_name: "Manage Hierarchy Lookups"
parent_skill_id: "cx.customer-data-management.enterprise-profile"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/manage-hierarchy-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/manage-hierarchy-lookups/current/"
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

# Manage Hierarchy Lookups

## Purpose and routing

Manage the lookup values used by Customer Data Management hierarchy setup. Resolve an unambiguous natural request directly. Reuse `core.fusion-api.apps-common` for lookup operations, `shared.setup-export.task-level-export` for export, the shared validators for validation, and `core.data-loader` for every import. Do not implement task-local OAuth, HTTP transport, CSV processing, polling, or generic lookup CRUD.

## Setup Task Skill Contract

- task_code: `HZ_MANAGE_HIERARCHY_LOOKUPS`
- task_name: `Manage Hierarchy Lookups`
- parent_skill_id: `cx.customer-data-management.enterprise-profile`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Enterprise Profile`
- functional_area_code: `ORA_ASK_ENTERPRISE_PROFILE`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Ownership and review

- Owner: CX Customer Data Management pillar team.
- Required functional reviewer: CX Customer Data Management Pillar Lead or hierarchy SME.
- Required framework reviewer: FSCR A-Team/core reviewer.
- Required functional-behavior reviewer: FSCR QA when read, mutation, validation, export, or import behavior changes.

Reviewer metadata is kept in the body because the current manifest schema permits `owner_team` but has no reviewer field.

## Task-specific lookup baseline

| Lookup type | Meaning | Configuration level | Evidence and restrictions |
|---|---|---|---|
| `PARTY_HIERARCHY_TYPE` | Party Hierarchy Type | Extensible in the tested baseline; verify with the target GET | Oracle documents this type as the list updated after creating a hierarchy type. Protect seeded codes and require evidence from Manage Tree Structures before adding a custom code. |
| `HZ_TREE_STATUS` | Hierarchy Status | System in the tested baseline; verify with the target GET | Oracle documents this lookup as the Active/Inactive hierarchy-status LOV. Its association with this task comes from the developer-provided tested task scope, not from its `HZ_` prefix. |

Use the tested task-scope baseline for direct retrieval and require a current GET before claiming that either lookup or configuration level remains available in the target environment. Report a missing type as a baseline discrepancy and never infer additional task members from prefixes or modules. Adding a lookup value does not create a hierarchy definition, version, node, or hierarchy data. Read [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md) for the official Oracle sources and evidence boundaries.

## Supported operations

| Natural request | Support |
|---|---|
| Show hierarchy lookup types or values | Read-only through the exact category resolved by `core.fusion-api.apps-common`; no approval required. |
| Retrieve one exact type or code | Read-only; require an exact match. |
| Add a hierarchy type code | Conditional for a permitted custom `PARTY_HIERARCHY_TYPE` code after dependency, configuration-level, seed, and describe checks. |
| Change meaning, dates, or enabled state | Conditional only for fields and custom codes permitted by current metadata. |
| Delete a custom hierarchy type code | Conditional after destructive preview and approval. |
| Export setup data | Supported; route to `shared.setup-export.task-level-export`. |
| Validate setup data | Route to both shared validators and apply task-local rules. |
| Import validated setup data | Supported through `core.data-loader` only after Task Hook validation of the exact immutable archive and separate explicit approval. |

Never silently upsert. Reject custom codes beginning with `ORA_`. Never alter lookup identity, module, category, or seeded-code identity.

## Manual field and operation restrictions

| Target | Create | Update | Enable or disable | Delete |
|---|---|---|---|---|
| `PARTY_HIERARCHY_TYPE` Extensible custom code | Permit only after exact hierarchy-type evidence, duplicate check, GET, and current describe validation | Permit `Meaning`, `Description`, `StartDateActive`, `EndDateActive`, `EnabledFlag`, or `DisplaySequence` only when both Oracle configuration rules and current describe metadata allow the named field | Permit only for a non-seeded custom code and a current writable `EnabledFlag` | Permit only for a non-seeded custom code after destructive preview and approval |
| `PARTY_HIERARCHY_TYPE` seeded code | No | Permit only a wording change that current Oracle rules and describe metadata explicitly allow; otherwise refuse | No | No |
| `HZ_TREE_STATUS` System code | No | At most a `Meaning` wording change, and only when current describe metadata confirms the field is writable | No | No |

The REST schema lists more writable-looking attributes than a particular lookup's configuration level permits. Apply the stricter intersection of task scope, configuration-level rules, seeded-data protection, current describe metadata, and the user's named change. Do not update `Tag` or `Module` for Extensible or System lookups. Treat `LookupType` and `LookupCode` as immutable identity.

Treat a code as predefined seed data when current evidence reports `LastUpdatedBy` as `SEED_DATA_FROM_APPLICATION`; do not substitute naming conventions or `CreatedBy` guesses for that check.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task.

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Route every import exclusively through `core.data-loader`.
5. For an FSM ZIP, preserve the archive unchanged, require the exact case-sensitive member basename `ASM_SETUP_CSV_METADATA.xml`, and require exactly one metadata task identity equal to `HZ_MANAGE_HIERARCHY_LOOKUPS`.
6. Let Core Data Loader prepare the final immutable upload artifact, then invoke its `data-load` Task Hook immediately before approval and upload. Require the Task Hook validation envelope to remain bound to that archive's SHA-256.
7. Require the user's separate explicit approval of the exact immutable preview. Any source, archive, environment, task identity, validation result, or approval change restarts the Core Data Loader and Task Hook lifecycle.
8. Core Data Loader owns UCM upload, initiation payload construction, endpoint and FSM routing selection, accepted-request reporting, and later status diagnostics. This pillar skill must not select an adapter, endpoint, loader routing field, or retry policy.

Use this task metadata:

- Offering: `Customer Data Management`
- Functional area / Setup Object: `Enterprise Profile`
- Setup task name: `Manage Hierarchy Lookups`
- Setup task code: `HZ_MANAGE_HIERARCHY_LOOKUPS`

## Manual lookup workflow

1. Resolve exactly one configured Fusion environment.
2. GET the exact lookup type and exact code when applicable.
3. Resolve the resource category and retrieve current describe metadata.
4. Validate configuration level, seeded-code protection, hierarchy-type dependency, dates, reserved prefixes, and supported fields.
5. Show one exact redacted method, endpoint, and payload preview.
6. Require explicit approval for the named mutation.
7. Send exactly one POST, PATCH, or DELETE through the shared REST transport. Never automatically retry a mutation.
8. Verify with a separate GET and distinguish verified success, unverified success, refusal, and classified failure.

For create, explicitly send `Upsert-Mode: false` or omit the header so its documented default remains false. Never set it to true.

## Privilege preflight

Before a live operation, verify all applicable access instead of relying on a role name alone:

1. Require `ORA_ASM_FUNCTIONAL_SETUPS_USER_ABSTRACT` and access to the exact setup task for UI-backed setup work.
2. Require the target role's task-specific Manage Hierarchy Lookups privilege. Current public Oracle documentation does not publish its code; use `core.diagnostics.role-access-check` or target-environment security evidence and fail closed when it cannot be confirmed.
3. Require `ORA_ASM_EXPORT_IMPORT_FUNCTIONAL_SETUPS_USER` for task CSV export or import.
4. Require authorization for the Standard Lookups REST resource and the exact lookup type. Treat a secured or unauthorized lookup as an authorization failure, not as an absent lookup.

## Natural prompts

- `Show the Hierarchy Lookups in the configured environment.`
- `Show the values for Party Hierarchy Type.`
- `Show the hierarchy status values.`
- `Add hierarchy type lookup code MY_CUSTOM_HIERARCHY with meaning My Custom Hierarchy.`
- `Change the meaning of MY_CUSTOM_HIERARCHY to My Customer Hierarchy.`
- `Disable MY_CUSTOM_HIERARCHY in Party Hierarchy Type.`
- `Delete custom lookup code MY_CUSTOM_HIERARCHY from Party Hierarchy Type.`
- `Export Manage Hierarchy Lookups setup data.`
- `Validate and import this Manage Hierarchy Lookups export.`

## Error handling contract

### Failure modes

| Failure class | Example | Recoverable behavior |
|---|---|---|
| `input_validation` | Missing environment, invalid code, invalid date order, or changed artifact | Correct locally and restart from preflight; no side effect occurred. |
| `catalog_or_metadata_mismatch` | Task flags, task scope, configuration level, or describe metadata differs | Stop and reconcile authoritative metadata; do not broaden scope. |
| `approval_blocker` | Core Data Loader Task Hook did not issue a current validation envelope bound to the exact immutable archive SHA-256 | Stop before upload or initiation; rebuild and approve the immutable Data Loader preview. |
| `auth_expired_or_invalid` | Cached-token 401 or 403 | Refresh a repository-managed cached token once; never replace an explicitly supplied token. |
| `authorization_or_privilege` | 403 persists or task-specific privilege is absent | Stop and report the missing access; do not retry the operation. |
| `transport_or_environment` | DNS, VPN, connection, or environment-resolution failure | Retry only a read with bounded shared-client policy; never retry a mutation automatically. |
| `fusion_api_error` | Fusion rejects an approved request | Report redacted status, endpoint path, response summary, and ECID when available; stop. |
| `process_timeout` | Export or import exceeds the owning executor's wait window | Stop polling and report TaskCode, ProcessId, last status, elapsed time, and the safe next-check path. |
| `process_failed` | Export or import completes with errors | Retrieve and preserve ProcessLog or status evidence when available; return failure or partial failure. |
| `artifact_persistence` | ZIP, validation result, run record, or token log cannot be saved | Preserve safe diagnostics in a temporary location and report the intended project path. |
| `approval_blocker` | Preview is missing, stale, declined, or changed | Do not submit; regenerate the exact preview when inputs change. |

### Preflight, retry, timeout, and recovery

- Preflight the exact environment, task code, catalog CSV flags, task membership, lookup type and code when applicable, configuration level, seeded evidence, supported fields, date order, privileges, immutable artifact hash, ZIP member safety, exact `ASM_SETUP_CSV_METADATA.xml` member, metadata task identity, current Task Hook validation envelope, destination path, and approval requirement.
- Permit at most one cached-token refresh for a read. Use bounded retries only for read-only transient transport failures. Never automatically retry POST, PATCH, DELETE, CSV import, loader, or ESS submission.
- Core Data Loader owns endpoint selection and any documented recoverable initiation behavior; this task skill must not override or duplicate that policy.
- Delegate polling windows to the owning export or Data Loader service. On timeout, preserve the external identifier and safe resume stage rather than submitting a replacement process.
- A manual lookup mutation has no automatic rollback. Reconcile uncertain completion with a separate GET. Request a new preview and approval for any compensating mutation.
- For failed CSV work, preserve the immutable source ZIP, validation result, ProcessId, ProcessLog/status payload, successful business-object results, and an `errors` array when safe and when `project_id` is supplied.

### Diagnostics, redaction, and approvals

Return `status`, `stage`, `failure_class`, `message`, `recommended_action`, environment identity, skill and task identity, redacted endpoint path, artifact references, ProcessId or ECID when available, completed checks, and verified side effects. Never print or persist credentials, tokens, authorization headers, token caches, full sensitive payloads, opaque signed URLs, or customer data. Require explicit approval bound to the displayed environment, operation, exact lookup identity or immutable ZIP, before/after values, expected impact, and preview fingerprint. Deletion, overwrite, force, mutation retry, import, and replacement submission always require fresh approval.

## Synthetic golden scenarios

| Scenario | Synthetic request | Expected result |
|---|---|---|
| Read baseline | Show the Hierarchy Lookups in the configured environment | Resolve one environment, GET the documented/tested types, report configuration levels and any task-scope discrepancy; no approval. |
| Protect System status | Disable `ACTIVE` in `HZ_TREE_STATUS` | Refuse before preview because System codes can't have enabled state changed. |
| Missing hierarchy dependency | Add `MY_CUSTOM_HIERARCHY` without Manage Tree Structures evidence | Return an approval blocker before preview; do not invent or call an undocumented hierarchy-type endpoint. |
| Update custom meaning | Change `MY_CUSTOM_HIERARCHY` meaning to `My Customer Hierarchy` | GET exact code, prove it is non-seeded, validate writable `Meaning`, preview one PATCH, require approval, submit once, and verify separately. |
| CSV validation failure | Import a ZIP whose task identity isn't `HZ_MANAGE_HIERARCHY_LOOKUPS` | Refuse before `core.data-loader` and report the task-identity mismatch. |
| Task-local import route selection | Import an exact-task FSM ZIP through a route selected by this pillar skill | Refuse before POST; Core Data Loader owns endpoint, adapter, routing-field, and retry selection. |
| Missing Task Hook validation envelope | Import an exact-task FSM ZIP without an envelope bound to its current SHA-256 | Stop with `approval_blocker`; do not upload, initiate, or reconstruct an envelope. |
| Valid CSV route | Validate and import an immutable export for the exact task | Validate the exact archive and task identity, complete Core Data Loader Task Hook validation and separate approval, then let Core Data Loader execute once. |

## Persistence

Fail closed on ambiguity or missing task, category, dependency, describe, configuration-level, source-guidance, privilege, or import-readiness evidence. When `project_id` is supplied, register durable artifacts, record the skill run, update applicable project state, and append token usage using the manifest policy. Repository-only authoring does not create a project workspace.
