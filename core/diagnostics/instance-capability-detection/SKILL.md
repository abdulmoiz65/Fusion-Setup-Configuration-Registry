---
skill_id: "core.diagnostics.instance-capability-detection"
name: "Instance Capability Detection"
description: "Provides the instance capability detection core capability for Oracle Fusion Cloud implementation workflows."
layer: "core"
pillar: "Core"
type: "assessment"
execution_mode: "assisted"
owner_team: "Central platform team"
version: "0.1.0"
inputs: 
  - "fusion_environment_context"
  - "request_payload"
  - "execution_options"
outputs: 
  - "execution_result"
  - "diagnostics"
  - "audit_summary"
depends_on: []
uses_core: []
applicability:
  industries: 
    - "All"
  countries: 
    - "All"
  fusion_releases: 
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: 
  - "Fusion privileges appropriate to the requested operation"
---

# Instance Capability Detection

## Purpose

Provides the instance capability detection core capability for Oracle Fusion Cloud implementation workflows.

## When to Use

Use this core skill when another router, shared, or pillar skill needs a reusable platform primitive instead of duplicating implementation-specific connection, loading, export, import, or diagnostic logic.

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
