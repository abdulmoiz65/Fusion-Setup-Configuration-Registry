---
skill_id: "hcm.workforce-absence-management"
name: "Workforce Absence Management"
description: "Coordinates HCM Workforce Absence Management implementation guidance and routes work to developer-created functional-area skills."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Absence Management"
type: "orchestration"
execution_mode: "assisted"
owner_team: "HCM Workforce Absence Management pillar team"
version: "0.2.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "hcm_scope"
  - "workforce_absence_management_requirements"
outputs:
  - "workforce_absence_management_scope"
  - "functional_area_skill_plan"
  - "workforce_absence_management_work_products"
  - "token_usage_record"
depends_on:
  - "shared.project-intake.scope-definition"
  - "shared.implementation-planning.offering-task-map-builder"
uses_core:
  - "core.fusion-dev.pillar-skill-gen"
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
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "scope"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
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

# Workforce Absence Management

## Purpose

Coordinates HCM Workforce Absence Management implementation guidance across functional areas, setup tasks, and standard implementation activities.

## When to Use

Use this offering-level skill after Workforce Absence Management is in scope and before routing to a specific functional-area skill.

## Catalog Identity

- Pillar: `HCM`
- Pillar slug: `hcm`
- Offering code: `ORA_WORKFORCE_ABSENCE_MANAGEMENT`
- Offering slug: `workforce-absence-management`
- Offering folder: `pillars/hcm/workforce-absence-management`
- Offering mapping source: `knowledge/setup-task-catalog/effective/pillars-offerings-mapping.json`
- Setup task catalog source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`

## Routing Responsibility

This skill routes control to functional-area skills created by developers under this folder. Developers should create functional-area skills with `core.fusion-dev.pillar-skill-gen` using the catalog-backed path pattern:

```text
pillars/hcm/workforce-absence-management/{functional-area-slug}/
```

When a requested functional area is not yet present under this offering, use the setup catalog below to identify the matching functional area and invoke `core.fusion-dev.pillar-skill-gen` to generate the child skill before adding functional-area-specific guidance.

## Implemented Functional Areas

- [Absence](absence/SKILL.md)
- [Absences Additional](absences-additional/SKILL.md)
- [Absence Management Common](absence-management-common/SKILL.md)

## Taxonomy Migration

The former `hcm.absence-management` skill hierarchy is replaced by the
catalog-backed `hcm.workforce-absence-management` hierarchy. Treat the path,
skill-ID, and project-output changes as a breaking migration for existing
consumers.

| Legacy identity | Current identity |
| --- | --- |
| `hcm.absence-management.absence` | `hcm.workforce-absence-management.absence` |
| `hcm.absence-management.absences-additional` | `hcm.workforce-absence-management.absences-additional` |
| `hcm.absence-management.common` | `hcm.workforce-absence-management.absence-management-common` |
| `hcm.absence-management.absence.leave-agreements` | `hcm.workforce-absence-management.absences-additional.leave-agreements` |

New project outputs use
`project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/`.
Existing project artifacts under the legacy path remain historical records and
must not be moved or overwritten implicitly.

The HCM dependency graph retains `hcm.absence-management.absence` and
`hcm.absence-management.absences-additional` as stable internal graph-node
identifiers. Treat those values as legacy graph keys, not as current skill
manifest IDs. Current skill and parent-skill references continue to use the
`hcm.workforce-absence-management` taxonomy.

## Inputs

- `implementation_objective`
- `project_context`
- `hcm_scope`
- `workforce_absence_management_requirements`

## Outputs

- `workforce_absence_management_scope`
- `functional_area_skill_plan`
- `workforce_absence_management_work_products`
- `token_usage_record`

## Functional Areas From Catalog

Source: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
Offering code: `ORA_WORKFORCE_ABSENCE_MANAGEMENT`
Functional area count: `12`
Setup task count: `33`

- `ORA_ABSENCE_MANAGEMENT_COMMON`: Absence Management Common
- `ORA_ABSENCE_MANAGEMENT_ENTERPRISE`: Absence Management Enterprise
- `ORA_ABSENCE_MANAGEMENT_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS`: Absence Management Legal and Legislative Organizations
- `ORA_ABSENCE_MANAGEMENT_ELEMENTS_EARNINGS_AND_DEDUCTIONS`: Absence Management Elements, Earnings and Deductions
- `ORA_ABSENCE_MANAGEMENT_PERSON_RECORD`: Absence Management Person Record
- `ORA_ABSENCE_MANAGEMENT_EMPLOYMENT_ACTIONS_FRAMEWORK`: Absence Management Employment Actions Framework
- `ORA_ABSENCE_MANAGEMENT_BENEFITS_ELIGIBILITY`: Absence Management Benefits Eligibility
- `ORA_ABSENCE_MANAGEMENT_WFM_COMMON`: Absence Management WFM Common
- `ORA_ABSENCE_MANAGEMENT_PAYROLL_TOOLS`: Absence Management Payroll Tools
- `ORA_ABSENCE_MANAGEMENT_PAYROLL_RATES_AND_VALUES`: Absence Management Payroll Rates and Values
- `ORA_ABSENCE`: Absence
- `ORA_ABSENCES_ADDITIONAL`: Absences Additional

## Implementation Notes

- Keep offering-level planning, scope decisions, sequencing, and cross-functional-area handoffs in this skill.
- Put functional-area-specific implementation guidance in generated child skills under this offering folder.
- Use `core.fusion-dev.pillar-skill-gen` for child functional-area skill creation so generated skills follow the repository contract.
- Use `core.fusion-dev.fusionapps-resource-authoring` after child skill creation when Oracle FusionApps `ora-resource/` guidance is needed.
- Do not create setup-task-specific skills directly under this offering folder unless the user explicitly requests nested task-level skill generation through the pillar skill generator.
