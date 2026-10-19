# Country Security Profile Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Security profile identity | A supplied Name or a Name derived from validated configuration, current target-environment task template, resolved country values, and CSV context | Stop | Preserve a supplied Name exactly as provided (up to the source-schema limit of 240 characters), or derive CountrySecurityProfile plus the configured validated CountryName values; for a derived Name only, retain only ASCII letters and digits and limit it to 119 characters, then export the current template, resolve country values, and prepare the template-backed CSV package | Creating a security profile | verify_country_security_profile_name_unique |
| Existing profile identity | Current Name and CountrySecurityProfileId; proposed new Name for a rename | Stop | Resolve the old exact Name to one profile and require its returned ID to equal the supplied current ID before checking the proposed new Name | Updating or renaming an existing profile | find_country_security_profile_by_exact_name |
| Country association | One or more CountryName values | Stop | Supply at least one CountryName and resolve each through hcmCountriesLov | Creating or updating a country security profile through the supported CSV package | resolve_country_by_exact_name |
| Existing profile target | CountrySecurityProfileId and current target-environment template-backed CSV context | Stop | Resolve one current profile by exact Name, export the current template, and resolve exact parent-child CSV linkage before an update | Updating a profile or its child collection | find_country_security_profile_by_exact_name |
| Supported CSV package layout | PER_COUNTRY_SECURITY_PROFILES.csv, ORA_PER_COUNTRY_SEC_PROF_COUNTRIES.csv, and ASM_SETUP_CSV_METADATA.xml with the current exported headers and metadata | Stop | Start from the current supported template export; do not rename, remove, or invent package members or columns | Generating a CSV import package | |
| CSV-only mutation package | Current target-environment task template, immutable ZIP preview, exact approval, one task-level import, and process-log verification | Stop before any create or update | Use the core.data-loader-authorized task-level CSV import workflow; do not construct or submit a direct REST mutation | Creating or updating a country security profile | resolve_country_security_profile_csv_context |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A supplied Name is empty or exceeds the source-schema limit of 240 characters | Blocked | Supply a valid Name of no more than 240 characters; preserve its supplied characters and length | |
| A derived Name is empty, contains a character other than an ASCII letter or digit, or exceeds 119 characters | Blocked | Derive a meaningful Name from the validated configuration by retaining only ASCII letters and digits and truncating it to 119 characters, or request a user-supplied Name | |
| No country association is supplied | Blocked | Supply at least one CountryName | resolve_country_by_exact_name |
| A CountryName resolves to zero or multiple countries | Blocked | Supply a disambiguating CountryName | resolve_country_by_exact_name |
| A CSV package is requested without the current supported template layout | Blocked | Export the current task template again; do not invent CSV columns, keys, or package metadata | |
| An existing profile is required but Name resolves to zero or multiple profiles | Blocked | Supply an unambiguous profile identity | find_country_security_profile_by_exact_name |
| A create or update lacks template-backed CSV context, immutable preview, exact approval, one import, or process-log verification | Blocked | Export the current target-environment template and use the approved CSV-only workflow; do not derive CSV mappings from a REST payload | resolve_country_security_profile_csv_context |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Profile Name availability | For a create or genuine rename, require zero exact matches for the proposed Name. An exact match blocks; multiple matches are ambiguous. If proposed Name equals current Name, use the unchanged-name update route. | A profile is created or a genuine rename is requested | verify_country_security_profile_name_unique |
| Rename CSV identity mapping | Block with `rename CSV identity mapping unverified` before CSV preview or import; never infer update keys from REST IDs or generated GroupingKeys | A genuine rename passes name availability |  |
| Name | For a supplied Name, preserve the value exactly as supplied and accept up to 240 characters. For a new profile without a supplied Name, derive CountrySecurityProfile followed by the validated CountryName values in configured order, remove all non-alphanumeric characters, and truncate to 119 characters | Always | |
| EnabledFlag | Accept a boolean; it is updateable and defaults to true | The flag is supplied | |
| ViewAllFlag | Do not accept a user-supplied value because the describe contract marks it non-updateable | Always | |
| CountrySecurityProfileName | Require a profile name in PER_COUNTRY_SECURITY_PROFILES.csv and the matching parent reference in ORA_PER_COUNTRY_SEC_PROF_COUNTRIES.csv | Always for a CSV package | |
| CountryName | Require at least one exact country name; resolve it through hcmCountriesLov | A country association is supplied | resolve_country_by_exact_name |
| CountryCode | Require the TerritoryCode returned by hcmCountriesLov and map it to CountryCode in ORA_PER_COUNTRY_SEC_PROF_COUNTRIES.csv | A country association is supplied | resolve_country_by_exact_name |
| Parent logical row | Require exactly one parent row in PER_COUNTRY_SECURITY_PROFILES.csv for the requested profile: CountrySecurityProfileName equals Name; GroupingKey is a newly generated distinct uppercase 32-character hexadecimal GUID; ViewInstanceName is CountrySecurityProfileMigration; EnabledFlag is Y or N; CountrySecurityProfileId is blank for create | Always for a create CSV package | |
| Child logical row | Require one ORA_PER_COUNTRY_SEC_PROF_COUNTRIES.csv row per resolved country: both parent-name references equal the parent Name; GroupingKey is a newly generated distinct uppercase 32-character hexadecimal GUID that differs from every other new row; when the exported template has TerritoryShortName, populate it from ValidatedCountryName, not from a REST response field; ViewInstanceName is CountrySecurityProfileCountryMigration; CountryCode equals the resolved TerritoryCode; creation IDs are blank | Always for a create CSV package | resolve_country_by_exact_name |
| RemoveRow | Accept Y only when removing an existing child association | Removing a child association | |
| CSV mapping source | Derive parent and child CSV fields only from the current task template and resolved lookup values; never derive them from a REST payload | Always for a create or update | resolve_country_security_profile_csv_context |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.VALIDATE | decision | 1 | validate_input | new_profile->CSP.VERIFY_PROFILE_NAME;existing_or_renamed_profile->CSP.FIND_PROFILE;invalid->CSP.ERROR | none | stop | A profile request is supplied; a proposed Name equal to current Name is an unchanged-name update |
