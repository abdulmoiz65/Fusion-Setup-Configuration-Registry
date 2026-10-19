# Manage Collective Agreements Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| CA-01 | The registered REST read contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| CA-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| CA-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| CA-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| CA-02 | Read, edit, or delete returns zero or multiple exact target matches | Input validation | Stop and request one precise business selector |
| CA-03 | Create finds an exact existing agreement | Input validation | Stop the duplicate create |
| CA-04 | No registered Core Data Loader business object supports the requested mutation | Catalog mismatch | Stop and report the unsupported operation without substituting a REST write |
| CA-05 | Core Data Loader cannot produce or preserve the reviewed source | Artifact persistence | Stop and follow the Core Data Loader correction |
| CA-06 | Source keys are partial or lack explicit supported provenance | Input validation | Stop and require complete supported key provenance; never invent values |
| CA-07 | The immutable Data Loader preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| CA-08 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| CA-08A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected agreements |
| CA-08B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| CA-08C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read route before considering any retry |
| CA-09 | Current loader metadata reports unknown attributes | Catalog mismatch | Remove unsupported blank columns, regenerate from current metadata, and revalidate the complete source |
| CA-10 | EFF_CATEGORY_CODE is missing | Catalog mismatch | Reapply the `PER_COL_EIT` default, rebuild the source, and obtain a new preview |
| CA-11 | An EFF unique reference is missing or has the wrong type | Catalog mismatch | Re-resolve the context-specific unique segment and type, rebuild every affected EFF row, and obtain new approval |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A selector, create identity, or source key is invalid or ambiguous | Correct the input and restart from validation |
| Catalog mismatch | The registered loader object, metadata, or EFF contract is unavailable or inconsistent | Refresh the contract and rebuild the source |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Artifact persistence | Core Data Loader reports that the reviewed source or immutable artifact cannot be produced or preserved | Follow the reported correction |
| Approval blocker | Preview or approval is missing, stale, or bound to different evidence | Re-preview and obtain new approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile current state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified agreement or EFF rows without assuming rollback |
| Approval blocker | Current source fingerprint and the reason the prior preview or approval is invalid |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or has an uncertain result | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not switch to Fusion REST, FSM CSV, ZAP, or another mutation route |
| Preview, approval, metadata, or source bytes changed | Do not reuse the earlier approval |
| A key, EFF category, segment, or type is unresolved | Do not invent or copy a value from an example |
| Diagnostics are returned | Do not expose credentials, runtime links, raw payloads, or surrogate IDs |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CA.ROUTE | decision | 7 | execution_gate | read->CA.DONE;create_or_edit_or_delete_ready->CA.LOADER_READY;mutation_blocked->CA.ERROR | CA.ENFORCE | stop | Select read completion or the Core Data Loader handoff |
| CA.ERROR | step | 8 | error_handler | stopped->CA.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| CA.DONE | terminal | 9 | terminal | none | CA.ROUTE | continue | Read completed |
| CA.LOADER_READY | terminal | 10 | terminal | none | CA.ROUTE | continue | Mutation rules passed; invoke core.data-loader and follow it through immutable preview |
| CA.BLOCKED | terminal | 11 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |

## Date-effective Split Deletion Failures

Classify incomplete or ambiguous split history as input validation; a REST or HDL DELETE source, mixed date-effective instructions, non-`YYYY/MM/DD` DAT date, missing `SET PURGE_FUTURE_CHANGES Y`, or non-MERGE source as catalog mismatch; and a missing retained-predecessor end-date boundary as input validation. Do not retry or substitute a REST delete. Re-read all splits through hcmDateEffectiveObjectChanges and rebuild the immutable HDL/Data Loader preview.

## Split Batch Boundaries

Do not submit a multi-split delete source from a stale timeline. If a Data Loader load is partial, failed, timed out, or uncertain, re-read the complete timeline through hcmDateEffectiveObjectChanges, report confirmed and unverified splits, and stop. Never retry automatically or substitute REST delete.

## Prohibited History-Service Mutation

Classify any attempt to submit a delete or update through hcmDateEffectiveObjectChanges as a route violation. Stop before side effects and rebuild the operation as an HDL/Core Data Loader MERGE.


## Corrected HDL Split-Deletion Contract (Supersedes Earlier Examples)

Use exactly one `SET PURGE_FUTURE_CHANGES Y` directive and one retained-predecessor `MERGE` row, with DAT dates in `YYYY/MM/DD`. The retained predecessor start and final selected end bound the contiguous removal. Reject HDL DELETE, mixed instructions, ISO DAT dates, first/only split deletion, and any REST mutation.
