# Sales Note Type Reference Lookups

Use the documented Sales Note Types resource only to verify the note types mapped into a source-object context. It is read-only and does not prove that an unmapped ZMM_NOTE_TYPE lookup row is absent.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/faaps/api-list-values-note-types.html | Read-only Note Types REST endpoint inventory |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-notetypes-get.html | Finder, queryable attributes, response fields, lengths, and read-only behavior |
| https://docs.oracle.com/en/cloud/saas/sales/oacts/define-notes.html | Business-object mapping and default-note fallback semantics |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_mapped_note_type_for_object | Operation is ValidateRuntimeAvailability and SourceObjectCode and NoteTypeCode are present | SourceObjectCode, NoteTypeCode | /crmRestApi/resources/11.13.18.05/noteTypes?finder=NoteTypeFinder;BindSourceObjectCode={SourceObjectCode}&fields=MappedLookupCode,Meaning,SourceObjectCode&onlyData=true | MappedLookupCode, Meaning, SourceObjectCode | Match exactly one row whose MappedLookupCode equals NoteTypeCode and whose SourceObjectCode equals the requested source object | RuntimeMappedLookupCode: MappedLookupCode, RuntimeMeaning: Meaning, RuntimeSourceObjectCode: SourceObjectCode | No match means the type is not exposed for that object in this result; do not infer that the base lookup row is absent. More than one exact match is ambiguous and blocks the conclusion. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Exact object-context match | Return the mapped code, meaning, and source object as read-only runtime evidence. |
| No object-context match | Report that object-specific availability was not verified. Review Manage Sales Note Type Mapping or the Default Note Types fallback before changing the base lookup. |
| More than one exact match | Stop and disclose the ambiguous rows without selecting one. |
| REST request failure | Stop and disclose the safe endpoint identity and response status when available; do not retry automatically. |
| Operation does not request runtime validation | Mark the lookup not requested and continue without a REST call. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_NOTE.RUNTIME_LOOKUP | decision | 3 | reference_lookup | matched->SALES_NOTE.DEFAULTS;not_found->SALES_NOTE.DEFAULTS;not_requested->SALES_NOTE.DEFAULTS;ambiguous->SALES_NOTE.FAILED;failure->SALES_NOTE.FAILED | SALES_NOTE.DEPENDENCIES | stop | Always |
