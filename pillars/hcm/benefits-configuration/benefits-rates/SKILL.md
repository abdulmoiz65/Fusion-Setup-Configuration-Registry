---
skill_id: "hcm.benefits-configuration.benefits-rates"
name: "Benefits Rates Implementation Guidance"
description: "Routes BenefitsStandardRate and VariableRateProfile HDL uploads, including ExtraInputValue and VrpAssociation child components, plus samples, validation, and results through core.data-loader for ORA_BENEFITS_RATES."
layer: "pillar"
pillar: "HCM"
offering: "Benefits Configuration"
functional_area: "Benefits Rates"
functional_area_code: "ORA_BENEFITS_RATES"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM benefits configuration pillar team"
version: "0.2.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "benefits_rates_scope"
  - "benefits_rates_requirements"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
uses_core:
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-rates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-rates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-rates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "BEN_MANAGE_BENEFIT_RATES"
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

# Benefits Rates Implementation Guidance

## Purpose

Provides HCM Benefits Configuration implementation guidance for the Benefits Rates functional area.

## When to Use

Use this functional-area skill after Benefits Configuration scope is confirmed and the project needs benefits rates setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Benefits Configuration` (`ORA_BENEFITS_CONFIG`)
- Functional area / Setup Object: `Benefits Rates` (`ORA_BENEFITS_RATES`)

## Setup Tasks

1. [Benefit Rates](benefit-rates.md) (`BEN_MANAGE_BENEFIT_RATES`)

## Inputs

- `implementation_objective`
- `project_context`
- `benefits_rates_scope`
- `benefits_rates_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## HDL Scope and Sources

The selected task is `BEN_MANAGE_BENEFIT_RATES`; `ORA_BENEFITS_RATES`
is its functional-area code, not a loader discriminator. Read
[the task metadata](benefit-rates.md) before routing a request.

The tested environment registers `BenefitsStandardRate` with `ExtraInputValue`
and `VrpAssociation` components. Oracle's overview uses the alternative names
`BenefitStandardRate` and `ExtraInputValues`; use the live registered names
for filenames and loader calls. Standard-rate maintenance includes create,
effective-dated update, correction, end dating, and deletion. A variable-rate
profile association is not creation of the referenced variable-rate profile.
Confirm each requested component and operation against target metadata.

### Upload routing

Select the root from the requested object or source contents, not the task's
standard-rate default. If an unqualified rates request has no identifying
source, ask whether it concerns standard rates or variable-rate profiles.

| Requested object/component | Registered root | DAT filename |
|---|---|---|
| BenefitsStandardRate | BenefitsStandardRate | BenefitsStandardRate.dat |
| ExtraInputValue | BenefitsStandardRate | BenefitsStandardRate.dat |
| VariableRateProfile | VariableRateProfile | VariableRateProfile.dat |
| VrpAssociation | BenefitsStandardRate | BenefitsStandardRate.dat |

Live Data Loader metadata checked on 2026-09-24 confirmed the two roots and
both standard-rate children. This is registration/template evidence, not a
successful upload test or a guarantee for another environment. Resolve the
current target metadata on every new validation; never use fixed attribute
lists or counts as the schema.

- `VariableRateProfile` is a separate root, not a `BenefitsStandardRate` child.
  Resolve its own template, keys, and supported operations through core.
- `ExtraInputValue` and `VrpAssociation` are child sections of the standard-rate
  root. Do not route them as standalone BOs or create `ExtraInputValue.dat` or
  `VrpAssociation.dat`. Preserve the exact singular component names.
- For child-only changes, resolve the existing parent and required references
  using live supported keys. Do not fabricate a parent MERGE row or create a
  rate, input value, formula, or profile merely to satisfy a missing reference.
  Keep the root filename/container; let core validate the child-only structure.
  For XLSX, follow core's root-sheet and child-sheet rules.
- When new profiles and dependent associations are requested together, plan
  separate dependency-ordered loads. Load profiles first, then confirm their
  successful completion through an explicitly requested status check before
  submitting dependent associations. Do not assume ZIP member order guarantees
  cross-root dependency processing or silently split a supplied archive.
- Preserve source bytes during review. A wrongly named child file requires a
  user-reviewed correction through core, not a guessed standalone registration.

Source: [Oracle: How You Manage Benefits Standard Rates Using HDL or HSDL](https://docs.oracle.com/en/cloud/saas/human-resources/faibf/how-you-manage-benefits-standard-rates-using-hdl-or-hsdl.html),
reviewed 2026-09-23. The source distinguishes HDL from HSDL; their operation
support must not be treated as interchangeable.

The catalog's `N` export/import and CSV flags describe FSM setup-data support.
They do not negate the documented HDL route or authorize FSM CSV export.
Do not invent an export endpoint or an HDL schema from those catalog flags.

## HDL Workflow

1. Establish the requested action: sample, attribute details, validation,
   load, or status. For maintenance, retain the user's distinction between
   update, correction, end dating, and deletion; do not turn one into another.
   Collect the target environment, rate identity, intended effective dates,
   requested components, and source artifact when relevant. Use prior project
   context where available.
2. Read [core.data-loader](../../../../core/data-loader/SKILL.md). Hand off
   HCM context, `BEN_MANAGE_BENEFIT_RATES`, import mode `HDL`, the documented
   root selected from the upload routing table, requested components,
   the requested operation, and the unchanged
   source path or business values. Preserve any existing Run Book context.
3. Let core.data-loader resolve the registered object and its current template,
   component hierarchy, required attributes, keys, and supported operations.
   Stop on missing or ambiguous registration. Do not substitute payroll
   `RateDefinition`, assume a REST resource with the same name, or fabricate
   DAT headers. Exact field and effective-date controls come from that metadata.
4. For sample requests, use the core sample workflow: XLSX by default and DAT
   only when explicitly requested. Retain its attribute-details and key-fields
   companions. Preserve documented children and parent linkage; do not add
   populated child records when the user has requested only a standard rate
   or a variable-rate profile. For a child sample, select the standard-rate
   root and identify the requested child; do not load unrelated sample rows.
   Sample generation performs no load.
   Create templates use placeholders, not existing rate values. For a request
   to derive a new rate from environment data, first use the core read-only
   update-sample route and require actual retrieved values. The tested
   environment returns 404 for the loader's generated BenefitsStandardRate
   FSCM read route. Until an authoritative supported read mapping or supplied
   rate export is available, stop that cloning workflow; do not submit a
   placeholder template or copy existing record identifiers into a create.
5. For source validation or load requests, use the core validation workflow
   for the selected HDL contract. Resolve the rate and child identities using
   supported keys; report missing references or ambiguous mappings through
   the core result. Do not create referenced setup objects as an implicit fix.
   Validate the requested date treatment before preparing the immutable archive.
6. For a load, let core.data-loader own source review, Task Hook validation,
   approval, upload, and initiation. Follow its approval policy without adding
   a second approval. Missing task resources follow the core Task Hook policy;
   do not claim a custom Benefits rule registry has run. Never call a native
   HDL service, import adapter, or UCM upload independently.
7. Return the core result in its required Markdown format. Accepted initiation
   is not completed import: retain the request ID and end the initiation turn.
   Route a subsequent status or errors request through core.data-loader and
   report returned counts and diagnostics, including partial failures.

## Failure and Recovery

- Input validation or catalog mismatch: identify the missing operation,
  ambiguous rate/object, unsupported component, or mismatched metadata and
  stop before submission. Do not guess a replacement.
- Authentication, privileges, or transport failures: use the core diagnostic
  and retry policy. Do not bypass it with another environment or credential.
- Failed or uncertain import: preserve the returned request ID and successful
  records. Inspect status/errors through core on request before considering a
  retry; never blindly resubmit a possibly accepted load.
- Corrected data requires a new validation and approval cycle under core's
  policy. Do not delete rates to simulate rollback.
- If a selected core operation times out, report its last status and next-check
  path; do not invent a completed outcome or an extra polling loop.

Runtime access and load privileges are checked by core.data-loader for the
chosen environment. Keep credentials and business data out of repository files.
The pillar owns durable planning decisions and the manifest's project outputs;
the loader owns its artifact and result contract. Reuse its returned evidence
when recording project results rather than creating duplicate loader logs.

## Review and Verification

Reviewers: HCM Benefits Pillar Lead or SME and FSCR A-Team/core reviewer.
Use [the synthetic workflow scenarios](tests/golden-scenarios.md) to review
routing and failure behavior. Schema and catalog validation are offline checks;
live registration, supported field controls, privileges, and successful imports
must be verified in the selected environment at execution time.
