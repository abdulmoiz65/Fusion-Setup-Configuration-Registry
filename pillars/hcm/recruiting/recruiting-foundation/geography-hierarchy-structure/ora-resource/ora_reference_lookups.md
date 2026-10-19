# Configured Geography Level Labels

POC/demo display enrichment for ORA_IRC_GEO_HRCHY_STRUCTURE. Reuses the address
metadata contract of HCM Manage Locations; it does not invoke that task's writes.
The FSM structure export remains authoritative for which elements are configured.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_structure_level_labels | Explaining an existing country's configured levels after GHS.VALIDATE selects the current exported row | Selected environment; exported CountryCode, GeoLevel2ColumnName, GeoLevel3ColumnName | GET /crmRestApi/resources/11.13.18.05/addressStyleFormats with finder=StyleFormatFilter;BindCountryCode={CountryCode},BindStyleCode=SUPP_TAX_AND_RPTNG_ADDR and expand=AddressStyleFormatLayout and onlyData=true | CountryCode, StyleFormatCode, AddressStyleFormatLayout.GeographyLevel, GeographyType, AttributeLabel | Require exactly one item with the exact CountryCode and StyleFormatCode=SUPP_TAX_AND_RPTNG_ADDR_{CountryCode}, complete pagination, and an array layout. For each nonblank exported GEOGRAPHY_ELEMENTn, match numeric GeographyLevel=n, not Recruiting level, row order, LineNumber, Position, or AttributeName. Require exactly one matching row with nonblank GeographyType | Display-only level label from nonblank AttributeLabel, otherwise GeographyType; include GeographyType, unchanged element column, country, environment and resolution status | Keep raw configured elements. Mark the affected label unresolved and disclose the reason; never select the first duplicate or substitute another country, style, CE API, or hardcoded mapping |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Live execution | Use core.fusion-api.rest-api-client and the selected environment's configured authentication. Do not add task-local transport or change auth settings. Retain sanitized export and response evidence with environment and retrieval time. |
| Parent or child data is paginated or incomplete | Resolve every relevant page through the declared client before claiming unique matches; otherwise report labels unresolved. |
| A configured value is blank | Display Not configured; do not infer a level from available address fields. |
| A configured value does not exactly match GEOGRAPHY_ELEMENT followed by an integer from 1 through 10 | Preserve the raw value and mark its label unresolved; do not parse partial strings or correct the mapping. |
| A layout row has null GeographyLevel or GeographyType | Do not use that row as mapping evidence. A matching level with missing type is unresolved. |
| More than one row matches an element number | Mark that element unresolved, even if labels appear identical; other uniquely resolved elements may still be displayed. |
| Address labels differ from geography types | Show both returned label and GeographyType; do not reinterpret or overwrite the type based on wording. |
| HTTP/authentication/transport failure | Allow the core client's single authentication refresh. If still unavailable, return the configured raw values with labels unresolved and the safe failure reason; do not retry repeatedly or call a substitute API. |
| Successful display | Lead with the resolved business labels and include the raw mapped elements. Describe them as address-format-derived POC labels, not guaranteed geography metadata. Country is the root; GeoLevel2ColumnName and GeoLevel3ColumnName represent Recruiting levels 2 and 3. If the user calls these the first and second sublevels, show the same two fields without shifting element numbers. |
| Import or update requested | The lookup supplies display information only. Never replace GEOGRAPHY_ELEMENTn in CSV with State, Province, City, or GeographyType. Do not alter ActiveFlag, ModuleId, ObjectStatus, omit a configured element, or authorize an import. Keep existing package and approval gates. |

## Evidence and Boundaries

Validated during the September 24, 2026 POC: Canada address metadata returned
2=PROVINCE, 3=CITY, 4=POSTAL_CODE; US returned 2=STATE, 3=COUNTY, 4=CITY,
5=POSTAL_CODE. A fresh US FSM export mapped Recruiting levels 2 and 3 to
GEOGRAPHY_ELEMENT2 and GEOGRAPHY_ELEMENT4. These are regression examples,
not runtime defaults or proof of coverage for other countries and styles.

Existing cross-area contract:
`pillars/hcm/global-human-resources/locations/manage-locations/ora-resource/ora_reference_lookups.md`,
resolver `resolve_location_address_contract`.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GHS.LABELS | step | 15 | reference_lookup | resolved->GHS.READ_DONE;unresolved->GHS.READ_DONE | GHS.VALIDATE | continue | A configured-level read passed input checks; run resolve_structure_level_labels and return resolved labels or explicit unresolved results |
