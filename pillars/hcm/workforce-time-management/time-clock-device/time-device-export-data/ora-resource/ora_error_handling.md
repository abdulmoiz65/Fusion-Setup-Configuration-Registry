# Time Device Export Data Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Name is missing or empty | Stop and request Name. |
| Start Date is ambiguous or cannot be normalized | Stop and request an unambiguous Start Date before provider handoff. |
| A field value cannot be preserved as supplied | Stop before provider handoff and request a corrected value. |
| A criteria search cannot retrieve every page, evaluate a supplied supported child attribute, or produce an unambiguous required selection | Stop before provider handoff; do not infer an identity or treat a partial result as no match. |
| Defaulting cannot complete safely | Stop before summary generation and request the missing or invalid business value. |
| Complete Summary cannot be formed solely from verified structured business values | Return to validation, lookup resolution, or defaulting; do not request provider approval. |
| Complete Summary or Defaults Applied is missing, incomplete, technical, or not displayed immediately before approval | Return to summary generation; do not enter the provider-owned approval process. |
| A validated ZIP archive is prepared but its direct link is omitted or out of order | Return to the approval-artifact disclosure gate. Display the business-only Complete Summary and Defaults Applied, then the direct validated ZIP link, then the approval request; do not upload the archive before that response is shown. |
| The provider-owned create or update operation reports an error | Stop before retrying, retain sanitized diagnostics, and require review before another attempt. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input validation failure | The missing or invalid business field and the required correction. |
| Criteria search is blocked | The incomplete, unavailable, or ambiguous search condition and one safe corrective action. |
| Complete Summary is blocked | The missing or unverified business value, affected summary section, and one safe corrective action; do not disclose technical values. |
| Approval response for a validated ZIP | The completed business-only summary, a direct link to the exact validated ZIP immediately below it, and the approval request immediately below the link. |
| Provider operation failure | The affected business record, sanitized error response, and that no automatic retry occurred. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TDEDEXPORT_PROVIDER_APPROVAL | step | 5 | execution_gate | ready->TDEDEXPORT_READY;blocked->TDEDEXPORT_APPROVAL_BLOCKED | TDEDEXPORT_ENFORCE_SUMMARY | stop | A valid business-only Complete Summary and Defaults Applied are displayed; provider execution and approval ownership remain unchanged |
| TDEDEXPORT_READY | terminal | 6 | terminal | none | TDEDEXPORT_PROVIDER_APPROVAL | stop | Input, criteria search, defaulting, and Complete Summary passed for handoff to the provider-owned approval process |
| TDEDEXPORT_INPUT_BLOCKED | terminal | 7 | terminal | none | TDEDEXPORT_VALIDATE_INPUT | stop | Input validation failed. |
| TDEDEXPORT_SEARCH_MULTIPLE_MATCHES | terminal | 8 | terminal | none | TDEDEXPORT_SEARCH_EXPORT_DATA | stop | Multiple matching Time Device Export Data definitions were shown for user selection. |
| TDEDEXPORT_SEARCH_NO_MATCHES | terminal | 9 | terminal | none | TDEDEXPORT_SEARCH_EXPORT_DATA | stop | No Time Device Export Data definition met every supplied search criterion. |
| TDEDEXPORT_AWAIT_DUPLICATE_CHOICE | terminal | 10 | terminal | none | TDEDEXPORT_SEARCH_EXPORT_DATA | stop | A create request has a matching Time Device Export Data definition and awaits the user's use-existing or create-new choice. |
| TDEDEXPORT_SEARCH_BLOCKED | terminal | 11 | terminal | none | TDEDEXPORT_SEARCH_EXPORT_DATA | stop | Criteria search is incomplete, unavailable, or ambiguous. |
| TDEDEXPORT_DEFAULTS_BLOCKED | terminal | 12 | terminal | none | TDEDEXPORT_APPLY_DEFAULTS | stop | Defaulting could not complete safely. |
| TDEDEXPORT_SUMMARY_BLOCKED | terminal | 13 | terminal | none | TDEDEXPORT_ENFORCE_SUMMARY | stop | Business-only Complete Summary requirements were not met. |
| TDEDEXPORT_APPROVAL_BLOCKED | terminal | 14 | terminal | none | TDEDEXPORT_PROVIDER_APPROVAL | stop | Provider approval gate is not ready. |
