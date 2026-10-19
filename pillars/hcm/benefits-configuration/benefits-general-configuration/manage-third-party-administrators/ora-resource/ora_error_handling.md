# Manage Third-Party Administrators Error Handling

| Failure class | Required response |
|---|---|
| `input_validation` | Identify the field and row, request correction, and stop before preview. |
| `catalog_or_metadata_mismatch` | Stop; do not guess a classification name, location code, object, or route. |
| `auth_authz` | Stop after core's permitted refresh and request authorized access restoration. |
| `transport_environment` or `fusion_api` | Report environment and stage; retry only a known-safe read through core. |
| `artifact_persistence` or `approval_blocker` | Stop; preserve the reviewed artifact, revalidate, and obtain appropriate approval. |
| `process_failed` | Preserve diagnostics and confirmed successes; reconcile state before correction. |
| `process_timeout` | Report environment, operation, process ID, last status, elapsed time, and next status-check path. |

Always report a redacted message, artifact reference where available, and one
safe next action. Never automatically retry a mutation, roll back a load, or
expose secrets, tokens, full rows, or protected identifiers.
