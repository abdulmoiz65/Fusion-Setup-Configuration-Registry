---
skill_id: "core.project-mgmt.artifact-version-manager"
name: "Artifact Version Manager"
description: "Applies project artifact versioning rules when regenerated skill outputs introduce major or minor changes."
layer: "core"
pillar: "Core"
type: "verification"
execution_mode: "assisted"
owner_team: "Central platform team"
version: "0.1.0"
inputs:
  - "existing_artifact"
  - "candidate_artifact"
  - "change_assessment"
  - "user_confirmation"
outputs:
  - "versioning_decision"
  - "artifact_record_update"
depends_on:
  - "core.project-mgmt.artifact-registry-manager"
uses_core: []
persists_project_state: true
state_updates:
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "reports"
workspace_outputs:
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/{skill-path}/artifact-index.json"
    versioning_policy: "major-new-version-minor-confirm-update"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "May supersede an artifact version or update the current artifact after user confirmation."
required_privileges: []
---

# Artifact Version Manager

## Purpose

Applies project artifact versioning rules when regenerated skill outputs introduce major or minor changes.

## When to Use

Use this skill when a previously generated artifact is regenerated or materially changed by a revisited skill.

## Inputs

- `existing_artifact`
- `candidate_artifact`
- `change_assessment`
- `user_confirmation`

## Outputs

- `versioning_decision`
- `artifact_record_update`

## Implementation Notes

Create a new version for major changes. For minor changes, update the current artifact only after explicit user confirmation. Append no-change skill runs without changing the current artifact.
