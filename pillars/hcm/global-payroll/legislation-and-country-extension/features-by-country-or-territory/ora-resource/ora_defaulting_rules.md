# Features by Country or Territory Defaulting Rules

The source's Business Attribute Registry owns the ten business values below. Apply omitted Create defaults only during preparation, after reference and dependency resolution and the required business-readable default confirmation. Existing records retain their exact values unless an editable value was explicitly changed. This file does not serialize a DAT or execute a loader.

## Evidence

| Evidence ID | Source | Evidence Status | Used For | Limitation |
|---|---|---|---|---|
| SOURCE-DEFAULTS | FSCR_Features_by_Country_or_Territory_Codex_Source.md, Business Attribute Registry and Value Semantics | Source contract; proposal safeguards approved for initial authoring | Fixed and derived Create values; three editable options; omission, explicit reset, preservation, and branch-specific values | D01-D10 remain pending. Create defaults do not authorize resetting existing records. |
| ZIP-E02-E03 | CREATE_payrollFeaturesByTerritoryOrCountry.zip and CREATE_MULTIPLE_payrollFeaturesByTerritoryOrCountry.zip | DAT rows match source fixtures exactly | Single Create with HRY; multiple Create with null PayrollLicense; POSTAL_ADDR, Y, N, N and null SeededStatus | Source-recorded success was not rerun; fixture values are not universal Update defaults. |
| ZIP-E05-E07 | UPDATE_payrollFeaturesByTerritoryOrCountry.zip, UPDATE_MULTIPLE_payrollFeaturesByTerritoryOrCountry.zip, and UPSERT_payrollFeaturesByTerritoryOrCountry.zip | DAT rows match source fixtures exactly | HRY Update, documented PayrollLicense null reset, and populated mixed Create/Update profile | T01 detailed mixed post-read, T02 preserved nondefault options, T03 omitted values in both branches, T06 null/PER semantics, and T15 distinct per-target overrides remain pending. |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| TerritoryCode | Resolved canonical territory identity | Preparation for a confirmed Create candidate, including a new UPSERT branch; do not use partial request text as identity | No | resolve_legislation_by_exact_value |
| TerritoryShortName | Resolved canonical Legislation name | Preparation for a confirmed Create candidate, including a new UPSERT branch | No | resolve_legislation_by_exact_value |
| LegislationCode | Resolved TerritoryCode | Preparation for a confirmed Create candidate, including a new UPSERT branch; fixed derivation, not an independently editable option | No | resolve_legislation_by_exact_value |
| ApplicationId | 801 | Preparation for a confirmed Create candidate, including a new UPSERT branch; reject conflicting user-supplied identity instead of silently overriding it | No | |
| InstalledTerritory | N | Preparation for a confirmed Create candidate, including a new UPSERT branch; fixed Create value | No | |
| SeededTerritory | N | Preparation for a confirmed Create candidate, including a new UPSERT branch; fixed Create value | No | |
| SeededStatus | null | Preparation for a confirmed Create candidate, including a new UPSERT branch; fixed Create value | No | |
| PayrollLicense | null | Create preparation when Selected Extension was omitted and the business-readable default was confirmed; an explicitly supplied valid extension remains the user's choice | No | resolve_selected_extension |
| AddressStyleCode | POSTAL_ADDR | Create preparation when Address Style was omitted and the business-readable default was confirmed; target-territory validity must be resolved before preview | No | resolve_address_style_by_territory |
| AddressValidation | Y | Create preparation when Address Validation was omitted and the business-readable default was confirmed | No | resolve_address_validation_value |
| Omitted Create option confirmation | No implicit acceptance | PayrollLicense, AddressStyleCode, or AddressValidation is omitted for a new record; present the default through the authoritative label lookup before applying it; unresolved label behavior follows D04 | No | |
| Explicitly supplied editable Create values | No default substitution | A user supplied Selected Extension, Address Style, or Address Validation; use the resolved valid requested value, or block invalid or ambiguous input instead of replacing it with a default | No | |
| Existing-record identities and state | No Create defaults; retain exact current TerritoryCode, TerritoryShortName, LegislationCode, ApplicationId, InstalledTerritory, SeededTerritory, and SeededStatus | Update or existing UPSERT branch; full mixed-profile rows require the current values, including actual seeded or predefined state | No | find_features_by_criteria |
| Omitted existing-record editable values | No default; retain each current PayrollLicense, AddressStyleCode, and AddressValidation value | Update or existing UPSERT branch when that option was not requested for change; populate the canonical profile from known current values | No | find_features_by_criteria |
| Explicit Selected Extension reset | null as the requested value, not an omission default | User explicitly requests reset to the documented default state; keep this intent separate from unspecified input and from unresolved explicit PER selection semantics under D01 | No | |
| Null Selected Extension display | Preserve stored null | A null default or existing null needs a business label; the lookup file owns reverse-label resolution and must not replace the planned stored null with PER | No | resolve_selected_extension |
| Explicit PER selection and business-equivalent no-op | TBD | D01 remains pending for Search, explicit selection, and no-op behavior involving null versus PER; preserve the original stored value and input intent without automatic normalization | No | resolve_selected_extension |
| Unavailable current value | No default | A required current value is missing because the read was incomplete; stop instead of treating unavailable data as null or a Create default | No | find_features_by_criteria |
| Branch-specific confirmation | No cross-branch reset | A mixed UPSERT plan contains Create and Update candidates; acceptance of defaults for new records does not authorize changing omitted values of existing records | No | |
| Phase without Create defaulting | No defaults applied | Search, Delete, final pre-approval validation, or verification; use the prepared plan and current evidence required by that phase without synthesizing new business values | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FBCT.APPLY_DEFAULTS | step | 40 | apply_default | applied->FBCT.ENFORCE_DESIGN;blocked->FBCT.HANDLE_ISSUES | FBCT.RESOLVE_DEPENDENCIES | stop | Preparation applies only eligible Create defaults; preserve explicit requested and existing values; other phases pass through without defaulting |
