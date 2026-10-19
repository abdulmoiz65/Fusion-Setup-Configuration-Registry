# Reference Lookups

## Official Oracle Documentation

| Source | Oracle URL | What It Confirms | Evidence Boundary |
|---|---|---|---|
| Overview of Lookup Types | https://docs.oracle.com/en/cloud/saas/sales/oasal/overview-of-lookup-types.html | Lookup configuration levels, allowed operations, and the Sales lookup-task family containing Manage Source System Lookups where listed | Does not provide a complete task-to-lookup-type inventory; effective FSCR catalog placement remains authoritative |
| Copy setup data reference | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26a/faiom/reference-for-copying-setup-data-between-instances-of-order.html | Describes Manage Source System Lookups as choices for the source-system model, including original system type | Does not enumerate every lookup type or establish current configuration levels |
| Work With Lookups | https://docs.oracle.com/en/cloud/saas/applications-common/26a/farca/Work_with_Lookups.html | Standard, Common, Generic, and Set-Enabled views and the need to know the correct lookup view | Does not attribute an arbitrary type to this task |
| Standard Lookups REST | https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html | Standard lookup GET and documented CRUD families | Does not override task membership, configuration, seed, describe, or approval gates |
| Common Lookups REST | https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-common-lookups.html | Common lookup GET and documented CRUD families | Same restriction; other categories must use their own documented resource |
| Setup Task CSV Exports | https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-exports.html | Task-level CSV export root, ProcessId, FileContent, and ProcessLog family | Exact catalog CSV flag and shared exporter remain binding |
| Setup Task CSV Imports | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html | Task-level CSV import root, ProcessId, and ProcessLog family | Does not authorize task-local dispatch or bypass validation and approval |
| Create setup task CSV import | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-fscmrestapi-resources-11.13.18.05-setuptaskcsvimports-post.html | Outer TaskCode, SetupTaskCSVImportProcess, inner TaskCode, FileContent, SourceTargetDiffOkFlag, and ProcessId | Background REST evidence only; metadata must match HZ_MANAGE_SOURCE_SYSTEM_LOOKUPS and Core Data Loader owns execution routing. |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| SSL.LOOKUP_TARGET | resolve_task_lookup_target | Read or mutation names an exact type/code with task-membership evidence | LookupType, optional LookupCode, authoritative task attribution | Resolve category read-only through Apps Common; use /fscmRestApi/resources/11.13.18.05/{resolvedLookupResource}/{LookupType}?expand=lookupCodes or exact returned item URI | LookupType, Meaning, Description, CustomizationLevel, LookupCode, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag, Module, CreatedBy, LastUpdatedBy, links | Exact type and code only; LastUpdatedBy equal to SEED_DATA_FROM_APPLICATION is seeded evidence | Category, exact type/code, level, current values, seed evidence, supported links, and describe fields | Stop on miss or ambiguity; 401 or 403 is auth/authz, not absence; never broaden with prefix or module inference |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| General task read | Return only confirmed task members and disclose incomplete inventory. |
| Exact unconfirmed type | Require authoritative task attribution before claiming membership or manual support. |
| Category unknown | Perform read-only Apps Common category discovery; stop on 401/403. |
| Mutation requested | Return evidence to the shared executor; this resource defines no task-local HTTP write node. |
| FSM ZIP import | Preserve immutable bytes, validate exact metadata task identity, and require core.data-loader to run its Task Hook against the exact final archive and issue a current validation envelope bound to the archive SHA-256 before approval and upload; Core Data Loader alone owns route selection and execution. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SSL.LOOKUP_TARGET | decision | 3 | reference_lookup | create->SSL.DEPENDENCY_READINESS;read_or_update->SSL.DESIGN_GATE;not_found->SSL.RETURN_ISSUES;failure->SSL.RETURN_ISSUES | SSL.DEFAULT_SCOPE | stop | Resolve exact task membership, category, type, code, level, seed evidence, and current fields. |
