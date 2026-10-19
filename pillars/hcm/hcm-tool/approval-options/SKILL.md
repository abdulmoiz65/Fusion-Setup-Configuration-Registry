---
skill_id: "hcm.hcm-tool.approval-options"
name: "Approval Options Implementation Guidance"
description: "Provides HCM HCM Tool implementation guidance for the Approval Options functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Approval Options"
functional_area_code: "CUSTOM_APPROVAL_OPTIONS"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm tool pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "approval_options_scope"
  - "approval_options_requirements"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.fusion-api.rest-api-client"
  - "core.diagnostics.role-access-check"
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
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/approval-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/approval-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/approval-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CUSTOM_BYPASS_APPROVALS"
  - "CUSTOM_ALERT_INITIATOR"
  - "CUSTOM_ARCHIVE_TRANSACTIONS"
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

# Approval Options Implementation Guidance

## Purpose

Provides HCM HCM Tool implementation guidance for the Approval Options functional area.

## When to Use

Use this functional-area skill after HCM Tool scope is confirmed and the project needs approval options setup planning, baseline export, import sequencing, or validation checkpoints.

## Approval Process Scope Gate

Configure approval options only for an explicitly specified approval process validated with `GET /hcmRestApi/resources/11.13.18.05/businessProcessApprovalOptions?finder=findByProcessName;Name={url_encoded_approval_process}&fields=Name,ArchivePeriod,PurgePeriod,ProcessId,ApprovalDisabledFlag,AsyncBypassEnabledFlag,AlertEnabledFlag,SendToUsersFlag,BypassSupportedFlag,AsyncBypassSupportedFlag,ApprovalOverrideSupportedFlag,ApprovalDisabledValue,IsParallelTransactionSupported,RuleFileName,IsTaskConfigSupported,IsParallelTransactionEnabled,isOverallParallelTransactionEnabled`.

Supply the process name unchanged to `findByProcessName` through the `Name` parameter and accept only one returned, nonblank Process Name that equals the supplied value; do not use partial, case-normalized, or similar-name matching. Do not infer, substitute, or create an approval process.  After the exact-match safety gate, return  the requested that are present in the resolved record. Report a requested setting as unavailable when the record does not supply it; do not probe guessed field names. Return `APPROVAL_PROCESS_NOT_FOUND` when the finder returns no result. When it returns more than one result, return `APPROVAL_PROCESS_AMBIGUOUS` and ask the requester to provide the exact Process Name to use; do not select a candidate.

Do not add, remove, or rename fields for the exact-process read check. Use only the setting field that the selected nested task owns.

## Post-Data-Loader Verification and Recovery

After Data Loader reports an accepted Approval Options mutation, use the exact-process finder to read back the setting owned by the selected nested task before reporting success. If the live value matches the approved requested value, report the change as verified.

If the read check does not match, treat the Data Loader operation as ineffective. With explicit approval that covers the fallback action, invoke the selected task's documented businessProcessApprovalOptions action exactly once outside the Data Loader context, using the identical approved payload and the required action headers. Then repeat the exact-process read check. Do not modify the payload, substitute an action or business object, or retry the direct action after an unsuccessful readback.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `HCM Tool` (`CUSTOM_HCM_TOOL`)
- Functional area / Setup Object: `Approval Options` (`CUSTOM_APPROVAL_OPTIONS`)

## Setup Tasks

1. [Bypass Approvals](bypass-approvals/SKILL.md) (`CUSTOM_BYPASS_APPROVALS`)
2. [Alert Initiator](alert-initiator/SKILL.md) (`CUSTOM_ALERT_INITIATOR`)
3. [Archive Transactions](archive-transactions/SKILL.md) (`CUSTOM_ARCHIVE_TRANSACTIONS`)

## Sample Prompt Usage

1. `Use approval-options skill to list bypass-approvals setting for process with exact name Promote and Change Position`
2. `Use approval-options skill to disable bypass-approvals setting for process with name Add Pending Worker if it is currently enabled`
3. `Use approval-options skill to set archive period setting to ORA_HRC_TXN_6_MONTHS for process with name Administer Salary`
4. `Use approval-options skill to enable alert Initiator On Error setting for process with name Cancel Work Relationship`

## Inputs

- `implementation_objective`
- `project_context`
- `approval_options_scope`
- `approval_options_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
