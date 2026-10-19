# Error Handling

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | Profile definition, scope, privilege, approval, or same-scope read-back gate fails | Stop before the configured value is changed or retried. |
| ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS | Manage Action Categories for Action Plans | Validation, import, or fresh-export verification fails | Preserve diagnostics and stop before a retry. |
| ORA_SVC_MANAGE_TEMPLATE_CATEGORIES_FOR_ACTION_PLANS | Manage Template Categories for Action Plans | Hash binding, processing status, or fresh-export verification fails | Preserve diagnostics and stop before another import. |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTION_STATUS_MAPPING | Manage Mapping of Action Plan Status Values | Validation, import, or fresh-export verification fails | Preserve diagnostics and stop before a retry. |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS | Manage Action Plan Actions | Validation, import, or fresh-export verification fails | Preserve diagnostics and stop before a retry. |
| ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES | Manage Action Plan Templates | Validation, import, or fresh-export verification fails | Preserve diagnostics and stop before a retry. |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | Approval gate | Exact profile option, scope, and proposed value. |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | APPROP.EXEC | decision | 4 | execution_gate | approved->APPROP.DONE;blocked->RETURN_ISSUES | APPROP.DESIGN | stop | A configuration change is requested |
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | APPROP.DONE | terminal | 5 | terminal | none | APPROP.EXEC | continue | Approved route completes with same-scope read-back |
| ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS | Manage Action Plan Profile Options | RETURN_ISSUES | terminal | 6 | terminal | none | none | continue | Any failed gate |
| ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS | Manage Action Categories for Action Plans | APACAT.EXEC | decision | 4 | execution_gate | approved->APACAT.DONE;blocked->RETURN_ISSUES | APACAT.DESIGN | stop | A package import is requested |
| ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS | Manage Action Categories for Action Plans | APACAT.DONE | terminal | 5 | terminal | none | APACAT.EXEC | continue | Fresh export verifies the change |
| ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS | Manage Action Categories for Action Plans | RETURN_ISSUES | terminal | 6 | terminal | none | none | continue | Any failed gate |
| ORA_SVC_MANAGE_TEMPLATE_CATEGORIES_FOR_ACTION_PLANS | Manage Template Categories for Action Plans | APTCAT.EXEC | decision | 4 | execution_gate | approved->APTCAT.DONE;blocked->RETURN_ISSUES | APTCAT.DESIGN | stop | A hash-bound package import is requested |
| ORA_SVC_MANAGE_TEMPLATE_CATEGORIES_FOR_ACTION_PLANS | Manage Template Categories for Action Plans | APTCAT.DONE | terminal | 5 | terminal | none | APTCAT.EXEC | continue | Terminal status and fresh export verify the change |
| ORA_SVC_MANAGE_TEMPLATE_CATEGORIES_FOR_ACTION_PLANS | Manage Template Categories for Action Plans | RETURN_ISSUES | terminal | 6 | terminal | none | none | continue | Any failed gate |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTION_STATUS_MAPPING | Manage Mapping of Action Plan Status Values | APSTAT.EXEC | decision | 4 | execution_gate | approved->APSTAT.DONE;blocked->RETURN_ISSUES | APSTAT.DESIGN | stop | A package import is requested |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTION_STATUS_MAPPING | Manage Mapping of Action Plan Status Values | APSTAT.DONE | terminal | 5 | terminal | none | APSTAT.EXEC | continue | Fresh export verifies the mapping |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTION_STATUS_MAPPING | Manage Mapping of Action Plan Status Values | RETURN_ISSUES | terminal | 6 | terminal | none | none | continue | Any failed gate |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS | Manage Action Plan Actions | APACT.EXEC | decision | 5 | execution_gate | approved->APACT.DONE;blocked->RETURN_ISSUES | APACT.DESIGN | stop | A package import is requested |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS | Manage Action Plan Actions | APACT.DONE | terminal | 6 | terminal | none | APACT.EXEC | continue | Fresh export verifies the action and mappings |
| ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS | Manage Action Plan Actions | RETURN_ISSUES | terminal | 7 | terminal | none | none | continue | Any failed gate |
| ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES | Manage Action Plan Templates | APTPL.EXEC | decision | 5 | execution_gate | approved->APTPL.DONE;blocked->RETURN_ISSUES | APTPL.DESIGN | stop | A supported template package import is requested |
| ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES | Manage Action Plan Templates | APTPL.DONE | terminal | 6 | terminal | none | APTPL.EXEC | continue | Fresh export verifies the template and action flow |
| ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES | Manage Action Plan Templates | RETURN_ISSUES | terminal | 7 | terminal | none | none | continue | Any failed gate |
