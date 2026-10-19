# Country Security Profile Reference Lookups

Execute every read-only Fusion REST lookup in this file through
`core.fusion-api.rest-api-client`; do not issue a direct REST request. Replace
`{fusion_environment_host}` and `{version}` at runtime with the live Fusion
environment host and active REST API version.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| verify_country_security_profile_name_unique | A profile is created or a genuine rename is requested after old-profile identity is verified | Proposed Name | GET /hcmRestApi/resources/{version}/countrySecurityProfiles through core.fusion-api.rest-api-client | CountrySecurityProfileId, Name | Retain only rows whose Name exactly equals the proposed Name. For a create or genuine rename, zero matches means the Name is available. A proposed Name equal to the verified current Name is an unchanged-name update, not a rename. | Proposed Name availability and exact-match count | One or more exact matches block a create or genuine rename; multiple matches are ambiguous. A genuine rename with zero matches proceeds only to CSP.RENAME_CSV_GATE, never to CSV preview. |
| find_country_security_profile_by_exact_name | An existing profile, rename target, or child association must be identified | Current exact Name; supplied current CountrySecurityProfileId for a rename | https://{fusion_environment_host}/hcmRestApi/resources/{version}/countrySecurityProfiles | CountrySecurityProfileId, Name, EnabledFlag, ViewAllFlag | Require exactly one returned profile whose Name exactly equals the current Name; for a rename, require its ID to equal the supplied current ID before checking the proposed Name | Verified current CountrySecurityProfileId, Name, EnabledFlag, ViewAllFlag | Stop on zero or multiple old-name matches, or a mismatch with the supplied current ID; never use the proposed new Name to identify the old profile |
| resolve_country_by_exact_name | A country is included in a country security profile | CountryName | /hcmRestApi/resources/{version}/hcmCountriesLov?q=CountryName%3D%27{url_encoded_CountryName}%27&onlyData=true&limit=100 | Read CountryName and TerritoryCode only | Require exactly one result | ValidatedCountryName: CountryName; CountryCode: TerritoryCode | Stop and request a disambiguating CountryName |

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_country_security_profile_csv_context | A country security profile create or update is prepared | Current target-environment task template, resolved country values, parent/child CSV rows, immutable preview, approval record, and process log | Require the exact template members and unchanged ASM_SETUP_CSV_METADATA.xml; require parent and child identity linkage; for every new row, generate a distinct uppercase 32-character hexadecimal GUID using only 0-9 and A-F, such as 551F45B6C8A2445BE0534280F50A76B1, and use it as that row's GroupingKey; bind approval to the immutable ZIP; require exactly one import result with a process log | Template-backed parent/child context; generated new-row GroupingKeys; preview fingerprint; approval record; and process-log evidence | Stop; do not derive CSV mappings from REST payloads, reuse a GroupingKey across new rows, submit a direct REST mutation, or reuse stale approval |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The profile lookup returns exactly one profile | Use the returned identifier only for the current scoped task operation |
| The profile lookup returns zero or multiple profiles | Stop; do not select a profile by guesswork |
| A country name is resolved | Use the URL-encoded exact predicate; for example, q=CountryName%3D%27Japan%27 |
| The country lookup returns exactly one country | Map TerritoryCode to CountryCode for the selected country association |
| The country lookup returns zero or multiple countries | Stop; do not select a country or CountryCode by guesswork |
| The exported child CSV has a TerritoryShortName column | Populate it from ValidatedCountryName after the exact CountryName match; it is a CSV-only value, not an hcmCountriesLov requested or returned field |
| A CSV mutation is prepared | Use resolve_country_security_profile_csv_context; the profile and country REST endpoints remain read-only lookup sources and never supply CSV field mappings |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.FIND_PROFILE | decision | 2 | reference_lookup | found_unchanged->CSP.RESOLVE_COUNTRY;found_rename->CSP.VERIFY_PROFILE_NAME;not_found_or_ambiguous->CSP.ERROR | CSP.VALIDATE | stop | An existing profile or rename target is requested; verify the supplied current ID for a rename |
| CSP.VERIFY_PROFILE_NAME | decision | 3 | reference_lookup | create_available->CSP.RESOLVE_COUNTRY;rename_available->CSP.RENAME_CSV_GATE;unavailable_or_ambiguous->CSP.ERROR | CSP.VALIDATE | stop | A new Name is checked only after the old target is verified for a rename |
| CSP.RESOLVE_COUNTRY | step | 5 | reference_lookup | resolved->CSP.DEFAULT;not_found_or_ambiguous->CSP.ERROR | none | stop | One or more countries are included in a country security profile |
