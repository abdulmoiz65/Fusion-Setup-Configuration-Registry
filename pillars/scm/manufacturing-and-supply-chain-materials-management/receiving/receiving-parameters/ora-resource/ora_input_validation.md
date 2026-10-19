# Receiving Parameters Input Validation

## Local Normalization Scope

Data Loader and Fusion own required-field, data-type, domain, and cross-field validation for `receivingOrganizationParameters`. This task-local validation only normalizes approved friendly values before Data Loader handoff.

| Input Condition | Local Handling | If Invalid |
|---|---|---|
| A documented boolean field is supplied as `yes`, `y`, `true`, or `Y` | Normalize to the lowercase JSON wire boolean `true`, not the string `"true"` or Python-style `True`. | Stop and request a supported boolean value. |
| A documented boolean field is supplied as `no`, `n`, `false`, or `N` | Normalize to the lowercase JSON wire boolean `false`, not the string `"false"` or Python-style `False`. | Stop and request a supported boolean value. |
| Receipt number generation is supplied as `Automatic` or `Manual` | Normalize to `AUTOMATIC` or `MANUAL`. | Stop and request Automatic or Manual, or the corresponding backend code. |
| Receipt number type is supplied as `Alphanumeric` or `Numeric` | Normalize to `ALPHANUMERIC` or `NUMERIC`. | Stop and request Alphanumeric or Numeric, or the corresponding backend code. |
| A supported standard lookup field is supplied as a display value | Resolve it through `resolve_receiving_parameter_standard_lookup` before Data Loader handoff | Stop when the resolver reports no exact match, ambiguity, inactive/disabled value where returned, or a conflict with a supplied code. |
| A supported standard lookup field is supplied as a code | Preserve the supplied code; do not independently revalidate its Fusion domain. | Data Loader/Fusion validates the code. |
| A Job Set value is supplied as either `JobSetDisplayName` or `JobSetName` | Resolve it through `resolve_receiving_parameter_job_set` before Data Loader handoff. | Stop when the resolver reports no exact match, ambiguity, a lookup read failure, or conflicting supplied display and backend values. |
| A field outside the documented standard lookup and Job Set groups is supplied | Preserve it for the registered business object. | Data Loader/Fusion validates it. |

## Boolean Fields

| Section | Backend Fields |
|---|---|
| Receipt Routing | `AllowRoutingOverrideFlag`, `UseQualityInspectionPlanFlag` |
| Receipt Processing | `AllowSubstituteReceiptsFlag`, `AllowUnorderedReceiptsFlag`, `EnforceBlindReceivingFlag`, `IncludeClosedPOsForReceiptsFlag`, `ProcessAllASNLinesTogetherFlag`, `PublishTransactionalBusinessEventsFlag` |
| Printing | `InterfaceDropShipsToShippingFlag`, `InterfaceReturnsToShippingFlag`, `InterfaceRMAsToShippingFlag`, `PrintReceiptTravelerFlag`, `PrintUsingDocumentOutputPreferencesFlag` |
| Receipt Deliveries | `AutocreateDeliveriesForExpenseFlag`, `AutocreateDeliveriesForPARLocationFlag` |
| Lot and Serial Number Processing | `AllowDefaultingLotsAndSerialsFromASNFlag`, `AllowDefaultingLotsAndSerialsFromTOFlag`, `LotAndSerialNumbersRequiredAtReceiptFlag` |
| RMA | `RMAValidateSerialNumbersFlag` |

Do not add local dependency behavior for checkbox combinations, Default Delivery Cart, or organization values; the registered business object owns those behaviors. Job Set resolution is limited to the documented read-only resolver.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| RCV_PARAMS.NORMALIZE_INPUT | step | 10 | validate_input | normalized->RCV_PARAMS.CHECK_READINESS;blocked->RCV_PARAMS.RETURN_ISSUES | none | stop | A Receiving Parameters request contains a documented friendly boolean, receipt generation/type value, standard lookup display value, or Job Set display/name value. |
