# Manage Grade Ladders Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| GLAD-01 | The Grade Ladder REST read contract is missing or incompatible | Catalog mismatch | Stop and record the capability gap with owner, task impact, approved fallback, and disposition |
| GLAD-01D | Grade Ladders rejects a GradeLadderName search field | Catalog mismatch | Use the declared Name field; do not report a missing Fusion capability |
| GLAD-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| GLAD-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| GLAD-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| GLAD-02 | Read, edit, or delete returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| GLAD-03 | Create finds an exact existing Grade Ladder | Input validation | Stop the duplicate create |
| GLAD-04 | No registered Core Data Loader business object supports the requested mutation | Catalog mismatch | Stop and report the unsupported operation |
| GLAD-05 | A required component or writable attribute cannot be resolved | Catalog mismatch | Stop before authoring and resolve it from the authorized read or current loader metadata |
| GLAD-05A | A GradeLadder create source omits GradeSetCode | Input validation | Apply the COMMON default or preserve a validated explicit value, then rebuild the source |
| GLAD-05B | Grade Steps do not resolve a complete ordered count and ceiling Step | Input validation | Correct the Grade dependency and rebuild the source |
| GLAD-05C | StepRateValue rows are missing or duplicated for a Rate by Grade Step combination | Input validation | Correct the complete matrix and rebuild the source |
| GLAD-05D | A constructed Grade Steps child path returns HTTP 404 | Catalog mismatch | Re-read the Grade through gradesV2 and follow its returned item and gradeSteps links; do not report missing Grade Steps |
| GLAD-06 | Core Data Loader cannot produce or preserve the reviewed source | Artifact persistence | Stop and follow the Core Data Loader correction |
| GLAD-07 | Source keys are partial or lack explicit supported provenance | Input validation | Stop and require complete supported key provenance |
| GLAD-08 | The immutable Data Loader preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| GLAD-09 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| GLAD-09A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected grade ladders |
| GLAD-09B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| GLAD-09C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| GLAD-10 | A date-effective split deletion lacks an exact retained start, aligned deletion end, safe predecessor row, or a loader contract that preserves `SET PURGE_FUTURE_CHANGES Y` | Input validation | Stop; re-read Grade Ladder history and rebuild the bounded `MERGE` range only when the current generated contract preserves the directive |
| GLAD-10A | The generated DAT omits `SET PURGE_FUTURE_CHANGES Y` or changes the reviewed bounded `MERGE` range | Catalog mismatch | Stop before preview; do not submit a source whose converted operation differs from the reviewed operation |
| GLAD-10B | Post-delete-effective-split history does not preserve the predecessor and remove only the confirmed future range | Process failed | Stop without retry and report the failed reconciliation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, duplicate check, loader key, or GradeType is invalid or ambiguous | Correct the input and restart validation |
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
| Partial or uncertain result | Confirmed, failed, and unverified Grade Ladder rows without assuming rollback |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| A read or platform capability is unavailable | Do not infer or substitute a capability without a declared approved route |
| Preview, approval, contract, or source bytes changed | Do not reuse the earlier approval |
| A component, field, ID, or loader key is unresolved | Do not invent a value |
| A date-effective split deletion is requested | Do not use an HDL `DELETE` instruction or delete the logical Grade Ladder record; use only a reviewed `GradeLadder` `MERGE` range with `SET PURGE_FUTURE_CHANGES Y` when the current generated Grade Ladder loader contract preserves it. |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or protected identifiers |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GLAD.ROUTE | decision | 6 | execution_gate | read->GLAD.DONE;create_or_edit_or_delete_ready->GLAD.LOADER_READY;not_ready->GLAD.ERROR | GLAD.ENFORCE | stop | Select read completion or the Core Data Loader handoff |
| GLAD.ERROR | step | 7 | error_handler | stopped->GLAD.STOPPED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, unverified, or unsupported |
| GLAD.DONE | terminal | 8 | terminal | none | GLAD.ROUTE | continue | Read completed |
| GLAD.LOADER_READY | terminal | 9 | terminal | none | GLAD.ROUTE | continue | Mutation rules passed; invoke core.data-loader and follow it through immutable ZIP preview |
| GLAD.STOPPED | terminal | 10 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
