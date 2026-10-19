# Manage Positions Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| POS-01 | The positionsV2 describe or REST response contract is missing or unusable | Catalog mismatch | Stop before resolution and report the unavailable contract; never guess a mapping |
| POS-01A | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed read stage |
| POS-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| POS-01C | A required REST or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| POS-02 | Read, edit, or delete returns zero or multiple exact targets | Input validation | Stop and request one precise business selector |
| POS-02A | A requested child link or polymorphic context is missing | Catalog mismatch | Stop and report the unsupported section or field; never construct a child path |
| POS-02B | A child update or delete resolves to zero or multiple rows | Input validation | Stop and request one complete current child business key |
| POS-02C | An edit row is missing its current parent or child key, or the loader reports You must enter dates without gaps and the dates must not overlap after the calendar dates themselves pass validation | Input validation | Stop before approval; classify every row as existing or new, re-read each existing target, and rebuild it with its exact current key and effective range |
| POS-02D | A Position parent delete does not distinguish zap from effective-split deletion | Input validation | Stop before authoring and require one explicit delete mode; do not infer purge scope |
| POS-02E | Effective-split history is incomplete, the selected row is first or ambiguous, or its predecessor and end boundary cannot be derived exactly | Input validation | Stop before authoring; refresh every PositionHistoryDef page and select one exact non-first split |
| POS-03 | Create finds an exact PositionName or supplied PositionCode match | Input validation | Stop the duplicate create |
| POS-04 | Business Unit, Department, Job, or supplied Location is unresolved, inactive, ambiguous, or out of effective range | Input validation | Stop before workbook authoring and request one exact valid value |
| POS-04A | A supplied Position or child field, lookup, foreign reference, context, or segment is absent from the current contract, unresolved, or ambiguous | Input validation | Stop before source authoring and request one exact supported value or complete business key |
| POS-04B | Delegate Position or Funding Position does not match its supplied Business Unit | Input validation | Stop before approval and resolve the referenced Position and its own Business Unit together |
| POS-04E | DelegatePositionBusinessUnitId or FundingPositionBusinessUnitId is blank, nonnumeric, contains a Business Unit display name, or the loader requests a valid value for that ID attribute | Input validation | Stop before approval; resolve the referenced Position again and place its numeric BusinessUnitId only in the ID field |
| POS-04C | GradeCode and GradeSetCode do not resolve together exactly once on the target date | Input validation | Stop before approval and resolve one complete effective Grade key |
| POS-04D | A context-qualified segment has a blank or mismatched FLEX selector, multiple contexts, an unsupported segment, or the wrong EFF category | Input validation | Stop before approval and rebuild the row from the current flexfield context contract |
| POS-04F | A qualified DFF or EFF segment is present without its matching FLEX declaration in the loader METADATA line, or the loader reports that the flexfield code in an attribute hint was not declared | Input validation | Stop before approval and rebuild the source with the explicit FLEX:FLEX_CODE selector and resolved context value |
| POS-05 | Core Data Loader cannot produce or preserve the reviewed source | Artifact persistence | Stop and follow the Core Data Loader correction |
| POS-05A | Final child dates, evaluation date, parent-child keys, dependency values, or source row counts fail the Position create/copy rules | Input validation | Stop before approval, correct the prepared content or evidence, and rerun every applicable rule |
| POS-05B | The final serialized edit was not reviewed, differs from its evidence, has a missing or misplaced existing-row key, misplaces an ID/display value, omits a required flex declaration or context, or would create an overlapping effective row | Input validation | Stop before preview or approval; re-read current rows and dependencies, rebuild the source, and rerun the complete serialized edit review |
| POS-06 | SourceSystemOwner or SourceSystemId is supplied for a mutation | Input validation | Stop and require a supported business key; never populate or modify either source-system key |
| POS-07 | Core Data Loader reports that current metadata is unavailable or stale | Catalog mismatch | Stop and follow the Core Data Loader correction |
| POS-07A | The immutable preview or approval is missing or stale | Approval blocker | Stop before submission and obtain approval for the current preview |
| POS-08 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| POS-08A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile affected positions |
| POS-08B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| POS-08C | The submission outcome cannot be confirmed | Process failed | Reconcile the affected parent or child through read_position_section_rows before considering any retry |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A target, duplicate check, dependency, effective range, PositionCode, or loader key is invalid | Correct the input and restart resolution |
| Catalog mismatch | The positionsV2 contract is unavailable, or Core Data Loader reports unavailable or stale metadata | Correct the reported contract before continuing |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Artifact persistence | Core Data Loader reports that the reviewed source cannot be produced or preserved | Follow the reported correction |
| Approval blocker | Preview or approval is missing, stale, or bound to changed evidence | Re-preview and obtain current approval |
| Process failed | Loader status is failed, completed with errors, partial, or uncertain | Preserve diagnostics, reconcile Position state, and stop before retry |
| Process timeout | Loader does not reach a terminal status within the allowed wait | Stop polling and retain the process for a later status check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Any failure | Environment, operation, stage, category, sanitized message, and one safe next action |
| Dependency failure | Dependency type, supplied business value, effective-date context, and failure reason without exposing surrogate IDs |
| Section-read failure | Requested section, requested fields, child selector when supplied, and whether the parent link, context, or exact row was unavailable |
| Loader failure or timeout | Process identifier, last status, elapsed wait when relevant, diagnostics, and reconciliation path |
| Partial or uncertain result | Confirmed, failed, and unverified Position or child rows without assuming rollback |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation fails, times out, or is uncertain | Do not retry automatically or assume rollback |
| The declared Data Loader route is unavailable | Do not switch to a REST write or another mutation route |
| Preview, approval, contract, or source bytes changed | Do not reuse the earlier approval |
| Final Position create/copy or serialized edit rule review is incomplete, blocked, or stale | Do not build or approve the Task Hook preview and do not submit |
| A mapping, dependency, loader key, or target is unresolved | Do not infer or invent a value |
| SourceSystemOwner or SourceSystemId is supplied or exists on the target | Do not populate, modify, default, or use either field; omit and preserve existing values |
| A delete is requested | Do not convert it to inactivation or issue a REST write; use the approved core.data-loader delete route |
| A Position zap is requested | Do not use MERGE, include split-range directives, or mix DELETE and MERGE for that logical Position in one file |
| A Position effective-split delete is requested | Do not use DELETE, delete the first split, copy the selected row's start as the MERGE start, or proceed without complete PositionHistoryDef evidence |
| Diagnostics are returned | Do not expose tokens, secrets, sensitive values, full payloads, or surrogate IDs |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POS.ROUTE | decision | 13 | execution_gate | read->POS.DONE;create_or_edit_or_delete_ready->POS.LOADER_READY;mutation_blocked->POS.ERROR | POS.DESIGN | stop | Select read completion or the Core Data Loader handoff |
| POS.ERROR | step | 14 | error_handler | stopped->POS.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| POS.DONE | terminal | 15 | terminal | none | POS.ROUTE | continue | Requested positionsV2 sections were read |
| POS.LOADER_READY | terminal | 16 | terminal | none | POS.ROUTE | continue | Create, edit, or delete rules passed; invoke core.data-loader in HDL mode and follow its authoritative preview and approval workflow |
| POS.BLOCKED | terminal | 17 | terminal | none | none | stop | The request cannot safely continue without correction or reconciliation |
