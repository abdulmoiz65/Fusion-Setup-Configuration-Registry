# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | Operation: list, read, search, create, edit, or delete | Stop and request one operation | The requester supplies exactly one supported operation | Every request |  |
| Exact configuration identity | ContextType code or context Meaning | Stop and request the exact ContextType code or context Meaning | Resolve through the exact-context configuration lookup | Read, create, edit, or delete | find_person_notes_visibility_configuration_by_exact_context |
| Search input | SearchTerm | Stop and request a nonblank context term | Use only the contains-context search resolver | Search | search_person_notes_visibility_configurations_by_context_term |
| Mutation artifact | Validated Data Loader workbook set and requested operation | Stop before preview | Generate and validate the personNotesVisibilityConfigurations workbook set through core.data-loader | Create, edit, or delete | verify_person_notes_visibility_data_loader_contract |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A configuration row is returned, or ContextType is supplied or must be validated | Lookup | Resolve the exact current code and meaning from ORA_FEEDBACK_CONTEXT_TYPE through Common > Manage Common Lookups | resolve_feedback_context_type |
| DefaultNoteVisibilityCode is a selected visibility value other than No Default | Lookup | Resolve the exact current code and meaning from ORA_NOTE_VISIBILITY_CODE through Common > Manage Common Lookups | resolve_feedback_default_visibility |
| Create or edit explicitly requests No Default | Verify | Preserve the normalized business value exactly as No Default; never convert it to blank, null, or #NULL. Stop before Data Loader preview unless the registered adapter contract explicitly maps No Default to the backend no-default state without persisting the label as a lookup code | verify_person_notes_visibility_data_loader_contract |
| ContextType is ORA_NO_CONTEXT and ManagerType or NotificationManagerTypeList is supplied or returned | Lookup | Resolve the exact current code and meaning from PER_SUPERVISOR_TYPE through Common > Manage Common Lookups | resolve_feedback_manager_type |
| ContextType is not ORA_NO_CONTEXT and ManagerType or NotificationManagerTypeList is supplied or returned | Verify | Keep NotificationManagerTypeList blank in create or edit artifacts, ignore any raw stored backend value for presentation, leave Manager Type blank in lists, and hide the field in detail or edit views |  |
| A profile option value affects the requested configuration | Lookup | Resolve the exact applicable value through the owning Common task | resolve_feedback_visibility_profile_option_value |
| Edit or delete is requested | Verify | Require one exact-context target and retain its Data Loader key fields | find_person_notes_visibility_configuration_by_exact_context |
| Create is requested | Verify | Require zero exact-context matches before preparing the artifact | find_person_notes_visibility_configuration_by_exact_context |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ContextType code or context Meaning is a nonblank string | Reject a blank or whitespace-only exact context identifier | Read, create, edit, or delete |  |
| SearchTerm is a nonblank string | Reject blank or whitespace-only SearchTerm | Search |  |
| Query literal escaping | Escape quote and backslash characters before URL encoding an exact resolved ContextType predicate | Exact-context read |  |
| No Default representation | Keep the normalized Default Visibility value exactly as No Default and reject normalization to blank, null, or #NULL. Do not place the literal label in a Data Loader artifact unless the registered adapter explicitly advertises that mapping | Create or edit requests No Default | verify_person_notes_visibility_data_loader_contract |
| Manager type applicability | Allow and display Manager Type only when ContextType is ORA_NO_CONTEXT; for every other context require NotificationManagerTypeList to be blank in create or edit artifacts, leave the list value blank, and hide the field in detail or edit views even when Fusion returns a stored value | Read, create, edit, or delete |  |
| Mutation route | Reject any request that would send a direct mutating Fusion REST call | Create, edit, or delete | verify_person_notes_visibility_data_loader_contract |
| Artifact identity | Require business object personNotesVisibilityConfigurations and the operation selected in the approved preview | Create, edit, or delete | verify_person_notes_visibility_data_loader_contract |
| REST ContextCode bind | For every create or edit row, derive `ContextTypeNotCode` from that row's exact `ContextType` LookupCode resolved through `ORA_FEEDBACK_CONTEXT_TYPE`; the two values must match exactly. Do not use a literal context value, a display meaning, a blank value, or another row's code. This column supplies Fusion's required REST user-key bind variable `ContextCode`. | Create or edit | resolve_feedback_context_type |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FEEDBACK_VISIBILITY.VALIDATE_REQUEST | decision | 1 | validate_input | list->FEEDBACK_VISIBILITY.LIST_CONFIGURATIONS;read->FEEDBACK_VISIBILITY.FIND_EXACT_CONTEXT;search->FEEDBACK_VISIBILITY.SEARCH_CONTEXT_TERM;create->FEEDBACK_VISIBILITY.FIND_EXACT_CONTEXT;edit->FEEDBACK_VISIBILITY.FIND_EXACT_CONTEXT;delete->FEEDBACK_VISIBILITY.FIND_EXACT_CONTEXT;invalid->FEEDBACK_VISIBILITY.INPUT_INVALID | none | stop | Every request |
