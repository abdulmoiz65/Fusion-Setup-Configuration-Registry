# Intersubinventory Parameters Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| Redwood `getall_destinationTypesLOVFetch.js` | `standardLookupsLOV`, lookup type `ORA_INV_TO_DESTINATION_TYPE`, `Meaning` display, and `LookupCode` value |
| Redwood `getall_TransferTypeLOVFetch.js` | `standardLookupsLOV`, lookup type `INV_IOP_TRANSIT_TYPE`, `Meaning` display, and `LookupCode` value |
| Redwood `getall_ReceiptRoutingLOVFetch.js` | `standardLookupsLOV`, lookup type `INV_IOP_ROUTING_TYPE`, `Meaning` display, and `LookupCode` value |
| Redwood service catalog | `/fscmRestApi/resources/11.13.18.05` service root and `standardLookupsLOV` resource |
| User-approved resolver scope | Only Destination Type, Transfer Type, and Receipt Routing; organization and subinventories remain BO-owned |
| Live FSM template | FSM route fields `DestinationType`, `TransferType`, and `ReceiptRouting` |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_intersub_destination_type | `DestinationTypeCode` code or `DestinationType` meaning is supplied | Code from `DestinationTypeCode`; meaning from `DestinationType` | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?fields=LookupCode,LookupType,Meaning&onlyData=true&q=LookupType='ORA_INV_TO_DESTINATION_TYPE' | LookupCode, LookupType, Meaning | Trim and compare case-insensitively and exactly; when both are supplied, both must identify one row | REST/Data Loader: `DestinationTypeCode`=`LookupCode`; FSM: `DestinationType`=`LookupCode`; retain returned code and meaning as evidence | Stop on no match, ambiguity, or representations resolving to different rows |
| resolve_intersub_transfer_type | `TransferTypeCode` code or `TransferType` meaning is supplied | Code from `TransferTypeCode`; meaning from `TransferType` | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?fields=LookupCode,LookupType,Meaning&onlyData=true&q=LookupType='INV_IOP_TRANSIT_TYPE' | LookupCode, LookupType, Meaning | Trim and compare case-insensitively and exactly; when both are supplied, both must identify one row | REST/Data Loader: `TransferTypeCode`=`LookupCode`; FSM: `TransferType`=`LookupCode`; retain returned code and meaning as evidence | Stop on no match, ambiguity, or representations resolving to different rows |
| resolve_intersub_receipt_routing | `ReceiptRoutingCode` code or `ReceiptRouting` meaning is supplied and routing applies | Code from `ReceiptRoutingCode`; meaning from `ReceiptRouting` | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?fields=LookupCode,LookupType,Meaning&onlyData=true&q=LookupType='INV_IOP_ROUTING_TYPE' | LookupCode, LookupType, Meaning | Trim and compare case-insensitively and exactly; when both are supplied, both must identify one row | REST/Data Loader: `ReceiptRoutingCode`=`LookupCode`; FSM: `ReceiptRouting`=`LookupCode`; retain returned code and meaning as evidence | Stop on no match, ambiguity, or representations resolving to different rows |

## BO-Owned References

| Field Group | Handling |
|---|---|
| Organization | Pass `OrganizationCode` and/or `OrganizationId` to the registered BO; FSM emits `OrganizationCode`; no task-local organization resolver |
| Source subinventory | Pass `FromSubinventory` to the BO; exact `All` normalization is owned by input validation; no task-local source resolver |
| Destination subinventory | Pass `ToSubinventory` to the BO; no task-local destination resolver |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Documented code or meaning field is supplied | Run only its documented resolver; validate a supplied canonical code instead of trusting it |
| One exact row matches | Fill the selected route's documented physical field and retain returned system values |
| Code and meaning are both supplied | Accept only when both identify the same returned row |
| No row or multiple rows match | Stop and request an unambiguous valid code or meaning; never fuzzy-match or select the first candidate |
| Organization or subinventory is supplied | Preserve it for BO/Data Loader and do not perform task-local REST resolution |
| Workflow selects a route | Emit only that route's physical field; do not infer route from whether user supplied a code or meaning field |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ISP.RESOLVE_DESTINATION_TYPE | step | 30 | reference_lookup | resolved->ISP.RESOLVE_TRANSFER_TYPE;skipped->ISP.RESOLVE_TRANSFER_TYPE;blocked->ISP.HANDLE_ERROR | ISP.CHECK_READINESS | stop | `DestinationTypeCode` code or `DestinationType` meaning is supplied |
| ISP.RESOLVE_TRANSFER_TYPE | step | 40 | reference_lookup | resolved->ISP.RESOLVE_RECEIPT_ROUTING;skipped->ISP.RESOLVE_RECEIPT_ROUTING;blocked->ISP.HANDLE_ERROR | ISP.RESOLVE_DESTINATION_TYPE | stop | `TransferTypeCode` code or `TransferType` meaning is supplied |
| ISP.RESOLVE_RECEIPT_ROUTING | step | 50 | reference_lookup | resolved->ISP.APPLY_DEFAULTS;skipped->ISP.APPLY_DEFAULTS;blocked->ISP.HANDLE_ERROR | ISP.RESOLVE_TRANSFER_TYPE | stop | `ReceiptRoutingCode` code or `ReceiptRouting` meaning is supplied and routing applies |
