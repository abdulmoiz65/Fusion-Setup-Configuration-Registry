---
skill_id: "core.project-mgmt.configuration-baseline-manager"
name: "Configuration Baseline Manager"
description: "Creates and registers project baselines from exported Fusion setup and configuration artifacts."
layer: "core"
pillar: "Core"
type: "export"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.1.0"
inputs:
  - "configuration_exports"
  - "baseline_scope"
  - "source_instance"
outputs:
  - "configuration_baseline"
  - "baseline_artifact_refs"
  - "updated_project_state"
depends_on:
  - "shared.setup-export.functional-area-export"
  - "shared.setup-export.offering-export"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
uses_core: []
persists_project_state: true
state_updates:
  - "exports"
  - "baselines"
workspace_outputs:
  - artifact_type: "configuration_export"
    default_location: "project/{project_id}/exports/"
    versioning_policy: "append-only"
  - artifact_type: "configuration_baseline"
    default_location: "project/{project_id}/baselines/"
    versioning_policy: "major-new-version-minor-confirm-update"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Registers local baseline artifacts created from exported setup data."
required_privileges:
  - "Fusion privileges required to export setup and configuration data"
---

# Configuration Baseline Manager

## Purpose

Creates and registers project baselines from exported Fusion setup and configuration artifacts.

## When to Use

Use this skill after setup or configuration data has been exported and the project needs a named baseline for design, comparison, validation, or migration planning.

## Inputs

- `configuration_exports`
- `baseline_scope`
- `source_instance`

## Outputs

- `configuration_baseline`
- `baseline_artifact_refs`
- `updated_project_state`

## Implementation Notes

Store raw exports under `project/{project_id}/exports/` and curated baselines under `project/{project_id}/baselines/`. Baseline records must reference the exact exports used to create them.
