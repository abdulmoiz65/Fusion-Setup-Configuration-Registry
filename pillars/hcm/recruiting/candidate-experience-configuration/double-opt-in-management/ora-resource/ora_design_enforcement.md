# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Apply regional scope | Render the unknown-location checkbox and locations list only for LIST_OF_REGIONS. |
| 2 | Preserve country value mapping | Display CountryName and store TerritoryCode for each regional location. |
| 3 | Serialize regional rows | Write one FSM regional-setting row per selected nonblank TerritoryCode. |
| 4 | Enforce uniqueness | Remove or change a duplicate selected country code before Save and Close. |
| 5 | Resolve setting identity | Retain the uniquely exported `SettingValueId` for an existing value. When ORA_IRC_CAMP_DOI_REGIONS value 11351 is blank/null, or it is absent and unclaimed globally, use it for the first selected territory and derive additional rows from it with offset 1000000000 in stable order using two fresh exports. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Mode is LIST_OF_REGIONS | Blocker | resolve_country_by_name | A displayed country row has no selection or duplicates another selected TerritoryCode | Complete every country selection and remove or change duplicate countries | Yes |
| Mode is LIST_OF_REGIONS and an FSM archive is prepared | Blocker | resolve_country_by_name | A regional CSV value contains multiple TerritoryCodes, or a TerritoryCode has more than one row | Write exactly one ORA_IRC_CAMP_DOI_REGIONS row per unique resolved TerritoryCode | Yes |
| Mode is switched to LIST_OF_REGIONS | Blocker | allocate_new_doi_setting_value_ids | The archive adds a separate LIST_OF_REGIONS value but leaves the current blank or GLOBAL mode row unchanged | Update the existing canonical mode row using its exported SettingValueId and StringValue LIST_OF_REGIONS | Yes |
| Mode is not LIST_OF_REGIONS | Blocker | | Regional-only values remain selected for Save and Close | Use the selected mode; null or GLOBAL clears locations and sets the unknown-location value to N | Yes |
| An existing value is updated | Blocker | resolve_existing_doi_setting_value_id | SettingValueId is absent, ambiguous, or has an invalid parent join | Resolve it from the fresh export and validate the final join; never request or generate a replacement numeric ID | Yes |
| A required SettingValueId cannot be resolved | Blocker | resolve_existing_doi_setting_value_id or allocate_new_doi_setting_value_ids | Export resolution is absent or ambiguous, or the governed allocation convention cannot produce a collision-free ID | Stop package preparation and ask the user to provide the exact SettingValueId without disclosing internal allocator values; do not invent a value or select an ambiguous row | Yes |
| A new regional value is authored | Blocker | allocate_new_doi_setting_value_ids | The ORA_IRC_CAMP_DOI_REGIONS value 11351 is duplicated, nonblank, has a mismatched parent join, is used globally by another setting, or an ID derived with offset 1000000000 is blank, nonnumeric, over 18 digits, present in either fresh export, or duplicated in the package | Use blank/null 11351, or create it when absent and unclaimed globally, for the first requested territory. For additional regions, derive in stable order from 11351 with offset 1000000000, then rebuild from the second export if its identity or collision state changed | Yes |
| A new value was imported | Blocker | | A fresh unscoped export does not show each allocated SettingValueId with the intended setting identity and parent join | Stop dependent work and resolve the import result before proceeding | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_country_by_name | Mode is LIST_OF_REGIONS and a country display value is supplied | TerritoryCode | ora_reference_lookups.md |
| resolve_existing_doi_setting_value_id | An existing value is updated | SettingValueId | ora_reference_lookups.md |
| allocate_new_doi_setting_value_ids | New regional values are authored | Seeded regional anchor 11351 for one region, or one unique numeric LONG per row derived from 11351 with offset 1000000000 for two or more | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOI.ENFORCE_REGION_DESIGN | decision | 30 | design_enforcement | compliant->DOI.APPLY_MODE_DEFAULT;blocked->DOI.HANDLE_DESIGN_ISSUE | DOI.VALIDATE_INPUT | stop | Before Save and Close |
