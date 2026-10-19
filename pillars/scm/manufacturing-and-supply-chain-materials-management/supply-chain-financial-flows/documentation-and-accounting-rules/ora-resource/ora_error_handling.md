# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required rule inputs are missing | Stop and request only the missing values |
| Both documentation outcomes are unselected | Stop and require Create trade distributions, Create intercompany invoice, or both |
| Track profits is true without Create trade distributions | Stop and require Track profits=false or Create trade distributions=Y |
| A supplied optional field is unavailable in the current live template | Stop and report the unsupported optional field; do not infer a loader column |
| UserConversionType has no exact LOV match or has multiple matches | Stop and request one valid, unambiguous UserConversionType value; do not infer ConversionTypeId |
| Currency conversion type lookup uses a field other than UserConversionType | Stop before the request; query only UserConversionType |
| Preferred currency lookup finds no exact case-insensitive name or code match, or finds more than one distinct currency | Stop and request a corrected, unambiguous Standard Currency name or code |
| Standard Currency lookup is requested with upper(), lower(), or like in q | Stop before the request and use the documented exact name/code query form |
| Registered Data Loader contract cannot be confirmed | Stop; do not substitute another business object or hand-build a source contract |
| Correction identity or effective-date range is missing | Stop; do not infer TaRuleSetId or existing dates from the rule name |
| Correction source omits or misstates effectiveOf | Stop; use the resolved existing range as `RangeMode=CORRECTION;RangeStartDate={existing-start};RangeEndDate={existing-end}` and keep replacement dates in the payload fields |
| InsertRecord or effective-period split is requested | Explain that updates are supported but Insert Record is currently unsupported through this skill's Data Loader workflow; stop before submission and do not offer the former experimental route |
| A historical InsertRecord failure is investigated | Preserve the failure evidence and distinguish transfer/import success from business-record load success; diagnosis does not enable another submission |
| Correction template lacks Operation | Stop; do not substitute a create payload |
| End-date template lacks Operation, effectiveOf, or an identity field | Stop before archive approval; do not substitute Correct or change the existing effective-date key |
| End-date load fails or its result is uncertain | Preserve the request and diagnostics; do not retry, invent child rows, or report that the end date changed |
| A FinancialTradeRelation references the DAR selected for deletion | Block delete preparation; show the matching agreement, primary-route number, and financial-route sequence. Do not cascade-delete or edit the Financial Orchestration Flow. |
| Financial Orchestration Flow usage scan is incomplete, fails, or does not expose TradeAccountingRuleSetId | Treat usage as unknown and block delete preparation; preserve sanitized endpoint/status diagnostics and do not interpret a partial scan as no references. |
| A design rule fails | Show the failed rule and the required correction before preview |
| A live operation later fails | Preserve redacted diagnostics and stop before retrying or changing the configuration |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing current Data Loader sample or Task Hook validation | Do not prepare an upload artifact or infer mandatory-field treatment |
| Currency Option is ORA_STANDARD_CURRENCY and no returned CurrencyCode is available | Do not send a StandardCurrency value inferred from the display name |
| No current preview and approval | Do not create, correct, or insert a documentation and accounting rule |
| Existing rule identity, effective-date context, or live update contract is unresolved | Do not correct or update a documentation and accounting rule |
| The resolved DAR is referenced by a FinancialTradeRelation or the usage scan is incomplete | Do not prepare, upload, or initiate its delete source; do not bypass the preflight or retry with the old archive |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RETURN-ISSUES | terminal | 99 | terminal | none | none | stop | Any blocking outcome |
| RETURN-SUCCESS | terminal | 100 | terminal | none | FO.DAR.ENFORCE-CURRENCY-POLICY | stop | Validated task-plan outcome |
| FO.DAR.DELETE-ELIGIBILITY-PASSED | terminal | 101 | terminal | none | FO.DAR.ENFORCE-DELETE-ELIGIBILITY | stop | Delete preflight only: complete Financial Orchestration Flow scan found no FTR reference; continue with the normal Data Loader delete-preparation and approval workflow, but do not perform the delete here |
