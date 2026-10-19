# Time Device Event Mapping Set Reference Lookups

## Source Basis

- Time Profiles Technical Design Document for FSCR, Confluence page 21722044713, read 2026-09-22.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| search_time_device_mapping_sets_by_criteria | A user searches, an existing Mapping Set is updated, or a new Mapping Set is checked for a possible duplicate | Every user-provided business attribute. For create, Name followed by every supplied non-Name parent or supported child attribute when neither Name check finds a match. | GET {FA_HOST}/hcmRestApi/resources/11.13.18.05/timeDeviceMappingSets/, following every response page until the collection is exhausted; retrieve record detail or follow supported child links when required to evaluate a supplied attribute | Every supplied parent attribute, MappingSetId, Name, Description, and supported child-resource attributes needed to evaluate supplied criteria | Name uses a case-insensitive contains match. Every other supplied attribute uses a normalized exact match. A candidate matches only when it satisfies every supplied criterion. For create, check exact Name first, then partial Name; only when neither finds a match evaluate every supplied non-Name attribute. | Sanitized matching Mapping Set business values; all matching candidates; selected complete record when applicable; duplicate-choice state for a matching create candidate | For search or update, show all matching candidates and request a selection when multiple match. If no candidate matches, state that no Mapping Set met every supplied criterion. For create, when any check finds a match, show it and wait for the user's choice to use it or create a new record. Treat incomplete pages, unavailable details, or an unresolved supported child link as blocked; never infer an identity. |
| resolve_existing_time_device_mapping_set | An update targets an existing Mapping Set or child relationship | Selected persisted MappingSetId | GET {FA_HOST}/hcmRestApi/resources/11.13.18.05/timeDeviceMappingSets/{MappingSetId}?expand=all | MappingSetId, Name, Description, Mappings.MappingSetDetailId, Mappings.MappingId | Require exactly one parent whose returned MappingSetId equals the selected persisted MappingSetId; use returned child rows only for existing child relationships | Persisted parent MappingSetId and existing child MappingSetDetailId paired with MappingId | Stop if the parent cannot be read exactly once or a requested existing child relationship is absent or ambiguous; never derive IDs from Name or MappingId |
| resolve_time_device_mappings | Mappings contains one or more MappingId values | Mappings[].MappingId | {FA_HOST}/hcmRestApi/resources/11.13.18.05/timeDeviceMappings?orderBy=Name | MappingId, Name | Each supplied MappingId must match one returned time device mapping | Validated Mappings[].MappingId | Stop and report the unknown or ambiguous MappingId values |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Criteria search and duplicate check | Retrieve every page before evaluation. For search and update, compare every candidate against every user-provided business attribute as conjunctive criteria: Name case-insensitively contains; all other attributes normalized exact. Retrieve detail or follow supported child links only when needed for a supplied attribute. |
| Search or update has multiple matches | Show all matching Mapping Sets and request one selection before an update is prepared. |
| Create duplicate decision | Check exact Name, then partial Name, then every supplied non-Name attribute only when neither Name check matches. If any check finds a match, show it and wait for the user's choice to use it or create a new Mapping Set. |
| Existing Mapping Set update | Read the selected parent with expand=all before preparing an update. Preserve the returned MappingSetId; use MappingSetDetailId only for a verified existing child relationship. |
| A MappingId is supplied | Read the time device mappings LOV source and validate that every supplied MappingId resolves exactly once |
| A MappingId does not resolve exactly once | Do not prepare a create request; ask the user to select valid Event Mappings |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TDEMSET_SEARCH_MAPPING_SETS | step | 2 | reference_lookup | selected->TDEMSET_RESOLVE_EXISTING_PARENT;no_equivalent->TDEMSET_RESOLVE_EXISTING_PARENT;multiple_matches->TDEMSET_SEARCH_MULTIPLE_MATCHES;no_matches->TDEMSET_SEARCH_NO_MATCHES;awaiting_create_choice->TDEMSET_AWAIT_DUPLICATE_CHOICE;blocked->TDEMSET_SEARCH_BLOCKED | TDEMSET_VALIDATE_INPUT | stop | A criteria search, update, or create duplicate check is prepared |
| TDEMSET_RESOLVE_EXISTING_PARENT | step | 3 | reference_lookup | resolved->TDEMSET_VALIDATE_PARENT_CHILD_IDS;not_applicable->TDEMSET_VALIDATE_PARENT_CHILD_IDS;not_resolved->TDEMSET_PARENT_BLOCKED | TDEMSET_SEARCH_MAPPING_SETS | stop | An update targets an existing Mapping Set; not applicable to create |
| TDEMSET_RESOLVE_MAPPING_IDS | step | 5 | reference_lookup | resolved->TDEMSET_APPLY_DEFAULTS;not_resolved->TDEMSET_MAPPING_BLOCKED | TDEMSET_VALIDATE_PARENT_CHILD_IDS | stop | Parent-child ID validation passed |
