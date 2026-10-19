# Naming Conventions

FSCR naming conventions keep repository content predictable across router,
core, shared, pillar, knowledge, schema, governance, and project workspace
layers. Use lowercase kebab-case folders, uppercase `SKILL.md` manifests for
skills, dot-separated skill IDs, and project artifact paths that mirror the
skill hierarchy.

## Repository Layers

| Layer | Path Pattern | Naming Role |
| --- | --- | --- |
| `router` | `router/{skill-folder}/SKILL.md` | Entry-point orchestration and routing skills. Skill IDs start with `router`. |
| `core` | `core/{domain}/{skill-folder}/SKILL.md` | Reusable technical services and automation primitives. Skill IDs use `core.{domain}.{skill-name}`. |
| `shared` | `shared/{domain}/{skill-folder}/SKILL.md` | Cross-pillar implementation methodology. Skill IDs use `shared.{domain}.{skill-name}`. |
| `pillars` | `pillars/{pillar}/{offering}/{functional-area}/SKILL.md` | Oracle Fusion pillar, offering, functional-area, setup-object, and setup-task guidance. Generated paths use catalog-backed slugs. |
| `knowledge` | `knowledge/{catalog-or-data-domain}/...` | Catalogs, generated hierarchy-browser data, dependency graphs, templates, and reference data. |
| `schemas` | `schemas/{contract-name}.schema.json` | Machine-readable contracts and validation schemas. |
| `governance` | `governance/{topic}.md` | Contribution, naming, review, and release guidance. |
| `project` | `project/{project_id}/{artifact-area}/...` | Durable local implementation workspace. Project artifacts should mirror the skill structure where practical. |

## General Rules

| Object | Convention | Notes |
| --- | --- | --- |
| Folders | Lowercase kebab-case | Examples: `business-requirements-intake`, `order-management`, `supply-chain-planning`. |
| Skill manifests | `SKILL.md` only | Do not create lowercase `skill.md` files. |
| Flat setup-task metadata | Lowercase kebab-case `.md` | Allowed only when the file is metadata, not a skill manifest. |
| Skill IDs | Dot-separated lowercase segments | Segments may contain hyphens. Schema pattern: `^[a-z0-9]+(\.[a-z0-9-]+)+$`. |
| Artifact files | Descriptive lowercase kebab-case | Examples: `sample-business-requirements.yaml`, `setup-task-map.json`, `validation-results.json`. |
| Schema files | `{contract-name}.schema.json` | Schema names use lowercase kebab-case plus the `.schema.json` suffix. |
| Catalog files | Preserve established source names | Examples: `Offerings_catalog.json`, `Functional_areas_catalog.json`, `setupTasksAll.json`. |
| Project IDs | Folder-safe lowercase names preferred | Persist work under `project/{project_id}`; do not rely on chat history for continuity. |

## Folder Examples

Use lowercase kebab-case for repository folders.

Examples:

- `business-requirements-intake`
- `task-dependency-resolver`
- `order-management`
- `supply-chain-planning`
- `receivables-credit-to-cash`

## Skill Manifests

Every FSCR skill manifest must be named `SKILL.md` and must align to
`schemas/skill-manifest.schema.json`.

Required manifest fields include:

- `skill_id`
- `name`
- `layer`
- `type`
- `execution_mode`
- `owner_team`
- `inputs`
- `outputs`

Layer values are `router`, `core`, `shared`, or `pillar`. Execution modes are
`advisory`, `assisted`, `automated`, and `hybrid`. Skill types are
`orchestration`, `advisory`, `assessment`, `planning`, `export`, `validation`,
`import`, and `verification`.

Router, shared, and pillar skills require enabled `token_usage_tracking` under
the manifest schema. Generated pillar skills use the shared token usage log path:

```text
project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md
```

### Pillar-only generated metadata

Only `layer: "pillar"` manifests may contain `offering`, `functional_area`,
`functional_area_code`, `task_code`, `task_name`, `parent_skill_id`,
`available_flag`,
`export_import_supported_flag`, `csv_export_import_supported_flag`,
`dataloader_import_mode`, `businessObject`, `businessObjects`, and `source_catalog`. Use
`businessObject` for zero or one configured Data Loader REST business object and
`businessObjects` for an ordered list of two or more unique values. Create these fields only through
`core.fusion-dev.pillar-skill-gen`; do not add them to `core`, `shared`, or
`router` manifests.

## Skill IDs

Use dot-separated identifiers. Shared repository layers use their established
layer-specific pattern:

```text
{layer}.{domain}.{skill-name}
```

Examples:

- `router.implementation-router`
- `shared.project-intake.business-requirements-intake`
- `core.fusion-api.rest-api-client`

Pillar IDs depend on the generated skill level:

| Scope | ID Pattern | Example |
| --- | --- | --- |
| Offering-level pillar | `{pillar}.{offering}` | `scm.product-management` |
| Functional-area pillar | `{pillar}.{offering}.{functional-area}` | `scm.product-management.items` |
| Nested setup-task pillar | `{parent_skill_id}.{setup-task-slug}` | `cx.customer-data-management.data-quality-foundation.manage-address-cleansing-configurations` |

Generated pillar IDs use lowercase pillar slugs and slugified catalog names.
Slugification lowercases the source value, replaces non-alphanumeric runs with
hyphens, trims leading and trailing hyphens, and collapses repeated hyphens.

## Artifact Names

Use descriptive lowercase kebab-case file names for reusable templates,
examples, validation outputs, generated reports, and other repository artifacts.

Examples:

- `sample-business-requirements.yaml`
- `setup-task-map.json`
- `validation-results.json`
- `configuration-drift-report.md`

Do not store customer-specific outputs, credentials, tenant secrets, token
caches, private certificates, or production-only sensitive values in reusable
repository artifacts.

## Pillar Skill Generator Naming

`core.fusion-dev.pillar-skill-gen` introduces catalog-backed naming for
functional-area and setup-task skills. It validates pillars, offerings,
functional areas, and setup tasks against `knowledge/setup-task-catalog`
catalogs before generation.

Allowed pillar inputs are `ERP`, `HCM`, `SCM`, `CX`, and `Common`. Output
folders use lowercase pillar slugs such as `erp`, `hcm`, `scm`, `cx`, and
`common`.

Generated functional-area skills are created at:

```text
pillars/{pillar}/{offering}/{functional-area}/SKILL.md
```

For example:

```text
pillars/scm/product-management/items/SKILL.md
```

Generated functional-area skill IDs use:

```text
{pillar}.{offering}.{functional-area}
```

For example:

```text
scm.product-management.items
```

## Setup-Task Naming

When a functional-area skill includes setup tasks, each task is represented in
one of two ways.

| Representation | Path Pattern | Use When |
| --- | --- | --- |
| Flat setup-task metadata | `pillars/{pillar}/{offering}/{functional-area}/{setup-task-slug}.md` | The functional-area skill owns the implementation guidance and the task only needs catalog identity, sequencing, and setup-data routing. |
| Nested setup-task skill | `pillars/{pillar}/{offering}/{functional-area}/{setup-task-slug}/SKILL.md` | The task needs its own workflow, routing, resources, token usage policy, or task-specific guidance boundary. |

Nested setup-task skill IDs append the setup-task slug to the parent
functional-area skill ID:

```text
{parent_skill_id}.{setup-task-slug}
```

A functional-area folder may use a hybrid structure containing both flat
metadata files and nested setup-task skills. The parent `## Setup Tasks` section
must link to the chosen representation:

```text
{setup-task-slug}.md
{setup-task-slug}/SKILL.md
```

The parent manifest stores setup task codes in `required_setup_tasks`.

Do not hand-create nested setup-task skill manifests when
`core.fusion-dev.pillar-skill-gen` can generate the catalog-backed structure.

## Offering-Level Pillar Structure

Offering-level folders and `SKILL.md` files are regenerated from:

```text
knowledge/setup-task-catalog/release/pillars-offerings-mapping.json
```

Use:

```text
core/fusion-dev/catalog-management/scripts/regenerate_pillar_offering_structure.py
```

to regenerate offering-level pillar folders under:

```text
pillars/{common,cx,erp,hcm,scm}/{offering-slug}/SKILL.md
```

Offering-level skill IDs use:

```text
{pillarSlug}.{offeringSlug}
```

Generated manifest input/output variable names may replace hyphens with
underscores, for example `product_management_requirements`.

## Pillar Resource Files

Generated pillar skills can include an `ora-resource/` folder for Oracle
FusionApps guidance files authored by
`core.fusion-dev.fusionapps-resource-authoring`.

Use lowercase snake-case file names with the `ora_` prefix. Place these files
only under the selected generated pillar skill's resource folder:

```text
pillars/{pillar}/{offering}/{functional-area}/ora-resource/ora_*.md
pillars/{pillar}/{offering}/{functional-area}/{setup-task}/ora-resource/ora_*.md
```

Functional-area resources belong under the generated functional-area skill's
`ora-resource/` folder. Task-level resources belong under a nested setup-task
skill's `ora-resource/` folder and require that the nested task `SKILL.md`
already exists.

Do not place generated `ora_*` files directly in the pillar skill root, nested
task root, `core/`, `shared/`, `project/`, another pillar skill, or any sibling
folder outside the selected target skill's `ora-resource/` subfolder.

## Allowed `ora-resource` File Names

`core.fusion-dev.fusionapps-resource-authoring` may create or update only these
files inside the selected generated skill's `ora-resource/` folder:

| File | Purpose |
| --- | --- |
| `ora_input_intake.md` | Accepted input formats, dependency/path/body fields, and body field handling. |
| `ora_input_validation.md` | Required groups, validation rules, and dependency-aware validation. |
| `ora_dependency_readiness.md` | Dependency order, dependency rules, and dependency classification. |
| `ora_reference_lookups.md` | Lookup resolver mechanics, request paths, match rules, and output mappings. |
| `ora_defaulting_rules.md` | Standard defaults and override behavior. |
| `ora_bulk_intake.md` | CSV, table, and bulk row behavior. |
| `ora_rest_execution.md` | Endpoint, path/body contract, preview pattern, and live execution pattern. |
| `ora_design_advisory.md` | Advisory design guidance and source boundaries. |
| `ora_error_handling.md` | Preview/live error diagnosis and stop-before-retry behavior. |
| `ora_design_enforcement.md` | Mandatory design gates, lookup requirements, and preview blockers. |

The lightweight FusionApps resource authoring workflow must not create
`resource.yaml`, `authoring-intake.md`, `resource-authoring-input.md`,
`customer-overrides/`, `tools/`, payload templates, type schemas, or standalone
resource guidance outside a generated pillar skill hierarchy.

Newly generated pillar skills should use this `ora-resource/` model for
source-aligned Oracle guidance.

## Project Artifact Naming

Use `project/{project_id}` as the durable implementation workspace.

Persist durable work under the appropriate project workspace area:

- `project/{project_id}/artifacts`
- `project/{project_id}/exports`
- `project/{project_id}/baselines`
- `project/{project_id}/decisions`
- `project/{project_id}/blueprints`
- `project/{project_id}/state/runs`

Record skill runs under:

```text
project/{project_id}/state/runs/
```

Generated pillar workspace outputs should mirror the pillar hierarchy where
practical. Example:

```text
project/{project_id}/artifacts/pillars/scm/product-management/items/current/
```

Shared token usage records default to:

```text
project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md
```

## Implementation Checklist

- Use lowercase kebab-case for folders and most reusable repository artifact
  file names.
- Use `SKILL.md` for every skill manifest; never introduce lowercase `skill.md`.
- Use dot-separated lowercase skill IDs with hyphenated segments where needed.
- Use `core.fusion-dev.pillar-skill-gen` for catalog-backed functional-area and
  nested setup-task skill creation.
- Use flat setup-task metadata `.md` files only when task-specific behavior does
  not need its own skill boundary.
- Use `core.fusion-dev.fusionapps-resource-authoring` only after the target
  generated pillar skill exists.
- Write only the allowed `ora_*.md` files under `ora-resource/`.
- Update source catalogs or generator scripts when regenerated `knowledge`
  artifacts are the correct path.
- After skill-file refactors, prove there are no lowercase `skill.md` filenames
  or references:

```bash
rg --files | rg '(^|/)skill\.md$'
rg -n 'skill\.md'
```
