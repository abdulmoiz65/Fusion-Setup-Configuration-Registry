# Reference Lookups

## Task Lookup Inventory

| Lookup Type | Meaning | Configuration Level | Validated Scope |
|---|---|---|---|
| ZCH_DEDUP_REQUEST_TYPE | Resolution Request Type | System | Duplicate resolution request types such as generic, link, and merge |
| ZCH_IDEN_TARGET | Duplicate Identification Target Object | System | Duplicate-identification target objects |
| ZCH_LINK_MASTER_PARTY_TYPE | Link Master Party Type | System | Master-party types used by link requests |
| ZCH_MERGE_REASON_CODE | Merge Reason | System | Reasons for duplicate merge requests |
| ZCH_MERGE_STATUS_CODE | Merge Status | System | Duplicate-resolution request statuses |
| ZCH_DEDUP_REQUEST_TYPE_OPTION | Resolution Request Type Option | System | Resolution-request processing choices |
| ZCH_MATCH_DATE_OPERATION | Date Operation Objects | System | Date comparison operators used by matching rules |
| ZCH_MATCH_OBJECT_TYPE | Match Object Type | System | Duplicate-identification match object types |
| ZCH_MATCH_OBJ_ACCOUNT | Account Attributes | System | Account attributes available to batch-rule criteria |
| ZCH_MATCH_OBJ_LOCATION | Location Attributes | System | Location attributes available to batch-rule criteria |
| ZCH_MATCH_OBJ_ORGANIZATION | Organization Attributes | Extensible | Organization attributes available to batch-rule criteria |
| ZCH_MATCH_OBJ_PARTYUSG_FR | Party Usage Filter Rule Attributes | System | Party-usage filter attributes available to batch rules |
| ZCH_MATCH_OBJ_PARTY_USG | Party Usage Attributes | System | Party-usage attributes available to batch-rule criteria |
| ZCH_MATCH_OBJ_PERSON | Person Attributes | Extensible | Person attributes available to batch-rule criteria |
| ZCH_MATCH_STRING_OPERATION | String Operation Objects | System | String comparison operators used by matching rules |
| ZCH_MERGE_OVERRIDE_ENTITY | Merge Override Entity Objects | System | Objects supported by merge override processing |
| ZCH_PROCESS_OPTION_CODE | Process Option | System | Duplicate-identification batch processing options |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| DML.LOOKUP | resolve_duplicate_management_lookup | Read or mutation names a type/code | LookupType and optional LookupCode | /fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}?expand=lookupCodes or exact returned item URI | LookupType, Meaning, Description, CustomizationLevel, code values, ModuleId, RestAccessSecured, CreatedBy, LastUpdatedBy, links, and code describe | Exact inventory member and exact code only | Category, level, current values, seed evidence, links, and writable fields | Stop with catalog_or_metadata_mismatch; never try another category or infer membership |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Read | Return current exact type or code values through Apps Common Standard Lookups. |
| System update | Return exact evidence for an approval-bound, current-describe-supported `Meaning` PATCH; no task-local HTTP node exists. |
| Extensible wording/display update | Permit current-describe-supported `Meaning`, `Description`, or `DisplaySequence`; protect seeded identity. |
| Extensible custom-code lifecycle | Permit create, `EnabledFlag`, active dates, or safe delete only for a proven custom code after exact preflight and approval. |
| Unsupported mutation | Refuse type/code rename, parent/module/security/level/`Tag` change, System structural or state mutation, and destructive change to seeded or unknown-origin codes. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DML.LOOKUP | decision | 20 | reference_lookup | resolved_or_not_needed->DML.DEFAULTS;missing_or_ambiguous->DML.ERROR | DML.VALIDATE | stop | Resolve exact task membership and current evidence. |
