# Pick Wave Release Rules Reference Lookups

Source: Redwood Pick Wave Release Rules page, dynamic layout, and VBC service catalog.

## Core REST Delegation

All live lookup nodes in this file invoke `core.fusion-api.rest-api-client`.
The core service obtains OAuth credentials, adds the required REST framework
header, and owns the one cached-token 401 or 403 refresh/retry boundary. Each
resolver performs only its documented GET request, with no request body and no
create, update, delete, import, or loader action.

Before invocation, confirm the configured target environment, exact resolver
path, and supplied display value. Retain only sanitized resolver name, match
count, and mapped code in validation evidence. Never expose or persist tokens,
authorization headers, client secrets, token-cache contents, or raw sensitive
responses. Stop and report `auth_expired_or_invalid`,
`authorization_or_privilege`, `transport_or_environment`, or
`fusion_api_error` when the core call fails; do not retry a non-auth failure.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_release_status_code | A Release Status display value is supplied and ReleaseStatusCode is blank | ReleaseStatus | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='WSH_BACKORDERS_FLAG'&fields=LookupCode,LookupType,Meaning&onlyData=true | LookupCode, LookupType, Meaning | Trim outer whitespace and require exactly one case-insensitive exact Meaning match. When both a display value and ReleaseStatusCode are supplied, they must resolve to the same row. | ReleaseStatusCode: LookupCode | Zero or multiple matches, or conflicting display value and code, block preview. Do not fuzzy-match or select the first result. |
| resolve_destination_type_code | A Destination Type display value is supplied and DestinationTypeCode is blank | DestinationType | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='WSH_DESTINATION_TYPE_CODE'&fields=LookupCode,LookupType,Meaning&onlyData=true | LookupCode, LookupType, Meaning | Trim outer whitespace and require exactly one case-insensitive exact Meaning match. When both a display value and DestinationTypeCode are supplied, they must resolve to the same row. | DestinationTypeCode: LookupCode | Zero or multiple matches, or conflicting display value and code, block preview. Do not fuzzy-match or select the first result. |
| resolve_order_type_code | An Order Type display value is supplied and OrderTypeCode is blank | OrderType | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='ORA_WSH_ORDER_LINE_TYPE'%20and%20LookupCode%20IN%20('SALES_ORDER','TRANSFER_ORDER','TRANSFER_ORDER_RETURN','RETURN_TO_CUSTOMER','RETURN_TO_VENDOR','OUTSIDE_PROCESSING','UNREFERENCED_SUPPLIER_RETURN')&fields=LookupCode,LookupType,Meaning&onlyData=true | LookupCode, LookupType, Meaning | Trim outer whitespace and require exactly one case-insensitive exact Meaning match from the UI-supported code set. When both a display value and OrderTypeCode are supplied, they must resolve to the same row. | OrderTypeCode: LookupCode | Zero or multiple matches, a value outside the UI-supported code set, or conflicting display value and code, block preview. Do not fuzzy-match or select the first result. |
| resolve_shipment_priority_code | A Shipment Priority display value is supplied and ShipmentPriorityCode is blank | ShipmentPriority | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='WSH_SHIPPING_PRIORITY'&fields=LookupCode,LookupType,Meaning&onlyData=true | LookupCode, LookupType, Meaning | Trim outer whitespace and require exactly one case-insensitive exact Meaning match. When both a display value and ShipmentPriorityCode are supplied, they must resolve to the same row. | ShipmentPriorityCode: LookupCode | Zero or multiple matches, or conflicting display value and code, block preview. Do not fuzzy-match or select the first result. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A supported display value is absent and its corresponding code is supplied | The resolver is not applicable; retain the supplied code. |
| A supported display value resolves | Store only the returned LookupCode in the corresponding backend code field; retain the display value only in sanitized validation evidence. |
| A supported display value has zero, multiple, or conflicting matches | Stop before preview and request an exact display value or a matching backend code. |
| A different Data Loader friendly value requires code or ID conversion | Do not resolve it until a complete, approved resolver contract is available. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PWR.RESOLVE_RELEASE_STATUS | step | 20 | reference_lookup | resolved->PWR.RESOLVE_DESTINATION_TYPE;not-applicable->PWR.RESOLVE_DESTINATION_TYPE;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | PWR.VALIDATE_INPUT | stop | Resolve a supplied Release Status display value to ReleaseStatusCode. |
| PWR.RESOLVE_DESTINATION_TYPE | step | 30 | reference_lookup | resolved->PWR.RESOLVE_ORDER_TYPE;not-applicable->PWR.RESOLVE_ORDER_TYPE;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | PWR.RESOLVE_RELEASE_STATUS | stop | Resolve a supplied Destination Type display value to DestinationTypeCode. |
| PWR.RESOLVE_ORDER_TYPE | step | 40 | reference_lookup | resolved->PWR.RESOLVE_SHIPMENT_PRIORITY;not-applicable->PWR.RESOLVE_SHIPMENT_PRIORITY;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | PWR.RESOLVE_DESTINATION_TYPE | stop | Resolve a supplied Order Type display value to OrderTypeCode. |
| PWR.RESOLVE_SHIPMENT_PRIORITY | step | 50 | reference_lookup | resolved->PWR.VALIDATE_DEPENDENCIES;not-applicable->PWR.VALIDATE_DEPENDENCIES;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | PWR.RESOLVE_ORDER_TYPE | stop | Resolve a supplied Shipment Priority display value to ShipmentPriorityCode. |
