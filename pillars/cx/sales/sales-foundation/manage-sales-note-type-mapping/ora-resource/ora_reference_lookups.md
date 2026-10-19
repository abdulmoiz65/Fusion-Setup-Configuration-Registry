# Sales Note Type Mapping Reference Lookups

Use Standard Lookups only to verify the parent `ZMM_NOTE_TYPE` code. Use the Sales Note Types resource only to verify effective object-context availability. The runtime result can include Default Note Types fallback and does not prove that an explicit mapping row exists.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-standard-lookups.html | Read-only parent lookup-code verification |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-notetypes-get.html | NoteTypeFinder, source-object binding, mapped-code fields, and read-only runtime evidence |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/api-object-metadata.html | Read-only object metadata boundary; not a substitute source for mapping codes |
| https://docs.oracle.com/en/cloud/saas/sales/oacts/define-notes.html | Object-specific mapping and Default Note Types fallback interpretation |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|---|
| NOTE_MAPPING.BASE_LOOKUP | find_active_sales_note_type_code | MappedLookupCode is supplied | MappedLookupCode | /fscmRestApi/resources/11.13.18.05/standardLookups/ZMM_NOTE_TYPE/child/lookupCodes/{MappedLookupCode}?onlyData=true | LookupCode, Meaning, EnabledFlag, StartDateActive, EndDateActive | Match exactly one row whose LookupCode equals MappedLookupCode and whose enabled and effective state permits use on the intended date | VerifiedLookupCode: LookupCode, VerifiedMeaning: Meaning, VerifiedEnabledFlag: EnabledFlag, VerifiedStartDate: StartDateActive, VerifiedEndDate: EndDateActive | No match or an inactive row blocks create or update guidance and routes code maintenance to Manage Sales Note Type. More than one exact match is ambiguous and stops the workflow. |
| NOTE_MAPPING.RUNTIME_LOOKUP | find_effective_note_type_for_object | Operation is ValidateRuntimeAvailability and SourceObjectCode and MappedLookupCode are present | SourceObjectCode, MappedLookupCode | /crmRestApi/resources/11.13.18.05/noteTypes?finder=NoteTypeFinder;BindSourceObjectCode={SourceObjectCode}&fields=MappedLookupCode,Meaning,SourceObjectCode&onlyData=true | MappedLookupCode, Meaning, SourceObjectCode | Match exactly one row whose MappedLookupCode and SourceObjectCode equal the requested values | RuntimeMappedLookupCode: MappedLookupCode, RuntimeMeaning: Meaning, RuntimeSourceObjectCode: SourceObjectCode | No match means the code was not verified as effectively available for that object. A match proves effective availability but not whether it came from an explicit row or Default Note Types fallback. More than one exact match is ambiguous and stops the conclusion. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Parent code found and applicable | Continue with the verified lookup code and meaning. |
| Parent code absent, disabled, or outside its effective dates | Stop mapping guidance and route code creation or correction to Manage Sales Note Type. |
| Exact runtime object-context match | Return effective availability while disclosing that the result does not identify explicit mapping versus fallback. |
| No runtime object-context match | Report that effective availability was not verified; do not claim that the base code or explicit mapping row is absent. |
| REST request fails or returns ambiguous evidence | Stop and disclose the safe endpoint identity and response status; do not retry automatically. |

## Source-Object Code Catalog Use

Read `ora_supported_object_codes.md` before forming a `BindSourceObjectCode` value. The `NoteTypeFinder` call can confirm effective availability for a supplied exact code, but it cannot distinguish an explicit mapping from Default Note Types fallback. Object Metadata is a separate public resource and its `ObjectCode` is not an approved transformation source for the mapping `SourceObjectCode`.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NOTE_MAPPING.BASE_LOOKUP | decision | 3 | reference_lookup | found->NOTE_MAPPING.RUNTIME_LOOKUP;not_requested->NOTE_MAPPING.RUNTIME_LOOKUP;not_found_or_inactive->NOTE_MAPPING.FAILED;ambiguous->NOTE_MAPPING.FAILED;failure->NOTE_MAPPING.FAILED | NOTE_MAPPING.DEPENDENCIES | stop | Always |
| NOTE_MAPPING.RUNTIME_LOOKUP | decision | 4 | reference_lookup | matched->NOTE_MAPPING.DEFAULTS;not_found->NOTE_MAPPING.DEFAULTS;not_requested->NOTE_MAPPING.DEFAULTS;ambiguous->NOTE_MAPPING.FAILED;failure->NOTE_MAPPING.FAILED | NOTE_MAPPING.BASE_LOOKUP | stop | Always |
