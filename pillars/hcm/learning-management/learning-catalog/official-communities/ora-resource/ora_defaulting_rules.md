# Official Communities Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| learningItemType | ORA_COMMUNITY | Create after exact Official Community subtype resolution | No; preserve the Describe-confirmed parent type and never use it as proof of subtype | |
| Creation lifecycle | Active business outcome | Create after the target supplies the exact supported status code | No; do not offer Draft and do not infer a code from the FDD meaning | |
| learningItemVisibility | Target-confirmed code meaning Open | Create omits visibility and the current target confirms the enabled Open value | Yes; preserve a supported explicit user choice | resolve_official_community_visibility |
| Member contributions | Disabled | Create omits contribution intent and the target capability supports this setting | Yes; enable only when explicitly requested and supported | |
| Creator relationship | Creator becomes initial manager | Create | No; disclose and verify this system behavior instead of adding a duplicate manager row | |
| Summary generation | No generated text unless tenant-required or requested, Generate is enabled, and the user permits it | Summary is missing | Yes; user-authored text always wins and generated text remains editable and approval-bound | |
| Applicable profile-option value | Preserve the current effective and configured value | The option trigger applies but no exact approved change is required | No; omit an already-correct value from the dialog and never change a profile silently | read_official_community_profile_options |
| Parent-child order | Create and read back parent before eligible child rows | Create includes child operations | No | |
| Batch failure scope | Block only the affected parent or child row | Some independent rows are invalid or unsupported | No; preserve valid independent rows for the revised proposal | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OCM.APPLY_DEFAULTS | decision | 4 | apply_default | applied->OCM.ENFORCE_DESIGN;preserved->OCM.ENFORCE_DESIGN;blocked->OCM.HANDLE_ERROR | OCM.RESOLVE_REFERENCE | stop | Validated Official Community rows omit only a source-documented and target-confirmed default |
