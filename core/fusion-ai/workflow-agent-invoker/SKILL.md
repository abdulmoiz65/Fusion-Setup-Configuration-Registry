---
skill_id: "core.fusion-ai.workflow-agent-invoker"
name: "Fusion AI Workflow Agent Invoker"
description: "Submits and tracks on-demand Oracle Fusion AI Studio workflow agent requests."
layer: "core"
pillar: "Core"
type: "import"
execution_mode: "automated"
owner_team: "Central platform team"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "workflow_code"
  - "agent_prompt"
  - "execution_options"
outputs:
  - "execution_result"
  - "diagnostics"
  - "audit_summary"
depends_on:
  - "core.auth.fusion-oauth-authentication"
uses_core:
  - "core.auth.fusion-oauth-authentication"
persists_project_state: false
workspace_outputs: []
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Oracle Fusion Cloud Applications 26A or newer"
side_effects:
  - "Connects to Oracle Fusion AI Agent Team REST endpoints when invoked."
  - "Submits an asynchronous workflow agent request when invoked without an existing jobId."
  - "May write structured output when --output is supplied."
  - "May write local conversation state only when --state-file is supplied."
  - "May refresh the OAuth token cache when the cached token is unavailable or rejected."
required_privileges:
  - "Fusion privileges appropriate to invoke the selected AI Studio workflow agent"
---

# Fusion AI Workflow Agent Invoker

## Purpose

Submits an on-demand Oracle Fusion AI Studio workflow agent request and optionally
polls the resulting job until a final or input-required status is returned.

## REST API Contract

This skill uses the Oracle Fusion AI Agent Team REST API:

- Submit: `POST /orchestrator/agent/v2/{workflowCode}/invokeAsync`
- Track: `GET /orchestrator/agent/v2/{workflowCode}/status/{jobId}`

Oracle A-Team examples call these endpoints through the Fusion AI gateway prefix:

- Submit: `POST /api/fusion-ai/orchestrator/agent/v2/{workflowCode}/invokeAsync`
- Track: `GET /api/fusion-ai/orchestrator/agent/v2/{workflowCode}/status/{jobId}`

The submit payload always includes `message`. It can also include Oracle
documented fields such as `invocationMode`, `conversational`,
`conversationId`, `version`, `parameters`, `agentCodes`, `toolCodes`,
`resumeNodeInput`, `streamOutput`, and `progressMessage`.

## Project Scripts

Run from the repository root:

```bash
python3 core/fusion-ai/workflow-agent-invoker/scripts/workflow_agent_invoker.py \
  --workflow-code <workflowCode> \
  --message "Search for YOZ Corp" \
  --version <publishedVersion> \
  --workflow-status PUBLISHED \
  --wait-seconds 300 \
  --token-cache auto
```

Resume status polling for an existing job:

```bash
python3 core/fusion-ai/workflow-agent-invoker/scripts/workflow_agent_invoker.py \
  --workflow-code <workflowCode> \
  --job-id <jobId> \
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

## Inputs

- `fusion_environment_context`
- `workflow_code`
- `agent_prompt`
- `execution_options`

Script-level inputs:

- `--workflow-code`: AI Studio workflow code used in the REST path.
- `--message`: user prompt to submit as the workflow request message.
- `--job-id`: existing workflow job ID to poll instead of submitting a new
  request.
- `--payload` or `--payload-file`: JSON object merged into the submit payload.
- `--path-prefix`: REST path prefix before `/orchestrator`; defaults to
  `/api/fusion-ai` based on Oracle A-Team invokeAsync samples. Use an empty
  value for the raw OpenAPI path.
- `--scope`: optional OAuth scope override for this invocation. Without an
  override, the invoker uses `ai_scope` from `core/auth/fusionEnv.properties`,
  falling back to `scope` when `ai_scope` is unavailable.
- `--parameter`: repeated JSON parameter as `name=value`, `name:=json`, or
  `name@file=path`.
- `--agent-code` and `--tool-code`: repeated values mapped to `agentCodes` and
  `toolCodes`.
- `--version`, `--workflow-status`, `--conversation-id`, `--conversational`,
  `--new`, optional `--state-file`, and
  `--client-generated-conversation-id`: options for conversational workflow
  turns. Use a path under `project/{project_id}/artifacts/core/fusion-ai/`
  when conversation state must persist across sessions.
- `--wait-seconds`, `--poll-interval`, and `--submit-only`: polling controls.
- `--token-cache`, `--force-login`, `--auth-code`, `--redirect-url`, and browser
  flags passed to the shared OAuth flow when login is required.

## Outputs

- `execution_result`
- `diagnostics`
- `audit_summary`

Script-level outputs:

- Structured JSON containing the submit payload, status payload, extracted
  `jobId`, status fields, polling diagnostics, and target environment summary.
- Optional conversation state file when `--state-file` is supplied.
- Exit code `0`: submitted/tracked successfully or non-terminal status returned
  when no wait was requested.
- Exit code `3`: wait timeout elapsed before a final or input-required status.
- Exit code `4`: Fusion reported a terminal unsuccessful status.

## Implementation Notes

Use the bundled script instead of writing workflow-specific authentication,
`invokeAsync`, or status polling code in consuming skills. Never print access
tokens, refresh tokens, client secrets, `.fusionaim_token.json` contents, or
Authorization headers.

Consuming skills must record the workflow code, prompt purpose, target
environment, returned `jobId`, and terminal status in their own audit artifacts
when the invocation has implementation side effects.
