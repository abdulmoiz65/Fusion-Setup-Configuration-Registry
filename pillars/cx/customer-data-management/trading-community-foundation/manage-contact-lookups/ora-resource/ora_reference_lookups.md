# Reference Lookups

## Official Oracle Documentation

| Source | Oracle URL | What It Confirms | Evidence Boundary |
|---|---|---|---|
| Overview of Lookup Types | https://docs.oracle.com/en/cloud/saas/sales/oacdm/overview-of-lookup-types.html | Lookup configuration levels, allowed operations, and the Sales lookup-task family containing Manage Contact Lookups where listed | Does not provide a complete task-to-lookup-type inventory; effective FSCR catalog placement remains authoritative |
| Work With Lookups | https://docs.oracle.com/en/cloud/saas/applications-common/26a/farca/Work_with_Lookups.html | Standard, Common, Generic, and Set-Enabled views and the need to know the correct lookup view | Does not attribute an arbitrary type to this task |
| Standard Lookups REST | https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html | Standard lookup GET and documented CRUD families | Does not override task membership, configuration, seed, describe, or approval gates |
| Common Lookups REST | https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-common-lookups.html | Common lookup GET and documented CRUD families | Same restriction; other categories must use their own documented resource |
| Setup Task CSV Exports | https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-exports.html | Task-level CSV export root, ProcessId, FileContent, and ProcessLog family | Exact catalog CSV flag and shared exporter remain binding |
| Setup Task CSV Imports | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html | Task-level CSV import root, ProcessId, and ProcessLog family | Does not authorize task-local dispatch or bypass validation and approval |
| Create setup task CSV import | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-fscmrestapi-resources-11.13.18.05-setuptaskcsvimports-post.html | Outer TaskCode, SetupTaskCSVImportProcess, inner TaskCode, FileContent, SourceTargetDiffOkFlag, and ProcessId | Background REST evidence only; metadata must match HZ_MANAGE_CONTACT_LOOKUPS and Core Data Loader owns execution routing. |

## Confirmed Task Inventory

Configured Fusion task-page membership plus exact Standard REST GET evidence captured on 2026-08-07:

| Configuration level | Exact lookup types |
|---|---|
| User | RESPONSIBILITY, HZ_SLS_CNTCT_AFFINITY_CODE, HZ_SLS_CNTCT_BUY_ROLE_CODE, HZ_SLS_CNTCT_INFLUENCE_LVL_CD, CONTACT_ROLE_TYPE, DEPARTMENT_TYPE |

Do not add members by inference. Reconfirm the exact type and configuration level before execution.

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| CL.LOOKUP_TARGET | resolve_task_lookup_target | Read or mutation names an exact confirmed type/code | LookupType and optional LookupCode | /fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}?expand=lookupCodes or exact returned item URI | LookupType, Meaning, Description, CustomizationLevel, LookupCode, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag, ModuleId, CreatedBy, LastUpdatedBy, links | Exact baseline member and code only; CreatedBy == SEED_DATA_FROM_APPLICATION proves seeded origin; LastUpdatedBy is audit only | Standard category, exact type/code, level, current values, seed evidence, links, and describe fields | Stop on miss, drift, or ambiguity; 401/403 is auth/authz, not absence |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| General task read | Return the six exact confirmed members and their current GET-confirmed levels. |
| Exact unconfirmed type | Refuse task attribution and manual support. |
| Baseline drift | Stop when current REST category or level differs; reconcile before execution. |
| Mutation requested | GET /standardLookups/{LookupType}/child/lookupCodes/describe, intersect its writable fields with configuration-level rules, and return evidence to the shared executor; this resource defines no task-local HTTP write node. |
| FSM ZIP import | Preserve immutable bytes, validate exact metadata task identity, and require core.data-loader to run its Task Hook against the exact final archive and issue a current validation envelope bound to the archive SHA-256 before approval and upload; Core Data Loader alone owns route selection and execution. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CL.LOOKUP_TARGET | decision | 3 | reference_lookup | create->CL.DEPENDENCY_READINESS;read_or_update->CL.DESIGN_GATE;not_found->CL.RETURN_ISSUES;failure->CL.RETURN_ISSUES | CL.DEFAULT_SCOPE | stop | Resolve exact task membership, category, type, code, level, seed evidence, and current fields. |
