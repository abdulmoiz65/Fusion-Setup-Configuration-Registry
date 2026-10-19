# Pick Slip Grouping Rules Error Handling

## Error Situations

| Situation | Classification | Required action |
|---|---|---|
| A supplied grouping option is not a supported representation | Input validation | Stop before Data Loader handoff and request `Y`, `N`, `yes`, `no`, `true`, or `false`. |
| A supplied catalog value is blank | Input validation | Stop before handoff and request a nonblank catalog value; do not ask for a catalog ID. |
| A supplied date has no year | Input validation | Ask the user whether the date is in the current year; do not infer the year. |
| A supplied numeric date is ambiguous | Input validation | Ask the user to provide an unambiguous date; do not select a date order. |
| Data Loader or Fusion rejects the prepared record | Data Loader or Fusion validation | Preserve the reported diagnostic and correct the source through the governed Data Loader workflow. |

## Retry Boundary

| Condition | What Must Not Happen |
|---|---|
| Date information is missing or ambiguous | Do not format, default, or submit the date. |
| A grouping-option value is unsupported | Do not infer `Y` or `N`. |
| Data Loader reports a failed or uncertain request | Do not resubmit until the Data Loader status and diagnostic have been reviewed. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| PICKSLIPGROUPING.DATALOADER_HANDOFF | terminal | 30 | terminal | none | PICKSLIPGROUPING.CHECK_HANDOFF_READINESS | continue | Local normalization and readiness checks passed; hand off the normalized source to core.data-loader for its governed validation, approval, and import workflow. |
| PICKSLIPGROUPING.RETURN_ISSUES | terminal | 90 | terminal | none | none | continue | Any local input validation, clarification, or handoff-readiness condition is blocked. |
