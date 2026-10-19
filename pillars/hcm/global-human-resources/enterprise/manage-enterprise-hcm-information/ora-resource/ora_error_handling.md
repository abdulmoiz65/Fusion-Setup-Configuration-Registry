# Manage Enterprise HCM Information Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| ENT-01 | The Enterprise REST response contains no row effective on the requested date | Input validation | Stop and request a corrected effective date |
| ENT-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| ENT-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| ENT-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| ENT-02 | Read returns zero or multiple Enterprise targets | Input validation | Stop and report the unresolved live Enterprise; do not request a name or identifier |
| ENT-03 | Core Data Loader reports that current metadata is unavailable or stale | Catalog mismatch | Stop and follow the Core Data Loader correction |
| ENT-03A | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| ENT-04 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| ENT-04A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected Enterprise information |
| ENT-04B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| ENT-04C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| ENT-05 | A context link or value-set match is missing or ambiguous | Input validation | Stop and request one precise context, segment, or value |
| ENT-05A | An all-context read finds an ambiguous describe context code or more than one matching live child link | Input validation | Stop without selecting a context; request a precise context or correct the deployed metadata |
| ENT-06 | An OrgInformation EFF segment lacks its flexfield code or EFF category | Catalog mismatch | Stop before preview and rebuild the source with the resolved EFF controls |
| ENT-07 | An OrgInformation EFF row lacks its resolved row identity or ENTERPRISE classification parent, including a `childLogicalFusionRows` null failure | Catalog mismatch | Stop before preview and resolve the context row and enterpriseEFF envelope without guessing or reusing stale IDs |
| ENT-08 | A configured multirow EFF unique-key segment is missing or duplicated | Input validation | Stop and correct the multirow EFF identity |
| ENT-09 | Delete targets the first date-effective row | Input validation | State that the first date-effective record cannot be deleted this way |
| ENT-09A | Post-delete history differs from the confirmed row removal and preceding-boundary change | Process failed | Stop without retry and report failed verification |
| ENT-09B | The history request fails | Fusion API | Report the actual REST failure and stop; do not describe history as incomplete |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Effective context, target, context, segment, or value is missing or ambiguous | Correct the input and restart resolution |
| Catalog mismatch | EFF controls or classification-parent evidence is missing or stale | Refresh the Enterprise EFF contract and rebuild the source |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Fusion API | Fusion rejects the declared history request | Report the sanitized response and correct the request before retry |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain current approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile Enterprise state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| EFF contract failure | Context, segment, missing control category, and required resolver stage without exposing classification IDs |
| All-context read | Context titles and safe business values returned from live child links; identify a context with no returned child link as `No current context row` |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Enterprise EFF rows without assuming rollback |
| Delete eligibility | Enterprise basic details and effective period only; never show FirstSplitFlag or internal identifiers |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not switch to another mutation route |
| Preview, approval, metadata, or source bytes changed | Do not reuse the earlier approval |
| EFF control or classification parent is unresolved | Do not guess or reuse a stale classification ID |
| Complete delete, ZAP, or first-row delete is requested | Do not invoke Core Data Loader or substitute another row |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or protected identifiers |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ENT.ROUTE | decision | 11 | execution_gate | read->ENT.DONE;edit_or_delete_ready->ENT.LOADER_READY;mutation_blocked->ENT.ERROR | ENT.DESIGN | stop | Select read completion or the Core Data Loader handoff |
| ENT.ERROR | step | 12 | error_handler | stopped->ENT.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, first-row, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| ENT.DONE | terminal | 13 | terminal | none | ENT.ROUTE | continue | Read completed |
| ENT.LOADER_READY | terminal | 14 | terminal | none | ENT.ROUTE | continue | Edit or eligible delete rules passed; invoke core.data-loader and follow it through immutable ZIP preview |
| ENT.BLOCKED | terminal | 15 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
