# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Payload differs from the fixed parent-job contract or targets RequestProcessJob | Classify as catalog_mismatch and stop before preview-ready status. |
| Refresh Metadata is unsupported or Dispatch Job Timeout is nonnumeric | Classify as input_validation and stop before preview. |
| Recurring schedule is missing, unbounded, malformed, violates an Oracle RRULE restriction, or is combined with scheduleId or top-level start/end fields | Classify as input_validation and stop before preview. |
| Scheduler rejects the approved recurrence | Preserve the exact schedule and response, classify as Fusion_API, and do not retry or replace it automatically. |
| Scheduler rejects a custom timeout | Preserve the exact value and response, classify as Fusion_API, and do not invent or retry with another value. |
| 401 or 403 | Classify auth_or_authorization; allow one token refresh through the core workflow, but never replay an uncertain POST. |
| Transport failure, timeout, missing response, or missing requestId after POST | Treat as an uncertain mutation, preserve the target and fingerprint, reconcile before any new submission, and never retry automatically. |
| Polling timeout | Preserve requestId, last state, elapsed wait, and same-request resume path. |
| Terminal process failure | Preserve requestId, state, cause, ECID, and available diagnostics; never submit a replacement automatically. |
| Scheduler reports Succeeded | Report completion only for the returned parent or child request; do not claim every recurrence or resolution request completed successfully without occurrence-level and business reconciliation. |
| Artifact persistence fails | Preserve the external requestId in the response and classify artifact_persistence without resubmitting. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RDJ.ERROR | step | 80 | error_handler | disclosed->RDJ.RETURN_ISSUES | none | stop | Any blocked validation, lookup, dependency, enforcement, execution, or tracking result. |
| RDJ.STATUS_DONE | terminal | 90 | terminal | none | RDJ.STATUS_LOOKUP | continue | Existing request status returned without a new submission. |
| RDJ.READY | terminal | 91 | terminal | none | RDJ.ENFORCE | continue | Validated and ready for the owning ESS executor after approval. |
| RDJ.RETURN_ISSUES | terminal | 99 | terminal | none | RDJ.ERROR | continue | Classified issues returned without a new side effect. |
