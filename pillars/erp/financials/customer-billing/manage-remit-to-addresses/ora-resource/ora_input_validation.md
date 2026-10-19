# Remit-to Input Validation

<!-- fscr-supported-operations: create, update -->
<!-- fscr-update-fields: AR_REMIT_TO_ADDRESS::Status -->
<!-- fscr-create-fields: AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.Address1, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.City, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.OrigSystemReference, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.PostalCode, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.SetCode, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.State, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.TerritoryCode, AR_REMIT_TO_ADDRESS::Country, AR_REMIT_TO_ADDRESS::PostalCodeHigh, AR_REMIT_TO_ADDRESS::PostalCodeLow, AR_REMIT_TO_ADDRESS::SetCode, AR_REMIT_TO_ADDRESS::State, AR_REMIT_TO_ADDRESS::Status, AR_REMIT_TO_LOCATION::AddrElementAttribute2, AR_REMIT_TO_LOCATION::AddrElementAttribute3, AR_REMIT_TO_LOCATION::Address1, AR_REMIT_TO_LOCATION::Address2, AR_REMIT_TO_LOCATION::Address3, AR_REMIT_TO_LOCATION::Address4, AR_REMIT_TO_LOCATION::City, AR_REMIT_TO_LOCATION::County, AR_REMIT_TO_LOCATION::OrigSystemReference, AR_REMIT_TO_LOCATION::PostalCode, AR_REMIT_TO_LOCATION::Province, AR_REMIT_TO_LOCATION::SetCode, AR_REMIT_TO_LOCATION::State, AR_REMIT_TO_LOCATION::TerritoryCode -->

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Owning reference set | AR_REMIT_TO_LOCATION.SetCode; matching child SetCode | Ask which reference data set owns the address | Resolve exact existing authorized set; do not choose COMMON | Every location and criterion | resolve_remit_set |
| Postal destination | TerritoryCode and country-appropriate address values, distinct from criteria Country | Ask for destination country/address information | Validate explicit country/address locally; disclose target validation pending normal FSM import per ../references/postal-validation-contract.md | Location creation | validate_postal_destination |
| Customer coverage | AR_REMIT_TO_ADDRESS.Country with intended optional State and PostalCodeLow/PostalCodeHigh | Ask which customers should use the address | Do not copy postal destination country into receipt-from Country | Criteria creation | resolve_criteria_country |
| Parent identity | Exact selected parent and its seven template-derived CSV references | Ask which remit-to location the criteria belong to | Match SetCode, TerritoryCode, Address1, OrigSystemReference, PostalCode, State and City exactly, preserving blank components; derive child references and include the parent dependency row if not created in this design | Child creation | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Scope and transport | Require exact AR_MANAGE_REMIT_TO_ADDRESSES task, successful source packages, matching release and schema, exact headers and row widths including trailing blanks; reject unrelated populated data | Every source package | |
| Empty address | Import deriveLocationId rejects when all six matching inputs are absent; ask for the business address instead of relying on service failure | Location create | validate_postal_destination |
| Scalar types | Validate exact metadata types without stringifying structured values; preserve postal leading zeros and nonnumeric country formats | All supplied fields and keys | |
| Country and state | Validate criteria country and country-bound state; DEFAULT is special receipt-from coverage, not a postal destination country | Criteria values | resolve_criteria_state |
| Status | Required one-character criteria Status; create uses A, exact-key update accepts A or I only. Blank, D, dates and other values require clarified intent and produce no candidate | Criteria create or update | resolve_criteria_status |
| Field contracts | Allow only the declared create fields after all applicable dependencies; excluded fields retain unresolved or unsupported disposition, never infer support from CSV presence | Create | |
| Audit and internal identifiers | LastUpdateDate, LastUpdatedBy, CreationDate, CreatedBy and LastUpdateLogin are service-owned; never customer inputs or copied candidate changes. LocationId=-1 is a UI placeholder, never a business key | All operations | |
| Duplicate and intent | Exact create collision asks whether update was intended; ambiguous target asks for distinguishing facts; zero-match update does not silently create | Identity resolution | |
| Standalone business identity | Resolve scope only from the current request or its explicitly attached business input. Relative references such as `same`, `above`, `those`, `it`, or `the existing address` do not inherit a set, destination, or criterion from preceding conversation or campaign order. Ask for the exact set plus distinguishing destination/coverage attributes and generate no candidate until one exported identity is proven | Every create/update intake | |
| Cross-destination coverage uniqueness | Check SetCode plus Country, State, PostalCodeLow and PostalCodeHigh across all exported criteria and proposed child creates. Parent and Status do not distinguish this key; Inactive rows still collide. Ask which different coverage is intended or whether the existing coverage should change; do not choose another ZIP or silently reassign | Criteria creation, including bulk/mixed requests; SRC-REMIT-CRITERIA-U1 in ../references/coverage-uniqueness.md | |
| No-op and preservation | Compare requested values with exact current identity; equivalent update produces no candidate. Omitted values and unrelated rows are preserved; explicit blank is not automatic deletion | Update intake | |
| Update contract | Permit only Status on one exact exported AR_REMIT_TO_ADDRESS key. Preserve child SetCode and all parent references; include the unchanged parent dependency once. Other fields require an evidence-backed contract, not a create fallback | Update | |
| Unresolved operations | Retain intended postal/description changes, criteria identity changes, explicit clearing or retirement and ask the missing business question. Explain that CSV import cannot delete and this task has no end-date field; immediate inactivation is a separate user choice | Clear, delete, end-date or other update | |
| Bulk and mixed requests | Validate every row and parent-child relationship before packaging; duplicate/conflicting/invalid/unresolved rows hold the complete request, with row-specific questions and no partial ZIP | Multiple requests | |

Sources: SRC-REMIT-AM-IMPL (RemitToServiceAMImpl.deriveLocationId/deriveSetId), SRC-REMIT-LOCATION-VO, SRC-REMIT-CRITERIA-VO, SRC-REMIT-CRITERIA-EO, SRC-REMIT-UI-STATUS, SRC-REMIT-FSM-BO. Import matching and source update-enabled flags are not equivalent.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMT_VALIDATE | decision | 10 | validate_input | valid->RMT_LOOKUPS;issues->RETURN_ISSUES | none | stop | Every request |
