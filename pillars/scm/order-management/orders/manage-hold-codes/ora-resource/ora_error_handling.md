# Manage Hold Codes Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required input, set, role, task, or hold identity is missing or ambiguous | Stop before source generation and show the specific missing or unresolved value. |
| Live lookup, template, schema, or transport validation fails | Classify the failure, preserve redacted evidence, and stop before approval or upload. |
| The current template cannot express a child relationship without a server-generated parent ID | Stop with catalog_or_metadata_mismatch; obtain updated business-object guidance. |
| Upload, initiation, or import fails | Do not retry automatically. Preserve returned diagnostics and use the documented status or verification workflow only when requested. |
| An approval preview, source, mapping, schema, or template changes | Invalidate approval and restart validation and preview preparation. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required user input is missing or invalid. | Correct the stated input. |
| catalog_or_metadata_mismatch | A lookup or live template cannot express the requested contract. | Obtain clarified catalog or business-object guidance. |
| transport_or_environment | A read-only environment request is unavailable. | Restore access and re-run the documented preflight. |
| approval_blocker | Preview, task validation, or execution approval is missing or stale. | Complete the required gate before upload. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Immutable approval preview | Target environment, requested hold values, resolved set identity, defaults, role and task mappings when applicable, and the exact immutable source. |
| Upload and initiation | Separate explicit approval immediately before the Data Loader operation. |
| Failure | Failure class, sanitized stage evidence, affected operation, and one safe next action; never disclose credentials, tokens, private keys, or sensitive payloads. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A create is requested | Do not use a direct REST POST instead of core.data-loader. |
| A lookup is ambiguous or unavailable | Do not guess an identifier, role, task, set, or application value. |
| A live operation fails or is indeterminate | Do not automatically retry, upload again, or initiate another load. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HOLD_CODES.APPROVAL_GATE | step | 60 | execution_gate | preview-ready->RETURN_SUCCESS;preview-missing-or-changed->RETURN_ISSUES | HOLD_CODES.ENFORCE_DESIGN | stop | The Data Loader source has passed task validation and is ready for its separate explicit upload approval. |
| RETURN_SUCCESS | terminal | 70 | terminal | none | HOLD_CODES.APPROVAL_GATE | continue | The validated source is ready for its separate explicit upload approval. |
| RETURN_ISSUES | terminal | 80 | terminal | none | none | continue | An input, lookup, dependency, design, preview, or approval gate failed. |
