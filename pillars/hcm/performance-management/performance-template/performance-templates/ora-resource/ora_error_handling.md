# Performance Templates Error Handling

Sources: [REST resource and field guidance](../../performance-template-rest-source-contract.md) and existing setup guidance. Preserve actual target messages and severity.

## Error Situations

| Situation | What Should Happen |
|---|---|
| An FSM CSV member uses blanket quoting | Stop before approval or import; remove quotes from headers and values that do not require CSV escaping, preserve quotes only for values containing a comma, double quote, carriage return, or line feed, then rebuild and revalidate the ZIP. |
| A request, approval, or import artifact asks to bypass a dependent-field rule | Apply the documented reset if one exists, then re-evaluate all applicable invariants. Stop before preview, approval, import, or mutation if the payload remains contradictory; do not waive the rule. |
| A period document-type row cannot resolve `DocTypeId` | Stop before approval or import. Resolve the document type by the row's bare `Name`, then replace its bare `DateFrom` and `DateTo` with that document type's effective dates. Do not use template or template-period dates in those columns. |
| A generated FSM row has a stale or mismatched `GroupingKey` | Stop before approval or import. Populate the row identity first, recompute the key from the documented CSV-specific composition, and replace the stale key. Do not reuse a comparator key. |
| A generated FSM child row has a stale parent reference | Stop before approval or import. Rewrite every `HRA_TEMPLATE.*`, `HRA_TEMPLATE_SECTION.*`, or `HRA_TMPL_PERIODS.*` parent-reference value from its owning row in the same archive, then revalidate the complete lineage. Do not assume a correct child grouping key repairs the reference. |
| A root DELETE is attempted | Stop; root DELETE is disabled. Use only the documented deletePerformanceTemplate action after lifecycle and approval gates pass. |
| A requested change or deletion is prohibited by its current lifecycle or field-specific restriction | Stop; do not retry with a different endpoint or malformed child payload. InUseFlag alone does not prohibit every update: resolve the exact operation and changed fields against the current contract. |
| The requested environment is outside the task's allowed target set or is explicitly forbidden | Stop and retain the selected allowed environment. Do not suggest that a new preview, approval, credential, or later request could enable an explicitly forbidden environment. |
| The current actor lacks permission for the requested operation | Stop and report the authorization failure for the current actor. Do not suggest another account, impersonation, credential, endpoint, or privilege workaround; no mutation is attempted. |
| A reference object cannot be resolved from its documented lookup | Stop; identify the supplied field, run only its resolver in ora_reference_lookups.md, and require a valid unambiguous value before retrying validation. |
| A write is requested | Stop before the write. Present the exact target environment, operation, and immutable preview or payload for explicit approval. |
| PT.DONE is reached | Report validation and approval complete, not a completed Fusion operation. This graph has no write node. Continue only through an execution contract explicitly selected by the task skill; otherwise report an execution-route blocker. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required, range, lookup-code, duplicate, or payload-shape validation fails | Correct values and validate again. |
| Lifecycle blocked | State or permission forbids the operation | Stop; do not retry until the lifecycle condition changes. |
| Reference lookup failure | A documented reference lookup returns no match or more than one match | Correct the supplied field value and validate again. |
| Approval blocker | A mutation lacks current approval tied to exact preview, target, and operation | Obtain explicit approval immediately before execution. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview and approval | Target environment, exact operation, affected template/child identity, sanitized immutable preview, and approval requirement. |
| Reference lookup failure | The unresolved field, resolver name, match count, and required correction. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A documented lookup returns no or multiple matches | Do not infer a value, substitute a different endpoint, or continue with an unresolved reference. |
| A write has no current exact approval | Do not POST, PATCH, invoke an action, delete, import, or retry. |
| A REST root DELETE is requested | Do not call the disabled root DELETE endpoint. |
| The target is explicitly forbidden by the active task | Do not offer reapproval, a new preview, or a credential change as a way to use that target. |
| The current actor lacks the required privilege | Do not switch accounts, impersonate another actor, seek alternate credentials, or use another endpoint to bypass the authorization failure. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PT.EXECUTION_APPROVAL_GATE | decision | 80 | execution_gate | approved->PT.DONE;missing_approval->RETURN_ISSUES | PT.ENFORCE_REST_DESIGN | stop | A mutation is requested after all validation and design gates pass |
| RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | Any validation, lifecycle, lookup, invariant, design, or approval issue exists |
| PT.DONE | terminal | 100 | terminal | none | PT.EXECUTION_APPROVAL_GATE | stop | The request is validated and has current exact approval |
