# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Double Opt In mode | Double Opt In Settings: null, GLOBAL, or LIST_OF_REGIONS | Stop before Save and Close | Select No Double Opt In, Enable Globally, or Set Specific Regions | Always | |
| Regional country selection | One or more HCM Countries LOV selections, or an explicit TerritoryCode after `findByWord` cannot resolve the supplied country; stored TerritoryCode | Stop before Save and Close | Select a country for every displayed row, or provide the exact TerritoryCode requested by the resolver | Mode is LIST_OF_REGIONS | resolve_country_by_name |
| Existing Double Opt In setting identity | One uniquely resolved exported SettingValueId, or an exact user-provided SettingValueId after resolution fails | Stop package preparation | Resolve the existing value from the fresh export; when that fails, ask the user for the exact SettingValueId; do not substitute an ID | An existing value is updated | resolve_existing_doi_setting_value_id |
| New Double Opt In setting identity | The existing blank or null ORA_IRC_CAMP_DOI_REGIONS anchor SettingValueId 11351, or 11351 when absent and unused globally, for the first region; then one collision-checked numeric LONG per additional region derived from 11351 with offset 1000000000 | Stop package preparation | Apply the temporary derived-ID convention using two fresh exports | New regional values are authored | allocate_new_doi_setting_value_ids |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Unknown-location setting | Accept Y or N | Mode is LIST_OF_REGIONS and the checkbox is supplied | |
| Country value | Use CountryName for display and TerritoryCode for the stored value; label an explicit fallback code as user-supplied | Mode is LIST_OF_REGIONS | resolve_country_by_name |
| Duplicate TerritoryCode | Do not commit when a selected country code is duplicated | Mode is LIST_OF_REGIONS | |
| FSM regional serialization | Write one ORA_IRC_CAMP_DOI_REGIONS CSV row for each resolved nonblank TerritoryCode; do not combine values with commas | Mode is LIST_OF_REGIONS and an FSM archive is prepared | |
| Existing SettingValueId | Retain the uniquely exported value and validate its intended parent join in the final archive; never generate a replacement numeric identifier | An existing value is updated | resolve_existing_doi_setting_value_id |
| Unresolved SettingValueId | Stop and ask the user for the exact SettingValueId when export resolution or the governed allocation convention cannot determine a collision-free identity; do not disclose an internal seed, derived value, or allocation formula in that prompt | An existing or new setting value is authored | resolve_existing_doi_setting_value_id or allocate_new_doi_setting_value_ids |
| New SettingValueId | For one ORA_IRC_CAMP_DOI_REGIONS territory, update the exported blank or null seed row with SettingValueId 11351, or create that row with 11351 when it is absent and unused globally. For two or more territories, assign 11351 to the first requested nonblank TerritoryCode and serialize one unique collision-checked positive decimal LONG per additional TerritoryCode, derived with offset 1000000000 in stable order beginning at 1000011351. Do not use 11352 or another consecutive seed ID. | A new regional value is authored | allocate_new_doi_setting_value_ids |
| Derived-ID revalidation | Obtain a second fresh unscoped export immediately before preflight. Reject a changed anchor, changed fallback state, collision, duplicate, nonnumeric value, or value exceeding 18 digits. | A new value is authored | allocate_new_doi_setting_value_ids |
| Canonical mode update | When switching to LIST_OF_REGIONS, retain the SettingValueId of the current blank or GLOBAL mode row and change its StringValue to LIST_OF_REGIONS. | Mode is switched to LIST_OF_REGIONS | allocate_new_doi_setting_value_ids |
| Allocated SettingValueId verification | After import, verify each allocated ID has the intended setting identity and parent join through a fresh unscoped export | A new value was imported | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOI.VALIDATE_INPUT | step | 20 | validate_input | valid->DOI.ENFORCE_REGION_DESIGN;invalid->DOI.HANDLE_INPUT_ISSUES | DOI.RESOLVE_COUNTRY | stop | Before Save and Close |
