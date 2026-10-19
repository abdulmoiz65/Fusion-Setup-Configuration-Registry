# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_product_management_index_delegation | A validated Item or Catalog request is ready for delegated handling | Active Run Book dashboard; `CUSTOM_EGP_MANAGE_PM_INDEXES`; `Manage Product Management Indexes`; target Fusion environment; one selected index; its complete requested profile; requested removals; rebuild preference | Require exactly one task in the active Run Book matching both the child task code and task name, then require one scalar selected index per child invocation. Require the selected profile identities to retain FIELD#ATTRIBUTE_GROUP#OBJECT form. | resolved_product_management_index_task; canonical_index_name request; single_index_request; attributes_to_add; attributes_to_remove; index_rebuild_requested; target environment | Stop when the active Run Book has zero or multiple exact child-task matches, the child task contract or any required single-index handoff value is absent, or two index profiles are combined in one child invocation. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_sales_index_attribute_names | After canonical-index and current-profile lookup, before preparing either child handoff | Verified canonical IndexName; complete selected AttributeCode#GroupCode#ObjectCode profile in input order; same target environment | Read-only POST /fscmRestApi/scm/redwood/11.13.18.05/indexAvailableAttributes with JSON body {"indexName":"<canonical IndexName>"}; use the Product Management workflow's declared Fusion REST client after its business-object, identity and privilege gates | REST-Framework-Version: 9; top-level items; IndexName; AttributeCode; AttributeName; GroupCode; GroupName; ObjectCode; ObjectName | Require a complete items response. For every requested triplet require exactly one item matching canonical IndexName and all three codes exactly, including attributes missing from the current index. Require nonblank returned names; never derive display names from codes or use current indexed rows as a fallback for missing attributes. | Ordered attributes_to_add rows with AttributeCode, AttributeName, GroupCode, GroupName, ObjectCode, ObjectName copied from each unique match; retain the full profile, not only missing identities | Zero or multiple matches, missing names, incomplete response or unavailable endpoint blocks both handoff paths; preserve evidence and request correction without mutation |
| verify_index_attribute_profile | A validated Item or Catalog request needs a current-profile comparison | Currently authenticated Fusion environment; selected Item or Catalog index; requested AttributeCode#GroupCode#ObjectCode identities | First GET /fscmRestApi/resources/11.13.18.05/standardLookups/ORA_EGP_PM_ES_INDEXES/child/lookupCodes with limit=500, offset=0, and totalResults=true; then GET /fscmRestApi/resources/11.13.18.05/productManagementESIndexedAttributes with q=IndexName='<canonical IndexName>'; fields=AttributeId,IndexName,AttributeCode,AttributeName,GroupCode,GroupName,ObjectCode,ObjectName; onlyData=true; limit=19999 | LookupCode; Meaning; IndexName; AttributeCode; GroupCode; ObjectCode | Resolve the selected index by exact case-insensitive equality against LookupCode or Meaning and require one returned LookupCode. Require every returned attribute row to match that canonical IndexName. Compare requested and current AttributeCode#GroupCode#ObjectCode identities exactly. | Canonical IndexName; current identities; comparison result: matches or delta | Stop when the canonical index is absent or ambiguous, a current attribute row has a different index or malformed identity, or the metadata response is unavailable or incomplete. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Current index metadata is required | Use the Product Management canonical-index and existing-index read-only metadata flow. Do not infer whether attributes already exist. |
| The authoritative comparison reports a complete match | Resolve the full named profile before preparing a rebuild-only delegated request; explicit removals route to delegated delta handling instead. |
| The authoritative comparison reports a delta | Prepare the selected profile for delegated Product Management index handling. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_INDEX.VERIFY-INDEX-PROFILE | decision | 30 | reference_lookup | matches->SALES_INDEX.APPLY-REBUILD-DEFAULT;delta->SALES_INDEX.ENFORCE-DELEGATED-INDEXING;not_found->RETURN_ISSUES;ambiguous->RETURN_ISSUES;failure->RETURN_ISSUES | SALES_INDEX.CHECK-DELEGATION-CONTRACT | stop | Every dependency-ready selected index request; first verify_index_attribute_profile then resolve_sales_index_attribute_names; matches requires a complete named profile and no removals; delta includes explicit removals; any lookup failure blocks |
