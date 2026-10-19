# Categories Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| learningItemType | ORA_COMMUNITY | Create omits the shared parent type | No; this does not replace Category subtype validation | |
| learningItemSubType | Current resolved Category subtype | Every create and every subtype-isolated title lookup | No; do not accept a Topic or Official Community subtype | resolve_category_field_values |
| learningItemStatus | Current resolved Active value | Create | No; FDD v7 maps create to activation, so send or verify Active explicitly and do not expose Draft | resolve_category_field_values |
| learningItemViewModeESS | Current confirmed Open value | Create omits visibility | No; disclose the code and meaning in the proposal and never widen visibility silently | resolve_category_field_values |
| Summary | No summary | Summary is omitted and generation is disabled or declined | Yes; accept user-authored text, or text generated only from the supplied title when generation is enabled, disclosed, and approved | |
| ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD | Preserve current effective value | Unified listing/CAP administration does not apply, or an applicable value change is not exactly approved | No; Site Y may be proposed only after applicable CAP validation | resolve_single_catalog_listing_profile |
| ORA_WLF_SS_CATALOG_SEARCH_MODE | Preserve current effective value | Category catalog search is not being designed/tuned, or no exact change is approved | No; never infer a new value from general search intent | resolve_category_search_mode_profile |
| Featured dates | No start and no end | Parent or Topic association dates are omitted | Yes; accept a valid start, or valid start/end pair | |
| Initial manager | Authenticated creator as system-populated manager | Create | No; display the relationship and preserve at least one active manager | |
| Batch failure scope | Block only the affected parent or child row | Some rows are invalid or a child capability is unavailable | No; preserve valid independent rows and stable row IDs | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAT.APPLY_DEFAULTS | decision | 4 | apply_default | applied->CAT.ENFORCE_DESIGN;preserved->CAT.ENFORCE_DESIGN;blocked->CAT.HANDLE_ERROR | CAT.RESOLVE_REFERENCE | stop | Validated profile decisions and Category rows preserve or apply only documented, disclosed safe defaults |
