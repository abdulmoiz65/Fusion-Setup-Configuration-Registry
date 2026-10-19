# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required fields, singleton cardinality, mapping dimension, grouping value, or in-transit auto-close dependency is invalid | Stop before preview and identify the affected business object and row. |
| A read-only reconciliation or describe request fails | Classify as auth/authz, transport/environment, or Fusion API; retain sanitized diagnostics and stop before retry. |
| Current state is ambiguous | Do not choose a record or generate a PATCH path; request a precise reconciliation. |
| An existing singleton has no user-provided changed values or no returned ParameterValueId | Stop before preview. Ask the user for the exact values to update, then rerun the corresponding read-only Data Loader query to obtain ParameterValueId. |
| A design rule blocks the preview | Return the specific correction, including the selected-organization scope or the required owner/subinventory condition. |
| Preview approval is missing or stale | Do not import; obtain approval that identifies the target environment, operation set, and immutable preview artifact. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required request value or documented combination is missing or invalid | Correct the affected row and rerun validation. |
| Catalog mismatch | A requested business object is not one of the six registered task business objects | Stop and correct the task routing. |
| Auth/authz or transport/environment or Fusion API | Describe or reconciliation cannot complete | Stop before retry; resolve the reported condition and preserve sanitized evidence. |
| Approval blocker | A live import lacks current explicit approval for its immutable preview | Request approval; do not submit. |
| Design blocker | A required configuration semantic is not met | Correct the configuration and regenerate the preview. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Reconciliation or describe failure | Target environment, business object, read-only operation purpose, failure classification, sanitized message, and safe next action. |
| Preview approval | Target environment, create/update/deactivate operations, affected business objects and row counts, immutable preview fingerprint, and approval requirement. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Uncertain singleton or item key | Do not manufacture ParameterValueId or submit an update. |
| Existing recallGlobalParams or recallItemValidationOrganizations row | Do not POST another singleton record. Do not use a user-provided ParameterValueId; pass only the value returned by the corresponding read-only business-object query to Data Loader. |
| Containment owner removal | Do not delete an existing mapping; use ActiveFlag false only through the approved supported update route. |
| Participating-organization scope change | Do not append selected organizations without reconciling the full desired scope. |
| Any live import | Do not bypass core.data-loader, preview, or the current explicit approval gate. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RECALL.PARAMETERS.GATE-PREVIEW-APPROVAL | decision | 60 | execution_gate | approved_preview->RECALL.PARAMETERS.DONE-READY-FOR-IMPORT;approval_missing->RECALL.PARAMETERS.HANDLE-APPROVAL-BLOCKER | RECALL.PARAMETERS.ENFORCE-DESIGN | stop | A live import is requested after core.data-loader produces an immutable preview |
| RECALL.PARAMETERS.HANDLE-INPUT-ERROR | step | 70 | error_handler | handled->RECALL.PARAMETERS.RETURN-ISSUES | RECALL.PARAMETERS.VALIDATE-INPUT | stop | Input validation is invalid |
| RECALL.PARAMETERS.HANDLE-LOOKUP-ERROR | step | 80 | error_handler | handled->RECALL.PARAMETERS.RETURN-ISSUES | RECALL.PARAMETERS.LOOKUP-EXISTING | stop | A reconciliation, dependency, or describe lookup is blocked, ambiguous, unsupported, or failed |
| RECALL.PARAMETERS.HANDLE-DEPENDENCY-ERROR | step | 85 | error_handler | handled->RECALL.PARAMETERS.RETURN-ISSUES | RECALL.PARAMETERS.RESOLVE-DEPENDENCIES | stop | A required dependency is blocked |
| RECALL.PARAMETERS.HANDLE-DESCRIBE-ERROR | step | 90 | error_handler | handled->RECALL.PARAMETERS.RETURN-ISSUES | RECALL.PARAMETERS.DESCRIBE-CONTRACT | stop | Describe metadata is unsupported or incomplete |
| RECALL.PARAMETERS.HANDLE-DESIGN-BLOCKER | step | 100 | error_handler | handled->RECALL.PARAMETERS.RETURN-ISSUES | RECALL.PARAMETERS.ENFORCE-DESIGN | stop | A design rule blocks preview |
| RECALL.PARAMETERS.HANDLE-APPROVAL-BLOCKER | step | 110 | error_handler | handled->RECALL.PARAMETERS.RETURN-ISSUES | RECALL.PARAMETERS.GATE-PREVIEW-APPROVAL | stop | Current explicit approval is missing or stale |
| RECALL.PARAMETERS.DONE-READY-FOR-IMPORT | terminal | 120 | terminal | none | RECALL.PARAMETERS.GATE-PREVIEW-APPROVAL | stop | The immutable preview is approved; core.data-loader owns the later import and verification workflow |
| RECALL.PARAMETERS.RETURN-ISSUES | terminal | 130 | terminal | none | none | stop | Validation, lookup, dependency, design, or approval issues are handled |
