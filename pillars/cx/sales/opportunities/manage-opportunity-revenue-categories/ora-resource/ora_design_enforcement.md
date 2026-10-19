# Manage Opportunity Revenue Categories Design Enforcement

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

Apply these rules after read-only parent/code resolution and route-aware package
readiness. Preserve documented Sales behavior, immutable task/package identity,
and the Core Data Loader ownership boundary.

## Enforcement Order

| Sequence | Step | What Must Happen |
| --- | --- | --- |
| 1 | Confirm request scope | Keep MOO_REVN_CATEGORY and MOO_MANAGE_REVENUE_CATEGORIES fixed; use one code only for SingleLookup and no code selector for full-task Export |
| 2 | Resolve current state | Enforce Create against fresh absence and Update or Disable against one exact existing state, independently for every changed Import row |
| 3 | Enforce customization policy | Permit U as Create, Update, or Disable; E as Create or non-seed date/enabled-state maintenance; S as Read only |
| 4 | Enforce package readiness | Require fresh exact-task export evidence, exact task identity and persisted Data Loader task context, ASM/member/header contract, exact MOO_REVN_CATEGORY parent-child closure, reviewed child delta, impact, preservation, and reopened final SHA-256 before FSM handoff |
| 5 | Enforce route boundary | Use Apps Common only for GET; route every supported write through the exact FSM package and core.data-loader |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
| --- | --- | --- | --- | --- | --- |
| SingleLookup Create or a Package Import Create row | Blocker | find_revenue_category_lookup_code | The same LookupCode already exists in MOO_REVN_CATEGORY or absence evidence is stale | Refresh exact state; choose a unique code or use Update only when that is the requester's intent | Yes |
| SingleLookup Update or Disable, a Package Import Update or Disable row, or Read | Blocker | find_revenue_category_lookup_code | No exact LookupCode exists in MOO_REVN_CATEGORY or the state lock is stale | Supply an existing code and rebuild package evidence; never convert the operation silently | Yes |
| SingleLookup mutation or any changed Package Import row | Blocker | verify_revenue_category_lookup_type | CustomizationLevel is missing or outside U, E, or S | Stop as unresolved configuration metadata; do not infer mutation permission | No automatic fix |
| SingleLookup mutation or any changed Package Import row with CustomizationLevel S | Blocker | verify_revenue_category_lookup_type | System lookup types do not permit lookup-code mutation | Use Read only; do not attempt REST or FSM mutation | No automatic fix |
| Update or Disable under CustomizationLevel E | Blocker | find_revenue_category_lookup_code | LastUpdatedBy is missing or equals SEED_DATA_FROM_APPLICATION | Extensible lookup types do not permit modifying predefined codes; select a non-predefined code or use Read | No automatic fix |
| Update of a non-predefined code under CustomizationLevel E | Blocker | verify_revenue_category_lookup_type | The delta includes Meaning, Description, DisplaySequence, or Tag instead of only EnabledFlag, StartDateActive, or EndDateActive | Limit the update to documented extensible-code active-state fields | Yes |
| SingleLookup Create, Update, or Disable; Package Import with changed child rows | Blocker | verify_revenue_category_lookup_type | FND_APP_STANDARD_LOOKUP.csv is header-only, lacks exactly one current MOO_REVN_CATEGORY parent carrier row, duplicates it, changes its business metadata, or any ORA_FND_APP_STANDARD_LOOKUP_CODE.csv row references a different parent key | Rebuild from the fresh export, add exactly one unchanged current parent carrier row with blank system-audit fields, verify every child references MOO_REVN_CATEGORY, then recompute the package hash | Yes |
| SingleLookup Create, Update, or Disable; Package Import | Blocker | verify_revenue_category_fsm_package | Fresh exact-target/release export, exact task name/code, persisted Data Loader task context, ASM/member/header identity, parent-child closure, reviewed delta/state/impact/preservation, or reopened SHA-256 is missing or inconsistent | Re-export, rebuild the smallest exact delta with its parent carrier row, validate every changed row, reopen/hash the ZIP, and never hand-author or synthesize task context | Yes |
| Package Export | Blocker | verify_revenue_category_fsm_package | Export is narrowed by LookupCode or row scope, or exact target/release/completed task identity and baseline receipt are missing | Export and validate the complete MOO_MANAGE_REVENUE_CATEGORIES task | Yes |
| Any direct REST, browser, shared setup import, or non-Data-Loader write route | Blocker |  | A supported mutation or Import is routed outside the exact FSM package and core.data-loader | Refuse that route and use the validated FSM package workflow | No automatic fix |
| Reading an existing revenue category under CustomizationLevel U, E, or S | Information | find_revenue_category_lookup_code | No blocker after one exact code resolves | Return sanitized current state through the read terminal without mutation preview or approval | No automatic fix |
| SetId, SetCode, BUOrgId, OrganizationCode, or MOO_SETID_REVN_CATEGORY is proposed as task scope | Blocker |  | A standard Revenue Line Set category is being treated as set-enabled setup | Use MOO_REVN_CATEGORY without a reference-set or business-unit identifier | Yes |
| Product selection or product-group assignment is proposed as the category-creation mechanism | Blocker |  | A runtime use of RevenueCategoryCode is being treated as lookup-code authoring | Supply the MOO_REVN_CATEGORY LookupCode and standard-lookup fields instead | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
| --- | --- | --- | --- |
| verify_revenue_category_lookup_type | Before reading or previewing a revenue-category code and before constructing a changed child-code package | Verified MOO_REVN_CATEGORY parent lookup type, current Meaning, Description, ModuleId, CustomizationLevel, RestAccessSecured, state fingerprint, and returned item link | ora_reference_lookups.md |
| find_revenue_category_lookup_code | Before returning SingleLookup Read or preparing a one-code Create, Update, or Disable package | Exact existing or absent state, timestamp, fingerprint, seed-data evidence, and returned child item link when present | ora_reference_lookups.md |
| verify_revenue_category_fsm_package | Before Package Export review or any FSM mutation handoff | For Export review, exact completed export/task identity only. For mutation/import handoff, add persisted Data Loader task context, parent carrier/closure, immutable package, row state/delta/impact/preservation evidence | ora_dependency_readiness.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.REVENUE_CATEGORY.DESIGN | decision | 6 | design_enforcement | read->OPP.REVENUE_CATEGORY.RETURN_READ;export_ready->OPP.REVENUE_CATEGORY.RETURN_EXPORT_READY;pass->OPP.REVENUE_CATEGORY.GATE;blocked->OPP.REVENUE_CATEGORY.RETURN_MISSING;failed->OPP.REVENUE_CATEGORY.RETURN_FAILED | OPP.REVENUE_CATEGORY.VERIFY_PACKAGE | stop | Enforce request mode, standard-lookup policy, per-row state and impact, immutable package readiness, and FSM-only mutation routing |
