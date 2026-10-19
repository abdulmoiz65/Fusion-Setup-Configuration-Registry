---
skill_id: "core.fusion-api.fsm-rest-client"
name: "FSM Rest Client"
description: "Provides the fsm rest client core capability for Oracle Fusion Cloud implementation workflows."
layer: "core"
pillar: "Core"
type: "import"
execution_mode: "automated"
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
side_effects: 
  - "May connect to a Fusion environment when implemented and approved."
required_privileges: 
  - "Fusion privileges appropriate to the requested operation"
---

# FSM Rest Client

## Purpose

Provides the FSM REST client core capability for Oracle Fusion Cloud
implementation workflows, including setup offering and functional-area
discovery through Fusion REST and BOSS extraction endpoints.

## When to Use

Use this core skill when another router, shared, or pillar skill needs a reusable platform primitive instead of duplicating implementation-specific connection, loading, export, import, or diagnostic logic.

Use the shared `core.fusion-api.rest-api-client` skill for endpoint execution.
For BOSS endpoints under `/api/boss`, route to
`core/fusion-api/rest-api-client/references/boss-rest-api.md` and invoke
`core/fusion-api/rest-api-client/scripts/boss-rest_client.py`.

For setup-task discovery by offering and functional area, use
[`references/tasks-by-feature.md`](references/tasks-by-feature.md). This
reference defines the `tasksByFeature` BOSS endpoint, required scope-code
parameters, and safe invocation pattern.

## Project Scripts

Run from the repository root.

Retrieve available setup functional areas for an offering short code:

```bash
python3 core/fusion-api/rest-api-client/scripts/boss-rest_client.py \
  /api/boss/extraction/queries/ora/commonSetup/features/v1/availableSetupFunctionalAreasByOffering \
  --query parentShortName=DOO_ORCHESTRATION
```

The BOSS script uses `boss_scope` and `.fusionaim_boss_token.json` by default.
Pass an offering short code from `knowledge/setup-task-catalog/release/Offerings_catalog.json`
as `parentShortName`.

## References

Read `references/available-features.md` when the request is to retrieve available
Fusion features. Use its script for the BOSS `setupEntities` query. By default,
return only the first 25 rows with Feature Name, Feature Shortname (Code), and
Product. Fetch every page and write a CSV only when the user explicitly asks
for all features.

Read `references/available-functional-areas.md` when the request is to retrieve
available functional areas. It follows the same 25-row preview and explicit
full-CSV-export behavior.

Read the matching reference for Business Objects, Offerings, Task Lists, or
Tasks: `available-business-objects.md`, `available-offerings.md`,
`available-task-lists.md`, or `available-tasks.md`.

Read `references/tasklist-tasks.md` when the request is for the items in each
task list, including task-list nesting, item type, and display sequence. Return
25 rows by default and generate the complete CSV only on an explicit request.

Read `references/promo-code-feature.md` when the request is for promotion-code
solution bundles and their features. Return 25 rows by default and generate the
complete five-column CSV only on an explicit request.

Read `references/tasks-bo.md` when the request is for setup-task to
business-object relations. Return 25 rows by default and generate the complete
five-column CSV only on an explicit request.

Read `references/offering-fa-feature.md` when the
request is to retrieve the report-shaped offering → functional area → feature
hierarchy with product, path, classification, and dependency release versions.
Follow the invocation details in `references/offering-fa-feature.md` for
the bounded preview or explicit full CSV export. Read
`references/offering-fa-feature-tasks.md` only when task relationship rows are
required.

Read `references/fa-feature-tl-tasks.md` when the request is for the
`FA_FEATURE_TL_Tasks` report: product, feature filter name, classification,
release versions, and directly associated task lists or tasks. Return 25 rows
by default; retrieve the complete list and write its exact seven-column CSV
only when the user explicitly asks for the entire list.

Read `references/offering-fa-feature-tl-task-bo.md` when the request is for the
report-shaped offering → FA/feature → task list → task → business object mapping
with product, classification, and hierarchy path. Run
`scripts/offering-fa-feature-tl-task-bo.py` for a bounded preview or explicit
full CSV export.

Read `references/parent-child-feature-hierarchy.md` when
the request is for direct parent-to-child feature relationships, feature codes,
classifications, display sequence, or product context. Follow
`references/parent-child-feature-hierarchy.md` for
a bounded preview or an explicit full CSV export.

## Inputs

- `fusion_environment_context`
- `request_payload`
- `execution_options`

Script-level inputs for the available functional-area lookup:

- `parentShortName`: offering short code, for example `DOO_ORCHESTRATION`.
- `--token-cache`: optional override for the file token cache. Leave unset to use
  `.fusionaim_boss_token.json` for BOSS endpoints.

## Outputs

- `execution_result`
- `diagnostics`
- `audit_summary`

## Implementation Notes

This file defines the contract for the capability. Implementations must record request parameters, environment identity, side effects, and any job or API identifiers returned by Fusion.

Never use the default `scope` token for `/api/boss` endpoints. The REST client
must obtain an OAuth access token using `boss_scope` before invoking BOSS
resources.

Authenticated BOSS requests may use only HTTPS hosts configured by
`restBaseUrl` or `*_restBaseUrl` in `core/auth/fusionEnv.properties`; reject
all other hosts and redirects to them.
