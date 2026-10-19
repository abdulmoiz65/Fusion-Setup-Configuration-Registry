# Picking Rule Assignments Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Item Type, Date Type, or Transaction Action resolves to zero or multiple standard-lookup rows | Stop before Data Loader handoff; show the supplied value, lookup type, resolver, match count, and required correction. |
| Friendly and canonical variants resolve to different lookup rows | Stop before Data Loader handoff and request one matching authoritative value. |
| A BO foreign-key value cannot be resolved | Preserve the Data Loader diagnostic and identify the target foreign-key attribute and supplied friendly input; do not create a local duplicate resolver. |
| BO metadata is unavailable or unpublished | Stop and report a Data Loader availability issue; do not fall back to direct REST write guidance. |
| Multiple exported FSM criterion rows match the requested `(ORA_INV_RULE.RuleName, SequenceNumber)` | Stop before Data Loader validation and obtain a corrected current `ORA_PICKING_RULE_ASSIGNMENTS` export. Do not select one row arbitrarily. |
| An FSM archive has missing/changed metadata, CSV members, headers, or malformed CSV | Stop before Data Loader validation; obtain a new current task export. Do not repair metadata or create a loose-CSV archive. |
| Script-free package authoring cannot preserve the source member set, non-target bytes, CSV encoding, or ZIP readability | Stop before Data Loader validation; retain the source export unchanged and report the package-authoring failure. Do not substitute a loose CSV or persist a task-local builder script. |
| Data Loader rejects a prepared row | Preserve Data Loader status, row identity, failure class, and sanitized message; Data Loader and Fusion own final validation. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Lookup readiness | Standard lookup is unavailable, not found, ambiguous, or conflicting. | Correct the exact standard-lookup Meaning or canonical value. |
| BO foreign-key resolution | A registered BO name-to-ID/code resolution fails. | Correct the friendly input or BO metadata based on the returned diagnostic. |
| Data Loader availability | BO metadata is not visible. | Publish/update BO metadata and validate the generated sample before retrying. |
| FSM package validation | Criterion-row merge, replacement-target identity, or export-package integrity fails. | Correct the package from a current task export and restart validation. |
| Data Loader validation | Data Loader or Fusion rejects prepared data. | Correct source data using the returned diagnostic. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Standard-lookup failure | Supplied friendly/canonical value, resolver, lookup type, request path, match count, and correction needed. |
| BO foreign-key failure | Target ID/code attribute, supplied friendly attribute, sanitized Data Loader message, and correction needed. |
| Data Loader handoff | Task code, task name, BO discriminator, and normalized standard-lookup values when applicable. |
| FSM Data Loader handoff | Task code, task name, verified export receipt, target environment/release compatibility result, and immutable FSM ZIP identity/fingerprint. |
| Data Loader failure | Data Loader request/process identifier when available, failed row identity, sanitized message, stage, and recommended next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Standard lookup is ambiguous | Do not choose the first candidate, fuzzy-match, or use contains matching. |
| BO foreign-key resolution fails | Do not bypass the BO with a task-local ID lookup or direct REST write. |
| BO metadata is unavailable | Do not use task-local REST POST or PATCH guidance as a fallback. |
| FSM archive validation fails | Do not manufacture metadata XML, create a loose-CSV ZIP, or use REST-derived attributes to construct a parent carrier. |
| Data Loader outcome is uncertain | Do not resubmit until status and read-only verification clarify the outcome. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PRA.DATA_LOADER_HANDOFF | decision | 60 | execution_gate | ready->PRA.DONE;blocked->PRA.HANDLE_ERROR;failure->PRA.HANDLE_ERROR | PRA.CHECK_READINESS | stop | Before handing normalized data to `core.data-loader`. |
| PRA.FSM_DATALOADER_HANDOFF | terminal | 61 | terminal | none | PRA.CHECK_FSM_READINESS | continue | Classified FSM archive passed native validation and readiness; hand off the unchanged ZIP to `core.data-loader` for its approval and import workflow. |
| PRA.HANDLE_ERROR | step | 70 | error_handler | handled->PRA.RETURN_ISSUES | none | stop | Any local lookup, readiness, BO, or Data Loader issue. |
| PRA.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | A blocking issue was classified and disclosed. |
| PRA.DONE | terminal | 90 | terminal | none | PRA.DATA_LOADER_HANDOFF | stop | Local task rules passed and Data Loader owns final validation and execution. |
