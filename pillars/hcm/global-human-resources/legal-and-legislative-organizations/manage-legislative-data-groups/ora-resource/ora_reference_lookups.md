# Manage Legislative Data Groups Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_legislative_data_groups | Read is requested, Create checks name uniqueness, or an exact target is needed before edit or delete | Exact Legislative Data Group Name or an explicit read-only contains/prefix pattern | GET legislativeDataGroups with REST-Framework-Version 9 | LegislativeDataGroupId, Name, TerritoryShortName, CurrencyName, and CostAllocationStructureName | Use exact Name equality for a single target. For an explicit contains or prefix request, use q=Name like '%term%'. Create requires zero exact Name matches. Edit and delete require exactly one exact Name. Pattern read returns its collection. | Create uniqueness result; exact-read record; or pattern-read collection with Name, country, currency, cost-allocation structure, and LegislativeDataGroupId for an internal delete locator | Create: one or more exact matches block. Exact read, edit, and delete: zero or multiple matches block. Pattern read: zero returns an empty collection and multiple matches are valid. |
| resolve_country_localization | Create, or edit when Country or Currency changes | Exact country name or territory code | /hcmRestApi/resources/{version}/hcmCountriesLov using exact CountryName or TerritoryCode, then /fscmRestApi/resources/{version}/currenciesLOV using the returned CurrencyCode | CountryName, TerritoryCode, CurrencyCode, ObsoleteFlag; CurrencyCode, Name, EnabledFlag, StartDateActive, and EndDateActive | Require one exact nonobsolete country and one exact enabled effective currency matching its CurrencyCode | LegislationCode=TerritoryCode, DefaultCurrencyCode=CurrencyCode, optional Territory=CountryName, and optional DefaultCurrency=currency Name | Stop on zero, multiple, obsolete, disabled, ineffective, or inconsistent results; do not use an existing Legislative Data Group as authority |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A Fusion lookup runs | Use core.fusion-api.rest-api-client with core.auth.fusion-oauth-authentication. |
| A read or mutation precheck runs | Execute applicable reference_lookup nodes through core.fusion-api.rest-api-client before source preparation; do not use core.data-loader, core.data-loader.task-rest, or ora_rest_execution.md for the read. |
| An exact target or country is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A delete target is resolved | Retain only the returned LegislativeDataGroupId as the internal root delete locator. Do not read or use SourceSystemOwner or SourceSystemId. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LDG.READ | decision | 2 | reference_lookup | resolved->LDG.COUNTRY;uniqueness_available->LDG.COUNTRY;not_found->LDG.ERROR;ambiguous->LDG.ERROR;failed->LDG.ERROR | LDG.VALIDATE | stop | Read is requested, Create checks name uniqueness, or an exact target is required before edit or delete |
| LDG.COUNTRY | decision | 3 | reference_lookup | resolved->LDG.DEPENDENCIES;not_required->LDG.DEPENDENCIES;not_found->LDG.ERROR;ambiguous->LDG.ERROR;failed->LDG.ERROR | LDG.READ | stop | Create, or edit when Country or Currency changes |
