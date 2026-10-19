# Remit-to Design Enforcement

<!-- fscr-supported-operations: create, update -->
<!-- fscr-update-fields: AR_REMIT_TO_ADDRESS::Status -->
<!-- fscr-create-fields: AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.Address1, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.City, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.OrigSystemReference, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.PostalCode, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.SetCode, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.State, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.TerritoryCode, AR_REMIT_TO_ADDRESS::Country, AR_REMIT_TO_ADDRESS::PostalCodeHigh, AR_REMIT_TO_ADDRESS::PostalCodeLow, AR_REMIT_TO_ADDRESS::SetCode, AR_REMIT_TO_ADDRESS::State, AR_REMIT_TO_ADDRESS::Status, AR_REMIT_TO_LOCATION::AddrElementAttribute2, AR_REMIT_TO_LOCATION::AddrElementAttribute3, AR_REMIT_TO_LOCATION::Address1, AR_REMIT_TO_LOCATION::Address2, AR_REMIT_TO_LOCATION::Address3, AR_REMIT_TO_LOCATION::Address4, AR_REMIT_TO_LOCATION::City, AR_REMIT_TO_LOCATION::County, AR_REMIT_TO_LOCATION::OrigSystemReference, AR_REMIT_TO_LOCATION::PostalCode, AR_REMIT_TO_LOCATION::Province, AR_REMIT_TO_LOCATION::SetCode, AR_REMIT_TO_LOCATION::State, AR_REMIT_TO_LOCATION::TerritoryCode -->

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve design | Complete input, reference, dependency and default rules |
| 2 | Enforce semantics | Exact identity, supported field contract and complete requested coverage |
| 3 | Preview | Show all normalized rows, applied defaults, preserved values and outstanding issues |
| 4 | Package and handoff | Only ready adapter and registry may prepare a candidate for Data Loader |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any scope | Error | resolve_remit_set | Set missing, ambiguous or unverified | Ask for precise business scope; do not create reference set | Only user-selected correction |
| Parent create/reuse | Error | validate_postal_destination | Missing/invalid input, known collision, ambiguity or reuse-value conflict | Run local postal preflight and bind pending application validation in preview; see ../references/postal-validation-contract.md | No invented key, prevalidated-country claim or global-uniqueness assertion |
| Criteria create | Error | resolve_criteria_country | Country missing or default coverage confused with destination | Show customer coverage separately from destination | Only clarified business scope |
| Cross-destination duplicate | Error | | Same exact set/country/state/postal bounds already exist under any parent or repeat within the batch, regardless of Status | Ask for intended distinct coverage or the existing rule; preserve the whole unresolved request. See ../references/coverage-uniqueness.md | No automatic postal change, reassignment or inactivate-and-recreate workaround |
| State restriction | Error | resolve_criteria_state | State not proven within chosen country | Resolve exact intended restriction | Never silently broaden |
| Criteria lifecycle | Error | resolve_criteria_status | Create requests a state other than A, or update requests anything except Status A/I on an exact existing key | Resolve immediate activation/inactivation separately from physical deletion or future end-date | No guessed code or silent change of intent |
| Flexfield request | Error | resolve_remit_flexfields | Context, segment meaning, requiredness or value set unresolved | Resolve deployment and retain exact field mapping | No arbitrary AttributeN mapping |
| Postal update or description | Error | | LocationPEO is read-only and deriveLocationId may reuse/create rather than edit; descriptions are not copied by create hook | Retain request and disclose unresolved task-CSV persistence; UI editing and seed updateEnabled do not prove it | No silent create fallback |
| Criteria identity change | Error | | AltCriteria includes parent, Country, State and postal bounds; old criteria removal/retirement unresolved | Establish exact old/new identity and lifecycle first | No undocumented delete |
| Candidate integrity | Error | | Invalid rows, populated audit columns, unrelated populated data, changed metadata or partial unresolved batch | Reject before handoff; preserve exact current metadata and template headers | Regenerate only after correction |
| No-op update | Error | | Requested status already equals the current export | Record requirement as already satisfied; no import. For mixed input, disclose exclusion and reconfirm the complete remaining design | Never silently drop a requirement |
| Reverse update | Error | | Fresh current status differs from the submitted forward value | Reconcile concurrent changes before preparing cleanup; preserve every other current field | Never overwrite a later change |
| Preservation and result | Error | | Requested row duplicated, baseline row unexpectedly removed/changed, or requirement not persisted | Compare exact submitted candidate with fresh export, preserving unrelated concurrent additions | No success inferred from upload |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_remit_set | All scope | Verified exact set and access | ora_reference_lookups.md |
| validate_postal_destination | Location create/reuse | Local input/match checks and explicit pending application-validation contract | ora_reference_lookups.md |
| resolve_criteria_country | Criteria create | Exact coverage country/special choice | ora_reference_lookups.md |
| resolve_criteria_state | State restriction | Country-bound state | ora_reference_lookups.md |
| resolve_criteria_status | Criteria state | Source-backed operation-specific state | ora_reference_lookups.md |
| resolve_remit_flexfields | Applicable flexfields | Deployed context/segment/value contracts | ora_reference_lookups.md |

Sources: SRC-REMIT-AM-IMPL; SRC-REMIT-LOCATION-VO; SRC-REMIT-CRITERIA-VO; SRC-REMIT-FSM-BO; SRC-REMIT-CODE-STATUS; SRC-REMIT-MIGRATION-UPDATE-TEST; SRC-FSM-CSV-NO-DELETE-26C. See ../references/lifecycle-contract.md. Offline validation is not live verification; unsupported CSV deletion is a route limitation, not a blanket product prohibition.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMT_DESIGN | decision | 50 | design_enforcement | valid->RMT_HANDOFF;issues->RETURN_ISSUES | RMT_DEFAULTS | stop | Complete normalized request |
