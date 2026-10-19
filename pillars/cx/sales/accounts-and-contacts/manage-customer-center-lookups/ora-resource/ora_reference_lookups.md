# Reference Lookups

## Official Oracle Documentation

| Source | Oracle URL | What It Confirms | Evidence Boundary |
|---|---|---|---|
| Overview of Lookup Types | https://docs.oracle.com/en/cloud/saas/sales/oasal/overview-of-lookup-types.html | Sales placement under Accounts and Contacts and configuration-level operations | Does not enumerate the exact eight task members; this target does not duplicate other catalog occurrences |
| Standard Lookups REST | https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html | Standard lookup GET and documented CRUD family | Does not override task membership, level, seed, describe, or approval gates |
| Standard Lookup Codes REST | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/25c/fasrp/api-standard-lookup-types-standard-lookup-codes.html | Lookup-code GET, POST, PATCH, and DELETE paths | Current describe and configuration policy remain binding |
| Setup Task CSV Exports | https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-exports.html | Task-level export ProcessId, FileContent, and ProcessLog family | Exact catalog CSV flag and shared exporter remain binding |
| Setup Task CSV Imports | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html | Task-level import ProcessId and ProcessLog family | Does not authorize task-local dispatch or bypass approval |
| Create setup task CSV import | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-fscmrestapi-resources-11.13.18.05-setuptaskcsvimports-post.html | Outer and inner TaskCode, FileContent, SourceTargetDiffOkFlag, and ProcessId | Background REST evidence only; metadata must match ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS and Core Data Loader owns execution routing. |

## Confirmed Task Inventory

Configured task-page membership supplied by the user plus exact Standard REST GET evidence captured on 2026-08-07:

| Configuration level | Exact lookup types |
|---|---|
| User | ZCA_ACCOUNT_TYPE, ZCA_ACCT_SRCH_RECORD_SET, ZCA_CONTACT_TYPE, ZCA_HOUSEHOLD_TYPE, ZCA_RECORD_TYPE, ZCA_RESOURCE_FUNCTION, ZCA_SALES_ACCOUNT_STATUS |
| Extensible | ZMM_NOTE_TYPE |

Do not add members by prefix, meaning, module, or neighboring task inference. Reconfirm the Standard category and current level before execution.

The effective catalog also lists the same task code under Customer Loyalty / Accounts and Contacts and Sales Marketing / Customer Center. This resource set is scoped only to the generated Sales / Accounts and Contacts parent and must not be copied into CDM or another occurrence without an explicit catalog-backed routing decision.

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| CC.LOOKUP_TARGET | resolve_customer_center_lookup | Read or mutation names an exact confirmed type/code | LookupType and optional LookupCode | /fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}?expand=lookupCodes or exact returned item URI | LookupType, Meaning, Description, CustomizationLevel, LookupCode, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag, ModuleId, CreatedBy, LastUpdatedBy, links | Exact baseline member and code only; CreatedBy equal to SEED_DATA_FROM_APPLICATION proves seeded origin; LastUpdatedBy is audit only | Standard category, exact type/code, level, current values, seed evidence, links, and describe fields | Stop on miss, drift, or ambiguity; 401 or 403 is auth or authz, not absence |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| General task read | Return the eight exact confirmed members and their current GET-confirmed levels. |
| Exact unconfirmed type | Refuse task attribution and manual support. |
| Baseline drift | Stop when current REST category or level differs; reconcile before execution. |
| Mutation requested | GET /standardLookups/{LookupType}/child/lookupCodes/describe, intersect writable fields with configuration rules, and return evidence to the shared executor. |
| FSM ZIP import | Preserve immutable bytes, validate exact metadata task identity, and require core.data-loader to run its Task Hook against the exact final archive and issue a current validation envelope bound to the archive SHA-256 before approval and upload; Core Data Loader alone owns route selection and execution. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CC.LOOKUP_TARGET | decision | 3 | reference_lookup | create->CC.DEPENDENCY_READINESS;read_or_update->CC.DESIGN_GATE;not_found->CC.RETURN_ISSUES;failure->CC.RETURN_ISSUES | CC.DEFAULT_SCOPE | stop | Resolve exact membership, Standard category, type/code, level, seed evidence, and current fields. |
