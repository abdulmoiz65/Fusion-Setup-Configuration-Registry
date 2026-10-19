# Error Handling Guidelines

## Purpose

These guidelines make FSCR error handling consistent across core automation,
shared implementation skills, generated pillar skills, validation flows, import
and export workflows, catalog generators, and project artifact persistence.

Use this file with:

- `governance/skill-design-standards.md`
- `governance/review-checklists.md`
- `governance/contribution-guidelines.md`
- `schemas/skill-run.schema.json`
- `schemas/validation-result.schema.json`

## Failure Taxonomy

| Class | Typical Trigger | Required Handling |
| --- | --- | --- |
| `input_validation` | Required input missing, malformed JSON or body, invalid ZIP, invalid argument combination | Fail before side effects and show the exact missing or invalid field. |
| `catalog_or_metadata_mismatch` | No confident catalog match, duplicate representation, unsupported CSV flag | Stop and provide close matches, supported alternatives, or a follow-up issue. |
| `auth_expired_or_invalid` | Cached token rejected by Fusion with 401 or 403 | Refresh once if cache-managed; otherwise ask the user or caller to re-authenticate. |
| `authorization_or_privilege` | 403 after refresh or missing Fusion role | Stop and recommend role, privilege, or environment-access diagnostics. |
| `transport_or_environment` | DNS, VPN, timeout, connection closure, unavailable service | Stop or retry only read-only calls with bounded attempts; record environment identity. |
| `fusion_api_error` | HTTP 4xx or 5xx with response body | Capture status, endpoint path, response body summary, ECID if present, and recommended action. |
| `process_timeout` | Long-running job did not complete in `wait_seconds` | Persist last status and ask before retrying the ProcessId or requestId. |
| `process_failed` | Terminal completed-errors or failed job | Retrieve ProcessLog or status payload when available and return failure status. |
| `artifact_persistence` | Cannot write output, invalid project path, schema invalid | Do not lose raw diagnostics; write to a safe temp location if needed and explain. |
| `approval_blocker` | Overwrite, destructive deletion, live execution, unsupported retry | Stop until explicit user approval is available. |

## Baseline Rules

1. Classify every durable failure with one of the failure taxonomy classes.
2. Run preflight checks before Fusion-changing actions.
3. Use preview, dry-run, or plan-first behavior for generated artifacts and live
   Fusion changes whenever the tool supports it.
4. Retry only when the failure is known to be transient or recoverable.
5. Fail closed on ambiguous catalog matches, destructive operations, overwrite
   conflicts, unsupported CSV flags, missing source guidance, or target paths
   outside the requested workspace.
6. Preserve partial progress when it is useful and safe, but return a distinct
   nonzero status for partial failure.
7. Persist durable diagnostics under `project/{project_id}` when a skill
   produces project output or when the diagnostics are needed by later stages.
8. Never print or persist credentials, tokens, token caches, private keys,
   tenant secrets, wallet files, full base64 payloads, or sensitive customer
   details.
9. Before handoff, report which validation, dry-run, structural, render, or
   execution checks were run and which were skipped.

## Preflight Checks

Before a side-effecting action, validate:

1. Environment identity and intended target.
2. Required roles, privileges, OAuth scopes, and session state.
3. Required input values and mutually exclusive arguments.
4. Catalog support flags, task codes, setup object names, and close matches.
5. Payload shape, JSON validity, ZIP signature, file existence, and file type.
6. Destination paths under the allowed project or skill workspace.
7. Whether the operation is preview, dry-run, or live.
8. Whether overwrite, deletion, force, retry, or live execution requires user
   approval.

## Retry Policy

1. Cached-token 401 or 403 responses may trigger one token-refresh retry.
2. Explicit access tokens should not be silently replaced.
3. Read-only transport failures may be retried with bounded attempts and clear
   wait or backoff.
4. Live POST, PATCH, DELETE, import, loader, or ESS operations must not be
   retried without an idempotency key or explicit user approval.
5. Do not retry when the failure is caused by invalid input, unsupported catalog
   metadata, missing privileges, overwrite conflicts, destructive operations, or
   missing approval.

## Timeout and Polling Policy

Long-running operations should define `wait_seconds` and polling interval.

On timeout:

1. Stop polling.
2. Report environment, operation, TaskCode or jobDefinitionId, ProcessId or
   requestId, last status, elapsed wait, and next-check guidance.
3. Persist last known status and diagnostic payload when project context exists.
4. Ask before retrying the same process or submitting a new live operation.
5. Do not continue polling indefinitely.

## Process Failure Handling

For failed Fusion jobs, setup exports/imports, ESS submissions, and loaders:

1. Retrieve ProcessLog, status payload, request diagnostics, or Fusion error body
   when available.
2. Preserve external identifiers such as ProcessId, requestId, ECID, or job
   definition name.
3. Summarize the failure without hiding the original Fusion diagnostic.
4. Persist diagnostics under the project workspace when durable output is
   relevant.
5. Return or record a failed status instead of presenting partial output as a
   successful run.

## Diagnostic Outputs

Durable diagnostics should include:

1. `status`
2. `stage`
3. `failure_class`
4. `message`
5. `recommended_action`
6. `environment`
7. `skill_id`
8. `artifact_refs`
9. External job or API identifiers such as ProcessId, requestId, ECID, endpoint
   path, or jobDefinitionId.
10. Validation, preview, dry-run, or execution checks that were run.

When partial progress is useful, include an `errors` array with:

1. `stage`
2. `entity_id`
3. `message`
4. `failure_class`
5. `recommended_action`

## Exit Code Guidance

Automated and hybrid scripts should document their exit codes. Use this baseline
unless a local tool already has a stricter contract:

| Code | Meaning |
| --- | --- |
| `0` | Success. |
| `1` | Unhandled error or validation failure before side effects. |
| `2` | Unsupported operation, catalog limitation, or partial failure. |
| `3` | Timeout, incomplete polling, or operation still running. |
| `4` | Terminal process failure or completed-with-errors state. |

## Skill Manifest Guidance

Automated, hybrid, validation, import, export, and generator skills should
declare error-handling behavior in manifest metadata or in explicit `SKILL.md`
sections.

Recommended fields or sections:

```yaml
error_handling:
  failure_modes:
    - "input_validation"
    - "authorization_or_privilege"
    - "fusion_api_error"
    - "process_timeout"
  retry_policy:
    cached_token_401_403: "refresh once unless access token was provided explicitly"
    live_mutation_retry: "requires explicit user approval or idempotency key"
  timeout_policy:
    wait_seconds: 300
    on_timeout: "persist last status and ask before retrying ProcessId"
  diagnostic_outputs:
    - "execution_result"
    - "diagnostics"
    - "audit_summary"
  redaction_rules:
    - "never print or persist tokens, secrets, token caches, or full base64 payloads"
```

If schema evolution is not available, include equivalent Markdown sections in
the skill body.

## Pillar Skill Guidance

Generated pillar skills should:

1. Include task CSV support behavior and route unsupported CSV tasks to
   validation or advisory guidance instead of export/import.
2. Load task-local `ora_error_handling.md` before preview or live execution when
   the file exists.
3. Generate or update `ora_error_handling.md` when endpoint execution,
   preview/live retries, or task-specific error diagnosis is in scope.
4. Use `Error Situations`, `Error Classifications`, `Disclosure Rules`, and
   `Refusal Rules` sections in task-local error guidance where useful.
5. Mark unknown Oracle behavior as `TBD`, clarify with source material, or raise
   a gap rather than inventing product behavior.

## Review Checklist

Reviewers should confirm:

1. Failure classes are explicit.
2. Preflight checks prevent side effects on invalid input.
3. Retry behavior is bounded and does not repeat live mutations without
   approval.
4. Timeout behavior stops polling and reports the required identifiers.
5. Failed Fusion jobs retrieve process logs or status payloads when available.
6. Durable diagnostics are persisted in the project workspace when needed.
7. Partial failures preserve successful outputs and list failed units.
8. Sensitive values are redacted.
9. Approval blockers stop execution until user approval is available.
