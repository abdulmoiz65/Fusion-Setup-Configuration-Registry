# Reference Lookups

## Task Lookup Inventory
| Lookup Type | Meaning | Configuration Level | Validated Scope |
|---|---|---|---|
| ZCH_CLNS_PROCESS_OPTION | Cleanse Process Option | System | Data-cleansing batch processing modes |
| ZCH_CLNS_PROCESS_STATUS_CODE | Cleansing Result Process Status | System | Processing status of cleansing results |
| ZCH_CLNS_LOC_STATUS_CODE | Cleanse Result Status | System | Status of a data-cleansing batch record |
| ZCH_CLNS_OBJ_ACCOUNT | Cleanse Account Attributes | System | Account attributes available to cleansing selection criteria |
| ZCH_CLNS_OBJ_PARTY | Cleanse Party Attributes | System | Party attributes available to cleansing selection criteria |
| ZCH_CLNS_OBJ_PARTYUSG_FR | Cleanse Party Usage Filter Attributes | System | Party-usage filter attributes available to cleansing selection criteria |
| ZCH_CLNS_OBJECT_TYPE | Cleanse Object Type | System | Selection object for data cleansing |
| ZCH_CLNS_OBJ_LOCATION | Cleanse Location Attributes | System | Location attributes available to cleansing selection criteria |
| ZCH_CLNS_OBJ_PARTY_USG | Cleanse Party Usage Attributes | System | Party-usage attributes available to cleansing selection criteria |
| ZCH_CLNS_TARGET | Cleanse Target Object | System | Target objects supported by data cleansing |

## Live Lookups
| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| DCL.LOOKUP | resolve_data_cleansing_lookup | Read or update names a type/code | LookupType and optional LookupCode | /fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}?expand=lookupCodes or exact returned item URI | Type, code values, level, module, security, seed fields, links, and code describe | Exact inventory member and exact code only | Current values, level, seed evidence, links, and writable fields | Stop with catalog_or_metadata_mismatch |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Read | Return current exact type or code values through Apps Common Standard Lookups. |
| Meaning update | Return exact evidence for an approval-bound, current-describe-supported PATCH through Apps Common; no task-local HTTP node exists. |
| Any other mutation | Refuse because all 10 task members are System lookups. |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCL.LOOKUP | decision | 20 | reference_lookup | resolved_or_not_needed->DCL.DEFAULTS;missing_or_ambiguous->DCL.ERROR | DCL.VALIDATE | stop | Resolve exact task membership and current evidence. |
