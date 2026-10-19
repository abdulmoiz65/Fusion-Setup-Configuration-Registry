# Manage Regulatory Bodies Error Handling

| Failure class | Trigger | Required response |
|---|---|---|
| input_validation | Missing, invalid, or conflicting business input or source row | Identify the field and row, request correction, and stop before preview. |
| catalog_or_metadata_mismatch | Organization metadata, the `REGBOD` classification LOV result, the effective-dated location LOV result, or operation support is missing or ambiguous | Stop and record the capability gap; do not hard-code a classification name, guess a location code, or substitute another object or route. |
| auth_authz | Authentication remains invalid after core's permitted refresh, or a required privilege is denied | Stop and request authorized reauthentication or access restoration. |
| transport_environment | Selected environment or required read is unavailable | Report the environment and stage; retry only a known-safe read through core. |
| fusion_api | A selected read returns an actionable Fusion error | Preserve the redacted message and correct the request before retrying. |
| artifact_persistence | Reviewed source, immutable archive, or approval binding cannot be preserved | Stop; do not upload an unreviewed rebuild. |
| approval_blocker | Approval is missing, stale, or bound to different source/environment/task context | Revalidate and obtain approval for the unchanged current artifact. |
| process_failed | Load fails, completes with errors, is partial, or has uncertain outcome | Preserve diagnostics and confirmed successes; reconcile state before considering correction. |
| process_timeout | Monitoring reaches its observation deadline | Report environment, operation, process ID, last status, elapsed wait, and next status-check path. |

For every failure, report the environment, operation, stage, failure class,
redacted message, artifact reference when available, and one safe next action.
Never automatically retry a mutation, roll back a load, or expose secrets,
tokens, full source rows, or protected identifiers.
