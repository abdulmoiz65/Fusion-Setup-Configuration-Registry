# Shipping Cost Types Input Validation

Source: Shipping Cost Types Redwood dynamic layout, create payload shaping, and approved LOV contracts.

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Shipping Cost Type Category friendly value | Accept a category Meaning or LookupCode. Delegate live resolution and population of ShippingCostTypeCategoryCode to the routed core.data-loader workflow. When both forms are supplied, the core workflow must require them to identify one identical LookupCode. | A category display value or code is supplied | |
| Currency friendly value | Accept a currency Name or CurrencyCode. Delegate live resolution and population of CurrencyCode to the routed core.data-loader workflow. When both forms are supplied, the core workflow must require them to identify one identical CurrencyCode. | A currency display value or code is supplied | |
| REST effective-date timestamp normalization | For every supplied datetime field, StartDateActive and EndDateActive, require the final XLSX and DAT value to be a literal string in YYYY-MM-DDTHH:mm:ss.sss+00:00 format. Convert the confirmed Redwood UTC display form M/D/YY h:mm AM/PM and a UTC suffix Z to that form. Preserve a supplied value only when it already has the required explicit +00:00 offset. Do not use an Excel native date/time cell or a datetime object, and reject a date-only, offset-free, Z-suffixed, or other-offset value; do not infer a different time zone or time of day. | StartDateActive or EndDateActive is supplied | |

Fusion Data Loader and Fusion own required-field, numeric, uniqueness, and server-side validation. No local default or normalization is defined for ShippingCostType, ShippingCostTypeDescription, Amount, dynamic flexfields, derived display fields, or audit fields.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SCT.VALIDATE_INPUT | step | 10 | validate_input | passed->SCT.DONE;failed->RETURN_ISSUES | none | stop | Creating or updating a Shipping Cost Type |
