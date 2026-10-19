---
skill_id: "core.fusion-api.apps-common.value-sets"
name: "Apps Common Value Sets"
description: "Read Oracle Fusion value sets and manage supported value-set values through the Application Common Features REST resources."
layer: "core"
pillar: "Core"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.2.0"
inputs: ["fusion_environment_context", "value_set_request", "execution_options"]
outputs: ["execution_result", "diagnostics", "audit_summary"]
depends_on: ["core.fusion-api.rest-api-client"]
uses_core: ["core.fusion-api.rest-api-client"]
persists_project_state: false
workspace_outputs: []
applicability:
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["Current Oracle Fusion Cloud Applications release"]
side_effects: ["May mutate supported value-set values after explicit approval."]
required_privileges: ["Fusion privileges appropriate to the requested value-set resource"]
---

# Apps Common Value Sets

## Purpose

Provide focused access to value sets and their supported child values.

Read [value-sets guidance](references/value-sets.md) before acting. Use
`core/fusion-api/rest-api-client/scripts/fusion_rest_client.py` with a relative
`/fscmRestApi` endpoint. Validate returned identifiers and the body; read the
current value and obtain explicit approval before a write. Do not retry a
mutating request automatically.

## Preflight and Error Handling

Preflight the environment, privilege, returned value-set identifiers, body,
and approval gate. Classify failures under
`governance/error-handling-guidelines.md`; redact credentials, bearer tokens,
headers, and sensitive value-set values from diagnostics.
