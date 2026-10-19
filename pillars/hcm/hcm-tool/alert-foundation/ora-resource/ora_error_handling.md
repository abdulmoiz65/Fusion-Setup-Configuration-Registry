# Alert Foundation Error Handling

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| CUSTOM_ALERTS | Alerts | Simple CREATE is selected | Do not block for omitted live describe, LOV, language or existing-code checks; disclose that Fusion validates business values on submission |
| CUSTOM_ALERTS | Alerts | Deep is selected and a required live check fails or is missing | Stop before approval; do not silently downgrade to simple |
| CUSTOM_ALERTS | Alerts | Validation mode changes after a preview | Regenerate the mode-bound work unit and obtain its new exact approval |
| CUSTOM_ALERTS | Alerts | Batch-create is requested | Present exactly one immutable whole-workbook unit and one Confirm Alert Batch approval; do not apply per-part sequential approvals |
| CUSTOM_ALERTS | Alerts | Batch HTTP 200 contains missing, duplicate, unknown, rejected or mismatched parts | Return external_operation_failed with sanitized per-part reconciliation evidence; HTTP 200 alone is not success |
| CUSTOM_ALERTS | Alerts | Batch submission errors or times out | No automatic retry, rollback or sequential fallback; reconcile every submitted part before proposing a newly approved recovery plan |
| CUSTOM_ALERTS | Alerts | Batch response matches all parts | Return submitted_pending_verification until independent Alert, Template and Recipient read-backs pass; disclose deferred Body verification |
| CUSTOM_ALERTS | Alerts | Input or payload validation fails | Stop before external access and identify exact invalid fields |
| CUSTOM_ALERTS | Alerts | Describe metadata is incompatible | Stop before mutation and report catalog_or_metadata_mismatch |
| CUSTOM_ALERTS | Alerts | OAuth is missing, expired, or rejected | Allow the shared client one refresh attempt for 401 or 403, then stop |
| CUSTOM_ALERTS | Alerts | Authorization remains rejected | Stop as authorization_or_privilege; do not infer permission from earlier GET success |
| CUSTOM_ALERTS | Alerts | POST, PATCH, DELETE, or copy returns an error | Record sanitized status, path, response summary, and request or ECID reference; do not retry automatically; stop the active work unit before its next write |
| CUSTOM_ALERTS | Alerts | Mutation response is uncertain | Reconcile with read-only exact identity checks before proposing any new mutation |
| CUSTOM_ALERTS | Alerts | Inline Template Body PATCH does not return HTTP 200 | Stop the work unit before Recipient creation; preserve earlier verified creates and do not retry automatically |
| CUSTOM_ALERTS | Alerts | BodyFilePath or BodyFileSHA256 is supplied | Stop before any mutation because version 0.8.0 has no governed raw-byte enclosure route |
| CUSTOM_ALERTS | Alerts | Read-back differs from the approved intent | Return external_operation_failed and preserve the mismatch evidence |
| CUSTOM_ALERTS | Alerts | A work-unit operation fails after earlier operations verified | Return partial_success with completed and failed sequence details; do not retry, continue, or issue compensating DELETE operations |

## Error Classifications

| Task Code | Task Name | Result Category | When Used | Next Action |
|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | input_validation | Required fields, enums, lengths, types, or payload shape fail | Correct input and regenerate preview |
| CUSTOM_ALERTS | Alerts | catalog_or_metadata_mismatch | Describe, finder, key, method, action, or attribute contract differs | Review compatibility before retry |
| CUSTOM_ALERTS | Alerts | auth_or_authz | OAuth refresh fails or Fusion returns persistent 401 or 403 | Correct identity, role, duty, or privilege |
| CUSTOM_ALERTS | Alerts | transport_or_environment | Host, TLS, timeout, or environment selection fails | Correct environment or retry only an eligible read |
| CUSTOM_ALERTS | Alerts | fusion_api_error | Fusion rejects a validly formed request | Review redacted response and current state |
| CUSTOM_ALERTS | Alerts | approval_blocker | Immediate approval is absent, stale, or mismatched | Re-present the exact preview |
| CUSTOM_ALERTS | Alerts | verification_failed | Independent read-back does not match intended state | Stop and reconcile without another mutation |
| CUSTOM_ALERTS | Alerts | partial_success | One or more earlier work-unit operations verified before a later operation failed | Preserve verified results and require a newly approved recovery plan |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| CUSTOM_ALERTS | Alerts | Before approval | For an eligible hierarchy create, the complete ordered work-unit document, every payload digest, execution policy, aggregate SHA-256, and exact Confirm Alert Work Unit phrase; otherwise the individual mutation preview |
| CUSTOM_ALERTS | Alerts | After submission | Per-operation single-submission outcome, sanitized HTTP status and response summary, safe returned identity, verification result, and final completed or partial-success state |
| CUSTOM_ALERTS | Alerts | On failure | Failure class, stage, environment, redacted evidence, external request identifiers when available, and one safe next action |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| CUSTOM_ALERTS | Alerts | Approval is missing or stale | Do not submit a mutation |
| CUSTOM_ALERTS | Alerts | A write result is uncertain | Do not replay POST, PATCH, DELETE, or copy |
| CUSTOM_ALERTS | Alerts | An approved work unit changes or a returned canonical key differs | Do not continue under the old aggregate approval |
| CUSTOM_ALERTS | Alerts | requested_intent is upsert or process | Do not substitute create/update behavior or call the action |
| CUSTOM_ALERTS | Alerts | Identity is ambiguous | Do not choose an arbitrary alert |
| CUSTOM_ALERTS | Alerts | Consumer supplies a raw endpoint or payload | Do not bypass the provider contract and design gates |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_ALERTS | Alerts | ALERT.APPROVAL | decision | 5 | execution_gate | approved->ALERT.READY;blocked->ALERT.RETURN_ISSUES | ALERT.DESIGN | stop | A mutation is requested; read-only requests record not applicable and continue |
| CUSTOM_ALERTS | Alerts | ALERT.READY | terminal | 6 | terminal | none | ALERT.APPROVAL | continue | All applicable gates passed; simple CREATE records lookup skipped_simple rather than a live pass |
| CUSTOM_ALERTS | Alerts | ALERT.RETURN_ISSUES | terminal | 7 | terminal | none | none | continue | Any validation, lookup, dependency, design, or approval gate blocked |
