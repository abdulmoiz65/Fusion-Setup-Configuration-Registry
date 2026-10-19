# Manage Legislative Data Groups Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Legislative Data Groups.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, or delete | Block | Provide one supported operation | Every request |  |
| Existing LDG selector | Exact LegislativeDataGroupId or Name; an explicit contains or prefix pattern is allowed only for collection get | Block | Provide an exact selector or explicit read pattern | get, edit, or delete | find_manage_legislative_data_groups |
| Delete locator | Freshly resolved LegislativeDataGroupId from one exact Name match | Block | Resolve the exact target and retain its returned identifier internally | delete | find_manage_legislative_data_groups |
| Create identity | Name | Block | Provide the Legislative Data Group name | create |  |
| Create legislation and currency | Exact Country, or LegislationCode and DefaultCurrencyCode | Block | Resolve Country to both required codes | create | resolve_country_localization |
| Edit changes | At least one explicit supported change | Block | Provide the intended change | edit |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An exact existing target does not resolve once | Missing | Request one exact ID or Name | find_manage_legislative_data_groups |
| A create Name matches an existing Legislative Data Group | Invalid | Stop the duplicate create | find_manage_legislative_data_groups |
| Country, legislation, or currency does not resolve to one consistent localization tuple | Invalid | Correct the country or currency | resolve_country_localization |
| A supplied cost allocation structure does not resolve exactly | Invalid | Correct StructureInstanceName |  |
| A delete target does not resolve to one current LegislativeDataGroupId | Invalid | Re-read one exact Name and use its returned delete locator | find_manage_legislative_data_groups |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Loader Boolean value | For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as Y and false or No as N; preserve Y or N; do not add an omitted attribute or change REST read values | A Data Loader mutation includes the attribute |  |
| Name length | Reject a Name longer than 240 characters | Name is supplied |  |
| Code lengths | Reject LegislationCode longer than 30 characters or DefaultCurrencyCode longer than 20 characters | A code is supplied |  |
| Required codes | Reject a create with blank LegislationCode or DefaultCurrencyCode after localization resolution; TerritoryShortName remains optional | create | resolve_country_localization |
| Currency-country consistency | Require the resolved default currency for the selected country; reject a blank or conflicting currency | create, or edit changes country or currency | resolve_country_localization |
| Cost allocation identity | Accept only one exact StructureInstanceName when a cost allocation key flexfield is associated | StructureInstanceName is supplied |  |
| Read cardinality | Return all matches for an explicit collection pattern; never select one by position | A contains or prefix get is requested | find_manage_legislative_data_groups |
| Supported fields | Reject response-only IDs, audit fields, links, and fields absent from the registered Legislative Data Group loader contract | A mutation value is supplied |  |
| Zap delete | Treat delete as a complete non-date-effective purge. Require one root LegislativeDataGroupId locator and a serialized DELETE directive; reject dates, split directives, child rows, EFF rows, country, currency, and MERGE rows | delete | find_manage_legislative_data_groups |
| Source-system keys | Reject SourceSystemOwner and SourceSystemId. Never request, populate, modify, preserve, or use them for a delete | delete |  |
| Verification boundary | Do not treat source generation, transport, or load acceptance as business verification | Every mutation |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LDG.VALIDATE | decision | 1 | validate_input | valid->LDG.READ;missing->LDG.ERROR;invalid->LDG.ERROR;unsupported->LDG.ERROR | none | stop | Every Manage Legislative Data Groups request |
