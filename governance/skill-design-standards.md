# Skill Design Standards

## Skill Types

Supported skill types:

- `orchestration`
- `advisory`
- `assessment`
- `planning`
- `export`
- `validation`
- `import`
- `verification`

## Execution Modes

| Mode | Use When |
| --- | --- |
| `advisory` | The skill provides documented guidance and the implementor performs the action offline. |
| `assisted` | The skill generates artifacts or recommendations that require human review. |
| `automated` | The skill performs approved actions directly through APIs, jobs, or loaders. |
| `hybrid` | The skill combines automated analysis with human approval or execution. |

## Design Rules

1. Keep skills focused on one implementation responsibility.
2. Align each manifest with `schemas/skill-manifest.schema.json`.
3. Name each manifest `SKILL.md`; do not create lowercase `skill.md` files.
4. Keep folders lowercase kebab-case and skill IDs dot-separated.
5. Declare every upstream input and downstream output.
6. Declare dependencies on other skills, catalogs, schemas, or core services.
7. Avoid hardcoded sequencing when manifest dependencies can express the
   relationship.
8. Use core services for Fusion authentication, API access, ESS, export, import,
   FBDI, HDL, diagnostics, and project-state management.
9. Keep pillar-specific rules out of `shared` unless they apply across pillars.
10. Produce machine-readable outputs for planning, validation, import,
    verification, generation, and automation skills.
11. Document side effects, required privileges, and approval gates for automated
    and hybrid skills.
12. Use synthetic data for examples, payloads, screenshots, validation fixtures,
    and golden scenarios.
13. Do not store credentials, secrets, tokens, private keys, tenant secrets, or
    real customer data in skills, examples, diagnostics, or project artifacts.

## Manifest Expectations

Skill manifests should declare:

1. Purpose and scope.
2. Inputs, outputs, and workspace persistence behavior.
3. Dependencies and related skills.
4. Owner team and reviewer group.
5. Execution mode and required privileges.
6. Applicability by pillar, offering, functional area, country, industry, or
   Fusion release when relevant.
7. Side effects and approval gates.
8. Expected validation, preview, dry-run, or live-execution behavior.
9. Error-handling and diagnostic behavior for automated, hybrid, validation,
   import, export, and generation skills.

## Error Handling and Diagnostics

Automated, hybrid, validation, import, export, and generation skills must follow
`governance/error-handling-guidelines.md`.

At minimum, the skill should define:

1. `failure_modes`: expected failure classes and whether each is recoverable.
2. `preflight_checks`: checks required before side effects.
3. `retry_policy`: retryable failures, maximum attempts, backoff, and operations
   that must not be retried without approval.
4. `timeout_policy`: polling window, interval, timeout output, and next-check
   guidance.
5. `diagnostic_outputs`: execution results, audit summaries, diagnostics,
   external IDs, process IDs, request IDs, ECIDs, and artifact paths.
6. `rollback_or_recovery`: compensation, resume, retry, or manual recovery
   behavior.
7. `error_redaction`: fields never printed or persisted.
8. `approval_gates`: live execution, overwrite, deletion, force, retry, and
   other user-approval blockers.

Live Fusion mutations should be preceded by preview, dry-run, plan-first, or
explicit approval behavior whenever the tool supports it. Live POST, PATCH,
DELETE, import, loader, or ESS operations should not be retried unless an
idempotency key or explicit user approval is available.

## Project Workspace Persistence

Skills must treat the `project` folder as the durable implementation workspace.
Any skill that produces output needed by later sessions or downstream skills
must:

1. Write or update a project artifact under `project/{project_id}/artifacts`,
   `project/{project_id}/exports`, `project/{project_id}/baselines`,
   `project/{project_id}/decisions`, or `project/{project_id}/blueprints`.
2. Register the artifact using the project artifact schema.
3. Update project state when the output changes objective, requirements, scope,
   task sequence, decisions, blueprints, exports, baselines, validations, or
   reports.
4. Record a skill run under `project/{project_id}/state/runs`.
5. Use new versions for major changes and require user confirmation before
   updating an existing artifact for minor changes.
6. Persist failed, timed-out, or partially completed durable runs with
   diagnostic metadata when `project_id` is supplied.

Project-intake, scope-definition, implementation-planning, baseline-assessment,
shared, and pillar skills should consume prior project artifacts before asking
the user to restate known information.

## Pillar Skill Design

Pillar skills should follow the catalog hierarchy and generated naming model.

1. Use `core/fusion-dev/pillar-skill-gen/scripts/pillar_skill_gen.py` for
   catalog-backed functional-area and nested setup-task skill creation.
2. Use generated offering, functional-area, setup-task, folder, and skill-ID
   names unless the source catalog is corrected and regeneration is appropriate.
3. Attach domain guidance with
   `core.fusion-dev.fusionapps-resource-authoring`.
4. Keep task-specific guidance near the resolved setup-task skill.
5. Put cross-cutting pillar guidance for integrations, extensibility, data
   conversion, and reporting in the pillar common folder instead of duplicating
   it across offerings or functional areas.
6. Reference shared/common skills for shared setup objects instead of copying
   logic into multiple pillars.

## Pillar Resource Files

Generated pillar skills can be augmented with Oracle FusionApps guidance files
under an `ora-resource/` folder. These files are generated or updated by
`core.fusion-dev.fusionapps-resource-authoring` after the pillar skill has been
created by `core.fusion-dev.pillar-skill-gen`.

Use this pattern for functional-area resources:

```text
SKILL.md
ora-resource/
  ora_input_intake.md
  ora_input_validation.md
  ora_dependency_readiness.md
  ora_reference_lookups.md
  ora_defaulting_rules.md
  ora_bulk_intake.md
  ora_rest_execution.md
  ora_design_advisory.md
  ora_error_handling.md
  ora_design_enforcement.md
```

Use the same `ora-resource/ora_*.md` pattern inside a generated nested
setup-task skill when task-specific guidance needs its own skill boundary.

Newly generated pillar skills should use the `ora-resource/` model for
source-aligned Oracle guidance.

When endpoint execution, preview/live retries, or task-specific diagnosis is in
scope, include `ora_error_handling.md` and load it before preview or live
execution. Unknown Oracle behavior should be marked `TBD`, clarified, or handled
as an explicit gap instead of invented.
