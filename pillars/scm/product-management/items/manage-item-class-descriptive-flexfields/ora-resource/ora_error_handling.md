# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required design information is missing or invalid | Return the exact missing or invalid input and stop before configuration. |
| Current item-class DFF definition cannot be retrieved or matched exactly | Stop and obtain the approved read-only retrieval contract or clarify the item-class and flexfield identity. |
| FND-3036 reports that the context identifier is required | Classify the failed import as a missing new-context API name. Do not reuse the failed ZIP or its approval. Obtain a reviewed valid ContextIdentifier, rebuild the candidate from the preserved baseline, rerun every validation, and request a new Data Loader approval. |
| FND-3039 reports that the segment identifier is required | Classify the failed import as a missing new-segment API name. Do not reuse the failed ZIP or its approval. Obtain a reviewed valid SegmentIdentifier, rebuild the candidate from a fresh reconciled baseline, rerun every validation, and request a new Data Loader approval. |
| ContextIdentifier or SegmentIdentifier violates API-name syntax or collides with known evidence | Return the exact field and rule. Do not strip underscores, truncate, case-shift, suffix, or otherwise rewrite an API name without explicit user review. |
| A design rule blocks the request | Return the blocking rule and the allowed correction; do not bypass the rule. |
| Validation, import, integration, search, reporting, or security testing fails | Stop before retry and retain the failed test evidence for correction. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required request, design, migration, test, or retrieval-contract information is absent | Supply the missing evidence and restart validation. |
| FAILED | A current-definition lookup, design rule, or representative test fails | Correct the documented issue and rerun validation. |
| FAILED_IMPORT | Fusion rejects an immutable approved package, including FND-3036 | Preserve the failed request evidence, correct the source through a new candidate, and restart validation and approval; never resubmit the failed artifact. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The current DFF definition is not available through an approved read-only contract | Do not infer current configuration or proceed to a configuration action. |
| A segment or context with active data lacks an approved migration plan | Do not repurpose or remove it. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RETURN_ISSUES | terminal | 4 | terminal | none | none | stop | A validation, lookup, design, or test failure occurs |
| ICDFF.ALL_GOOD | terminal | 5 | terminal | none | ICDFF.ENFORCE_DESIGN | stop | All applicable validation and design-enforcement checks pass |
