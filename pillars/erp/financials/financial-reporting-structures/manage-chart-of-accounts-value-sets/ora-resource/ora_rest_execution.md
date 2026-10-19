# Execution Contract

## Runtime Sources

| Source | Purpose |
|---|---|
| Shared FDOS FSM export/import and validation skills | Supported package operations |
| Core FSM REST client and OAuth skill | Approved shared primitives only |

## Execution Contract

| Situation | What Happens |
|---|---|
| Direct REST write contract unavailable | Mark TBD; do not invent endpoint, payload, or UI-label code |
| Value-set lookup returns absent for a validated COA segment | Continue with export and package readiness using the validated defaulted candidate. Do not require a separate value-set creation confirmation. |
| Live import | Require preview, read-only discovery, readiness record, and explicit approval |
