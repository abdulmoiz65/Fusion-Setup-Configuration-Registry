# Manage Opportunity Profile Options Design Enforcement

Read-only and FSM requests use DESIGN. Confirmed omission and failed-export
requests use APPS_COMMON_DESIGN after exact live resolution. Failed-export
requests require an existing child and PATCH only. Approval follows the route.

Oracle's current Product-level restriction is documented in
[Set Profile Option Values](https://docs.oracle.com/en/cloud/saas/applications-common/26d/facia/set-profile-option-values.html).
Product reads and eligible updates of existing legacy values remain available
through the declared core contract. New Product values require separate current
Oracle support evidence; service capability flags and approval alone do not
resolve deprecation.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Exact identity and route | Require complete live evidence; Review records not_requested_for_review without export/approval; Inventory/mutation record export outcome and distinguish omission/failure/missing value rows |
| 2 | Scope and stored-value contract | Require exact scope/key, enabled/updatable flags, current state, and deterministic stored-value dependencies |
| 3 | Route-specific artifact | FSM preserves existing export rows and immutable package; REST builds a minimal deterministic request with omission or failure evidence |
| 4 | State and approval boundary | FSM locks live state/package/task context for Data Loader handoff; REST locks full preview and requires separate approval immediately before write |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Inventory discovery | Blocker | resolve_opportunity_option_candidates | A claimed complete scope has unresolved identities, unaccounted candidates, or lacks verified complete applicable ownership evidence; failed export leaves task coverage unknown | Preserve known-candidate live results and coverage gaps; return RETURN_PARTIAL_INVENTORY for unproved all-options scope. Explicit-candidate completion requires that exact user-selected scope | Yes |
| Review or mutation identity | Blocker | resolve_opportunity_option_candidates | Exact code lacks source-backed Opportunity ownership, display-only input lacks one exact code mapping, or supplied/live/source identities conflict | Resolve the missing exact identity/source evidence without prefix inference or an export requirement for exact-code Review | Yes |
| Inventory or Review | Blocker | resolve_live_profile_option | Live definition/status, live level flags, complete children/absence, or timestamps are incomplete | Complete declared live reads or report the classified failure | Yes |
| Review or mutation | Blocker | resolve_live_profile_option | Code is absent, ambiguous, wrong product area, or conflicts across supplied/live/export/package identities | Require one exact Opportunity code and scope; do not select a similar definition | Yes |
| Exact-code Review | Blocker | resolve_live_profile_option | Workflow demands export, export approval, ZIP, Data Loader context, or mutation privilege instead of direct live reads | Use declared Apps Common GET route with read privileges; export is not a prerequisite | Yes |
| Mutation route selection | Blocker | resolve_profile_option_export_baseline | Export was never attempted, a supplied successful artifact is invalid/is template-only/is filtered, or successful-export membership is ambiguous | Require exact attempted-call evidence; successful membership or classified failure may select REST readiness; failed-export unknown membership is allowed and never proves omission | Yes |
| FSM Set/BulkSet | Blocker | resolve_profile_option_export_baseline | Exact exported definition, Site/User capability row, existing value row, matching live state, or dependency closure is missing | Correct the existing exported target; do not substitute REST when the option is present | Yes |
| FSM Set/BulkSet | Blocker | resolve_profile_option_export_baseline | Selected Site/User level is not enabled/updatable in live and export evidence or proposed value fails current contract | Correct the eligible level/value without changing capability metadata | Yes |
| FSM package preparation | Blocker | resolve_profile_option_export_baseline | Delta changes definitions, level flags, keys, validation, descriptions, audit fields, metadata, members, headers, dependencies, or unrelated values | Rebuild from baseline changing only reviewed existing ProfileOptionValue rows | Yes |
| FSM handoff | Blocker | verify_profile_option_final_package | Final target/release/task/ASM/member/header/delta/state/preservation/path/hash receipt or persisted TaskContextPath/positive TaskSequence/exact context resolution is missing | Rebuild/reopen package and resolve persisted context from project task plan; never synthesize it solely for Data Loader | Yes |
| REST Set/BulkSet | Blocker | resolve_profile_option_export_baseline | Neither confirmed successful-export omission nor a classified failed exact-task export is recorded | Resolve exact export outcome; failure permits only existing-child Update, omission permits Create/Update | Yes |
| REST scope and privilege | Blocker | resolve_live_profile_option | Site/Product/User live level capability is disabled/read-only, exact key is unresolved, current rows are ambiguous, or FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV is missing | Resolve exact eligible scope, child state, and privilege before preview | Yes |
| REST Product creation | Blocker | resolve_live_profile_option | Requested Product child is absent and no verified current Oracle evidence explicitly permits new Product values for this release/resource/operation | Block new Product POST by default. An exception must identify Oracle source, applicable release, resource, creation operation, restrictions, and required privilege; bind the evidence to preview and revalidate before writing. User approval, enabled flags, generic POST support, and the Rel13 service description are insufficient | Yes |
| REST legacy Product update | Blocker | resolve_live_profile_option | Product PATCH is presented as ordinary new configuration, the exact existing legacy row is absent, or current advertised update/capability evidence is missing | Preserve existing-row PATCH under the core contract, label the scope deprecated legacy-only, and apply all existing state, dependency, privilege, approval, and verification gates. Never convert absence into POST | Yes |
| REST failed-export update | Blocker | resolve_live_profile_option | Requested exact live child is absent or the request proposes POST after export failure | Return missing value and block; this fallback updates existing values only | Yes |
| REST stored value | Blocker | resolve_live_profile_option | Proposed value is a display label instead of validated stored code/ID or required dependency evidence is absent | Resolve the exact supported current value contract; never execute SqlValidation SQL | Yes |
| REST request | Blocker | resolve_live_profile_option | POST targets an existing row, PATCH an absent row, parent definition is targeted, body has unrelated/audit fields, or Upsert-Mode hides state | Select POST/PATCH from live state; use only ProfileOptionValue plus required Create LevelValue | Yes |
| REST approval/execution | Blocker | resolve_live_profile_option | Complete preview digest or standalone approval is missing/mismatched, route/environment/request changed, or immediate live reread shows drift | Return preview before approval; refresh evidence and obtain new approval on change | Yes |
| REST verification | Blocker | resolve_live_profile_option | Fresh exact child read does not equal approved stored value | Report mismatch or uncertain result and stop without retry or compensation | Yes |
| BulkSet | Blocker | resolve_profile_option_export_baseline | Targets are duplicated or include both FSM and REST routes | Deduplicate or return route-specific batches before handoff/write; approvals remain route-specific | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_opportunity_option_candidates | Before Inventory reads or Review/mutation identity acceptance | Exact source-backed code/name/ownership mappings, candidate receipt, explicit scope, accounted live results, unresolved identities, coverage gaps, and completion status | ora_reference_lookups.md |
| resolve_live_profile_option | Every request and mutation state refresh | Exact identity/status, live level flags, complete children/absence, current-state lock, scope, supported stored-value dependencies, and conditional privilege | ora_reference_lookups.md |
| resolve_profile_option_export_baseline | After export attempt and before mutation selection | Exact export-attempt identity/outcome; complete artifact/hash/count only on success; existing closure for FSM or omission/failure receipt for REST; failed-export membership stays unknown | ora_reference_lookups.md |
| verify_profile_option_final_package | Immediately before FSM handoff only | Final task/target/context, ASM/member/header/delta/state/preservation receipt, immutable path and reopened SHA-256 | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.PROFILE_OPTIONS.DESIGN | decision | 5 | design_enforcement | pass->OPP.PROFILE_OPTIONS.GATE;blocked->OPP.PROFILE_OPTIONS.RETURN_MISSING;failed->OPP.PROFILE_OPTIONS.RETURN_FAILED | OPP.PROFILE_OPTIONS.ROUTE | stop | Require source-backed identity and complete exact-code Review without export/mutation approval; Inventory may pass known-candidate results with partial coverage solely to its partial terminal; preserve existing FSM prerequisites and separate REST branch |
| OPP.PROFILE_OPTIONS.APPS_COMMON_DESIGN | decision | 7 | design_enforcement | pass->OPP.PROFILE_OPTIONS.APPS_COMMON_GATE;blocked->OPP.PROFILE_OPTIONS.RETURN_MISSING;failed->OPP.PROFILE_OPTIONS.RETURN_FAILED | OPP.PROFILE_OPTIONS.ROUTE | stop | Preserve omission or classified-failure gates, existing-child PATCH after failure, exact live scope/state/privilege/dependencies, minimal request, immutable preview, approval and verification. Require current creation-support evidence for new Product rows; preserve eligible legacy Product PATCH |
