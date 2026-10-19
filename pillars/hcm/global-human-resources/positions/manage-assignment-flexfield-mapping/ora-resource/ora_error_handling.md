# Manage Assignment Flexfield Mapping Error Handling

## Purpose

Defines task-specific failure classification, safe disclosure, and
stop-before-retry behavior for Manage Assignment Flexfield Mapping.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| AFM-01 | Runtime resource discovery or mapping pagination fails | Catalog mismatch | Stop; do not match, preview, or mutate from a partial snapshot |
| AFM-02 | An exact selector has zero or multiple mappings | Input validation | Return the count and minimum business disambiguators; never select the first row |
| AFM-03 | A context or segment is unresolved, ambiguous, or has an invalid scope pairing | Input validation | Stop before preview and request a corrected business value |
| AFM-13 | Fusion Data Loader rejects datatype, precision, or value-set compatibility during a submitted load | Process failed | Preserve the returned diagnostic, reconcile the mapping through authorized reads, and stop before retry |
| AFM-12 | A request includes a legal-employer name, identifier, or association delta | Input validation | Stop before preview; remove the legal-employer input because this task supports only Position Segment to Assignment Segment mappings |
| AFM-04 | The registered Data Loader business object is unavailable or rejects the reviewed source | Artifact persistence | Stop and follow the Core Data Loader correction; do not substitute a direct REST mutation |
| AFM-05 | Preview or exact mutation approval is absent or stale | Approval blocker | Rebuild the preview and obtain current approval |
| AFM-06 | Core Data Loader is failed, completed with errors, partial, timed out, or uncertain | Process failed | Preserve diagnostics, reconcile through authorized reads, and stop before retry |
| AFM-07 | Verification does not prove the requested business state | Verification | Return FAILED or UNCERTAIN from the available evidence; do not replay automatically |
| AFM-08 | A child CUD source has no matching root grouping row, a nonblank root RestAction, a blank grouping ID, different parent and child FlexSegmentMappingGroupKey values, or a key reused by another independent request | Input validation | Rebuild the immutable source with one non-mutating root grouping row and one fresh unique group key for each independent request; do not submit it |
| AFM-09 | An update or delete child source cannot obtain one exact current FlexSegmentMappingId | Input validation | Stop, reread the current mapping state, and resolve the exact target; do not generate a replacement dummy ID |
| AFM-10 | A delete load returns a child Delete error, including missing RAW_REST payload configuration or HTTP 400 | Process failed | Preserve the error log, reconcile the target, and stop; do not retry a compact sample, DELETE directive, or nonblank Delete-row RestAction |
| AFM-11 | The live raw DAT template cannot be fetched or its registered shape changes | Catalog mismatch | Stop before preview; refresh the registered business object and raw UCM template, then rebuild and validate the source |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required input, target identity, reference, or mapping compatibility is invalid | Correct the input and restart resolution |
| Catalog mismatch | The read contract is unavailable or incomplete | Rediscover the current read contract before continuing |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion read or Data Loader privilege is denied | Restore required access; do not change routes |
| Artifact persistence | The reviewed Data Loader source cannot be produced or preserved | Follow the reported Core Data Loader correction |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain current approval |
| Process failed | Data Loader fails, completes with errors, returns partial results, or has an uncertain outcome | Preserve diagnostics, reconcile mapping state, and stop before retry |
| Process timeout | Data Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |
| Verification | Fresh authorized reads do not prove the intended result | Reconcile and do not replay |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Read resolution failure | Applied business filters, match count, and minimum safe disambiguators |
| Data Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified mappings without assuming rollback |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation is requested | Do not submit a direct REST custom action; use core.data-loader with AssignmentFlexfieldsMapping |
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| Target, mapping, delta, or approval is ambiguous | Do not prepare or submit CUD source data |
| Diagnostics are returned | Do not expose tokens, secrets, full payloads, internal synchronization configuration, or transient identifiers |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AFM.ROUTE | decision | 8 | execution_gate | read->AFM.DONE_READ;cud_ready->AFM.LOADER_READY;mutation_blocked->AFM.ERROR | AFM.DESIGN | stop | Select read completion or the Core Data Loader handoff |
| AFM.ERROR | step | 9 | error_handler | stopped->AFM.BLOCKED | none | stop | A prior node returns missing, invalid, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| AFM.DONE_READ | terminal | 10 | terminal | none | AFM.ROUTE | continue | Read completed |
| AFM.LOADER_READY | terminal | 11 | terminal | none | AFM.ROUTE | continue | CUD attributes are validated and ready for core.data-loader |
| AFM.BLOCKED | terminal | 12 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
