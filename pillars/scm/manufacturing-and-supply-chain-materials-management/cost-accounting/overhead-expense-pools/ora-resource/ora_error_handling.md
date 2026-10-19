# Error Handling

## Source

- [FSCR Data Loader](../../../../../../core/data-loader/SKILL.md)

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required Create field is omitted, null, empty, or invalid | Identify the field and reject the request before payload construction. |
| A supplied PATCH field is null, empty, or invalid | Identify the field and reject the change; an omitted PATCH field remains unchanged. |
| A prepared source omits, blanks, or mismatches RestAction | Stop before preview. Rebuild the JSON and source with `POST` for Create, `PATCH` for PATCH, or `DELETE` for DELETE, then rerun validation. |
| A DELETE request omits ExpensePoolCode, supplies a mutable attribute, undocumented selector, or user-supplied internal ID | Identify the invalid delete field and reject the request before Data Loader preparation. |
| A DELETE selector has no exact target, has multiple targets, or an optional qualifier conflicts with the selected target | Return the match outcome and ask for a valid ExpensePoolCode or a more precise supported qualifier; never select the first candidate. |
| InactiveFlag cannot be normalized to `Y` or `N` | Reject the request; accept only `Y`/`y`, `N`/`n`, `true`, `false`, `active`, or `inactive`, then normalize to uppercase `Y` or `N`. Do not default an explicitly supplied null or invalid value. |
| Expense pool type lookup has no exact normalized Meaning match or has multiple matches | Return allowed meanings from the complete paginated ORA_CST_EXPENSE_POOL_TYPES result for no match. For multiple matches, ask for a more precise meaning. |
| A Create or DELETE SetName candidate query has no candidate, multiple candidates, or a failed local normalized verification | For no candidate, ask for a valid set. For multiple candidates or a failed local verification, ask for a more precise set name. |
| A PATCH request supplies SetName, SetId, or SetCode | Reject the request because the set is immutable after Create. |
| Lookup auth, authorization, transport, or response-shape failure | Stop and report the failure class without retrying or selecting a result. |
| Data Loader source or Business Object validation fails | Stop before preview, correct the source data, and revalidate it through core.data-loader using costAccountingOverheadExpensePools. |
| Upload or initiation is requested without an immutable Data Loader approval preview and a later standalone approve | Stop before the first POST. |
| Data Loader REST submission is requested | Route the operation through core.data-loader for upload and initiation using costAccountingOverheadExpensePools; do not construct a direct REST request. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required Create or DELETE field, supplied PATCH field, prohibited DELETE input, or inactive-flag value cannot normalize to `Y` or `N` | Return the specific validation issue. |
| Target resolution | A DELETE selector does not identify exactly one existing Expense Pool | Return the candidate outcome and request a valid or more precise supported selector. |
| Reference lookup | A documented read-only lookup has no unique result | Return allowed values or request the specified disambiguator. |
| Auth/authz | A lookup returns authentication or authorization failure | Stop and request authorized environment access. |
| Transport/environment | A lookup cannot reach the approved environment or has an invalid response shape | Stop and preserve sanitized diagnostic context. |
| Data Loader validation | The source or costAccountingOverheadExpensePools Business Object does not pass Data Loader validation | Correct the source data and generate a new immutable approval preview. |
| Approval blocker | Upload or initiation is requested without a current immutable approval preview and later standalone approve | Stop before upload; obtain a new preview and then send approve in a separate message. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation rejection | The failed field, sanitized supplied value state, and the rule needed to correct it. |
| Lookup rejection | Resolver name, match outcome, and allowed values or required disambiguator without selecting a candidate. |
| Delete target rejection | ExpensePoolCode, supplied qualifier names, sanitized candidate count, and the next accepted selector; do not show internal IDs. |
| Data Loader validation failure | The affected source data, validation result, and corrective action. |
| Data Loader approval gate | The immutable preview and the required standalone approve action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Required Create or DELETE validation, supplied PATCH-field validation, or lookup is incomplete | Do not construct a final payload or initiate Data Loader work. |
| Data Loader validation or approval gate is incomplete | Do not upload, initiate, retry, or construct a direct REST request. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| OEP.HANDLE_ISSUE | step | 20 | error_handler | disclosed->RETURN_ISSUES | none | stop | A Create, DELETE, supplied PATCH-field validation, lookup, target-resolution, or payload-enforcement issue occurs |
| OEP.DONE_OPERATION | terminal | 10 | terminal | none | OEP.ENFORCE_PAYLOAD | stop | Create, DELETE, or PATCH input and lookup validation passed; core.data-loader owns subsequent execution. |
| RETURN_ISSUES | terminal | 21 | terminal | none | none | stop | Error disclosure is complete |
