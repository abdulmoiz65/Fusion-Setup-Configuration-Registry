# Topics Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| learningItemType | ORA_COMMUNITY | Create omits the shared root type and the target confirms the supplied Describe default | No; never substitute another item type | resolve_topic_runtime_values |
| learningItemSubType | No implicit default | Every create | No; require the exact target-supported Topic subtype | resolve_topic_runtime_values |
| learningItemStatus | Target-resolved Active value | Create | No; current 26C Topic creation is Active and no Draft option is offered | resolve_topic_runtime_values |
| learningItemVisibility | Target-confirmed Open value | Create omits visibility and the proposal discloses the confirmed default | No; preserve an explicit supported user value | resolve_topic_runtime_values |
| Summary | Blank with warning, or editable text generated only from the user-supplied title | Create omits summary; generation is used only when enabled and permitted | Never replace user-authored text, use another source, or generate without permission; label generated text and keep it editable | |
| Member contributions | Target-confirmed disabled value | Create omits the setting and the target supports the root contribution field | An explicit enable request may override only after capability, privilege, and impact approval | resolve_topic_runtime_values |
| Initial manager | Creator as system-populated manager | Create | No; disclose and verify the automatic relationship | read_topic_relationships |
| Category relationship | Standalone Topic | Create has no approved Category child row | An approved post-create Category relationship may be added through its confirmed route | |
| ORA_WLF_SS_CATALOG_SEARCH_MODE | Preserve the current effective value | Topic catalog-search behavior is being designed or tuned and no exact change is approved | Never change silently; use only the approved broader-recall, balanced-matching, or tighter-precision choice and verify representative searches | resolve_topic_profile_option |
| Batch failure scope | Block only the affected parent or child row | Some rows are invalid or unsupported | No; preserve valid independent rows for proposal | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TOP.APPLY_DEFAULTS | decision | 4 | apply_default | applied->TOP.ENFORCE_DESIGN;preserved->TOP.ENFORCE_DESIGN;blocked->TOP.HANDLE_ERROR | TOP.RESOLVE_REFERENCE | stop | Validated Topic rows omit only a documented, target-confirmed, disclosed default |
