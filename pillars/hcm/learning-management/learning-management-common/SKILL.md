---
skill_id: "hcm.learning-management.learning-management-common"
name: "Learning Management Common Implementation Guidance"
description: "Plan and validate Oracle Learning foundations using the approved Common taxonomy: profile options, lookups, value sets, DFFs, search, audit, and data-load, background-process and Redwood handoffs. Includes Learning security decision support; execution stays with the selected core or shared provider."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Management Common"
functional_area_code: "ORA_LEARNING_MANAGEMENT_COMMON"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM learning management pillar team"
version: "0.2.3"
inputs:
  - "implementation_objective"
  - "project_context"
  - "learning_management_common_scope"
  - "learning_management_common_requirements"
  - "source_documents_and_business_decisions"
  - "verified_baseline_and_provider_readiness_when_available"
  - "foundation_setup_inputs"
  - "current_configuration_evidence"
  - "learning_setup_capabilities_in_scope"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
  - "learning_common_proposal"
  - "foundation_configuration_proposal"
  - "setup_capability_assessment"
  - "learning_setup_inventory"
  - "security_decision_handoff"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "shared.best-practices.security-role-guidance"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
  - "core.data-loader"
  - "core.fusion-api.apps-common"
  - "core.fusion-api.apps-common.profile-options"
  - "core.fusion-api.apps-common.lookups"
  - "core.fusion-api.apps-common.value-sets"
  - "core.fusion-api.apps-common.descriptive-flexfields"
  - "core.fusion-api.audit-setup"
  - "core.fusion-api.ess-job-submitter"
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
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-management-common/current/learning-setup-inventory.json"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-management-common/current/learning-setup-inventory.md"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-management-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-management-common/current/foundation-configuration-proposal.json"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-management-common/current/foundation-validation.json"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "FND_MANAGE_PROFILE_OPTIONS"
  - "FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES"
  - "FND_MANAGE_COMMON_LOOKUPS"
  - "FND_MANAGE_VALUE_SETS"
  - "FND_MANAGE_DESCRIPTIVE_FLEXFIELDS"
  - "ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS"
  - "ORA_FND_SUGGESTION_GROUPS"
  - "ORA_FND_MANAGE_INDEX_CONFIGURATION"
  - "FND_MANAGE_AUDIT_POLICIES"
  - "ORA_GMS_MANAGE_AUDIT_TYPES"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Writes sanitized plans, decisions, validation results and run records in the active implementation project."
  - "External reads, exports, imports, deployments and writes occur only through a separately selected provider workflow and its gates."
required_privileges:
  - "None for offline planning; exact environment and operation privileges must pass the selected provider's preflight before external access."
---

# Learning Management Common Implementation Guidance

## Purpose

Own Learning-specific decisions for shared application foundations, not new
transport, authentication or permission-assignment implementations. This is an
assisted functional-area skill, not a claim that every listed task has an
end-to-end live execution contract.

## When to Use

Use this functional-area skill after Learning Management scope is confirmed and the project needs learning management common setup planning, baseline export, import sequencing, or validation checkpoints.

For implementation work, enter through the repository implementation router and
reuse the selected project. Authoring this skill does not itself start a tenant
setup run. Read [taxonomy and source reconciliation](references/taxonomy-and-sources.md)
first. The taxonomy's P0/cleared labels are roadmap metadata, not tenant readiness.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Learning Management` (`ORA_LEARNING_MANAGEMENT`)
- Functional area / Setup Object: `Learning Management Common` (`ORA_LEARNING_MANAGEMENT_COMMON`)

## Setup Tasks

1. [Manage Profile Options](manage-profile-options.md) (`FND_MANAGE_PROFILE_OPTIONS`)
2. [Manage Administrator Profile Values](manage-administrator-profile-values.md) (`FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`)
3. [Manage Common Lookups](manage-common-lookups.md) (`FND_MANAGE_COMMON_LOOKUPS`)
4. [Manage Value Sets](manage-value-sets.md) (`FND_MANAGE_VALUE_SETS`)
5. [Manage Descriptive Flexfields](manage-descriptive-flexfields.md) (`FND_MANAGE_DESCRIPTIVE_FLEXFIELDS`)
6. [Manage Applications Core Global Search Configurations](manage-applications-core-global-search-configurations.md) (`ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS`)
7. [Manage Applications Core Global Search Suggestion Groups](manage-applications-core-global-search-suggestion-groups.md) (`ORA_FND_SUGGESTION_GROUPS`)
8. [Manage Search Indexes](manage-search-indexes.md) (`ORA_FND_MANAGE_INDEX_CONFIGURATION`)
9. [Manage Audit Policies](manage-audit-policies.md) (`FND_MANAGE_AUDIT_POLICIES`)
10. [Manage Audit Types](manage-audit-types.md) (`ORA_GMS_MANAGE_AUDIT_TYPES`)

## Inputs

- `implementation_objective`
- `project_context`
- `learning_management_common_scope`
- `learning_management_common_requirements`
- Relevant business decisions or supported source files, and verified baseline
  evidence when available; files are not approval or proof of tenant state.

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`
- `learning_common_proposal`: versioned, sanitized JSON current-to-proposed rows.
- `learning_setup_inventory`: item-by-item requirements, configured state,
  confirmed gaps and unverified items in JSON and a readable report, delivered
  before change proposals for broad setup/review requests.
- `security_decision_handoff`: persona/action/data-scope decisions, unresolved
  questions and acceptance cases, not a role-assignment payload.

## Read Order and Ownership

1. For a broad setup request, read [offering-wide intake and response](references/setup-capability-handoffs.md#offering-wide-intake-and-response),
   then the C1–C8 capability assessment in that reference. Present the complete
   functional-area scope, including all current Learning Catalog child task
   routes and separately identified deferred capabilities. Common owns its
   foundations, not the other areas' executors. For a specific request, select
   the corresponding task above directly without expanding its scope.
2. Read [Common workflow](references/workflow.md) for intake, provider selection,
   proposal JSON, approval, reconciliation and project compatibility. Detailed
   profile/lookup review buckets and source conflicts live in their task files.
   Apply its [validation and confirmation summary](references/workflow.md#implementer-facing-validation-and-confirmation)
   for accepted inputs, actionable gaps and provider-resolved operation counts.
   For broad setup/review requests or a requested configured/missing list, read
   [setup inventory](references/setup-inventory.md) and deliver that inventory
   before proposing changes. A partial assessment still lists unverified areas;
   counts or a change-only table do not replace the item-by-item report.
3. Read only the selected task's Markdown guidance. For access design also read
   [security decisions](references/security-decisions.md); HCM Security Profile,
   HCM Data Role, HCM Tool and CAP retain separate ownership.
   For DFF verification, use the task's [export and evidence contract](references/dff-verification.md);
   preparing an export and assessing its returned data are separate stages.
4. Before task-node validation, read the
   [execution guide](references/task-node-execution.md),
   run `scripts/rule_plan.py` for the exact task, and load only its rows and source anchors
   from [ora-resource](ora-resource/ora_input_validation.md). Incomplete contracts
   remain incomplete; this documentation move does not bypass their gates.
5. Read the selected provider SKILL.md and required references before external
   steps. Core owns service versions, clients and execution mechanics.

## Dependencies and Design Pattern

Use the [dependency and provider map](references/dependencies.md) to select
the shared services, task provider and conditional business prerequisites.
Global Human Resources Common is an authoring reference only: reuse its
functional-area manifest, task index, shared-provider routing and validation
pattern with Learning's own taxonomy and contracts. It is not a Learning
dependency, runtime prerequisite or execution handoff.

The numbered task list is catalog order, not an approved execution sequence.
Resolve dependencies through the declared shared planner; legacy graph nodes
do not establish prerequisites for this functional area. Missing execution
contracts remain explicit and are not made executable by regeneration.

## Common Taxonomy and Related Setup

The ten task files above retain their generated identities and flags. The
[complete taxonomy](references/taxonomy-and-sources.md) also includes Data Load
and Migration, Background Process, and Visual Builder/Redwood Extension
foundations; their [non-FSM handoffs](references/setup-capability-handoffs.md#non-fsm-foundation-handoffs)
do not create additional FSM task codes.

Search task files preserve the blank-business-object guard. Audit Types
retains its catalog-owner clarification requirement. Profile enablement does
not complete integration, extension, security, template or process setup.

`foundation_configuration_proposal` is the compatibility name for
`learning_common_proposal`. Return `setup_capability_assessment` to the offering
parent with selected routes, readiness, missing decisions and next actions.
Read the workflow's [existing-project compatibility rules](references/workflow.md#existing-project-compatibility-and-completion)
before creating a new version; do not delete prior offering-level artifacts.

## Review and Verification

Owner: HCM Learning Management pillar team. Reviewers: Learning SME/Pillar Lead,
FSCR core reviewer, QA, and security reviewer for access-design changes.
Run [acceptance scenarios](tests/acceptance.md) and the preserved
[PM setup scenarios](tests/learning-setup-acceptance.md) with synthetic data. Repository
validation proves metadata, scope and graph integrity, not tenant behavior.
Keep Learning Audience and Catalog Administration Profiles operation contracts
unchanged and hand off to them only when separately requested.
