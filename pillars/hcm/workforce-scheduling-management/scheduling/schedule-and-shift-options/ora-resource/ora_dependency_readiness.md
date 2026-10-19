# Schedule and Shift Options Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Current setup options | Retrieve the complete current scheduleCommonSetups collection and identify the one row to update. |
| 2 | Lookup values | Resolve required lookup display values to provider-returned codes where the selected parameter uses a lookup. |
| 3 | Validation and design gates | Validate the normalized value and confirm the operation is an allowed item update. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| SSO-CURRENT-ROW | Current Schedule Common Setups row | Yes | Any update request | Lookup | Fusion scheduleCommonSetups collection | resolve_current_schedule_common_setups | SetupParamId is the documented item key and prevents updating an inferred row | Select the exact setup option to change | SetupParamId, ParameterCode, current ParameterValue |
| SSO-LOOKUP-CODE | Lookup code | Conditional | The selected parameter renders a lookup | Lookup | Technical-design lookup provider | resolve_setup_option_common_lookup | The update stores the selected value while the UI displays the provider meaning | Select one provider-returned value | ParameterValue |
| SSO-CONTENT-TYPE | Content Type selection | Yes | CONTENT_TYPE is updated | Lookup | Fusion contentTypesLOV provider | resolve_content_type | CONTENT_TYPE is mandatory | Select one or more supported Content Type values | ParameterValue |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The current row is identified and all applicable lookup and product-decision gates are satisfied | Yes |
| Blocked | A required value, exact row, resolved lookup, or product decision is missing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SSO.DEPENDENCIES | step | 2 | resolve_dependency | ready->SSO.LOOKUP.CURRENT;blocked->SSO.ERROR | SSO.VALIDATE | stop | Always |
