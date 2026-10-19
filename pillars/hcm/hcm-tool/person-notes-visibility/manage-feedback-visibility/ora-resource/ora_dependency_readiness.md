# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Exact configuration identity | Resolve an exact current ContextType code or meaning for read, create uniqueness, edit, or delete. |
| 2 | Common lookup values | Resolve ContextType through ORA_FEEDBACK_CONTEXT_TYPE, selected DefaultNoteVisibilityCode values other than No Default through ORA_NOTE_VISIBILITY_CODE, and ManagerType or NotificationManagerTypeList through PER_SUPERVISOR_TYPE only when ContextType is ORA_NO_CONTEXT, using Common > Manage Common Lookups. Preserve No Default exactly as the normalized business value without a lookup. Treat a returned literal #NULL as invalid stored data. For every context other than ORA_NO_CONTEXT, keep manager type blank and do not run the manager-type lookup. |
| 3 | Profile option values | Resolve each applicable profile option value through Common > Manage Profile Options. |
| 4 | Data Loader contract | Verify operation, key fields, required fields, editable attributes, registered adapter type, and an explicit supported No Default mapping when No Default is requested for personNotesVisibilityConfigurations. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| exact_configuration | Exact Person Notes Visibility configuration | Conditional | Read, create, edit, or delete | Lookup | ContextType code or context Meaning | find_person_notes_visibility_configuration_by_exact_context | Reads require one exact context row, creates require absence, and edit or delete requires one exact current target | Supply the exact ContextType code or context Meaning | Exact identity, current values, key fields, context Meaning, and match count |
| feedback_context_type | Feedback context type | Conditional | A configuration row is returned, or ContextType is supplied or must be validated | Lookup | Common > Manage Common Lookups; LookupType ORA_FEEDBACK_CONTEXT_TYPE | resolve_feedback_context_type | ContextType must resolve to one current exact feedback-context lookup code and meaning | Supply the exact ContextType code or meaning | ContextType and displayed Context meaning |
| feedback_default_visibility | Feedback default visibility | Conditional | DefaultNoteVisibilityCode is a selected value other than No Default | Lookup | Common > Manage Common Lookups; LookupType ORA_NOTE_VISIBILITY_CODE | resolve_feedback_default_visibility | A selected default visibility must resolve to one current exact lookup code and meaning | Supply the exact DefaultNoteVisibilityCode or meaning; supply the exact business value No Default when no default is requested | DefaultNoteVisibilityCode and displayed Default Visibility meaning |
| feedback_manager_type | Feedback notification manager type | Conditional | ContextType is ORA_NO_CONTEXT and ManagerType or NotificationManagerTypeList is supplied or returned | Lookup | Common > Manage Common Lookups; LookupType PER_SUPERVISOR_TYPE | resolve_feedback_manager_type | Manager Type applies only to Anytime Feedback and must resolve to one current exact supervisor-type lookup code and meaning | For Anytime Feedback, supply the exact ManagerType or NotificationManagerTypeList code or meaning; for every other context leave it blank | NotificationManagerTypeList and displayed Manager Type meaning for ORA_NO_CONTEXT only |
| profile_option_value | Applicable profile option value | Conditional | A profile option affects the requested configuration | Lookup | Common > Manage Profile Options | resolve_feedback_visibility_profile_option_value | Profile-level precedence must be evaluated by the owning Common task | Supply the exact profile option code or name and level context | Profile option identity, level, and effective value |
| dataloader_contract | Person Notes Visibility Data Loader metadata | Yes | Create, edit, or delete | Verify | core.data-loader metadata for personNotesVisibilityConfigurations | verify_person_notes_visibility_data_loader_contract | Mutation preparation requires supported operation metadata and exact keys; No Default additionally requires an explicit adapter mapping because the normalized value must remain No Default and must not be sent as blank, null, #NULL, or an unrecognized lookup value | Generate and retain the editable, key-fields, and attribute-details workbooks; when No Default is requested, provide metadata proving the supported adapter mapping or stop | Operation, key fields, required fields, editable attributes, adapter type, No Default mapping support, and artifact references |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency is exact and current | Yes for read-only lookups; mutation preparation continues only through core.data-loader |
| Lookup | A named read-only resolver can establish the value | Yes, read-only lookup only |
| Blocked | A target, lookup, profile option value, key, operation, or artifact is missing or ambiguous | No |
