# Reference Lookups

Use `core.fusion-api.rest-api-client` for HCM LOV resources. The `{version}`
path parameter defaults to `latest`. URL-encode parameters at runtime; never
store a host, tenant value, or resolved identifier.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_country_by_name | Mode is LIST_OF_REGIONS and a CountryName display value is supplied | CountryName | core.fusion-api.rest-api-client -> /hcmRestApi/resources/{version}/hcmCountriesLov, where `{version}` defaults to `latest`, with finder=findByWord;DataSecurityPrivilege=true,FilterAttributes=CountryName,SearchTerms=<runtime URL-encoded CountryName>; q=ObsoleteFlag=false; fields=TerritoryCode,CountryName,ObsoleteFlag; onlyData=true; limit=25; offset=0 | CountryName, TerritoryCode, ObsoleteFlag | Read every page, exclude obsolete results, and require exactly one result whose CountryName exactly matches the supplied CountryName; never choose by result position | TerritoryCode: TerritoryCode; CountryName: CountryName for preview | If `findByWord` cannot return one exact current match, request the explicit TerritoryCode; do not infer or substitute one. |
| resolve_existing_doi_setting_value_id | An existing Double Opt In value is being updated | Fresh unscoped `ORA_IRC_DOI_MANAGEMENT` export and requested mode | Exported setting-value rows and their parent joins | Require exactly one exported `SettingValueId` whose setting identity and parent joins match the existing Double Opt In value; retain that value without deriving or generating an ID | SettingValueId | N/A | Stop package preparation and ask the user for the exact SettingValueId when the existing value cannot be determined uniquely; do not substitute an unrelated exported ID. |
| allocate_new_doi_setting_value_ids | New Double Opt In regional values are authored | Two fresh unscoped `ORA_IRC_DOI_MANAGEMENT` exports and planned regional rows | Exported ORA_IRC_CAMP_DOI_REGIONS values, SettingValueId inventory, and package rows | Resolve the seeded ORA_IRC_CAMP_DOI_REGIONS row, SettingValueId 11351 for this release. When it is blank or null, use it for the first requested region. When it is absent and 11351 is unused globally, create the first requested regional row with 11351; derive each additional region from 11351 with offset 1000000000. | Region anchor and territory SettingValueId values | N/A | Stop package preparation on a duplicate, nonblank, mismatched, globally colliding, stale base, or overflow. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| One or more CountryName values are supplied while mode is LIST_OF_REGIONS | Resolve each supplied CountryName independently through hcmCountriesLov `findByWord` with runtime URL encoding and complete pagination; retain one TerritoryCode per exact current match. |
| `findByWord` is unavailable, returns no exact current match, or returns multiple exact current matches | Stop resolution for that country and ask the user to supply its exact TerritoryCode. Do not choose a result by position or manufacture a code. |
| An explicit TerritoryCode is supplied after the fallback prompt | Use the exact nonblank value as the stored regional value and mark it user-supplied in the preview. It is not evidence that hcmCountriesLov resolved the CountryName; still reject duplicate supplied or resolved TerritoryCode values. |
| An existing Double Opt In setting value cannot be resolved uniquely from the fresh export | Stop package preparation and ask the user to provide the exact SettingValueId. Do not reuse an unrelated SettingValueId. |
| A new Double Opt In setting value is authored | Apply the temporary derived-ID convention below and serialize one collision-checked nonblank numeric LONG SettingValueId for each new row. If the required ID cannot be resolved by the convention, stop and ask the user to provide the exact SettingValueId. The FSM importer requires the field; it does not generate a blank value. |
| An import that adds a new Double Opt In setting value completes | Perform a fresh unscoped export and verify exactly one intended setting identity and parent join for each allocated SettingValueId. |
| An FSM archive is prepared for one or more resolved regions | Serialize each resolved TerritoryCode as its own ORA_IRC_CAMP_DOI_REGIONS CSV row; never send a comma-separated list in one StringValue. |
| The country is absent, obsolete, or the match is ambiguous and no TerritoryCode is supplied | Stop before Save and Close and request the exact TerritoryCode; do not select a result by position or substitute a TerritoryCode. |
| Mode is null or GLOBAL | Do not call the country lookup. |

## Temporary Derived-ID Convention

This release-only convention exists because the DOI FSM importer requires a
nonblank `SettingValueId` and does not invoke Fusion's server-side ID generator
for a blank CSV field. It is a client-side compatibility policy, not a
reserved Fusion ID range. Retire it when the importer creates omitted IDs
server-side.

1. Obtain a first fresh, unscoped `ORA_IRC_DOI_MANAGEMENT` export and collect
   every numeric `SettingValueId`.
2. Resolve `SettingValueId` `11351` as the first-region identity.
   - When exactly one `ORA_IRC_CAMP_DOI_REGIONS` row with `11351` has a blank
     or null StringValue, validate its parent join and use it for the first
     requested TerritoryCode, including a multi-region request.
   - When no such regional row exists and no exported setting value anywhere
     uses `11351`, create the first requested regional row with `11351`.
   - If more than one matching regional row exists, any value anywhere uses
     `11351` under another setting, or the regional row has a nonblank value
     or mismatched parent join, stop. Do not substitute the mode ID `11350`.
3. With two or more requested regional rows, assign `11351` to the first
   requested TerritoryCode in stable package order. Assign each additional
   TerritoryCode from the regional anchor using offset `1000000000`:
   `SettingValueId = region_anchor_id + 1000000000 + ordinal`, where the first
   derived territory is `1000011351` and each additional territory increments
   by one. Never assume `11352`, `11353`, or subsequent consecutive seed IDs
   are available; SettingValueId is globally unique.
4. Require every derived value to be a positive decimal integer with no more
   than 18 digits, absent from the first export, and unique within the complete
   package. Preserve every existing exported ID unchanged. Do not use blank
   IDs, `max + 1`, arbitrary user-supplied IDs, or a derived value that collides
   with an exported value.
5. Immediately before Data Loader preflight, obtain a second fresh, unscoped
   export and repeat the anchor and collision checks. If the region anchor,
   anchor state, or any derived ID differs or collides, discard the prepared
   archive and rebuild from the second export.

If an existing ID cannot be resolved uniquely, or the governed allocation
convention cannot supply a collision-free ID, stop preparation and ask the user
to provide the exact `SettingValueId`. The user-facing prompt must not disclose
an internal seed, derived value, or allocation formula. Do not invent a numeric
value, select an ambiguous export row, or replace an existing value.

When configuring the mode as LIST_OF_REGIONS, resolve the current canonical
mode row from the fresh export. If its StringValue is blank or GLOBAL, serialize
that same SettingValueId with StringValue `LIST_OF_REGIONS` in the archive.
Do not add a second LIST_OF_REGIONS row as a substitute for updating the
canonical current mode row. The regional anchor is separate: it is the seeded
ORA_IRC_CAMP_DOI_REGIONS row with SettingValueId `11351`.

Record the two export references, chosen anchor, offset, derived values, and
collision-check result with the immutable archive. A blank/null anchor or an
unclaimed `11351` becomes the configured first regional row; every additional
territory uses a derived ID. After import, fresh-export and verify the mode and
every territory ID with their intended setting identity and parent join.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOI.RESOLVE_COUNTRY | decision | 15 | reference_lookup | resolved->DOI.VALIDATE_INPUT;not_applicable->DOI.VALIDATE_INPUT;blocked->DOI.HANDLE_INPUT_ISSUES | DOI.CHECK_READINESS | stop | Before validating a regional country selection |
