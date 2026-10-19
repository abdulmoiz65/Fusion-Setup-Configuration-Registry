# Interorganization Parameters Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| Redwood Interorganization Parameters lookup action chains | Confirms genericLookupsLOV, version 11.13.18.05, LookupType filters, and Meaning display values |
| Redwood Interorganization Parameters payload shaping | Confirms the five implementation fields selected by the page |
| User-approved Data Loader mapping | Requires LookupCode as the canonical value for Data Loader handoff and permits supplied LookupCode or Meaning |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_interorg_transfer_type | A Transfer Type value is supplied | Supplied LookupCode or Meaning for Transfer Type | /fscmRestApi/resources/11.13.18.05/genericLookupsLOV?fields=LookupCode,LookupType,Meaning,Description,ApplicationCode,Tag&onlyData=true&q=LookupType='INV_IOP_TRANSIT_TYPE' | LookupCode, LookupType, Meaning, Description, ApplicationCode, Tag | Trim each supplied representation and compare case-insensitively and exactly against both LookupCode and Meaning; when code and meaning are supplied, both must resolve to one row | IntransitType: LookupCode; returned Meaning and LookupCode retained as validation evidence | Stop on no match, ambiguity, or representations resolving to different rows |
| resolve_interorg_inventory_receipt_routing | An inventory Receipt Routing value is supplied | Supplied LookupCode or Meaning for inventory Receipt Routing | /fscmRestApi/resources/11.13.18.05/genericLookupsLOV?fields=LookupCode,LookupType,Meaning,Description,ApplicationCode,Tag&onlyData=true&q=LookupType='INV_IOP_ROUTING_TYPE' | LookupCode, LookupType, Meaning, Description, ApplicationCode, Tag | Trim each supplied representation and compare case-insensitively and exactly against both LookupCode and Meaning; when code and meaning are supplied, both must resolve to one row | RoutingHeaderId: LookupCode; returned Meaning and LookupCode retained as validation evidence | Stop on no match, ambiguity, or representations resolving to different rows |
| resolve_interorg_inventory_cancel_backorders | An inventory Cancel Backorders value is supplied | Supplied LookupCode or Meaning for inventory Cancel Backorders | /fscmRestApi/resources/11.13.18.05/genericLookupsLOV?fields=LookupCode,LookupType,Meaning,Description,ApplicationCode,Tag&onlyData=true&q=LookupType='ORA_INV_TO_FILLKILL_OPTIONS' | LookupCode, LookupType, Meaning, Description, ApplicationCode, Tag | Trim each supplied representation and compare case-insensitively and exactly against both LookupCode and Meaning; when code and meaning are supplied, both must resolve to one row | FillKillInvToLookup: LookupCode; returned Meaning and LookupCode retained as validation evidence | Stop on no match, ambiguity, or representations resolving to different rows |
| resolve_interorg_expense_receipt_routing | An expense Receipt Routing value is supplied | Supplied LookupCode or Meaning for expense Receipt Routing | /fscmRestApi/resources/11.13.18.05/genericLookupsLOV?fields=LookupCode,LookupType,Meaning,Description,ApplicationCode,Tag&onlyData=true&q=LookupType='INV_IOP_ROUTING_TYPE' | LookupCode, LookupType, Meaning, Description, ApplicationCode, Tag | Trim each supplied representation and compare case-insensitively and exactly against both LookupCode and Meaning; when code and meaning are supplied, both must resolve to one row | ExpenseDestReceiptRouting: LookupCode; returned Meaning and LookupCode retained as validation evidence | Stop on no match, ambiguity, or representations resolving to different rows |
| resolve_interorg_expense_cancel_backorders | An expense Cancel Backorders value is supplied | Supplied LookupCode or Meaning for expense Cancel Backorders | /fscmRestApi/resources/11.13.18.05/genericLookupsLOV?fields=LookupCode,LookupType,Meaning,Description,ApplicationCode,Tag&onlyData=true&q=LookupType='ORA_INV_TO_FILLKILL_OPTIONS' | LookupCode, LookupType, Meaning, Description, ApplicationCode, Tag | Trim each supplied representation and compare case-insensitively and exactly against both LookupCode and Meaning; when code and meaning are supplied, both must resolve to one row | FillKillExpToLookup: LookupCode; returned Meaning and LookupCode retained as validation evidence | Stop on no match, ambiguity, or representations resolving to different rows |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A selected lookup field has a supplied code or friendly value | Run only the resolver documented for that field; do not trust a supplied canonical code without validating it |
| Lookup returns one exact matched row | Fill the documented LookupCode and retain the returned system values in validation evidence |
| Code and friendly values are both supplied | Accept them only when both match the same returned row |
| Lookup returns no or multiple exact matches | Stop and request a valid, unambiguous value; never fuzzy-match or select the first result |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IOP.RESOLVE_TRANSFER_TYPE | step | 30 | reference_lookup | resolved->IOP.RESOLVE_INVENTORY_RECEIPT_ROUTING;skipped->IOP.RESOLVE_INVENTORY_RECEIPT_ROUTING;blocked->IOP.HANDLE_ERROR | IOP.CHECK_READINESS | stop | A Transfer Type code or friendly value is supplied |
| IOP.RESOLVE_INVENTORY_RECEIPT_ROUTING | step | 40 | reference_lookup | resolved->IOP.RESOLVE_INVENTORY_CANCEL_BACKORDERS;skipped->IOP.RESOLVE_INVENTORY_CANCEL_BACKORDERS;blocked->IOP.HANDLE_ERROR | IOP.RESOLVE_TRANSFER_TYPE | stop | An inventory Receipt Routing code or friendly value is supplied |
| IOP.RESOLVE_INVENTORY_CANCEL_BACKORDERS | step | 50 | reference_lookup | resolved->IOP.RESOLVE_EXPENSE_RECEIPT_ROUTING;skipped->IOP.RESOLVE_EXPENSE_RECEIPT_ROUTING;blocked->IOP.HANDLE_ERROR | IOP.RESOLVE_INVENTORY_RECEIPT_ROUTING | stop | An inventory Cancel Backorders code or friendly value is supplied |
| IOP.RESOLVE_EXPENSE_RECEIPT_ROUTING | step | 60 | reference_lookup | resolved->IOP.RESOLVE_EXPENSE_CANCEL_BACKORDERS;skipped->IOP.RESOLVE_EXPENSE_CANCEL_BACKORDERS;blocked->IOP.HANDLE_ERROR | IOP.RESOLVE_INVENTORY_CANCEL_BACKORDERS | stop | An expense Receipt Routing code or friendly value is supplied |
| IOP.RESOLVE_EXPENSE_CANCEL_BACKORDERS | step | 70 | reference_lookup | resolved->IOP.DATA_LOADER_HANDOFF;skipped->IOP.DATA_LOADER_HANDOFF;blocked->IOP.HANDLE_ERROR | IOP.RESOLVE_EXPENSE_RECEIPT_ROUTING | stop | An expense Cancel Backorders code or friendly value is supplied |
