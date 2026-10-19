# Manage Person Name Styles Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_person_name_styles | Read is requested, or an exact target is needed before create or edit | Resolved legislation code, or exact person name style | /hcmRestApi/resources/latest/managePersonNameStyles?expand=nameSetups&limit=499&onlyData=true&orderBy=NameStyle | LegislationCode, NameStyle, NameStyleId, required-name flags, and expanded nameSetups | For a country request, match the exact returned LegislationCode; do not filter by country name. For an exact style, match NameStyle. | NameStyleId, current name-style values, and nameSetups | For create, zero exact matches confirms availability. For edit, stop on zero or multiple exact matches. |
| resolve_name_style_component | A Name Component is supplied | Exact component code or meaning | [Global Human Resources Common > Manage Common Lookups](../../../global-human-resources-common/manage-common-lookups/SKILL.md), lookup type PER_NAME_STYLE_ATTRIBUTES | Enabled lookup code, meaning, and effective range | Require one enabled compatible code; never use a display label as the load value | Stored component code | Stop and request a more precise component |
| resolve_country_context | Country or legislation is supplied | Exact country name or territory code | /hcmRestApi/resources/{version}/hcmCountriesLov | CountryName and TerritoryCode | Follow bounded pages and require one exact name or code match | CountryName and TerritoryCode to LegislationCode and parent GroupingKey | Stop on zero or multiple exact matches |
| validate_parent_before_child | Create or edit source is prepared | Current exported FSM package and scoped parent and child CSV rows | Reviewed exported FSM archive | ASM_SETUP_CSV_METADATA.xml marker, exported CSV names, parent row, child rows, grouping keys, row order, and generated IDs | Require the exact-case marker and exported CSV names. Require the parent first, parent GroupingKey equal to LegislationCode, and each child GroupingKey equal to LegislationCode,ColumnName. Generated IDs remain blank on create. | Immutable FSM ZIP for core.data-loader and submitTaskCSVImport | Stop on a missing marker, renamed CSV, missing parent, malformed key, child-before-parent order, or unrelated row. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |
| Person Name Style components are presented | **Mandatory completion gate:** show every available component column from the read, export, or validation source in source order. `ColumnName` is mandatory in the presentation; do not omit any returned field or replace fields with a display-only summary. When an FSM export augments the live REST response, show the combined available columns and identify the source of every non-REST field. Do not mark the result complete until the full union is presented. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PNS.READ | decision | 3 | reference_lookup | resolved->PNS.DEFAULTS;not_found->PNS.ERROR;ambiguous->PNS.ERROR;failed->PNS.ERROR | PNS.DEPENDENCY | stop | Read is requested, or exact target and reference resolution is required before create or edit |
