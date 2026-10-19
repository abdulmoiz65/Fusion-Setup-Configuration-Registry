---
skill_id: "shared.setup-import.rest-config-import"
name: "Rest Config Import"
description: "Provides the rest config import shared setup capability for Oracle Fusion Cloud implementation workflows."
layer: "shared"
pillar: "Common"
type: "import"
execution_mode: "hybrid"
owner_team: "Shared implementation enablement team"
version: "0.1.0"
inputs: 
  - "fusion_environment_context"
  - "request_payload"
  - "execution_options"
outputs: 
  - "execution_result"
  - "diagnostics"
  - "audit_summary"
  - "token_usage_record"
depends_on: []
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
side_effects: 
  - "May connect to a Fusion environment when implemented and approved."
required_privileges: 
  - "Fusion privileges appropriate to the requested operation"
---

# Rest Config Import

## Purpose

Provides the rest config import shared setup capability for Oracle Fusion Cloud implementation workflows.

## When to Use

Use this shared skill when another router, shared, or pillar skill needs a reusable cross-pillar setup import or export capability instead of duplicating implementation-specific connection, loading, export, import, or diagnostic logic.

## Inputs

- `fusion_environment_context`
- `request_payload`
- `execution_options`

## Outputs

- `execution_result`
- `diagnostics`
- `audit_summary`

## Implementation Notes

This file defines the contract for the capability. Implementations must record request parameters, environment identity, side effects, and any job or API identifiers returned by Fusion.
