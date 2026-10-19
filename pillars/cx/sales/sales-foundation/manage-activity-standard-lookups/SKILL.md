---
skill_id: "cx.sales.sales-foundation.manage-activity-standard-lookups"
name: "Manage Activity Standard Lookups Setup Task Guidance"
description: "Reviews and manages Sales Activity standard lookup codes through exact Apps Common reads and guarded lookup-code CRUD, including governed ZMM_ACTIVITY_TYPE creation with function-derived tags. Explicit setup-data export, import, and supported translation workflows remain available without becoming the default code-mutation route."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Sales Foundation"
functional_area_code: "ORA_ZBS_SALES_FOUNDATION"
task_code: "ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS"
task_name: "Manage Activity Standard Lookups"
parent_skill_id: "cx.sales.sales-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "CX sales pillar team"
version: "0.4.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "operation"
  - "lookup_type"
  - "lookup_code"
  - "lookup_code_values"
  - "activity_function_codes"
  - "fusion_environment_context"
  - "execution_intent"
  - "approval"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "current_lookup_state"
  - "normalized_change_preview"
  - "impact_assessment"
  - "execution_authorization"
  - "execution_result"
  - "verification_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.apps-common"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.apps-common"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-foundation/manage-activity-standard-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-foundation/manage-activity-standard-lookups/current/"
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
  - "Reads Standard Lookup types and lookup codes from the configured Fusion environment."
  - "After an exact immutable preview and explicit approval, may create, update, deactivate, or delete one Activity standard lookup code through core.fusion-api.apps-common."
  - "May export or import approved setup data for ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS through the shared setup-data workflow."
  - "May refresh the local gitignored OAuth token cache through the invoked core skill."
required_privileges:
  - "Fusion task and REST privileges appropriate to view or manage Manage Activity Standard Lookups."
  - "ORA_ASM_FUNCTIONAL_SETUPS_USER_ABSTRACT and task-specific setup privileges for setup-data export or import."
---

# Manage Activity Standard Lookups Setup Task Guidance

## Purpose

Plan, review, validate, create, update, deactivate, delete, translate, export,
import, and verify lookup-code values owned by `Manage Activity Standard
Lookups` under `Sales Foundation`. Keep the parent lookup type explicit and
existing. Use task-specific rules for configuration-level editability, tags,
display-sequence impact, predefined data, immutable approval, and verification.

Lookup-code Create, Update, Deactivate, and safe Delete use
`core.fusion-api.apps-common` after an immutable preview and explicit approval.
The catalog's FSM and CSV flags describe setup-data capabilities; they do not
make an export, FSM ZIP, or Data Loader handoff a prerequisite for code CRUD.
Use the package workflow only when the requester explicitly asks to Export,
Import, or perform a supported translation workflow.

## Runtime Interface

Apply the parent `cx.sales.sales-foundation` runtime guidance. Review and
lookup-code CRUD load the Apps Common standard-lookups contract. Apps Common
owns OAuth and HTTP transport; this task owns Activity scope, configuration
level and predefined-data checks, exact identity, function-derived tags,
sequence impact, preview, approval, and verification gates.

Do not inspect or reproduce shared-client implementation during normal runtime.
If a documented interface fails, inspect only its owning contract and command
help. Do not substitute browser automation, Data Loader, setup import, direct
curl, or task-local scripts for lookup-code CRUD.

## Setup Task Skill Contract

- task_code: `ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS`
- task_name: `Manage Activity Standard Lookups`
- parent_skill_id: `cx.sales.sales-foundation`
- pillar: `CX`
- offering: `Sales`
- functional_area: `Sales Foundation`
- functional_area_code: `ORA_ZBS_SALES_FOUNDATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill for an individual Activity standard lookup value or a reviewed
task setup-data package. Examples include creating a task-owned objective,
outcome, or Activity Type value; changing a meaning or effective state;
changing a default-driving display sequence; reviewing current values;
translating a value; or migrating the task configuration. A new
`ZMM_ACTIVITY_TYPE` code is complete only when its exact supplied Activity
functions are encoded in the canonical colon-delimited `Tag` value and the
function-specific Activity Type LOV verifies the result.

Do not use this skill to create a new lookup type or to guess which parent type
an individual value belongs to. A request such as `Create TEST_LOOKUP` requires
the exact existing `LookupType` and a user-facing `Meaning` before a mutation
preview can be prepared.

## Setup Task Metadata

- Task name: `Manage Activity Standard Lookups`
- Task code: `ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Supported Scenarios

| Scenario | Route | Important Boundary |
|---|---|---|
| Review or validate one lookup value | Read-only Standard Lookups REST through `core.fusion-api.apps-common` | Resolve the exact parent and code; no mutation |
| Create one lookup value | Approved Standard Lookups child `POST` through `core.fusion-api.apps-common` | Existing User or Extensible parent, exact code absent, no upsert, immutable preview, explicit approval, exact GET verification |
| Update meaning, description, dates, enablement, sequence, or permitted tag | Approved item `PATCH` through `core.fusion-api.apps-common` | Change only fields allowed by configuration level and predefined-data state; never rename LookupCode |
| Deactivate one lookup value | Approved item `PATCH` through `core.fusion-api.apps-common` | Requester must choose disablement, end-dating, or both; no inferred method |
| Delete one lookup value | Approved item `DELETE` through `core.fusion-api.apps-common` | Only when Oracle editability permits it and downstream and historical impact is explicitly accepted |
| Translate one lookup value | Guided task UI or current task CSV package | The FSCR Standard Lookups reference documents translation reads but no translation mutation executor contract |
| Change a calendar color | Guided UI pending current-environment representation review | The same Tag field carries Activity-function membership in current task exports; do not overwrite a function tag with a color value unless a reviewed combined representation is proven |
| Create an Activity Type | Approved Standard Lookups child `POST` through `core.fusion-api.apps-common`; use task CSV only for an explicit Import request | Require exact supplied functions from APPOINTMENT, TASK, and CALLREPORT; derive a canonical colon-wrapped Tag; require start date and enablement; verify through the function-specific Activity Type LOV |
| Change default task status | Guided UI or approved PATCH of `DisplaySequence` for `ZMM_ACTIVITY_STATUS_CD` | Lowest sequence becomes the default; read all siblings and approve the impact |
| Change default Activity search | Guided UI or approved PATCH of `DisplaySequence` for `ORA_ZMM_ACTIVITY_FILTER_TYPE` | Review the resulting order; do not add, delete, or end-date values in this fixed list |
| Export or import task setup data | Shared task export, validation, and `core.data-loader` FSM route | Use a current package for task code `ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS`; never invent CSV files or headers |

## Publicly Documented Activity Lookup Types

| Lookup Type | Documented Behavior |
|---|---|
| `ORA_ZMM_ACTIVITY_OBJECTIVE` | Activity Objective values; tags are not supported |
| `ZMM_ACTIVITY_OUTCOME` | Activity Outcome values; tags are not supported |
| `ZMM_ACTIVITY_STATUS_CD` | Display order for task statuses; the lowest display sequence is the default status |
| `ZMM_ACTIVITY_TYPE` | Activity Type values; current task exports and the function-specific LOV carry Activity-function membership in Tag, while Oracle also documents Tag for calendar color, so color changes require representation review |
| `ORA_ZMM_ACTIVITY_FILTER_TYPE` | Order of Activity-search filters and the default search; supplied values cannot be added, deleted, or end-dated |

This list is documented scope, not a claim that Oracle publishes every lookup
type exposed by the task. For another type, require current task-page or
task-export evidence before treating it as owned by this skill.

## Preflight Checks

Before any Fusion-changing action, verify the exact target environment and
authorized identity, required task and REST privileges, existing parent lookup
type and task ownership, exact current code state, configuration level and
predefined-data restrictions, Activity-specific function and sequence impact,
selected Apps Common or explicit package route, minimal payload or validated
ZIP shape, immutable preview, and matching approval. Stop before side effects
when any preflight value is missing, ambiguous, stale, or unsupported.

## Individual Lookup-Code Workflow

1. Collect `Operation`, exact existing `LookupType`, exact `LookupCode`, and the
   fields required for that operation. Create also requires `Meaning`.
2. Read the task resources in the order below and execute the compiled task-node
   plan. Resolve the exact parent and code using the Standard Lookups resource.
3. For a create, require the code to be absent and set `Upsert-Mode=false`. For
   maintenance, require exactly one current code and its canonical item link.
4. Apply the User, Extensible, or System configuration matrix, predefined-data
   restrictions, Activity-specific tag rules, and sequence-impact checks.
5. For `ZMM_ACTIVITY_TYPE` Create, require `ActivityFunctionCodes`,
   `EnabledFlag`, and `StartDateActive`. Derive `Tag` by ordering the selected
   functions as `APPOINTMENT`, `TASK`, `CALLREPORT`, joining them with colons,
   and adding leading and trailing colons. For example, Appointment only is
   `:APPOINTMENT:`. Reject a conflicting user-supplied Tag.
6. For a live mutation, display an immutable preview containing the target
   environment, task, current state, method, canonical endpoint, exact JSON body
   or no-body delete, impact, verification GET, and approval fingerprint.
7. After explicit approval of that exact preview, invoke
   `core.fusion-api.apps-common`. Submit the mutation once; never automatically
   retry POST, PATCH, or DELETE.
8. Verify the exact code with GET. For an Activity Type, also verify every
   selected function through the Activity Type LOV. If the transport outcome is uncertain,
   reconcile once with GET before any retry decision. Record the safe HTTP
   outcome and request ID or ECID when available.

## Oracle Resource Read Order

1. [ora_input_validation.md](ora-resource/ora_input_validation.md)
2. [ora_dependency_readiness.md](ora-resource/ora_dependency_readiness.md)
3. [ora_reference_lookups.md](ora-resource/ora_reference_lookups.md)
4. [ora_defaulting_rules.md](ora-resource/ora_defaulting_rules.md)
5. [ora_design_enforcement.md](ora-resource/ora_design_enforcement.md)
6. [ora_error_handling.md](ora-resource/ora_error_handling.md)
7. [ora_rule_registry.json](ora-resource/ora_rule_registry.json) for the compiled
   task-node graph

For direct standard lookup reads or approved writes, also read
`core/fusion-api/apps-common/SKILL.md` and
`core/fusion-api/apps-common/references/lookups/standard-lookups.md`. The core
skill owns OAuth-backed transport; this task skill owns Activity business rules
and authorization gates.

## Public Documentation

- [Overview of Sales Lookup Types](https://docs.oracle.com/en/cloud/saas/sales/oasal/overview-of-lookup-types.html)
- [Overview of Lookups](https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html)
- [Standard Lookups REST Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html)
- [About Activity Type and Subtype](https://docs.oracle.com/en/cloud/saas/sales/oasal/about-activity-type-and-subtype.html)
- [Associate Activity Type with a Function and Subtype](https://docs.oracle.com/en/cloud/saas/sales/oasal/associate-activity-type-with-a-function-and-subtype.html)
- [Activity Type Lookups REST Endpoints](https://docs.oracle.com/en/cloud/saas/sales/faaps/api-list-values-activity-type-lookups.html)
- [Considerations When Setting Up Call Reports](https://docs.oracle.com/en/cloud/saas/sales/oasal/considerations-when-setting-up-call-reports.html)
- [Enable Default Task Status](https://docs.oracle.com/en/cloud/saas/sales/oasal/enable-default-task-status.html)
- [Change Calendar Colors](https://docs.oracle.com/en/cloud/saas/sales/oasal/change-calendar-colors.html)
- [Configure the Default Activity Search](https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-do-i-configure-default-activity-search-in-accounts.html)

## Offline Contract Tests

Run from the repository root:

```bash
python3 -m unittest discover \
  -s pillars/cx/sales/sales-foundation/manage-activity-standard-lookups/tests \
  -p 'test_*.py' \
  -v
```

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Sales`
- Functional area / Setup Object: `Sales Foundation`
- Setup task name: `Manage Activity Standard Lookups`
- Setup task code: `ORA_ZMM_MANAGE_ACTIVITY_LOOKUPS`

## Execution Route Selection

For lookup-code Create, Update, Deactivate, or safe Delete, use
`core.fusion-api.apps-common`; do not require an export package and do not
initialize browser control. Guided UI is used only when explicitly requested.
Use the CSV/FSM workflow and `core.data-loader` only for an explicit Export,
Import, or supported translation request. If the selected package workflow
cannot represent that explicit request, stop with the package limitation
instead of changing routes.

## Failure and Recovery

Classify failures as input validation, catalog or task-scope mismatch,
authentication or authorization, transport or environment, Fusion API,
process timeout or failure, stale state, approval blocker, verification
mismatch, partial completion, or artifact persistence. Preserve safe request
IDs, ECIDs, ProcessIds, last status, and one recommended action. Retrieve a
documented process result or log once when an import fails or is uncertain.

Retry only the shared client's documented cached-token refresh. Never retry or
replay POST, PATCH, DELETE, or import automatically. Reconcile an uncertain
lookup-code write once with the exact GET; require a new preview and approval
before any later mutation. Do not issue automatic compensation.

Redact and never print or persist credentials, bearer tokens, authorization
headers, client secrets, token-cache content, private keys, full base64
payloads, or sensitive customer details. Persist only sanitized task or
relative-endpoint identity, status, request ID or ECID, classified message, and
safe next action.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `operation`
- `lookup_type`
- `lookup_code`
- `activity_function_codes`
- `meaning`
- `description`
- `enabled_flag`
- `start_date_active`
- `end_date_active`
- `display_sequence`
- `tag`
- `language`
- `translated_meaning`
- `translated_description`
- `target_environment`
- `execution_intent`
- `approval`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `current_lookup_state`
- `normalized_change_preview`
- `impact_assessment`
- `execution_authorization`
- `execution_result`
- `verification_result`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.sales.sales-foundation` for
functional-area sequencing and scope decisions. Use only the reusable FSCR core
executors named above; do not add task-local OAuth, REST, or payload scripts.
The Oracle resource rules do not themselves authorize a Fusion write. Track
token usage for any generated project artifact or skill-run record using the
manifest policy.
