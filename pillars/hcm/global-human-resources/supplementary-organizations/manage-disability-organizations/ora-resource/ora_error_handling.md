# Manage Disability Organizations Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| DISORG-01 | The Disability Organization REST read contract is missing or incompatible | Catalog mismatch | Stop and record the capability gap with owner, task impact, approved fallback, and disposition |
| DISORG-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| DISORG-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| DISORG-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| DISORG-02 | Read, edit, or delete returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| DISORG-03 | Create finds an exact existing Disability Organization | Input validation | Stop the duplicate create |
| DISORG-04 | No registered Core Data Loader business object supports the requested mutation | Catalog mismatch | Stop and report the unsupported operation without substituting a REST write |
| DISORG-05 | Core Data Loader cannot produce or preserve the reviewed source | Artifact persistence | Stop and follow the Core Data Loader correction |
| DISORG-06 | An included Organization EFF row is incomplete | Input validation | Stop and correct the EFF row |
| DISORG-07 | The immutable Data Loader preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| DISORG-08 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| DISORG-08A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected disability organizations |
| DISORG-08B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| DISORG-08C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| DISORG-09 | A date-effective split deletion lacks a retained predecessor, aligned final target, or `SET PURGE_FUTURE_CHANGES Y` | Input validation | Re-read the history and rebuild the bounded `MERGE` range |
| DISORG-09A | Post-delete history differs from the confirmed row removal and preceding-boundary change | Process failed | Stop without retry and report failed verification |
| DISORG-09B | The history request fails | Fusion API | Report the actual REST failure and stop; do not describe history as incomplete |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, duplicate check, loader key, classification, or EFF row is invalid or ambiguous | Correct the input and restart resolution |
| Catalog mismatch | The registered loader object does not support the mutation | Restore the loader contract before authoring |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Fusion API | Fusion rejects the declared history request | Report the sanitized response and correct the request before retry |
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
| Partial or uncertain result | Confirmed, failed, and unverified Disability Organization rows without assuming rollback |
| Delete eligibility | Basic organization details and effective period only; never show FirstSplitFlag or internal identifiers |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| A read or platform capability is unavailable | Do not infer or substitute a capability without a declared approved route |
| The declared Data Loader route is unavailable | Do not substitute a REST write or another mutation route |
| Preview, approval, contract, or source bytes changed | Do not reuse the earlier approval |
| A loader key or target is unresolved | Do not invent a value |
| A date-effective split deletion is requested | Do not use an HDL `DELETE` instruction or delete the logical organization; use only a reviewed retained-predecessor `MERGE` range with `SET PURGE_FUTURE_CHANGES Y` |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or protected identifiers |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DISORG.ROUTE | decision | 9 | execution_gate | read->DISORG.DONE;create_or_edit_or_inactivate_or_delete_ready->DISORG.LOADER_READY;mutation_blocked->DISORG.ERROR | DISORG.DESIGN | stop | Select read completion or the Core Data Loader handoff |
| DISORG.ERROR | step | 10 | error_handler | stopped->DISORG.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, first-row, blocked, failed, partial, timed-out, uncertain, stale, unverified, or unsupported |
| DISORG.DONE | terminal | 11 | terminal | none | DISORG.ROUTE | continue | Read completed |
| DISORG.LOADER_READY | terminal | 12 | terminal | none | DISORG.ROUTE | continue | Mutation rules passed; invoke core.data-loader and follow it through immutable ZIP preview |
| DISORG.BLOCKED | terminal | 13 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
