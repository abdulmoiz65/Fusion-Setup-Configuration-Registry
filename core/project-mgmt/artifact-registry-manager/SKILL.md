---
skill_id: "core.project-mgmt.artifact-registry-manager"
name: "Artifact Registry Manager"
description: "Registers generated skill outputs in the project artifact index and maps each artifact to the skill that produced it."
layer: "core"
pillar: "Core"
type: "import"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.1.0"
inputs:
  - "artifact_metadata"
  - "skill_id"
  - "artifact_location"
outputs:
  - "artifact_record"
  - "updated_artifact_index"
uses_core: []
persists_project_state: true
state_updates:
  - "skill_path"
workspace_outputs:
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/artifact-index.json"
    versioning_policy: "replace-after-confirmation"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Updates the local project artifact index."
required_privileges: []
---

# Artifact Registry Manager

## Purpose

Registers generated skill outputs in the project artifact index and maps each artifact to the skill that produced it.

## When to Use

Use this skill after any skill writes an output artifact under `project/{project_id}/artifacts`, `project/{project_id}/baselines`, `project/{project_id}/exports`, `project/{project_id}/decisions`, or `project/{project_id}/blueprints`.

## Inputs

- `artifact_metadata`
- `skill_id`
- `artifact_location`

## Outputs

- `artifact_record`
- `updated_artifact_index`

## Implementation Notes

Every artifact record must include artifact type, producing skill, location, version, status, timestamps, and checksum when available.
