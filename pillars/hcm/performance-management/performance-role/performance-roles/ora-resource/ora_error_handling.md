# Performance Roles Error Handling

Sources: Performance Roles REST contract and Performance Roles Frontend Validations.

## Error Situations

| Situation | What Should Happen |
|---|---|
| An FSM CSV member uses blanket quoting | Stop before approval or import; remove quotes from headers and values that do not require CSV escaping, preserve quotes only for values containing a comma, double quote, carriage return, or line feed, then rebuild and revalidate the ZIP. |
| Required role data is missing, invalid, or violates the date range rule | Stop and correct the request before preview or mutation. |
| Manager or participant field restrictions are violated | Stop and correct the type-specific fields. |
| An update changes RoleType or an in-use protected field | Stop; the REST and frontend contracts prohibit the change. |
| Role lookup does not resolve the intended update or delete target | Stop and obtain the exact RoleId. |
| The REST entity returns HRC:::HRC_ATOM_NOAUTH | Stop and use a caller with manage-performance-roles permission. |
| A REST create, update, or delete request is proposed | Require current explicit approval bound to the exact validated role and operation. |
| A REST write result is uncertain | Stop and reconcile the target with a read-only lookup before considering another write. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required values, lengths, domains, or date relationships are invalid. | Correct the request and validate again. |
| Dependency readiness | Target RoleId, authorization, or in-use state is unresolved. | Resolve the missing dependency and validate again. |
| Design blocker | The request violates a type-specific, insert-only, read-only, or in-use rule. | Correct the request; do not bypass the restriction. |
| Authorization | Fusion returns HRC:::HRC_ATOM_NOAUTH. | Use an authorized caller. |
| Transport or Fusion API | A read or write request fails, or a write result is uncertain. | Preserve diagnostics and stop before retrying a write. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview | Target identity, proposed writable fields, current lookup results, dependencies, and blockers. |
| Mutation approval | Exact target environment, operation, and immutable validated request. |
| Uncertain write | That the outcome is unknown and the required read-only reconciliation step. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A write lacks current approval or an exact validated target | Do not create, update, or delete. |
| A write outcome is uncertain | Do not retry automatically. |
| A caller supplies hidden, read-only, or type-prohibited fields | Do not forward those fields in a write request. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_ROLES.EXECUTION_GATE | decision | 60 | execution_gate | approved->PERFORMANCE_ROLES.DONE;blocked->PERFORMANCE_ROLES.STOP_CONTRACT | PERFORMANCE_ROLES.ENFORCE | stop | A REST create, update, or delete is ready for its approval gate. |
| PERFORMANCE_ROLES.STOP_INVALID | terminal | 70 | terminal | none | none | stop | Input validation fails. |
| PERFORMANCE_ROLES.STOP_DEPENDENCY | terminal | 80 | terminal | none | none | stop | A target, authorization, or in-use dependency is unresolved. |
| PERFORMANCE_ROLES.STOP_DESIGN | terminal | 90 | terminal | none | none | stop | A design restriction blocks the request. |
| PERFORMANCE_ROLES.STOP_CONTRACT | terminal | 100 | terminal | none | none | stop | An approval or write-safety gate blocks the request. |
| PERFORMANCE_ROLES.DONE | terminal | 110 | terminal | none | PERFORMANCE_ROLES.EXECUTION_GATE | stop | The request passed validation, enforcement, and approval gating. |
