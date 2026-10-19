# Reservation Priority for Sales Orders Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_reservation_priority_attribute | A Reservation Priority attribute is supplied | Supplied attribute name or code | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder&LookupType=ORA_FOM_RESERVE_PRIORITY_ATTR` | LookupCode and the finder response fields needed to evaluate the supplied attribute | Require exactly one exact match for the supplied attribute name or code; never fuzzy-match or select the first result | Returned attribute `LookupCode`, stored as the Reservation Priority attribute in the export-derived field | Zero or multiple matches block package preparation; do not store the submitted attribute value |
| resolve_reservation_priority_order_type | Order Type is supplied as a Reservation Priority attribute | Supplied Order Type value | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder&LookupType=ORA_DOO_ORDER_TYPES` | LookupCode and the finder response fields needed to evaluate the supplied value | Require exactly one exact match for the supplied Order Type value; never fuzzy-match or select the first result | `LookupCode`, to be stored in the export-derived field for the selected Reservation Priority section | Zero or multiple matches block package preparation; do not store the submitted display value |
| resolve_reservation_priority_demand_class | Demand Class is supplied as a Reservation Priority attribute | Supplied Demand Class value | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder&LookupType=ORA_DOO_DEMAND_CLASS` | LookupCode and the finder response fields needed to evaluate the supplied value | Require exactly one exact match for the supplied Demand Class value; never fuzzy-match or select the first result | `LookupCode`, to be stored in the export-derived field for the selected Reservation Priority section | Zero or multiple matches block package preparation; do not store the submitted display value |
| resolve_reservation_priority_sales_channel | Sales Channel is supplied as a Reservation Priority attribute | Supplied Sales Channel value | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder&LookupType=ORA_QP_CHANNEL_METHODS` | LookupCode and the finder response fields needed to evaluate the supplied value | Require exactly one exact match for the supplied Sales Channel value; never fuzzy-match or select the first result | `LookupCode`, to be stored in the export-derived field for the selected Reservation Priority section | Zero or multiple matches block package preparation; do not store the submitted display value |
| resolve_reservation_priority_customer_class | Customer Class is supplied as a Reservation Priority attribute | Supplied Customer Class value | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder&LookupType=CUSTOMER%20CLASS` | LookupCode and the finder response fields needed to evaluate the supplied value | Require exactly one exact match for the supplied Customer Class value; never fuzzy-match or select the first result | `LookupCode`, to be stored in the export-derived field for the selected Reservation Priority section | Zero or multiple matches block package preparation; do not store the submitted display value |
| resolve_reservation_priority_shipment_priority | Shipment Priority is supplied as a Reservation Priority attribute | Supplied Shipment Priority value | `/fscmRestApi/resources/11.13.18.05/standardLookupsLOV?finder=LookupTypeFinder&LookupType=WSH_SHIPPING_PRIORITY` | LookupCode and the finder response fields needed to evaluate the supplied value | Require exactly one exact match for the supplied Shipment Priority value; never fuzzy-match or select the first result | `LookupCode`, to be stored in the export-derived field for the selected Reservation Priority section | Zero or multiple matches block package preparation; do not store the submitted display value |
| resolve_reservation_priority_customer | Customer is supplied as a Reservation Priority attribute | Supplied Customer value | `/fscmRestApi/resources/11.13.18.05/omCustomersLOV` | `PartyId` and the response fields needed to evaluate the supplied value | Require exactly one exact match for the supplied Customer value; never fuzzy-match or select the first result | `PartyId`, to be stored in the export-derived field for the selected Reservation Priority section | Zero or multiple matches block package preparation; do not store the submitted display value |

## Live Lookups

Use `core.fusion-api.rest-api-client` for these read-only GET requests after
the fresh FSM export and before package preparation. Keep the responses in
sanitized validation evidence and reconcile them with the export-derived CSV
baseline; do not use a REST response as an import package source.

| Resolver | Runs When | Method | Resource Path | Query Parameters | Requested Fields | Values to Validate | If the Read Fails |
|---|---|---|---|---|---|---|---|
| fetch_reservation_priority_default_sort_orders | A default sorting order is created, changed, or validated | GET | `/fscmRestApi/resources/11.13.18.05/omReservationPriorities` | `q=RESERVATION_PRIORITY`; `fields=defaultSortingOrder`; `limit=1000`; `offset=0`; `onlyData=true`; `totalResults=true` | `defaultSortingOrder` child object and total-result count | Existing default sorting orders for the Reservation Priority preference | Stop before package preparation; record a transport, auth/authz, or Fusion API diagnostic and do not infer live state. |
| fetch_reservation_priority_rules | A Reservation Priority sorting rule is created, changed, or validated | GET | `/fscmRestApi/resources/11.13.18.05/omReservationPriorities` | `q=RESERVATION_PRIORITY`; `fields=ruleDetails`; `limit=1000`; `offset=0`; `onlyData=true`; `totalResults=true` | `ruleDetails` child object and total-result count | Existing Reservation Priority rules | Stop before package preparation; record a transport, auth/authz, or Fusion API diagnostic and do not infer live state. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Reservation Priority attribute is absent | `resolve_reservation_priority_attribute` is not applicable; continue without a lookup. |
| Reservation Priority attribute lookup succeeds | Store only the returned attribute `LookupCode`; retain the supplied name or code only in sanitized validation evidence. |
| Reservation Priority attribute lookup is zero-match or ambiguous | Stop before package preparation and request an exact attribute name or code from `ORA_FOM_RESERVE_PRIORITY_ATTR`. |
| Order Type is absent | `resolve_reservation_priority_order_type` is not applicable; continue without a lookup. |
| Order Type lookup succeeds | Store only the returned `LookupCode`; retain the supplied display value only in sanitized validation evidence. |
| Order Type lookup is zero-match or ambiguous | Stop before package preparation and request an exact Order Type value. |
| Demand Class is absent | `resolve_reservation_priority_demand_class` is not applicable; continue without a lookup. |
| Demand Class lookup succeeds | Store only the returned `LookupCode`; retain the supplied display value only in sanitized validation evidence. |
| Demand Class lookup is zero-match or ambiguous | Stop before package preparation and request an exact Demand Class value. |
| Sales Channel is absent | `resolve_reservation_priority_sales_channel` is not applicable; continue without a lookup. |
| Sales Channel lookup succeeds | Store only the returned `LookupCode`; retain the supplied display value only in sanitized validation evidence. |
| Sales Channel lookup is zero-match or ambiguous | Stop before package preparation and request an exact Sales Channel value. |
| Customer Class is absent | `resolve_reservation_priority_customer_class` is not applicable; continue without a lookup. |
| Customer Class lookup succeeds | Store only the returned `LookupCode`; retain the supplied display value only in sanitized validation evidence. |
| Customer Class lookup is zero-match or ambiguous | Stop before package preparation and request an exact Customer Class value. |
| Shipment Priority is absent | `resolve_reservation_priority_shipment_priority` is not applicable; continue without a lookup. |
| Shipment Priority lookup succeeds | Store only the returned `LookupCode`; retain the supplied display value only in sanitized validation evidence. |
| Shipment Priority lookup is zero-match or ambiguous | Stop before package preparation and request an exact Shipment Priority value. |
| Customer is absent | `resolve_reservation_priority_customer` is not applicable; continue without a lookup. |
| Customer lookup succeeds | Store only the returned `PartyId`; retain the supplied display value only in sanitized validation evidence. |
| Customer lookup is zero-match or ambiguous | Stop before package preparation and request an exact Customer value. |
| Default sorting-order read succeeds | Reconcile the returned `defaultSortingOrder` child object and total-result count with the fresh exported Order Preferences Details baseline before package preparation. |
| Reservation Priority rule read succeeds | Reconcile the returned `ruleDetails` child object and total-result count with the fresh exported Order Preference Rules baseline before package preparation. |
| A required live configuration read fails or is incomplete | Stop before package preparation; persist a sanitized diagnostic classified as transport/environment, auth/authz, or Fusion API. Do not substitute a stale response or infer the missing state. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RESERVATION_PRIORITY.RESOLVE_ATTRIBUTE | step | 12 | reference_lookup | resolved->RESERVATION_PRIORITY.RESOLVE_ORDER_TYPE;not-applicable->RESERVATION_PRIORITY.RESOLVE_ORDER_TYPE;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | RESERVATION_PRIORITY.VALIDATE_FSM_PACKAGE | stop | Resolve a supplied Reservation Priority attribute through `ORA_FOM_RESERVE_PRIORITY_ATTR` and persist only its `LookupCode`. |
| RESERVATION_PRIORITY.RESOLVE_ORDER_TYPE | step | 15 | reference_lookup | resolved->RESERVATION_PRIORITY.RESOLVE_DEMAND_CLASS;not-applicable->RESERVATION_PRIORITY.RESOLVE_DEMAND_CLASS;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | RESERVATION_PRIORITY.RESOLVE_ATTRIBUTE | stop | Resolve Order Type only when it is supplied as a Reservation Priority attribute. |
| RESERVATION_PRIORITY.RESOLVE_DEMAND_CLASS | step | 18 | reference_lookup | resolved->RESERVATION_PRIORITY.RESOLVE_SALES_CHANNEL;not-applicable->RESERVATION_PRIORITY.RESOLVE_SALES_CHANNEL;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | RESERVATION_PRIORITY.RESOLVE_ORDER_TYPE | stop | Resolve Demand Class only when it is supplied as a Reservation Priority attribute. |
| RESERVATION_PRIORITY.RESOLVE_SALES_CHANNEL | step | 19 | reference_lookup | resolved->RESERVATION_PRIORITY.RESOLVE_CUSTOMER_CLASS;not-applicable->RESERVATION_PRIORITY.RESOLVE_CUSTOMER_CLASS;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | RESERVATION_PRIORITY.RESOLVE_DEMAND_CLASS | stop | Resolve Sales Channel only when it is supplied as a Reservation Priority attribute. |
| RESERVATION_PRIORITY.RESOLVE_CUSTOMER_CLASS | step | 20 | reference_lookup | resolved->RESERVATION_PRIORITY.RESOLVE_SHIPMENT_PRIORITY;not-applicable->RESERVATION_PRIORITY.RESOLVE_SHIPMENT_PRIORITY;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | RESERVATION_PRIORITY.RESOLVE_SALES_CHANNEL | stop | Resolve Customer Class only when it is supplied as a Reservation Priority attribute. |
| RESERVATION_PRIORITY.RESOLVE_SHIPMENT_PRIORITY | step | 21 | reference_lookup | resolved->RESERVATION_PRIORITY.RESOLVE_CUSTOMER;not-applicable->RESERVATION_PRIORITY.RESOLVE_CUSTOMER;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | RESERVATION_PRIORITY.RESOLVE_CUSTOMER_CLASS | stop | Resolve Shipment Priority only when it is supplied as a Reservation Priority attribute. |
| RESERVATION_PRIORITY.RESOLVE_CUSTOMER | step | 22 | reference_lookup | resolved->RESERVATION_PRIORITY.FSM_IMPORT_PREVIEW;not-applicable->RESERVATION_PRIORITY.FSM_IMPORT_PREVIEW;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | RESERVATION_PRIORITY.RESOLVE_SHIPMENT_PRIORITY | stop | Resolve Customer only when it is supplied as a Reservation Priority attribute and persist only its PartyId. |
