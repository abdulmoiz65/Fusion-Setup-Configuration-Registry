# Time Device Export Data Reference Lookups

## Source Basis

- Time Profiles Technical Design Document for FSCR, Confluence page 21722044713, read 2026-09-23.
- Developer-provided Time Device Export Data search requirements, 2026-09-23.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| search_time_device_export_data_by_criteria | A user searches, an existing Time Device Export Data definition is updated, or a new definition is checked for a possible duplicate | Every user-provided business attribute. For create, Name followed by every supplied non-Name parent or supported child attribute when neither Name check finds a match. | GET {FA_HOST}/hcmRestApi/resources/11.13.18.05/timeDeviceExportDataDefinitions, following every response page until the collection is exhausted; retrieve item detail through GET {FA_HOST}/hcmRestApi/resources/11.13.18.05/timeDeviceExportDataDefinitions/{TcdExpDataDefId} or follow a supported child link only when required to evaluate a supplied attribute | Every supplied parent attribute, TcdExpDataDefId, Name, Description, and supported child-resource attributes needed to evaluate supplied criteria | Name uses a case-insensitive contains match. Every other supplied attribute uses a normalized exact match. A candidate matches only when it satisfies every supplied criterion. For create, check exact Name first, then partial Name; only when neither finds a match evaluate every supplied non-Name attribute. | Sanitized matching Time Device Export Data business values; all matching candidates; selected complete record when applicable; duplicate-choice state for a matching create candidate | For search or update, show all matching candidates and request a selection when multiple match. If no candidate matches, state that no Time Device Export Data definition met every supplied criterion. For create, when any check finds a match, show it and wait for the user's choice to use it or create a new definition. Treat incomplete pages, unavailable details, or an unresolved supported child link as blocked; never infer an identity. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Criteria search and duplicate check | Retrieve every page before evaluation. For search and update, compare every candidate against every user-provided business attribute as conjunctive criteria: Name case-insensitively contains; all other attributes normalized exact. Retrieve detail or follow a supported child link only when needed for a supplied attribute. |
| Search or update has multiple matches | Show all matching Time Device Export Data definitions and request one selection before an update is prepared. |
| Create duplicate decision | Check exact Name, then partial Name, then every supplied non-Name attribute only when neither Name check matches. If any check finds a match, show it and wait for the user's choice to use it or create a new definition. |
| Search needs no item detail | Evaluate the candidate from the paginated collection result. |
| Search needs item detail or a supported child attribute | Retrieve the item detail or follow the supported child link before evaluating the criterion. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TDEDEXPORT_SEARCH_EXPORT_DATA | step | 2 | reference_lookup | selected->TDEDEXPORT_APPLY_DEFAULTS;ready_for_create->TDEDEXPORT_APPLY_DEFAULTS;multiple_matches->TDEDEXPORT_SEARCH_MULTIPLE_MATCHES;no_matches->TDEDEXPORT_SEARCH_NO_MATCHES;awaiting_create_choice->TDEDEXPORT_AWAIT_DUPLICATE_CHOICE;blocked->TDEDEXPORT_SEARCH_BLOCKED | TDEDEXPORT_VALIDATE_INPUT | stop | A criteria search, update, or create duplicate check is prepared |
