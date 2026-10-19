# Manage Worker Unions Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| UNION-01 | The Worker Union REST read contract is missing or incompatible | Catalog mismatch | Stop and record the capability gap with owner, task impact, approved fallback, and disposition |
| UNION-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| UNION-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| UNION-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| UNION-02 | Read, edit, or delete returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| UNION-03 | Create finds an exact existing Worker Union | Input validation | Stop the duplicate create |
| UNION-04 | No registered Core Data Loader business object supports the requested mutation | Catalog mismatch | Stop and report the unsupported operation |
| UNION-05 | The `ORA_PER_UNION` classification or Organization component is missing | Catalog mismatch | Stop before workbook authoring and resolve current loader metadata |
| UNION-06 | An EFF category, context discriminator, multirow key, segment, or segment value is missing or ambiguous | Input validation | Stop and correct the OrgInformation row |
| UNION-07 | Associated Bargaining Unit is resolved from anything except its context value set | Catalog mismatch | Stop and resolve it from current EFF metadata |
| UNION-07A | A missing bargaining unit is declined or does not re-resolve after Manage Common Lookups completes | Input validation | Stop the Worker Union flow; do not use the unresolved value or build its preview |
| UNION-08 | Additional Information code is already used | Input validation | Stop and request a unique code without copying or reusing the existing code |
| UNION-09 | Core Data Loader cannot produce or preserve the reviewed source | Artifact persistence | Stop and follow the Core Data Loader correction |
| UNION-11 | The immutable Data Loader preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| UNION-12 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| UNION-12A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected worker unions |
| UNION-12B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| UNION-12C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| UNION-13 | A date-effective split deletion lacks an exact retained start, aligned deletion end, adjacent future split, safe predecessor row, or operation-required classification association | Input validation | Stop; re-read Worker Union history and rebuild the bounded MERGE range with `SET PURGE_FUTURE_CHANGES Y` and at least one `OrgUnitClassification` association |
| UNION-13A | Post-delete-effective-split history differs from the confirmed row removal and preceding-boundary change | Process failed | Stop without retry and report failed verification |
| UNION-13B | The history request fails | Fusion API | Report the actual REST failure and stop; do not describe history as incomplete |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, context, segment, code, loader key, or EFF row is invalid or ambiguous | Correct the input and restart resolution |
| Catalog mismatch | Loader object, Organization component, classification, or EFF value-set contract is unavailable | Refresh current loader or EFF metadata before authoring |
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
| EFF contract failure | Context, segment, classification or value-set failure, and required metadata-refresh action |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Worker Union or Additional Information rows without assuming rollback |
| Delete eligibility | Worker Union basic details and effective period only; never show FirstSplitFlag or internal identifiers |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| A read or platform capability is unavailable | Do not infer or substitute a capability without a declared approved route |
| The declared Data Loader route is unavailable | Do not substitute another mutation route |
| Preview, approval, metadata, or source bytes changed | Do not reuse the earlier approval |
| Classification, component, context, segment, value set, key, or target is unresolved | Do not infer or invent a value |
| A bargaining unit has no value-set match | Do not create it implicitly or continue before Manage Common Lookups verifies creation and the segment re-resolves |
| Additional Information code already exists | Do not copy or reuse the existing code |
| Complete delete, ZAP, first-row delete, or an unbounded split range is requested | Do not invoke Core Data Loader or substitute another row |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or protected identifiers |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UNION.ROUTE | decision | 9 | execution_gate | read->UNION.DONE;create_or_edit_or_delete_ready->UNION.LOADER_READY;mutation_blocked->UNION.ERROR | UNION.DESIGN | stop | Select read completion or the Core Data Loader handoff |
| UNION.ERROR | step | 10 | error_handler | stopped->UNION.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, first-row, blocked, failed, partial, timed-out, uncertain, stale, unverified, or unsupported |
| UNION.DONE | terminal | 11 | terminal | none | UNION.ROUTE | continue | Read completed |
| UNION.LOADER_READY | terminal | 12 | terminal | none | UNION.ROUTE | continue | Mutation rules passed; return UNION.LOADER_READY to the task skill |
| UNION.BLOCKED | terminal | 13 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
