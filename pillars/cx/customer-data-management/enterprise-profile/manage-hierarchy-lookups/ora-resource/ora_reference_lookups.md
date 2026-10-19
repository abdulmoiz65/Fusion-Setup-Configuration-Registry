# Reference Lookups

## Official Oracle Documentation

| Source | Oracle URL | What It Confirms | Evidence Boundary |
|---|---|---|---|
| How can I create a new hierarchy type? | https://docs.oracle.com/en/cloud/saas/customer-data-management/faudm/how-can-i-create-a-new-hierarchy-type.html | Create the hierarchy type with Manage Tree Structures, then add it under Party Hierarchy Type | Does not publish a REST endpoint for verifying Manage Tree Structures completion |
| Overview of Lookup Types | https://docs.oracle.com/en/cloud/saas/sales/oasal/overview-of-lookup-types.html | Manage Hierarchy Lookups is a lookup task; User, Extensible, and System mutation rules | Sales documentation groups the task under Accounts and Contracts; FSCR catalog placement remains authoritative for this skill |
| Audit Party Hierarchy | https://docs.oracle.com/en/cloud/saas/sales/fauss/audit-party-hierarchy.html | PARTY_HIERARCHY_TYPE supplies hierarchy type and HZ_TREE_STATUS supplies Active or Inactive status | Confirms hierarchy usage, but not by itself exact membership of HZ_TREE_STATUS in this setup task |
| Import hierarchy data | https://docs.oracle.com/en/cloud/saas/customer-data-management/faudm/import-your-hierarchy-data.html | TreeStructureCode values come from PARTY_HIERARCHY_TYPE and the lookup is available through Manage Standard Lookups | Covers hierarchy-data import, not task CSV setup-data import |
| Standard Lookups REST endpoints | https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html | Standard lookup parent GET and resource category | Product-specific task filtering and authorization still require live evidence |
| Standard Lookup Codes REST endpoints | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-standard-lookups-lookup-codes.html | Code-level GET, POST, PATCH, and DELETE paths | Paths don't override configuration-level, seeded-data, approval, or describe gates |
| Create a Standard Lookup code | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-http-servername-fscmrestapi-resources-11.13.18.05-standardlookups-lookuptype-child-lookupcodes-post.html | Code child POST path, field schema, length limits, and Upsert-Mode behavior | Current describe metadata remains binding for the target environment |
| Get a Standard Lookup code | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-http-servername-fscmrestapi-resources-11.13.18.05-standardlookups-lookuptype-child-lookupcodes-lookupcode-get.html | Exact code GET path | A 401 or 403 is not lookup absence |
| Update a Standard Lookup code | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-http-servername-fscmrestapi-resources-11.13.18.05-standardlookups-lookuptype-child-lookupcodes-lookupcode-patch.html | Exact code PATCH path and writable-looking REST fields | Configuration-level and seeded-data rules can be stricter than REST schema hints |
| Task CSV export and import tutorial | https://docs.oracle.com/en/cloud/saas/applications-common/faqac/export-and-import-task-setup-data-using-csv-files.html | Task actions expose CSV export and import only when supported and require result verification | FSCR catalog flag and shared executors remain the runtime routing authority |
| Create a setup task CSV import | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-fscmrestapi-resources-11.13.18.05-setuptaskcsvimports-post.html | Root POST path, outer TaskCode, SetupTaskCSVImportProcess array, inner TaskCode, FileContent, SourceTargetDiffOkFlag, and returned ProcessId | Background REST evidence only; Core Data Loader remains authoritative for execution routing and this task skill must not select this endpoint or payload. |
| Setup Task CSV Imports endpoints | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html | Documents the setup-task CSV import REST family | Background evidence only; Core Data Loader owns execution routing and the catalog flag remains required. |
| Security Requirements | https://docs.oracle.com/en/cloud/saas/applications-common/26b/oafsm/security-requirements.html | Functional Setups User, task-specific privilege, and Export Import Functional Setups User requirements | The exact Manage Hierarchy Lookups task privilege code isn't published on this page |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| HL.LOOKUP_TARGET | resolve_hierarchy_lookup_target | A read or mutation names a lookup type or code, or a general hierarchy-lookups read uses the developer-provided tested baseline scope | LookupType, LookupCode, PARTY_HIERARCHY_TYPE, HZ_TREE_STATUS | /fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}?expand=lookupCodes; for an exact code use /fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes/{LookupCode} | LookupType, Meaning, Description, CustomizationLevel, LookupCode, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag, CreatedBy, LastUpdatedBy, links | Match each requested type and code exactly; a general read resolves both tested baseline types independently and treats LastUpdatedBy equal to SEED_DATA_FROM_APPLICATION as predefined-data evidence | Exact type, configuration level, code state, seeded evidence, supported links, and current fields | Stop on an exact-target miss or ambiguity; classify 401 or 403 separately; for a general read report either baseline failure explicitly rather than hiding a partial result |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| User supplies another exact lookup type | Retrieve it and classify its resource category and configuration level before claiming support. |
| User requests all hierarchy lookups | Retrieve PARTY_HIERARCHY_TYPE and HZ_TREE_STATUS; report partial failures explicitly. |
| Authentication or authorization fails | Classify the failure; never report it as lookup absence. |
| Lookup type or code is ambiguous | Stop; do not infer from prefix, module, or meaning. |
| REST schema and configuration rules differ | Apply the stricter configuration-level, seeded-data, current describe, and task-scope restriction. |
| A mutation is requested | Return lookup evidence to the owning shared executor; this v3 resource defines no REST write node or payload. |
| An FSM task ZIP import is requested | Preserve the archive, validate the exact metadata task identity, and route it only through Core Data Loader. Require its current Task Hook validation envelope bound to the exact archive SHA-256; this resource never selects an endpoint or payload. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HL.LOOKUP_TARGET | decision | 3 | reference_lookup | create->HL.DEPENDENCY_READINESS;read_or_update->HL.DESIGN_GATE;not_found->HL.RETURN_ISSUES;failure->HL.RETURN_ISSUES | HL.DEFAULT_SCOPE | stop | Resolve the exact current lookup state before a read or supported named mutation. |
