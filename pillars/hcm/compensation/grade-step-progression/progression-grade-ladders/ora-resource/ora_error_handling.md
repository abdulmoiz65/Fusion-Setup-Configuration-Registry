# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The registered-BO finder returns no or multiple `ProgressionGradeLadder` matches | Stop and report a registered-business-object validation gap. |
| Object detail, component, or attribute metadata cannot be read | Stop before field validation or import preparation. Do not infer field names, payload shape, dependencies, or defaults. |
| A supplied field is absent from the current component metadata | Stop and identify the field that must be removed or corrected. |
| A supplied value violates current type, length, mandatory, key, lookup, or reference metadata | Stop and identify the failing field contract. |
| A required parent, grade membership, rate, or rate-value dependency is missing | Stop and request the declared user-key or lookup-backed value. |
| A metadata request fails outside authentication handling | Do not automatically retry it; report the failure class and safe next action. |
| A user asks to change Fusion data | Route only through the task's separate approved Data Loader workflow after metadata validation completes. |
| A create, update, or import reaches the handoff gate | Invoke core.data-loader with the validated task context and immutable source; Core owns preview, approval, and submission. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Registered-business-object validation gap | The discriminator is not uniquely resolved | Correct the registered object condition and rerun the read-only finder. |
| Schema validation gap | Current detail, component, or attribute metadata is unavailable or mismatched | Restore readable metadata; do not infer the contract. |
| Input validation gap | A supplied field or value violates current metadata | Correct the supplied value and validate again. |
| Dependency validation gap | A supplied lookup or foreign-key dependency is not satisfied | Provide the applicable declared dependency value. |
| Fusion API failure | A read-only metadata request fails | Stop and report the failure without exposing credentials. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| `ProgressionGradeLadder` is not uniquely registered | Do not substitute a similarly named object. |
| Current schema is unavailable | Do not infer fields, request payloads, lookup values, dependencies, or defaults. |
| A metadata call fails outside 401 or 403 handling | Do not retry automatically. |
| A mutation is requested | Do not mutate through these resources; require the separate Data Loader workflow, exact preview, and explicit approval. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PGL.ROUTE | decision | 50 | execution_gate | validated_only->PGL.DONE_VALIDATED;create_or_update_or_import_ready->PGL.LOADER_READY;mutation_blocked->PGL.HANDLE_ISSUE | PGL.CHECK_DEPENDENCIES | stop | Select validation completion or the Core Data Loader handoff |
| PGL.HANDLE_ISSUE | step | 60 | error_handler | handled->PGL.RETURN_ISSUES | none | stop | Any registered-BO, schema, dependency, input, or Fusion API issue |
| PGL.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| PGL.DONE_VALIDATED | terminal | 80 | terminal | none | PGL.ROUTE | continue | Values are metadata-validated; no mutation was requested |
| PGL.LOADER_READY | terminal | 90 | terminal | none | PGL.ROUTE | continue | Mutation rules passed; invoke core.data-loader and follow it through immutable ZIP preview |
