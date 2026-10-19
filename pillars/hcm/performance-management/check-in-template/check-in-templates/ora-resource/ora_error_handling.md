# Check-In Templates Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| An FSM CSV member uses blanket quoting | Stop before approval or import; remove quotes from headers and values that do not require CSV escaping, preserve quotes only for values containing a comma, double quote, carriage return, or line feed, then rebuild and revalidate the ZIP. |
| Required field, cross-field, or parent-child validation fails | Stop before mutation and return the exact invalid field or relationship. |
| A request, approval, or import artifact asks to bypass a dependent-field rule | Normalize the documented reset if possible, then re-evaluate every applicable dependent-field invariant. Stop before preview, approval, import, or mutation if the payload remains inconsistent; do not waive the rule. |
| A lookup yields no exact match or an ambiguous match | Stop before mutation and request a valid unique reference value. |
| A lifecycle or uniqueness rule fails | Stop before mutation; do not retry a write with the same state. |
| Authorization is missing for create, update, or delete | Stop before mutation and request appropriate manage permission. |
| A destructive delete is requested for an in-use template | Stop and retain the template. |
| A CSV import is requested for this CSV-enabled task | Use the validated task export/template as the source and route it through `core.data-loader`; do not require a separately invented creation schema. |
| A non-CSV live operation is requested, or no export/template source is available | Stop; the supplied documentation provides no execution contract for that operation or source. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Payload violates a documented field or dependent-field constraint. | Correct the affected field relationship. |
| Lookup | A required reference lookup is missing, invalid, or ambiguous. | Supply a valid unique reference. |
| Design enforcement | Lifecycle, uniqueness, or authorization gate blocks the action. | Resolve the blocker before preview or mutation. |
| Contract gap | A non-CSV live operation is requested, or CSV creation lacks a comparable export/template. | Obtain the supported export/template or an authorized source-backed execution contract. |


## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A request needs an unsupported lookup contract | Do not invent an endpoint, query, payload, or fallback write. |
| No CSV export/template source for a CSV-enabled task | Do not invent headers, identifiers, defaults, parent-child rows, endpoints, or retries. Export a comparable record or obtain a task template. |


## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CHECKIN.SUCCESS | terminal | 70 | terminal | none | CHECKIN.ENFORCE_DESIGN | stop | Design enforcement returns compliant |
| CHECKIN.HANDLE_INPUT_ERROR | terminal | 80 | terminal | none | none | stop | Input validation or defaulting returns invalid |
| CHECKIN.HANDLE_DEPENDENCY_ERROR | terminal | 90 | terminal | none | none | stop | Dependency readiness returns missing |
| CHECKIN.HANDLE_LOOKUP_ERROR | terminal | 100 | terminal | none | none | stop | Reference lookup returns unresolved |
| CHECKIN.HANDLE_DESIGN_ERROR | terminal | 110 | terminal | none | none | stop | Dependent-field or design enforcement returns blocked |
