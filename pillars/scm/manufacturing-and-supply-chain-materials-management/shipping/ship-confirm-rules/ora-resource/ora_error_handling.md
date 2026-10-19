# Ship Confirm Rules Error Handling

Source: Ship Confirm Rules Redwood page and approved V3 authoring boundary.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A REST Boolean value is not true or false | Stop before default REST Data Loader handoff and normalize Yes or No to a canonical Boolean value. |
| REST Data Loader reports an EffectiveStartDate or EffectiveEndDate timestamp-format error | Rebuild the REST import artifact and verify the actual field value is YYYY-MM-DDTHH:MM:SS.sss+hh:mm, with exactly three millisecond digits and a signed offset. Do not send a Z suffix. For UTC, use +00:00; for example, 2026-09-29T18:30:00.000+00:00. |
| An FSM flag is not Y or N | When FSM Import was explicitly selected, stop before import and normalize Yes or No to the exported `StageDelFlag`, `AcCloseDeliveryFlag`, or `AcDeferInterfaceFlag` value. |
| FSM import reports an EffectiveStartDate or EffectiveEndDate timestamp-format error | When FSM Import was explicitly selected, rebuild the FSM ZIP from the export template and verify the actual CSV field value is YYYY/MM/DD HH:MM:SS.0 after UTC conversion. For example, use 2026/09/29 18:30:00.0. Do not send the REST ISO format or a Z suffix. |
| The FSM package is missing its template metadata or has changed CSV columns | When FSM Import was explicitly selected, stop before import. Re-export the template, preserve `ASM_SETUP_CSV_METADATA.xml`, and retain the exact `WSH_SHIP_CONFIRM_RULE.csv` header. |
| ActionFlag is missing or unsupported | When FSM Import was explicitly selected, stop before import and obtain the supported value from the exported template; do not invent a default. |
| ShipWith is A and a ship quantity option is supplied | Stop before Data Loader handoff and remove the quantity option. |
| A friendly LOV display value is supplied without a verified resolver | Stop before Data Loader handoff and request the backend code. ShipWith, ShipQuantityNotSpecifiedOption, PackingSlipStatus, and JobSetName use their approved resolvers. |
| Fusion Data Loader rejects the request | Preserve the redacted diagnostic through the Data Loader workflow; do not retry a live operation automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SCR.DONE | terminal | 70 | terminal | none | SCR.VALIDATE_DEPENDENCIES | stop | Input and dependency validation passed |
| RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | Input or dependency validation failed |
