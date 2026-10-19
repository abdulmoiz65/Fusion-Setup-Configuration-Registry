# Units of Measure Usages Error Handling

## Source Evidence

| Source | Used For |
|---|---|
| Developer-provided BO registration record and live Data Loader metadata check | Governed business-object route and availability baseline |
| Generated task skill metadata | Data Loader is the selected execution route |

## Error Situations

| Situation | What Should Happen |
|---|---|
| Data Loader metadata for unitOfMeasureUsages is unavailable in a future environment | Stop and report the BO registration and failed metadata retrieval. Do not fall back to direct REST write guidance. |
| A request proposes a direct REST write or an undocumented alternate route | Stop before execution and use the governed core.data-loader route. |
| Data Loader or Fusion rejects prepared setup data | Preserve the reported status and sanitized diagnostic. Correct the source data and restart the Data Loader validation and preview workflow. |
| A failure leaves the result of a previous load uncertain | Stop before retry. Use the governed Data Loader status and error workflow to reconcile the result. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Data Loader availability | Business-object metadata is unavailable. | Verify BO registration and configured-environment access before retrying. |
| Execution route | A request bypasses core.data-loader. | Use the governed Data Loader route. |
| Data Loader validation | Data Loader or Fusion rejects prepared data. | Correct the source data using the reported diagnostic. |
| Uncertain outcome | A prior submission may have completed. | Reconcile through the approved Data Loader status workflow before any retry. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Data Loader metadata is unavailable | Do not create direct REST POST, PATCH, or DELETE guidance as a fallback. |
| A retry follows an uncertain Data Loader failure | Do not resubmit until Data Loader status and read-only verification clarify the outcome. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UOMUSAGES.DATALOADER_HANDOFF | terminal | 30 | terminal | none | UOMUSAGES.CHECK_DATALOADER_READINESS | continue | The governed route and dependency readiness passed; hand off to core.data-loader. |
| UOMUSAGES.RETURN_ISSUES | terminal | 90 | terminal | none | none | continue | Any execution-route or dependency prerequisite is blocked or fails. |
