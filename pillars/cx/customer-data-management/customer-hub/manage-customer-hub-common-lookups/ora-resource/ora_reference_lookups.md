# Reference Lookups

## Task Lookup Inventory

| Lookup Type | Scope |
|---|---|
| ZCH_BATCH_TYPE | Customer Hub batch type |
| ZCH_VALUE_CODE_OP | Code comparison operator |
| ZCH_VALUE_STRING_OP | String comparison operator |
| ZCH_VALUE_NUMBER_OP | Number comparison operator |
| ZCH_BATCH_STATUS_CODE | Customer Hub batch status |
| ZCH_VALUE_DATE_OP | Date comparison operator |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| CHC.LOOKUP | resolve_customer_hub_common_lookup_type | Read/mutation names a type/code or setup-data routing validates membership | LookupType and optional LookupCode | `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}` with child lookupCodes or exact item URI | LookupType, Meaning, Description, CustomizationLevel, code values, ModuleId, CreatedBy, LastUpdatedBy, links | Exact member and exact type/code only; `CreatedBy == SEED_DATA_FROM_APPLICATION` proves seeded origin | Standard category, level, values, seed origin, links, and describe fields | Stop with metadata mismatch; never try another category or infer membership |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| General read | Return the closed 6-type inventory and current read results. |
| Exact unconfirmed type | Refuse; the task has no add-type operation. |
| Mutation | Return evidence to the shared executor after exact preview/approval; no task-local HTTP write node exists. |
| Import | Preserve bytes and require Core Data Loader Task Hook validation bound to exact SHA-256. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHC.LOOKUP | decision | 20 | reference_lookup | resolved_or_not_needed->CHC.DEFAULTS;missing_or_ambiguous->CHC.ERROR | CHC.VALIDATE | stop | Resolve exact task membership and current evidence when applicable. |
