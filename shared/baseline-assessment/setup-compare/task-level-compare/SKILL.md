---
skill_id: "shared.baseline-assessment.setup-compare.task-level-compare"
name: "Task Level Compare"
description: "Compares two Oracle Fusion setup ZIP packages for a specific setup task, resolving TaskCode when needed and storing compare reports under the FSCR project workspace."
layer: "shared"
pillar: "Common"
type: "verification"
execution_mode: "hybrid"
owner_team: "Shared implementation enablement team"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "setup_task_identifier"
  - "source_setup_zip_1"
  - "source_setup_zip_2"
  - "execution_options"
outputs:
  - "compare_process_status"
  - "compare_artifacts"
  - "standard_report"
  - "diagnostics"
  - "token_usage_record"
depends_on:
  - "shared.baseline-assessment.setup-compare.fsm-setup-compare"
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
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/shared/baseline-assessment/setup-compare/task/<setup-task-name>/"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Connects to a Fusion environment when approved."
  - "Uploads two local setup ZIP packages to Fusion setup migration process files."
  - "Submits a task-level setup compare process in Fusion."
  - "Writes compare reports and downloaded artifacts to the local project workspace."
required_privileges:
  - "Fusion privileges appropriate to upload setup migration process files and run setup task compare"
---

# Task Level Compare

## Purpose

Compares two FSM setup ZIP packages for one setup task. This wrapper owns
task-specific input validation and then delegates upload, compare submission,
polling, download, report rendering, and token logging to
`shared.baseline-assessment.setup-compare.fsm-setup-compare`.

## REST Flow

1. Authenticate with `core.auth.fusion-oauth-authentication` when login or token
   refresh is needed.
2. Require two readable setup ZIP files, `object-name`, and either `TaskCode` or
   a task name that resolves to exactly one `TaskCode`.
3. Create both setup package uploads through the shared compare engine.
4. Submit a task-level compare request with `TaskCode`.
5. Poll for terminal status, download compare artifacts, and write the standard
   report plus sanitized process output.

## Project Scripts

Run from the repository root:

```bash
python3 shared/baseline-assessment/setup-compare/task-level-compare/scripts/compare_setup_task_zips.py \
  --zip1 /path/source1.zip \
  --zip2 /path/source2.zip \
  --object-name "Manage Lot Grades" \
  --task-code INV_MANAGE_LOT_GRADES \
  --token-cache auto
```

The script derives the FSCR project workspace from the `environment` value in
`core/auth/fusionEnv.properties`; pass `--project-id` when the project
workspace cannot be resolved from `FDOS_PROJECT_ID`, the existing initialized
workspace, or the Fusion `environment` fallback.
Default outputs are written under:

```text
project/{project_id}/artifacts/shared/baseline-assessment/setup-compare/task/<setup-task-name>/
```

Use `--source-cfg-created-by-flow TASK` or `TASK_CSV` only when the package
origin is known. Otherwise let Fusion validate the package without a source-flow
hint.

## Inputs

- `fusion_environment_context`: usable `core/auth/fusionEnv.properties`.
- `setup_task_identifier`: task name or `TaskCode`.
- `source_setup_zip_1` and `source_setup_zip_2`: local FSM setup ZIP packages.
- `execution_options`: token cache, polling interval, timeout, output
  directory, optional source-flow hint, diagnostics, and browser/login controls.

## Outputs

- `compare_process_status`
- `compare_artifacts`
- `standard_report`
- `diagnostics`
- `token_usage_record`

## Implementation Notes

Do not duplicate setup compare REST mechanics in this skill. Keep task-specific
validation here and call `shared.baseline-assessment.setup-compare.fsm-setup-compare` for upload,
compare submission, polling, artifact download, report rendering, and token
usage logging.

Keep the Python entrypoint aligned with setup-export drivers: local repository
bootstrap, `fusion_auth` token handling, `utc_now`, `parse_args`, `get_token`,
`resolve_scope_feature_code`, `resolve_project_id`, `run_compare`, and `main`.
Do not add an `agents/openai.yaml`, a local setup-compare `fusion_skill_paths.py`,
or custom project path handling beyond the shared `--project-id` input.

For a completed compare, lead with the task name/code, compare process ID, and
final status, then link `*_standard_report.md` and the downloaded
`COMPARISON_DIAGNOSTICS_PACKAGE_ZIP` when available before rendering the report's
**Process Details** and **Results** tables in the response. The process table
must show `Step`, `Process ID`, `Status`, and `Name`; the results table must
show `Business object`, `Source 1 count`, `Source 2 count`, `Mismatch count`,
`Match count`, and `Total count`. Use the generated standard report or
`COMPARISON_RESULTS_XML` as the source of those values, state the reported
warnings/errors, and say when a value is unavailable. Finish with links to the
sanitized process-output JSON and downloaded artifacts; do not paste binary
report data, raw XML, ZIP content, tokens, credentials, or headers.
