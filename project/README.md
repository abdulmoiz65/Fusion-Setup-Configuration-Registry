# Project Workspace

This folder contains local implementation workspaces for a cloned FSCR
repository. Each implementation project gets its own containing folder named by
`project_id`.

Do not store customer secrets, passwords, access tokens, or private keys in this
folder. Runtime credentials should be supplied through an approved local secret
store or environment-specific credential profile.

## Workspace Structure

```text
project/
|-- _template/
|   |-- state/
|   |-- artifacts/
|   |-- baselines/
|   |-- exports/
|   |-- decisions/
|   `-- blueprints/
`-- {project_id}/
    |-- state/
    |   |-- project-state.json
    |   `-- runs/
    |-- artifacts/
    |   |-- router/
    |   |-- core/
    |   |-- shared/
    |   `-- pillars/
    |-- baselines/
    |-- exports/
    |-- decisions/
    `-- blueprints/
```

The project workspace initializer copies or materializes the `_template`
structure into `project/{project_id}/` when a new implementation project is
created.

The `artifacts` folder mirrors the skills repository structure. A skill with ID
`shared.implementation-planning.offering-task-map-builder` writes generated
artifacts under:

```text
project/{project_id}/artifacts/shared/implementation-planning/offering-task-map-builder/
```

A pillar offering skill such as `scm.product-management` writes generated
artifacts under:

```text
project/{project_id}/artifacts/pillars/scm/product-management/
```

A developer-generated child functional-area skill under that offering mirrors
its child folder:

```text
project/{project_id}/artifacts/pillars/scm/product-management/item-organizations/
```

Estimated token usage records for implementation tasks that write project
artifacts belong under:

```text
project/{project_id}/artifacts/shared/token-usage/
```

These records are operational estimates for planning and comparison, not
billing-grade usage metrics.

Workspace-updating activities must log token usage by default. Any script or
assisted workflow that creates or updates files under `project/{project_id}`
should append a row to:

```text
project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md
```

Repository scripts should use `core/project-mgmt/scripts/token_usage_logger.py`
instead of hand-writing the Markdown table.

## Persistent Project State

`project/{project_id}/state/project-state.json` is the current durable state of
the implementation. It should reference the latest objective, requirements,
scope, task sequence, baselines, decisions, configuration blueprints, and
validation outputs.

Router, project-intake, scope-definition, implementation-planning, baseline,
shared, and pillar skills must update this state through an artifact record
instead of relying on chat history.

## Artifact Versioning

Each generated artifact should have an artifact metadata record that follows
`schemas/project-artifact.schema.json`.

Use this rule when a skill is revisited:

1. Major change: create a new artifact version and mark the previous version as
   superseded.
2. Minor change: update the current artifact only after explicit user
   confirmation.
3. No material change: keep the current artifact and append the skill run record
   for auditability.

Recommended folder pattern:

```text
project/{project_id}/artifacts/{skill-path}/
|-- current/
|-- versions/
|   |-- v1.0.0/
|   `-- v2.0.0/
`-- artifact-index.json
```

## Baselines and Exports

Raw setup/configuration exports belong under `project/{project_id}/exports/`.
Curated project baselines belong under `project/{project_id}/baselines/` and
should include a `configuration-baseline.json` record that references the
exported files used to create the baseline.
