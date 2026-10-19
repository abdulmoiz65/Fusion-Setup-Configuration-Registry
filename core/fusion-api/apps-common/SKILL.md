---
skill_id: "core.fusion-api.apps-common"
name: "Apps Common"
description: "Routes Oracle Fusion Application Common Features requests to a focused nested skill for lookups, flexfields, profile options, trees, or value sets. Extensible Flexfield requests use task-level CSV export and Data Loader FSM CSV import."
layer: "core"
pillar: "Core"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.2.0"
inputs: ["fusion_environment_context", "common_feature_request", "execution_options"]
outputs: ["execution_result", "diagnostics", "audit_summary"]
depends_on: ["core.fusion-api.rest-api-client", "shared.setup-export.task-level-export", "core.data-loader"]
uses_core: ["core.fusion-api.rest-api-client"]
persists_project_state: false
workspace_outputs: []
applicability:
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["Current Oracle Fusion Cloud Applications release"]
side_effects: ["Routes to a nested Application Common Features skill; the selected skill declares any external operation."]
required_privileges: ["Privileges appropriate to the selected Application Common Feature"]
---

# Apps Common

## Purpose

This stable entry point preserves compatibility for callers that invoke
`core/fusion-api/apps-common`. Select and follow exactly one nested skill;
callers that already know the feature may invoke that nested skill directly.

## Route the Request

| Calling context | Nested skill |
| --- | --- |
| Lookup type, lookup code, translation, or reference-data set | [lookups](lookups/SKILL.md) |
| Descriptive Flexfield (DFF) setup task | [descriptive-flexfields](descriptive-flexfields/SKILL.md) |
| Extensible Flexfield (EFF) request | [extensible-flexfields](extensible-flexfields/SKILL.md) |
| Attachment entity, category, or file-format setup task | [attachments](attachments/SKILL.md) |
| Key Flexfield (KFF) request | [key-flexfields](key-flexfields/SKILL.md) |
| Effective or configured profile option value | [profile-options](profile-options/SKILL.md) |
| Tree or tree-version request | [trees](trees/SKILL.md) |
| Value set, validation table, or value-set value | [value-sets](value-sets/SKILL.md) |

If the request crosses these boundaries, route each independently. Do not use
this router to select a REST endpoint or substitute a direct client call for a
nested workflow.

DFF, EFF, and KFF setup-task exports route through
`shared.setup-export.task-level-export`. Their setup-task imports route through
`core.data-loader` as `FSM CSV Import` after the respective nested skill
resolves task context and verifies its eligibility.

## Shared Boundaries

Nested skills use the shared REST client or the declared setup-task workflow.
They require target, operation, resource identity, and body validation before
an external operation; writes require explicit approval immediately before the
declared execution step. Do not retry a mutating request automatically.

## Preflight and Error Handling

Preflight the selected nested skill's inputs, target environment, privileges,
resource identity, and approval gate before an external operation. Classify a
failure using `governance/error-handling-guidelines.md` and return the selected
route plus safe next action. Redact credentials, bearer tokens, headers, and
sensitive feature values from diagnostics and audit summaries.

Run the focused offline contract tests from the repository root:

```bash
for test_dir in core/fusion-api/apps-common/*/tests; do
  python3 -m unittest discover -s "$test_dir" -p 'test_*.py' -v
done
```
