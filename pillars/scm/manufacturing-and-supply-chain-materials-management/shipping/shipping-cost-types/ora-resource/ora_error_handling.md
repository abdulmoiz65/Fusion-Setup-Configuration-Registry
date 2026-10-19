# Shipping Cost Types Error Handling

Source: Shipping Cost Types Redwood create and update action chains, and approved V3 authoring boundary.

## Error Situations

| Situation | What Should Happen |
|---|---|
| The routed core.data-loader workflow reports that a category or currency LOV value has no exact match, multiple matches, or a conflicting display value and code | Stop before Data Loader handoff and request a single exact category or currency value. Do not fuzzy-match or select the first result. Do not issue a task-resource REST request as a fallback. |
| StartDateActive or EndDateActive is not a literal string in YYYY-MM-DDTHH:mm:ss.sss+00:00 format in the final DAT | Stop before Data Loader handoff. Rebuild the XLSX and DAT so the value is a literal canonical UTC string, for example 2026-09-24T06:42:00.000+00:00. Do not submit an Excel native date/time cell, a Z-suffixed value, a date-only value, an offset-free value, or another-offset value. |
| Fusion Data Loader rejects the request | Preserve the redacted diagnostic through the Data Loader workflow. Do not retry a live operation automatically. |
| The Redwood create or update route reports an error | Preserve the returned detail for diagnosis and correct the source data before a new governed Data Loader attempt. Do not use the UI REST route as a fallback. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SCT.DONE | terminal | 40 | terminal | none | SCT.VALIDATE_INPUT | stop | Input validation passed; any required live lookup is delegated to core.data-loader |
| RETURN_ISSUES | terminal | 50 | terminal | none | none | stop | Input validation or lookup resolution failed |
