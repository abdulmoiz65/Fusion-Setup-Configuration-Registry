# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Read current profile state | Resolve the selected profile definition, scope availability, updateability, and current scoped value. |
| 2 | Confirm change design | Confirm the requested scope is enabled and updateable and the proposed value has documented semantics. |
| 3 | Obtain approval | Obtain explicit approval for the exact profile option, scope, and proposed value. |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | Configuring a profile option | Blocking | resolve_profile_option_scope | The selected level is not enabled and updateable, the profile-value privilege is unavailable, or the exact option, scope, and proposed value lack approval | Read current scope state and obtain approval for the exact change | Yes |
| ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS | Manage Action Categories for Action Plans | Creating, updating, or disabling an action category | Blocking | resolve_action_category_lookup_code | The package is not based on a completed export of this task, changes an unapproved value, or uses a reserved ORA-prefixed create code | Retain task-owned values and change only approved fields | Yes |
| ORA_SVC_MANAGE_TEMPLATE_CATEGORIES_FOR_ACTION_PLANS | Manage Template Categories for Action Plans | Creating, updating, or disabling a template category | Blocking | resolve_template_category_lookup_code | The package is incomplete, the import hash is not bound to approval, or processing status is not terminal | Retain all required export members and wait for terminal processing status | Yes |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTION_STATUS_MAPPING | Manage Mapping of Action Plan Status Values | Creating or updating a status mapping | Blocking | resolve_status_mapping_code_values | The mapping uses an object-field or condition shape from a different action type | Use the selected action type's exported condition shape | Yes |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS | Manage Action Plan Actions | Creating or updating an action | Blocking | resolve_action_code_values | A template-action link or TemplateNumber is included in an Actions-only package, linkage inputs are inferred, or a required code is unresolved | Complete and approve the action operation independently | Yes |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS | Manage Action Plan Actions | Creating or updating an action with attribute mappings | Blocking | resolve_object_entity_attribute_metadata | An AttributeName is not in the selected ObjectEntityName described candidate list | Select mappings only from the declared ObjectEntity describe result | Yes |
| ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES | Manage Action Plan Templates | Creating or updating a template or template action | Blocking | verify_selected_action_identity | The parent-only choice, verified action identity, fresh parent TemplateNumber, order, or mandatory setting is missing | Create any absent parent separately, fresh-read its TemplateNumber, then prepare a separately approved linkage package | Yes |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | resolve_profile_option_scope | Before configuring a profile option | Profile definition, enabled and updateable scope, current configured value | ora_reference_lookups.md |
| ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS | Manage Action Categories for Action Plans | resolve_action_category_lookup_code | Before package construction | Exact code and lookup metadata for ORA_SVC_AP_ACTION_CATEGORY_CD | ora_reference_lookups.md |
| ORA_SVC_MANAGE_TEMPLATE_CATEGORIES_FOR_ACTION_PLANS | Manage Template Categories for Action Plans | resolve_template_category_lookup_code | Before package construction | Exact code and lookup metadata for ORA_SVC_AP_ACTION_PLAN_TYPE_CD | ora_reference_lookups.md |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTION_STATUS_MAPPING | Manage Mapping of Action Plan Status Values | resolve_status_mapping_code_values | Before package construction | Candidate codes and source-backed lookup metadata for every supplied field | ora_reference_lookups.md |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS | Manage Action Plan Actions | resolve_object_entity_attribute_metadata | Attribute mappings are requested | Candidate AttributeName values for the action's selected ObjectEntityName | ora_reference_lookups.md |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS | Manage Action Plan Actions | resolve_action_code_values | Before package construction | Candidate codes and source-backed lookup metadata for every supplied field | ora_reference_lookups.md |
| ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES | Manage Action Plan Templates | verify_selected_action_identity | Template Actions are requested | Verified ActionNumber, ActionId, Name, target TemplateNumber | ora_reference_lookups.md |
| ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES | Manage Action Plan Templates | resolve_template_code_values | Before package construction | Candidate codes and source-backed lookup metadata for every supplied field | ora_reference_lookups.md |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | APPROP.DESIGN | decision | 3 | design_enforcement | pass->APPROP.EXEC;blocked->RETURN_ISSUES | APPROP.READ_CURRENT | stop | A configuration change is requested |
| ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS | Manage Action Categories for Action Plans | APACAT.DESIGN | decision | 3 | design_enforcement | pass->APACAT.EXEC;blocked->RETURN_ISSUES | APACAT.LOOKUP_CODES | stop | Creating, updating, or disabling an action category |
| ORA_SVC_MANAGE_TEMPLATE_CATEGORIES_FOR_ACTION_PLANS | Manage Template Categories for Action Plans | APTCAT.DESIGN | decision | 3 | design_enforcement | pass->APTCAT.EXEC;blocked->RETURN_ISSUES | APTCAT.LOOKUP_CODES | stop | Creating, updating, or disabling a template category |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTION_STATUS_MAPPING | Manage Mapping of Action Plan Status Values | APSTAT.DESIGN | decision | 3 | design_enforcement | pass->APSTAT.EXEC;blocked->RETURN_ISSUES | APSTAT.LOOKUP_CODES | stop | Creating or updating a status mapping |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS | Manage Action Plan Actions | APACT.DESIGN | decision | 4 | design_enforcement | pass->APACT.EXEC;blocked->RETURN_ISSUES | APACT.LOOKUP_CODES | stop | Creating or updating an action |
| ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES | Manage Action Plan Templates | APTPL.DESIGN | decision | 4 | design_enforcement | pass->APTPL.EXEC;blocked->RETURN_ISSUES | APTPL.LOOKUP_CODES | stop | Creating or updating a template or template action |
