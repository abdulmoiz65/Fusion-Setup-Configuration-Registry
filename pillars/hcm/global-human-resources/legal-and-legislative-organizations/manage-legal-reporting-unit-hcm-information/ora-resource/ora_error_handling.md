# Legal Reporting Unit HCM Information Error Handling

## Purpose

Defines fail-closed handling for declared Fusion reads, synchronization, and
the handoff of classification, EFF, and delete mutations to Core Data Loader.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| LRU-01 | Search returns zero or multiple matches | Input validation | Stop and request one unique valid Name |
| LRU-02 | Neither supported classification is active before a branch read | Input validation | Pause the original flow and ask Should be classified as Tax Reporting Unit? Yes/No and Should be classified as Reporting Establishment? Yes/No. For a view or edit, both No remains blocked; require at least one Yes before preparing ManageLegalReportingUnitHcmClassifications. While those questions are pending, `Both` or `Yes to both` is explicit Yes/Yes: do not ask again, resolve the pre-classification identity, and immediately prepare the classification-only Core Data Loader preview |
| LRU-03 | Valid same-session ManageLegalReportingUnit synchronization evidence is absent or older than 24 hours | Input validation | Return LRU.SYNC_LOADER_READY for the exact fresh LRU; after the approved synchronization-only loader run reaches terminal success, refresh advanced search and resume before classification evaluation. Reuse only same-identity, same-environment evidence from this session within 24 hours |
| LRU-04 | ManageLegalReportingUnit synchronization fails or is uncertain | Input validation | Reconcile through fresh advanced search; do not invoke it again automatically and do not continue to classifications or roots without confirmed synchronized state |
| LRU-05 | ManageLegalReportingUnitHcmClassifications fails or is uncertain | Input validation | Reconcile once through advanced search; continue a pending detail read or edit only when TruStatus and ReStatus match the approved targets, do not replay the classification load automatically, and do not repeat completed synchronization unless its evidence is stale |
| LRU-06 | Applicable root, CategoryCode, describe, or link is missing | Catalog mismatch | Refresh read-only metadata/data once, then stop without guessing |
| LRU-07 | Classified default context collection is empty during View | Input validation | Treat as a valid empty configuration; use the active describe to show the context and supported segments with values Not configured, and do not report a retrieval failure |
| LRU-08 | EffectiveStartDate is missing | Input validation | Show only current Basic details and effective period, request YYYY-MM-DD, and do not show changes, map, or submit |
| LRU-09 | Operation EffectiveStartDate precedes any affected top-level organization's current EffectiveStartDate | Input validation | Request a date valid for every affected organization |
| LRU-10 | Context lookup returns more than one row for a single-row context | Input validation | Stop before preview and report a metadata or data inconsistency |
| LRU-11 | Value-set input does not resolve uniquely after its declared LOV or table-validation contract has been followed | Input validation | Stop and request one current compatible business value; do not pause merely because a table-validated value set has an empty static values collection |
| LRU-12 | Multirow removal lacks one exact row or current loader support | Input validation | Stop without substituting another row or route |
| LRU-13 | DE Delete targets ineligible scope | Input validation | Refuse and do not substitute another date or delete mode |
| LRU-14 | Loader metadata is absent, stale, or incompatible with the selected object or operation | Catalog mismatch | Stop at loader preparation and refresh the registered contract |
| LRU-15 | Classification source omits organizationId, establishmentId, isTRU, isRE, or RestAction POST, or includes ManageLegalReportingUnit | Input validation | Stop before preview and rebuild a classification-only ManageLegalReportingUnitHcmClassifications archive from current identifiers and live metadata |
| LRU-16 | A root header or row omits FLEX:PER_ORGANIZATION_INFORMATION_EFF or EFF_CATEGORY_CODE; the FLEX value is the literal flexfield identifier instead of the row's resolved context code; or a control value is stale | Catalog mismatch | Stop before preview and rebuild every affected root row from current context and category evidence |
| LRU-17 | DAT member, root discriminator, section name, or action-field case is wrong | Catalog mismatch | Stop before preview and rebuild the source for the selected business object |
| LRU-18 | An effectiveOf mode, required parent locator, child identity/date field, or ModifyOrganizationUnitForChildCorrect or SplitOrganizationUnitForEFFUpdate action contract does not match the operation; a child uses the wrong PATCH/POST or `effectiveOf` contract; a new child populates OrgInformationId, EffectiveStartDate, or EffectiveEndDate; action OrgInformationId is populated; or an action is absent from an affected EFF branch | Input validation | Stop before preview, compare the requested operation date with each affected top-level organization's current EffectiveStartDate, and rebuild every operation-specific member from fresh source rows. Existing children require PATCH, the available fresh parent locator set, their current OrgInformationId, and current child dates. A new POST child requires the available fresh parent locator set and blank OrgInformationId, EffectiveStartDate, and EffectiveEndDate. Put the requested date in effectiveOf and the applicable action: a dated-update POST uses `RangeStartDate=YYYY-MM-DD` without RangeMode; correction uses `RangeMode=CORRECTION;RangeStartDate=YYYY-MM-DD`. Keep action dummyId/OrgInformationId blank, use `RestAction=invoke`, and supply the live-template ISO action date and resolved organization identifier fields |
| LRU-19 | Parent-delete source uses an EFF object, omits a required DeleteOrganizationUnitForDTDelete field, contains EFF/root locator fields or action sections, or duplicates the same organization/history-start pair | Catalog mismatch | Stop before preview and rebuild one DeleteOrganizationUnitForDTDelete row from the current OrganizationId and selected complete-history start |
| LRU-20 | Loader source, ZIP, preview, environment, or approval fingerprint changes | Transport/environment | Invalidate approval and rebuild through core.data-loader |
| LRU-21 | Loader process fails or partially succeeds | Process failed | Preserve sanitized process evidence, report every failed object or row, and do not assume atomic success |
| LRU-22 | Loader process times out or is uncertain | Process timeout | Preserve ProcessId and last status, reconcile through declared reads, and do not resubmit automatically |
| LRU-23 | Post-loader verification differs from the approved result | Process failed | Return failed verification and require a rebuilt loader preview before any retry |
| LRU-24 | CSV export or artifact persistence fails | Artifact persistence | Preserve sanitized artifact evidence and stop |
| LRU-25 | organizationsLOV returns zero or multiple distinct OrganizationIds for exact Name and ClassificationCode=HCM_LRU during classification preparation | Catalog mismatch | Stop before preview, preserve the synchronized exact LRU and both classification answers, and report that the pre-classification organization identity is unresolved; do not query inactive TRU or Reporting Establishment roots as a substitute |
| LRU-26 | A clear `Both` or `Yes to both` response to the two pending classification questions is treated as missing input or merely acknowledged | Input validation | Record Tax Reporting Unit=Yes and Reporting Establishment=Yes, do not repeat either question, and continue immediately through LRU.CLASSIFICATION_IDENTITY and LRU.CLASSIFICATION_GATE. This response is not Data Loader submission approval |
| LRU-27 | Authoring treats legitimate date differences between top-level, parent, or existing-child rows as incompatible, puts any child identity/date field on a new POST child, or requires locator fields copied from another EFF object's template | Input validation | Rebuild from fresh rows and the exact selected object's current live template. Preserve every existing child's OrgInformationId and dates, populate each available fresh parent locator, and leave all three child identity/date fields blank for a new POST child; use the requested operation date only in effectiveOf and applicable action fields; do not invent columns or generated REST paths |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Identity, operation, date, context, row, scope, or value is invalid | Correct input and resume at validation |
| Catalog mismatch | Task mode, business objects, classification facts, metadata, CategoryCode, or context contract is unresolved | Refresh authoritative catalog or metadata evidence |
| Authentication | Fusion identity is absent or expired | Refresh cached authentication once; do not replay a mutation |
| Authorization | A required read or Data Loader privilege fails | Correct access and restart the affected preflight |
| Transport/environment | Host, route, timeout, or connection fails | Preserve diagnostics and retry only an eligible read |
| Fusion API | A declared read or synchronization custom method returns an Oracle error | Stop with sanitized Oracle detail |
| Approval blocker | Core Data Loader preview and approval is absent or stale | Resume at the loader approval gate |
| Process failed | Loader process reports failed or partial completion | Preserve status and logs and do not resubmit automatically |
| Process timeout | Loader process does not reach a terminal state in the allowed wait | Preserve ProcessId, last status, elapsed wait, and next-check path |
| Artifact persistence | Immutable loader source, ZIP, run record, or diagnostics cannot be persisted | Stop before submission or success reporting |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Classification needed | LRU Name followed by Should be classified as Tax Reporting Unit? Yes/No and Should be classified as Reporting Establishment? Yes/No |
| Synchronization loader handoff | Safe environment alias, exact LRU, ManageLegalReportingUnit operation, and that this synchronization-only approval does not authorize classification or another mutation |
| Classification loader handoff | Safe environment alias, synchronized exact LRU, both business-facing Yes/No answers, and only ManageLegalReportingUnitHcmClassifications; do not show internal loader field names |
| Missing edit date | Current Name, Status, Effective period, and Legislation followed by YYYY-MM-DD request; no requested/proposed change table |
| Loader handoff | Safe environment alias, applicable business object or objects, operation, business target, effective boundary, and sanitized proposed changes |
| Date-effective delete | Explicit HCM Information row scope, selected effective range, and expected boundary effect |
| Success | Requested business details or verified changes only |
| Failure | Safe environment alias, LRU Name, business stage, and recommended action without technical orchestration |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Ambiguous identity or classification choice | Do not select a branch, classify, read, edit, or delete |
| Missing current identity or localization metadata | Do not guess an identifier, suffix, field, code, or path. For classification, do not require an active TRU or Reporting Establishment root; use only the exact HCM_LRU organizationsLOV resolver |
| Classification mutation | Do not invoke manageLegalReportingUnitHcmClassifications directly; do not omit either flag or include ManageLegalReportingUnit in the ManageLegalReportingUnitHcmClassifications loader archive |
| Synchronization is incomplete or uncertain | Do not read classification roots or build ManageLegalReportingUnitHcmClassifications. Do not repeat ManageLegalReportingUnit automatically; reuse only successful same-session evidence no more than 24 hours old |
| Mutation requested | Do not use a direct REST action, ADF batch, POST, PATCH, PUT, DELETE, setup import, or another fallback executor; do not invoke deleteOrganizationUnitForDTDelete directly |
| Parent mutation | Do not change Name, Status, classification, CategoryCode, or another parent attribute outside the explicit classification route |
| Delete outside supported scope | Do not physically delete the LRU, remove the first or only history row, or remove a single-row EFF context |
| Missing or stale loader approval | Do not submit; Core Data Loader owns the single authoritative approval gate |
| Failed, partial, timed-out, or uncertain loader result | Do not automatically retry or claim success |
| User-facing or persisted output | Do not expose secrets, tokens, raw payloads, internal IDs, opaque links, environment locators, audit data, or protected business values |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRU.SYNC_GATE | decision | 3 | execution_gate | required->LRU.SYNC_LOADER_READY;completed->LRU.CLASSIFICATION_CHECK;failed->LRU.ERROR;uncertain->LRU.ERROR | LRU.SEARCH | stop | One exact fresh LRU is selected and mandatory ManageLegalReportingUnit synchronization readiness must be resolved |
| LRU.SYNC_LOADER_READY | terminal | 4 | terminal | none | LRU.SYNC_GATE | continue | A synchronization-only ManageLegalReportingUnit archive is ready for Core Data Loader; after successful completion, refresh search and resume before classification evaluation |
| LRU.CLASSIFICATION_GATE | decision | 8 | execution_gate | loader_ready->LRU.CLASSIFICATION_LOADER_READY;missing->LRU.ERROR;blocked->LRU.ERROR | LRU.CLASSIFICATION_IDENTITY | stop | A classification change has one organizationsLOV-derived OrganizationId, the advanced-search EstablishmentId, both business-facing Yes/No answers, their internal mapping, and the live ManageLegalReportingUnitHcmClassifications loader contract |
| LRU.CLASSIFICATION_LOADER_READY | terminal | 9 | terminal | none | LRU.CLASSIFICATION_GATE | continue | A classification-only ManageLegalReportingUnitHcmClassifications archive is ready for Core Data Loader; when it is a prerequisite for a pending explicit detail read or edit, poll to terminal status, refresh classification facts, and resume that operation without repeating synchronization unless stale; otherwise return the accepted standalone initiation response |
| LRU.ROUTE | decision | 20 | execution_gate | read_or_export->LRU.DONE;mutation_ready->LRU.LOADER_READY;mutation_blocked->LRU.ERROR | LRU.DESIGN | stop | Select a terminal read result or a Core Data Loader handoff without executing a mutation here |
| LRU.ERROR | step | 21 | error_handler | blocked->LRU.BLOCKED | none | stop | Any validation, synchronization, lookup, classification, metadata, loader-readiness, process, persistence, approval, or verification gate fails |
| LRU.DONE | terminal | 22 | terminal | none | LRU.ROUTE | continue | The requested read or explicit export completes |
| LRU.LOADER_READY | terminal | 23 | terminal | none | LRU.ROUTE | continue | A supported EFF or delete mutation is fully mapped to taxReportingUnitsEFF, reportingEstablishmentsEFF, both EFF objects, or DeleteOrganizationUnitForDTDelete as appropriate and is ready for core.data-loader |
| LRU.BLOCKED | terminal | 24 | terminal | none | none | stop | The request is blocked with sanitized diagnostics and a resume action |
