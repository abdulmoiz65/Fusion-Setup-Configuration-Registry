---
skill_id: "shared.baseline-assessment.setup-compare.fsm-setup-compare"
name: "FSM Setup Compare"
description: "Shared implementation engine for comparing two Oracle Fusion FSM setup ZIP packages through setupMigrationProcesses using FSCR OAuth token-cache authentication."
layer: "shared"
pillar: "Common"
type: "verification"
execution_mode: "hybrid"
owner_team: "Shared implementation enablement team"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "compare_scope"
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
    default_location: "project/{project_id}/artifacts/shared/baseline-assessment/setup-compare/{entity_type}/{object_name}/"
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
  - "Creates setup compare upload processes and submits a compare process in Fusion."
  - "Writes compare reports, downloaded artifacts, and sanitized process output to the local project workspace."
required_privileges:
  - "Fusion privileges appropriate to upload setup migration process files and run setup compare"
---

# FSM Setup Compare

Use this shared engine for the low-level Oracle Fusion setup ZIP compare
workflow. Prefer the entity-specific user-facing skills for normal work:

- `shared.baseline-assessment.setup-compare.task-level-compare`
- `shared.baseline-assessment.setup-compare.offering-compare`
- `shared.baseline-assessment.setup-compare.functional-area-compare`

## Engine Boundary

This engine owns the REST mechanics for setup compare:

1. Validate the two local ZIP files.
2. Normalize the Fusion environment URL to a `fscmRestApi/resources` root.
3. Resolve setup object codes by read-only lookup when requested.
4. Create two setup migration file blobs.
5. Upload both ZIP files.
6. Create upload processes for both sources.
7. Retrieve the compare request name.
8. Submit the compare process.
9. Poll for terminal status.
10. Download compare artifacts and write a standard report.

Entity skills own object-specific input rules and defaults. They must call this
engine instead of duplicating compare upload, polling, download, or report
rendering logic.

## Project Assumptions

- Run from the repository root.
- Use `core/auth/fusion-oauth-authentication` for login, authentication,
  and access token refresh.
- Prefer file token cache `.fusionaim_token.json` because macOS Keychain may be
  unreadable from the shell.
- Use this skill's scripts:
  - `shared/baseline-assessment/setup-compare/fsm-setup-compare/scripts/fsm_setup_compare.py`
  - `shared/baseline-assessment/setup-compare/fsm-setup-compare/scripts/fsm_setup_compare_engine.py`
- Use `--project-id` for explicit workspace selection when provided. Otherwise
  use `FDOS_PROJECT_ID`, then the only initialized `project/{project_id}`
  workspace, with the Fusion `environment` value as a compatibility fallback.
- Entity-specific wrappers call this engine directly and pass their own
  `skill_id` for token usage logging. Do not route wrapper scripts by mutating
  `sys.argv`.
- Store outputs under:

```text
project/{project_id}/artifacts/shared/baseline-assessment/setup-compare/<entity-type>/<object-name>/
```

- Do not print access tokens, refresh tokens, client secrets,
  `.fusionaim_token.json` contents, Authorization headers, or raw binary ZIP
  content.
- Network access to Fusion REST normally requires command approval/escalation.

## Authentication

Authenticate with Fusion using `core.auth.fusion-oauth-authentication` when login
or token refresh is needed. After authentication, use the shared managed external token
cache to compare scripts:

```bash
python3 core/auth/fusion-oauth-authentication/scripts/fusion_login.py \
  --token-cache auto
```

## Raw Compare

Use the raw engine only when the caller already knows the entity type and code
shape:

```bash
python3 shared/baseline-assessment/setup-compare/fsm-setup-compare/scripts/fsm_setup_compare.py \
  --zip1 /path/source1.zip \
  --zip2 /path/source2.zip \
  --object-name "Manage Lot Grades" \
  --entity-type TASK \
  --task-code INV_MANAGE_LOT_GRADES \
  --token-cache auto
```

## Compare Artifacts

The engine attempts to download these default artifacts after completion:

- `COMPARISON_RESULTS_XML`
- `COMPARISON_REPORT`
- `COMPARISON_RESULTS_REPORT`
- `COMPARISON_PROCESS_SUMMARY_REPORT`
- `COMPARISON_PROCESS_STATUS_DETAILS`

Use `--include-diagnostics` to also request
`COMPARISON_DIAGNOSTICS_PACKAGE_ZIP`.

## Final Response

For completed compare runs, present the outcome in a user-readable format,
not merely as artifact paths:

1. Lead with the entity type, object name, resolved code fields, compare
   process ID, and final status.
2. Link the generated `*_standard_report.md` as the primary report and, when
   downloaded, the `COMPARISON_DIAGNOSTICS_PACKAGE_ZIP` diagnostic package.
3. Render its **Process Details** as a compact Markdown table with `Step`,
   `Process ID`, `Status`, and `Name`. Include each source-upload process and
   the submitted compare process when those fields are available.
4. Render its **Results** as a compact Markdown table with `Business object`,
   `Source 1 count`, `Source 2 count`, `Mismatch count`, `Match count`, and
   `Total count`. Read the values from the standard report or the downloaded
   `COMPARISON_RESULTS_XML`; do not infer mismatches from source counts.
5. State whether the report lists warnings or errors. If a table or field is
   unavailable, say so plainly rather than fabricating a value.
6. Then link the sanitized process-output JSON and the downloaded comparison
   artifacts. Do not paste raw XML, binary report content, ZIP data, tokens,
   credentials, or authorization headers.

Use this response shape:

```markdown
Compare completed: `<object name>` (`<code>`) — `<final status>`

[Open the standard report](<standard-report-path>)

[Download diagnostics package](<comparison-diagnostics-package-zip-path>)

### Process details

| Step | Process ID | Status | Name |
| --- | --- | --- | --- |
| ... |

### Results

| Business object | Source 1 | Source 2 | Mismatches | Matches | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| ... |

Warnings/errors: `<none or summarized report value>`.
```
