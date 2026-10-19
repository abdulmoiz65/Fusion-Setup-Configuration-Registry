# Organization Structures Design Advisory

## Guidance Sources

| Task Code | Task Name | Source Mode | Allowed Sources | When Used |
|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Oracle implementation guidance and data model | Oracle Financials implementation guide; Oracle data-model references cited below | Explain Business Unit and reference-data-set choices |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Oracle implementation guidance and data model | Oracle Financials implementation guide; Oracle data-model references cited below | Explain function, primary-ledger, and legal-entity choices |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Oracle implementation guidance and data model | Oracle Financials implementation guide; Oracle data-model references cited below | Explain client/provider relationships |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Oracle implementation guidance | Oracle Financials implementation guide | Explain reference-data-object assignments |

## Guidance Topics

| Task Code | Task Name | Topic | Advisory Level | What To Explain | Do Not Include |
|---|---|---|---|---|---|
| FUN_MANAGE_BUSINESS_UNIT | Manage Business Unit | Business Unit purpose | Advisory | A Business Unit performs one or more functions, supports management hierarchy, and can process transactions for many legal entities | A claim that a database ID must be manually entered |
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | Ledger terminology | Advisory | A Business Unit uses one primary ledger for transactions; primary ledgers can have reporting currencies and secondary ledgers for reporting options | Do not treat a secondary ledger or reporting currency as the assigned primary ledger |
| FUN_MANAGE_SERVICE_PROVIDER_RELATIONSHIPS | Manage Service Provider Relationships | Shared-service model | Advisory | A service-provider model identifies one Business Unit as provider and another as client for a business function | Unsupported endpoint, CSV, or payload instructions |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | Reference-data sharing | Advisory | The default set is assigned to reference data objects initially; individual assignments can be changed | A recommendation to alter an assignment after transactions without considering lifecycle effects |

## Output Rules

| Task Code | Task Name | Situation | What Happens |
|---|---|---|---|
| FUN_ASSIGN_BUSINESS_UNIT_BUSINESS_FUNCTION | Assign Business Unit Business Function | A user asks whether to use a secondary ledger or reporting currency as the primary ledger | State that these are distinct accounting constructs; request the actual primary ledger |
| FUN_MANAGE_BUSINESS_UNIT_SET_ASSIGNMENT | Manage Business Unit Set Assignment | A user asks whether assignment is optional | State that Oracle guidance requires saving the task even if default assignments remain unchanged |
