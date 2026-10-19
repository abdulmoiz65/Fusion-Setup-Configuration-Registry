# Reference Lookups

## Task Lookup Inventory
| Lookup Type | Meaning | Configuration Level | Validated Scope |
|---|---|---|---|
| ZMM_NOTE_TYPE | Note Type | Extensible | Product-specific classifications used to select note types |

## Live Lookups
| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| NT.LOOKUP | resolve_customer_data_hub_note_type | Any REST operation | Optional exact LookupCode | /fscmRestApi/resources/11.13.18.05/standardLookups/ZMM_NOTE_TYPE?expand=lookupCodes or exact code URI | Type/code values, level, module, security, seed fields, links, and code describe | Exact parent and exact code; CreatedBy equal to SEED_DATA_FROM_APPLICATION proves seeded origin | Current values, seed state, links, and writable fields | Stop with catalog_or_metadata_mismatch |

## Lookup Execution Rules
| Situation | What Happens |
|---|---|
| Read | Return current ZMM_NOTE_TYPE values through Apps Common. |
| Custom code mutation | After exact GET, describe, preview, and approval, return evidence for one Apps Common POST, PATCH, or DELETE. |
| Seeded or unknown-origin code | Refuse delete, identity, state/date, description, sequence, or tag changes; allow at most a separately proven wording change. |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NT.LOOKUP | decision | 20 | reference_lookup | resolved_or_not_needed->NT.DEFAULTS;missing_or_ambiguous->NT.ERROR | NT.VALIDATE | stop | Resolve current note-type evidence. |
