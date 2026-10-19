# Manage Legislative Data Groups Design Enforcement

## Purpose

Defines the mandatory Legislative Data Group identity and country-localization
design gates evaluated before preview or routing. It does not perform lookups,
apply defaults, or infer legislation.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Require zero exact Name matches for create or one exact target for other operations |
| 2 | Confirm context | Retain the current target values needed by the requested operation; for delete, retain only the fresh LegislativeDataGroupId locator |
| 3 | Resolve country localization | Resolve country-derived LegislationCode and DefaultCurrencyCode; use TerritoryShortName only when available |
| 4 | Confirm related setup | Require one exact related value when the request needs it |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| IDENTITY | Every request | Blocking | find_manage_legislative_data_groups | Create Name already exists, or another operation is absent, unresolved, or ambiguous | Supply one exact business identifier | Input fix |
| CONTEXT | Current target context is required | Blocking | find_manage_legislative_data_groups | Required current values are absent or unresolved | Re-read one exact Legislative Data Group | Lookup fix |
| COUNTRY_CURRENCY | Create, or edit when Country or Currency changes | Blocking | resolve_country_localization | Country is unresolved, or Currency differs from its default | Supply one exact Country and its default Currency | Lookup fix |
| LOADER_CODES | Create | Blocking | resolve_country_localization | LegislationCode or DefaultCurrencyCode is blank | Resolve the required loader codes before preview; TerritoryShortName is optional | Lookup fix |
| TERRITORY_NAME | Create | Blocking |  | TerritoryShortName is invented or treated as mandatory when the resolver does not return it | Omit TerritoryShortName when it is unavailable | Input fix |
| RELATED | A related business value is supplied or required | Blocking |  | The related value is absent or ambiguous | Supply one exact related value | Input fix |
| ZAP_DELETE | Delete | Blocking | find_manage_legislative_data_groups | The target lacks one fresh LegislativeDataGroupId, the final artifact has any row other than one root DELETE row, contains MERGE, dates, split directives, country, currency, child, EFF, or source-system-key values | Re-read the exact target and rebuild the root-only DELETE row using its returned locator | Lookup or payload fix |


| LDG_CONFIGURATION | Create or edit | Warning |  | Country, legislation, currency, or cost allocation structure is not confirmed | Confirm the required country configuration before payroll setup | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_legislative_data_groups | Target, current-context, create-uniqueness, or zap-delete evaluation | Exact Name result, current Legislative Data Group values, and a fresh LegislativeDataGroupId for delete | ora_reference_lookups.md |
| resolve_country_localization | Create, or edit when Country or Currency changes | One country code, default currency, and optional TerritoryShortName | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LDG.DESIGN | decision | 6 | design_enforcement | passed->LDG.ROUTE;not_required->LDG.ROUTE;blocked->LDG.ERROR | LDG.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
