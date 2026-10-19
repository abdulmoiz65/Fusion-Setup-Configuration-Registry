# Inventory Transaction Reasons Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| Redwood inventoryTransactionReasonsV2 Type LOV action chain | Type LOV uses standardLookupsLOV with LookupType INV_REASON_TYPES and returns LookupCode, LookupType, and Meaning |
| Redwood inventoryTransactionReasonsV2 Context LOV action chain | Context LOV uses standardLookupsLOV with LookupType INV_REASON_CONTEXT and returns LookupCode, LookupType, and Meaning |
| Redwood inventoryTransactionReasonsV2 layout | Reason Context is dependent on ReasonType and is enabled only when ReasonType equals 1 |
| User decision | Retain both Type and Context display-value resolvers in the task skill |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_inventory_reason_type | ReasonTypeMeaning is supplied, ReasonType is blank, or both values need comparison | ReasonTypeMeaning, ReasonType | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='INV_REASON_TYPES'&orderBy=Meaning&fields=LookupCode,LookupType,Meaning&onlyData=true | LookupCode, LookupType, Meaning | Trim outer whitespace and require one case-insensitive exact Meaning match for ReasonTypeMeaning, or one case-insensitive exact LookupCode match for ReasonType. When both are supplied, they must identify the same row. | ReasonType: LookupCode; ReasonTypeMeaning: Meaning | Stop and ask for a valid Type display value or ReasonType code; do not fuzzy-match, use the UI contains filter as a final match, or choose the first candidate |
| resolve_inventory_reason_context | ReasonContext is supplied, ReasonContextCode is blank, or both values need comparison | ReasonContext, ReasonContextCode, ReasonType | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='INV_REASON_CONTEXT'&fields=LookupCode,LookupType,Meaning&onlyData=true | LookupCode, LookupType, Meaning | Run only after ReasonType equals 1. Trim outer whitespace and require one case-insensitive exact Meaning match for ReasonContext, or one case-insensitive exact LookupCode match for ReasonContextCode. When both are supplied, they must identify the same row. | ReasonContextCode: LookupCode; ReasonContext: Meaning | Stop and ask for a valid Context display value or ReasonContextCode; do not fuzzy-match, use the UI contains filter as a final match, or choose the first candidate |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Reason Type display value is omitted and ReasonType is supplied | Do not resolve by Meaning; retain the supplied implementation code after exact consistency validation when a display value is also supplied |
| Reason Context is omitted | Do not run the Context lookup |
| Reason Context is supplied | Resolve Type first, require ReasonType equals 1, then resolve one exact Context entry |
| A supplied display value and code identify different entries | Stop with a conflicting-input issue; do not select either value automatically |
| Lookup is unavailable, has no match, or is ambiguous | Classify as a lookup readiness issue and stop before Data Loader handoff |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ITR.RESOLVE_REASON_TYPE | decision | 20 | reference_lookup | resolved->ITR.RESOLVE_REASON_CONTEXT;not_required->ITR.RESOLVE_REASON_CONTEXT;blocked->ITR.HANDLE_ERROR;failure->ITR.HANDLE_ERROR | ITR.VALIDATE_INPUT | stop | Resolve a supplied Type display value or compare supplied Type code and display value |
| ITR.RESOLVE_REASON_CONTEXT | decision | 30 | reference_lookup | resolved->ITR.CHECK_DEPENDENCIES;not_required->ITR.CHECK_DEPENDENCIES;blocked->ITR.HANDLE_ERROR;failure->ITR.HANDLE_ERROR | ITR.RESOLVE_REASON_TYPE | stop | Resolve a supplied Context display value after Type is available |
