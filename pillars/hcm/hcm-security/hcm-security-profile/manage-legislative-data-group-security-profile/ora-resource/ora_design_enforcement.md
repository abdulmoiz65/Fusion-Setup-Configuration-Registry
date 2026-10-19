# Legislative Data Group Security Profile Design Enforcement

Source: developer-provided legislative data group security profile rules and the current supported task CSV package.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce CSV-only mutation route | Use the current target-environment Fusion task template and the core.data-loader-authorized task-level CSV import workflow for every create or update; do not use direct REST mutation |
| 2 | Confirm legislative data group scope | Confirm that the security profile includes at least one resolved legislative data group |
| 3 | Confirm supported CSV layout | Require a current task export, unchanged ASM_SETUP_CSV_METADATA.xml, immutable ZIP preview, exact approval, one import, and process-log verification before generating a CSV import package |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A profile is created or a genuine rename is requested | Error | find_ldg_security_profile_by_exact_name; verify_ldg_security_profile_name_unique | A rename's old exact Name does not resolve to one profile with the supplied current ID, or the proposed new Name has one or more exact matches; a create has any exact proposed-Name match | Correct the old identity or provide an available new Name; treat an unchanged proposed Name as an unchanged-name update | Yes |
| A genuine rename has an available new Name | Blocker |  | The current template-backed contract does not prove parent and child update identity across the Name change | Stop with `rename CSV identity mapping unverified` before CSV preview or import; do not infer update keys from REST IDs or name-based GroupingKey fallbacks | No |
| Creating or updating a legislative data group security profile | Blocker | resolve_legislative_data_group_by_name | No legislative data group association is present | Add at least one legislative data group identified by exact Name | Yes |
| Generating a CSV import package | Blocker | resolve_current_task_csv_layout | The package omits or changes a resolver-identified member, header, field mapping, parent-child linkage, metadata byte, or metadata node order; or its ViewInstanceName or GroupingKey differs from the template output and applicable member-specific fallback | Map parent and child records only to the current template resolver output. When the template omits a migration value, use the documented fallback and retain ASM_SETUP_CSV_METADATA.xml byte-for-byte unchanged | Yes |
| A legislative data group security profile create or update is requested | Blocker | resolve_ldg_security_profile_csv_context | The requested mutation does not use a current target-environment task-template CSV package, immutable ZIP preview, exact approval, one task-level CSV import, and process-log verification | Use the CSV-only task workflow; direct REST POST, PATCH, PUT, and DELETE are not supported | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_ldg_security_profile_by_exact_name | An existing profile is updated or renamed | Verified current Name and LegislativeDataGroupSecurityProfileId | ora_reference_lookups.md |
| verify_ldg_security_profile_name_unique | A profile is created or genuinely renamed | Proposed Name availability and exact-match count | ora_reference_lookups.md |
| resolve_legislative_data_group_by_name | Before the profile is ready | LegislativeDataGroupId for at least one selected legislative data group | ora_reference_lookups.md |
| resolve_current_task_csv_layout | Before CSV package generation | Exact members, headers and order, field mappings, parent-child linkage, ViewInstanceName values, GroupingKey patterns, metadata bytes, and node order | ora_reference_lookups.md |
| resolve_ldg_security_profile_csv_context | A legislative data group security profile create or update is requested | Current template, parent-child CSV linkage, immutable preview, approval, and process-log context | ora_dependency_readiness.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LDGSP.ENFORCE | decision | 8 | design_enforcement | compliant->LDGSP.READY;blocked->LDGSP.ERROR | LDGSP.READINESS | stop | A legislative data group security profile create or update is being prepared for preview or import |
