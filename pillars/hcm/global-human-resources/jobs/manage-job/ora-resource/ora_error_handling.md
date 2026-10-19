# Manage Jobs Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| JOB-01 | The jobsV2 REST response contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| JOB-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| JOB-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| JOB-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| JOB-02 | Read, edit, inactivate, or delete-effective-split returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| JOB-03 | Create finds an exact existing Job | Input validation | Stop the duplicate create |
| JOB-03A | A date-effective split deletion lacks an exact retained start, aligned deletion end, or safe predecessor row | Input validation | Stop; re-read Job history and rebuild the bounded `MERGE` range with `SET PURGE_FUTURE_CHANGES Y` |
| JOB-03B | Post-delete history differs from the confirmed split-range removal and preceding-boundary change | Process failed | Stop without retry and report failed verification |
| JOB-03C | The history request fails | Fusion API | Report the actual REST failure and stop; do not describe history as incomplete |
| JOB-04 | Core Data Loader cannot produce or preserve the reviewed source | Artifact persistence | Stop and follow the Core Data Loader correction |
| JOB-05 | Job Family or selected reference-data-set context is unresolved or inconsistent | Input validation | Stop and resolve one effective Job Family in the selected set context |
| JOB-06 | XLSX or DAT includes an unmodified child or EFF object | Input validation | Remove its worksheet and Data Loader Map row, then regenerate the DAT internally |
| JOB-07 | A Job EFF category, context discriminator, or multirow unique key is missing or incorrect | Catalog mismatch | Correct the EFF controls and rebuild the source |
| JOB-07A | A new Job EFF child row omits a required create-time identity field | Input validation | Stop before preview, resolve the current child identity shape, and rebuild the source |
| JOB-09 | Core Data Loader reports that current metadata is unavailable or stale | Catalog mismatch | Stop and follow the Core Data Loader correction |
| JOB-09A | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| JOB-10 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| JOB-10A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected jobs |
| JOB-10B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| JOB-10C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, Job Family context, modified-object scope, loader key, or EFF row is invalid | Correct the input or source scope and restart resolution |
| Catalog mismatch | An EFF category differs from the registered Job child-object contract | Correct the category and rebuild the source |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Fusion API | Fusion rejects the declared history request | Report the sanitized response and correct the request before retry |
| Artifact persistence | Core Data Loader reports that the reviewed source cannot be produced or preserved | Follow the reported correction |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain current approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile current state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| EFF category failure | Affected child object, observed category, and required JOB_LEG or JOB_EIT category |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Job, child, or EFF rows without assuming rollback |
| Delete eligibility | Job code or name, retained effective start, and inclusive deletion end only; never show FirstSplitFlag or internal identifiers |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not switch to a REST write or another mutation route |
| Preview, approval, contract, or source bytes changed | Do not reuse the earlier approval |
| A loader key, Job Family, or set context is unresolved | Do not infer or invent a value |
| A child or EFF object was not modified | Do not retain its worksheet or Data Loader Map row |
| A date-effective split deletion is requested | Do not use an HDL `DELETE` instruction or delete the logical Job record; use only a reviewed Job `MERGE` range with `SET PURGE_FUTURE_CHANGES Y` |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or surrogate IDs |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JOB.ROUTE | decision | 7 | execution_gate | read->JOB.DONE;create_or_edit_or_inactivate_or_split_delete_ready->JOB.LOADER_READY;mutation_blocked->JOB.ERROR | JOB.DESIGN | stop | Select read completion or the Core Data Loader handoff |
| JOB.ERROR | step | 8 | error_handler | stopped->JOB.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, first-row, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| JOB.DONE | terminal | 9 | terminal | none | JOB.ROUTE | continue | Read completed |
| JOB.LOADER_READY | terminal | 10 | terminal | none | JOB.ROUTE | continue | Mutation rules passed; invoke core.data-loader and follow it through immutable ZIP preview |
| JOB.BLOCKED | terminal | 11 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
