# Manage Locations Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Locations.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, or delete | Block | Provide one supported operation | Every request |  |
| ZAP or physical delete | Unsupported | Stop | Use an eligible date-effective delete of a non-first Location split, if that is the intended business effect | Every request |  |
| Existing location selector | Exact LocationCode or LocationName | Block | Provide one exact selector | get, edit, or delete | find_manage_locations |
| Create identity | LocationCode and LocationName | Block | Provide both values | create |  |
| Effective context | Explicit EffectiveStartDate in YYYY/MM/DD format | Block | Provide one valid date for the logical object | Create, edit, or delete |  |
| Reference-data set | Exact SetCode or SetId, or neither | Block only an invalid supplied set | Resolve a supplied set; continue to defaulting when omitted | Create or edit | resolve_location_reference_set |
| MAIN address | Country | Block | Provide Country; collect mandatory labelled values after address lookup | Create |  |
| Edit changes | At least one explicit supported change | Block | Provide the intended change | edit |  |
| Delete target | Exact Location and selected non-first EffectiveStartDate | Block | Resolve the target and complete history row | delete | resolve_location_delete_history |
| Date-effective delete history | Complete Location history, selected non-first row, and its immediately preceding row | Block | Derive the retained start and inclusive deletion end from history | delete | resolve_location_delete_history |

A request containing `ZAP`, `zap`, or an intent to physically delete the logical
Location is `UNSUPPORTED`, not a delete candidate. Stop before target lookup,
history resolution, source generation, Task Hook preview, approval, or any
`core.data-loader` call.

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An existing Location does not resolve exactly once | Missing | Provide one exact LocationCode or LocationName | find_manage_locations |
| A create LocationCode matches an existing Location | Invalid | Stop the duplicate create; an existing LocationName is permitted | find_manage_locations |
| A reference-data set does not resolve exactly once | Invalid | Correct the SetCode or SetId | resolve_location_reference_set |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Loader Boolean value | For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as Y and false or No as N; preserve Y or N; do not add an omitted attribute or change REST read values | A Data Loader mutation includes the attribute |  |
| Date format | Accept YYYY/MM/DD only for Data Loader date fields | A date is supplied |  |
| Logical-object effective date | For create or edit, apply the supplied EffectiveStartDate to the Location row and every included child row. For date-effective delete, treat the supplied date as the selected history start and author the root MERGE with the predecessor EffectiveStartDate and selected EffectiveEndDate derived from complete history. | Create, edit, or delete | resolve_location_delete_history |
| Date-effective update action reason | `ActionReasonCode` is optional. Never copy, preserve, or default the prior or create reason. When the user explicitly supplies an update reason, resolve that value independently for the new effective date; otherwise omit the field. | Edit with a changed effective date | resolve_location_action_reason |
| Location identity length | Require LocationCode at most 120 characters and LocationName at most 60 characters | Create or an identity change |  |
| MAIN address placement | Require MAIN address fields on the base `Location` row for create and MAIN-address edit; never represent MAIN with `LocationOtherAddress` | Create or MAIN-address edit | resolve_location_address_contract |
| Address field mapping | Require every included layout AttributeName to map exactly once through the declared crosswalk to a current loader field; reject an unknown or unavailable mapping | Create or MAIN-address edit | resolve_location_address_contract |
| Postal code | Preserve a supplied postal code as text | Address data is supplied |  |
| Time zone | For loader `TimezoneName`, resolve the source or selected MAIN-address `TimezoneCode` to exactly one enabled `timezonesLOV` item and write its `Name`. Reject `TimezoneCode`, `LongName`, `ShortName`, an address REST display string, or any inferred value. | TimezoneName is supplied | resolve_location_address_contract |
| Ship-to contract | If `ShipToSiteFlag` is `Y`, require `ShipToLocationId`, `ShipToLocationCode`, and `ShipToLocationSetCode` to be omitted. If it is `N`, require either one resolved `ShipToLocationId` or both resolved `ShipToLocationCode` and `ShipToLocationSetCode`; reject partial or conflicting alternatives. | ShipToSiteFlag or a ship-to reference is supplied | find_manage_locations |
| Phone mapping | Split the supplied main phone into MainphoneCountryCode, MainphoneAreaCode, MainphoneSubscriberNumber, and extension when supplied | Main phone is supplied |  |
| Live section coverage | Reconcile every supplied row and attribute against the current `Location`, `LocationOtherAddress`, `LocationExtraInfo`, or `LocationLegislative` live template section before loader handoff; reject an unknown section, absent attribute, duplicate target, response-only value, or unresolved value | A Data Loader mutation includes source data |  |
| Attribute contract | Resolve every supplied attribute's current data type, key role, reference/lookup contract, effective-date behavior, and EFF context where applicable; let `core.data-loader` enforce the operation-specific mandatory and source-key contract | A Data Loader mutation includes the attribute |  |
| Live value constraints | Validate every supplied value against the current live attribute metadata: data type, maximum length, precision/scale, allowed value/domain, and reference contract. Apply this to dynamically resolved EFF segments as well as base and child attributes; do not hardcode segment names or reuse constraints from a prior run | A Data Loader mutation includes the attribute |  |
| Edit surrogate keys | Require `LocationId` on the base edit row and the live `LocationExtraInfoId` or `LocationLegId` on each edited EFF object. Resolve `LocAddressUsageId` for address evidence, but reject a MAIN edit represented as a `LocationOtherAddress` row | Edit or delete | find_manage_locations |
| Extra-information context | Require `EFF_CATEGORY_CODE` `HCM_LOC`; set `FLEX:PER_LOCATION_INFORMATION_EFF` to the resolved `LeiInformationCategory` context name (not `Global Data Elements`, unless it is itself the resolved context); and require every supplied segment to be in that context's live section | A LocationExtraInfo row is supplied | read_location_eff_context |
| Legislative-information context | Require `EFF_CATEGORY_CODE` `HCM_LOC_LEG`; set `FLEX:PER_LOCATION_LEG_EFF` to the resolved `LleInformationCategory` context name (not `Global Data Elements`, unless it is itself the resolved context); and require every supplied segment to be in that context's live section | A LocationLegislative row is supplied | read_location_eff_context |
| Generated DAT shape | Remove a loader column only when it is blank in every authored data row. After XLSX conversion, require every emitted DAT line, including each `METADATA` line, to contain no more than 4000 characters. | A Data Loader mutation is prepared |  |
| Date-effective delete source | Use the full current Location workbook with exactly one `SET PURGE_FUTURE_CHANGES Y` directive and one root `Location` MERGE. Require the fresh root identity tuple `LocationId`, `SetCode`, and `LocationCode`, then use predecessor EffectiveStartDate and selected EffectiveEndDate only. Do not accept `LocationId` alone: the runtime Location translation entity requires `LocationCode`. Omit ActionReasonCode, address, LocationOtherAddress, ExtraInfo, Legislative, and all business-value deltas. Reject root DELETE/ZAP, first-split, unbounded, mixed MERGE/DELETE, an incomplete identity tuple, or non-history-derived ranges. | delete | resolve_location_delete_history |
| Mutation source scope | Keep the Location worksheet, map entry, and base row for every mutation; require the MAIN address on the base row for create; include LocationOtherAddress, LocationExtraInfo, and LocationLegislative only when explicitly modified for create or edit. A date-effective delete includes no child or EFF row. | Create, edit, or delete |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LOC.INPUT | decision | 1 | validate_input | valid->LOC.IDENTITY;missing->LOC.ERROR;invalid->LOC.ERROR;unsupported->LOC.ERROR | none | stop | Every Manage Locations request |
