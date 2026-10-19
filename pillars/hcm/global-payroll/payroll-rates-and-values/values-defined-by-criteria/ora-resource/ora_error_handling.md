# Values Defined by Criteria HDL Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required input, target metadata, or prerequisite is missing | Stop preparation and identify the missing field, target evidence, or setup reference. |
| A target lookup returns no match or multiple matches | Stop and report the supplied value and match result; do not choose a substitute. |
| A hierarchy or calculation design is invalid | Stop and report the affected root, criterion, leaf, sequence, or payload rule. |
| HCM Data Loader rejects a file | Preserve sanitized component, row, and attribute diagnostics; correct the source and regenerate the immutable artifact. |
| A production load or retry is considered | Stop before retry; route through core.data-loader with current target evidence and approval for the exact regenerated artifact. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required fields or artifact shape are missing or invalid | Correct the HDL design or supplied input before revalidation. |
| Catalog mismatch | Target metadata does not support a selected header, code, or calculation payload | Export current target metadata and revise the file. |
| Dependency | LDG, group, database item, value set, or calculation reference is missing or ambiguous | Resolve the prerequisite through its authorized workflow. |
| Process failed | HCM Data Loader returns a component or row diagnostic | Correct the documented failure and regenerate the immutable artifact. |
| Approval blocker | Production target, immutable artifact, validation evidence, or current approval is absent | Complete the core.data-loader approval workflow. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Pre-import validation failure | Affected component, field or row, supplied value, and safe corrective action without secrets or protected identifiers. |
| Loader diagnostic | Sanitized component, row, attribute, status, and next corrective action. |
| Production approval | Exact target environment, immutable artifact reference, validated business effect, and approval status. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Object-specific REST contract is unavailable | Do not invent a REST endpoint, method, payload, or error format. |
| Target metadata is unavailable | Do not infer header order, requiredness, technical codes, or CalculationValues field mappings. |
| A match is missing or ambiguous | Do not choose a reference or create related setup through this task. |
| An HDL import fails or outcome is uncertain | Do not retry, resubmit, or promote the artifact without diagnosis, regeneration, and current approval. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VALUE_BY_CRITERIA.EXECUTION_GATE | decision | 60 | execution_gate | ready->VALUE_BY_CRITERIA.DONE;blocked->VALUE_BY_CRITERIA.HANDLE_EXECUTION_BLOCKER | VALUE_BY_CRITERIA.DESIGN_GATE | stop | Require validated nonproduction evidence and the owning core.data-loader approval before a live HDL import. |
| VALUE_BY_CRITERIA.DONE | terminal | 70 | terminal | none | VALUE_BY_CRITERIA.EXECUTION_GATE | stop | The task-local validation and readiness path completed; any live import remains owned by core.data-loader. |
| VALUE_BY_CRITERIA.HANDLE_INPUT_ERROR | step | 80 | error_handler | handled->RETURN_ISSUES | none | stop | Input validation failed. |
| VALUE_BY_CRITERIA.HANDLE_DEPENDENCY_ERROR | step | 81 | error_handler | handled->RETURN_ISSUES | none | stop | Dependency readiness failed. |
| VALUE_BY_CRITERIA.HANDLE_LOOKUP_ERROR | step | 82 | error_handler | handled->RETURN_ISSUES | none | stop | Reference resolution failed. |
| VALUE_BY_CRITERIA.HANDLE_DESIGN_BLOCKER | step | 83 | error_handler | handled->RETURN_ISSUES | none | stop | Design enforcement failed. |
| VALUE_BY_CRITERIA.HANDLE_EXECUTION_BLOCKER | step | 84 | error_handler | handled->RETURN_ISSUES | none | stop | Execution readiness failed. |
| RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | Return documented blocking issues for correction. |
