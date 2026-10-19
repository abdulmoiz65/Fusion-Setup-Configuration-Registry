---
skill_id: "erp.financials.general-ledger.assign-balancing-segment-values-to-legal-entities"
name: "Assign Balancing Segment Values to Legal Entities Setup Task Guidance"
description: "Provides task-specific setup guidance for Assign Balancing Segment Values to Legal Entities under the General Ledger functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "General Ledger"
functional_area_code: "ORA_FIN_GENERAL_LEDGER"
task_code: "GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEGAL_ENTITIES"
task_name: "Assign Balancing Segment Values to Legal Entities"
parent_skill_id: "erp.financials.general-ledger"
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
  - "submission_recovery_anchor"
  - "submission_recovery_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/general-ledger/assign-balancing-segment-values-to-legal-entities/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/general-ledger/assign-balancing-segment-values-to-legal-entities/current/"
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

# Assign Balancing Segment Values to Legal Entities Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Assign Balancing Segment Values to Legal Entities` under `General Ledger`.

## Setup Task Skill Contract

- task_code: `GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEGAL_ENTITIES`
- task_name: `Assign Balancing Segment Values to Legal Entities`
- parent_skill_id: `erp.financials.general-ledger`
- pillar: `ERP`
- offering: `Financials`
- functional_area: `General Ledger`
- functional_area_code: `ORA_FIN_GENERAL_LEDGER`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Assign Balancing Segment Values to Legal Entities` under `General Ledger`.

## Setup Task Metadata

- Task name: `Assign Balancing Segment Values to Legal Entities`
- Task code: `GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEGAL_ENTITIES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Create the criteria-bearing populated task export with `core.fusion-api.rest-api-client`, then use the result polling and download mechanics from `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Financials`
- Functional area / Setup Object: `General Ledger`
- Setup task name: `Assign Balancing Segment Values to Legal Entities`
- Setup task code: `GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEGAL_ENTITIES`

## Coexistence with Assign Balancing Segment Values to Ledger

This skill owns assignments where the target is an explicitly identified Legal
Entity within the resolved ledger context. The separate
`Assign Balancing Segment Values to Ledger`
(`GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEDGER`) skill owns direct ledger
assignments.

- If the request explicitly names a Legal Entity or says to assign a BSV or
  Company Value to a Legal Entity, use this skill.
- If the request identifies only a Ledger and no Legal Entity target, do not
  ask for a Legal Entity or treat its absence as an error; route to `Assign
  Balancing Segment Values to Ledger`.
- If the request names both a Ledger and a Legal Entity, use this skill: the
  ledger supplies scope and the Legal Entity is the assignment target.
- If the target wording could mean either a direct Ledger assignment or a
  Legal Entity assignment, ask the user to confirm the target before running
  lookups, exports, or imports.
- Do not apply this skill's missing-Legal-Entity validation to a request whose
  target is only a Ledger.




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

Use the parent functional-area skill `erp.financials.general-ledger` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

For every create or update execution, resolve the exact PRIMARY LedgerId and first submit a new populated task CSV export filtered to that ledger. The newly downloaded package may be reused only within the same execution while its scope, contents, and checksum remain unchanged through preview, approval, and import.

The high-level task export wrapper does not expose task-criteria arguments. Do not treat that wrapper limitation as a workflow blocker and do not submit an unscoped export. For the populated export only, invoke `core.fusion-api.rest-api-client` against `POST /fscmRestApi/resources/11.13.18.05/setupTaskCSVExports` with this exact payload shape, substituting only the resolved LedgerId:

```json
{
  "TaskCode": "GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEGAL_ENTITIES",
  "SetupTaskCSVExportCriteria": [
    {
      "TaskCode": "GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEGAL_ENTITIES",
      "BusinessObjectCode": "GL_PRIMARY_LEDGER",
      "AttributeSet": "Set1",
      "AttributeName": "PRIMARY_LEDGER_ID",
      "AttributeValue": "{LedgerId}"
    }
  ],
  "SetupTaskCSVExportProcess": [
    {
      "TaskCode": "GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEGAL_ENTITIES"
    }
  ]
}
```

Require one returned `SetupTaskCSVExportProcess` item with a positive `ProcessId`. Pass that TaskCode and ProcessId to the existing `shared.setup-export.task-level-export` result poll/download helper. Preserve its normal status, FileContent, and ProcessLog handling. This pillar-local routing changes no shared or core implementation and must also be used for the identical-scope post-import verification export.

Use a current template export only as a controlled fallback when the same-run populated export cannot return a usable carrier after the shared bounded read-only handling. Require ProcessLog or safe HTTP/client evidence that classifies the failure as a size limit, HTTP 413, completed-with-warning/incomplete carrier, transient 429 or 5xx, timeout, or result-download/transport failure. Do not use the fallback for invalid task or scope criteria, HTTP 400, final 401 or 403, missing privilege, unresolved ledger or legal entity, business conflict, corrupt downloaded content, or user cancellation.

Invoke shared.setup-export.task-level-export in template-only mode for the same environment, release, and task. Treat that template as physical-contract evidence only: members, headers, field order, and ASM manifest. Before authoring, separately prove the exact current legal-entity parent, balancing value set and values, legal-entity assignment state, and direct-ledger assignment state with supported current read-only Fusion evidence. A previous populated export may support reviewed static same-release field-role constants, but it must never prove current ownership. If the current parent or ownership state cannot be proven, stop before preview or import.

Bind the populated-export failure receipt, template process receipt and checksum, current business-state receipts, final package checksum, and approval to the same execution. Disclose the fallback and its reason in the preview. For post-import verification, first attempt a new identical-scope populated export; if the same eligible carrier failure recurs, use supported current read-only business-state verification, otherwise report verification as incomplete and do not claim success.

## CSV Serialization and Archive Integrity

When authoring the requested delta, use a CSV writer or equivalent serializer;
do not construct CSV records by string concatenation or shell-escaped text.
In particular, a textual escape sequence such as `` `r`n `` or `\\r\\n` must
never stand in for an actual CSV record boundary.

Before approval, independently inspect every changed CSV member from the final
ZIP. Confirm that it parses as CSV, retains the exact export-derived header and
column order, has one physical header record followed by the intended physical
data records, and that every record has the expected field count. Reject a
package that contains literal line-ending escape text where a row boundary is
required, merges a header and data row, changes an untouched member's order,
or otherwise differs from the selected carrier outside the approved delta.

Record this parser-based check, the changed-member row counts, and the final
archive checksum in the approval preview. A serialization failure is a package
defect: rebuild from the current carrier, revalidate, and obtain fresh approval;
never submit it as a live discovery attempt.

## Data Loader Submission and Timeout Recovery

Before the first approved Data Loader write, create a recovery anchor for the exact final ZIP. Use an attempt-unique ZIP basename no longer than 200 characters, bind that basename and SHA-256 checksum to the preview and approval, and pass the same basename as both `fileName` and `dataSetName`. Capture the authenticated submitter, UTC submission-window start, TaskCode, SourceType `FSM`, and the current `SetupTaskCSVImportProcess` ProcessIds for this exact task as a pre-submit baseline.

Invoke the existing `core.data-loader` adapter exactly once with an outer command timeout of at least 300 seconds. Its HTTP operation can wait longer than 60 seconds. When the execution host yields, continue waiting on that same invocation in intervals no longer than 60 seconds; do not terminate it or launch another upload merely because the first observation window elapsed.

If the invocation ends without returning `ContentId` or `RequestId`, the server-side outcome is unknown. Do not retry. First query `/hcmRestApi/resources/latest/dataLoaderDataSets` for the exact approval-bound `DataSetName`, submitter, `SourceType=FSM`, task code, and bounded submission window. When exactly one row matches, recover `UcmContentId`, `DataSetRequestId`, `DataSetId`, `FsmMigRequestId`, and `FsmTaskCode`, then resume the normal Data Loader status and result workflow.

If exact dataset recovery is unavailable or unauthorized, query `/fscmRestApi/resources/latest/setupTaskCSVImports/{TaskCode}/child/SetupTaskCSVImportProcess`, compare it with the pre-submit baseline, and accept only one new positive ProcessId for the exact task and submission window. Read its `SetupTaskCSVImportProcessResult` status, log, and result reports and resume normal monitoring. Zero candidates remains unknown; more than one is ambiguous. Neither case authorizes another upload or import.

For a legacy timeout that has no unique DataSetName or pre-submit baseline, use all exact read-only evidence that is available but do not guess an identity. If one exact process cannot be proved, retain the unknown outcome. A later attempt requires a newly named package, regenerated preview, and fresh approval.
