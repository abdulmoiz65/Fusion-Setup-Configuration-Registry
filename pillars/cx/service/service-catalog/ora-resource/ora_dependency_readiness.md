# Dependency Readiness

## Required Dependency Order

| Task Code | Task Name | Sequence | Dependency | What Must Happen |
|---|---|---:|---|---|
| QSC_MANAGE_PRODUCT_GROUPS | Manage Product Groups | 1 | Product-group lock | Lock the product group and wait for the response before publishing it. |

## Dependency Rules

| Task Code | Task Name | Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|---|---|
| QSC_MANAGE_PRODUCT_GROUPS | Manage Product Groups | product_group_lock_before_publish | Product-group lock | Yes | Publish is requested | Verify | Read-only product-group identity response and completed lock response | resolve_product_group_identity | Oracle documents that a product group must be locked before publishing. | Provide the exact target identity, complete the lock operation, and wait for its response before requesting publish. | ProdGroupId, ProductGroupLockedFlag |

## Dependency Classification

| Task Code | Task Name | Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|---|---|
| QSC_MANAGE_PRODUCT_GROUPS | Manage Product Groups | Blocked | The required lock is absent, unresolved, or its response has not completed | No |
| QSC_MANAGE_PRODUCT_GROUPS | Manage Product Groups | Satisfied | The resolved product group is locked by the initiating user and the lock response completed | Yes |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---:|---|---|---|---|---|---|
| QSC_MANAGE_PRODUCT_GROUPS | Manage Product Groups | MPG.LOCK_REQUIRED | step | 5 | resolve_dependency | satisfied->MPG.EXECUTION_GATE;blocked->MPG.BLOCKED;failure->MPG.FAILED | MPG.VALIDATE_REQUEST | stop | Publish is requested. |
