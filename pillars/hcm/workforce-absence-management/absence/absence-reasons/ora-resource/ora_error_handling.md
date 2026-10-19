# Absence Reasons Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required mutation input is missing or invalid | Apply documented create defaults for omitted Status and LegislationCode; identify any remaining required or invalid field and stop before Data Loader preparation. Do not require mutation fields or apply the create US default for AC1 reads |
| AC1 search returns zero or multiple rows | Return the candidate results, including an empty result when appropriate; neither outcome authorizes creation nor constitutes an identity lookup failure |
| AC1 search URL, body, response envelope, or pagination is invalid | Classify the contract or environment failure and stop the affected read. Retain already verified pages as partial, disclose the failed stage and next action, and do not claim a complete count or switch execution routes |
| AC1 selected details cannot be read for the selected dated row | Keep the verified search columns and disclose the unavailable detail and date context. Missing Description is not an empty Description, and a different dated row is not a substitute |
| Status or legislation lookup returns no match or multiple matches | Show the supplied or defaulted value and resolver classification, then request one precise value |
| Exact reason lookup finds more than one current matching reason | Stop the association workflow and request one precise reason identity; do not select the first row |
| Exact reason lookup finds no matching reason | Create a reason only when find-or-create was explicitly requested and all Absence Reasons create requirements are satisfied; otherwise return not found without a mutation |
| A reason load was initiated for a dependent absence type | Do not prepare the Absence Types archive until the reason load status is successful; failed, timed-out, or unavailable status blocks the downstream task |
| Describe or DFF metadata is unavailable or stale | Stop and require a current target-environment describe response |
| The registered Data Loader template is unavailable or does not expose effectiveOf for an included section | Stop before DAT preparation; do not infer the column from REST describe or a reduced sample |
| effectiveOf is absent, malformed, or inconsistent with the requested operation | Preserve the selected operation, safe date values, and validation issue; require correction before preview |
| A final DAT uses `YYYY/MM/DD` for an Absence Reasons physical effective date | Classify as input validation; rebuild the parent or flexfield row with `YYYY-MM-DD` before a new preview and approval |
| Fusion reports an orphan REST flex child or a missing PARENT key | Classify as a payload-contract failure; add an `absenceReasons` parent `MERGE` with the same resolved `AbsenceReasonId` and matching `effectiveOf`. A parent `METADATA` header alone is not sufficient |
| AbsenceReasonsFlex or AbsenceReasonsDDFFlex returns Not Found for PATCH | Classify as a flex-target identity failure, not a field-value failure. Stop without replay, read the exact parent effective slice and returned child collection, and select PATCH only if one exact child now exists. Select POST only for a missing child under an already-committed parent slice |
| A load creates the parent effective slice but its flex child fails | Classify the request as a partial failure even if aggregate row counts show loaded records. Preserve the parent side effect, re-read both effective-dated records, and require a new archive, preview, and approval for the child retry |
| A requested flex update also needs a new parent effective slice | Prepare a parent-only archive first. Do not include a child PATCH until the parent load succeeds and resolve_absence_reason_flex_item returns one exact child; if it returns no child under the committed parent, prepare child POST instead |
| The final immutable DAT omits derived effectiveOf on the parent or an included flexfield row | Classify as input validation; identify the section and block preview, approval, upload, and initiation until the archive is rebuilt |
| Delete scope is ambiguous or ZAP is not explicitly approved | Stop; require DELETE_CHANGES or ZAP selection, and bind ZAP to the immutable Data Loader approval preview |
| Fusion returns HTTP 401 or 403 for a read-only lookup | Classify authentication or authorization failure; refresh a rejected cached token at most once for the read operation |
| Fusion returns a 400-series contract or business-rule response | Preserve the redacted Fusion error detail, classify the failed stage, and stop |
| A non-idempotent operation has an uncertain or failed result | Do not replay it automatically; reconcile through the approved Data Loader workflow and safe reads |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required fields, shape, type, length, or non-writable-field checks fail | Correct the identified input and rerun validation |
| Lookup resolution | Status or legislation does not resolve exactly once | Supply a precise supported code or display value |
| Metadata validation | Current absenceReasons describe or DFF metadata cannot validate the source | Refresh metadata in the target environment and retry validation |
| Effective-date validation | effectiveOf, operation, date, range, or included flexfield values are missing or inconsistent | Correct the selected operation or date values and rebuild effectiveOf before a fresh validation |
| Authentication or authorization | A read-only lookup returns 401 or 403 | Correct access or refresh an eligible cached token once; do not retry a mutation |
| Fusion contract or business rule | Fusion returns a redacted 400-series contract or business failure | Correct the contract or business data before a fresh approved attempt |
| Approval blocker | A mutation lacks an exact Data Loader preview and explicit approval | Stop and complete the Data Loader approval workflow |
| Dependent process failed | A reason needed by an absence type failed to load or cannot be verified | Preserve the reason request ID and diagnostics, correct the reason, and obtain a new approval before preparing the type |
| Flex target identity | The exact effective-dated child is missing, ambiguous, mismatched, or was addressed with the wrong POST/PATCH action | Reconcile the parent and child through returned links, derive the child action from existence, and rebuild a new approved archive |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| AC1 result | Name, Legislation, Status, Effective Start Date, Effective End Date, and verified Description for a selected detail result when requested/applicable; disclosed search context, blank cells for actual nulls, and any incompleteness warning. Do not expose pagination internals or label filtered results as all system records |
| Validation failure | Field, supplied value when safe, violated rule, and one corrective action |
| Lookup failure | Resolver, requested identity, zero or multiple match classification, and requested correction |
| Metadata failure | Target environment, resource absenceReasons, failed metadata stage, and safe next action |
| Effective-date failure | Requested operation, safe date/range values, included sections, failed effectiveOf rule, and required correction |
| Data Loader handoff | Exact task and BusinessObject absenceReasons, validated values, defaults applied, unresolved items, target environment, and required approval state |
| Reason handoff | Exact reason name, match classification, resolved reason reference when found, or the separately approved reason-load status when created |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A direct POST, PATCH, DELETE, or upsert mutation is requested from this resource package | Do not execute or author a direct REST mutation; route the request through core.data-loader. Only the exact search-only POST defined by search_absence_reasons_advanced is permitted as an AC1 read, with its verified target, allowlisted body and no mutation headers |
| A lookup is ambiguous | Do not choose the first row or infer a code |
| DFF metadata is stale or missing | Do not reuse captured pod-specific segments as authoritative |
| A prior mutation result is uncertain | Do not retry automatically or claim success |
| A flex PATCH returned Not Found or a prior load partially changed the parent | Do not replay the same archive, change PATCH to POST without an exact child lookup, or treat loaded row counts as overall success |
| A reason is absent | Do not create it without explicit find-or-create intent and a separate Data Loader approval |
| A Task Hook preview for a date-effective archive relies on caller-provided ruleResults | Do not treat the declared rule results as proof; inspect the final immutable DAT member and rebuild the preview if it omits effectiveOf |
| Credentials or bearer tokens appear in evidence | Do not persist or disclose them |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AR.READINESS_GATE | decision | 100 | execution_gate | ready->AR.DONE_VALIDATED;blocked->AR.HANDLE_ISSUE | AR.ENFORCE_DESIGN | stop | Before handing validated setup data to core.data-loader |
| AR.HANDLE_ISSUE | step | 110 | error_handler | handled->AR.RETURN_ISSUES | none | stop | Any input, lookup, metadata, design, approval, or Fusion error |
| AR.REASON_FOUND | terminal | 120 | terminal | none | AR.LOOKUP_REASON | stop | One exact current reason was found and is ready for the Absence Types handoff |
| AR.RETURN_VIEW_RESULTS | terminal | 125 | terminal | none | AR.SEARCH_REASONS | stop | AC1 search or selected-detail results are ready, including zero results or an explicitly disclosed detail limitation; no defaults for mutation, DAT/ZIP, Data Loader template, load approval, or load submission follows |
| AR.RETURN_ISSUES | terminal | 130 | terminal | none | AR.HANDLE_ISSUE | stop | A blocking issue was classified and disclosed |
| AR.DONE_VALIDATED | terminal | 140 | terminal | none | AR.READINESS_GATE | stop | Absence Reasons data is validated and ready for the separate core.data-loader workflow |
