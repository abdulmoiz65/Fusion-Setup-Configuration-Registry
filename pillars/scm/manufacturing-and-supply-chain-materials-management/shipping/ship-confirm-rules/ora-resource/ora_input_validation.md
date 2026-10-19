# Ship Confirm Rules Input Validation

Source: Ship Confirm Rules Redwood page and dynamic layout.

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| REST Boolean payload | Normalize Yes to true and No to false for CreateShipmentStageFlag, CloseShipmentFlag, and DeferInterfaceFlag. Preserve those canonical values for the default REST Data Loader handoff. | A flag is supplied and FSM was not explicitly selected | |
| REST effective-date timestamp normalization | Parse an ISO timestamp with an explicit offset, or an unambiguous local date or date-time in M/D/YY, M/D/YYYY, M/D/YY h:mm AM, or M/D/YYYY h:mm AM form. Interpret an input without an offset in Asia/Kolkata, convert it to UTC, and serialize it strictly as YYYY-MM-DDTHH:MM:SS.sss+00:00. The emitted value must contain exactly three millisecond digits and an explicit signed offset; do not emit a Z suffix. Preserve the represented instant for an input that already has an explicit offset. A date-only value uses 00:00:00 local time. For example, 9/10/26 6:39 AM serializes as 2026-09-10T01:09:00.000+00:00. | EffectiveStartDate or EffectiveEndDate is supplied and FSM was not explicitly selected | |
| FSM Boolean payload | Normalize Yes to Y and No to N in the exported `StageDelFlag`, `AcCloseDeliveryFlag`, and `AcDeferInterfaceFlag` columns. Do not emit REST JSON Boolean fields. | FSM Import was explicitly selected and a flag is supplied for an FSM CSV row | |
| FSM effective-date timestamp normalization | Parse an ISO timestamp with an explicit offset, or an unambiguous local date or date-time in M/D/YY, M/D/YYYY, M/D/YY h:mm AM, or M/D/YYYY h:mm AM form. Interpret an input without an offset in Asia/Kolkata, convert it to UTC, and serialize it in the exported FSM CSV format YYYY/MM/DD HH:MM:SS.0. Preserve the represented instant for an input that already has an explicit offset. A date-only value uses 00:00:00 local time. For example, 9/10/26 6:39 AM serializes as 2026/09/10 01:09:00.0. | FSM Import was explicitly selected and EffectiveStartDate or EffectiveEndDate is supplied for an FSM CSV row | |
| Effective-date range | Reject an EffectiveEndDate earlier than EffectiveStartDate after normalization. | Both effective dates are supplied | |
| FSM template column contract | Preserve the exported `WSH_SHIP_CONFIRM_RULE.csv` header and use its fields `ShipWithUi`, `ShipQuantityNotSpecifiedUi`, `PackingSlipStatus`, `JobSetName`, and `JobSetPackageName`. Do not substitute REST payload attribute names for these FSM columns. | FSM Import was explicitly selected | |
| FSM ActionFlag contract | Retain the `ActionFlag` value and semantics supplied by the exported template; block an absent or unsupported value rather than inferring a default. | FSM Import was explicitly selected | |
| Ship-with and quantity coupling | When ShipWith is A, do not send ShipQuantityNotSpecifiedOption. | ShipWith is A | |
| Ship With friendly value | Resolve a supplied ShipWith display value through resolve_ship_with_code. When both a display value and ShipWith code are supplied, they must resolve to the same code. | ShipWith is supplied as a display value | resolve_ship_with_code |
| Ship Quantity friendly value | Resolve a supplied ShipQuantityNotSpecifiedOption display value through resolve_ship_quantity_not_specified_option_code. When both a display value and code are supplied, they must resolve to the same code. | ShipWith is S and ShipQuantityNotSpecifiedOption is supplied as a display value | resolve_ship_quantity_not_specified_option_code |
| Packing Slip Status friendly value | Resolve a supplied PackingSlipStatus display value through resolve_packing_slip_status_code. When both a display value and code are supplied, they must resolve to the same code. | PackingSlipStatus is supplied as a display value | resolve_packing_slip_status_code |
| Shipping Document Job Set friendly value | Resolve a supplied JobSetName display value through resolve_shipping_document_job_set_name. When both a display value and backend value are supplied, they must resolve to the same JobSetName. | JobSetName is supplied as a display value | resolve_shipping_document_job_set_name |
| Friendly LOV display values | Require the backend code when a display value is supplied for ShipMethodCode. | A display value is supplied without its backend value | |

Fusion Data Loader and Fusion own required fields, dates, uniqueness, and all server-side validation for Ship Confirm Rules. FSM template semantics apply only to an explicitly selected FSM route.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SCR.VALIDATE_INPUT | step | 10 | validate_input | passed->SCR.RESOLVE_SHIP_WITH;failed->RETURN_ISSUES | none | stop | Creating or updating a Ship Confirm Rule |
