# Country Security Profile Design Enforcement

Source: the supported task CSV template export for `PER_MANAGE_COUNTRY_SECURITY_PROFILE` and the failed import diagnostic that reports a missing child logical-row collection when the child row uses the parent view instance.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce CSV-only mutation route | Use the current target-environment Fusion task template and the core.data-loader-authorized task-level CSV import workflow for every create or update; do not use direct REST mutation |
| 2 | Parent logical row | Confirm the parent row uses CountrySecurityProfileMigration, CountrySecurityProfileName equals Name, and GroupingKey is a newly generated distinct uppercase 32-character hexadecimal GUID |
| 3 | Child logical rows | Confirm every country row uses CountrySecurityProfileCountryMigration, its two parent-name references equal the parent Name, and its GroupingKey is a newly generated distinct uppercase 32-character hexadecimal GUID different from every other new row |
| 4 | Country mapping | Confirm CountryCode equals the TerritoryCode returned by resolve_country_by_exact_name; if the exported child template contains TerritoryShortName, confirm it equals ValidatedCountryName and was not sourced from hcmCountriesLov |
| 5 | Package integrity | Confirm template headers and ASM_SETUP_CSV_METADATA.xml are unchanged, then require an immutable ZIP preview, exact approval, one import, and process-log verification |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A profile is created or a genuine rename is requested | Error | find_country_security_profile_by_exact_name; verify_country_security_profile_name_unique | A rename old exact Name does not resolve to one profile with the supplied current ID, or the proposed new Name has one or more exact matches; a create has any exact proposed-Name match | Correct the old identity or provide an available new Name; treat an unchanged proposed Name as an unchanged-name update | Yes |
| A genuine rename has an available new Name | Blocker |  | The current template-backed contract does not prove parent and child update identity across the Name change | Stop with `rename CSV identity mapping unverified` before CSV preview or import; do not infer update keys from REST IDs or generated GroupingKeys | No |
| A create CSV package is prepared | Error | resolve_country_by_exact_name | The parent ViewInstanceName is not CountrySecurityProfileMigration; its CountrySecurityProfileName does not equal Name; its GroupingKey is not a newly generated uppercase 32-character hexadecimal GUID; duplicates another new-row GroupingKey; or its creation ID is populated | Rebuild the parent row from the current template using the exact parent logical-row mapping and a distinct generated GroupingKey | Yes |
| A create CSV package includes one or more countries | Error | resolve_country_by_exact_name | A child ViewInstanceName is not CountrySecurityProfileCountryMigration; a child parent-name reference differs from the parent Name; its GroupingKey is not a newly generated uppercase 32-character hexadecimal GUID or duplicates another new-row GroupingKey; a child CountryCode differs from its resolved TerritoryCode; or a creation ID is populated | Rebuild every child row using the exact child logical-row mapping and a distinct generated GroupingKey; do not use the parent view instance for a child row | Yes |
| A create CSV package is prepared | Error |  | A required package member, header, or ASM_SETUP_CSV_METADATA.xml content differs from the current supported template | Export a current template and rebuild the package without changing its package schema | Yes |
| A country security profile create or update is requested | Error | resolve_country_security_profile_csv_context | The requested mutation does not use a current target-environment task-template CSV package, immutable ZIP preview, exact approval, one task-level CSV import, and process-log verification | Use the CSV-only task workflow; direct REST POST, PATCH, PUT, and DELETE are not supported | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_country_security_profile_by_exact_name | An existing profile is updated or renamed | Verified current Name and CountrySecurityProfileId | ora_reference_lookups.md |
| verify_country_security_profile_name_unique | A profile is created or genuinely renamed | Proposed Name availability and exact-match count | ora_reference_lookups.md |
| resolve_country_by_exact_name | Every child country row | CountryName, TerritoryCode | ora_reference_lookups.md |
| resolve_country_security_profile_csv_context | A country security profile create or update is requested | Current template, parent-child CSV linkage, immutable preview, approval, and process-log context | ora_dependency_readiness.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.LAYOUT | decision | 7 | design_enforcement | compliant->CSP.READINESS;noncompliant->CSP.ERROR | CSP.DEFAULT | stop | A country security profile create or update is being prepared for preview or import |
