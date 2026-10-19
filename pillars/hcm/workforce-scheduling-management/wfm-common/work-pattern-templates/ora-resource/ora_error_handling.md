# Work Pattern Templates Error Handling

## Source Basis

- REST describe Boolean typing and lowercase DAT Boolean serialization, user-directed correction, received 8 October 2026

- Work Pattern Templates Rest Describe, Confluence page 21510086973, version 3
- Work Pattern Templates Technical Design Document for FSCR, Confluence page 21509588886, version 9
- User-Facing Value Resolution Policy, attached text source, received 12 August 2026
- New Shift UI screenshot showing break-duration validation, developer-provided, received 13 August 2026
- Failed Work Pattern Template load reporting an orphan Break child, developer-provided Fusion diagnostic, received 13 August 2026
- Work Pattern Shift unpaid-break total requirement, developer-confirmed functional source, received 13 August 2026
- Cumulative DayOfWorkPattern rule for multi-cycle templates, user-provided, received 17 August 2026
- Failed Work Pattern Template duplicate load reporting a non-whole-number WorkPatternShiftId, developer-provided Fusion diagnostic, received 14 August 2026
- ID-only Work Pattern Template deletion requirement, user-provided, received 17 August 2026
- Successful Work Pattern Templates create DAT with parent, Shift, and Break loader correlations, user-provided, received 17 August 2026
- Break timing requirements by break type, user-provided, received 18 August 2026
- Duration, Flexible days and times, and ShiftName input rules, user-provided, received 18 August 2026
- User-facing field-label, defaulting, and Template Name rules, user-provided, received 18 August 2026
- Break-type eligibility by Shift Period Type, user-provided, received 18 August 2026
- Work Pattern Template Data Loader source-route and approval-fingerprint handling, user-provided, received 21 August 2026
- WFM-81615 Recommended Best Practices: complete shift-duration reconciliation, Jira, reviewed 10 September 2026
- WFM-81615 AC2: Work Pattern Template reuse, duplication, and unsuitable classification, Jira, reviewed 10 September 2026
- WFM-81615 AC7: incomplete or conflicting requirement clarification, Jira, reviewed 10 September 2026
- Break Name defaulting from duration, Shift Period Type, and paid or unpaid status, developer-provided, received 18 September 2026
- Existing Work Pattern Template immutable-field rule, user-provided, received 1 October 2026

## Error Situations

| Situation | What Should Happen |
|---|---|
| REST field typing is unresolved or a prepared Boolean DAT value is not lowercase true or false | Classify as input validation or catalog/metadata mismatch as applicable. Identify the affected business field, resolve its type through resolve_work_pattern_field_types, and correct and regenerate the source before preview. A String label in Data Loader metadata does not override verified REST Boolean typing. Do not lowercase unrelated text or automatically replay a failed load; a corrected archive requires validation and approval. |
| Required template, shift, break, or assignment-rule information is missing or invalid | Identify the affected business record and missing or invalid business value, then stop before preview |
| A requirement is incomplete, incompatible, or conflicts with another requirement | Stop before preview, approval, creation, or duplication. Present the unresolved question, available verified business options, business impact, and a recommended assumption for specialist resolution. Do not apply the recommendation as a default or continue until the user resolves the conflict. |
| One or more required supported fields have no resolved value and no documented default | Ask for all missing fields together, using only their exact labels from the current Data Loader describe, REST metadata, or approved UI input source. Do not request an invented alias or a documented default value |
| A user-facing prompt or suggestion contains a field label not supported by the current Data Loader describe, REST metadata, or approved UI input source | Stop before presenting the response and replace it with the exact supported field label |
| A lookup returns zero or many exact matches | Report the unresolved business selection and request a more precise displayed value |
| A relevant existing template cannot be completely compared or classified | Stop before recommending reuse, duplication, or creation. Explain the incomplete comparison in business language and request the missing business information or a corrected selection. |
| Final completion verification reaches a failed terminal status, times out, or returns a template that differs from the approved configuration | Report final status, totals, actionable diagnostics when present, and one safe resume action. Do not retry the submission automatically or report final success |
| Multiple complete Enterprise Shift matches were presented but the user did not select one | Stop before preview or artifact generation and request a selection from the presented complete matches. A single complete match is selected automatically; no complete match proceeds with supplied local times without an Enterprise Shift prompt |
| A lookup returns 401 or 403 | Classify it as authentication or authorization failure; do not treat the referenced setup as absent |
| An existing selected enterprise shift is inactive | Block the affected shift and request one active Shift |
| A generated DAT or REST artifact contains an unverified field mapping, omission, default, derived value, or parent association | Block only the affected artifact field; validate it against the current registered attributes or REST describe and correct the mapping before preview |
| A new-template create source treats the local WorkPatternTemplateId correlation as a Fusion-generated Work Pattern Code or as an existing Fusion identifier | Stop before preview; retain the local parent correlation only to associate the new template and Shift rows, omit WorkPatternCode for create, and regenerate the source |
| A Data Loader PATCH cannot resolve the Work Pattern Template from its user key | Stop without retry; retrieve the existing template with WorkPatternCode explicitly requested, replace the source with that exact returned value, and regenerate validation and approval artifacts |
| An update to an existing Work Pattern Template changes Shift Period Type, Cycles, or Unit of Measure | Stop before preview or submission and show only the requested immutable field labels: You can't change {requested immutable field labels} for an existing Work Pattern Template. Preserve the verified existing values; do not retry the update with altered values. |
| A deletion artifact requires or contains WorkPatternCode as its identity | Stop before preview; regenerate the deletion row with the verified WorkPatternTemplateId and RestAction=DELETE, without WorkPatternCode |
| A create or update is blocked because no direct REST operation is authored or a spreadsheet runtime is unavailable | Treat the block as an incorrect executor route; prepare the mutation through core Data Loader using a DAT source and immutable ZIP archive, then run the normal validation and approval gates |
| The explicit ZIP source route is rejected before UCM upload | Do not change the DAT source or retry the explicit ZIP route. Use the validated DAT source through core Data Loader, which must regenerate the immutable ZIP internally. Retain the existing approval only when the loader confirms the same archive SHA-256 and the source, mappings, schema, and eligibility results are unchanged; otherwise create a new preview and obtain fresh approval. |
| UnpaidBreakDurationMinutes is missing or differs from the total of the Work Pattern Shift's unpaid Break rows | Block the affected shift artifact; derive and include the exact unpaid-break total before preview |
| Work Duration, paid-break duration, unpaid-break duration, Total Duration, or elapsed Start Time to End Time are inconsistent | Stop before approval or creation. Identify the affected shift and show the conflicting business values with the expected duration relationship, then ask the user to clarify or correct the values before revalidation. |
| A Break child has no association to its intended Work Pattern Shift | Block the affected Break artifact; attach it to its intended Shift before preview and do not submit an orphan child |
| A Duration or Flexible days and times Break uses a Break Type other than Any time during shift, or requires Start or End | Block the affected Break artifact. Use only Any time during shift with Break Name, paid or unpaid status, and Duration in Minutes; preserve a supplied Break Name or derive it from any available combination of Duration in Minutes, Shift Period Type, and paid or unpaid status; do not request missing naming components or Start or End. |
| A Break for another Shift Period Type is missing required timing, duration, or paid status, or an Any time during shift Break does not use its parent Shift's Start Time and End Time | Block the affected Break artifact. For Any time during shift, set the Break Start Time and End Time to the parent Shift's Start Time and End Time. For every other Break Type, require Start Time, End Time, Duration in Minutes, and paid status before preview; preserve a supplied Break Name or derive it from any available combination of Duration in Minutes, Shift Period Type, and paid or unpaid status without requesting missing naming components. |
| A Start and end times or Flexible days Shift has no required Start or End value | Block the affected Shift artifact and request only the missing applicable time field. Do not apply this rule to Duration or Flexible days and times. |
| A Duration or Flexible days and times Shift lacks a positive Duration, or the flow requests Start, End, or ShiftName | Block the affected Shift artifact. Require only Duration and the selected days; do not request Start, End, or ShiftName. |
| Fusion rejects a new WorkPatternShiftId because it is not a whole number | Treat the value as an invalid Data Loader correlation value, not a missing Fusion record; allocate a unique local whole-number Shift correlation value, repeat it in each new child Break parent reference, and regenerate the artifact |
| A day-code lookup does not produce a usable Shift day | Stop before preview; resolve the weekday from the active lookup and apply (cycle - 1) x 7 plus the verified weekday index rather than sending a lookup code as DayOfWorkPattern |
| Break details do not match the shift's break duration | Block the affected shift and ask the user to add or adjust break details until their combined duration exactly matches the selected Shift's break duration |
| A template, shift, break, cycle, overlap, duration, or assignment-rule validation fails | Preserve the local aggregate, disclose the affected business item, and require correction before retrying validation |
| Fusion returns a 4xx or 5xx response | Preserve redacted status, service error details when present, response summary, affected operation, and correlation evidence; stop before retry |
| A non-idempotent write has an uncertain result | Do not replay it automatically; reconcile through a documented read-only lookup before considering another attempt |
| Delete or deleteAllRules is requested | Stop until dependency and cascade effects, exact target, rollback plan, and explicit approval are confirmed |
| Concurrency or retry behavior is required | Report that ETag, If-Match, rate-limit, and optimistic-concurrency behavior are not documented for this resource; do not invent them |
| A component-private condition-builder contract is required | Report the specific unresolved contract and stop rather than deriving a URL, query, response schema, or delete behavior |
| An internal value has no verified display mapping | Stop recommendation generation, mark the selection unresolved or incomplete, and request the displayed label or relevant lookup information without repeating the raw value |
| A supplied internal value conflicts with a supplied display label | Report inconsistent selection information without exposing the internal value |
| A verified field label is unavailable | Describe the field by its business purpose without exposing its internal attribute name |
| A technical URL would expose a record key | Replace the key with a descriptive placeholder |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required, conditional, type, range, length, overlap, cycle, or uniqueness rules fail | Correct the affected business value and rerun validation |
| Catalog or metadata mismatch | A requested field, operation, lookup, or business behavior is not supported by current source-backed metadata | Reconcile the source or target metadata before preview |
| Existing-record key resolution | A Data Loader update cannot resolve the current Work Pattern Template from its registered user key | Retrieve the exact system-generated WorkPatternCode from the current template and regenerate the update artifact; do not invent or retry with a name-derived code |
| New-child correlation | A new template, Shift, or Break cannot be associated in the flat Data Loader source, a template correlation is confused with a Fusion-generated value, or Fusion rejects a new Shift correlation because it is not a whole number | Use a unique local template correlation for the new template and its Shift rows, then a unique local whole-number Shift correlation for each new Shift and its Break rows; do not substitute WorkPatternCode for either correlation |
| Authentication or authorization | A read-only Fusion request returns 401 or 403 | Refresh authentication once where the shared client permits, then stop if access is still rejected |
| Fusion API | Fusion returns a documented service error or an unexpected 4xx/5xx response | Preserve redacted diagnostic evidence and stop before retry |
| Approval blocker | A destructive or live operation lacks an exact current preview and approval | Present the exact target and effect through the owning runbook and wait for approval |
| Concurrency gap | Safe stale-data detection or uncertain-write reconciliation is not documented | Stop and obtain a source-backed concurrency or verification contract |
| Component contract gap | A framework-managed condition-builder or external component contract is unavailable | Stop and obtain the missing endpoint, request, response, or action semantics |
| User-facing value resolution | A selected value or field cannot be mapped to verified business terminology | Return an unresolved business-language result and do not recommend from the unresolved value |
| Inconsistent selection | A supplied display label does not represent the supplied internal selection | Request corrected selection information without exposing the internal value |
| Response sanitization | Internal or implementation-only material remains after response construction | Remove it and rerun the design-enforcement check |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation failure | Affected business record, failed rule, sanitized supplied value or missing business field, and required correction |
| Lookup failure | Resolver purpose, business-facing selection, result count or safe failure class, and one safe next action |
| Fusion service failure | Environment identity, operation, redacted status and error details, correlation evidence when available, and retry prohibition |
| Destructive-action gate | Exact business target, intended destructive effect, dependency/cascade uncertainty, rollback plan, and approval state |
| Resolved result | Verified display labels, business names, meanings, descriptions, and user-facing field labels only |
| Unresolved selection | State that the selected value could not be resolved to a business label; do not display the value, guess a meaning, or expose a code-to-label mapping |
| Recommendation | Use business terminology and only verified resolved meanings |
| Required information | Show only user-facing labels for missing mandatory business values |
| Optional information | Show only user-facing labels for optional business values |
| Unavailable or hidden information | Explain the business reason without internal field names or implementation details |
| Validation | State the business-facing rule and affected selection without raw internal values |
| Technical URL | Use a descriptive placeholder instead of a real identifier |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Validation or lookup is incomplete | Do not present the task as preview-ready or execution-ready |
| A write fails or its result is uncertain | Do not automatically retry POST, PATCH, DELETE, upsert, deleteAllRules, or batch |
| A destructive action lacks exact approval | Do not issue the operation or treat general implementation approval as sufficient |
| ADF batch is considered | Do not include findByAdvancedSearchQuery or deleteAllRules; both are documented as batch-disabled |
| ETag, If-Match, retry, delete restriction, rate limit, or cascade behavior is undocumented | Do not infer or fabricate it |
| A component-private contract is unavailable | Do not derive a publicWorkers base, HCM Rules delete URL, internal endpoint, response type, or query shape |
| A user-facing response contains an internal value | Do not send it; resolve and sanitize the response first |
| A label would be inferred rather than verified | Do not remove prefixes, replace underscores, change capitalization, expand abbreviations, or infer from a similar value |
| A recommendation depends on an unresolved value | Do not recommend; return an unresolved or incomplete result |
| A code is not proven to be intentionally displayed by the UI | Do not present it as a business-facing code |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WPT.HANDLE_ERROR | step | 70 | error_handler | handled->WPT.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, defaulting, design, service, approval, or sanitization gate is blocked |
| WPT.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | A blocking issue was disclosed in business language with one safe next action |
| WPT.READY | terminal | 90 | terminal | none | WPT.WAIT_FOR_FINAL_COMPLETION | stop | An approved asynchronous request reached terminal success and its exact Work Pattern Template read-back matched the approved configuration |
