---
skill_id: "core.fusion-api.apps-common.lookups"
name: "Apps Common Lookups"
description: "Access Oracle Fusion common, standard, generic, and set-enabled lookups through the appropriate Application Common Features REST resource."
layer: "core"
pillar: "Core"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.2.0"
inputs: ["fusion_environment_context", "lookup_request", "execution_options"]
outputs: ["execution_result", "diagnostics", "audit_summary"]
depends_on: ["core.fusion-api.rest-api-client"]
uses_core: ["core.fusion-api.rest-api-client"]
persists_project_state: false
workspace_outputs: []
applicability:
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["Current Oracle Fusion Cloud Applications release"]
side_effects: ["May read or mutate lookup resources after explicit approval."]
required_privileges: ["Fusion privileges appropriate to the requested lookup resource"]
---

# Apps Common Lookups

## Purpose

Provide a focused, safely routed Application Common Features lookup workflow.

Use the shared `core/fusion-api/rest-api-client/scripts/fusion_rest_client.py`
with relative `/fscmRestApi` endpoints. Route by the caller's named lookup
view:

| Lookup view | Guidance |
| --- | --- |
| Common lookup | [common-lookups.md](references/common-lookups.md) |
| Standard lookup | [standard-lookups.md](references/standard-lookups.md) |
| Generic lookup | [generic-lookups.md](references/generic-lookups.md) |
| Set-enabled lookup | [set-enabled-lookups.md](references/set-enabled-lookups.md) |

For an ambiguous lookup request, make read-only discovery attempts in this
order: Common, Standard, Generic, then Set-Enabled. Stop on the first exact
resource match. A `401` or `403` is an authentication or privilege failure,
not evidence that the lookup is absent; stop and report it. Do not mutate while
identifying the lookup category.

Validate the target, resource key, and body before every request. Read the
current resource and obtain explicit approval before a create, update, or
delete. Do not retry a mutating request automatically; redact credentials,
tokens, and sensitive values from results.

## Preflight and Error Handling

Preflight the lookup view, target environment, privileges, returned resource
identity, body, and approval gate. Classify failures under
`governance/error-handling-guidelines.md`; report the endpoint and safe next
action while redacting credentials, bearer tokens, headers, and sensitive
lookup values.
