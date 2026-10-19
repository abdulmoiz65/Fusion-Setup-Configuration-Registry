# Manage Extended Lookup Codes Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| XLOOK-01 | The Extended Lookup Code REST read contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| XLOOK-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| XLOOK-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| XLOOK-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| XLOOK-02 | Read, edit, or delete returns zero or multiple exact targets | Input validation | Stop and request one precise scoped business key |
| XLOOK-03 | Create finds an exact existing Extended Lookup Code | Input validation | Stop the duplicate create |
| XLOOK-04 | No registered Core Data Loader business object supports the requested mutation | Catalog mismatch | Stop and report the unsupported operation without substituting a REST write |
| XLOOK-05 | A mutation has no reviewed live-validated XLSX source | Artifact persistence | Stop before internal DAT or ZIP generation and rebuild the source |
| XLOOK-05A | The internally generated DAT header, record verb, or ZIP member filename differs from the native Extended Lookup contract | Catalog mismatch | Regenerate from the frozen XLSX through Core Data Loader, use `MERGE` for create/edit or `DELETE` for delete, and name the member after the exact top-level discriminator |
| XLOOK-06 | Base-create source keys are missing, partial, present-but-blank, or lack explicit supported provenance | Input validation | Require a complete validated caller pair or generate the deterministic FDOS pair before preview |
| XLOOK-06A | Fusion reports that a MERGE line does not include values defining a unique reference | Process failed | Confirm that no row loaded, reconcile the exact business key, rebuild the source with the required complete source-key pair, and require a new immutable preview and approval; never replay the failed bytes |
| XLOOK-07 | The immutable Data Loader preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| XLOOK-08 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| XLOOK-08A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected lookup codes |
| XLOOK-08B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| XLOOK-08C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A scoped key, duplicate check, or source key is invalid or ambiguous | Correct the input and restart from validation |
| Catalog mismatch | The registered loader object does not support the mutation | Restore the contract before rebuilding the source |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Artifact persistence | The reviewed XLSX or derived immutable artifact is unavailable | Rebuild and preserve the complete source artifact |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain new approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile current state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Extended Lookup Code rows without assuming rollback |
| Approval blocker | Current XLSX and ZIP fingerprints and the reason approval is missing or stale |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not substitute a REST write, FSM, CSV, or another mutation route |
| Preview, approval, contract, or source bytes changed | Do not reuse the earlier approval |
| A scoped business key or source key is unresolved | Do not infer, reuse a saved internal ID, or invent a value |
| A base create omits source keys | Do not preview, approve, upload, or retry a keyless MERGE; require nonblank SourceSystemOwner and SourceSystemId values in both metadata and data |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or surrogate IDs |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| XLOOK.ROUTE | decision | 6 | execution_gate | read->XLOOK.DONE;create_or_edit_or_delete_ready->XLOOK.LOADER_READY;mutation_blocked->XLOOK.ERROR | XLOOK.ENFORCE | stop | Select read completion or the Core Data Loader handoff |
| XLOOK.ERROR | step | 7 | error_handler | stopped->XLOOK.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| XLOOK.DONE | terminal | 8 | terminal | none | XLOOK.ROUTE | continue | Read completed |
| XLOOK.LOADER_READY | terminal | 9 | terminal | none | XLOOK.ROUTE | continue | Mutation rules passed; invoke Core Data Loader and follow it through immutable ZIP preview |
| XLOOK.BLOCKED | terminal | 10 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
