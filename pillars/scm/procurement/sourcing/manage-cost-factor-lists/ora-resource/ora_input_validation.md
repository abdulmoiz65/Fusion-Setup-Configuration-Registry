# Manage Cost Factor Lists Input Validation

Sources: Oracle Fusion Cloud Procurement 26C, Cost Factors and Cost Factor Lists, accessed 2026-09-23; user-provided Cost Factor List Data Loader creation and update contracts on 2026-09-24.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Data Loader parent-child create | One Cost Factor List parent row and one or more Cost Factor child rows | Reject the source before preview | Include the selected Cost Factor child rows in the same Data Loader source as the new list parent. | Creating a Cost Factor List through Data Loader | |
| Existing-list Cost Factor add | Existing ListId and one or more Cost Factor child rows with RestAction POST; no parent row | Reject the source before preview | Use the existing ListId in each child row and omit the Cost Factor List parent row. | Adding Cost Factors to an existing Cost Factor List | |
| Existing-list Cost Factor update | Existing ListId, ListCostFactorId, one or more Cost Factor child rows with RestAction PATCH, and the requested mutable Cost Factor values; no parent row | Reject the source before preview | Retrieve the existing child identity, use its ListId and ListCostFactorId, and submit only the child PATCH rows. | Updating Cost Factors in an existing Cost Factor List | |
| Existing-list Cost Factor delete | Existing ListId, ListCostFactorId, and one or more Cost Factor child rows with RestAction DELETE; no parent row | Reject the source before preview | Retrieve the existing child row identity, use its ListId and ListCostFactorId, and omit the Cost Factor List parent row. | Deleting Cost Factors from an existing Cost Factor List | |
| Existing Cost Factor List update | Existing ListId, parent RestAction PATCH, and one or more of ListName, Description, ListStatus, or ListStatusCode; no Cost Factor child rows | Reject the source before preview | Submit only the identified parent row with the requested mutable field values. | Updating an existing Cost Factor List through Data Loader | |
| Cost Factor List delete cascade | Existing ListId parent row with RestAction DELETE and DELETE rows for every current child Cost Factor, each with ListId and ListCostFactorId | Reject the source before preview | Retrieve every current child row, include a DELETE row for each, and include the parent DELETE row. | Deleting an existing Cost Factor List | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Generated ListId | Do not supply ListId for a new list. Data Loader generates the ListId and uses the generated value for the parent and its child Cost Factor rows. | Creating a Cost Factor List through Data Loader | |
| Existing-list child POST | Do not send a parent PATCH when the requested operation only adds Cost Factor child rows. | Adding Cost Factors to an existing Cost Factor List | |
| Existing-list child PATCH | Do not send a parent row when the requested operation updates Cost Factor child rows. | Updating Cost Factors in an existing Cost Factor List | |
| Existing-list child DELETE | Do not send a parent row when the requested operation deletes Cost Factor child rows. | Deleting Cost Factors from an existing Cost Factor List | |
| Existing Cost Factor List update fields | Allow only ListName, Description, ListStatus, and ListStatusCode as mutable parent values. Do not include Cost Factor child rows. | Updating an existing Cost Factor List through Data Loader | |
| Cost Factor List cascade delete | Delete the parent list and every current child Cost Factor in the same source; do not omit any discovered child row. | Deleting an existing Cost Factor List | |

## Delegated Resource Validation

Fusion REST validates the Cost Factor List classification, application scope, and cost-factor relationship. Do not request or enforce those values in this task's local validation.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COST_FACTOR_LIST.CLASSIFY_REQUEST | decision | 5 | evaluate_result | list_setup->COST_FACTOR_LIST.VALIDATE_LIST_CONTEXT;unsupported->RETURN_ISSUES | none | stop | A Manage Cost Factor Lists request is received. |
| COST_FACTOR_LIST.VALIDATE_LIST_CONTEXT | step | 10 | validate_input | valid->COST_FACTOR_LIST.RETURN_VALIDATED_CREATE_SOURCE;invalid->RETURN_ISSUES | COST_FACTOR_LIST.CLASSIFY_REQUEST | stop | A source either creates a Cost Factor List with parent and child rows and no generated ListId, adds child POST rows to an existing ListId without a parent row, updates child rows using existing ListId, ListCostFactorId, and RestAction PATCH without a parent row, updates one existing Cost Factor List parent using RestAction PATCH and ListName, Description, ListStatus, or ListStatusCode without child rows, deletes child rows using existing ListId and ListCostFactorId values without a parent row, or deletes a list with its parent DELETE row and every current child DELETE row. |
