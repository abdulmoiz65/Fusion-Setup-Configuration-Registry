---
skill_id: "erp.project-financial-management.project-organizations"
name: "Project Organizations Implementation Guidance"
description: "Provides ERP Project Financial Management implementation guidance for the Project Organizations functional area."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Organizations"
functional_area_code: "ORA_PJF_PROJ_ORG"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP project financial management pillar team"
version: "0.1.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "project_organizations_scope"
  - "project_organizations_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "PJF_MANAGE_PROJECT_UNIT_ORGANIZATIONS"
  - "PJF_MANAGE_PROJECT_UNITS"
  - "PJF_MANAGE_PROJECT_ORGANIZATION_CLASSIFICATIONS"
  - "PJF_MANAGE_ORGANIZATION_HIERARCHIES_AND_CLASSIFICATIONS"
  - "PJF_CONFIGURE_PROJECT_ACCOUNTING_BUSINESS_FUNCTION"
  - "PJF_SUBMIT_PROCESS_TO_DENORMALIZE_ORGANIZATION_HIERARCHY"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Writes declared functional-area project artifacts, artifact registrations, state updates, skill-run records and token-usage records through the declared core project services."
required_privileges: []
---

# Project Organizations Implementation Guidance

## Purpose

Provides ERP Project Financial Management implementation guidance for the Project Organizations functional area.

## When to Use

Use this functional-area skill after Project Financial Management scope is confirmed and the project needs project organizations setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `ERP`
- Offering: `Project Financial Management` (`PJF_PROJ_MNG`)
- Functional area / Setup Object: `Project Organizations` (`ORA_PJF_PROJ_ORG`)

## Setup Tasks

1. [Manage Project Unit Organizations](manage-project-unit-organizations/SKILL.md) (`PJF_MANAGE_PROJECT_UNIT_ORGANIZATIONS`)
2. [Manage Project Unit Options](manage-project-unit-options/SKILL.md) (`PJF_MANAGE_PROJECT_UNITS`)
3. [Manage Project Organization Classifications](manage-project-organization-classifications/SKILL.md) (`PJF_MANAGE_PROJECT_ORGANIZATION_CLASSIFICATIONS`)
4. [Manage Organization Hierarchies and Classifications](manage-organization-hierarchies-and-classifications/SKILL.md) (`PJF_MANAGE_ORGANIZATION_HIERARCHIES_AND_CLASSIFICATIONS`)
5. [Submit Process to Maintain Project Organizations](submit-process-to-maintain-project-organizations/SKILL.md) (`PJF_SUBMIT_PROCESS_TO_DENORMALIZE_ORGANIZATION_HIERARCHY`)
6. [Configure Project Accounting Business Function](configure-project-accounting-business-function/SKILL.md) (`PJF_CONFIGURE_PROJECT_ACCOUNTING_BUSINESS_FUNCTION`)

## Inputs

- `implementation_objective`
- `project_context`
- `project_organizations_scope`
- `project_organizations_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Parent-Owned Durable Outputs

Persist this parent's `functional_area_setup_plan`, `configuration_guidance` and
`validation_checkpoints` when they are produced or changed, before returning them
as a durable handoff. Project Organizations outputs summarize in-scope unit,
classification, hierarchy and accounting-function requirements and any proposed
Maintain Project Organizations handoff. A saved plan does not submit that ESS
process or establish that a child import or verification has completed.

1. Resolve one selected `project_id` from `project_context` and the active
   workflow, and reuse existing project artifacts. If no project exists, follow
   the repository project-initialization policy before writing. An ambiguous or
   conflicting project identity is an `input_validation` blocker; do not infer a
   different project or require the caller to repeat known context.
2. Preflight the candidate outputs, catalog/task identity, artifact metadata and
   destinations. Use the manifest's Project Organizations artifact directory under
   `project/{project_id}/artifacts/pillars/erp/project-financial-management/project-organizations/current/`,
   its decisions directory, run directory and shared token log as applicable.
   Resolve paths and reject traversal or symlinks escaping the selected project.
   Check existing versions and write conflicts before side effects. A missing or
   inconsistent task mapping is `catalog_or_metadata_mismatch`; an unconfirmed
   replacement is `approval_blocker`. Stop the affected handoff in either case.
3. Use `core.project-mgmt.artifact-version-manager` to compare existing and
   candidate artifacts. Create a new version for major changes; update an
   existing artifact for a minor change only after explicit confirmation. Keep
   append-only decisions and history intact. A no-change revisit reuses existing
   artifacts and registrations without replacing them.
4. Save changed parent outputs at their declared locations and register them
   through `core.project-mgmt.artifact-registry-manager` using
   `schemas/project-artifact.schema.json`: retain producing skill, location,
   version, actual review status, timestamps and checksum when available. Never
   mark an artifact approved merely because it was saved. Link child-owned
   evidence instead of copying or overwriting child artifacts or executor receipts.
5. Use `core.project-mgmt.project-state-manager` for deterministic updates
   supported by the existing state schema and limited to this parent's declared
   output categories. Record which run and artifact references caused a change.
   The `setup_task_sequence` category represents a saved planning proposal; it
   does not authorize changing the active workflow's sequence, route, current
   step or approvals. Return proposed changes to that workflow for adoption under
   its own gates; do not add state fields or maintain a parallel workflow state.
6. Record `skill_run_record` under `project/{project_id}/state/runs/` using
   `schemas/skill-run.schema.json`, with this parent's skill ID, input/output and
   artifact references, timestamps and actual status. Append a completed run for
   a successful no-change revisit as well. Record token usage at the manifest's
   shared token-log location through the declared project service's token-usage
   guidance; include the same estimate and log reference in the run's supported
   `token_usage` fields. Return the saved output and run references to the caller.

## Persistence Failure and Recovery

If an artifact write, registration, state update, run record or token-log write
fails, stop the affected parent handoff with `artifact_persistence`; do not claim
a completed durable result or continue child execution from it. Preserve safely
written artifacts and existing state. Record a failed run when writable, using
schema-supported `notes` and `artifact_refs` for the failed stage, failure class,
redacted cause, intended paths, completed writes and recommended recovery action.
If that record also cannot be written, report those details to the caller without
claiming that diagnostics were persisted or switching to another project.

Writes across these services are not assumed atomic. Do not retry blindly, delete
partial artifacts or replay child operations. On recovery, inspect existing files,
versions, checksums, registrations and state references; reconcile completed
steps and resume only the missing local persistence work, retaining the existing
versioning and confirmation gates. If a required service or supported contract
is unavailable, report the workflow gap instead of substituting another writer.
Never print or persist credentials, tokens, token-cache contents, private keys
or sensitive payloads. This procedure grants no external-operation authority.
