# Remit-to Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Reference set and access | Establish chosen existing scope, not a default from another environment |
| 2 | Postal destination | Validate explicit destination and known matching hazards locally; leave application-owned postal checks pending import |
| 3 | Receipt-from coverage | Establish criteria domain and exact parent association |
| 4 | Optional flexfields | Establish deployed context only when requested/applicable |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| remit_set | Existing authorized reference data set | Yes | All locations/criteria | Verify | Exact-task FSM export positive scope evidence; import authorization remains a separate runtime check | resolve_remit_set | Import resolves SetCode, not a new set | Which reference data set should own this address? | AR_REMIT_TO_LOCATION.SetCode; AR_REMIT_TO_ADDRESS.SetCode |
| remit_postal | Shared postal location and country validation | Yes | Location create or reuse | Verify | Exact FSM references and local import-match inspection; target country/style validation and shared-location resolution belong to normal FSM import | validate_postal_destination | Do not require global HZ enumeration; no uniqueness claim; require process success and exact fresh-export reconciliation | Provide intended country/address and any business-owned distinguishing reference; see ../references/postal-validation-contract.md | AR_REMIT_TO_LOCATION.TerritoryCode; Address1; Address2; Address3; Address4; City; State; County; Province; PostalCode; AddrElementAttribute2; AddrElementAttribute3; OrigSystemReference |
| criteria_country | Receipt-from country | Yes | Criteria create | Verify | Observed Country values in validated task export plus source domain; not a complete runtime choice list | resolve_criteria_country | Chooses customer bill-to coverage | Which customer country or default coverage is intended? | AR_REMIT_TO_ADDRESS.Country |
| criteria_state | Receipt-from state | Conditional | State restriction requested | Verify | Observed Country and State pairs in validated task export; preserve intentional blank restrictions | resolve_criteria_state | Avoid mismatched state or broadening coverage | Which state within that country should use this address? | AR_REMIT_TO_ADDRESS.State |
| criteria_status | Criteria lifecycle domain | Yes | Criteria create or exact-key Status update | Verify | Reviewed UI create default, CODE_STATUS seed data and migration criteria VO/EO; ../references/lifecycle-contract.md | resolve_criteria_status | New criteria use A; exact existing criteria support immediate A/I updates with other values preserved. Physical deletion and scheduled end-dating remain unsupported by this adapter | For a missing or ambiguous intent, ask whether to activate or inactivate existing coverage immediately; do not ask for new product evidence when an exact authorized A/I update is already specified | AR_REMIT_TO_ADDRESS.Status |
| remit_flex | Deployed regional/DFF context | Conditional | Context or segment applies | Verify | Explicit conditional deployment evidence request; task export alone is insufficient | resolve_remit_flexfields | Labels and requiredness vary by deployment | What regional information does the business require? | AR_REMIT_TO_LOCATION.GlobalAttributeCategory; AR_REMIT_TO_ADDRESS.AttributeCategory |

Sources: SRC-REMIT-AM-IMPL; SRC-REMIT-LOCATION-VO; SRC-REMIT-CRITERIA-VO; SRC-REMIT-CODE-STATUS; SRC-REMIT-MIGRATION-UPDATE-TEST; SRC-REMIT-HELP-26C. Reference access and geography evidence remain distinct from transport/schema validation.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMT_DEPENDENCIES | decision | 30 | resolve_dependency | satisfied->RMT_DEFAULTS;issues->RETURN_ISSUES | RMT_LOOKUPS | stop | Applicable prerequisites |
