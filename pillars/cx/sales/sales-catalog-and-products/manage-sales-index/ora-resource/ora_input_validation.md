# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Index request | requested_index_name for one index, or requested_index_names containing one or both distinct values Item and Catalog | Stop before preparing delegated requests | Provide Item, Catalog, or both without duplicates. | Every request | |
| Target environment | target_fusion_environment, or the currently authenticated Fusion environment | Stop before preparing delegated requests | Use the logged-in Fusion environment when the request does not name a different target. | Every request | |
| Item profile | The exact 17 Item attribute identities supplied for this task | Stop before preparing a delegated Item request | Supply every Item identity in the profile table | requested_index_name is Item | |
| Catalog profile | The exact 21 Catalog attribute identities supplied for this task | Stop before preparing a delegated Catalog request | Supply every Catalog identity in the profile table | requested_index_name is Catalog | |

## Required Attribute Profiles

| Index | Required Attribute Identities |
|---|---|
| Item | ITEM_NUMBER#Main#ITEM; DESCRIPTION#Main#ITEM; ORGANIZATION_CODE#Main#ITEM; PRIMARY_UOM_CODE#Main#ITEM; CUSTOMER_ORDER_ENABLED_FLAG#OrderManagement#ITEM; CATEGORY_NAME#ES_ITEM_CATEGORIES#ES_ITEM_CATEGORIES; CATALOG_NAME#ES_ITEM_CATEGORIES#ES_ITEM_CATEGORIES; START_DATE#ES_ITEM_CATEGORIES#ES_ITEM_CATEGORIES; END_DATE#ES_ITEM_CATEGORIES#ES_ITEM_CATEGORIES; SALES_PRODUCT_TYPE#OrderManagement#ITEM; SERV_REQ_ENABLED_CODE#Service#ITEM; CSS_ENABLED_FLAG#Service#ITEM; INVENTORY_ITEM_STATUS_CODE#Main#ITEM; BOM_ITEM_TYPE#BillofMaterials#ITEM; LONG_DESCRIPTION#Main#ITEM; CATEGORY_CODE#ES_ITEM_CATEGORIES#ES_ITEM_CATEGORIES; CATALOG_CODE#ES_ITEM_CATEGORIES#ES_ITEM_CATEGORIES |
| Catalog | FUNCTIONAL_AREA_ID#CATALOG_SEEDED#ES_CATALOG_CATEGORY; CATEGORY_NAME#CATEGORY_SEEDED#ES_CATALOG_CATEGORY; CATALOG_NAME#CATALOG_SEEDED#ES_CATALOG_CATEGORY; TERRITORY#CATEGORY_SEEDED#ES_CATALOG_CATEGORY; CATALOG_CODE#CATALOG_SEEDED#ES_CATALOG_CATEGORY; START_DATE#CATALOG_SEEDED#ES_CATALOG_CATEGORY; END_DATE#CATALOG_SEEDED#ES_CATALOG_CATEGORY; CONTROL_LEVEL#CATALOG_SEEDED#ES_CATALOG_CATEGORY; DEFAULT_CATEGORY_ID#CATALOG_SEEDED#ES_CATALOG_CATEGORY; DESCRIPTION#CATALOG_SEEDED#ES_CATALOG_CATEGORY; MULT_ITEM_CAT_ASSIGN_FLAG#CATALOG_SEEDED#ES_CATALOG_CATEGORY; CATALOG_CONTENT_CODE#CATALOG_SEEDED#ES_CATALOG_CATEGORY; CATEGORY_CODE#CATEGORY_SEEDED#ES_CATALOG_CATEGORY; START_DATE_ACTIVE#CATEGORY_SEEDED#ES_CATALOG_CATEGORY; END_DATE_ACTIVE#CATEGORY_SEEDED#ES_CATALOG_CATEGORY; DESCRIPTION#CATEGORY_SEEDED#ES_CATALOG_CATEGORY; CATEGORY_CONTENT_CODE#CATEGORY_SEEDED#ES_CATALOG_CATEGORY; CATEGORY_SHARED_FLAG#CATEGORY_SEEDED#ES_CATALOG_CATEGORY; PARENT_HIERARCHY_LEVEL#CATEGORY_SEEDED#ES_CATALOG_CATEGORY; PARENT_HIERARCHY_CATEGORY_CODE#CATEGORY_SEEDED#ES_CATALOG_CATEGORY; PARENT_HIERARCHY_CATEGORY_ID#CATEGORY_SEEDED#ES_CATALOG_CATEGORY |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A selected profile omits, alters, or adds an identity | BLOCKED | Restore the exact profile for the selected index before delegation. | |
| target_fusion_environment is absent and no Fusion environment is authenticated | BLOCKED | Log in to Fusion or provide the exact target environment before delegation. | |
| One or both selected indexes have complete profiles | READY | Check the delegated Product Management Indexes contract for each selected index. | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Index selector | Accept Item, Catalog, or both. Each Product Management invocation receives exactly one index. | Every request | |
| Target environment | Use the explicit target when provided; otherwise use the currently authenticated Fusion environment. | Every request | |
| Attribute identity format | Require FIELD#ATTRIBUTE_GROUP#OBJECT for every identity. | Every selected profile | |
| Profile completeness | Require the complete exact profile listed above for the selected index. | Every selected profile | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_INDEX.VALIDATE-REQUEST | decision | 10 | validate_input | valid->SALES_INDEX.CHECK-DELEGATION-CONTRACT;invalid->RETURN_ISSUES | none | stop | Every Manage Sales Index request |
