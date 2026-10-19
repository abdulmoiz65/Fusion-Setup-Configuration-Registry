# Manage Legal Entity Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Identity and resolver gate | Entity identity, country, primary country result, user-specified identifying jurisdiction, legal address, and optional PSU resolve; the jurisdiction's import Name is unambiguous |
| 2 | Aggregate completeness gate | Root, same-name main LRU, identifying entity registration, and identifying main-LRU registration are each present exactly once |
| 3 | Supported-scope gate | Authority values are null, both function files have zero candidate rows, and geography is the fixed country mapping |
| 4 | Package gate | Exact target hierarchy and any unchanged existing-parent rows are present; export supplies no CREATE business values except the address natural key; this graph validates final-package readiness, while the selected task SKILL.md local FSM workflow constructs the archive; resource rules do not construct, approve, upload, or import it |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every CREATE | Error | find_entity_conflict | Identifier exists, name conflict is unresolved, or lookup failed | Resolve the exact existing identity or select a new approved identity | Yes |
| Every CREATE | Error | resolve_entity_country_geography | Territory/primary country result is unresolved, ineffective, or inconsistent with the defaulting contract | Correct or explicitly refine the input and rebuild carriers from the resolved territory and country result | Yes |
| Every CREATE | Error | resolve_entity_identifying_jurisdiction | Jurisdiction input/selection is unresolved, ineligible, export-derived, or has an ambiguous exact import Name | Request missing/corrected input or an explicit eligible candidate choice; a choice cannot override eligibility or ambiguous name-based import | Yes |
| Every CREATE | Error | resolve_entity_legal_address | Address is absent, inactive, ambiguous, country-incompatible, or LocationId is supplied | Select one exact natural key and leave LocationId blank | Yes |
| Every CREATE | Error |  | Root or any of the three explicit children is missing, duplicated, mismatched, or partial | Author exactly the four-row UI-equivalent aggregate | Yes |
| Every supported CREATE | Error | resolve_entity_enabled_function_code | Authority/function input is present or either function file contains a candidate row | Remove unsupported inputs, preserve existing function rows unchanged, and retain header-only files when already header-only in the baseline | Yes |
| Package preview | Error | verify_entity_package_baseline | Exact current hierarchy, parent-row requirement, header, empty-child, or fingerprint evidence is missing | Refresh the target export and rerun the selected task SKILL.md local FSM package-preparation workflow | Yes |

## Resolved Scope Decisions

| ID | Status | Enforced Contract | Future Expansion Gate |
|---|---|---|---|
| LS-TBD-007 | Resolved for supported scope | Authority is optional but unsupported; PartyName, IssuingFormattedAddress, and hidden authority/site values remain null; supplied authority blocks | Exact active eligible XLE authority plus active identifying authority-site/address resolver compatible with jurisdiction |
| LS-TBD-008 | Resolved for supported scope | Both function CSVs contain zero candidate rows; supplied function blocks; enabled XLE_LE_FUNCTION lookup alone is insufficient | JurisdictionFunctionVO or XLE_JUR_FUNCTIONS permission resolver plus the LS-TBD-007 authority/site contract |
| LS-TBD-010 | Resolved for country-only scope | Use resolved territory and primary country values with the explicit defaulting contract; GeographyIdentifierId is receipt-only and no country GeographyId is required. GeographyElement1 remains a documented country-level derivation | UI-equivalent full natural-key hierarchy resolver for STATE, CITY, or other non-country geography |
| LS-TBD-013 | Resolved | Root-only import does not regenerate children; explicitly author root, same-name main LRU, identifying entity registration, and identifying main-LRU registration | None for the supported aggregate; function and authority expansion remains separately gated |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_entity_conflict | Every CREATE | Identifier availability, name-collision receipt, and existing natural key when applicable | ora_reference_lookups.md |
| resolve_entity_country_geography | Every CREATE | Resolved territory and primary country values, fixed main-LRU tuple, source-specific identifier evidence | ora_reference_lookups.md |
| resolve_entity_identifying_jurisdiction | Every CREATE | Selected exact jurisdiction Name, identifying semantics, LE/LRU registration type codes, exact-name uniqueness, and jurisdiction IDs retained only as evidence | ora_reference_lookups.md |
| resolve_entity_legal_address | Every CREATE | LegalAddress and both FormattedAddress natural keys | ora_reference_lookups.md |
| verify_entity_package_baseline | Every preview | Exact hierarchy and package evidence | ora_reference_lookups.md |
| resolve_entity_enabled_function_code | Function input is supplied for scope assessment | Enabled code/meaning receipt that does not authorize CREATE | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LE.ENFORCE_DESIGN | decision | 50 | design_enforcement | passed->LE.PACKAGE_PREVIEW_GATE;blocked->LE.HANDLE_ERROR | LE.APPLY_DEFAULTS | stop | Before final-package readiness validation |
