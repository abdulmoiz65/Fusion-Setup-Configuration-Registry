# Lot Grades Error Handling

## Source Evidence

| Source | Used For |
|---|---|
| Redwood inventory-lot-serial setup lot-grades page | Active checkbox maps to GradeDisabledCode and the UI surfaces REST error details to the user |
| User confirmation and live Data Loader metadata check | Inventory Lot Grades is registered and visible in the configured target environment |

## Error Situations

| Situation | What Should Happen |
|---|---|
| GradeDisabledCode has an unsupported or conflicting local representation | Stop before Data Loader handoff and identify the supplied value and accepted representations |
| Data Loader metadata for Inventory Lot Grades is unavailable in a future environment | Stop and report the BO registration confirmation and failed metadata retrieval; do not fall back to direct REST write guidance |
| Data Loader rejects the prepared row | Preserve Data Loader status, row identity, failure class, and sanitized message; Data Loader and Fusion own backend validation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input normalization | GradeDisabledCode is not active, an empty checkbox selection, N, or Y, or conflicting values are supplied | Provide one accepted representation |
| Data Loader availability | Business-object metadata is unavailable | Verify registration and environment access before retrying |
| Data Loader validation | Data Loader or Fusion rejects prepared data | Correct the source data using the reported diagnostic |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Normalization failure | Supplied representation, accepted representations, and the required correction |
| Data Loader handoff | Task code, task name, business object Inventory Lot Grades, normalized GradeDisabledCode when supplied, and metadata visibility status |
| Data Loader failure | Data Loader request or process identifier when available, failed row identity, sanitized message, stage, and recommended next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Normalization input is unsupported or conflicting | Do not fuzzy-match, guess, or choose a status value |
| Data Loader metadata is unavailable | Do not create direct REST POST, PATCH, or DELETE guidance as a fallback |
| A retry follows an uncertain Data Loader failure | Do not resubmit until Data Loader status and read-only verification clarify the outcome |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LOTGRADE.DATA_LOADER_HANDOFF | decision | 30 | execution_gate | ready->LOTGRADE.DONE;blocked->LOTGRADE.HANDLE_ERROR;failure->LOTGRADE.HANDLE_ERROR | LOTGRADE.CHECK_DEPENDENCIES | stop | Before handing normalized data to core.data-loader for Inventory Lot Grades |
| LOTGRADE.HANDLE_ERROR | step | 40 | error_handler | handled->LOTGRADE.RETURN_ISSUES | none | stop | Any normalization, dependency, or Data Loader handoff issue |
| LOTGRADE.RETURN_ISSUES | terminal | 50 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| LOTGRADE.DONE | terminal | 60 | terminal | none | LOTGRADE.DATA_LOADER_HANDOFF | stop | Local normalization and readiness rules passed; Data Loader owns final validation and execution |
