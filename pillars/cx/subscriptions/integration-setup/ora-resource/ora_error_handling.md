# Error Handling

Source: Oracle REST API for Subscription Grouping Rule Sets and the user-declared review and Data Loader REST import scope.

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | Required rule-set identity is missing or invalid | Stop and report the missing or invalid identifier |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | A lookup has no exact match or returns an ambiguous exact-name selection | Stop and ask for the rule-set number or a disambiguating value |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | A child attributes enclosure is absent or unreadable | Return the parent and available child values, identify the unresolved child, and stop the incomplete detail flow |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | ruleBuilderConditions retrieval fails | Return the parent details, disclose the sanitized read failure, and stop the incomplete detail flow |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | A ConditionJson enclosure is absent, unreadable, or cannot be parsed | Return the condition identity, disclose the sanitized read or parse failure, and stop the incomplete detail flow |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | A SplittingRuleAttrs enclosure is absent, unreadable, or cannot be parsed | Return the parent details, disclose the sanitized read or parse failure, and stop the incomplete detail flow |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | Grouping Rules or Segregation Rule attributes cannot resolve a title | Display the API name only for review; retain the required consumer header (`GroupingRuleGrouping` for Grouping Rules and `GroupingRuleSplitting` for Segregation Rule); stop a create preview if a supplied display title is ambiguous or unresolved |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | Selection Rule attributes cannot resolve a title | Display the API name only for review; stop a create preview if a supplied display title is ambiguous or unresolved |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | Object metadata cannot resolve a supplied DisplayName to one RestResource | Stop the create preview and request a disambiguating object DisplayName |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | The Data Loader source, live schema, mapping, archive, Task Hook envelope, or approval is incomplete or invalid | Stop before upload or initiation and present the exact blocking requirement |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | Data Loader schema validation, upload, initiation, or processing fails | Preserve the redacted Data Loader diagnostic and stop; do not retry upload or initiation without a new valid approval |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | A Fusion GET request fails | Preserve the redacted response status and error, then stop without retrying or attempting any write |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | The read-semantic getPublishedStatus POST fails or returns no result | Preserve the redacted response status and error, then stop without retrying or invoking the publish action |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | The read-semantic getOmOssAttrMap POST fails or returns no result | Preserve the redacted response status and error, then stop without retrying or invoking a write action |

## Error Classifications

| Task Code | Task Name | Result Category | When Used | Next Action |
|---|---|---|---|---|
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | MISSING | Required input or exact identity is unavailable | Request only the missing value |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | FAILED | Fusion read-only lookup fails | Disclose the sanitized failure and stop |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | A load request without a matching immutable Data Loader archive, Task Hook validation envelope, and explicit current approval | Do not upload or initiate a Data Loader request |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | A direct REST mutation, CSV import, or an unapproved Data Loader upload/initiation is requested | Do not execute it; this task supports review and approved Data Loader REST import or publishing only |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | GROUPRULE.DONE | terminal | 80 | terminal | none | GROUPRULE.REVIEW | stop | Read-only specific-rule-set view or review is complete |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | GROUPRULE.LIST_DONE | terminal | 85 | terminal | none | GROUPRULE.LIST | stop | Read-only rule-set list view is complete |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | GROUPRULE.PUBLISHED_STATUS_DONE | terminal | 86 | terminal | none | GROUPRULE.PUBLISHED_STATUS | stop | Read-only published-status lookup is complete |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | GROUPRULE.OM_OSS_ATTR_MAP_DONE | terminal | 87 | terminal | none | GROUPRULE.OM_OSS_ATTR_MAP | stop | Read-only Order Management to Subscription attribute-map lookup is complete |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | GROUPRULE.RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | Validation, lookup, or design checks fail |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | GROUPRULE.CREATE_READY | terminal | 95 | terminal | none | GROUPRULE.CREATE_PREVIEW | stop | Exact Data Loader archive preview is ready for explicit approval |
| CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS | Manage Grouping Rules for Order Management to Subscriptions | GROUPRULE.OM_OSS_ATTR_MAP_UPDATE_READY | terminal | 96 | terminal | none | GROUPRULE.OM_OSS_ATTR_MAP_UPDATE_PREVIEW | stop | Exact Order Management to Subscription attribute-map Data Loader archive preview is ready for explicit approval |
