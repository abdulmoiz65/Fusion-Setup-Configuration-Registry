---
skill_id: "core.fusion-api.ess-job-submitter"
name: "ESS Job Submitter"
description: "Provides the ess job submitter core capability for Oracle Fusion Cloud implementation workflows."
layer: "core"
pillar: "Core"
type: "import"
execution_mode: "automated"
owner_team: "Central platform team"
version: "0.1.1"
inputs: 
  - "ess_delegation_contract"
outputs: 
  - "execution_result"
  - "diagnostics"
  - "audit_summary"
depends_on:
  - "core.auth.fusion-oauth-authentication"
  - "schemas/ess-delegation-contract.schema.json"
uses_core:
  - "core.auth.fusion-oauth-authentication"
applicability:
  industries: 
    - "All"
  countries: 
    - "All"
  fusion_releases: 
    - "Current Oracle Fusion Cloud release"
side_effects: 
  - "Connects to Fusion ESS REST APIs when invoked."
  - "Submits ESS job requests when invoked without an existing requestId."
  - "May refresh the OAuth token cache when the cached token is unavailable or rejected."
required_privileges: 
  - "Fusion privileges appropriate to the requested operation"
---

# ESS Job Submitter

## Purpose

Provides the ESS job submitter core capability for Oracle Fusion Cloud
implementation workflows.

## Canonical ESS Delegation Contract

Accept only a validated `approved_submission` conforming to
`schemas/ess-delegation-contract.schema.json` version `1.0`. Require the
approved immutable `request_payload`, job contract, target environment,
polling options, and approval hash. This core skill does not classify FSM tasks,
choose business defaults, construct a payload, or obtain approval; it submits
and tracks the exact approved payload.

## When to Use

Use this core skill when another router, shared, or pillar skill needs to run an
Oracle Fusion ESS scheduled process and track its result. Any implementation
activity that submits, monitors, or resumes tracking an ESS job should call this
skill instead of duplicating REST authentication, request submission, or polling
logic.

## REST API Contract

This skill uses the Oracle Fusion Scheduler REST API:

- Submit: `POST /ess/rest/scheduler/v1/requests`
- Track: `GET /ess/rest/scheduler/v1/requests/{requestId}`

The submit response returns an ESS request identifier as `id`; the tracking call
uses that value as `requestId`. The payload supports the Oracle request fields
such as `jobDefinitionId`, `requestParameters`, `application`, `description`,
`priority`, `retries`, `requestTimeout`, `schedule`, `scheduleId`, `startTime`,
and `endTime`.

Do not use `callbackSubscription` for now. The implementation rejects payloads
that include it so all callers use the async submit-and-poll flow consistently.

## Project Scripts

Run from the repository root:

```bash
python3 core/fusion-api/ess-job-submitter/scripts/ess_job_submitter.py \
  --job-definition-id oracle/apps/ess/somePackage/someJob \
  --application someApplication \
  --parameter Param1=STRING=value1 \
  --wait-seconds 600 \
  --poll-interval 15 \
  --token-cache auto
```

Submit with an exact Oracle payload:

```bash
python3 core/fusion-api/ess-job-submitter/scripts/ess_job_submitter.py \
  --payload-file request.json \
  --wait-seconds 600 \
  --token-cache auto
```

Resume tracking an existing ESS request:

```bash
python3 core/fusion-api/ess-job-submitter/scripts/ess_job_submitter.py \
  --request-id 123456789 \
  --wait-seconds 300 \
  --token-cache auto
```

The script reads the default Fusion environment properties file:

```text
core/auth/fusionEnv.properties
```

It imports OAuth helpers from:

```text
core/auth/fusion-oauth-authentication/scripts/fusion_auth.py
```

If the cached token is missing, expired, or rejected by Fusion with HTTP 401 or
403, the script invokes `core.auth.fusion-oauth-authentication` to obtain a
fresh token, saves it to the requested cache, and retries the ESS API call once.

## Inputs

- `ess_delegation_contract`: a validated `approved_submission` envelope
  conforming to `schemas/ess-delegation-contract.schema.json` version `1.0`.
  The core adapter extracts its `fusion_environment_context`, exact
  `request_payload`, and `execution_options` only after validation; callers
  must not provide those as independent skill-level inputs.

Script-level adapter inputs (internal mapping from the validated envelope):

- `--payload` or `--payload-file`: complete JSON submit payload.
- `--job-definition-id`: convenience input for `jobDefinitionId`.
- `--application`, `--description`, `--product`, `--request-category`,
  `--request-log-level`, `--priority`, `--retries`, `--request-timeout`,
  `--start-time`, `--end-time`, and `--schedule-id`: convenience inputs mapped
  into the submit payload.
- `--parameter`: repeated parameter as `name=value` or `name=TYPE=value`, where
  `TYPE` is `BOOLEAN`, `LONG`, `INTEGER`, `DATETIME`, or `STRING`.
- `--request-id`: track an existing ESS request instead of submitting a new one.
- `--find-recent-job-definition` with `--since-minutes`: read-only lookup for
  recent requests matching one exact job definition. Use only when the active
  workflow selects recovery lookup and the user explicitly asks to check.
- `--wait-seconds`: maximum polling time, default `300`.
- `--poll-interval`: seconds between status calls, default `10`.
- `--submit-only`: submit the request and return the requestId without polling.
- `--full-status`: return the full tracking payload rather than a compact field
  set.
- `--output`: write structured result JSON to a file.
- `--token-cache`: file token cache path, defaulting to the managed external profile cache.
- `--force-login`, `--auth-code`, `--redirect-url`, and browser flags passed to
  the shared OAuth flow when login is required.

## Outputs

- `execution_result`
- `diagnostics`
- `audit_summary`

Script-level outputs:

- Structured JSON with `execution_result`, `diagnostics`, and `audit_summary`.
- When `--output` is supplied, the submitter writes a redacted structured
  failure result even when it cannot obtain an ESS request ID. Callers must
  collect that artifact before classifying an outcome as indeterminate.
- `execution_result.requestId` contains the ESS request identifier.
- `execution_result.status` contains a compact status summary with state,
  process phase, cause, completion time, elapsed time, ECID, and any error or
  warning message returned by Fusion.
- Exit code `0`: submitted/tracked successfully or non-terminal status returned
  when no wait was requested.
- Exit code `3`: wait timeout elapsed before a terminal ESS status.
- Exit code `4`: Fusion reported a terminal unsuccessful ESS status.

## Implementation Notes

Use the bundled script or import
`core/fusion-api/ess-job-submitter/scripts/ess_job_submitter.py` from consuming
skills instead of writing endpoint-specific ESS code.

The implementation records the target environment, submit response, requestId,
status summary, and polling diagnostics. It does not print access tokens,
refresh tokens, client secrets, `.fusionaim_token.json` contents, or
Authorization headers.

Authenticated REST requests are restricted to HTTPS hosts configured by
`restBaseUrl` or `*_restBaseUrl` in `core/auth/fusionEnv.properties`; other
hosts and redirects to them are rejected.

For mutating invocations, consuming skills must include the ESS `requestId`, job
definition, request purpose, target environment, and terminal status in their own
audit artifacts.
