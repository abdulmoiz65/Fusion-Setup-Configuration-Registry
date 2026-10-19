# Manage Locations Design Enforcement

## Purpose

Defines the mandatory Location identity, set, address, source-scope, and
loader-key design gates evaluated before preview or routing. It does not
perform lookups, apply defaults, or create missing setup.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Resolve one exact target or confirm zero exact LocationCode matches for create |
| 2 | Validate context | Confirm YYYY/MM/DD effective context and one exact reference-data set |
| 3 | Validate MAIN address | Require the resolved country's mandatory MAIN-address fields on the base Location row |
| 4 | Limit mutation scope | Keep the base row and only child or EFF rows the user modified |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| IDENTITY | Read, edit, or delete | Blocking | find_manage_locations | Identity is absent, unresolved, or ambiguous | Supply one exact LocationCode or LocationName | Input fix |
| CREATE_UNIQUENESS | Create | Blocking | find_manage_locations | Exact LocationCode already exists or is ambiguous | Supply one unique LocationCode; a duplicate LocationName is permitted | Input fix |
| SET_CONTEXT | Create or edit | Blocking | resolve_location_reference_set | SetCode or SetId is unresolved or ambiguous | Supply one exact reference-data set | Lookup fix |
| MAIN_ADDRESS | Create or MAIN-address edit | Blocking | resolve_location_address_contract | Country or its SUPP_TAX_AND_RPTNG_ADDR layout is unresolved; a mandatory labelled value is missing; or a layout attribute does not map to one loader field | Supply the missing labelled values or correct the country-specific mapping | Input or lookup fix |
| MAIN_ADDRESS_EDIT | MAIN address edit | Blocking | resolve_location_address_contract | The requested delta combined with the fresh MAIN address fails the resulting country/style layout | Correct the delta; author only the requested changes | Input fix |
| UPDATE_ACTION_REASON | Date-effective edit includes `ActionReasonCode` | Blocking | resolve_location_action_reason | The value lacks explicit user provenance, was copied or defaulted from a prior/create row, is expired for the requested date, or is invalid for the update operation | Omit the optional field, or resolve the exact user-supplied update reason independently | Lookup or input fix |
| ZAP_PROHIBITED | ZAP or physical-delete request | Blocking |  | The requested operation would physically remove the logical Location or uses ZAP | Return `UNSUPPORTED`; do not perform target/history resolution, build a Data Loader source, preview, approve, or invoke Core Data Loader | No |
| DATE_EFFECTIVE_DELETE | Delete | Blocking | resolve_location_delete_history | The selected history row is first, unresolved, ambiguous, has no predecessor, or the derived retained start/deletion end does not exactly match complete fresh history | Resolve one non-first row and derive the range from its immediately preceding row and selected end | Lookup or input fix |
| DATE_EFFECTIVE_DELETE_SOURCE | Delete | Blocking |  | The source contains root DELETE/ZAP, mixed MERGE and DELETE, any child row, ActionReasonCode, an absent or repeated `SET PURGE_FUTURE_CHANGES Y` directive, a non-Location MERGE, an unsupported key, a root identity other than the fresh `LocationId` + `SetCode` + `LocationCode` tuple, or a range other than predecessor start through selected end | Rebuild a one-root-row Location MERGE from the live workbook with the complete root identity and derived history range | Source rebuild |
| EDIT_SURROGATE_KEYS | Edit or delete of any Location object | Blocking | find_manage_locations | Any edited base, ExtraInfo, or Legislative row lacks its live `LocationId`, `LocationExtraInfoId`, or `LocationLegId`; or a MAIN edit is represented as a LocationOtherAddress row | Resolve every edited row's live surrogate ID; keep MAIN address changes on the root row | Lookup fix |
| TIMEZONE_LOADER_VALUE | TimezoneName is included on the base Location row | Blocking | resolve_location_address_contract | TimezoneName is not the exact `Name` of one enabled time-zone LOV item matched by the selected TimezoneCode | Resolve the enabled LOV record and write its `Name`; do not use a code or display variant | Lookup fix |
| SHIP_TO_REFERENCE_CONTRACT | ShipToSiteFlag or a ship-to reference is included | Blocking | find_manage_locations | `Y` includes any ship-to reference; or `N` lacks either a resolved ID or a complete code-and-set pair; or both alternatives are populated | Omit all references for `Y`; for `N`, provide exactly one valid reference alternative | Input or lookup fix |
| LIVE_SCHEMA_COVERAGE | Create, edit, or delete | Blocking |  | An included Location section or supplied attribute is not reconciled to the current live Data Loader template and its value contract | Resolve or remove the unsupported value, regenerate the source from current metadata, and restart review | Source rebuild |
| LIVE_VALUE_CONSTRAINTS | Create, edit, or delete | Blocking |  | Any supplied value violates the current live data type, maximum length, precision/scale, allowed value/domain, or reference contract; this includes any dynamically resolved EFF segment | Correct or resolve the value from current live metadata; never hardcode an EFF segment contract; regenerate and restart review | Input or lookup fix |
| EFF_CONTEXT_COVERAGE | A LocationExtraInfo or LocationLegislative row is included | Blocking | read_location_eff_context | Its category, context, unique-key segments, or supplied segments do not match current live metadata; or its FLEX value does not exactly equal its `LeiInformationCategory` or `LleInformationCategory` | Resolve the exact context and rebuild only that included EFF row | Input or lookup fix |
| DAT_LINE_LIMIT | A DAT artifact is generated or supplied | Blocking |  | Any emitted line, including a `METADATA` line, exceeds 4000 characters | Remove only columns blank in every data row, regenerate, and revalidate before preview | Source rebuild |
| COPY_SOURCE | Create is based on an existing Location | Blocking |  | ShipToLocationId, ShipToLocationCode, or a site flag is copied without explicit user input | Use the source only as value evidence and omit unrequested fields | Input fix |
| MODIFIED_SECTIONS | Create, edit, or delete | Blocking |  | The mutation includes child or EFF rows the user did not modify, uses an unkeyed additional-address row, or uses LocationOtherAddress for MAIN | Keep the base Location row and only explicitly modified EFF rows or keyed non-MAIN additional-address rows | Input fix |

| NAMING_ADDRESS_LIFECYCLE | Create, edit, or inactivate | Warning |  | Name or code is not meaningful, address data is incomplete, or active dependencies remain before end-dating | Use meaningful identifiers, complete the address, and resolve dependencies | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_locations | Read, edit, delete, or create uniqueness check | Exact identity, duplicate-check result, effective range, and current values | ora_reference_lookups.md |
| resolve_location_reference_set | Create or edit | One exact SetCode or SetId | ora_reference_lookups.md |
| resolve_location_address_contract | Create, MAIN-address edit, or complete address read | Country layout and loader mapping for mutation; current MAIN address for read | ora_reference_lookups.md |
| resolve_location_action_reason | Date-effective edit includes `ActionReasonCode` | Exact user-supplied operation reason and effective date | ora_reference_lookups.md |
| resolve_location_delete_history | Date-effective delete | Fresh LocationId, selected EffectiveStartDate, and complete history | ora_reference_lookups.md |
| read_location_eff_context | A LocationExtraInfo or LocationLegislative row is included | Exact category, context, unique keys, and supplied segments | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LOC.DESIGN | decision | 7 | design_enforcement | passed->LOC.ROUTE;not_required->LOC.ROUTE;blocked->LOC.ERROR | LOC.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
