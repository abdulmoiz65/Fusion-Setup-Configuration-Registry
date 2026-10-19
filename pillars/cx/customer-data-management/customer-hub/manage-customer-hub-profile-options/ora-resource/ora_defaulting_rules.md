# Defaulting Rules

Documented defaults are reference values. Apply one only when the user explicitly requests the documented default, the current profile definition agrees, and the exact value is included in the approval preview.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ZCH_CLNS_PROC_BT_SIZE | 10000 | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |
| ZCH_DEDUP_REQUEST_TYPE_OPTION | Merge | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |
| ZCH_DI_PROC_BT_SIZE | 100 | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |
| ZCH_USER_MERGE_REQUESTS | Unspecified / null | User explicitly requests the documented default and acknowledges its processing effect | No | read_customer_hub_profile_definition |
| ZCH_ENABLE_SURVIVORSHIP | Yes | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |
| ZCH_AUTO_LINK_THRESHOLD | 0 | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |
| ZCH_AUTO_MERGE_THRESHOLD | 100 | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |
| ZCH_DI_MERGEREQ_REC_SIZE | 10 | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |
| ORA_ZCH_SETATTRIBUTE_OPTIONS | IGNORE_NULL_VALUE | User explicitly requests the documented default and confirms null-survivorship behavior | No | read_customer_hub_profile_definition |
| ORA_ZCH_ALLOW_REMOVE_FEATURE | N | User explicitly requests restoration of the documented safe default | No | read_customer_hub_profile_definition |
| ORA_ZCH_ACCOUNT_BATCH_ENRICHMENT_IMPORT_MAP | Automatic Mapping | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |
| ORA_ZCH_ADDITIONAL_NAME_BATCH_ENRICHMENT_IMPORT_MAP | Automatic Mapping | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |
| ORA_ZCH_ADDITIONAL_IDENTIFIER_BATCH_ENRICHMENT_IMPORT_MAP | Automatic Mapping | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |
| ORA_ZCH_CLASSIFICATION_BATCH_ENRICHMENT_IMPORT_MAP | Automatic Mapping | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |
| ORA_ZCH_ADDRESS_BATCH_ENRICHMENT_IMPORT_MAP | Automatic Mapping | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |
| ORA_ZCH_CONTACT_BATCH_ENRICHMENT_IMPORT_MAP | Automatic Mapping | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |
| ORA_ZCH_CONTACT_POINT_BATCH_ENRICHMENT_IMPORT_MAP | Automatic Mapping | User explicitly requests the documented default and the live definition confirms it | No | read_customer_hub_profile_definition |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHP.APPLY_DEFAULT | decision | 4 | apply_default | applied->CHP.DESIGN_GATE;not_applicable->CHP.DESIGN_GATE;blocked->CHP.ERROR | CHP.DEPENDENCY_READINESS | stop | When a user asks to use or restore a documented default; otherwise take the not_applicable branch |
