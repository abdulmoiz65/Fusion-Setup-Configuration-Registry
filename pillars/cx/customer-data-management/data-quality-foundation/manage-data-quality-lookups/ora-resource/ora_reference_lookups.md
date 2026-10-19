# Reference Lookups

## Task Lookup Inventory

| Lookup Type | Scope |
|---|---|
| ZCQ_IIR_MATCH_TOLERANCE | Match tolerance |
| ZCQ_ADDR_CLEANSED_STATUS | Address cleansing status |
| ZCQ_BATCH_MATCH_MODE | Batch match mode |
| ZCQ_PARAMETER_LEVEL | Parameter level |
| ZCQ_PARAMETER_TYPE | Parameter type |
| ZCQ_SORT_BY_SCORE | Sort by score |
| ZCQ_BATCH_PURGE_MODE | Batch purge mode |
| ZCQ_BATCH_STATUS | Batch status |
| ZCQ_BATCH_TYPE | Batch type |
| ZCQ_IIR_ASM_CHARSET | IIR character set |
| ZCQ_IIR_ASM_FORCE_COUNTRY | IIR forced country |
| ZCQ_IIR_ASM_VAL_MODE | IIR validation mode |
| ZCQ_OPERATIONS | Data quality operations |
| ZCQ_ORG_MATCH_OPTION_CODE | Organization match option |
| ZCQ_ASM_ATTRIBUTES | Address cleansing attributes |
| ZCQ_BATCH_REQUESTOR_TYPE | Batch requestor type |
| ZCQ_ENTITY | Data quality entity |
| ZCQ_IIR_SEARCH_WIDTH | IIR search width |
| ZCQ_PARAMETER_CARDINALITY | Parameter cardinality |
| ZCQ_PER_MATCH_OPTION_CODE | Person match option |
| ZCQ_IIR_ASM_PREF_LANG_TYPE | IIR preferred language type |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| DQL.LOOKUP | resolve_data_quality_lookup_type | Read or mutation names a type/code, or setup-data routing needs membership validation | LookupType and optional LookupCode | `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}` with child lookupCodes or exact returned item URI | LookupType, Meaning, Description, CustomizationLevel, LookupCode, EnabledFlag, dates, DisplaySequence, Tag, ModuleId, CreatedBy, LastUpdatedBy, links | Exact task member and exact type/code only; `CreatedBy == SEED_DATA_FROM_APPLICATION` proves seeded origin | Standard category, current level, values, seed origin, links, and describe fields | Stop with catalog or metadata mismatch; never try another category or infer a member |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| General read | Return the closed 21-type inventory and current read results. |
| Exact unconfirmed type | Refuse; the task has no add-type operation. |
| Mutation | Return resolved evidence to the shared executor after preview and approval; no task-local HTTP write node exists. |
| Import | Preserve immutable bytes and require Core Data Loader Task Hook validation bound to the archive SHA-256. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DQL.LOOKUP | decision | 20 | reference_lookup | resolved_or_not_needed->DQL.DEFAULTS;missing_or_ambiguous->DQL.ERROR | DQL.VALIDATE | stop | Resolve exact task membership and current lookup evidence when applicable. |
