# Configure Seniority Dates Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| SEN-01 | The REST read or describe contract is missing or incompatible | Catalog mismatch | Stop before the read and restore the declared contract |
| SEN-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| SEN-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| SEN-01C | A required REST, describe, or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| SEN-02 | Read, edit, or delete returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| SEN-03 | Create finds an exact existing seniority rule | Input validation | Stop the duplicate create |
| SEN-04 | No registered Core Data Loader business object supports the requested mutation | Catalog mismatch | Stop and report the unsupported operation without substituting a REST write |
| SEN-05 | A mutation has no reviewed XLSX source | Artifact persistence | Stop before DAT or ZIP generation and rebuild the source |
| SEN-06 | Source keys are partial or lack explicit supported provenance | Input validation | Stop and require complete supported key provenance |
| SEN-07 | The immutable Data Loader preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| SEN-08 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| SEN-08A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected seniority rules |
| SEN-08B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| SEN-08C | The submission outcome cannot be confirmed | Process failed | Reconcile through the authorized read before considering any retry |
| SEN-09 | A rule, lookup, worker type, or scope reference has zero or multiple compatible matches | Input validation | Stop and request one exact selector; never select by position |
| SEN-10 | Source contains a technical ID, audit value, link, unsupported field, or unknown multi-value encoding | Catalog mismatch | Stop and rebuild a registered-object-supported source shape |
| SEN-11 | A field required by the current operation-specific create template, including SeniorityVersion when required, has no supported value, authoritative default, or unambiguous metadata | Catalog mismatch | Report the required field and current template evidence; stop before source or preview. Do not block an absent or optional blank field. |
| SEN-12 | A display selector resolves but its Data Loader ID or code target is missing | Catalog mismatch | Stop before preview without sending the REST Select display field as a substitute |
| SEN-13 | Fusion reports an invalid Object, SourceField, or TriggeringFieldType | Fusion API | Refresh describe and tuple evidence, rebuild XLSX, and obtain new approval before one explicitly approved retry |
| SEN-14 | Import reports SourceRefTableName or SourceRef001 through SourceRef010 as unknown for V2 | Catalog mismatch | Remove every unsupported SourceRef column, regenerate from the current operation template, validate, and reapprove |
| SEN-15 | Country was omitted by the user | Input validation | Keep LegislationCode blank without copying another reference's Country |
| SEN-16 | A displayed SeniorityDateCode, TriggeringField, LevelCode, Cumulative, or AllowEdit value has zero or multiple current exact lookup matches | Input validation | Report the affected rule and unresolved or ambiguous display value; do not infer, generate, or partially match a meaning. |
| SEN-17 | Create intake omits a business-controlled value or explicit scope choice | Input validation | Ask once for every missing create value; do not prepare a partial source. |
| SEN-18 | Fresh state, duplicate cardinality, reference, package state, or fingerprint differs from the current preview | Approval blocker | Invalidate approval, refresh the evidence, and generate a new preview. |
| SEN-19 | The required rule-usage evaluation is unavailable or malformed; or existing seniority records use the rule and the requested update is outside Active, Allow Edit, or Display in UI; or deletion is requested | Input validation | Stop. For a blocked delete, state that deletion is not eligible because existing seniority records use the rule; do not create a delete source or preview. For a blocked update, identify the blocked fields and recommend a new rule or disabling the existing rule. Do not derive RecordPresent from the configuration row. |
| SEN-20 | The current delete template does not accept mandatory `RestAction=DELETE`, does not accept primary key `SeniorityDateSetupId`, or does not resolve to one current eligible target | Catalog mismatch | Stop before preview or approval; refresh the registered delete template and target evidence. |
| SEN-21 | Execution completes but a fresh read cannot prove the approved business result or preserved values | Verification failure | Return failed or uncertain, preserve sanitized evidence, and do not replay the mutation. |
| SEN-22 | After complete intake, a named current authoritative metadata source explicitly proves that a supplied create Attribute, Level, Cumulative, or override/time-basis value conflicts with the exact combination | Input validation | Stop before package or preview, identify the authoritative source, and request corrected values. Approval cannot override the proven compatibility failure. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, reference, source key, or user-owned Country value is invalid or ambiguous | Correct the input and restart resolution |
| Catalog mismatch | Loader object, source shape, describe mapping, tuple, or operation template is unavailable or inconsistent | Refresh the current contract and rebuild the source |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Fusion API | Fusion rejects the resolved technical tuple | Refresh tuple evidence and rebuild the source before seeking approval for one retry |
| Artifact persistence | The reviewed XLSX or immutable artifact is unavailable | Rebuild and preserve the complete source artifact |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain new approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile current state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |
| Verification failure | A fresh authorized read cannot prove the requested state or deletion absence | Return FAILED or UNCERTAIN and reconcile through read-only evidence; do not retry |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Blocked delete | Exact rule selector, that existing seniority records use the rule, and that no delete preview was created |
| Eligible delete preview | Exact rule selector, `Existing seniority records using this rule: No`, and `Deletion eligibility: Eligible`; do not expose the internal `RecordPresent` label |
| Update preview | Exact rule selector, usage result, requested fields, and each field's permitted or blocked status |
| Tuple failure | TriggeringField, tuple cardinality, missing or invalid tuple members, and evidence-refresh action |
| Operation-template failure | Unsupported SourceRef columns or missing loader target mapping and required template regeneration |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Seniority Date rows without assuming rollback |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not substitute a REST write, FSM import, CSV omission, or another route |
| Preview, approval, describe evidence, tuple, template, or source bytes changed | Do not reuse the earlier approval |
| A resolver returns zero, blank, or multiple tuple results | Do not select one by position or semantic inference |
| A display selector lacks its loader target | Do not send the REST Select display field as a substitute |
| Country is omitted | Do not copy Country or LegislationCode from another reference |
| Diagnostics are returned | Do not expose credentials, runtime links, raw payloads, transient IDs, audit values, or sensitive data |
| Approval is absent, negative, conditional, ambiguous, stale, or bound to another preview | Do not execute; create or refresh the exact preview and require a clear standalone approval |
| A current authoritative compatibility source explicitly proves a conflict | Do not generate a package or preview, and do not accept user approval as an override |
| A compatibility source is absent or ambiguous | Do not manufacture an Attribute/Level conflict from a code or lookup display meaning; report compatibility could not be established and continue with the remaining declared validation |
| A registered delete source cannot be built | Do not construct a bodyless REST delete, endpoint, payload, identifier, or alternate transport. |
| A list result is presented | Do not expose row coordinates, reference IDs, SeniorityDateSetupId, links, host URLs, payloads, credentials, or tokens |
| DisplayInUI is presented | Do not claim that UI visibility grants access to worker data; Fusion data-security roles remain a separate control |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SEN.ROUTE | decision | 7 | execution_gate | read->SEN.DONE;create_or_update_or_delete_ready->SEN.LOADER_READY;mutation_blocked->SEN.ERROR | SEN.ENFORCE | stop | For create, update, or delete, require the complete preview, standalone approval, immediate fresh revalidation, one Core Data Loader submission, and fresh verification. A delete source uses `RestAction=DELETE` and fresh primary key `SeniorityDateSetupId`. |
| SEN.ERROR | step | 8 | error_handler | stopped->SEN.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| SEN.DONE | terminal | 9 | terminal | none | SEN.ROUTE | continue | Read completed |
| SEN.LOADER_READY | terminal | 10 | terminal | none | SEN.ROUTE | continue | Create, update, or delete rules passed; invoke Core Data Loader, bind standalone approval to the immutable preview, submit once after revalidation, and reconcile through a fresh current-state read |
| SEN.BLOCKED | terminal | 11 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
