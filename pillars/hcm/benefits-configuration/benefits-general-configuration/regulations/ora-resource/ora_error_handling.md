# Benefit Regulations Error Handling

## Error Situations

| Situation | What Should Happen |
| --- | --- |
| Missing operation, identity, date, effective range, or immutable artifact | Classify as `input_validation`; stop and identify the exact missing value |
| Current sample, object, header, action, or date-effective support conflicts with the request | Classify as `catalog_or_metadata_mismatch`; do not invent a field or operation |
| Cached-token 401 or 403 during selected read-only activity | Delegate at most one refresh to the selected core service; then classify remaining denial as `authorization_or_privilege` |
| Read-only transport/environment failure | Classify as `transport_or_environment`; use only the selected core service's bounded retry policy |
| Fusion response rejects an artifact | Classify as `fusion_api_error`; preserve sanitized status evidence and rebuild from the current sample |
| Process timeout or terminal failure | Classify as `process_timeout` or `process_failed`; stop and report target, task, artifact, process/request ID, last status, elapsed wait, and next-check path |
| Mutation failure or uncertain outcome | Classify as `approval_blocker`; do not retry upload, initiation, update, delete, or ZAP automatically |

## Disclosure and Redaction

Persist diagnostic status, stage, failure class, recommended action, environment,
artifact reference, and available external identifiers under the project
workspace when a durable run exists. Redact credentials, tokens, token-cache
contents, private keys, customer data, and full payload/base64 content.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BEN_REG.GATE_EXECUTION | decision | 50 | execution_gate | approved->BEN_REG.READY_FOR_APPROVAL;blocked->BEN_REG.HANDLE_ISSUE | BEN_REG.ENFORCE_DESIGN | stop | Confirm a data-changing action has current approval bound to the validated artifact and target |
| BEN_REG.HANDLE_ISSUE | step | 90 | error_handler | handled->BEN_REG.RETURN_ISSUES | none | stop | A validation, readiness, design, approval, or execution issue occurs |
| BEN_REG.READY_FOR_APPROVAL | terminal | 100 | terminal | none | BEN_REG.GATE_EXECUTION | stop | All gates passed; ready for the authoritative `core.data-loader` approval workflow |
| BEN_REG.RETURN_ISSUES | terminal | 110 | terminal | none | none | stop | A blocking issue was safely disclosed |
