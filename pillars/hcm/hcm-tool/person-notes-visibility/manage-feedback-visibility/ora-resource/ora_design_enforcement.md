# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve the target | Create must prove exact-context absence; edit and delete must resolve exactly one current ContextType row. |
| 2 | Resolve dependencies | ContextType must resolve through ORA_FEEDBACK_CONTEXT_TYPE, selected DefaultNoteVisibilityCode values other than No Default through ORA_NOTE_VISIBILITY_CODE, ManagerType or NotificationManagerTypeList through PER_SUPERVISOR_TYPE only when ContextType is ORA_NO_CONTEXT, and profile option values through their owning Common tasks. Preserve No Default exactly as the normalized business value. Treat a returned literal #NULL as invalid stored data. Manager type must remain blank for every other context. |
| 3 | Verify Data Loader metadata | Confirm the requested operation, keys, editable attributes, registered adapter type, and explicit supported No Default mapping when applicable for personNotesVisibilityConfigurations. |
| 4 | Select the mutation route | Route create, edit, and delete only through core.data-loader. |
| 5 | Gate execution | Bind approval to the exact environment, operation, keys, values, and immutable Data Loader artifact immediately before execution. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A configuration row is returned, or ContextType is supplied or must be validated | Error | resolve_feedback_context_type | The value does not resolve to exactly one current code and meaning in ORA_FEEDBACK_CONTEXT_TYPE | Use the exact ContextType LookupCode and display Meaning returned by Common > Manage Common Lookups | Yes |
| DefaultNoteVisibilityCode is a selected value other than No Default | Error | resolve_feedback_default_visibility | The value does not resolve to exactly one current code and meaning in ORA_NOTE_VISIBILITY_CODE | Use the exact DefaultNoteVisibilityCode LookupCode and display Meaning returned by Common > Manage Common Lookups | Yes |
| Create or edit explicitly requests No Default | Error | verify_person_notes_visibility_data_loader_contract | The normalized value is blank, null, or #NULL; or the registered adapter does not advertise a mapping from the exact business value No Default to the backend no-default state | Preserve the normalized value exactly as No Default and stop before Data Loader preview until the adapter mapping is documented and supported | No |
| A read returns #NULL in DefaultNoteVisibilityCode | Error |  | The literal value is stored in Fusion and does not represent the normalized No Default business value | Repair the row through an approved supported Data Loader operation using a valid mapped value; do not reuse #NULL | Yes |
| ContextType is ORA_NO_CONTEXT and ManagerType or NotificationManagerTypeList is supplied or returned | Error | resolve_feedback_manager_type | The value does not resolve to exactly one current code and meaning in PER_SUPERVISOR_TYPE | Use the exact NotificationManagerTypeList LookupCode and display Meaning returned by Common > Manage Common Lookups | Yes |
| ContextType is not ORA_NO_CONTEXT | Error |  | NotificationManagerTypeList is nonblank in a create or edit artifact, a list shows a manager value, or Manager Type is visible in a detail or edit view | Keep NotificationManagerTypeList blank in the mutation artifact; ignore any raw stored value in the normalized result, leave list output blank, and hide Manager Type in detail or edit views | Yes |
| A profile option value is required | Error | resolve_feedback_visibility_profile_option_value | The profile option, level, or applicable value cannot be resolved exactly | Use the exact effective value returned by the owning Common task | Yes |
| Create, edit, or delete is requested | Error | verify_person_notes_visibility_data_loader_contract | Data Loader metadata does not advertise the operation, key fields, or editable attributes | Correct the Data Loader artifact or stop the unsupported operation | Yes |
| Create or edit is requested | Error | resolve_feedback_context_type | `ContextTypeNotCode` is blank or does not exactly equal the current row's resolved `ContextType` LookupCode. Fusion requires this source column as REST user-key bind variable `ContextCode`. | Derive both fields from the row's exact lookup result; do not hardcode a context value. Regenerate the immutable archive and restart validation. | Yes |
| Create, edit, or delete would use a direct Fusion REST mutation | Error |  | The route contains POST, PATCH, PUT, DELETE, or an action request sent directly to Fusion | Route the operation through core.data-loader | Yes |
| Edit or delete target resolution used a partial-context search | Error | find_person_notes_visibility_configuration_by_exact_context | No separate exact-context read proves one current target | Resolve one exact ContextType code or context Meaning before preparing the Data Loader artifact | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_feedback_context_type | A configuration row is returned, or ContextType is supplied or must be validated | ContextType and displayed Context meaning from ORA_FEEDBACK_CONTEXT_TYPE | ora_reference_lookups.md |
| resolve_feedback_default_visibility | DefaultNoteVisibilityCode is a selected value other than No Default | DefaultNoteVisibilityCode and displayed Default Visibility meaning from ORA_NOTE_VISIBILITY_CODE | ora_reference_lookups.md |
| resolve_feedback_manager_type | ContextType is ORA_NO_CONTEXT and ManagerType or NotificationManagerTypeList is supplied or returned | NotificationManagerTypeList and displayed Manager Type meaning from PER_SUPERVISOR_TYPE | ora_reference_lookups.md |
| resolve_feedback_visibility_profile_option_value | A profile option value affects the configuration | Profile option identity, level, and effective value | ora_reference_lookups.md |
| verify_person_notes_visibility_data_loader_contract | Create, edit, or delete is requested | Supported operation, key fields, required fields, and editable attributes | ora_reference_lookups.md |
| find_person_notes_visibility_configuration_by_exact_context | Edit or delete is requested | Exact configuration identity, key fields, context Meaning, and current values | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FEEDBACK_VISIBILITY.ENFORCE_MUTATION_ROUTE | decision | 9 | design_enforcement | dataloader_ready->FEEDBACK_VISIBILITY.DATALOADER_READY;direct_rest_requested->FEEDBACK_VISIBILITY.ROUTE_UNSUPPORTED;preview_incomplete->FEEDBACK_VISIBILITY.INPUT_INVALID | FEEDBACK_VISIBILITY.VERIFY_DATALOADER_CONTRACT | stop | The requested operation is create, edit, or delete |
