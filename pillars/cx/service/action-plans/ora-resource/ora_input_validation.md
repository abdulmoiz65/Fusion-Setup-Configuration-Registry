# Input Validation

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | Profile option selection | Existing profile option code and requested Site or User scope | Stop before configuration | Provide the exact existing profile option and supported scope | Reviewing or configuring | resolve_profile_option_scope |
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | Proposed configured value | Proposed value and stated business intent | Stop before configuration | Provide a value supported by the selected profile option's documented semantics | Configuring | |
| ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS | Manage Action Categories for Action Plans | Lookup-code identity | Preserve selected code for update or disable; provide approved customer-owned code for create | Stop before package construction | Do not change identity; for create, provide a non-ORA code | Creating, updating, or disabling | resolve_action_category_lookup_code |
| ORA_SVC_MANAGE_TEMPLATE_CATEGORIES_FOR_ACTION_PLANS | Manage Template Categories for Action Plans | Export package integrity | Retained parent CSV, all lookup-code rows, headers, and ASM_SETUP_CSV_METADATA.xml | Stop before package construction | Provide a completed same-task export package | Creating, updating, or disabling | |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTION_STATUS_MAPPING | Manage Mapping of Action Plan Status Values | Action-type condition shape | Selected action type and its exported object-field and condition shape | Stop before package construction | Use the selected action type's export; do not borrow another action type's shape | Creating or updating | |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS | Manage Action Plan Actions | Action identity and scope | Retain selected action identity and type; include only mappings supported by its type and context | Stop before package construction | Do not include TemplateNumber for an Actions-only operation | Creating or updating | |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS | Manage Action Plan Actions | New root identity | ActionNumber column omitted from ORA_SVC_AP_ACTIONS.csv | Stop before package construction | Remove ActionNumber, including a blank column, for a new root action | Creating a new root action | |
| ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES | Manage Action Plan Templates | Template operation choice | Explicit parent-only or Template Actions choice | Stop before package construction | Provide the requested template operation | Creating or updating a template or template action | verify_selected_action_identity |
| ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES | Manage Action Plan Templates | Template Action linkage | Verified action identity, fresh TemplateNumber, order, and mandatory setting | Stop before package construction | Create absent parent separately and fresh-read its TemplateNumber | Creating a Template Action | verify_selected_action_identity |

## Dependency-Aware Validation

| Task Code | Task Name | Applies When | Result | Next Action | Resolver |
|---|---|---|---|---|---|
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | The selected option or scope cannot be resolved exactly | Blocked | Do not configure; obtain a precise option or supported scope | resolve_profile_option_scope |
| ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS | Manage Action Categories for Action Plans | The proposed create code duplicates an existing code or selected existing code is unresolved | Blocked | Do not construct or import a package | resolve_action_category_lookup_code |
| ORA_SVC_MANAGE_TEMPLATE_CATEGORIES_FOR_ACTION_PLANS | Manage Template Categories for Action Plans | Export package is incomplete or the code selection is unresolved | Blocked | Do not construct or import a package | resolve_template_category_lookup_code |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTION_STATUS_MAPPING | Manage Mapping of Action Plan Status Values | A code-valued field lacks an exact enabled source-backed value | Blocked | Do not construct or import a package | resolve_status_mapping_code_values |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS | Manage Action Plan Actions | AttributeName is absent from the selected ObjectEntityName describe result or code value is unresolved | Blocked | Do not construct or import a package | resolve_object_entity_attribute_metadata |
| ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES | Manage Action Plan Templates | Parent-only choice, verified action identity, current parent, order, or mandatory setting is missing | Blocked | Do not construct or import a package | verify_selected_action_identity |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | APPROP.VALIDATE | step | 1 | validate_input | pass->APPROP.READ_CURRENT;fail->RETURN_ISSUES | none | stop | Any supported profile-option use case |
| ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS | Manage Action Categories for Action Plans | APACAT.VALIDATE | step | 1 | validate_input | pass->APACAT.LOOKUP_CODES;fail->RETURN_ISSUES | none | stop | Any supported action-category use case |
| ORA_SVC_MANAGE_TEMPLATE_CATEGORIES_FOR_ACTION_PLANS | Manage Template Categories for Action Plans | APTCAT.VALIDATE | step | 1 | validate_input | pass->APTCAT.LOOKUP_CODES;fail->RETURN_ISSUES | none | stop | Any supported template-category use case |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTION_STATUS_MAPPING | Manage Mapping of Action Plan Status Values | APSTAT.VALIDATE | step | 1 | validate_input | pass->APSTAT.LOOKUP_CODES;fail->RETURN_ISSUES | none | stop | Any supported status-mapping use case |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS | Manage Action Plan Actions | APACT.VALIDATE | step | 1 | validate_input | pass->APACT.ATTRIBUTE_METADATA;fail->RETURN_ISSUES | none | stop | Any supported action use case |
| ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES | Manage Action Plan Templates | APTPL.VALIDATE | step | 1 | validate_input | pass->APTPL.VERIFY_ACTIONS;fail->RETURN_ISSUES | none | stop | Any supported template use case |
