# Manage Pricing Lookups Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The supplied lookup type cannot be resolved exactly | Stop before inspecting or changing lookup codes and request the exact lookup type. |
| The lookup-code lookup is ambiguous or fails | Stop before creating or changing a lookup code. Preserve only sanitized diagnostics and do not retry automatically. |
| A predefined lookup change has an uncertain effect on Pricing logic | Stop and consult Oracle before changing the lookup. |
| A requested mutation lacks an exact target environment, operation, and reviewed payload or setup artifact | Stop before mutation and obtain the required approval through the authorized task route. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Read-only lookup | The lookup type or code queried, the sanitized match outcome, and any safe diagnostic. |
| Mutation gate | Target environment, exact lookup type and code, proposed attributes, business effect, and the approval required before mutation. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A lookup lookup is unresolved or ambiguous | Guess a lookup type or code, prepare a mutation, or modify another lookup. |
| The effect on Pricing logic is uncertain | Modify the lookup without Oracle guidance. |
| A read-only GET succeeds | Treat the read as authorization for a POST, PATCH, DELETE, import, or other mutation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| QP.LOOKUPS.EXECUTION_GATE | decision | 40 | execution_gate | approved-preview->RETURN_READY_FOR_AUTHORIZED_EXECUTION;approval_missing->RETURN_APPROVAL_REQUIRED;contract_missing->RETURN_EXECUTION_CONTRACT_ISSUES | QP.LOOKUPS.ENFORCE_DESIGN | stop | A compliant lookup change is ready for the task-specific authorized executor. |
| RETURN_READY_FOR_AUTHORIZED_EXECUTION | terminal | 50 | terminal | none | QP.LOOKUPS.EXECUTION_GATE | continue | The lookup-resolution, design, and approval gates passed; any mutation remains subject to its authorized execution route and current approval. |
| RETURN_LOOKUP_ISSUES | terminal | 61 | terminal | none | none | continue | The read-only lookup could not resolve a unique required identity. |
| RETURN_ORACLE_CONSULTATION | terminal | 62 | terminal | none | none | continue | Oracle guidance is required before a change with an uncertain effect on Pricing logic. |
| RETURN_DESIGN_ISSUES | terminal | 63 | terminal | none | none | continue | A documented design rule blocks the requested lookup change. |
| RETURN_APPROVAL_REQUIRED | terminal | 64 | terminal | none | none | continue | A current approval bound to the exact mutation preview is required. |
| RETURN_EXECUTION_CONTRACT_ISSUES | terminal | 65 | terminal | none | none | continue | The task-specific execution contract is incomplete or cannot authorize a mutation. |
