# Reference Lookups

## Official Oracle Documentation

| Source | Oracle URL | What It Confirms | Evidence Boundary |
|---|---|---|---|
| Overview of Lookup Types | https://docs.oracle.com/en/cloud/saas/sales/oasal/overview-of-lookup-types.html | Lookup configuration levels, allowed operations, and the Sales lookup-task family containing Manage Party Usage Lookups where listed | Does not provide a complete task-to-lookup-type inventory; effective FSCR catalog placement remains authoritative |
| How You Define Party Usage | https://docs.oracle.com/en/cloud/saas/customer-data-management/faicd/how-you-define-party-usage.html | Assignment, exclusivity, incompatibility, and transition rule semantics | Does not enumerate this setup task's lookup inventory or authorize lookup writes |
| HZ_PARTY_USAGE_RULES | https://docs.oracle.com/en/cloud/saas/sales/oedms/hzpartyusagerules-20355.html | PARTY_USAGE_RULE_TYPE is validated by HZ_PARTY_USAGE_RULE_TYPE | Confirms one lookup consumer, not the complete task inventory or writable fields |
| Exact-task Fusion UI evidence | Configured environment, Manage Party Usage Lookups | Establishes the closed four-type OOTB task inventory | Environment-specific membership evidence; REST describe and System rules govern manual fields |
| Work With Lookups | https://docs.oracle.com/en/cloud/saas/applications-common/26a/farca/Work_with_Lookups.html | Standard, Common, Generic, and Set-Enabled views and the need to know the correct lookup view | Does not attribute an arbitrary type to this task |
| Standard Lookups REST | https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html | Standard lookup GET and documented CRUD families used by all four members | Current describe must be intersected with System configuration, identity, preview, and approval gates |
| Setup Task CSV Exports | https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-exports.html | Task-level CSV export root, ProcessId, FileContent, and ProcessLog family | Exact catalog CSV flag and shared exporter remain binding |
| Setup Task CSV Imports | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html | Task-level CSV import root, ProcessId, and ProcessLog family | Does not authorize task-local dispatch or bypass validation and approval |
| Create setup task CSV import | https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-fscmrestapi-resources-11.13.18.05-setuptaskcsvimports-post.html | Outer TaskCode, SetupTaskCSVImportProcess, inner TaskCode, FileContent, SourceTargetDiffOkFlag, and ProcessId | Background REST evidence only; metadata must match HZ_MANAGE_PARTY_USAGE_LOOKUPS and Core Data Loader owns execution routing. |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| PU.LOOKUP_TARGET | resolve_task_lookup_target | Read or mutation names an exact type/code in the closed baseline | LookupType and optional LookupCode | `/fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}` with child lookupCodes or exact returned item URI | LookupType, Meaning, Description, CustomizationLevel, LookupCode, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag, ModuleId, CreatedBy, LastUpdatedBy, links | Exact type/code only; CreatedBy equal to SEED_DATA_FROM_APPLICATION proves seeded origin; LastUpdatedBy is audit only | Exact type/code, Standard category, System level, current values, seed origin, links, and current describe fields | Stop on miss or ambiguity; 401/403 is auth/authz; never try another category or infer a new member |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| General task read | Return the closed four-type OOTB inventory and current read results. |
| Exact unconfirmed type | Refuse because this task has no add-type operation. |
| Standard GET miss | Stop with catalog_or_metadata_mismatch; do not try another lookup category. |
| Manual PATCH | Permit only Meaning after current REST describe and System-level checks. |
| Mutation requested | Return evidence to the shared executor; this resource defines no task-local HTTP write node. |
| FSM ZIP import | Preserve immutable bytes, validate exact metadata task identity, and require core.data-loader to run its Task Hook against the exact final archive and issue a current validation envelope bound to the archive SHA-256 before approval and upload; Core Data Loader alone owns route selection and execution. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PU.LOOKUP_TARGET | decision | 3 | reference_lookup | create->PU.DEPENDENCY_READINESS;read_or_update->PU.DESIGN_GATE;not_found->PU.RETURN_ISSUES;failure->PU.RETURN_ISSUES | PU.DEFAULT_SCOPE | stop | Resolve exact task membership, category, type, code, level, seed evidence, and current fields. |
