# Manage Grade Rates Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| GRAT-01 | The Grade Rate REST read contract is missing or incompatible | Catalog mismatch | Stop and record the capability gap with owner, task impact, approved fallback, and disposition |
| GRAT-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| GRAT-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| GRAT-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| GRAT-02 | Read, edit, or delete returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| GRAT-03 | Create finds an exact existing Grade Rate | Input validation | Stop the duplicate create |
| GRAT-04 | No registered Core Data Loader business object supports the requested mutation | Catalog mismatch | Stop and report the unsupported operation |
| GRAT-05 | A required component or writable attribute cannot be resolved | Catalog mismatch | Stop before authoring and resolve it from the authorized read or current loader metadata |
| GRAT-05A | The GradeRate parent lacks a complete supported key and GradeRateValue rows report a missing parent | Input validation | Correct the parent key, keep exact parent-key parity on every child, and rebuild the source |
| GRAT-05B | The preview summary differs from the populated workbook or generated DAT | Input validation | Stop before approval and rebuild the artifact from the validated values |
| GRAT-05C | A date-effective split deletion lacks an exact retained start, aligned deletion end, safe predecessor row, or complete future GradeRateValue readback | Input validation | Stop; re-read Grade Rate history and affected future values, then rebuild the MERGE range with `SET PURGE_FUTURE_CHANGES Y` |
| GRAT-05D | Create asks the end user for RateObjectId or accepts an unverified supplied value | Input validation | Stop the prompt, resolve the Grade business key, use GradeCode with SetCode by default, and derive RateObjectId from the resolved GradeId only if Core Data Loader selects the internal-ID alternative |
| GRAT-06 | Core Data Loader cannot produce or preserve the reviewed source | Artifact persistence | Stop and follow the Core Data Loader correction |
| GRAT-08 | The immutable Data Loader preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| GRAT-09 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| GRAT-09A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected grade rates |
| GRAT-09B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| GRAT-09C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, duplicate check, loader key, or currency is invalid or ambiguous | Correct the input and restart validation |
| Catalog mismatch | The loader object, component, or writable attribute contract is unavailable | Restore the contract before authoring |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Artifact persistence | Core Data Loader reports that the reviewed source or immutable artifact cannot be produced or preserved | Follow the reported correction |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain new approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile current state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Capability gap | Owner, affected task, impact, approved fallback when one exists, and disposition |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Grade Rate rows without assuming rollback |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| A read or platform capability is unavailable | Do not infer or substitute a capability without a declared approved route |
| Preview, approval, contract, or source bytes changed | Do not reuse the earlier approval |
| A component, field, ID, or loader key is unresolved | Do not invent a value |
| A GradeRateValue row needs its Grade key | Do not request RateObjectId from the end user; resolve the Grade business key and keep internal identifiers hidden |
| A date-effective split deletion is requested | Do not use an HDL DELETE instruction, delete the logical Grade Rate, or author GradeRateValue rows; use only a reviewed Grade Rate MERGE range with `SET PURGE_FUTURE_CHANGES Y` |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or protected identifiers |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GRAT.ROUTE | decision | 6 | execution_gate | read->GRAT.DONE;create_or_edit_or_delete_or_split_delete_ready->GRAT.LOADER_READY;not_ready->GRAT.ERROR | GRAT.ENFORCE | stop | Select read completion or the Core Data Loader handoff |
| GRAT.ERROR | step | 7 | error_handler | stopped->GRAT.STOPPED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, unverified, or unsupported |
| GRAT.DONE | terminal | 8 | terminal | none | GRAT.ROUTE | continue | Read completed |
| GRAT.LOADER_READY | terminal | 9 | terminal | none | GRAT.ROUTE | continue | Mutation rules passed; invoke core.data-loader, verify source and DAT key parity, and follow it through immutable ZIP preview. For a split deletion, re-read retained Grade Rate history and the purged segment's GradeRateValue rows after load. |
| GRAT.STOPPED | terminal | 10 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
