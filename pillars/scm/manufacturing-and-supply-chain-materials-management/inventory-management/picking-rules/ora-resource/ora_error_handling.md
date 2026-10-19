# Picking Rules Error Handling

## Source Evidence

| Source | Used For |
|---|---|
| Redwood Picking Rules priority LOV chains | Priority lookup failures and excluded selected values |
| Redwood rules-page.js payload builder | Supported checkbox values map to canonical true or false strings before submission when included by the UI |
| User approval | AllocateLPNFlag and LPNLocationOnlyFlag are normalized when supplied, with no Advanced Inventory REST verification |
| Developer-provided Data Loader registration and visibility record | Governed business-object route and availability baseline |

## Error Situations

| Situation | What Should Happen |
|---|---|
| A priority display Meaning has no exact match, multiple exact matches, or conflicts with a supplied LookupCode | Stop before Data Loader handoff and identify the affected priority field and supplied value |
| A priority value duplicates another selected priority code | Stop before Data Loader handoff and request a distinct priority value |
| A supported boolean flag has an unsupported or conflicting local representation | Stop before Data Loader handoff and identify the supplied value and accepted REST checkbox/canonical or FSM `Y`/`N` representation |
| FSM `ShelfDays` is not a whole number | Correct the field to a whole-number value and restart FSM archive validation; Data Loader and Fusion remain the final type validators |
| No eligible Picking Rules FSM template is available | Stop before package authoring; reuse a verified project-local template or obtain one through the approved task-level template/spec export workflow |
| An FSM template has the wrong task, target, release, metadata marker, member/header shape, or contains data rows | Stop before package authoring; do not repair metadata, flatten CSVs, or use the package as an authoring carrier |
| Data Loader metadata for inventoryPickingRules is unavailable in a future environment | Stop and report the BO registration and failed metadata retrieval; do not fall back to direct REST write guidance |
| Data Loader rejects a prepared row | Preserve Data Loader status, row identity, failure class, and sanitized message; Data Loader and Fusion own backend validation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Reference lookup | A priority display value cannot resolve exactly once or conflicts with a supplied code | Provide one permitted exact priority Meaning or canonical LookupCode |
| Priority context | A priority code duplicates another priority | Correct the priority values |
| Input normalization | A supported boolean field is not a selected checkbox token, an empty checkbox selection, true, false, `Y`, or `N`, or has conflicting representations | Provide one accepted representation |
| FSM template contract | No verified empty template exists or its provenance, structure, or empty-row checks fail | Reuse an eligible template or request the routed template/spec export |
| Data Loader availability | Business-object metadata is unavailable | Verify registration and environment access before retrying |
| Data Loader validation | Data Loader or Fusion rejects prepared data | Correct the source data using the reported diagnostic |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup failure | Affected priority field, supplied value, exact-match result, and required correction |
| Boolean normalization failure | Supplied representation, accepted representations, and the required correction |
| REST Data Loader handoff | Task code, task name, business object inventoryPickingRules, resolved priority codes when applicable, and metadata visibility status |
| FSM Data Loader handoff | Task code, task name, verified template receipt result, and immutable FSM package identity |
| Data Loader failure | Data Loader request or process identifier when available, failed row identity, sanitized message, stage, and recommended next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Priority lookup has zero, multiple, excluded, or conflicting results | Do not fuzzy-match, guess, or choose a priority value |
| A supported boolean representation is unsupported or conflicting | Do not infer a boolean state or overwrite a supplied canonical value |
| Data Loader metadata is unavailable | Do not create direct REST POST, PATCH, or DELETE guidance as a fallback |
| FSM template validation fails | Do not manufacture metadata XML, create a loose-CSV ZIP, or use a populated current-data export as the authoring template |
| A retry follows an uncertain Data Loader failure | Do not resubmit until Data Loader status and read-only verification clarify the outcome |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PICKRULES.REST_DATALOADER_HANDOFF | terminal | 50 | terminal | none | PICKRULES.RESOLVE_PRIORITY | continue | Classified REST validation, dependency readiness, and priority resolution passed; hand off the REST source to core.data-loader for its normal approval and import workflow. |
| PICKRULES.FSM_DATALOADER_HANDOFF | terminal | 51 | terminal | none | PICKRULES.CHECK_FSM_READINESS | continue | Classified FSM archive and template readiness passed; hand off the unchanged FSM ZIP to core.data-loader for its normal approval and import workflow. |
| PICKRULES.RETURN_ISSUES | terminal | 90 | terminal | none | none | continue | Any route classification, input, lookup, dependency, template, or Data Loader handoff prerequisite is blocked or fails. |
