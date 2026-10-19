---
skill_id: "core.fusion-api.apps-common.profile-options"
name: "Apps Common Profile Options"
description: "Read effective Oracle Fusion profile values and manage configured profile-option values through the supported Application Common Features REST resources."
layer: "core"
pillar: "Core"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.2.0"
inputs: ["fusion_environment_context", "profile_option_request", "execution_options"]
outputs: ["execution_result", "diagnostics", "audit_summary"]
depends_on: ["core.fusion-api.rest-api-client"]
uses_core: ["core.fusion-api.rest-api-client"]
persists_project_state: false
workspace_outputs: []
applicability:
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["Current Oracle Fusion Cloud Applications release"]
side_effects: ["May read or mutate profile-option values after explicit approval."]
required_privileges: ["FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV to create, update, or delete profile option values"]
---

# Apps Common Profile Options

## Purpose

Provide focused access to effective and configured profile option values.

Read [profile-options guidance](references/profile-options.md) before acting.
Use `core/fusion-api/rest-api-client/scripts/fusion_rest_client.py` with a
relative `/fscmRestApi` endpoint. Validate the profile definition, level,
target, resource key, and body first. Read the current value and obtain
explicit approval before a write; do not retry a mutating request automatically.

## Preflight and Error Handling

Preflight the environment, privilege, profile definition, level, resource key,
body, and approval gate. Classify failures under
`governance/error-handling-guidelines.md`; redact credentials, bearer tokens,
headers, and sensitive profile values from diagnostics.

## Post-Mutation User Notification

After a successful create, update, or delete of a profile-option value, inform
the user that the change is effective immediately but is visible only in their
next Fusion user session. Tell the user to re-login to Fusion to verify that
the change is effective.
