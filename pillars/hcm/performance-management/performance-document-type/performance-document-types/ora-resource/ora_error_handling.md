# Performance Document Types Error Handling

Source: Oracle Fusion Cloud Talent Management, Overview of Performance Document Types.

## Error Situations

| Situation | What Should Happen |
|---|---|
| An FSM CSV member uses blanket quoting | Stop before approval or import; remove quotes from headers and values that do not require CSV escaping, preserve quotes only for values containing a comma, double quote, carriage return, or line feed, then rebuild and revalidate the ZIP. |
| Document type dates do not contain the date range of a performance template that uses the document type | Stop and align the document type or template dates before associating them. |
| A document type that must be available has status other than Active | Stop and set the status to Active. |
| A performance template has no performance document type | Stop and select a document type on the General tab. |
| A template using interim evaluations has no associated document type for its document period | Stop and associate at least one document type and applicable review periods. |
| A goal plan intended for performance documents has no associated document type | Stop and associate the document type and review period with the goal plan. |
| A request sets an in-use document type to Inactive | Stop; a document type used by a template or goal plan cannot be set to Inactive. |
| A CSV import is requested for this CSV-enabled task | Use a validated task export/template and the `core.data-loader` route; the CSV export/import flag is the route authorization. |
| A non-CSV live operation is requested, or CSV creation has no comparable export/template | Stop; the writable endpoint, payload, or source record set is not established. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required document type information is absent or invalid. | Correct the inputs and validate again. |
| Dependency readiness | A template, interim-evaluation document period, or goal-plan association is unresolved. | Resolve the documented relationship and validate again. |
| Design blocker | A date, availability, association, or inactivation restriction is violated. | Correct the design, except retain Active status when the inactivation restriction applies. |
| Contract gap | A non-CSV live operation is requested, or CSV creation has no comparable export/template. | Obtain the supported export/template or an authorized source-backed execution contract. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Planning review | Document type dates, status, template and goal-plan associations, interim-evaluation associations, and unresolved items. |
| Execution request | The missing source-backed writable contract and the safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| No comparable export/template for CSV creation | Do not invent headers, identifiers, defaults, relationship rows, endpoints, or retries. Export a comparable record or obtain a task template. |
| In-use document type inactivation restriction applies | Do not propose setting the document type to Inactive. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_DOCUMENT_TYPES.EXECUTION_CONTRACT | decision | 60 | execution_gate | contract_missing->PERFORMANCE_DOCUMENT_TYPES.STOP_CONTRACT;ready->PERFORMANCE_DOCUMENT_TYPES.DONE | PERFORMANCE_DOCUMENT_TYPES.ENFORCE | stop | A non-CSV live operation is requested, or a CSV import lacks a validated export/template source. |
| PERFORMANCE_DOCUMENT_TYPES.DONE | terminal | 70 | terminal | none | PERFORMANCE_DOCUMENT_TYPES.EXECUTION_CONTRACT | stop | The CSV export/template source is validated or another complete execution contract is available. |
| PERFORMANCE_DOCUMENT_TYPES.STOP_INVALID | terminal | 80 | terminal | none | none | stop | Input validation fails. |
| PERFORMANCE_DOCUMENT_TYPES.STOP_DEPENDENCY | terminal | 90 | terminal | none | none | stop | A documented dependency is unresolved. |
| PERFORMANCE_DOCUMENT_TYPES.STOP_DESIGN | terminal | 100 | terminal | none | none | stop | A documented design blocker remains. |
| PERFORMANCE_DOCUMENT_TYPES.STOP_CONTRACT | terminal | 110 | terminal | none | PERFORMANCE_DOCUMENT_TYPES.EXECUTION_CONTRACT | stop | The source-backed writable execution contract is unavailable. |
