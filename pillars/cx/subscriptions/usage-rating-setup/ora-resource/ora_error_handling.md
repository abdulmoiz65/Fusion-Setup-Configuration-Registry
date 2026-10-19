# Manage Balance Codes Error Handling

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | BalanceCode is missing or the read-only item GET does not find the requested balance code | Return an actionable issue and stop; do not retry or attempt a write |
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | The read-only balance-code collection GET fails | Report the API failure and stop; do not retry automatically |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | A balance-profile lookup does not return a record or reports an API failure | Return an actionable issue and stop; do not retry or attempt a write |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | A usage-entitlement lookup does not return a record or reports an API failure | Return an actionable issue and stop; do not retry or attempt a write |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | The entitlement-plan listing through subscriptionUsageEntitlements fails or returns an invalid pagination response | Do not retry the primary request; continue once through the declared subscriptionEntitlementPlans and subscriptionEntitlementAssignments fallback |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | An entitlement-plan lookup does not return an exact record, reports an API failure, or returns a status incompatible with the requested status action | Return an actionable issue and stop; do not prepare, retry, or submit a Data Loader source |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | A fallback entitlement-plan or entitlement-assignment collection GET fails, returns an invalid pagination response, or cannot be joined by EntitlementPlanNumber | Report the API failure, pagination defect, or join defect and stop; do not retry automatically or attempt a write |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | An entitlement-assignment lookup does not return an exact record, reports an API failure, or returns a status incompatible with the requested status action | Return an actionable issue and stop; do not prepare, retry, or submit a Data Loader source |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | An entitlement-assignment collection GET fails or returns an invalid pagination response | Report the API failure or pagination defect and stop; do not retry automatically or attempt a write |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | BALCODE.LIST.RESULTS | terminal | 30 | terminal | none | BALCODE.LIST | stop | The collection lookup returned one or more balance-code rows with status in the default presentation |
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | BALCODE.LIST.EMPTY | terminal | 40 | terminal | none | BALCODE.LIST | stop | The collection lookup returned an empty result set |
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | BALCODE.SUCCESS | terminal | 60 | terminal | none | BALCODE.LOOKUP | stop | The read-only item lookup returned BalanceCode, Type, and Status |
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | BALCODE.ISSUES | terminal | 70 | terminal | none | none | stop | BalanceCode input is missing or a read-only lookup did not return a result |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | BALPROFILE.LIST.RESULTS | terminal | 30 | terminal | none | BALPROFILE.LIST | stop | The collection lookup returned one or more balance-profile rows |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | BALPROFILE.LIST.EMPTY | terminal | 40 | terminal | none | BALPROFILE.LIST | stop | The collection lookup returned an empty result set |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | BALPROFILE.SUCCESS | terminal | 70 | terminal | none | BALPROFILE.GROUP_CRITERIA | stop | The item lookup returned one balance-profile record and its requested grouping criteria |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | BALPROFILE.ISSUES | terminal | 80 | terminal | none | none | stop | A balance-profile input is missing or the lookup did not return a record |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | USAGEENT.LIST.RESULTS | terminal | 30 | terminal | none | USAGEENT.LIST | stop | The collection lookup returned one or more usage-entitlement rows |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | USAGEENT.LIST.EMPTY | terminal | 40 | terminal | none | USAGEENT.LIST | stop | The collection lookup returned an empty result set |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | ENTPLAN.SUCCESS | terminal | 55 | terminal | none | ENTPLAN.LOOKUP | stop | The item lookup returned one entitlement-plan record with its number and status |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | ENTASSIGN.SUCCESS | terminal | 56 | terminal | none | ENTASSIGN.LOOKUP | stop | The item lookup returned one entitlement-assignment record with its number and status |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | USAGEENT.PLAN.LIST.RESULTS | terminal | 57 | terminal | none | USAGEENT.PLAN.LIST | stop | The subscriptionUsageEntitlements collection returned one or more entitlement-plan rows and final pagination metadata |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | USAGEENT.PLAN.LIST.EMPTY | terminal | 58 | terminal | none | USAGEENT.PLAN.LIST | stop | The subscriptionUsageEntitlements collection returned an empty entitlement-plan result set |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | ENTPLAN.LIST.EMPTY | terminal | 59 | terminal | none | ENTPLAN.LIST | stop | The fallback subscriptionEntitlementPlans collection returned an empty result set |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | ENTPLAN.LIST.RESULTS | terminal | 60 | terminal | none | ENTPLAN.COMBINE | stop | The fallback plan and assignment collections were combined by exact EntitlementPlanNumber |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | ENTASSIGN.LIST.RESULTS | terminal | 61 | terminal | none | ENTASSIGN.LIST | stop | The collection lookup returned one or more entitlement-assignment rows and final pagination metadata |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | ENTASSIGN.LIST.EMPTY | terminal | 62 | terminal | none | ENTASSIGN.LIST | stop | The collection lookup returned an empty entitlement-assignment result set |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | USAGEENT.SUCCESS | terminal | 63 | terminal | none | USAGEENT.LOOKUP | stop | The item lookup returned one usage-entitlement record |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | ENTPLAN.ISSUES | terminal | 65 | terminal | none | none | stop | An entitlement-plan input is missing, the item lookup did not return an exact record, or its status cannot support the requested action |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | ENTASSIGN.ISSUES | terminal | 66 | terminal | none | none | stop | An entitlement-assignment input is missing, the item lookup did not return an exact record, or its status cannot support the requested action |
| CUSTOM_MANAGE_USAGE_ENTITLEMENT | Manage Usage Entitlement | USAGEENT.ISSUES | terminal | 70 | terminal | none | none | stop | A usage-entitlement input is missing or the lookup did not return a record |
