---
skill_id: "core.data-loader.task-hook"
name: "Data Loader Task Hook"
description: "Dispatch task-level validation for Data Loader."
layer: "core"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Central platform team"
inputs:
  - "task_context"
  - "requested_route"
  - "rule_results"
outputs:
  - "route_plan"
  - "validation_result"
uses_core:
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
state_updates:
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/core/data-loader/task-hook/runs/{run_id}/"
    versioning_policy: "append-only"
side_effects:
  - "Reads the supplied task context, task-rule results, and local Data Loader validation artifacts."
  - "Creates or verifies local preview and approval-envelope artifacts for a task-routed Data Loader upload."
  - "Persists and registers the final validation result and records the Task Hook run in the active project workspace."
required_privileges: []
---

# Data Loader Task Hook

## Purpose

Dispatch the selected task's Data Loader validation and preview lifecycle while
preserving the supplied task identity, rule order, approval envelope, and final
archive digest.

## Preflight

Before any command, require the supplied task context and an exact supported
route. For `data-load`, validate the selected task name and positive sequence;
before building a preview, require the expected ordered rule results and archive
SHA-256. Validate the preview when recording approval, and require its matching
approval envelope before verifying the final archive. Fail closed on missing,
ambiguous, inconsistent, or unrecognized inputs without selecting another task,
route, or execution mechanism.

- **Data Loader preflight:**
  - Confirm the persisted preflight before invoking `data-load`.
  - Require `taskRouted: true`, `mappingComplete: true`, and a SHA-256 matching
    the final artifact.
  - Stop before Task Validation when the preflight is missing or invalid.
  - Keep preflight parsing and verification in Data Loader.
  - Do not import Data Loader implementation code into Task Hook.

## Redaction

Never include credentials, access tokens, or archive contents in Task Hook
output or diagnostics. Preserve the existing user-visible preview fields and
return only the validation, approval, and digest evidence defined by the
selected command.

Use this as the single task-level dispatcher after the workflow has supplied
the selected task context. Do not modify or
reinterpret that task context.

- `data-load`: required Ora Resource Task Validation using
  `../task-validator/scripts/task_validator.py` and
  `../references/task-rule-registry-execution.md`. Use this Task Hook's
  `build-data-load-preview`, `approve-data-load-preview`, and
  `verify-approved-data-load-archive` commands for the preview lifecycle;
  callers must not invoke Task Validator commands directly. Continue only with
  an approved envelope that matches the final upload artifact SHA-256.

Never scan arbitrary Skills, reselect a task, or call Run Book REST APIs.

## Data Loader Preview Lifecycle

Handle `data-load`'s returned `taskValidation.taskValidationStatus` before continuing:

- `ready`: the rule plan is executable. The caller must immediately read the
  returned `executionGuide` and rule files and execute applicable nodes using
  the registry prerequisites and transitions. Declared read-only Fusion GETs
  through the shared REST client are part of this selected workflow. Record
  evidence and ordered `ruleResults`. This assisted execution step does not
  require a separate evaluator command; its absence is not a workflow gap.
- `overridden`: require the existing explicit user waiver, preserve its reason
  and original failure evidence, require literal
  `allowReadinessOverride: true`, and execute remaining applicable rules.
- `skipped`: record unavailable task guidance or rule registry as
  `not_applicable` and continue without requesting a user override.
- Resolver errors or missing/unrecognized statuses: stop with the actual error
  or status. Do not substitute a different route.

`ready` is registry readiness, not completed validation. Follow the returned
`nextAction`; only evaluated results may be supplied to preview creation.

After `data-load` resolves the task plan and the non-write rules have been
evaluated, call `build-data-load-preview --input-stdin` with JSON containing
`taskContextPath`, `taskName`, `sequence`, `finalData`, and
ordered `ruleResults`. `finalData.archiveSha256` is required. Rule exceptions
remain visible as `status: overridden` with their user waiver and reason.

Only after explicit user approval, call `approve-data-load-preview --input-stdin`
with the preview. Then call `verify-approved-data-load-archive --input-stdin
--archive <final-zip>` with the preview and approval. Its
`taskValidationEnvelope` is the exact JSON object to persist and pass to
`core.data-loader` as `--task-validation-envelope`.

Never manually create, reconstruct, or modify Task Hook preview, approval, or
`taskValidationEnvelope` outputs, including approval flags, archive digests, or
Run Book bindings. Obtain these outputs only through the prescribed Task Hook
preview, approval, and archive-verification commands, and persist and pass the
returned `taskValidationEnvelope` unchanged. If it is missing, invalid, or no
longer matches the artifact, stop submission and repeat the required Task Hook
validation and approval steps. Never substitute direct Task Validator calls.

## Project Evidence

- Persist only the successful `verify-approved-data-load-archive` output as
  `artifacts/core/data-loader/task-hook/runs/{run_id}/validation-result.json`.
- Register the validation result using
  `core.project-mgmt.artifact-registry-manager`.
- Record one `core.data-loader.task-hook` skill run for the complete Task Hook
  lifecycle using `core.project-mgmt.project-state-manager`; do not create one
  run record per Task Hook command.
- Append one token-usage entry for that lifecycle using
  `core/project-mgmt/scripts/token_usage_logger.py`.
- On failure, record the failed skill run and token usage; do not create a
  successful validation-result artifact.
