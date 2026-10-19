# Manage Balance Codes Input Validation

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | Read-only balance code retrieval | BalanceCode | Return issues and stop before the REST lookup | Provide the BalanceCode used by the alternate-key finder | Retrieving one balance code | find_balance_code_by_exact_code |
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | Read-only balance code listing | Optional limit, offset, fields | Continue with the supplied optional parameters | Omit BalanceCode to retrieve the current response page | Retrieving balance codes without a BalanceCode | list_balance_codes |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | Read-only balance profile retrieval | BalanceProfileNumber | Return issues and stop before the REST lookup | Provide the BalanceProfileNumber collection filter value | Retrieving one balance profile | find_balance_profile_by_exact_number |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | Read-only balance profile listing | Optional limit, offset, fields | Continue with the supplied optional parameters | Omit BalanceProfileNumber to retrieve the current response page | Retrieving balance profiles without a number | list_balance_profiles |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | Read-only usage entitlement retrieval | UsageEntitlementNumber | Return issues and stop before the REST lookup | Provide the UsageEntitlementNumber used by the alternate-key finder | Retrieving one usage entitlement | find_usage_entitlement_by_exact_number |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | Read-only usage entitlement listing | Optional limit, offset | Continue with the supplied optional parameters | Omit UsageEntitlementNumber to retrieve the current response page | Retrieving usage entitlements without a number | list_usage_entitlements |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | Read-only entitlement-plan listing | Optional limit, offset, fields, q, orderBy | Continue with the supplied optional parameters | Request subscriptionUsageEntitlements first; use the documented paging values to retrieve all pages and use the declared fallback only when the primary collection lookup fails | Retrieving entitlement plans without an EntitlementPlanNumber | list_usage_entitlement_plans |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | Read-only entitlement-assignment listing | Optional limit, offset, fields, q, orderBy | Continue with the supplied optional parameters | Request the assignment collection; use the documented paging values to retrieve all pages | Retrieving entitlement assignments without an EntitlementAssignmentNumber | list_entitlement_assignments |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | Entitlement-plan status action retrieval | EntitlementPlanNumber | Return issues and stop before preparing a Data Loader activation or deactivation source | Provide the exact EntitlementPlanNumber used by the entitlement-plan item GET | Activating or deactivating an entitlement plan | find_entitlement_plan_by_exact_number |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | Entitlement-assignment status action retrieval | EntitlementAssignmentNumber | Return issues and stop before preparing a Data Loader activation or deactivation source | Provide the exact EntitlementAssignmentNumber used by the entitlement-assignment item GET | Activating or deactivating an entitlement assignment | find_entitlement_assignment_by_exact_number |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | BALCODE.VALIDATE | decision | 10 | validate_input | item->BALCODE.LOOKUP;list->BALCODE.LIST;issues->BALCODE.ISSUES | none | stop | Any Manage Balance Codes request |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | BALPROFILE.VALIDATE | decision | 10 | validate_input | item->BALPROFILE.LOOKUP;list->BALPROFILE.LIST;issues->BALPROFILE.ISSUES | none | stop | Any Manage Balance Profiles request |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | USAGEENT.VALIDATE | decision | 10 | validate_input | item->USAGEENT.LOOKUP;list->USAGEENT.LIST;entitlement_plan->ENTPLAN.LOOKUP;entitlement_plan_list->USAGEENT.PLAN.LIST;entitlement_assignment->ENTASSIGN.LOOKUP;entitlement_assignment_list->ENTASSIGN.LIST;issues->USAGEENT.ISSUES | none | stop | Any Manage Usage Entitlement request |
