# Error Handling

| Failure class | Required response |
|---|---|
| `input_validation` | Correct required scope, role, archive, or approval input and restart. |
| `catalog_mismatch` | Stop and reconcile task identity or catalog flags. |
| `auth/authz` | Report missing access without exposing credentials; do not retry blindly. |
| `transport/environment` | Report target-resolution or connectivity issue; only the owner may apply read retry policy. |
| `Fusion API` | Preserve redacted response evidence and stop. |
| `process_timeout` / `process_failed` | Preserve identifier, last status, elapsed time, and permitted process evidence; do not replace the process. |
| `artifact_persistence` | Preserve safe diagnostics and report intended project path. |
| `approval_blocker` | Stop before mutation/import; regenerate preview and obtain fresh approval if anything changed. |

Diagnostics contain status, stage, failure class, message, recommended action, environment, artifact references, and external identifiers only when safe. Redact credentials, tokens, customer data, role assignments, and policy details.
