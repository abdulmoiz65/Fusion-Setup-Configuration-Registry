# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Run Book task or business object is missing | Stop and request the missing input. |
| Source artifact is absent but an explicit supported parameter change is present | Generate the live assetSystemOptions update XLSX sample through core.data-loader; do not ask the user to create a workbook. |
| Source artifact and an explicit supported parameter change are both absent | Stop and request the missing input. |
| The active Run Book does not include assetSystemOptions in Data Loader scope | Stop; correct or recreate the Run Book scope. |
| A direct Fusion REST write is requested | Stop; route the request to core.data-loader through the active Run Book. |
| Data Loader validation, preview, approval, submission, or status reports a failure | Preserve the safe Data Loader diagnostic and follow its recovery guidance; do not submit another attempt automatically. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Asset Maintenance Parameters create or update | Do not construct a REST payload, select a REST endpoint, or call a direct Fusion REST write. |
| Data Loader scope or approval is absent | Do not submit a load. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AAMP.DATALOADER_GATE | decision | 40 | execution_gate | handoff_ready->AAMP.DATALOADER_HANDOFF;blocked->AAMP.HANDOFF_BLOCKED | AAMP.ENFORCE_DATALOADER_ROUTE | stop | Before core.data-loader preview or submission |
| AAMP.MISSING_INPUT | terminal | 90 | terminal | none | none | stop | Required input is missing or invalid |
| AAMP.SCOPE_BLOCKED | terminal | 91 | terminal | none | none | stop | Run Book scope does not include assetSystemOptions |
| AAMP.DIRECT_REST_BLOCKED | terminal | 92 | terminal | none | none | stop | Direct REST execution was requested |
| AAMP.HANDOFF_BLOCKED | terminal | 93 | terminal | none | none | stop | Data Loader preview or approval gate is not ready |
| AAMP.DATALOADER_HANDOFF | terminal | 100 | terminal | none | AAMP.DATALOADER_GATE | stop | Validated request is handed to core.data-loader |
