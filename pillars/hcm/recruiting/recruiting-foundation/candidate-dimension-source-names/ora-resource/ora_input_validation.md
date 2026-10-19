# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Exact task | Candidate Dimension Source Names under Recruiting Foundation | UNSUPPORTED | Resolve ORA_MANAGE_CANDIDATE_DIMENSION_SOURCE_NAMES internally | Every request | |
| Operation | Retrieve, maintain Name, add-row, translation guidance, or internal validate_import | MISSING | Identify the requested operation without converting Create to Update | Every request | |
| Rename | Current Name and replacement Name; Source URL and medium if needed to disambiguate | MISSING | Require one exact source-language match | Name maintenance | resolve_source_export |
| Add Row | Name, Source URL and verified language; optional Display Sequence | MISSING | Preserve the supplied Name and URL; do not invent a URL | Add Row | resolve_source_export |
| Validation artifacts | Completed baseline, final candidate, exact request, selected environment and fingerprints | BLOCKED | Supply the existing immutable artifacts; no export or submission inside Task Hook | Internal validate_import | resolve_source_export |
| Translation guidance | Exact source identity and language, verified UI action | BLOCKED | Inspect the separate Translation Editor contract | Translation guidance | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Name and URL | Require nonblank strings without outer whitespace or control characters, at most 2000 characters; preserve case and spelling | Add Row and replacement Name | |
| Display Sequence | If supplied require a nonnegative integer of at most 16 digits | Add Row | |
| Language | Require the explicitly selected session/request language to occur in the baseline; no first-translation fallback | Add Row or explicit-language retrieval | resolve_source_export |
| Unsupported maintenance | Existing Source URL, source medium, sequence, translations, remove and bulk writes are outside the verified import contract | Maintain | |

Retrieve reports only Display Sequence, Name and Source URL unless metadata is requested.
Name lookup and duplicate policy belong to design enforcement; language and base/TL
join mechanics belong to reference lookups.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDSN.VALIDATE_REQUEST | decision | 10 | validate_input | valid->CDSN.CHECK_DEPENDENCIES;invalid->CDSN.HANDLE_ISSUES | none | stop | Every supported request; internal validate_import is read-only |
