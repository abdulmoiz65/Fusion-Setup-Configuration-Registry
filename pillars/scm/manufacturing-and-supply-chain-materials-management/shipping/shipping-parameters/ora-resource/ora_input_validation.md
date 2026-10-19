# Shipping Parameters Input Validation

Source: Shipping Parameters Redwood page and dynamic layouts.

Fusion Data Loader and Fusion own mandatory fields, server-side domains, and all business-object validation. These rules only govern the approved standard-lookup friendly-value contract.

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Standard lookup friendly value or code | Accept either the documented display Meaning or the corresponding backend code for an approved standard-lookup field. When both are supplied, they must identify the same lookup row. | Any approved standard-lookup field is supplied | |
| Required on Packing Slip friendly selections | Accept the Redwood display selections for Required on Packing Slip and resolve them to DESCRP, REASON, or STATUS. ALL expands to all three selections. Do not infer a selection when the field is blank. | Required on Packing Slip is supplied as a friendly value | resolve_shipping_parameter_packing_attributes |
| BO-owned foreign key or non-standard LOV | Do not require a raw backend ID or run a task-level resolver. Preserve a supplied business value for Business Object or Data Loader derivation. When absent, leave the field absent; only a returned Fusion diagnostic or an explicit operation contract can require a value. Do not infer clear versus unchanged behavior. | A value is supplied or omitted for a field outside the approved standard lookup types | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SP.VALIDATE_INPUT | step | 10 | validate_input | passed->SP.RESOLVE_APPENDING_LIMIT;failed->RETURN_ISSUES | none | stop | Shipping Parameters input is prepared for Data Loader handoff |
