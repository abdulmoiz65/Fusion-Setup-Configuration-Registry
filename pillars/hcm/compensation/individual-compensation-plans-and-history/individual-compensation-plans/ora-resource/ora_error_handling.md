# Error Handling

| Failure Class | Condition | Action |
|---|---|---|
| registered-business-object validation | Object absent or ambiguous | Stop; do not substitute another business object. |
| schema validation | Template, child metadata, or supplied field is unavailable or invalid | Stop; correct the source or restore metadata access. |
| dependency readiness | Parent lineage, payroll element, or schema-declared reference cannot be resolved | Stop; correct the owning setup and rerun validation. |
| query-contract failure | payrollElementDefinitionsLOV metadata does not declare the required finder, separately serialized finder arguments are rejected, or the returned row does not satisfy the requested element and resolved identity | Stop; do not report the element as missing and do not retry with generic `q` syntax or split finder arguments. |
| authorization or transport | A required read-only lookup returns 401, 403, or fails | Stop and report the environment failure without a fallback route. |

## Task Nodes

| Rule ID | Action Type | Transitions | Prerequisites | Applies When |
|---|---|---|---|---|
| ICP.HANDLE_ISSUE | error_handler | handled -> ICP.RETURN_ISSUES | none | Any lookup, schema, dependency, or input issue. |
| ICP.RETURN_ISSUES | terminal | none | none | A blocking issue was classified and disclosed. |
| ICP.DONE_VALIDATED | terminal | none | ICP.ENFORCE_SCHEMA_GATE | The source is validated and ready for the separate Data Loader workflow. |
