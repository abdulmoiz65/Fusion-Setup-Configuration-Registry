# Sales Play Knowledge Management REST API Instructions

Use this instruction file for Oracle Fusion Knowledge Management endpoints
under:

```text
/api/knowledge-management
```

Invoke these endpoints with the single scope token containing
`knowledge-management` from the regular OAuth `scope` property in
`core/auth/fusionEnv.properties`. Use the task-local wrapper instead of the
BOSS client so the `/api/knowledge-management` path boundary remains enforced.

## Script

Run from the repository root:

```bash
python3 pillars/cx/sales/sales-orchestration/sales-plays-and-content/scripts/knowledge_rest_client.py \
  '/api/knowledge-management/v2/contentIntelligence' \
  --method POST \
  --header 'Content-Type=application/json' \
  --body '<serialized-request-body>'
```

## OAuth Scope and Cache

The script reads the regular `scope` from:

```text
core/auth/fusionEnv.properties
```

It splits that value on whitespace and uses the single scope token containing
`knowledge-management` to acquire the OAuth token. If no matching scope token
or more than one matching scope token exists, stop before requesting a token and
fix the `scope` property.

Default Knowledge Management token cache, local to this task skill:

```text
pillars/cx/sales/sales-orchestration/sales-plays-and-content/.fusionaim_km_token.json
```

The task-local `.gitignore` excludes this cache. Keep it separate from
`.fusionaim_token.json` and `.fusionaim_boss_token.json`. The client refreshes
the Knowledge Management cache and retries exactly once after HTTP 401 or 403.

If the interactive authorization callback returns `unauthorized_client`, stop
without retrying. The configured OAuth client or regular scope is not accepted
by the target identity domain, and no Knowledge Management endpoint request was
sent. Require an approved OAuth client registration and regular scope that can
obtain a token for the selected `knowledge-management` scope token; do not fall
back to a separate Knowledge Management scope property or a pasted bearer token.

## Endpoint Rules

- The wrapper accepts only endpoints under `/api/knowledge-management`; this
  skill invokes only `/api/knowledge-management/v2/contentIntelligence`.
- Relative endpoints are joined to `restBaseUrl`.
- Use JSON request bodies through `--body` or `--body-file`.
- Never pass a bearer token or Authorization header from user input.
- The Content Intelligence POST has semantic-read behavior. The wrapper does
  not grant approval for another POST or any mutation.
