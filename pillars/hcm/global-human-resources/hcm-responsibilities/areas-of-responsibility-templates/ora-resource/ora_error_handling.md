# Areas of Responsibility Templates Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| AORT-01 | The AOR Template REST read contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| AORT-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| AORT-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| AORT-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| AORT-02 | Read, edit, or delete returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| AORT-03 | Create finds an exact existing TemplateCode | Input validation | Stop the duplicate create; an existing TemplateName alone is permitted |
| AORT-04 | No registered Core Data Loader business object supports the requested mutation | Catalog mismatch | Stop and report the unsupported operation without substituting a REST write |
| AORT-05 | A mutation has no reviewed XLSX source | Artifact persistence | Stop before DAT or ZIP generation and rebuild the source |
| AORT-06 | Source keys are partial or lack explicit supported provenance | Input validation | Stop and require complete supported key provenance |
| AORT-07 | The immutable Data Loader preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| AORT-08 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| AORT-08A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected template rows |
| AORT-08B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| AORT-08C | The completed initiation command returns no Content ID or Request ID | Process failed | Reconcile through the authorized read before considering any retry. An active command session or empty incremental command response is not a completed initiation outcome: retain and poll that same session first. |
| AORT-08D | Fusion returns the known security-related AOR import message while one or more rows are loaded, no rows have failed, and no terminal failure status is returned | Warning | Retain the sanitized message, continue status polling, and do not request source correction solely because of this warning |
| AORT-09 | A template code, lookup, Job, Location, worker assignment, or effective row has zero or multiple compatible matches | Input validation | Stop and request one exact selector; never select by position |
| AORT-10 | Source contains an ID, audit value, link, generated value, read-only meaning, or unknown multi-value encoding | Catalog mismatch | Stop and rebuild a registered-object-supported source shape |
| AORT-11 | TemplateCriteria reports that MERGE has no unique reference | Fusion API | Put TemplateCode, resolved CriteriaAttributeName, and its matching value field in the same row, then rebuild and reapprove the complete workbook |
| AORT-12 | The load reports that no responsibility scope item was provided | Fusion API | Preserve the failed AttributeName and its scope row. Do not retry a blank scope encoding until the exact AttributeName has a proven AORTemplate loader contract; do not infer that support from schema validation or another scope attribute. Then rebuild and require new approval. |
| AORT-13 | The load reports an invalid `{ATTR_VALUE}` for `{ATTR_NAME}` in a lookup list | Fusion API | Stop; identify the failed Scope or Criteria row, re-resolve its value against the declared backing list, correct only the mapped source field, rebuild the archive, and require a new approval. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, reference, effective row, or source key is invalid or ambiguous | Correct the selector and restart resolution |
| Catalog mismatch | The loader object or source shape differs from the registered AORTemplate contract | Correct the source from the current contract |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Fusion API | Fusion rejects TemplateCriteria identity or TemplateScope content | Rebuild the exact rejected parent and child source rows |
| Artifact persistence | The reviewed XLSX or immutable artifact is unavailable | Rebuild and preserve the complete source artifact |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain new approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile current state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |
| Warning | A known informational diagnostic accompanies loaded rows with no failures and no terminal failure status | Retain the diagnostic, continue polling, and report success only after a terminal success status |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| TemplateCriteria rejection | TemplateCode, CriteriaAttributeName, required matching value field, and rejected row identity |
| TemplateScope rejection | AttributeName, required matching scope field, and affected parent and child row identities |
| Approval preview | Per-row Scope and Criteria Mapping: requested value, resolver and backing list, exact matched display value, stored key, and final source column/value |
| Partial or uncertain result | Confirmed, failed, and unverified template, criteria, scope, or representative rows without assuming rollback |
| Informational loader warning | Current status, loaded and failed counts, sanitized warning, and the fact that terminal success is still pending |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not substitute a REST write, FSM CSV, direct API batch, or another route |
| Preview, approval, metadata, or source bytes changed | Do not reuse the earlier approval |
| A target, reference, row identity, or encoding is unresolved | Do not select by position, invent an ID, or guess a source shape |
| Diagnostics are returned | Do not expose credentials, runtime links, raw payloads, transient IDs, audit values, or sensitive data |
| A known informational warning accompanies loaded rows with no failures | Do not direct source correction or retry solely because of that warning |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AORT.ROUTE | decision | 7 | execution_gate | read->AORT.DONE;create_or_edit_or_delete_ready->AORT.LOADER_READY;mutation_blocked->AORT.ERROR | AORT.ENFORCE | stop | Select read completion or the Core Data Loader handoff |
| AORT.ERROR | step | 8 | error_handler | stopped->AORT.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| AORT.DONE | terminal | 9 | terminal | none | AORT.ROUTE | continue | Read completed |
| AORT.LOADER_READY | terminal | 10 | terminal | none | AORT.ROUTE | continue | Mutation rules passed; invoke Core Data Loader and follow it through immutable ZIP preview |
| AORT.BLOCKED | terminal | 11 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
