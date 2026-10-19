# Reference Lookups

## Live Lookups
| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| NTM.LOOKUP | resolve_note_type_mapping | Effective note types are requested for an object | SourceObjectCode defaults to NOTE when omitted; otherwise one of NOTE, ZCH_DUP_IDNT_BATCH, or ZCH_DUP_RES_REQUEST; optional exact MappedLookupCode | /crmRestApi/resources/11.13.18.05/noteTypes; use finder=NoteTypeFinder;BindSourceObjectCode={effective SourceObjectCode} | SourceObjectCode, MappedLookupCode, Meaning, and links | Apply NOTE when SourceObjectCode is omitted; otherwise require one supported exact source object and an exact code filter when supplied; returned rows are effective mappings | Effective mapped lookup codes and meanings | Return empty as no effective rows; stop on unsupported source object, ambiguity, or auth failure |

## Lookup Execution Rules
| Situation | What Happens |
|---|---|
| Read | Use the CRM noteTypes collection or exact returned item URI with GET only. |
| Mutation | Refuse. Live describe exposes only collection/item GET and all fields have allowChanges never. |
| Mapping change | Use explicit supported FSM import or guided task UI; do not substitute Apps Common lookup CRUD. |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NTM.LOOKUP | decision | 20 | reference_lookup | resolved_or_empty_or_not_needed->NTM.DEFAULTS;ambiguous_or_failed->NTM.ERROR | NTM.VALIDATE | stop | Resolve effective note-type mappings. |
