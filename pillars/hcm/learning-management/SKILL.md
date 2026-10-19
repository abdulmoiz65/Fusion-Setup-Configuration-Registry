---
skill_id: "hcm.learning-management"
name: "Learning Management"
description: "Scope Oracle Learning implementation work and route setup to Learning Management Common and the owning functional-area skills. Keeps offering-level decisions and work-product references; detailed setup guidance lives in the selected child."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Learning Management pillar team"
version: "0.4.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "hcm_scope"
  - "learning_management_requirements"
  - "foundation_setup_inputs"
  - "current_configuration_evidence"
  - "learning_setup_capabilities_in_scope"
outputs:
  - "learning_management_scope"
  - "functional_area_skill_plan"
  - "learning_management_work_products"
  - "setup_capability_assessment"
  - "foundation_configuration_proposal"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.project-intake.scope-definition"
  - "shared.implementation-planning.offering-task-map-builder"
  - "hcm.learning-management.learning-management-common"
uses_core:
  - "core.project-mgmt.project-state-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.artifact-version-manager"
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
  - "scope"
  - "skill_path"
  - "setup_task_sequence"
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "scope"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/current/"
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
  - "Persists offering scope, routing decisions and child work-product references in the active project; does not execute Fusion setup changes."
required_privileges: []
---

# Learning Management

## Purpose and Entry

Coordinate offering scope and route work to the responsible functional area.
For implementation work, enter through
[Implementation Router](../../../router/implementation-router/SKILL.md) and
reuse the selected project's objective, decisions and evidence. This parent
does not own profile, lookup, flexfield or other setup procedures.

For a general “set up Learning” request, route initial capability assessment to
[Learning Management Common](learning-management-common/SKILL.md), using its
[offering-wide intake and response](learning-management-common/references/setup-capability-handoffs.md#offering-wide-intake-and-response).
Present all catalog functional areas for scope assessment before narrowing to
applicable PM capabilities C1–C8 or selected tasks. Self-Paced Learning and
Catalog Administration Profiles both belong in Learning Catalog; a delivery-mode
answer does not select the entire implementation scope. Common handles its own
foundations and returns explicit handoffs for capabilities owned elsewhere.
Assessment coverage is not a mandate to configure every area or authorization
to create catalog content. Preserve a user's explicitly narrower request.

## Catalog Identity

- Pillar: `HCM`
- Offering: `Learning Management` (`ORA_LEARNING_MANAGEMENT`)
- Offering mapping: `knowledge/setup-task-catalog/effective/pillars-offerings-mapping.json`
- Task hierarchy: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`

## Routing Responsibility

| Requested work | Route |
| --- | --- |
| Common foundations or guided setup assessment | [Learning Management Common](learning-management-common/SKILL.md); its task Markdown files own the detailed setup decisions and its references own intake, proposals and handoffs. |
| Catalog administration profiles | [Existing CAP child](learning-catalog/manage-catalog-administration-profiles/SKILL.md). The current catalog associates this task with Learning Catalog; preserve the child's supported operations and approval gates. |
| Learning audience criteria or user groups | [Existing Learning Audience child](learning-audience/SKILL.md); preserve its Data Loader/criteria contracts. |
| Learning defaults or background-processing configuration | [Learning Configurations](learning-configurations/SKILL.md); includes evaluation, enrollment, assignment, certificate, attendance and PM C7 topics. Its two live task contracts remain incomplete. |
| Security profiles/data roles, HCM Tool, resources, catalog transactions, assignments, recommendations, locations or external providers | Select the actual owning catalog area below and an existing supported project workflow. Common may capture related design questions; it does not become their executor. |

Pass known inputs and unresolved questions to the selected child; do not ask
for decisions already recorded. A missing user attribute calls for a focused
question while independent valid work continues. A missing or ambiguous
technical route stops the affected external operation, not all planning.
Do not use a browser, generic REST call or loader as an undeclared fallback.

Do not invoke a generator during an implementation merely because a child is
missing. Record the missing capability and the owner/next action. Repository
authoring is outside this implementation workflow; route missing capabilities
to the repository owner. Do not change an existing task
representation implicitly.

## Inputs and Outputs

The parent accepts the implementation objective, project context, HCM scope
and Learning requirements. Forward existing `foundation_setup_inputs`,
`current_configuration_evidence` and `learning_setup_capabilities_in_scope`
to Common without turning supplied files into a tenant baseline or approval.

Return `learning_management_scope`, `functional_area_skill_plan` and
`learning_management_work_products` with each selected child, readiness,
safe artifact references and next action. For existing callers,
`setup_capability_assessment`, `foundation_configuration_proposal` and
`validation_checkpoints` expose the corresponding Common/child work-product
references; their content is produced and maintained by that child.

## Functional Areas From Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_LEARNING_MANAGEMENT`
Functional area count: `11`
Setup task count: `37`

- `ORA_LEARNING_MANAGEMENT_COMMON`: Learning Management Common
- `ORA_LEARNING_MANAGEMENT_HCM_SECURITY_PROFILE`: Learning Management HCM Security Profile
- `ORA_LEARNING_MANAGEMENT_HCM_TOOL`: Learning Management HCM Tool
- `ORA_LEARNING_MANAGEMENT_LOCATIONS`: Learning Management Locations
- `ORA_LEARNING_CONFIGURATIONS`: Learning Configurations
- `ORA_LEARNING_RESOURCES`: Learning Resources
- `ORA_LEARNING_AUDIENCE`: Learning Audience
- `ORA_LEARNING_CATALOG`: Learning Catalog
- `ORA_LEARNING_ASSIGNMENT`: Learning Assignment
- `ORA_RECOMMENDATIONS`: Recommendations
- `ORA_EXTERNAL_PROVIDERS`: External Providers

## Persistence and Completion

Persist offering scope, task selection and child artifact references using
the manifest's project locations. Child-specific proposals, decisions and
validation results follow the child's workspace contract. Reuse earlier
project artifacts rather than deleting or silently moving them. Register
artifacts, update state, record the run and append/report token usage.

Completion means the requested scope is routed with clear ownership, existing
decisions and evidence passed through, and each unresolved item has an owner
and next action. It does not mean Fusion configuration has been executed.
External operations follow the selected child's preflight, approval,
verification and diagnostic rules; this refactor adds no live execution route.
Do not persist sensitive data, rosters, credentials or raw responses.

Reviewers: HCM Learning SME/Pillar Lead, FSCR core reviewer and QA; include
security review for access-design changes. Run the
[Common acceptance checks](learning-management-common/tests/acceptance.md) and
[preserved setup scenarios](learning-management-common/tests/learning-setup-acceptance.md).
