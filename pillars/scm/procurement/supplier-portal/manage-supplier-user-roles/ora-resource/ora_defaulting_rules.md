# Manage Supplier User Roles Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Allow supplier provision flag | True | The role code is ORA_POS_SUPPLIER_ACCOUNTS_RECEIVABLE_SPECIALIST_JOB, ORA_POS_SUPPLIER_CUSTOMER_SERVICE_REPRESENTATIVE_JOB, ORA_INV_SUPPLIER_INVENTORY_MANAGER_JOB, ORA_POS_SUPPLIER_SALES_REPRESENTATIVE_JOB, or ORA_PON_SUPPLIER_BIDDER_ABSTRACT. | No |  |
| Allow supplier provision flag | False | The role code is ORA_POS_SUPPLIER_SELF_SERVICE_ADMINISTRATOR_ABSTRACT. | No |  |
| Default for Supplier Portal flag | True | The role code is ORA_POS_SUPPLIER_ACCOUNTS_RECEIVABLE_SPECIALIST_JOB, ORA_POS_SUPPLIER_CUSTOMER_SERVICE_REPRESENTATIVE_JOB, ORA_INV_SUPPLIER_INVENTORY_MANAGER_JOB, ORA_POS_SUPPLIER_SALES_REPRESENTATIVE_JOB, or ORA_POS_SUPPLIER_SELF_SERVICE_ADMINISTRATOR_ABSTRACT. | No |  |
| Default for Supplier Portal flag | False | The role code is ORA_PON_SUPPLIER_BIDDER_ABSTRACT. | No |  |
| Default for Sourcing flag | True | The role code is ORA_PON_SUPPLIER_BIDDER_ABSTRACT. | No |  |
| Default for Sourcing flag | False | The role code is ORA_POS_SUPPLIER_ACCOUNTS_RECEIVABLE_SPECIALIST_JOB, ORA_POS_SUPPLIER_CUSTOMER_SERVICE_REPRESENTATIVE_JOB, ORA_INV_SUPPLIER_INVENTORY_MANAGER_JOB, ORA_POS_SUPPLIER_SALES_REPRESENTATIVE_JOB, or ORA_POS_SUPPLIER_SELF_SERVICE_ADMINISTRATOR_ABSTRACT. | No |  |

## Initial Empty-Configuration Defaults

| Supplier User Role | Allow Supplier Provision Flag | Default for Supplier Portal Flag | Default for Sourcing Flag | Applies When | Override User Value? |
|---|---|---|---|---|---|
| Supplier Accounts Receivable Specialist | True | True | False | The Supplier User Roles configuration contains no existing roles. | No |
| Supplier Customer Service Representative | True | True | False | The Supplier User Roles configuration contains no existing roles. | No |
| Supplier Inventory Manager | True | True | False | The Supplier User Roles configuration contains no existing roles. | No |
| Supplier Sales Representative | True | True | False | The Supplier User Roles configuration contains no existing roles. | No |
| Supplier Bidder | True | False | True | The Supplier User Roles configuration contains no existing roles. | No |
| Supplier Self Service Administrator | False | True | False | The Supplier User Roles configuration contains no existing roles. | No |

## Initial Configuration Boundary

| Situation | What Happens |
|---|---|
| The Supplier User Roles configuration contains no existing roles. | The documented initial default role set may be applied. |
| One or more Supplier User Role records already exist. | Do not add, remove, or overwrite roles by using the initial default role set. |
| Any role outside the documented initial default role set is requested. | Do not apply a default; only the predefined roles and values in the Initial Empty-Configuration Defaults table may be defaulted. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SUR.APPLY_ROLE_DEFAULTS | step | 30 | apply_default | applied->POZ.SUR.ENFORCE_ROLE_POLICY;not_applicable->POZ.SUR.ENFORCE_ROLE_POLICY;failure->POZ.SUR.RETURN_ISSUES | POZ.SUR.CHECK_DEPENDENCIES | stop | An empty Supplier User Roles configuration is initialized without explicit role defaults. |
