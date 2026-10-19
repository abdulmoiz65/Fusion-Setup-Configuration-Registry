# AutoInvoice Grouping Rule Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver | Source IDs |
|---|---|---|---|---|---|

No FSM import default is established for this task.

## Explicit Inputs and Unresolved Defaults

| Field | Requirement | Applies When | Override User Value? | Resolver | Source IDs |
|---|---|---|---|---|---|
| StartDate | No FSM import default established; supply an explicit date | Create | No | | SRC-CODE-PRIMARY-EO, SRC-CODE-PRIMARY-VO |
| Class11 | No default; choose one of C, D or I | Class child present | No | resolve_grouping_transaction_class | SRC-CODE-CLASS-SEED, SRC-CODE-CLASS-EDIT-UIVO |
| FromColumnName | No default; supply an exact target-pod characteristic | Group-by child present | No | resolve_grouping_column_name | SRC-CODE-AMIMPL, SRC-CODE-GROUPBY-COLUMN-VO |

The Create UI's date prefill is not evidence of an FSM CSV import default. This file declares no executable defaulting node.
