---
skill_id: "shared.validation.setup-data-validator"
name: "Setup Data Validator"
description: "Provides cross-pillar setup data validator guidance for Oracle Fusion Cloud implementations."
layer: "shared"
pillar: "Common"
type: "validation"
execution_mode: "assisted"
owner_team: "Shared enablement team with pillar review"
version: "0.1.1"
inputs: 
  - "implementation_objective"
  - "project_context"
  - "pillar_scope"
  - "offering_scope"
  - "functional_area_scope"
  - "setup_data_zip"
  - "task_code"
  - "task_name"
outputs: 
  - "recommendations"
  - "work_products"
  - "review_points"
  - "validation_findings"
  - "validation_report"
  - "token_usage_record"
uses_core: []
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

# Setup Data Validator

## Purpose

Provides cross-pillar setup data validator guidance for Oracle Fusion Cloud implementations. The validator resolves the applicable pillar and setup-task metadata before validating setup data. It does not perform task-specific Ora Resource validation; `core.data-loader.task-hook` governs that validation in Data Loader workflows.

## When to Use

Use this shared skill when setup data is being reviewed before import, migration, baseline comparison, or release readiness. The skill is shared, but the validation must be specialized by the detected offering, functional area, and setup task metadata from `pillars/*`.

## Inputs

- `implementation_objective`
- `project_context`
- `pillar_scope`
- `offering_scope`
- `functional_area_scope`
- `setup_data_zip`
- `task_code`
- `task_name`

## Outputs

- `recommendations`
- `work_products`
- `review_points`
- `validation_findings`
- `validation_report`

## Pillar Context Resolution

Before validating a setup data artifact, resolve the functional-area pillar skill and setup-task metadata using files under `pillars/*`.

Use `scripts/setup_data_validation_context.py` to resolve:

- offering skill metadata, when an offering-level skill exists
- functional area skill metadata
- setup task metadata
- default validation report location under `project/{project_id}`

Example:

```bash
python3 shared/validation/setup-data-validator/scripts/setup_data_validation_context.py \
  --task-code EGP_MANAGE_ITEM_ORGANIZATIONS \
  --project-id item-master-demo-mvp
```

For JSON context:

```bash
python3 shared/validation/setup-data-validator/scripts/setup_data_validation_context.py \
  --task-code INV_MANAGE_INVENTORY_ORGANIZATIONS \
  --project-id item-master-demo-mvp \
  --json
```

The validator should prefer `task_code` when available because task names can vary in capitalization or wording across exports and implementation documents.

## Validation Guidance Sources

Use these guidance sources for shared artifact checks:

1. Metadata and implementation notes from the resolved task metadata, functional area skill, and offering skill, excluding Ora Resource content.
2. Current Oracle Fusion Cloud documentation for setup task CSV export/import, implementation projects, and the applicable offering or functional area.

Do not use task-local or setup-object-local Ora Resource files as validation criteria in this shared skill. Task Hook owns that validation in the Data Loader workflow.

## Validation Workflow

1. Resolve pillar metadata from the setup task code or setup task name.
2. Inspect the resolved offering, functional area, and setup-task metadata.
3. Do not load or execute task-specific Ora Resource validation; leave it to `core.data-loader.task-hook`.
4. Inspect the setup data ZIP contents, manifest, CSV files, row counts, headers, required identifiers, dependencies, and import readiness signals that can be evaluated without Ora Resource rules.
5. Map each shared finding to the pillar skill metadata or Oracle documentation reference that supports it.
6. Persist findings in Markdown table format under:

```text
project/{project_id}/artifacts/shared/validation/setup-data-validator/{task_name_kebab}/current/
```

7. Include a concise decision summary for the shared validation scope, such as `ready`, `conditionally ready`, or `not ready`, and identify shared import blockers separately from advisory findings.

## Required Finding Table Columns

Validation reports must include tabular findings with these columns where applicable:

- `ID`
- `Severity`
- `Area`
- `Finding`
- `Evidence`
- `Recommendation`
- `Source`

## Implementation Notes

Keep outputs reusable by pillar skills. Where the guidance depends on a specific offering, country, release, or setup task, capture that condition in the work product rather than hardcoding it in the generic shared method.

Do not place validation outputs in a root-level implementation folder. All validation reports and derivative artifacts must stay under `project/{project_id}`.
