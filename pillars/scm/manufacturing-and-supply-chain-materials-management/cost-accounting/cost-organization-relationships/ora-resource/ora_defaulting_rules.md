# Defaulting Rules

## Source

| Source | Location | Used For |
|---|---|---|
| Oracle Create Cost Organization Relationships | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/create-cost-organization-relationships.html | End-date, ledger, periodic-average-cost, and period-end-validation defaults |
| Oracle Important Points to Know Before Creating Cost Organization Relationships | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/important-points-to-know-before-creating-cost-organization-relationships.html | Effective-end-date behavior |
| Reference Data Set Object LOV lookup | /fscmRestApi/resources/11.13.18.05/referenceDataSetObjectsLOV | Reference group and determinant values |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Inventory Organization Effective End Date | 12/31/12 with year 4712 | The relationship is saved without an effective end date | Yes | |
| Cost Book Currency | Ledger currency | A Ledger is selected for the Cost Book association | No | |
| Cost Book Accounting Calendar | Ledger accounting calendar | A Ledger is selected for the Cost Book association | No | |
| Periodic Average Cost indicator | Selected | The selected Cost Book is periodic average cost enabled | No | |
| Primary Cost Book indicator | Selected | The selected Ledger is the primary Ledger | No | |
| Maximum Open Periods | 1 | The Cost Book is periodic average cost enabled | No | |
| Create Accounting | Selected | The selected Ledger is the primary Ledger | No | |
| Create Accounting | Selected | The selected Ledger is a secondary Ledger | Yes | |
| Period End Validation State | ERROR | A period-end validation is selected | Yes | resolve_period_validation_state |
| ReferenceGroupName | Resolved ReferenceGroupName | Creating or updating a Cost Organization Relationship | Yes | resolve_reference_data_set_object |
| DeterminantType | Resolved DeterminantType | Creating or updating a Cost Organization Relationship | Yes | resolve_reference_data_set_object |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COR.APPLY_DEFAULTS | step | 16 | apply_default | applied->COR.ENFORCE_DESIGN | COR.RESOLVE_REFERENCE_DATA_SET_OBJECT | stop | Creating or updating Cost Organization Relationships |
