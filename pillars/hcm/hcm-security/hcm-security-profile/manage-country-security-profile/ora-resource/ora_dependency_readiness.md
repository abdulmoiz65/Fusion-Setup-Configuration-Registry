# Country Security Profile Dependency Readiness

Source: the developer-provided country resolver contract and the supported task CSV template export for `PER_MANAGE_COUNTRY_SECURITY_PROFILE`.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Profile identity and Name availability | For a rename, resolve the old exact Name and match its ID to the supplied current ID. Then require zero exact matches for the proposed new Name. An unchanged proposed Name follows the update route. |
| 1 | Official task template | Export and retain the current target-environment task template with PER_COUNTRY_SECURITY_PROFILES.csv, ORA_PER_COUNTRY_SEC_PROF_COUNTRIES.csv, and unchanged ASM_SETUP_CSV_METADATA.xml |
| 2 | Profile identity | Validate Name and resolve one existing profile identifier when an update or child operation needs it |
| 3 | Country association | Resolve each supplied CountryName through hcmCountriesLov and obtain its TerritoryCode |
| 4 | Parent logical row | Create the parent row with ViewInstanceName CountrySecurityProfileMigration, use Name as its CountrySecurityProfileName, and use one newly generated distinct uppercase 32-character hexadecimal GUID as its GroupingKey |
| 5 | Child logical rows | Create one child row per resolved country with ViewInstanceName CountrySecurityProfileCountryMigration, parent Name references, a newly generated distinct uppercase 32-character hexadecimal GUID as that child row's GroupingKey, TerritoryShortName from ValidatedCountryName only when that column exists in the exported template, and CountryCode from TerritoryCode |
| 6 | Immutable import | Build the CSV ZIP from the current template, obtain approval of the exact preview, submit one task-level import through core.data-loader, and verify its process log |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| country_security_profile_name_availability | Proposed Name availability | Yes | A profile is created or a genuine rename is requested | Verify | countrySecurityProfiles through core.fusion-api.rest-api-client | verify_country_security_profile_name_unique | The proposed Name must have zero exact matches; a rename first verifies the old profile identity | Supply an available new Name; an existing exact match is a collision | Proposed Name availability and exact-match count |
| CSP-PROFILE | Existing profile identity | Conditional | Updating, renaming, or changing a child collection | Lookup | countrySecurityProfiles and current template-backed CSV context | find_country_security_profile_by_exact_name | Resolve the old exact Name to one profile; for rename require its ID to equal the supplied current ID before checking the proposed Name | Supply the current Name and ID for a rename; stop on no match, ambiguity, or ID mismatch | Verified CountrySecurityProfileId |
| CSP-RENAME-CSV | Rename CSV identity mapping | Yes | A genuine rename has passed proposed-name availability | Blocked | Current target-environment task template |  | The current contract does not prove how the existing parent and children retain update identity across a Name change | Stop with `rename CSV identity mapping unverified`; do not prepare preview or import or infer update keys from REST IDs or generated GroupingKeys | No import-ready rename mapping |
| CSP-COUNTRY | Country association | Yes | Creating or updating a country security profile | Lookup | hcmCountriesLov | resolve_country_by_exact_name | A country security profile must include at least one country, and each selected country needs its resolved CountryCode | Supply at least one CountryName | CountryCode: TerritoryCode |
| CSP-CSV | Parent/child logical row layout | Yes | Generating a create or update CSV import package | Verify | Current target-environment task CSV template export | resolve_country_security_profile_csv_context | Parent and child rows have distinct ViewInstanceName values, parent-name linkage, and one distinct generated GroupingKey per new row; the import requires its child logical-row collection to be present | Use CountrySecurityProfileMigration only for the parent row and CountrySecurityProfileCountryMigration only for child rows; preserve the template headers and metadata; generate one distinct uppercase 32-character hexadecimal GUID for every new row and use it as that row's GroupingKey; do not derive mappings from REST payloads; if the template contains TerritoryShortName, populate it from ValidatedCountryName rather than an hcmCountriesLov response | Parent: CountrySecurityProfileName, ViewInstanceName, GroupingKey, EnabledFlag; child: parent name references, template-only TerritoryShortName from ValidatedCountryName, ViewInstanceName, GroupingKey, CountryCode |
| CSP-CSV-MUTATION | CSV-only mutation route | Yes | Creating or updating a country security profile | Verify | Current target-environment task template, immutable preview, explicit approval, and task-level import process log | resolve_country_security_profile_csv_context | This task supports mutation only through its core.data-loader-authorized task-level CSV import workflow | Do not use direct REST POST, PATCH, PUT, or DELETE; submit one approved CSV import and verify the returned process log | Immutable CSV ZIP preview; approval record; import process log |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | A create has zero proposed-Name matches; an unchanged-name update has one verified old-name match; a genuine rename has a verified old Name and ID plus zero proposed-new-Name matches | Yes; read-only lookup only |
| Blocked | An existing target is missing, ambiguous, or has a different ID; or a create or genuine rename has an exact proposed-Name match | No; correct the target identity or proposed Name |
| Blocked | A genuine rename passes name availability but parent and child CSV update identity across the rename is unverified | No; report `rename CSV identity mapping unverified` before preview or import |
| Lookup | A CountryName has one exact hcmCountriesLov match | Lookup only |
| Blocked | No country is supplied | No |
| Blocked | A CountryName resolves to zero or multiple countries | No |
| Blocked | The supported CSV layout is unavailable | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.RENAME_CSV_GATE | decision | 4 | resolve_dependency | mapping_unverified->CSP.ERROR | CSP.VERIFY_PROFILE_NAME | stop | A genuine rename has an available new Name but its CSV parent and child update identity is unverified; block before preview or import |
| CSP.READINESS | decision | 8 | resolve_dependency | ready->CSP.READY;blocked->CSP.ERROR | CSP.LAYOUT | stop | A country security profile has at least one resolved country and a supported CSV package is required |
