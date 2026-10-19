---
skill_id: "shared.baseline-assessment.setup-compare.export-and-compare"
name: "Export and Compare"
description: "Exports Oracle Fusion setup data from one or two environments when needed, then compares two setup ZIP packages at offering, functional-area, or setup-task level."
layer: "shared"
pillar: "Common"
type: "verification"
execution_mode: "hybrid"
owner_team: "Shared implementation enablement team"
version: "0.1.0"
inputs:
  - "compare_level"
  - "entity_identifiers"
  - "source_inputs"
  - "compare_environment_context"
  - "execution_options"
outputs:
  - "source_export_packages"
  - "source_export_process_statuses"
  - "compare_process_status"
  - "compare_artifacts"
  - "standard_report"
  - "diagnostics"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.setup-export.functional-area-export"
  - "shared.setup-export.offering-export"
  - "shared.baseline-assessment.setup-compare.task-level-compare"
  - "shared.baseline-assessment.setup-compare.functional-area-compare"
  - "shared.baseline-assessment.setup-compare.offering-compare"
  - "core.auth.fusion-oauth-authentication"
uses_core:
  - "core.auth.fusion-oauth-authentication"
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
persists_project_state: true
state_updates:
  - "exports"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_export"
    default_location: "project/{project_id}/exports/baseline-assessment/setup-compare/export-and-compare/{source-environment}/{compare-level}/{entity-name}/"
    versioning_policy: "append-only"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/shared/baseline-assessment/setup-compare/export-and-compare/{compare-level}/{entity-name}/"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Connects to each approved source Fusion environment and creates setup export processes when a source ZIP is not supplied."
  - "Connects to the approved compare Fusion environment, uploads two setup ZIP packages, and submits a setup compare process."
  - "Writes export packages, process status, diagnostics, reports, and downloaded compare artifacts to the selected project workspace."
required_privileges:
  - "Fusion privileges appropriate to create and retrieve FSM CSV export packages in each source environment."
  - "Fusion privileges appropriate to upload setup migration process files and run setup compare in the compare environment."
---

# Export and Compare

## Purpose

Compare setup data at exactly one level: `offering`, `functional-area`, or
`setup-task`. The input may be two local ZIP packages, one ZIP plus one source
environment, or two source environments. Reuse the existing hierarchy-specific
export and compare skills; this skill only coordinates the end-to-end flow.

## Required Intake

Collect the compare level and exact entity identity before any external action:

- `offering`: offering name or OfferingCode.
- `functional-area`: offering plus functional-area name or codes.
- `setup-task`: task name or TaskCode; collect offering and functional area when
  available to resolve an ambiguous task name.

Identify one source mode:

1. **Two ZIPs**: require two readable local FSM setup ZIP packages.
2. **ZIP plus environment**: require one readable ZIP and one source environment
   from which to create the other package.
3. **Two environments**: require separate source environment contexts for both
   packages.

Always ask where the compare is to run. The compare target may be the default
environment in `core/auth/fusionEnv.properties`, a supplied environment, or a
distinct environment from both sources. Confirm its environment identity before
submitting the compare process.

## Environment Context and Secrets

For an environment used as an export source or compare target, request only the
properties required by `core.auth.fusion-oauth-authentication`: `environment`,
`restBaseUrl`, `clientId`, `clientSecret` when confidential OAuth is used,
`scope`, `redirectUrl`, `tokenUrl`, and `authorizeUrl`. Preserve optional
service scopes when supplied. Never echo these values in a report, diagnostic,
command output, example, or project artifact.

When an environment context is absent, read only the environment label and URL
needed to identify the default from `core/auth/fusionEnv.properties`, then ask:

> May I export from the default configured environment `<environment>`?

Do not use that environment for export unless the user explicitly confirms. If
they decline, request a source environment context. Do not request a real
credential template in chat when the user can provide a secure local properties
file path instead.

Never modify `core/auth/fusionEnv.properties` to switch environments. Create a
restricted, gitignored, per-run properties file outside `project/` for every
supplied environment and pass it with `--properties`. Use a distinct gitignored
token-cache path per environment. Delete temporary configuration only when the
user asks; do not persist credentials, token caches, or secrets under `project/`.

## Route the Work

Use the matching export wrapper for each required source package:

| Compare level | Export skill | Compare skill |
| --- | --- | --- |
| `offering` | `shared.setup-export.offering-export` | `shared.baseline-assessment.setup-compare.offering-compare` |
| `functional-area` | `shared.setup-export.functional-area-export` | `shared.baseline-assessment.setup-compare.functional-area-compare` |
| `setup-task` | `shared.setup-export.task-level-export` | `shared.baseline-assessment.setup-compare.task-level-compare` |

Pass the same resolved level-specific codes/names to both export sources and the
compare wrapper. Run two independent source exports sequentially unless the
user explicitly authorizes parallel interaction with the source environments.
Preserve each resulting ZIP under the source-specific project exports path;
never overwrite a prior package.

## Execution Gates

1. Preflight all ZIP paths, exact scope identity, CSV support for setup tasks,
   project path, source environments, compare target, and required privileges.
2. Present the resolved plan: source environment(s), compare target, level,
   entity identifiers, and whether export and compare processes will be
   created. Do not include secrets.
3. Obtain explicit approval immediately before each external operation group:
   source export process creation and compare package upload/compare submission.
   Approval to export does not authorize a later compare submission.
4. Authenticate through `core.auth.fusion-oauth-authentication`, then pass the
   per-environment properties and token-cache paths to the selected wrapper.
5. Allow each export wrapper to create, poll, download, and persist the ZIP.
   Do not recreate a submitted export process on timeout.
6. After two valid ZIPs exist, invoke the selected compare wrapper against the
   approved compare environment. Allow it to upload, submit, poll, download the
   comparison artifacts, and produce its standard report.

## Polling, Results, and Failure Handling

Use the delegated wrappers' polling intervals and bounded timeout. For every
export and compare process, persist the sanitized status, ProcessId, environment
label, elapsed time, and artifact paths.

On a timeout, stop polling and return the environment, operation, ProcessId,
last status, elapsed wait, and the manual check path. Tell the user they can
ask this skill to check that ProcessId later; do not submit a replacement
process or continue indefinitely.

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_expired_or_invalid`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `approval_blocker`. Refresh a
cache-managed token once after a 401/403. Do not retry export creation, package
upload, or compare submission without explicit approval. Retrieve a process log
or sanitized status payload for terminal failures.

On successful completion, return the source ZIP paths, source export ProcessIds,
compare ProcessId and final status. Link the standard comparison report and the
downloaded `COMPARISON_DIAGNOSTICS_PACKAGE_ZIP` when available, then render its
**Process Details** table (`Step`, `Process ID`, `Status`, `Name`) and **Results**
table (`Business object`, `Source 1 count`, `Source 2 count`, `Mismatch count`,
`Match count`, `Total count`) directly in the user response.
Use only values present in the standard report or comparison-results XML; do
not infer mismatches from source counts. State the reported warnings/errors,
then link the sanitized process output and downloaded compare artifacts,
including any unavailable optional artifact. Do not attach or print raw ZIP
data, tokens, credentials, authorization headers, properties file contents,
raw XML, or binary report content.
