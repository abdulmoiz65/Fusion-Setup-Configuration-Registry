# Absence Categories Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| An end-date load omitted resolved parent fields | Compare the exact DAT with the parent end-date source contract in ora_input_validation.md. Rebuild from live resolved values and obtain fresh immutable approval. Retaining Name, LegislationCode, and Status matches the observed successful payload; do not claim which omitted field caused a prior error without a server trace. If the complete parent-only load still fails, retain the actual diagnostic and investigate HDL/Fusion rather than adding child changes. |
| A parent-only end-date load fails with a child effective-date constraint | Preserve the actual Fusion diagnostic and classify the failure as an unresolved HDL/Fusion dependency-handling issue. Do not generate child association updates, inactivate associations, end-date an actual absence type, or retry automatically. Reconcile current state and require a fresh immutable parent-only preview and approval for a requested retry. Delegating association handling to HDL is the workflow boundary, not proof that server-side cascading succeeded. |
| Required input is missing or invalid | Identify the exact field and stop before Data Loader preparation |
| Status, legislation, or associated-type lookup returns no match or multiple matches | Show the supplied value and resolver classification, then request one precise value |
| An associated type does not match legislation or is not effective on the resolved association start date | Stop and request a compatible existing absence type or corrected legislation and date |
| A date-effective mapping is missing or caller-authored | Identify the requested operation and required effective date; derive the matching effectiveOf or stop |
| The final immutable DAT omits derived effectiveOf on an included parent or child/DFF row | Classify as input validation; identify the section and block preview, approval, upload, and initiation until the archive is rebuilt. An absent parent row is valid for flex-only correction. |
| A non-create identity is absent or ambiguous | Resolve one exact selected effective-dated category identity before DAT preparation |
| A category view has no matches | Return an empty filtered view and state the applied filters; do not select or mutate a category |
| A selected category needs associations or history | Route a read-only task-level export and stop if the export cannot provide the selected identity and its effective-dated association evidence |
| A create omits the category effective start date | Present the current system date only as a proposed default and stop until the consultant confirms it or supplies another date |
| An association is duplicate, overlapping, ineffective, incompatible, inactive, end-dated, or inaccessible | Identify the type and association date, retain the category-history evidence, and stop before source preparation |
| A deletion has dependencies or Fusion rejects it | Relay the application-provided constraint without paraphrasing it as permission; do not retry or substitute a different delete action |
| A policy-to-category proposal has unresolved decisions | Return the unresolved decisions and owners; do not imply statutory, pay, eligibility, or reporting behavior that the requester did not supply or confirm |
| The registered template lacks effectiveOf for a selected section | Stop before archive preparation; do not use REST describe or invent a DAT column |
| DELETE scope is ambiguous or ZAP intent is absent | Require explicit DELETE_CHANGES or explicit destructive ZAP intent; retain the normal immutable Data Loader approval gate |
| Describe or flexfield metadata is unavailable or stale | Stop and require a current target-environment absenceCategories describe response |
| Fusion returns Not Found for a DDF or DFF PATCH after the parent AbsenceCategoryId resolved | Retrieve the failed child details and read back parent/child state. Check ID, both child date fields, requested effectiveOf, and parent-before-child ordering against the exact archive. A 404 alone does not prove a missing separate surrogate. Prepare a corrected source from the evidence and use the normal immutable approval cycle; do not replay an uncertain write. |
| A flex source omits EffectiveEndDate or conflates an existing slice with a planned update slice | Classify as input validation. Recover the existing range through the flex resolver, preserve its end date, and derive correction versus update dates before rebuilding the source. |
| RestAction is MERGE | Classify as input validation. MERGE is the DAT record directive; use RestAction=PATCH for correction or update. |
| Language was supplied or defaulted | Remove it and rerun validation because Fusion derives Language from login context |
| EffectiveEndDate was client-defaulted | Remove an invented default. Retain an explicitly supplied end date or the observed existing child end date required for DDF/DFF maintenance identity. |
| Fusion returns HTTP 401 or 403 for a read-only lookup | Classify authentication or authorization failure; refresh a rejected cached token at most once for the read operation |
| Fusion returns a 400-series contract or business-rule response | Preserve redacted Fusion error detail, classify the failed stage, and stop |
| A non-idempotent operation has an uncertain or failed result | Do not replay it automatically; reconcile through the approved core.data-loader workflow and safe reads |
| An association child reports Not Found | Inspect the actual child diagnostic, final DAT, resolved parent ID and dated child collection. A blank User Key does not prove a missing AbsenceCategoryId: the association registration has empty ObjectUserKeys, ParentId AbsenceCategoryId and its own SurrogateId AbsenceTypeCateId. Do not invent a missing key or attribute the failure to RangeMode without a supporting request trace. |
| The parent update succeeded but the new association failed | Preserve the successful category slice. Reconcile the old and requested associations and flex values; prepare only the missing association if it is still absent. Use the create mapping from ora_defaulting_rules.md and a fresh immutable approval. Do not replay the successful parent UPDATE. |
| Aggregate counts show loaded records but a child diagnostic exists | Report partial failure, not success. Verify the requested child and preserved values by effective-dated readback regardless of aggregate failed count. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required fields, date shape, length, non-writable-field, Language, or EffectiveEndDate defaulting checks fail | Correct the identified input and rerun validation |
| Lookup resolution | Status, territory, or associated type does not resolve exactly once | Supply a precise supported code, display value, or existing type identity |
| Dependency mismatch | Associated type legislation or effective range does not match the category | Select a compatible type or correct the category legislation or start date |
| Metadata validation | Current absenceCategories describe cannot validate the supplied flexfield source | Refresh metadata in the target environment and retry validation |
| Flexfield loader identity or effective-date failure | Fusion rejects a registered DDF/DFF PATCH despite a resolved parent | Diagnose the failed row's category ID, start/end dates, operation, effectiveOf and exact server error. If complete source still fails, inspect Fusion's generated child URL or loader resolver; report that unresolved server behavior without declaring all flex updates unsupported. |
| Authentication or authorization | A read-only lookup returns 401 or 403 | Correct access or refresh an eligible cached token once; do not retry a mutation |
| Fusion contract or business rule | Fusion returns a redacted 400-series contract or business failure | Correct the contract or business data before a fresh approved attempt |
| Approval blocker | A mutation lacks an exact core.data-loader preview and explicit approval | Stop and complete the Data Loader approval workflow |
| Template contract | The registered UCM DAT template is unavailable, mismatched, or lacks effectiveOf for an included date-effective section | Refresh the template or remove the unsupported section; do not infer support from REST describe |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation failure | Field, supplied value when safe, violated rule, and one corrective action |
| Lookup failure | Resolver, requested identity, zero or multiple match classification, and requested correction |
| Dependency failure | Associated type identity, category legislation and start date, failed compatibility rule, and correction needed |
| Metadata failure | Target environment, resource absenceCategories, failed metadata stage, and safe next action |
| Data Loader handoff | Exact task and BusinessObject absenceCategories, validated values, omitted server-owned fields, unresolved items, target environment, and required approval state |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A direct POST, PATCH, DELETE, or upsert is requested from this resource package | Do not execute or author a direct REST mutation; route it through core.data-loader in REST mode |
| A lookup is ambiguous | Do not choose the first row or infer a code |
| Language is absent | Do not create a default; Fusion derives it from login context |
| EffectiveEndDate is absent | Do not create a default. For DDF/DFF maintenance, resolve and retain the existing child end date; omit ordinary parent end dates unless supplied. |
| Flexfield metadata is stale or missing | Do not reuse captured tenant-specific contexts or segments as authoritative |
| A prior mutation result is uncertain | Do not retry automatically or claim success |
| A date-effective operation is requested | Do not accept a free-form effectiveOf value or default a non-create date/range |
| A Task Hook preview for a date-effective archive relies on caller-provided ruleResults | Do not treat the declared rule results as proof; inspect the final immutable DAT member and rebuild the preview if it omits effectiveOf |
| A registered DDF or DFF correction or update uses AbsenceCategoryId as both surrogate and parent ID | Do not demand an invented separate ID or prohibit flex maintenance merely because a previous incomplete source failed. Validate the registered identity and both date fields, prepare the requested change and report the actual load result. |
| DELETE is requested | Do not infer DELETE_CHANGES versus ZAP, and do not execute ZAP without explicit destructive intent and immutable Data Loader approval |
| Credentials or bearer tokens appear in evidence | Do not persist or disclose them |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AC.READINESS_GATE | decision | 120 | execution_gate | ready->AC.DONE_VALIDATED;blocked->AC.HANDLE_ISSUE | AC.ENFORCE_DESIGN | stop | Before handing validated setup data to core.data-loader |
| AC.HANDLE_ISSUE | step | 130 | error_handler | handled->AC.RETURN_ISSUES | none | stop | Any input, lookup, dependency, metadata, design, approval, transport, Fusion, process, or persistence error |
| AC.RETURN_ISSUES | terminal | 140 | terminal | none | AC.HANDLE_ISSUE | stop | A blocking issue was classified and disclosed |
| AC.DONE_VALIDATED | terminal | 150 | terminal | none | AC.READINESS_GATE | stop | Absence Categories data is validated and ready for the separate core.data-loader workflow |
